/**
 * Workflow Orchestrator Service Tests
 *
 * Tests the main orchestrator that coordinates all services for end-to-end workflow execution.
 */

import { WorkflowOrchestratorService, WorkflowInput } from '../../src/services/workflow-orchestrator.service';
import { WorkflowStateMachineService } from '../../src/services/workflow-state-machine.service';
import { AIAgentOrchestratorService } from '../../src/services/ai-agent-orchestrator.service';
import { ProgressTrackerService } from '../../src/services/progress-tracker.service';
import { AuditService } from '../../src/services/audit.service';
import { CodeValidationService } from '../../src/services/code-validation.service';
import { createClient } from '@supabase/supabase-js';

jest.mock('../../src/services/workflow-state-machine.service');
jest.mock('../../src/services/ai-agent-orchestrator.service');
jest.mock('../../src/services/progress-tracker.service');
jest.mock('../../src/services/audit.service');
jest.mock('../../src/services/job-queue.service');
jest.mock('../../src/services/quota.service');
jest.mock('../../src/services/code-validation.service');
jest.mock('../../src/services/error-recovery.service');
jest.mock('../../src/services/iteration.service');
jest.mock('@supabase/supabase-js');

describe('WorkflowOrchestratorService', () => {
  let service: WorkflowOrchestratorService;
  let mockWorkflowStateMachine: any;
  let mockAIOrchestrator: any;
  let mockProgressTracker: any;
  let mockAuditService: any;
  let mockCodeValidation: any;
  let mockSupabaseClient: any;

  const mockInput: WorkflowInput = {
    userId: 'user-123',
    projectName: 'Test App',
    projectDescription: 'A test mobile application',
    targetPlatforms: ['ios', 'android'],
  };

  const mockProjectId = 'proj-456';

  beforeEach(() => {
    // Mock Workflow State Machine
    mockWorkflowStateMachine = {
      initializeWorkflow: jest.fn().mockResolvedValue({
        id: 'workflow-123',
        project_id: mockProjectId,
        current_phase: 'problem_deconstruction',
        status: 'active',
      }),
      transitionToPhase: jest.fn().mockResolvedValue({
        current_phase: 'screen_mapping',
        status: 'active',
      }),
      completePhase: jest.fn().mockResolvedValue({
        status: 'completed',
      }),
      failPhase: jest.fn().mockResolvedValue({
        status: 'failed',
      }),
    };
    (WorkflowStateMachineService.getInstance as jest.Mock).mockReturnValue(mockWorkflowStateMachine);

    // Mock AI Orchestrator
    mockAIOrchestrator = {
      execute: jest.fn().mockResolvedValue({
        content: JSON.stringify({
          title: 'Test App',
          description: 'Test description',
          targetAudience: 'Test users',
          coreFeatures: ['Feature 1', 'Feature 2'],
          screens: ['Home', 'Profile'],
          technicalRequirements: ['React Native'],
          successCriteria: ['App works'],
        }),
        tokensUsed: {
          prompt: 100,
          completion: 200,
          total: 300,
        },
        model: 'gpt-4-turbo',
        latencyMs: 1000,
        finishReason: 'stop',
      }),
    };
    (AIAgentOrchestratorService.getInstance as jest.Mock).mockReturnValue(mockAIOrchestrator);

    // Mock Progress Tracker
    mockProgressTracker = {
      trackPhaseStart: jest.fn().mockResolvedValue(undefined),
      trackStep: jest.fn().mockResolvedValue(undefined),
      trackPhaseComplete: jest.fn().mockResolvedValue(undefined),
      trackPhaseError: jest.fn().mockResolvedValue(undefined),
      trackWorkflowComplete: jest.fn().mockResolvedValue(undefined),
      getPhaseSteps: jest.fn().mockReturnValue(['Step 1', 'Step 2', 'Step 3']),
    };
    (ProgressTrackerService.getInstance as jest.Mock).mockReturnValue(mockProgressTracker);

    // Mock Audit Service
    mockAuditService = {
      log: jest.fn().mockResolvedValue(undefined),
    };
    (AuditService.getInstance as jest.Mock).mockReturnValue(mockAuditService);

    // Mock Code Validation
    mockCodeValidation = {
      validateGeneratedCode: jest.fn().mockResolvedValue({
        overall_status: 'passed',
        eslint_result: { errors: 0, warnings: 0, fixable: 0 },
        typescript_result: { errors: 0, warnings: 0 },
        semgrep_result: { critical: 0, high: 0, medium: 0, low: 0 },
        npm_audit_result: {
          vulnerabilities: { critical: 0, high: 0, moderate: 0, low: 0 },
        },
        recommendations: [],
      }),
    };
    (CodeValidationService.getInstance as jest.Mock).mockReturnValue(mockCodeValidation);

    // Mock Supabase Client
    mockSupabaseClient = {
      from: jest.fn(() => mockSupabaseClient),
      insert: jest.fn(() => mockSupabaseClient),
      select: jest.fn(() => mockSupabaseClient),
      single: jest.fn(),
    };
    (createClient as jest.Mock).mockReturnValue(mockSupabaseClient);

    // Mock project creation
    mockSupabaseClient.single.mockResolvedValue({
      data: { id: mockProjectId },
      error: null,
    });

    service = WorkflowOrchestratorService.getInstance();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Workflow Execution', () => {
    it('should execute complete workflow successfully', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(result.status).toBe('completed');
      expect(result.projectId).toBe(mockProjectId);
      expect(result.prd).toBeDefined();
      expect(result.screenMap).toBeDefined();
      expect(result.designs).toBeDefined();
      expect(result.generatedCode).toBeDefined();
      expect(result.qualityReport).toBeDefined();
      expect(result.totalTokensUsed).toBeGreaterThan(0);
      expect(result.estimatedCost).toBeGreaterThan(0);
    });

    it('should create project record in database', async () => {
      await service.executeWorkflow(mockInput);

      expect(mockSupabaseClient.from).toHaveBeenCalledWith('projects');
      expect(mockSupabaseClient.insert).toHaveBeenCalledWith(
        expect.objectContaining({
          user_id: mockInput.userId,
          name: mockInput.projectName,
          description: mockInput.projectDescription,
          target_platforms: mockInput.targetPlatforms,
          status: 'in_progress',
        })
      );
    });

    it('should initialize workflow state machine', async () => {
      await service.executeWorkflow(mockInput);

      expect(mockWorkflowStateMachine.initializeWorkflow).toHaveBeenCalledWith(mockProjectId);
    });

    it('should log workflow start in audit log', async () => {
      await service.executeWorkflow(mockInput);

      expect(mockAuditService.log).toHaveBeenCalledWith(
        expect.objectContaining({
          userId: mockInput.userId,
          projectId: mockProjectId,
          action: 'workflow_started',
          resourceType: 'workflow',
        })
      );
    });

    it('should log workflow completion in audit log', async () => {
      await service.executeWorkflow(mockInput);

      expect(mockAuditService.log).toHaveBeenCalledWith(
        expect.objectContaining({
          action: 'workflow_completed',
          projectId: mockProjectId,
        })
      );
    });

    it('should track workflow completion', async () => {
      await service.executeWorkflow(mockInput);

      expect(mockProgressTracker.trackWorkflowComplete).toHaveBeenCalledWith(mockProjectId);
    });

    it('should return total duration and cost estimates', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(result.totalDurationMs).toBeGreaterThan(0);
      expect(result.totalTokensUsed).toBeGreaterThan(0);
      expect(result.estimatedCost).toBeGreaterThan(0);
    });
  });

  describe('Phase 1: Problem Deconstruction', () => {
    it('should execute problem deconstruction phase', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(mockProgressTracker.trackPhaseStart).toHaveBeenCalledWith(
        mockProjectId,
        'problem_deconstruction'
      );

      expect(mockAIOrchestrator.execute).toHaveBeenCalledWith(
        expect.objectContaining({
          taskType: 'problem_deconstruction',
          userId: mockInput.userId,
          projectId: mockProjectId,
        })
      );

      expect(result.prd).toEqual(
        expect.objectContaining({
          title: 'Test App',
          screens: expect.arrayContaining(['Home', 'Profile']),
        })
      );
    });

    it('should track progress steps during problem deconstruction', async () => {
      await service.executeWorkflow(mockInput);

      const steps = mockProgressTracker.getPhaseSteps('problem_deconstruction');
      expect(mockProgressTracker.trackStep).toHaveBeenCalledTimes(
        expect.any(Number)
      );
    });

    it('should complete problem deconstruction phase', async () => {
      await service.executeWorkflow(mockInput);

      expect(mockWorkflowStateMachine.completePhase).toHaveBeenCalled();
      expect(mockProgressTracker.trackPhaseComplete).toHaveBeenCalledWith(
        mockProjectId,
        'problem_deconstruction',
        expect.any(Object)
      );
    });
  });

  describe('Phase 2: Screen Mapping', () => {
    it('should execute screen mapping phase', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(mockProgressTracker.trackPhaseStart).toHaveBeenCalledWith(
        mockProjectId,
        'screen_mapping'
      );

      expect(result.screenMap).toBeDefined();
      expect(result.screenMap?.screens).toBeInstanceOf(Array);
    });

    it('should use PRD output as input for screen mapping', async () => {
      await service.executeWorkflow(mockInput);

      const aiCalls = mockAIOrchestrator.execute.mock.calls;
      const screenMappingCall = aiCalls.find(
        (call: any) => call[0].taskType === 'screen_mapping'
      );

      expect(screenMappingCall).toBeDefined();
      expect(screenMappingCall[0].prompt).toContain('Test App');
    });
  });

  describe('Phase 3: Design Generation', () => {
    it('should execute design generation phase', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(mockProgressTracker.trackPhaseStart).toHaveBeenCalledWith(
        mockProjectId,
        'design_generation'
      );

      expect(result.designs).toBeDefined();
      expect(result.designs?.designTokens).toBeDefined();
      expect(result.designs?.componentSpecs).toBeInstanceOf(Array);
    });

    it('should incorporate design preferences', async () => {
      const inputWithPreferences: WorkflowInput = {
        ...mockInput,
        designPreferences: {
          colorScheme: 'dark',
          brandColors: ['#FF0000', '#00FF00'],
        },
      };

      await service.executeWorkflow(inputWithPreferences);

      const aiCalls = mockAIOrchestrator.execute.mock.calls;
      const designCall = aiCalls.find(
        (call: any) => call[0].taskType === 'design_generation'
      );

      expect(designCall[0].prompt).toContain('dark');
    });
  });

  describe('Phase 4: Stitch Iteration', () => {
    it('should execute stitch iteration phase (automated mode)', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(mockProgressTracker.trackPhaseStart).toHaveBeenCalledWith(
        mockProjectId,
        'stitch_iteration'
      );

      expect(mockProgressTracker.trackPhaseComplete).toHaveBeenCalledWith(
        mockProjectId,
        'stitch_iteration',
        expect.objectContaining({ skipped: true })
      );
    });
  });

  describe('Phase 5: Code Generation', () => {
    it('should execute code generation phase', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(mockProgressTracker.trackPhaseStart).toHaveBeenCalledWith(
        mockProjectId,
        'code_generation'
      );

      expect(result.generatedCode).toBeDefined();
      expect(result.generatedCode?.files).toBeInstanceOf(Array);
      expect(result.generatedCode?.projectPath).toBeDefined();
    });

    it('should use lower temperature for code generation', async () => {
      await service.executeWorkflow(mockInput);

      const aiCalls = mockAIOrchestrator.execute.mock.calls;
      const codeGenCall = aiCalls.find(
        (call: any) => call[0].taskType === 'code_generation'
      );

      expect(codeGenCall[0].temperature).toBeLessThanOrEqual(0.5);
    });
  });

  describe('Phase 6: Code Review', () => {
    it('should execute code review phase', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(mockProgressTracker.trackPhaseStart).toHaveBeenCalledWith(
        mockProjectId,
        'code_review'
      );

      expect(mockCodeValidation.validateGeneratedCode).toHaveBeenCalled();

      expect(result.qualityReport).toEqual(
        expect.objectContaining({
          overallStatus: 'passed',
          eslintResults: expect.any(Object),
          typescriptResults: expect.any(Object),
          semgrepResults: expect.any(Object),
          npmAuditResults: expect.any(Object),
        })
      );
    });

    it('should return quality report with all validation results', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(result.qualityReport?.eslintResults.errors).toBe(0);
      expect(result.qualityReport?.typescriptResults.errors).toBe(0);
      expect(result.qualityReport?.semgrepResults.critical).toBe(0);
      expect(result.qualityReport?.npmAuditResults.critical).toBe(0);
    });
  });

  describe('Error Handling', () => {
    it('should handle project creation failure', async () => {
      mockSupabaseClient.single.mockResolvedValue({
        data: null,
        error: { message: 'Database error' },
      });

      const result = await service.executeWorkflow(mockInput);

      expect(result.status).toBe('failed');
      expect(result.error).toContain('Database error');
    });

    it('should handle AI request failure', async () => {
      mockAIOrchestrator.execute.mockRejectedValue(new Error('AI service unavailable'));

      const result = await service.executeWorkflow(mockInput);

      expect(result.status).toBe('failed');
      expect(result.error).toContain('AI service unavailable');
    });

    it('should log failed workflow in audit', async () => {
      mockAIOrchestrator.execute.mockRejectedValue(new Error('Test error'));

      await service.executeWorkflow(mockInput);

      expect(mockAuditService.log).toHaveBeenCalledWith(
        expect.objectContaining({
          action: 'workflow_failed',
          metadata: expect.objectContaining({
            error: 'Test error',
          }),
        })
      );
    });

    it('should mark workflow as failed in state machine', async () => {
      mockAIOrchestrator.execute.mockRejectedValue(new Error('Test error'));

      await service.executeWorkflow(mockInput);

      expect(mockWorkflowStateMachine.failPhase).toHaveBeenCalledWith(
        mockProjectId,
        expect.objectContaining({
          error: 'Test error',
          retryable: false,
        })
      );
    });

    it('should identify retryable errors', async () => {
      mockAIOrchestrator.execute.mockRejectedValue(new Error('Rate limit exceeded'));

      await service.executeWorkflow(mockInput);

      expect(mockWorkflowStateMachine.failPhase).toHaveBeenCalledWith(
        mockProjectId,
        expect.objectContaining({
          retryable: true,
        })
      );
    });

    it('should return partial results on failure', async () => {
      // Succeed for problem deconstruction, fail on screen mapping
      let callCount = 0;
      mockAIOrchestrator.execute.mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          return Promise.resolve({
            content: JSON.stringify({
              title: 'Test',
              description: 'Test',
              targetAudience: 'Users',
              coreFeatures: ['Feature'],
              screens: ['Home'],
              technicalRequirements: ['React Native'],
              successCriteria: ['Works'],
            }),
            tokensUsed: { prompt: 100, completion: 200, total: 300 },
            model: 'gpt-4',
            latencyMs: 1000,
            finishReason: 'stop',
          });
        }
        return Promise.reject(new Error('Screen mapping failed'));
      });

      const result = await service.executeWorkflow(mockInput);

      expect(result.status).toBe('failed');
      expect(result.totalTokensUsed).toBe(300); // Only first phase tokens
    });
  });

  describe('Token Usage Tracking', () => {
    it('should accumulate token usage across all phases', async () => {
      const result = await service.executeWorkflow(mockInput);

      // Each AI call uses 300 tokens (mocked)
      // 4 phases use AI (problem deconstruction, screen mapping, design generation, code generation)
      expect(result.totalTokensUsed).toBeGreaterThanOrEqual(300);
    });

    it('should calculate estimated cost', async () => {
      const result = await service.executeWorkflow(mockInput);

      expect(result.estimatedCost).toBeGreaterThan(0);
      // With default avg cost of $0.01 per 1K tokens and 300+ tokens:
      // Cost should be at least $0.003
      expect(result.estimatedCost).toBeGreaterThanOrEqual(0.003);
    });
  });

  describe('JSON Parsing', () => {
    it('should handle well-formed JSON responses', async () => {
      mockAIOrchestrator.execute.mockResolvedValue({
        content: JSON.stringify({
          title: 'Valid JSON',
          description: 'Test',
          targetAudience: 'Users',
          coreFeatures: ['Feature 1'],
          screens: ['Home'],
          technicalRequirements: ['React Native'],
          successCriteria: ['Works'],
        }),
        tokensUsed: { prompt: 100, completion: 200, total: 300 },
        model: 'gpt-4',
        latencyMs: 1000,
        finishReason: 'stop',
      });

      const result = await service.executeWorkflow(mockInput);

      expect(result.prd?.title).toBe('Valid JSON');
    });

    it('should handle malformed JSON with fallback', async () => {
      mockAIOrchestrator.execute.mockResolvedValue({
        content: 'This is not JSON at all',
        tokensUsed: { prompt: 100, completion: 200, total: 300 },
        model: 'gpt-4',
        latencyMs: 1000,
        finishReason: 'stop',
      });

      const result = await service.executeWorkflow(mockInput);

      // Should fall back to basic PRD from input
      expect(result.prd?.title).toBe(mockInput.projectName);
      expect(result.prd?.description).toBe(mockInput.projectDescription);
    });

    it('should handle JSON embedded in prose', async () => {
      mockAIOrchestrator.execute.mockResolvedValue({
        content: `Here is the PRD:

${JSON.stringify({
  title: 'Embedded JSON',
  description: 'Test',
  targetAudience: 'Users',
  coreFeatures: ['Feature'],
  screens: ['Home'],
  technicalRequirements: ['React Native'],
  successCriteria: ['Works'],
})}

That's the complete document.`,
        tokensUsed: { prompt: 100, completion: 200, total: 300 },
        model: 'gpt-4',
        latencyMs: 1000,
        finishReason: 'stop',
      });

      const result = await service.executeWorkflow(mockInput);

      expect(result.prd?.title).toBe('Embedded JSON');
    });
  });
});
