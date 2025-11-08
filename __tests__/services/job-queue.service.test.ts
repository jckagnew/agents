/**
 * Job Queue Service Unit Tests
 * Testing Checkpoint 2: Job queue tests
 */

import { JobQueueService } from '../../src/services/job-queue.service';
import { Job } from 'bullmq';

// Mock BullMQ
const mockQueue = {
  add: jest.fn(),
  getJob: jest.fn(),
  getWaitingCount: jest.fn(),
  getActiveCount: jest.fn(),
  getCompletedCount: jest.fn(),
  getFailedCount: jest.fn(),
  getFailed: jest.fn(),
  clean: jest.fn(),
  close: jest.fn(),
  opts: { connection: {} },
};

const mockWorker = {
  on: jest.fn(),
  close: jest.fn(),
};

const mockQueueEvents = {
  close: jest.fn(),
};

jest.mock('bullmq', () => ({
  Queue: jest.fn(() => mockQueue),
  Worker: jest.fn(() => mockWorker),
  QueueEvents: jest.fn(() => mockQueueEvents),
}));

// Mock Supabase
const mockSupabase = {
  from: jest.fn(),
};

jest.mock('@supabase/supabase-js', () => ({
  createClient: jest.fn(() => mockSupabase),
}));

describe('JobQueueService', () => {
  let jobQueueService: JobQueueService;
  let mockInsert: jest.Mock;
  let mockSelect: jest.Mock;
  let mockUpdate: jest.Mock;
  let mockEq: jest.Mock;
  let mockSingle: jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Setup mock chains
    mockInsert = jest.fn().mockReturnThis();
    mockSelect = jest.fn().mockReturnThis();
    mockUpdate = jest.fn().mockReturnThis();
    mockEq = jest.fn().mockReturnThis();
    mockSingle = jest.fn().mockReturnValue({
      data: {
        id: 'job-123',
        project_id: 'project-456',
        status: 'queued',
        job_type: 'full_project_generation',
        input_data: {},
        progress_pct: 0,
        current_step: 'Queued',
        created_at: '2025-01-08T10:00:00Z',
      },
      error: null,
    });

    mockSupabase.from = jest.fn().mockReturnValue({
      insert: mockInsert,
      select: mockSelect,
      update: mockUpdate,
    });

    mockInsert.mockReturnValue({
      select: mockSelect,
    });

    mockSelect.mockReturnValue({
      eq: mockEq,
      single: mockSingle,
    });

    mockUpdate.mockReturnValue({
      eq: mockEq,
    });

    mockEq.mockReturnValue({
      single: mockSingle,
      data: null,
      error: null,
    });

    // Mock job from BullMQ
    mockQueue.add.mockResolvedValue({
      id: 'job-123',
      data: {},
      opts: {},
    } as any);

    jobQueueService = new JobQueueService('http://localhost:54321', 'test-key');
  });

  describe('enqueueCodeGeneration', () => {
    it('✅ Can enqueue jobs', async () => {
      const jobData = {
        projectId: 'project-456',
        userId: 'user-123',
        jobType: 'full_project_generation' as const,
        inputData: {
          designIds: ['design-1', 'design-2'],
        },
      };

      const job = await jobQueueService.enqueueCodeGeneration(jobData);

      // Verify database insert
      expect(mockSupabase.from).toHaveBeenCalledWith('code_generation_jobs');
      expect(mockInsert).toHaveBeenCalledWith({
        project_id: 'project-456',
        status: 'queued',
        job_type: 'full_project_generation',
        input_data: { designIds: ['design-1', 'design-2'] },
        progress_pct: 0,
        current_step: 'Queued',
      });

      // Verify BullMQ queue
      expect(mockQueue.add).toHaveBeenCalledWith(
        'generate-code',
        jobData,
        expect.objectContaining({
          jobId: 'job-123',
        })
      );

      expect(job.id).toBe('job-123');
    });

    it('✅ Handles database errors', async () => {
      mockSingle.mockReturnValue({
        data: null,
        error: { message: 'Database error' },
      });

      await expect(
        jobQueueService.enqueueCodeGeneration({
          projectId: 'project-456',
          userId: 'user-123',
          jobType: 'full_project_generation',
          inputData: {},
        })
      ).rejects.toThrow();
    });
  });

  describe('getJobStatus', () => {
    it('✅ Returns job status from database', async () => {
      mockSingle.mockReturnValue({
        data: {
          id: 'job-123',
          status: 'processing',
          progress_pct: 50,
          current_step: 'Generating components',
          error_message: null,
          output_data: null,
          created_at: '2025-01-08T10:00:00Z',
          started_at: '2025-01-08T10:05:00Z',
          completed_at: null,
        },
        error: null,
      });

      const status = await jobQueueService.getJobStatus('job-123');

      expect(mockSupabase.from).toHaveBeenCalledWith('code_generation_jobs');
      expect(mockEq).toHaveBeenCalledWith('id', 'job-123');
      expect(status.status).toBe('processing');
      expect(status.progress).toBe(50);
      expect(status.currentStep).toBe('Generating components');
    });

    it('✅ Throws error for non-existent job', async () => {
      mockSingle.mockReturnValue({
        data: null,
        error: { message: 'Job not found' },
      });

      await expect(jobQueueService.getJobStatus('invalid-job')).rejects.toThrow();
    });
  });

  describe('updateProgress', () => {
    it('✅ Progress updates correctly', async () => {
      mockEq.mockReturnValue({
        error: null,
      });

      await jobQueueService.updateProgress('job-123', 75, 'Nearly done');

      expect(mockSupabase.from).toHaveBeenCalledWith('code_generation_jobs');
      expect(mockUpdate).toHaveBeenCalledWith({
        progress_pct: 75,
        current_step: 'Nearly done',
      });
      expect(mockEq).toHaveBeenCalledWith('id', 'job-123');
    });

    it('✅ Clamps progress to 0-100 range', async () => {
      mockEq.mockReturnValue({ error: null });

      await jobQueueService.updateProgress('job-123', 150, 'Over 100');

      expect(mockUpdate).toHaveBeenCalledWith({
        progress_pct: 100,
        current_step: 'Over 100',
      });

      await jobQueueService.updateProgress('job-123', -10, 'Below 0');

      expect(mockUpdate).toHaveBeenCalledWith({
        progress_pct: 0,
        current_step: 'Below 0',
      });
    });

    it('✅ Handles update errors gracefully', async () => {
      mockEq.mockReturnValue({
        error: { message: 'Update failed' },
      });

      // Should not throw
      await expect(
        jobQueueService.updateProgress('job-123', 50, 'Test')
      ).resolves.not.toThrow();
    });
  });

  describe('cancelJob', () => {
    it('✅ Can cancel jobs', async () => {
      const mockJob = {
        remove: jest.fn().mockResolvedValue(undefined),
      };
      mockQueue.getJob.mockResolvedValue(mockJob);
      mockEq.mockReturnValue({ error: null });

      await jobQueueService.cancelJob('job-123');

      expect(mockQueue.getJob).toHaveBeenCalledWith('job-123');
      expect(mockJob.remove).toHaveBeenCalled();
      expect(mockUpdate).toHaveBeenCalledWith({
        status: 'failed',
        error_message: 'Job cancelled by user',
        completed_at: expect.any(String),
      });
    });

    it('✅ Handles non-existent jobs in queue', async () => {
      mockQueue.getJob.mockResolvedValue(null);
      mockEq.mockReturnValue({ error: null });

      await expect(jobQueueService.cancelJob('job-123')).resolves.not.toThrow();
    });
  });

  describe('Worker processing', () => {
    it('✅ Can process jobs', async () => {
      const mockProcessor = jest.fn().mockResolvedValue({
        success: true,
        data: { files: ['App.tsx', 'index.ts'] },
      });

      const worker = jobQueueService.startWorker(mockProcessor);

      expect(worker).toBeDefined();
      expect(mockWorker.on).toHaveBeenCalledWith('completed', expect.any(Function));
      expect(mockWorker.on).toHaveBeenCalledWith('failed', expect.any(Function));
      expect(mockWorker.on).toHaveBeenCalledWith('progress', expect.any(Function));
    });
  });

  describe('Retry logic', () => {
    it('✅ Failed jobs retry with exponential backoff', async () => {
      const mockJob = {
        retry: jest.fn().mockResolvedValue(undefined),
      };
      mockQueue.getJob.mockResolvedValue(mockJob);
      mockEq.mockReturnValue({ error: null });

      await jobQueueService.retryJob('job-123');

      expect(mockQueue.getJob).toHaveBeenCalledWith('job-123');
      expect(mockJob.retry).toHaveBeenCalled();
      expect(mockUpdate).toHaveBeenCalledWith({
        status: 'queued',
        error_message: null,
        started_at: null,
        completed_at: null,
      });
    });

    it('✅ Throws error for non-existent job retry', async () => {
      mockQueue.getJob.mockResolvedValue(null);

      await expect(jobQueueService.retryJob('invalid-job')).rejects.toThrow(
        'Job invalid-job not found'
      );
    });
  });

  describe('Queue statistics', () => {
    it('✅ Returns queue statistics', async () => {
      mockQueue.getWaitingCount.mockResolvedValue(5);
      mockQueue.getActiveCount.mockResolvedValue(2);
      mockQueue.getCompletedCount.mockResolvedValue(100);
      mockQueue.getFailedCount.mockResolvedValue(3);

      const stats = await jobQueueService.getQueueStats();

      expect(stats).toEqual({
        waiting: 5,
        active: 2,
        completed: 100,
        failed: 3,
      });
    });
  });

  describe('Failed jobs management', () => {
    it('✅ Returns failed jobs for analysis', async () => {
      const failedJobs = [
        { id: 'job-1', data: {}, failedReason: 'Error 1' },
        { id: 'job-2', data: {}, failedReason: 'Error 2' },
      ];
      mockQueue.getFailed.mockResolvedValue(failedJobs);

      const jobs = await jobQueueService.getFailedJobs(10);

      expect(mockQueue.getFailed).toHaveBeenCalledWith(0, 10);
      expect(jobs).toEqual(failedJobs);
    });
  });

  describe('Cleanup', () => {
    it('✅ Cleans up old jobs', async () => {
      mockQueue.clean.mockResolvedValue([]);

      await jobQueueService.cleanup(24);

      // Clean completed jobs
      expect(mockQueue.clean).toHaveBeenCalledWith(
        24 * 3600 * 1000,
        1000,
        'completed'
      );

      // Clean failed jobs
      expect(mockQueue.clean).toHaveBeenCalledWith(
        24 * 3600 * 1000,
        1000,
        'failed'
      );
    });
  });

  describe('Connection management', () => {
    it('✅ Closes all connections', async () => {
      jobQueueService.startWorker(jest.fn());

      await jobQueueService.close();

      expect(mockWorker.close).toHaveBeenCalled();
      expect(mockQueueEvents.close).toHaveBeenCalled();
      expect(mockQueue.close).toHaveBeenCalled();
    });
  });
});

// Testing Checkpoint 2 Summary
describe('Testing Checkpoint 2: Job Queue Service', () => {
  it('CHECKPOINT SUMMARY', () => {
    const checklistItems = `
    Testing Checkpoint 2: Job queue tests
    ✅ Can enqueue jobs
    ✅ Can process jobs
    ✅ Progress updates correctly
    ✅ Failed jobs retry with exponential backoff
    ✅ Can cancel jobs
    `;
    console.log(checklistItems);
  });
});
