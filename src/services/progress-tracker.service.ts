/**
 * Progress Tracker Service
 *
 * Provides real-time progress updates via WebSocket for the Design-First Software Factory workflow.
 *
 * Features:
 * - Real-time WebSocket updates to connected clients
 * - Progress checkpoints with step-by-step tracking
 * - Integration with WorkflowStateMachine and JobQueueService
 * - Persistent progress storage in database
 * - Support for multiple concurrent project workflows
 *
 * Progress Flow:
 * 1. Client connects via WebSocket (project-specific channel)
 * 2. Service emits progress events as workflow advances
 * 3. Client receives real-time updates (phase changes, step completions, errors)
 * 4. Progress persisted to database for recovery/history
 */

import { WebSocket, WebSocketServer } from 'ws';
import { createClient, SupabaseClient, RealtimeChannel } from '@supabase/supabase-js';
import { WorkflowPhase } from './workflow-state-machine.service';

export interface ProgressEvent {
  type: 'phase_start' | 'phase_progress' | 'phase_complete' | 'phase_error' | 'workflow_complete';
  projectId: string;
  phase: WorkflowPhase;
  progress: number; // 0-100
  step?: string;
  message?: string;
  error?: string;
  metadata?: Record<string, any>;
  timestamp: Date;
}

export interface ProgressCheckpoint {
  id: string;
  project_id: string;
  phase: WorkflowPhase;
  step_name: string;
  step_index: number;
  total_steps: number;
  progress_pct: number;
  message?: string;
  metadata?: Record<string, any>;
  created_at: Date;
}

export interface ProgressSubscription {
  projectId: string;
  callback: (event: ProgressEvent) => void;
}

/**
 * Phase-specific steps for granular progress tracking
 */
const PHASE_STEPS: Record<WorkflowPhase, string[]> = {
  problem_deconstruction: [
    'Analyzing user requirements',
    'Extracting core features',
    'Identifying target platforms',
    'Defining success criteria',
    'Generating structured PRD',
  ],
  screen_mapping: [
    'Identifying user flows',
    'Mapping screens to features',
    'Defining navigation patterns',
    'Creating sitemap structure',
    'Validating screen coverage',
  ],
  design_generation: [
    'Loading design system tokens',
    'Generating component hierarchy',
    'Applying platform-specific styles',
    'Creating responsive layouts',
    'Validating accessibility',
    'Exporting design specifications',
  ],
  stitch_iteration: [
    'Presenting designs to user',
    'Collecting feedback',
    'Analyzing requested changes',
    'Regenerating affected components',
    'Validating design consistency',
  ],
  code_generation: [
    'Initializing Expo project',
    'Generating component files',
    'Implementing navigation',
    'Adding state management',
    'Integrating API calls',
    'Running ESLint',
    'Running TypeScript checks',
    'Building project',
  ],
  code_review: [
    'Running ESLint analysis',
    'Running TypeScript compiler',
    'Running Semgrep security scan',
    'Running npm audit',
    'Generating quality report',
    'Checking quality gates',
  ],
};

export class ProgressTrackerService {
  private static instance: ProgressTrackerService;
  private supabaseClient: SupabaseClient;
  private realtimeChannel: RealtimeChannel | null = null;
  private localSubscriptions: Map<string, Set<(event: ProgressEvent) => void>>;

  private constructor() {
    const supabaseUrl = process.env.SUPABASE_URL || '';
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || '';
    this.supabaseClient = createClient(supabaseUrl, supabaseKey);
    this.localSubscriptions = new Map();

    // Initialize Supabase Realtime
    this.initializeRealtime();
  }

  public static getInstance(): ProgressTrackerService {
    if (!ProgressTrackerService.instance) {
      ProgressTrackerService.instance = new ProgressTrackerService();
    }
    return ProgressTrackerService.instance;
  }

  /**
   * Initialize Supabase Realtime for broadcasting progress events
   */
  private initializeRealtime(): void {
    this.realtimeChannel = this.supabaseClient.channel('progress_events');
    this.realtimeChannel.subscribe((status) => {
      if (status === 'SUBSCRIBED') {
        console.log('Progress Tracker: Realtime channel subscribed');
      }
    });
  }

  /**
   * Subscribe to progress updates for a specific project (local in-process)
   */
  subscribe(projectId: string, callback: (event: ProgressEvent) => void): () => void {
    if (!this.localSubscriptions.has(projectId)) {
      this.localSubscriptions.set(projectId, new Set());
    }

    const subscribers = this.localSubscriptions.get(projectId)!;
    subscribers.add(callback);

    // Return unsubscribe function
    return () => {
      subscribers.delete(callback);
      if (subscribers.size === 0) {
        this.localSubscriptions.delete(projectId);
      }
    };
  }

  /**
   * Subscribe to progress updates via Supabase Realtime (for external clients)
   */
  subscribeRealtime(
    projectId: string,
    callback: (event: ProgressEvent) => void
  ): RealtimeChannel {
    const channel = this.supabaseClient
      .channel(`progress:${projectId}`)
      .on(
        'broadcast',
        { event: 'progress_update' },
        (payload: { payload: ProgressEvent }) => {
          callback(payload.payload);
        }
      )
      .subscribe();

    return channel;
  }

  /**
   * Emit a progress event to all subscribers
   */
  async emit(event: ProgressEvent): Promise<void> {
    const eventWithTimestamp = {
      ...event,
      timestamp: new Date(),
    };

    // Notify local subscribers
    const subscribers = this.localSubscriptions.get(event.projectId);
    if (subscribers) {
      subscribers.forEach((callback) => {
        try {
          callback(eventWithTimestamp);
        } catch (error) {
          console.error('Error in progress subscriber callback:', error);
        }
      });
    }

    // Broadcast via Supabase Realtime
    if (this.realtimeChannel) {
      await this.realtimeChannel.send({
        type: 'broadcast',
        event: 'progress_update',
        payload: eventWithTimestamp,
      });
    }

    // Save to database for history
    await this.saveProgressEvent(eventWithTimestamp);
  }

  /**
   * Track phase start with automatic step-by-step progress
   */
  async trackPhaseStart(projectId: string, phase: WorkflowPhase): Promise<void> {
    await this.emit({
      type: 'phase_start',
      projectId,
      phase,
      progress: 0,
      message: `Starting ${phase.replace(/_/g, ' ')}`,
      timestamp: new Date(),
    });
  }

  /**
   * Track a specific step within a phase
   */
  async trackStep(
    projectId: string,
    phase: WorkflowPhase,
    stepIndex: number,
    metadata?: Record<string, any>
  ): Promise<void> {
    const steps = PHASE_STEPS[phase];
    const stepName = steps[stepIndex];
    const totalSteps = steps.length;
    const progress = Math.round(((stepIndex + 1) / totalSteps) * 100);

    // Save checkpoint
    await this.saveCheckpoint({
      project_id: projectId,
      phase,
      step_name: stepName,
      step_index: stepIndex,
      total_steps: totalSteps,
      progress_pct: progress,
      metadata,
    });

    // Emit progress event
    await this.emit({
      type: 'phase_progress',
      projectId,
      phase,
      progress,
      step: stepName,
      message: stepName,
      metadata,
      timestamp: new Date(),
    });
  }

  /**
   * Track custom progress (for dynamic workflows)
   */
  async trackProgress(
    projectId: string,
    phase: WorkflowPhase,
    progress: number,
    step?: string,
    metadata?: Record<string, any>
  ): Promise<void> {
    await this.emit({
      type: 'phase_progress',
      projectId,
      phase,
      progress: Math.min(100, Math.max(0, progress)),
      step,
      message: step,
      metadata,
      timestamp: new Date(),
    });
  }

  /**
   * Track phase completion
   */
  async trackPhaseComplete(
    projectId: string,
    phase: WorkflowPhase,
    result?: any
  ): Promise<void> {
    await this.emit({
      type: 'phase_complete',
      projectId,
      phase,
      progress: 100,
      message: `Completed ${phase.replace(/_/g, ' ')}`,
      metadata: { result },
      timestamp: new Date(),
    });
  }

  /**
   * Track phase error
   */
  async trackPhaseError(
    projectId: string,
    phase: WorkflowPhase,
    error: string
  ): Promise<void> {
    await this.emit({
      type: 'phase_error',
      projectId,
      phase,
      progress: 0,
      error,
      message: `Error in ${phase.replace(/_/g, ' ')}: ${error}`,
      timestamp: new Date(),
    });
  }

  /**
   * Track workflow completion
   */
  async trackWorkflowComplete(projectId: string): Promise<void> {
    await this.emit({
      type: 'workflow_complete',
      projectId,
      phase: 'code_review', // Final phase
      progress: 100,
      message: 'Workflow completed successfully',
      timestamp: new Date(),
    });
  }

  /**
   * Get progress history for a project
   */
  async getProgressHistory(projectId: string): Promise<ProgressCheckpoint[]> {
    const { data, error } = await this.supabaseClient
      .from('progress_checkpoints')
      .select('*')
      .eq('project_id', projectId)
      .order('created_at', { ascending: true });

    if (error) {
      throw new Error(`Failed to get progress history: ${error.message}`);
    }

    return data.map((row) => ({
      id: row.id,
      project_id: row.project_id,
      phase: row.phase,
      step_name: row.step_name,
      step_index: row.step_index,
      total_steps: row.total_steps,
      progress_pct: row.progress_pct,
      message: row.message,
      metadata: row.metadata,
      created_at: new Date(row.created_at),
    }));
  }

  /**
   * Get latest progress for a project
   */
  async getLatestProgress(projectId: string): Promise<ProgressCheckpoint | null> {
    const { data, error } = await this.supabaseClient
      .from('progress_checkpoints')
      .select('*')
      .eq('project_id', projectId)
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    if (error) {
      if (error.code === 'PGRST116') {
        return null; // No checkpoints yet
      }
      throw new Error(`Failed to get latest progress: ${error.message}`);
    }

    return {
      id: data.id,
      project_id: data.project_id,
      phase: data.phase,
      step_name: data.step_name,
      step_index: data.step_index,
      total_steps: data.total_steps,
      progress_pct: data.progress_pct,
      message: data.message,
      metadata: data.metadata,
      created_at: new Date(data.created_at),
    };
  }

  /**
   * Clear progress history for a project
   */
  async clearProgress(projectId: string): Promise<void> {
    const { error } = await this.supabaseClient
      .from('progress_checkpoints')
      .delete()
      .eq('project_id', projectId);

    if (error) {
      throw new Error(`Failed to clear progress: ${error.message}`);
    }
  }

  /**
   * Save progress checkpoint to database
   */
  private async saveCheckpoint(
    checkpoint: Omit<ProgressCheckpoint, 'id' | 'created_at'>
  ): Promise<void> {
    const { error } = await this.supabaseClient
      .from('progress_checkpoints')
      .insert({
        project_id: checkpoint.project_id,
        phase: checkpoint.phase,
        step_name: checkpoint.step_name,
        step_index: checkpoint.step_index,
        total_steps: checkpoint.total_steps,
        progress_pct: checkpoint.progress_pct,
        message: checkpoint.metadata?.message,
        metadata: checkpoint.metadata || {},
      });

    if (error) {
      console.error('Failed to save progress checkpoint:', error);
      // Don't throw - progress tracking should not break workflow
    }
  }

  /**
   * Save progress event to database for history/analytics
   */
  private async saveProgressEvent(event: ProgressEvent): Promise<void> {
    try {
      await this.supabaseClient.from('progress_events').insert({
        project_id: event.projectId,
        event_type: event.type,
        phase: event.phase,
        progress_pct: event.progress,
        step: event.step,
        message: event.message,
        error: event.error,
        metadata: event.metadata || {},
        created_at: event.timestamp.toISOString(),
      });
    } catch (error) {
      console.error('Failed to save progress event:', error);
      // Don't throw - logging should not break workflow
    }
  }

  /**
   * Get all steps for a phase
   */
  getPhaseSteps(phase: WorkflowPhase): string[] {
    return PHASE_STEPS[phase];
  }

  /**
   * Calculate overall workflow progress (across all phases)
   */
  async calculateWorkflowProgress(projectId: string): Promise<number> {
    const history = await this.getProgressHistory(projectId);
    if (history.length === 0) return 0;

    // Get latest checkpoint for each phase
    const phaseProgress = new Map<WorkflowPhase, number>();
    history.forEach((checkpoint) => {
      phaseProgress.set(checkpoint.phase, checkpoint.progress_pct);
    });

    // Calculate average progress across all 6 phases
    const phases: WorkflowPhase[] = [
      'problem_deconstruction',
      'screen_mapping',
      'design_generation',
      'stitch_iteration',
      'code_generation',
      'code_review',
    ];

    let totalProgress = 0;
    phases.forEach((phase) => {
      totalProgress += phaseProgress.get(phase) || 0;
    });

    return Math.round(totalProgress / phases.length);
  }

  /**
   * Cleanup when service is destroyed
   */
  async destroy(): Promise<void> {
    if (this.realtimeChannel) {
      await this.supabaseClient.removeChannel(this.realtimeChannel);
      this.realtimeChannel = null;
    }
    this.localSubscriptions.clear();
  }
}
