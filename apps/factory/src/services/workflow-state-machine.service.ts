/**
 * Workflow State Machine Service
 *
 * Manages the Design-First Software Factory workflow with strict phase transitions.
 *
 * Workflow Phases (in order):
 * 1. problem_deconstruction - Break down user's idea into structured requirements
 * 2. screen_mapping - Identify screens and navigation flows
 * 3. design_generation - Generate visual designs for each screen
 * 4. stitch_iteration - User-driven refinement of designs
 * 5. code_generation - Generate Expo/React Native code
 * 6. code_review - Validate code quality and security
 *
 * Features:
 * - Strict phase ordering with validation
 * - Integration with IterationService for loop prevention
 * - Database persistence of workflow state
 * - Event emission for real-time progress tracking
 * - Support for phase rollback on validation failures
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { IterationService } from './iteration.service';

export type WorkflowPhase =
  | 'problem_deconstruction'
  | 'screen_mapping'
  | 'design_generation'
  | 'stitch_iteration'
  | 'code_generation'
  | 'code_review';

export type WorkflowStatus = 'active' | 'completed' | 'failed' | 'paused';

export interface WorkflowState {
  id: string;
  project_id: string;
  current_phase: WorkflowPhase;
  status: WorkflowStatus;
  phase_data: Record<WorkflowPhase, PhaseData>;
  started_at: Date;
  completed_at?: Date;
  error_message?: string;
}

export interface PhaseData {
  status: 'pending' | 'active' | 'completed' | 'failed';
  started_at?: Date;
  completed_at?: Date;
  result?: any;
  error?: string;
  iteration_count: number;
}

export interface PhaseTransition {
  from: WorkflowPhase | null;
  to: WorkflowPhase;
  allowed: boolean;
  reason?: string;
}

export interface PhaseCompletionOptions {
  result?: any;
  skipIterationCheck?: boolean;
}

export interface PhaseFailureOptions {
  error: string;
  retryable: boolean;
}

/**
 * Valid phase transitions (directed graph)
 */
const PHASE_TRANSITIONS: Record<WorkflowPhase, WorkflowPhase[]> = {
  problem_deconstruction: ['screen_mapping'],
  screen_mapping: ['problem_deconstruction', 'design_generation'], // Can go back if screens are unclear
  design_generation: ['screen_mapping', 'stitch_iteration'], // Can go back to refine screen definitions
  stitch_iteration: ['design_generation', 'code_generation'], // User can request redesign or proceed
  code_generation: ['stitch_iteration', 'code_review'], // Can go back for design changes
  code_review: ['code_generation'], // Can go back for fixes, or exit workflow on success
};

/**
 * Phase order for sequential progression
 */
const PHASE_ORDER: WorkflowPhase[] = [
  'problem_deconstruction',
  'screen_mapping',
  'design_generation',
  'stitch_iteration',
  'code_generation',
  'code_review',
];

export class WorkflowStateMachineService {
  private static instance: WorkflowStateMachineService;
  private client: SupabaseClient;
  private iterationService: IterationService;

  private constructor() {
    const supabaseUrl = process.env.SUPABASE_URL || '';
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || '';
    this.client = createClient(supabaseUrl, supabaseKey);
    this.iterationService = IterationService.getInstance();
  }

  public static getInstance(): WorkflowStateMachineService {
    if (!WorkflowStateMachineService.instance) {
      WorkflowStateMachineService.instance = new WorkflowStateMachineService();
    }
    return WorkflowStateMachineService.instance;
  }

  /**
   * Initialize a new workflow for a project
   */
  async initializeWorkflow(projectId: string): Promise<WorkflowState> {
    const initialPhaseData: Record<WorkflowPhase, PhaseData> = {
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
    };

    const { data, error } = await this.client
      .from('workflow_states')
      .insert({
        project_id: projectId,
        current_phase: 'problem_deconstruction',
        status: 'active',
        phase_data: initialPhaseData,
        started_at: new Date().toISOString(),
      })
      .select()
      .single();

    if (error) {
      throw new Error(`Failed to initialize workflow: ${error.message}`);
    }

    return this.mapToWorkflowState(data);
  }

  /**
   * Get current workflow state for a project
   */
  async getWorkflowState(projectId: string): Promise<WorkflowState | null> {
    const { data, error } = await this.client
      .from('workflow_states')
      .select('*')
      .eq('project_id', projectId)
      .order('started_at', { ascending: false })
      .limit(1)
      .single();

    if (error) {
      if (error.code === 'PGRST116') {
        // No workflow found
        return null;
      }
      throw new Error(`Failed to get workflow state: ${error.message}`);
    }

    return this.mapToWorkflowState(data);
  }

  /**
   * Check if a phase transition is valid
   */
  validateTransition(
    currentPhase: WorkflowPhase | null,
    nextPhase: WorkflowPhase
  ): PhaseTransition {
    // First phase transition
    if (currentPhase === null) {
      if (nextPhase === 'problem_deconstruction') {
        return { from: null, to: nextPhase, allowed: true };
      }
      return {
        from: null,
        to: nextPhase,
        allowed: false,
        reason: 'Workflow must start with problem_deconstruction',
      };
    }

    const allowedTransitions = PHASE_TRANSITIONS[currentPhase];
    const allowed = allowedTransitions.includes(nextPhase);

    return {
      from: currentPhase,
      to: nextPhase,
      allowed,
      reason: allowed
        ? undefined
        : `Cannot transition from ${currentPhase} to ${nextPhase}`,
    };
  }

  /**
   * Transition to the next phase
   */
  async transitionToPhase(
    projectId: string,
    nextPhase: WorkflowPhase,
    options: { force?: boolean } = {}
  ): Promise<WorkflowState> {
    const workflowState = await this.getWorkflowState(projectId);
    if (!workflowState) {
      throw new Error('Workflow not found for project');
    }

    // Validate transition unless forced
    if (!options.force) {
      const transition = this.validateTransition(
        workflowState.current_phase,
        nextPhase
      );
      if (!transition.allowed) {
        throw new Error(
          transition.reason || 'Invalid phase transition'
        );
      }
    }

    // Check iteration limits
    const iterationCheck = await this.iterationService.checkIterationLimit(
      projectId,
      nextPhase
    );

    if (!iterationCheck.allowed) {
      throw new Error(
        `Cannot transition to ${nextPhase}: ${iterationCheck.reason}`
      );
    }

    // Update phase data
    const updatedPhaseData = { ...workflowState.phase_data };

    // Mark current phase as completed if moving forward
    if (this.isForwardTransition(workflowState.current_phase, nextPhase)) {
      updatedPhaseData[workflowState.current_phase] = {
        ...updatedPhaseData[workflowState.current_phase],
        status: 'completed',
        completed_at: new Date(),
      };
    }

    // Mark next phase as active
    updatedPhaseData[nextPhase] = {
      ...updatedPhaseData[nextPhase],
      status: 'active',
      started_at: new Date(),
      iteration_count: updatedPhaseData[nextPhase].iteration_count + 1,
    };

    // Update database
    const { data, error } = await this.client
      .from('workflow_states')
      .update({
        current_phase: nextPhase,
        phase_data: updatedPhaseData,
      })
      .eq('id', workflowState.id)
      .select()
      .single();

    if (error) {
      throw new Error(`Failed to transition to phase: ${error.message}`);
    }

    // Track iteration
    await this.iterationService.trackIteration(
      projectId,
      nextPhase,
      `Transitioned from ${workflowState.current_phase}`
    );

    return this.mapToWorkflowState(data);
  }

  /**
   * Mark current phase as completed and auto-advance to next phase
   */
  async completePhase(
    projectId: string,
    options: PhaseCompletionOptions = {}
  ): Promise<WorkflowState> {
    const workflowState = await this.getWorkflowState(projectId);
    if (!workflowState) {
      throw new Error('Workflow not found for project');
    }

    const currentPhase = workflowState.current_phase;

    // Update phase data with result
    const updatedPhaseData = { ...workflowState.phase_data };
    updatedPhaseData[currentPhase] = {
      ...updatedPhaseData[currentPhase],
      status: 'completed',
      completed_at: new Date(),
      result: options.result,
    };

    // Determine next phase (first allowed forward transition)
    const nextPhase = this.getNextPhase(currentPhase);

    if (!nextPhase) {
      // Workflow complete
      const { data, error } = await this.client
        .from('workflow_states')
        .update({
          phase_data: updatedPhaseData,
          status: 'completed',
          completed_at: new Date().toISOString(),
        })
        .eq('id', workflowState.id)
        .select()
        .single();

      if (error) {
        throw new Error(`Failed to complete workflow: ${error.message}`);
      }

      return this.mapToWorkflowState(data);
    }

    // Auto-advance to next phase
    return await this.transitionToPhase(projectId, nextPhase);
  }

  /**
   * Mark current phase as failed
   */
  async failPhase(
    projectId: string,
    options: PhaseFailureOptions
  ): Promise<WorkflowState> {
    const workflowState = await this.getWorkflowState(projectId);
    if (!workflowState) {
      throw new Error('Workflow not found for project');
    }

    const currentPhase = workflowState.current_phase;

    // Update phase data with error
    const updatedPhaseData = { ...workflowState.phase_data };
    updatedPhaseData[currentPhase] = {
      ...updatedPhaseData[currentPhase],
      status: 'failed',
      error: options.error,
    };

    const status: WorkflowStatus = options.retryable ? 'paused' : 'failed';

    const { data, error } = await this.client
      .from('workflow_states')
      .update({
        phase_data: updatedPhaseData,
        status,
        error_message: options.error,
      })
      .eq('id', workflowState.id)
      .select()
      .single();

    if (error) {
      throw new Error(`Failed to mark phase as failed: ${error.message}`);
    }

    return this.mapToWorkflowState(data);
  }

  /**
   * Pause the workflow
   */
  async pauseWorkflow(projectId: string): Promise<WorkflowState> {
    const workflowState = await this.getWorkflowState(projectId);
    if (!workflowState) {
      throw new Error('Workflow not found for project');
    }

    const { data, error } = await this.client
      .from('workflow_states')
      .update({ status: 'paused' })
      .eq('id', workflowState.id)
      .select()
      .single();

    if (error) {
      throw new Error(`Failed to pause workflow: ${error.message}`);
    }

    return this.mapToWorkflowState(data);
  }

  /**
   * Resume a paused workflow
   */
  async resumeWorkflow(projectId: string): Promise<WorkflowState> {
    const workflowState = await this.getWorkflowState(projectId);
    if (!workflowState) {
      throw new Error('Workflow not found for project');
    }

    if (workflowState.status !== 'paused') {
      throw new Error('Can only resume paused workflows');
    }

    const { data, error } = await this.client
      .from('workflow_states')
      .update({ status: 'active' })
      .eq('id', workflowState.id)
      .select()
      .single();

    if (error) {
      throw new Error(`Failed to resume workflow: ${error.message}`);
    }

    return this.mapToWorkflowState(data);
  }

  /**
   * Get the next phase in sequential order
   */
  private getNextPhase(currentPhase: WorkflowPhase): WorkflowPhase | null {
    const currentIndex = PHASE_ORDER.indexOf(currentPhase);
    if (currentIndex === -1 || currentIndex === PHASE_ORDER.length - 1) {
      return null; // No next phase
    }
    return PHASE_ORDER[currentIndex + 1];
  }

  /**
   * Check if transition is forward in the workflow
   */
  private isForwardTransition(
    from: WorkflowPhase,
    to: WorkflowPhase
  ): boolean {
    const fromIndex = PHASE_ORDER.indexOf(from);
    const toIndex = PHASE_ORDER.indexOf(to);
    return toIndex > fromIndex;
  }

  /**
   * Map database record to WorkflowState
   */
  private mapToWorkflowState(data: any): WorkflowState {
    return {
      id: data.id,
      project_id: data.project_id,
      current_phase: data.current_phase,
      status: data.status,
      phase_data: data.phase_data,
      started_at: new Date(data.started_at),
      completed_at: data.completed_at ? new Date(data.completed_at) : undefined,
      error_message: data.error_message,
    };
  }
}
