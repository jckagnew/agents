/**
 * Progress Tracker Service Tests
 *
 * Tests real-time progress tracking, WebSocket events, and progress history.
 */

import { ProgressTrackerService, ProgressEvent } from '../../src/services/progress-tracker.service';
import { createClient } from '@supabase/supabase-js';

jest.mock('@supabase/supabase-js');

describe('ProgressTrackerService', () => {
  let service: ProgressTrackerService;
  let mockSupabaseClient: any;
  let mockRealtimeChannel: any;

  const mockProjectId = 'proj-123';

  beforeEach(() => {
    // Mock Realtime Channel
    mockRealtimeChannel = {
      subscribe: jest.fn((callback) => {
        if (typeof callback === 'function') {
          callback('SUBSCRIBED');
        }
        return mockRealtimeChannel;
      }),
      send: jest.fn().mockResolvedValue(undefined),
      on: jest.fn().mockReturnThis(),
    };

    // Mock Supabase Client
    mockSupabaseClient = {
      channel: jest.fn(() => mockRealtimeChannel),
      removeChannel: jest.fn().mockResolvedValue(undefined),
      from: jest.fn(() => mockSupabaseClient),
      insert: jest.fn(() => mockSupabaseClient),
      select: jest.fn(() => mockSupabaseClient),
      eq: jest.fn(() => mockSupabaseClient),
      order: jest.fn(() => mockSupabaseClient),
      limit: jest.fn(() => mockSupabaseClient),
      single: jest.fn(),
      delete: jest.fn(() => mockSupabaseClient),
    };

    (createClient as jest.Mock).mockReturnValue(mockSupabaseClient);

    service = ProgressTrackerService.getInstance();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Initialization', () => {
    it('should initialize realtime channel on creation', () => {
      expect(mockSupabaseClient.channel).toHaveBeenCalledWith('progress_events');
      expect(mockRealtimeChannel.subscribe).toHaveBeenCalled();
    });
  });

  describe('Local Subscriptions', () => {
    it('should allow subscribing to progress updates', () => {
      const callback = jest.fn();
      const unsubscribe = service.subscribe(mockProjectId, callback);

      expect(typeof unsubscribe).toBe('function');
    });

    it('should receive events after subscribing', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      mockSupabaseClient.insert.mockResolvedValue({ error: null });

      await service.emit({
        type: 'phase_start',
        projectId: mockProjectId,
        phase: 'problem_deconstruction',
        progress: 0,
        message: 'Starting',
        timestamp: new Date(),
      });

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'phase_start',
          projectId: mockProjectId,
          phase: 'problem_deconstruction',
        })
      );
    });

    it('should stop receiving events after unsubscribing', async () => {
      const callback = jest.fn();
      const unsubscribe = service.subscribe(mockProjectId, callback);

      mockSupabaseClient.insert.mockResolvedValue({ error: null });

      // First event should be received
      await service.emit({
        type: 'phase_start',
        projectId: mockProjectId,
        phase: 'problem_deconstruction',
        progress: 0,
        timestamp: new Date(),
      });

      expect(callback).toHaveBeenCalledTimes(1);

      // Unsubscribe
      unsubscribe();

      // Second event should not be received
      await service.emit({
        type: 'phase_progress',
        projectId: mockProjectId,
        phase: 'problem_deconstruction',
        progress: 50,
        timestamp: new Date(),
      });

      expect(callback).toHaveBeenCalledTimes(1); // Still 1
    });

    it('should support multiple subscribers per project', async () => {
      const callback1 = jest.fn();
      const callback2 = jest.fn();

      service.subscribe(mockProjectId, callback1);
      service.subscribe(mockProjectId, callback2);

      mockSupabaseClient.insert.mockResolvedValue({ error: null });

      await service.emit({
        type: 'phase_start',
        projectId: mockProjectId,
        phase: 'problem_deconstruction',
        progress: 0,
        timestamp: new Date(),
      });

      expect(callback1).toHaveBeenCalled();
      expect(callback2).toHaveBeenCalled();
    });

    it('should not notify subscribers of other projects', async () => {
      const callback1 = jest.fn();
      const callback2 = jest.fn();

      service.subscribe('project-1', callback1);
      service.subscribe('project-2', callback2);

      mockSupabaseClient.insert.mockResolvedValue({ error: null });

      await service.emit({
        type: 'phase_start',
        projectId: 'project-1',
        phase: 'problem_deconstruction',
        progress: 0,
        timestamp: new Date(),
      });

      expect(callback1).toHaveBeenCalled();
      expect(callback2).not.toHaveBeenCalled();
    });
  });

  describe('Event Emission', () => {
    it('should broadcast events via Supabase Realtime', async () => {
      mockSupabaseClient.insert.mockResolvedValue({ error: null });

      await service.emit({
        type: 'phase_start',
        projectId: mockProjectId,
        phase: 'screen_mapping',
        progress: 0,
        timestamp: new Date(),
      });

      expect(mockRealtimeChannel.send).toHaveBeenCalledWith({
        type: 'broadcast',
        event: 'progress_update',
        payload: expect.objectContaining({
          type: 'phase_start',
          phase: 'screen_mapping',
        }),
      });
    });

    it('should save events to database', async () => {
      mockSupabaseClient.insert.mockResolvedValue({ error: null });

      await service.emit({
        type: 'phase_complete',
        projectId: mockProjectId,
        phase: 'design_generation',
        progress: 100,
        message: 'Design complete',
        timestamp: new Date(),
      });

      expect(mockSupabaseClient.from).toHaveBeenCalledWith('progress_events');
      expect(mockSupabaseClient.insert).toHaveBeenCalledWith(
        expect.objectContaining({
          project_id: mockProjectId,
          event_type: 'phase_complete',
          phase: 'design_generation',
          progress_pct: 100,
          message: 'Design complete',
        })
      );
    });

    it('should not fail if database save fails', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      mockSupabaseClient.insert.mockRejectedValue(new Error('Database error'));

      // Should not throw
      await expect(
        service.emit({
          type: 'phase_start',
          projectId: mockProjectId,
          phase: 'problem_deconstruction',
          progress: 0,
          timestamp: new Date(),
        })
      ).resolves.not.toThrow();

      // Subscribers should still be notified
      expect(callback).toHaveBeenCalled();
    });
  });

  describe('Phase Tracking', () => {
    beforeEach(() => {
      mockSupabaseClient.insert.mockResolvedValue({ error: null });
    });

    it('should track phase start', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      await service.trackPhaseStart(mockProjectId, 'code_generation');

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'phase_start',
          phase: 'code_generation',
          progress: 0,
          message: 'Starting code generation',
        })
      );
    });

    it('should track individual steps within a phase', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      await service.trackStep(mockProjectId, 'code_generation', 0);

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'phase_progress',
          phase: 'code_generation',
          step: 'Initializing Expo project',
          progress: expect.any(Number),
        })
      );

      expect(mockSupabaseClient.from).toHaveBeenCalledWith('progress_checkpoints');
    });

    it('should calculate progress percentage based on step index', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      // code_generation has 8 steps (see PHASE_STEPS)
      // Step 4 (index 3) should be ~50% progress
      await service.trackStep(mockProjectId, 'code_generation', 3);

      const call = callback.mock.calls[0][0] as ProgressEvent;
      expect(call.progress).toBeGreaterThanOrEqual(40);
      expect(call.progress).toBeLessThanOrEqual(60);
    });

    it('should track custom progress', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      await service.trackProgress(
        mockProjectId,
        'design_generation',
        75,
        'Applying platform-specific styles',
        { platform: 'ios' }
      );

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'phase_progress',
          phase: 'design_generation',
          progress: 75,
          step: 'Applying platform-specific styles',
          metadata: { platform: 'ios' },
        })
      );
    });

    it('should clamp progress to 0-100 range', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      await service.trackProgress(mockProjectId, 'code_generation', 150);
      expect((callback.mock.calls[0][0] as ProgressEvent).progress).toBe(100);

      await service.trackProgress(mockProjectId, 'code_generation', -10);
      expect((callback.mock.calls[1][0] as ProgressEvent).progress).toBe(0);
    });

    it('should track phase completion', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      await service.trackPhaseComplete(mockProjectId, 'screen_mapping', {
        screens: ['Home', 'Profile'],
      });

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'phase_complete',
          phase: 'screen_mapping',
          progress: 100,
          message: 'Completed screen mapping',
          metadata: {
            result: { screens: ['Home', 'Profile'] },
          },
        })
      );
    });

    it('should track phase errors', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      await service.trackPhaseError(
        mockProjectId,
        'code_generation',
        'TypeScript compilation failed'
      );

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'phase_error',
          phase: 'code_generation',
          error: 'TypeScript compilation failed',
          message: 'Error in code generation: TypeScript compilation failed',
        })
      );
    });

    it('should track workflow completion', async () => {
      const callback = jest.fn();
      service.subscribe(mockProjectId, callback);

      await service.trackWorkflowComplete(mockProjectId);

      expect(callback).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'workflow_complete',
          phase: 'code_review',
          progress: 100,
          message: 'Workflow completed successfully',
        })
      );
    });
  });

  describe('Progress History', () => {
    it('should retrieve progress history for a project', async () => {
      const mockHistory = [
        {
          id: 'cp-1',
          project_id: mockProjectId,
          phase: 'problem_deconstruction',
          step_name: 'Analyzing user requirements',
          step_index: 0,
          total_steps: 5,
          progress_pct: 20,
          created_at: new Date().toISOString(),
        },
        {
          id: 'cp-2',
          project_id: mockProjectId,
          phase: 'problem_deconstruction',
          step_name: 'Extracting core features',
          step_index: 1,
          total_steps: 5,
          progress_pct: 40,
          created_at: new Date().toISOString(),
        },
      ];

      mockSupabaseClient.single.mockResolvedValue({ data: null, error: null });
      jest.spyOn(mockSupabaseClient, 'select').mockReturnValue({
        ...mockSupabaseClient,
        data: mockHistory,
        error: null,
      });

      const history = await service.getProgressHistory(mockProjectId);

      expect(history).toHaveLength(2);
      expect(history[0].step_name).toBe('Analyzing user requirements');
      expect(history[1].step_name).toBe('Extracting core features');
      expect(mockSupabaseClient.eq).toHaveBeenCalledWith('project_id', mockProjectId);
    });

    it('should retrieve latest progress for a project', async () => {
      const mockLatest = {
        id: 'cp-1',
        project_id: mockProjectId,
        phase: 'code_generation',
        step_name: 'Running TypeScript checks',
        step_index: 6,
        total_steps: 8,
        progress_pct: 87,
        created_at: new Date().toISOString(),
      };

      mockSupabaseClient.single.mockResolvedValue({ data: mockLatest, error: null });

      const latest = await service.getLatestProgress(mockProjectId);

      expect(latest).not.toBeNull();
      expect(latest?.phase).toBe('code_generation');
      expect(latest?.progress_pct).toBe(87);
      expect(mockSupabaseClient.limit).toHaveBeenCalledWith(1);
    });

    it('should return null if no progress exists', async () => {
      mockSupabaseClient.single.mockResolvedValue({
        data: null,
        error: { code: 'PGRST116' },
      });

      const latest = await service.getLatestProgress(mockProjectId);

      expect(latest).toBeNull();
    });

    it('should clear progress history for a project', async () => {
      mockSupabaseClient.delete.mockResolvedValue({ error: null });

      await service.clearProgress(mockProjectId);

      expect(mockSupabaseClient.from).toHaveBeenCalledWith('progress_checkpoints');
      expect(mockSupabaseClient.delete).toHaveBeenCalled();
      expect(mockSupabaseClient.eq).toHaveBeenCalledWith('project_id', mockProjectId);
    });
  });

  describe('Phase Steps', () => {
    it('should return all steps for a phase', () => {
      const steps = service.getPhaseSteps('code_generation');

      expect(steps).toHaveLength(8);
      expect(steps[0]).toBe('Initializing Expo project');
      expect(steps[7]).toBe('Building project');
    });

    it('should have steps defined for all phases', () => {
      const phases = [
        'problem_deconstruction',
        'screen_mapping',
        'design_generation',
        'stitch_iteration',
        'code_generation',
        'code_review',
      ] as const;

      phases.forEach((phase) => {
        const steps = service.getPhaseSteps(phase);
        expect(steps.length).toBeGreaterThan(0);
      });
    });
  });

  describe('Workflow Progress Calculation', () => {
    it('should calculate overall workflow progress', async () => {
      const mockHistory = [
        {
          id: 'cp-1',
          project_id: mockProjectId,
          phase: 'problem_deconstruction',
          step_name: 'Complete',
          step_index: 4,
          total_steps: 5,
          progress_pct: 100,
          created_at: new Date().toISOString(),
        },
        {
          id: 'cp-2',
          project_id: mockProjectId,
          phase: 'screen_mapping',
          step_name: 'Complete',
          step_index: 4,
          total_steps: 5,
          progress_pct: 100,
          created_at: new Date().toISOString(),
        },
        {
          id: 'cp-3',
          project_id: mockProjectId,
          phase: 'design_generation',
          step_name: 'In progress',
          step_index: 2,
          total_steps: 6,
          progress_pct: 50,
          created_at: new Date().toISOString(),
        },
      ];

      mockSupabaseClient.single.mockResolvedValue({ data: null, error: null });
      jest.spyOn(mockSupabaseClient, 'select').mockReturnValue({
        ...mockSupabaseClient,
        data: mockHistory,
        error: null,
      });

      const overallProgress = await service.calculateWorkflowProgress(mockProjectId);

      // 2 complete phases (100%) + 1 at 50% = (100 + 100 + 50) / 6 ≈ 42%
      expect(overallProgress).toBeGreaterThanOrEqual(35);
      expect(overallProgress).toBeLessThanOrEqual(50);
    });

    it('should return 0 for projects with no progress', async () => {
      jest.spyOn(mockSupabaseClient, 'select').mockReturnValue({
        ...mockSupabaseClient,
        data: [],
        error: null,
      });

      const overallProgress = await service.calculateWorkflowProgress(mockProjectId);

      expect(overallProgress).toBe(0);
    });
  });
});
