/**
 * Workflow State Machine Service Tests
 *
 * Tests the workflow orchestration logic that manages phase transitions
 * through the Design-First Software Factory pipeline.
 */

import { WorkflowStateMachineService } from '../../src/services/workflow-state-machine.service';
import { IterationService } from '../../src/services/iteration.service';
import { createClient } from '@supabase/supabase-js';

jest.mock('@supabase/supabase-js');
jest.mock('../../src/services/iteration.service');

describe('WorkflowStateMachineService', () => {
  let service: WorkflowStateMachineService;
  let mockSupabaseClient: any;
  let mockIterationService: any;

  const mockProjectId = 'proj-123';
  const mockWorkflowId = 'workflow-456';

  beforeEach(() => {
    // Mock Supabase client
    mockSupabaseClient = {
      from: jest.fn(() => mockSupabaseClient),
      insert: jest.fn(() => mockSupabaseClient),
      update: jest.fn(() => mockSupabaseClient),
      select: jest.fn(() => mockSupabaseClient),
      eq: jest.fn(() => mockSupabaseClient),
      order: jest.fn(() => mockSupabaseClient),
      limit: jest.fn(() => mockSupabaseClient),
      single: jest.fn(),
    };

    (createClient as jest.Mock).mockReturnValue(mockSupabaseClient);

    // Mock IterationService
    mockIterationService = {
      checkIterationLimit: jest.fn().mockResolvedValue({
        allowed: true,
        current_count: 1,
        max_iterations: 5,
      }),
      trackIteration: jest.fn().mockResolvedValue({
        allowed: true,
        current_count: 2,
        max_iterations: 5,
      }),
    };

    (IterationService.getInstance as jest.Mock).mockReturnValue(mockIterationService);

    service = WorkflowStateMachineService.getInstance();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('initializeWorkflow', () => {
    it('should create a new workflow starting with problem_deconstruction', async () => {
      const mockWorkflow = {
        id: mockWorkflowId,
        project_id: mockProjectId,
        current_phase: 'problem_deconstruction',
        status: 'active',
        phase_data: {
          problem_deconstruction: {
            status: 'active',
            started_at: new Date(),
            iteration_count: 0,
          },
          screen_mapping: { status: 'pending', iteration_count: 0 },
          design_generation: { status: 'pending', iteration_count: 0 },
          stitch_iteration: { status: 'pending', iteration_count: 0 },
          code_generation: { status: 'pending', iteration_count: 0 },
          code_review: { status: 'pending', iteration_count: 0 },
        },
        started_at: new Date().toISOString(),
      };

      mockSupabaseClient.single.mockResolvedValue({ data: mockWorkflow, error: null });

      const result = await service.initializeWorkflow(mockProjectId);

      expect(result.project_id).toBe(mockProjectId);
      expect(result.current_phase).toBe('problem_deconstruction');
      expect(result.status).toBe('active');
      expect(result.phase_data.problem_deconstruction.status).toBe('active');
      expect(mockSupabaseClient.from).toHaveBeenCalledWith('workflow_states');
      expect(mockSupabaseClient.insert).toHaveBeenCalled();
    });

    it('should throw error if database insert fails', async () => {
      mockSupabaseClient.single.mockResolvedValue({
        data: null,
        error: { message: 'Database error' },
      });

      await expect(service.initializeWorkflow(mockProjectId)).rejects.toThrow(
        'Failed to initialize workflow: Database error'
      );
    });
  });

  describe('getWorkflowState', () => {
    it('should retrieve the most recent workflow for a project', async () => {
      const mockWorkflow = {
        id: mockWorkflowId,
        project_id: mockProjectId,
        current_phase: 'design_generation',
        status: 'active',
        phase_data: {},
        started_at: new Date().toISOString(),
      };

      mockSupabaseClient.single.mockResolvedValue({ data: mockWorkflow, error: null });

      const result = await service.getWorkflowState(mockProjectId);

      expect(result).not.toBeNull();
      expect(result?.project_id).toBe(mockProjectId);
      expect(result?.current_phase).toBe('design_generation');
      expect(mockSupabaseClient.eq).toHaveBeenCalledWith('project_id', mockProjectId);
      expect(mockSupabaseClient.order).toHaveBeenCalledWith('started_at', { ascending: false });
      expect(mockSupabaseClient.limit).toHaveBeenCalledWith(1);
    });

    it('should return null if no workflow exists', async () => {
      mockSupabaseClient.single.mockResolvedValue({
        data: null,
        error: { code: 'PGRST116' },
      });

      const result = await service.getWorkflowState(mockProjectId);

      expect(result).toBeNull();
    });

    it('should throw error for database errors other than not found', async () => {
      mockSupabaseClient.single.mockResolvedValue({
        data: null,
        error: { code: 'OTHER_ERROR', message: 'Database error' },
      });

      await expect(service.getWorkflowState(mockProjectId)).rejects.toThrow(
        'Failed to get workflow state: Database error'
      );
    });
  });

  describe('validateTransition', () => {
    it('should allow first transition to problem_deconstruction', () => {
      const transition = service.validateTransition(null, 'problem_deconstruction');

      expect(transition.allowed).toBe(true);
      expect(transition.from).toBeNull();
      expect(transition.to).toBe('problem_deconstruction');
    });

    it('should reject first transition to any phase other than problem_deconstruction', () => {
      const transition = service.validateTransition(null, 'code_generation');

      expect(transition.allowed).toBe(false);
      expect(transition.reason).toBe('Workflow must start with problem_deconstruction');
    });

    it('should allow valid forward transitions', () => {
      const transition = service.validateTransition(
        'problem_deconstruction',
        'screen_mapping'
      );

      expect(transition.allowed).toBe(true);
      expect(transition.from).toBe('problem_deconstruction');
      expect(transition.to).toBe('screen_mapping');
    });

    it('should allow valid backward transitions for iteration', () => {
      const transition = service.validateTransition(
        'design_generation',
        'screen_mapping'
      );

      expect(transition.allowed).toBe(true);
    });

    it('should reject invalid transitions', () => {
      const transition = service.validateTransition(
        'problem_deconstruction',
        'code_generation'
      );

      expect(transition.allowed).toBe(false);
      expect(transition.reason).toContain('Cannot transition');
    });
  });

  describe('transitionToPhase', () => {
    const mockCurrentWorkflow = {
      id: mockWorkflowId,
      project_id: mockProjectId,
      current_phase: 'problem_deconstruction' as const,
      status: 'active' as const,
      phase_data: {
        problem_deconstruction: { status: 'active' as const, iteration_count: 1 },
        screen_mapping: { status: 'pending' as const, iteration_count: 0 },
        design_generation: { status: 'pending' as const, iteration_count: 0 },
        stitch_iteration: { status: 'pending' as const, iteration_count: 0 },
        code_generation: { status: 'pending' as const, iteration_count: 0 },
        code_review: { status: 'pending' as const, iteration_count: 0 },
      },
      started_at: new Date(),
    };

    beforeEach(() => {
      // Mock getWorkflowState
      jest.spyOn(service as any, 'getWorkflowState').mockResolvedValue(mockCurrentWorkflow);
    });

    it('should transition to next phase successfully', async () => {
      const updatedWorkflow = {
        ...mockCurrentWorkflow,
        current_phase: 'screen_mapping',
      };

      mockSupabaseClient.single.mockResolvedValue({ data: updatedWorkflow, error: null });

      const result = await service.transitionToPhase(mockProjectId, 'screen_mapping');

      expect(result.current_phase).toBe('screen_mapping');
      expect(mockIterationService.checkIterationLimit).toHaveBeenCalledWith(
        mockProjectId,
        'screen_mapping'
      );
      expect(mockIterationService.trackIteration).toHaveBeenCalledWith(
        mockProjectId,
        'screen_mapping',
        expect.any(String)
      );
    });

    it('should reject invalid transitions', async () => {
      await expect(
        service.transitionToPhase(mockProjectId, 'code_generation')
      ).rejects.toThrow('Cannot transition');
    });

    it('should allow forced transitions', async () => {
      const updatedWorkflow = {
        ...mockCurrentWorkflow,
        current_phase: 'code_generation',
      };

      mockSupabaseClient.single.mockResolvedValue({ data: updatedWorkflow, error: null });

      const result = await service.transitionToPhase(
        mockProjectId,
        'code_generation',
        { force: true }
      );

      expect(result.current_phase).toBe('code_generation');
    });

    it('should reject transition if iteration limit exceeded', async () => {
      mockIterationService.checkIterationLimit.mockResolvedValue({
        allowed: false,
        reason: 'Maximum iterations exceeded',
        current_count: 5,
        max_iterations: 5,
      });

      await expect(
        service.transitionToPhase(mockProjectId, 'screen_mapping')
      ).rejects.toThrow('Maximum iterations exceeded');
    });

    it('should mark previous phase as completed on forward transition', async () => {
      const updatedWorkflow = {
        ...mockCurrentWorkflow,
        current_phase: 'screen_mapping',
        phase_data: {
          ...mockCurrentWorkflow.phase_data,
          problem_deconstruction: {
            status: 'completed',
            iteration_count: 1,
            completed_at: new Date(),
          },
          screen_mapping: {
            status: 'active',
            iteration_count: 1,
            started_at: new Date(),
          },
        },
      };

      mockSupabaseClient.single.mockResolvedValue({ data: updatedWorkflow, error: null });

      const result = await service.transitionToPhase(mockProjectId, 'screen_mapping');

      expect(mockSupabaseClient.update).toHaveBeenCalledWith(
        expect.objectContaining({
          current_phase: 'screen_mapping',
          phase_data: expect.objectContaining({
            problem_deconstruction: expect.objectContaining({ status: 'completed' }),
            screen_mapping: expect.objectContaining({ status: 'active' }),
          }),
        })
      );
    });
  });

  describe('completePhase', () => {
    const mockCurrentWorkflow = {
      id: mockWorkflowId,
      project_id: mockProjectId,
      current_phase: 'screen_mapping' as const,
      status: 'active' as const,
      phase_data: {
        problem_deconstruction: { status: 'completed' as const, iteration_count: 1 },
        screen_mapping: { status: 'active' as const, iteration_count: 1 },
        design_generation: { status: 'pending' as const, iteration_count: 0 },
        stitch_iteration: { status: 'pending' as const, iteration_count: 0 },
        code_generation: { status: 'pending' as const, iteration_count: 0 },
        code_review: { status: 'pending' as const, iteration_count: 0 },
      },
      started_at: new Date(),
    };

    beforeEach(() => {
      jest.spyOn(service as any, 'getWorkflowState').mockResolvedValue(mockCurrentWorkflow);
    });

    it('should complete phase and auto-advance to next', async () => {
      const updatedWorkflow = {
        ...mockCurrentWorkflow,
        current_phase: 'design_generation',
      };

      mockSupabaseClient.single.mockResolvedValue({ data: updatedWorkflow, error: null });

      // Mock transitionToPhase
      jest.spyOn(service, 'transitionToPhase').mockResolvedValue(updatedWorkflow as any);

      const result = await service.completePhase(mockProjectId, {
        result: { screens: ['Home', 'Profile'] },
      });

      expect(service.transitionToPhase).toHaveBeenCalledWith(
        mockProjectId,
        'design_generation'
      );
    });

    it('should mark workflow as completed when completing final phase', async () => {
      const finalPhaseWorkflow = {
        ...mockCurrentWorkflow,
        current_phase: 'code_review' as const,
        phase_data: {
          ...mockCurrentWorkflow.phase_data,
          code_review: { status: 'active' as const, iteration_count: 1 },
        },
      };

      jest.spyOn(service as any, 'getWorkflowState').mockResolvedValue(finalPhaseWorkflow);

      const completedWorkflow = {
        ...finalPhaseWorkflow,
        status: 'completed',
        completed_at: new Date().toISOString(),
      };

      mockSupabaseClient.single.mockResolvedValue({ data: completedWorkflow, error: null });

      const result = await service.completePhase(mockProjectId);

      expect(result.status).toBe('completed');
      expect(mockSupabaseClient.update).toHaveBeenCalledWith(
        expect.objectContaining({ status: 'completed' })
      );
    });
  });

  describe('failPhase', () => {
    const mockCurrentWorkflow = {
      id: mockWorkflowId,
      project_id: mockProjectId,
      current_phase: 'code_generation' as const,
      status: 'active' as const,
      phase_data: {
        problem_deconstruction: { status: 'completed' as const, iteration_count: 1 },
        screen_mapping: { status: 'completed' as const, iteration_count: 1 },
        design_generation: { status: 'completed' as const, iteration_count: 1 },
        stitch_iteration: { status: 'completed' as const, iteration_count: 2 },
        code_generation: { status: 'active' as const, iteration_count: 1 },
        code_review: { status: 'pending' as const, iteration_count: 0 },
      },
      started_at: new Date(),
    };

    beforeEach(() => {
      jest.spyOn(service as any, 'getWorkflowState').mockResolvedValue(mockCurrentWorkflow);
    });

    it('should mark phase as failed and pause workflow if retryable', async () => {
      const failedWorkflow = {
        ...mockCurrentWorkflow,
        status: 'paused',
        error_message: 'TypeScript compilation error',
      };

      mockSupabaseClient.single.mockResolvedValue({ data: failedWorkflow, error: null });

      const result = await service.failPhase(mockProjectId, {
        error: 'TypeScript compilation error',
        retryable: true,
      });

      expect(result.status).toBe('paused');
      expect(result.error_message).toBe('TypeScript compilation error');
      expect(mockSupabaseClient.update).toHaveBeenCalledWith(
        expect.objectContaining({ status: 'paused' })
      );
    });

    it('should mark workflow as failed if error is not retryable', async () => {
      const failedWorkflow = {
        ...mockCurrentWorkflow,
        status: 'failed',
        error_message: 'Quota exceeded',
      };

      mockSupabaseClient.single.mockResolvedValue({ data: failedWorkflow, error: null });

      const result = await service.failPhase(mockProjectId, {
        error: 'Quota exceeded',
        retryable: false,
      });

      expect(result.status).toBe('failed');
      expect(mockSupabaseClient.update).toHaveBeenCalledWith(
        expect.objectContaining({ status: 'failed' })
      );
    });
  });

  describe('pauseWorkflow', () => {
    it('should pause an active workflow', async () => {
      const activeWorkflow = {
        id: mockWorkflowId,
        project_id: mockProjectId,
        current_phase: 'design_generation' as const,
        status: 'active' as const,
        phase_data: {},
        started_at: new Date(),
      };

      jest.spyOn(service as any, 'getWorkflowState').mockResolvedValue(activeWorkflow);

      const pausedWorkflow = { ...activeWorkflow, status: 'paused' };
      mockSupabaseClient.single.mockResolvedValue({ data: pausedWorkflow, error: null });

      const result = await service.pauseWorkflow(mockProjectId);

      expect(result.status).toBe('paused');
      expect(mockSupabaseClient.update).toHaveBeenCalledWith({ status: 'paused' });
    });
  });

  describe('resumeWorkflow', () => {
    it('should resume a paused workflow', async () => {
      const pausedWorkflow = {
        id: mockWorkflowId,
        project_id: mockProjectId,
        current_phase: 'design_generation' as const,
        status: 'paused' as const,
        phase_data: {},
        started_at: new Date(),
      };

      jest.spyOn(service as any, 'getWorkflowState').mockResolvedValue(pausedWorkflow);

      const activeWorkflow = { ...pausedWorkflow, status: 'active' };
      mockSupabaseClient.single.mockResolvedValue({ data: activeWorkflow, error: null });

      const result = await service.resumeWorkflow(mockProjectId);

      expect(result.status).toBe('active');
      expect(mockSupabaseClient.update).toHaveBeenCalledWith({ status: 'active' });
    });

    it('should reject resuming non-paused workflows', async () => {
      const activeWorkflow = {
        id: mockWorkflowId,
        project_id: mockProjectId,
        current_phase: 'design_generation' as const,
        status: 'active' as const,
        phase_data: {},
        started_at: new Date(),
      };

      jest.spyOn(service as any, 'getWorkflowState').mockResolvedValue(activeWorkflow);

      await expect(service.resumeWorkflow(mockProjectId)).rejects.toThrow(
        'Can only resume paused workflows'
      );
    });
  });
});
