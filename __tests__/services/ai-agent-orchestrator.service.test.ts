/**
 * AI Agent Orchestrator Service Tests
 *
 * Tests AI model routing, multi-model aggregation, and error recovery.
 */

import { AIAgentOrchestratorService } from '../../src/services/ai-agent-orchestrator.service';
import { ErrorRecoveryService } from '../../src/services/error-recovery.service';
import { QuotaService } from '../../src/services/quota.service';
import { createClient } from '@supabase/supabase-js';
import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';
import { GoogleGenerativeAI } from '@google/generative-ai';

jest.mock('openai');
jest.mock('@anthropic-ai/sdk');
jest.mock('@google/generative-ai');
jest.mock('@supabase/supabase-js');
jest.mock('../../src/services/error-recovery.service');
jest.mock('../../src/services/quota.service');

describe('AIAgentOrchestratorService', () => {
  let service: AIAgentOrchestratorService;
  let mockOpenAI: any;
  let mockAnthropic: any;
  let mockGoogle: any;
  let mockSupabase: any;
  let mockErrorRecovery: any;
  let mockQuotaService: any;

  const mockUserId = 'user-123';
  const mockProjectId = 'proj-456';

  beforeEach(() => {
    // Mock OpenAI
    mockOpenAI = {
      chat: {
        completions: {
          create: jest.fn(),
        },
      },
    };
    (OpenAI as jest.Mock).mockImplementation(() => mockOpenAI);

    // Mock Anthropic
    mockAnthropic = {
      messages: {
        create: jest.fn(),
      },
    };
    (Anthropic as jest.Mock).mockImplementation(() => mockAnthropic);

    // Mock Google
    const mockGeminiModel = {
      generateContent: jest.fn(),
      generateContentStream: jest.fn(),
    };
    mockGoogle = {
      getGenerativeModel: jest.fn(() => mockGeminiModel),
    };
    (GoogleGenerativeAI as jest.Mock).mockImplementation(() => mockGoogle);

    // Mock Supabase
    mockSupabase = {
      from: jest.fn(() => mockSupabase),
      insert: jest.fn(() => mockSupabase),
      select: jest.fn(() => mockSupabase),
    };
    (createClient as jest.Mock).mockReturnValue(mockSupabase);

    // Mock ErrorRecoveryService
    mockErrorRecovery = {
      executeWithCircuitBreaker: jest.fn((key, fn, config) => fn()),
      retryWithBackoff: jest.fn((fn, options) => fn()),
    };
    (ErrorRecoveryService.getInstance as jest.Mock).mockReturnValue(mockErrorRecovery);

    // Mock QuotaService
    mockQuotaService = {
      checkQuota: jest.fn().mockResolvedValue({
        allowed: true,
        current_usage: 10000,
        limit: 100000,
      }),
      incrementUsage: jest.fn().mockResolvedValue(undefined),
    };
    (QuotaService.getInstance as jest.Mock).mockReturnValue(mockQuotaService);

    service = AIAgentOrchestratorService.getInstance();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Model Selection', () => {
    it('should use explicitly specified model', async () => {
      const mockResponse = {
        choices: [
          {
            message: { content: 'Test response' },
            finish_reason: 'stop',
          },
        ],
        usage: {
          prompt_tokens: 10,
          completion_tokens: 20,
          total_tokens: 30,
        },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const result = await service.execute({
        taskType: 'general',
        model: 'gpt-4',
        prompt: 'Test prompt',
        userId: mockUserId,
      });

      expect(result.model).toBe('gpt-4');
      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith(
        expect.objectContaining({ model: 'gpt-4' })
      );
    });

    it('should auto-select Claude for problem_deconstruction', async () => {
      const mockResponse = {
        id: 'msg-123',
        content: [{ type: 'text', text: 'Deconstructed problem' }],
        usage: {
          input_tokens: 10,
          output_tokens: 20,
        },
        stop_reason: 'end_turn',
      };

      mockAnthropic.messages.create.mockResolvedValue(mockResponse);

      const result = await service.execute({
        taskType: 'problem_deconstruction',
        prompt: 'Deconstruct this idea',
        userId: mockUserId,
      });

      expect(result.model).toBe('claude-3-5-sonnet');
      expect(mockAnthropic.messages.create).toHaveBeenCalledWith(
        expect.objectContaining({ model: 'claude-3-5-sonnet' })
      );
    });

    it('should auto-select GPT-4 Turbo for code_generation', async () => {
      const mockResponse = {
        choices: [
          {
            message: { content: 'Generated code' },
            finish_reason: 'stop',
          },
        ],
        usage: {
          prompt_tokens: 100,
          completion_tokens: 500,
          total_tokens: 600,
        },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const result = await service.execute({
        taskType: 'code_generation',
        prompt: 'Generate React component',
        userId: mockUserId,
      });

      expect(result.model).toBe('gpt-4-turbo');
    });

    it('should auto-select Gemini Pro for design_generation', async () => {
      const mockResult = {
        response: {
          text: () => 'Design specification',
        },
      };

      mockGoogle.getGenerativeModel().generateContent.mockResolvedValue(mockResult);

      const result = await service.execute({
        taskType: 'design_generation',
        prompt: 'Generate design',
        userId: mockUserId,
      });

      expect(result.model).toBe('gemini-1.5-pro');
    });
  });

  describe('OpenAI Integration', () => {
    it('should execute OpenAI request successfully', async () => {
      const mockResponse = {
        choices: [
          {
            message: { content: 'AI response' },
            finish_reason: 'stop',
          },
        ],
        usage: {
          prompt_tokens: 50,
          completion_tokens: 100,
          total_tokens: 150,
        },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      const result = await service.execute({
        taskType: 'general',
        model: 'gpt-3.5-turbo',
        prompt: 'Test prompt',
        systemPrompt: 'You are a helpful assistant',
        temperature: 0.5,
        maxTokens: 1000,
        userId: mockUserId,
        projectId: mockProjectId,
      });

      expect(result.content).toBe('AI response');
      expect(result.tokensUsed.total).toBe(150);
      expect(result.finishReason).toBe('stop');
      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
        model: 'gpt-3.5-turbo',
        messages: [
          { role: 'system', content: 'You are a helpful assistant' },
          { role: 'user', content: 'Test prompt' },
        ],
        temperature: 0.5,
        max_tokens: 1000,
      });
    });

    it('should handle OpenAI request without system prompt', async () => {
      const mockResponse = {
        choices: [{ message: { content: 'Response' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 10, completion_tokens: 20, total_tokens: 30 },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await service.execute({
        taskType: 'general',
        model: 'gpt-3.5-turbo',
        prompt: 'Test',
        userId: mockUserId,
      });

      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith(
        expect.objectContaining({
          messages: [{ role: 'user', content: 'Test' }],
        })
      );
    });
  });

  describe('Anthropic Integration', () => {
    it('should execute Anthropic request successfully', async () => {
      const mockResponse = {
        id: 'msg-123',
        content: [{ type: 'text', text: 'Claude response' }],
        usage: {
          input_tokens: 25,
          output_tokens: 75,
        },
        stop_reason: 'end_turn',
      };

      mockAnthropic.messages.create.mockResolvedValue(mockResponse);

      const result = await service.execute({
        taskType: 'code_review',
        model: 'claude-3-5-sonnet',
        prompt: 'Review this code',
        systemPrompt: 'You are an expert code reviewer',
        temperature: 0.3,
        userId: mockUserId,
      });

      expect(result.content).toBe('Claude response');
      expect(result.tokensUsed.prompt).toBe(25);
      expect(result.tokensUsed.completion).toBe(75);
      expect(result.tokensUsed.total).toBe(100);
      expect(result.finishReason).toBe('stop');
      expect(mockAnthropic.messages.create).toHaveBeenCalledWith({
        model: 'claude-3-5-sonnet',
        max_tokens: 2000,
        system: 'You are an expert code reviewer',
        messages: [{ role: 'user', content: 'Review this code' }],
        temperature: 0.3,
      });
    });
  });

  describe('Google Gemini Integration', () => {
    it('should execute Gemini request successfully', async () => {
      const mockResult = {
        response: {
          text: () => 'Gemini response',
        },
      };

      mockGoogle.getGenerativeModel().generateContent.mockResolvedValue(mockResult);

      const result = await service.execute({
        taskType: 'design_generation',
        model: 'gemini-1.5-flash',
        prompt: 'Generate design tokens',
        userId: mockUserId,
      });

      expect(result.content).toBe('Gemini response');
      expect(result.model).toBe('gemini-1.5-flash');
      expect(result.tokensUsed.total).toBeGreaterThan(0);
    });
  });

  describe('Quota Checking', () => {
    it('should check quota before execution', async () => {
      const mockResponse = {
        choices: [{ message: { content: 'OK' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 10, completion_tokens: 10, total_tokens: 20 },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await service.execute({
        taskType: 'general',
        model: 'gpt-3.5-turbo',
        prompt: 'Test',
        userId: mockUserId,
      });

      expect(mockQuotaService.checkQuota).toHaveBeenCalledWith(mockUserId, 'tokens');
    });

    it('should reject request if quota exceeded', async () => {
      mockQuotaService.checkQuota.mockResolvedValue({
        allowed: false,
        reason: 'Monthly token limit exceeded',
        current_usage: 100000,
        limit: 100000,
      });

      await expect(
        service.execute({
          taskType: 'general',
          model: 'gpt-3.5-turbo',
          prompt: 'Test',
          userId: mockUserId,
        })
      ).rejects.toThrow('Monthly token limit exceeded');
    });

    it('should increment usage after successful execution', async () => {
      const mockResponse = {
        choices: [{ message: { content: 'OK' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 50, completion_tokens: 100, total_tokens: 150 },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await service.execute({
        taskType: 'general',
        model: 'gpt-3.5-turbo',
        prompt: 'Test',
        userId: mockUserId,
      });

      expect(mockQuotaService.incrementUsage).toHaveBeenCalledWith(
        mockUserId,
        'tokens',
        150
      );
    });

    it('should skip quota check if no user ID provided', async () => {
      const mockResponse = {
        choices: [{ message: { content: 'OK' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 10, completion_tokens: 10, total_tokens: 20 },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await service.execute({
        taskType: 'general',
        model: 'gpt-3.5-turbo',
        prompt: 'Test',
      });

      expect(mockQuotaService.checkQuota).not.toHaveBeenCalled();
      expect(mockQuotaService.incrementUsage).not.toHaveBeenCalled();
    });
  });

  describe('Error Recovery', () => {
    it('should use circuit breaker for requests', async () => {
      const mockResponse = {
        choices: [{ message: { content: 'OK' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 10, completion_tokens: 10, total_tokens: 20 },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await service.execute({
        taskType: 'general',
        model: 'gpt-3.5-turbo',
        prompt: 'Test',
        userId: mockUserId,
      });

      expect(mockErrorRecovery.executeWithCircuitBreaker).toHaveBeenCalledWith(
        'ai-gpt-3.5-turbo',
        expect.any(Function),
        expect.objectContaining({
          failureThreshold: 5,
          resetTimeout: 60000,
        })
      );
    });

    it('should retry failed requests with backoff', async () => {
      const mockResponse = {
        choices: [{ message: { content: 'OK' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 10, completion_tokens: 10, total_tokens: 20 },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await service.execute({
        taskType: 'general',
        model: 'gpt-3.5-turbo',
        prompt: 'Test',
        userId: mockUserId,
      });

      expect(mockErrorRecovery.retryWithBackoff).toHaveBeenCalledWith(
        expect.any(Function),
        expect.objectContaining({
          maxAttempts: 3,
          initialDelay: 1000,
          maxDelay: 10000,
        })
      );
    });
  });

  describe('Multi-Model Execution', () => {
    beforeEach(() => {
      const mockOpenAIResponse = {
        choices: [{ message: { content: 'GPT response' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 10, completion_tokens: 20, total_tokens: 30 },
      };

      const mockClaudeResponse = {
        content: [{ type: 'text', text: 'Claude response' }],
        usage: { input_tokens: 10, output_tokens: 20 },
        stop_reason: 'end_turn',
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockOpenAIResponse);
      mockAnthropic.messages.create.mockResolvedValue(mockClaudeResponse);
    });

    it('should execute multiple models and return first response', async () => {
      const result = await service.executeMultiModel({
        requests: [
          { taskType: 'general', model: 'gpt-3.5-turbo', prompt: 'Test' },
          { taskType: 'general', model: 'claude-3-5-sonnet', prompt: 'Test' },
        ],
        aggregationStrategy: 'first',
      });

      expect(result.responses).toHaveLength(2);
      expect(result.aggregatedContent).toBe('GPT response');
      expect(result.strategy).toBe('first');
    });

    it('should execute multiple models and select best response', async () => {
      const result = await service.executeMultiModel({
        requests: [
          { taskType: 'general', model: 'gpt-3.5-turbo', prompt: 'Test' },
          { taskType: 'general', model: 'claude-3-5-sonnet', prompt: 'Test' },
        ],
        aggregationStrategy: 'best',
      });

      expect(result.responses).toHaveLength(2);
      // Both responses complete successfully, so pick longer one
      expect(result.aggregatedContent).toContain('response');
    });

    it('should execute multiple models and combine all responses', async () => {
      const result = await service.executeMultiModel({
        requests: [
          { taskType: 'general', model: 'gpt-3.5-turbo', prompt: 'Test' },
          { taskType: 'general', model: 'claude-3-5-sonnet', prompt: 'Test' },
        ],
        aggregationStrategy: 'all',
      });

      expect(result.aggregatedContent).toContain('GPT response');
      expect(result.aggregatedContent).toContain('Claude response');
      expect(result.aggregatedContent).toContain('---');
    });
  });

  describe('Request Logging', () => {
    it('should log successful requests to database', async () => {
      const mockResponse = {
        choices: [{ message: { content: 'OK' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 25, completion_tokens: 50, total_tokens: 75 },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);

      await service.execute({
        taskType: 'code_generation',
        model: 'gpt-4-turbo',
        prompt: 'Test',
        userId: mockUserId,
        projectId: mockProjectId,
      });

      expect(mockSupabase.from).toHaveBeenCalledWith('ai_requests');
      expect(mockSupabase.insert).toHaveBeenCalledWith(
        expect.objectContaining({
          user_id: mockUserId,
          project_id: mockProjectId,
          task_type: 'code_generation',
          model: 'gpt-4-turbo',
          prompt_tokens: 25,
          completion_tokens: 50,
          total_tokens: 75,
          finish_reason: 'stop',
        })
      );
    });

    it('should not fail execution if logging fails', async () => {
      const mockResponse = {
        choices: [{ message: { content: 'OK' }, finish_reason: 'stop' }],
        usage: { prompt_tokens: 10, completion_tokens: 10, total_tokens: 20 },
      };

      mockOpenAI.chat.completions.create.mockResolvedValue(mockResponse);
      mockSupabase.insert.mockRejectedValue(new Error('Database error'));

      const result = await service.execute({
        taskType: 'general',
        model: 'gpt-3.5-turbo',
        prompt: 'Test',
        userId: mockUserId,
      });

      expect(result.content).toBe('OK');
    });
  });
});
