/**
 * Job Queue Service
 * Manages background code generation jobs using BullMQ
 *
 * Features:
 * - Job enqueueing and processing
 * - Progress tracking
 * - Automatic retries with exponential backoff
 * - Job cancellation
 * - Dead letter queue for failed jobs
 */

import { Queue, Worker, Job, QueueEvents } from 'bullmq';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

export interface CodeGenerationJobData {
  projectId: string;
  userId: string;
  jobType: 'html_to_react_native' | 'full_project_generation';
  inputData: {
    designIds?: string[];
    prdData?: any;
    [key: string]: any;
  };
}

export interface JobStatus {
  id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress: number;
  currentStep?: string;
  error?: string;
  result?: any;
  createdAt: Date;
  startedAt?: Date;
  completedAt?: Date;
}

export interface JobResult {
  success: boolean;
  data?: any;
  error?: string;
}

/**
 * Job Queue Service using BullMQ
 */
export class JobQueueService {
  private queue: Queue<CodeGenerationJobData>;
  private worker?: Worker<CodeGenerationJobData, JobResult>;
  private queueEvents?: QueueEvents;
  private supabase: SupabaseClient;

  constructor(
    supabaseUrl: string,
    supabaseKey: string,
    redisConnection?: {
      host: string;
      port: number;
      password?: string;
    }
  ) {
    // Default to localhost Redis for development
    const connection = redisConnection || {
      host: 'localhost',
      port: 6379,
    };

    // Initialize BullMQ queue
    this.queue = new Queue<CodeGenerationJobData>('code-generation', {
      connection,
      defaultJobOptions: {
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 2000, // Start with 2 seconds
        },
        removeOnComplete: {
          age: 24 * 3600, // Keep completed jobs for 24 hours
          count: 1000, // Keep max 1000 completed jobs
        },
        removeOnFail: false, // Keep failed jobs for analysis
      },
    });

    // Initialize Supabase client for database updates
    this.supabase = createClient(supabaseUrl, supabaseKey);

    // Initialize queue events
    this.queueEvents = new QueueEvents('code-generation', { connection });
  }

  /**
   * Enqueue a code generation job
   */
  async enqueueCodeGeneration(data: CodeGenerationJobData): Promise<Job> {
    // Create database record first
    const { data: dbJob, error: dbError } = await this.supabase
      .from('code_generation_jobs')
      .insert({
        project_id: data.projectId,
        status: 'queued',
        job_type: data.jobType,
        input_data: data.inputData,
        progress_pct: 0,
        current_step: 'Queued',
      })
      .select()
      .single();

    if (dbError) throw dbError;

    // Enqueue in BullMQ
    const job = await this.queue.add(
      'generate-code',
      data,
      {
        jobId: dbJob.id, // Use database ID as job ID
      }
    );

    return job;
  }

  /**
   * Get job status from database
   */
  async getJobStatus(jobId: string): Promise<JobStatus> {
    const { data, error } = await this.supabase
      .from('code_generation_jobs')
      .select('*')
      .eq('id', jobId)
      .single();

    if (error) throw error;
    if (!data) throw new Error(`Job ${jobId} not found`);

    return {
      id: data.id,
      status: data.status,
      progress: data.progress_pct || 0,
      currentStep: data.current_step,
      error: data.error_message,
      result: data.output_data,
      createdAt: new Date(data.created_at),
      startedAt: data.started_at ? new Date(data.started_at) : undefined,
      completedAt: data.completed_at ? new Date(data.completed_at) : undefined,
    };
  }

  /**
   * Update job progress
   */
  async updateProgress(
    jobId: string,
    progress: number,
    step: string
  ): Promise<void> {
    const { error } = await this.supabase
      .from('code_generation_jobs')
      .update({
        progress_pct: Math.min(100, Math.max(0, progress)),
        current_step: step,
      })
      .eq('id', jobId);

    if (error) {
      console.error('Failed to update job progress:', error);
    }
  }

  /**
   * Cancel a job
   */
  async cancelJob(jobId: string): Promise<void> {
    // Remove from queue
    const job = await this.queue.getJob(jobId);
    if (job) {
      await job.remove();
    }

    // Update database
    await this.supabase
      .from('code_generation_jobs')
      .update({
        status: 'failed',
        error_message: 'Job cancelled by user',
        completed_at: new Date().toISOString(),
      })
      .eq('id', jobId);
  }

  /**
   * Start worker to process jobs
   * This should be called in a separate process/server
   */
  startWorker(
    processor: (job: Job<CodeGenerationJobData>) => Promise<JobResult>
  ): Worker<CodeGenerationJobData, JobResult> {
    this.worker = new Worker<CodeGenerationJobData, JobResult>(
      'code-generation',
      async (job) => {
        try {
          // Update status to processing
          await this.supabase
            .from('code_generation_jobs')
            .update({
              status: 'processing',
              started_at: new Date().toISOString(),
              progress_pct: 0,
              current_step: 'Starting code generation',
            })
            .eq('id', job.id);

          // Process the job
          const result = await processor(job);

          // Update status to completed
          await this.supabase
            .from('code_generation_jobs')
            .update({
              status: 'completed',
              output_data: result.data,
              completed_at: new Date().toISOString(),
              progress_pct: 100,
              current_step: 'Completed',
            })
            .eq('id', job.id);

          return result;
        } catch (error: any) {
          // Update status to failed
          await this.supabase
            .from('code_generation_jobs')
            .update({
              status: 'failed',
              error_message: error.message,
              completed_at: new Date().toISOString(),
              retry_count: (job.attemptsMade || 0) + 1,
            })
            .eq('id', job.id);

          throw error;
        }
      },
      {
        connection: this.queue.opts.connection,
        concurrency: 3, // Process up to 3 jobs concurrently
      }
    );

    // Setup event handlers
    this.worker.on('completed', (job) => {
      console.log(`Job ${job.id} completed successfully`);
    });

    this.worker.on('failed', (job, error) => {
      console.error(`Job ${job?.id} failed:`, error.message);
    });

    this.worker.on('progress', (job, progress) => {
      console.log(`Job ${job.id} progress: ${progress}%`);
    });

    return this.worker;
  }

  /**
   * Get queue statistics
   */
  async getQueueStats(): Promise<{
    waiting: number;
    active: number;
    completed: number;
    failed: number;
  }> {
    const [waiting, active, completed, failed] = await Promise.all([
      this.queue.getWaitingCount(),
      this.queue.getActiveCount(),
      this.queue.getCompletedCount(),
      this.queue.getFailedCount(),
    ]);

    return { waiting, active, completed, failed };
  }

  /**
   * Get failed jobs for analysis
   */
  async getFailedJobs(limit: number = 10): Promise<Job<CodeGenerationJobData>[]> {
    return this.queue.getFailed(0, limit);
  }

  /**
   * Retry a failed job
   */
  async retryJob(jobId: string): Promise<void> {
    const job = await this.queue.getJob(jobId);
    if (!job) throw new Error(`Job ${jobId} not found`);

    await job.retry();

    // Reset database status
    await this.supabase
      .from('code_generation_jobs')
      .update({
        status: 'queued',
        error_message: null,
        started_at: null,
        completed_at: null,
      })
      .eq('id', jobId);
  }

  /**
   * Clean up old jobs
   */
  async cleanup(ageInHours: number = 24): Promise<void> {
    await this.queue.clean(ageInHours * 3600 * 1000, 1000, 'completed');
    await this.queue.clean(ageInHours * 3600 * 1000, 1000, 'failed');
  }

  /**
   * Close connections
   */
  async close(): Promise<void> {
    if (this.worker) {
      await this.worker.close();
    }
    if (this.queueEvents) {
      await this.queueEvents.close();
    }
    await this.queue.close();
  }
}

/**
 * Singleton instance
 */
let jobQueueServiceInstance: JobQueueService | null = null;

export function getJobQueueService(
  supabaseUrl?: string,
  supabaseKey?: string,
  redisConnection?: {
    host: string;
    port: number;
    password?: string;
  }
): JobQueueService {
  if (!jobQueueServiceInstance && (!supabaseUrl || !supabaseKey)) {
    throw new Error('Supabase config required to initialize JobQueueService');
  }

  if (supabaseUrl && supabaseKey && !jobQueueServiceInstance) {
    jobQueueServiceInstance = new JobQueueService(
      supabaseUrl,
      supabaseKey,
      redisConnection
    );
  }

  return jobQueueServiceInstance!;
}
