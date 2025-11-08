/**
 * AI Agent Orchestrator Service
 *
 * Routes AI requests to appropriate models and orchestrates multi-model workflows.
 *
 * Supported Models:
 * - OpenAI (GPT-4, GPT-4 Turbo, GPT-3.5 Turbo)
 * - Anthropic Claude (Claude 3.5 Sonnet, Claude 3 Opus)
 * - Google Gemini (Gemini 1.5 Pro, Gemini 1.5 Flash)
 *
 * Features:
 * - Model selection based on task complexity and cost
 * - Streaming response support for real-time UX
 * - Multi-model aggregation (e.g., generate with GPT-4, validate with Claude)
 * - Token usage tracking for quota enforcement
 * - Error recovery with automatic fallback models
 */

import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { ErrorRecoveryService } from './error-recovery.service';
import { QuotaService } from './quota.service';

export type AIModel =
  | 'gpt-4'
  | 'gpt-4-turbo'
  | 'gpt-3.5-turbo'
  | 'claude-3-5-sonnet'
  | 'claude-3-opus'
  | 'gemini-1.5-pro'
  | 'gemini-1.5-flash';

export type AITaskType =
  | 'problem_deconstruction'
  | 'screen_mapping'
  | 'design_generation'
  | 'code_generation'
  | 'code_review'
  | 'general';

export interface AIRequest {
  taskType: AITaskType;
  model?: AIModel; // Optional: auto-select if not specified
  prompt: string;
  systemPrompt?: string;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
  userId?: string;
  projectId?: string;
}

export interface AIResponse {
  content: string;
  model: AIModel;
  tokensUsed: {
    prompt: number;
    completion: number;
    total: number;
  };
  latencyMs: number;
  finishReason: 'stop' | 'length' | 'content_filter' | 'error';
}

export interface StreamChunk {
  delta: string;
  done: boolean;
}

export interface MultiModelRequest {
  requests: AIRequest[];
  aggregationStrategy: 'first' | 'best' | 'consensus' | 'all';
}

export interface MultiModelResponse {
  responses: AIResponse[];
  aggregatedContent?: string;
  strategy: string;
}

/**
 * Model capabilities and cost tiers
 */
const MODEL_CONFIG: Record<
  AIModel,
  {
    provider: 'openai' | 'anthropic' | 'google';
    costPer1kTokens: { prompt: number; completion: number };
    maxTokens: number;
    capabilities: AITaskType[];
    fallbackModel?: AIModel;
  }
> = {
  'gpt-4': {
    provider: 'openai',
    costPer1kTokens: { prompt: 0.03, completion: 0.06 },
    maxTokens: 8192,
    capabilities: [
      'problem_deconstruction',
      'screen_mapping',
      'design_generation',
      'code_generation',
      'code_review',
      'general',
    ],
    fallbackModel: 'gpt-3.5-turbo',
  },
  'gpt-4-turbo': {
    provider: 'openai',
    costPer1kTokens: { prompt: 0.01, completion: 0.03 },
    maxTokens: 128000,
    capabilities: [
      'problem_deconstruction',
      'screen_mapping',
      'design_generation',
      'code_generation',
      'code_review',
      'general',
    ],
    fallbackModel: 'gpt-3.5-turbo',
  },
  'gpt-3.5-turbo': {
    provider: 'openai',
    costPer1kTokens: { prompt: 0.0005, completion: 0.0015 },
    maxTokens: 16385,
    capabilities: ['screen_mapping', 'code_review', 'general'],
    fallbackModel: 'gemini-1.5-flash',
  },
  'claude-3-5-sonnet': {
    provider: 'anthropic',
    costPer1kTokens: { prompt: 0.003, completion: 0.015 },
    maxTokens: 200000,
    capabilities: [
      'problem_deconstruction',
      'screen_mapping',
      'design_generation',
      'code_generation',
      'code_review',
      'general',
    ],
    fallbackModel: 'gpt-4-turbo',
  },
  'claude-3-opus': {
    provider: 'anthropic',
    costPer1kTokens: { prompt: 0.015, completion: 0.075 },
    maxTokens: 200000,
    capabilities: [
      'problem_deconstruction',
      'design_generation',
      'code_generation',
      'code_review',
      'general',
    ],
    fallbackModel: 'claude-3-5-sonnet',
  },
  'gemini-1.5-pro': {
    provider: 'google',
    costPer1kTokens: { prompt: 0.00125, completion: 0.005 },
    maxTokens: 2097152,
    capabilities: [
      'problem_deconstruction',
      'screen_mapping',
      'design_generation',
      'code_generation',
      'code_review',
      'general',
    ],
    fallbackModel: 'gemini-1.5-flash',
  },
  'gemini-1.5-flash': {
    provider: 'google',
    costPer1kTokens: { prompt: 0.000125, completion: 0.0005 },
    maxTokens: 1048576,
    capabilities: ['screen_mapping', 'code_review', 'general'],
  },
};

/**
 * Default model selection per task type
 */
const DEFAULT_MODEL_PER_TASK: Record<AITaskType, AIModel> = {
  problem_deconstruction: 'claude-3-5-sonnet', // Best at structured reasoning
  screen_mapping: 'gpt-4-turbo', // Good at spatial/visual reasoning
  design_generation: 'gemini-1.5-pro', // Handles large multimodal context
  code_generation: 'gpt-4-turbo', // Strong at code
  code_review: 'claude-3-5-sonnet', // Excellent at analysis
  general: 'gpt-3.5-turbo', // Fast and cheap for simple tasks
};

export class AIAgentOrchestratorService {
  private static instance: AIAgentOrchestratorService;
  private openaiClient: OpenAI;
  private anthropicClient: Anthropic;
  private googleClient: GoogleGenerativeAI;
  private supabaseClient: SupabaseClient;
  private errorRecovery: ErrorRecoveryService;
  private quotaService: QuotaService;

  private constructor() {
    this.openaiClient = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY || '',
    });

    this.anthropicClient = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY || '',
    });

    this.googleClient = new GoogleGenerativeAI(
      process.env.GOOGLE_API_KEY || ''
    );

    const supabaseUrl = process.env.SUPABASE_URL || '';
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || '';
    this.supabaseClient = createClient(supabaseUrl, supabaseKey);

    this.errorRecovery = ErrorRecoveryService.getInstance();
    this.quotaService = QuotaService.getInstance();
  }

  public static getInstance(): AIAgentOrchestratorService {
    if (!AIAgentOrchestratorService.instance) {
      AIAgentOrchestratorService.instance = new AIAgentOrchestratorService();
    }
    return AIAgentOrchestratorService.instance;
  }

  /**
   * Execute an AI request with automatic model selection and error recovery
   */
  async execute(request: AIRequest): Promise<AIResponse> {
    const selectedModel = this.selectModel(request);
    const config = MODEL_CONFIG[selectedModel];

    // Check quota if user ID provided
    if (request.userId) {
      const quotaCheck = await this.quotaService.checkQuota(
        request.userId,
        'tokens'
      );
      if (!quotaCheck.allowed) {
        throw new Error(quotaCheck.reason || 'Token quota exceeded');
      }
    }

    // Execute with circuit breaker and retry
    const response = await this.errorRecovery.executeWithCircuitBreaker(
      `ai-${selectedModel}`,
      async () => {
        return await this.errorRecovery.retryWithBackoff(
          async () => {
            return await this.executeWithModel(request, selectedModel);
          },
          {
            maxAttempts: 3,
            initialDelay: 1000,
            maxDelay: 10000,
          }
        );
      },
      {
        failureThreshold: 5,
        resetTimeout: 60000,
      }
    );

    // Update quota usage
    if (request.userId) {
      await this.quotaService.incrementUsage(
        request.userId,
        'tokens',
        response.tokensUsed.total
      );
    }

    // Log to database
    await this.logAIRequest(request, response);

    return response;
  }

  /**
   * Execute request with streaming response
   */
  async *executeStream(request: AIRequest): AsyncGenerator<StreamChunk> {
    const selectedModel = this.selectModel(request);

    // Check quota
    if (request.userId) {
      const quotaCheck = await this.quotaService.checkQuota(
        request.userId,
        'tokens'
      );
      if (!quotaCheck.allowed) {
        throw new Error(quotaCheck.reason || 'Token quota exceeded');
      }
    }

    const config = MODEL_CONFIG[selectedModel];

    if (config.provider === 'openai') {
      yield* this.streamOpenAI(request, selectedModel);
    } else if (config.provider === 'anthropic') {
      yield* this.streamAnthropic(request, selectedModel);
    } else if (config.provider === 'google') {
      yield* this.streamGoogle(request, selectedModel);
    }
  }

  /**
   * Execute multiple models and aggregate results
   */
  async executeMultiModel(
    multiRequest: MultiModelRequest
  ): Promise<MultiModelResponse> {
    // Execute all requests in parallel
    const responses = await Promise.all(
      multiRequest.requests.map((req) => this.execute(req))
    );

    let aggregatedContent: string | undefined;

    switch (multiRequest.aggregationStrategy) {
      case 'first':
        aggregatedContent = responses[0]?.content;
        break;

      case 'best':
        // Select response with lowest error rate or highest quality
        const best = responses.sort((a, b) => {
          // Prefer responses that completed successfully
          if (a.finishReason === 'stop' && b.finishReason !== 'stop') return -1;
          if (b.finishReason === 'stop' && a.finishReason !== 'stop') return 1;
          // Prefer longer, more detailed responses
          return b.content.length - a.content.length;
        })[0];
        aggregatedContent = best?.content;
        break;

      case 'consensus':
        // Simple voting: pick most common response
        const contentCounts = new Map<string, number>();
        responses.forEach((r) => {
          const count = contentCounts.get(r.content) || 0;
          contentCounts.set(r.content, count + 1);
        });
        const [mostCommon] = Array.from(contentCounts.entries()).sort(
          (a, b) => b[1] - a[1]
        )[0];
        aggregatedContent = mostCommon;
        break;

      case 'all':
        aggregatedContent = responses.map((r) => r.content).join('\n\n---\n\n');
        break;
    }

    return {
      responses,
      aggregatedContent,
      strategy: multiRequest.aggregationStrategy,
    };
  }

  /**
   * Select the best model for a given request
   */
  private selectModel(request: AIRequest): AIModel {
    if (request.model) {
      // Validate model supports this task
      const config = MODEL_CONFIG[request.model];
      if (!config.capabilities.includes(request.taskType)) {
        console.warn(
          `Model ${request.model} may not be optimal for ${request.taskType}, using anyway`
        );
      }
      return request.model;
    }

    // Auto-select based on task type
    return DEFAULT_MODEL_PER_TASK[request.taskType];
  }

  /**
   * Execute request with OpenAI
   */
  private async executeWithModel(
    request: AIRequest,
    model: AIModel
  ): Promise<AIResponse> {
    const config = MODEL_CONFIG[model];
    const startTime = Date.now();

    if (config.provider === 'openai') {
      return await this.executeOpenAI(request, model);
    } else if (config.provider === 'anthropic') {
      return await this.executeAnthropic(request, model);
    } else if (config.provider === 'google') {
      return await this.executeGoogle(request, model);
    }

    throw new Error(`Unsupported provider: ${config.provider}`);
  }

  /**
   * Execute with OpenAI API
   */
  private async executeOpenAI(
    request: AIRequest,
    model: AIModel
  ): Promise<AIResponse> {
    const startTime = Date.now();

    const completion = await this.openaiClient.chat.completions.create({
      model: model,
      messages: [
        ...(request.systemPrompt
          ? [{ role: 'system' as const, content: request.systemPrompt }]
          : []),
        { role: 'user' as const, content: request.prompt },
      ],
      temperature: request.temperature ?? 0.7,
      max_tokens: request.maxTokens ?? 2000,
    });

    const latencyMs = Date.now() - startTime;

    return {
      content: completion.choices[0]?.message?.content || '',
      model,
      tokensUsed: {
        prompt: completion.usage?.prompt_tokens || 0,
        completion: completion.usage?.completion_tokens || 0,
        total: completion.usage?.total_tokens || 0,
      },
      latencyMs,
      finishReason:
        (completion.choices[0]?.finish_reason as any) || 'error',
    };
  }

  /**
   * Execute with Anthropic Claude API
   */
  private async executeAnthropic(
    request: AIRequest,
    model: AIModel
  ): Promise<AIResponse> {
    const startTime = Date.now();

    const message = await this.anthropicClient.messages.create({
      model: model,
      max_tokens: request.maxTokens ?? 2000,
      system: request.systemPrompt,
      messages: [{ role: 'user', content: request.prompt }],
      temperature: request.temperature ?? 0.7,
    });

    const latencyMs = Date.now() - startTime;

    const content =
      message.content[0]?.type === 'text' ? message.content[0].text : '';

    return {
      content,
      model,
      tokensUsed: {
        prompt: message.usage.input_tokens,
        completion: message.usage.output_tokens,
        total: message.usage.input_tokens + message.usage.output_tokens,
      },
      latencyMs,
      finishReason: message.stop_reason === 'end_turn' ? 'stop' : 'error',
    };
  }

  /**
   * Execute with Google Gemini API
   */
  private async executeGoogle(
    request: AIRequest,
    model: AIModel
  ): Promise<AIResponse> {
    const startTime = Date.now();

    const geminiModel = this.googleClient.getGenerativeModel({
      model: model,
    });

    const result = await geminiModel.generateContent({
      contents: [
        ...(request.systemPrompt
          ? [{ role: 'user', parts: [{ text: request.systemPrompt }] }]
          : []),
        { role: 'user', parts: [{ text: request.prompt }] },
      ],
      generationConfig: {
        temperature: request.temperature ?? 0.7,
        maxOutputTokens: request.maxTokens ?? 2000,
      },
    });

    const latencyMs = Date.now() - startTime;
    const response = result.response;
    const content = response.text();

    // Gemini doesn't provide detailed token usage in the free tier
    const estimatedTokens = {
      prompt: Math.ceil(request.prompt.length / 4),
      completion: Math.ceil(content.length / 4),
      total: Math.ceil((request.prompt.length + content.length) / 4),
    };

    return {
      content,
      model,
      tokensUsed: estimatedTokens,
      latencyMs,
      finishReason: 'stop',
    };
  }

  /**
   * Stream responses from OpenAI
   */
  private async *streamOpenAI(
    request: AIRequest,
    model: AIModel
  ): AsyncGenerator<StreamChunk> {
    const stream = await this.openaiClient.chat.completions.create({
      model: model,
      messages: [
        ...(request.systemPrompt
          ? [{ role: 'system' as const, content: request.systemPrompt }]
          : []),
        { role: 'user' as const, content: request.prompt },
      ],
      temperature: request.temperature ?? 0.7,
      max_tokens: request.maxTokens ?? 2000,
      stream: true,
    });

    for await (const chunk of stream) {
      const delta = chunk.choices[0]?.delta?.content || '';
      const done = chunk.choices[0]?.finish_reason !== null;

      yield { delta, done };
    }
  }

  /**
   * Stream responses from Anthropic
   */
  private async *streamAnthropic(
    request: AIRequest,
    model: AIModel
  ): AsyncGenerator<StreamChunk> {
    const stream = await this.anthropicClient.messages.create({
      model: model,
      max_tokens: request.maxTokens ?? 2000,
      system: request.systemPrompt,
      messages: [{ role: 'user', content: request.prompt }],
      temperature: request.temperature ?? 0.7,
      stream: true,
    });

    for await (const event of stream) {
      if (event.type === 'content_block_delta') {
        const delta =
          event.delta.type === 'text_delta' ? event.delta.text : '';
        yield { delta, done: false };
      } else if (event.type === 'message_stop') {
        yield { delta: '', done: true };
      }
    }
  }

  /**
   * Stream responses from Google
   */
  private async *streamGoogle(
    request: AIRequest,
    model: AIModel
  ): AsyncGenerator<StreamChunk> {
    const geminiModel = this.googleClient.getGenerativeModel({
      model: model,
    });

    const result = await geminiModel.generateContentStream({
      contents: [
        ...(request.systemPrompt
          ? [{ role: 'user', parts: [{ text: request.systemPrompt }] }]
          : []),
        { role: 'user', parts: [{ text: request.prompt }] },
      ],
      generationConfig: {
        temperature: request.temperature ?? 0.7,
        maxOutputTokens: request.maxTokens ?? 2000,
      },
    });

    for await (const chunk of result.stream) {
      const delta = chunk.text();
      yield { delta, done: false };
    }

    yield { delta: '', done: true };
  }

  /**
   * Log AI request to database for analytics
   */
  private async logAIRequest(
    request: AIRequest,
    response: AIResponse
  ): Promise<void> {
    try {
      await this.supabaseClient.from('ai_requests').insert({
        user_id: request.userId || null,
        project_id: request.projectId || null,
        task_type: request.taskType,
        model: response.model,
        prompt_tokens: response.tokensUsed.prompt,
        completion_tokens: response.tokensUsed.completion,
        total_tokens: response.tokensUsed.total,
        latency_ms: response.latencyMs,
        finish_reason: response.finishReason,
        created_at: new Date().toISOString(),
      });
    } catch (error) {
      console.error('Failed to log AI request:', error);
      // Don't throw - logging should not break the main flow
    }
  }
}
