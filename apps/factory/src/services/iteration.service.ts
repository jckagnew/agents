/**
 * Iteration Service
 * Tracks and limits iterations per workflow phase to prevent infinite loops
 *
 * Features:
 * - Per-phase iteration tracking
 * - Configurable limits
 * - Automatic limit enforcement
 * - Iteration reason tracking
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';

export type WorkflowPhase =
  | 'problem_deconstruction'
  | 'screen_mapping'
  | 'design_generation'
  | 'stitch_iteration'
  | 'code_generation'
  | 'code_review';

export interface IterationRecord {
  id: string;
  project_id: string;
  phase: WorkflowPhase;
  iteration_count: number;
  max_iterations: number;
  last_iteration_reason: string | null;
  created_at: Date;
  updated_at: Date;
}

export interface IterationCheckResult {
  within_limit: boolean;
  allowed: boolean; // Alias for within_limit for backwards compatibility
  current_iteration: number;
  max_iterations: number;
  remaining_iterations: number;
  reason?: string; // Optional reason if limit exceeded
}

/**
 * Default max iterations per phase
 */
export const DEFAULT_MAX_ITERATIONS: Record<WorkflowPhase, number> = {
  problem_deconstruction: 3,
  screen_mapping: 3,
  design_generation: 5,
  stitch_iteration: 10, // User-driven, allow more
  code_generation: 3,
  code_review: 5,
};

/**
 * Iteration Service
 */
export class IterationService {
  private static instance: IterationService;
  private client: SupabaseClient;

  constructor(supabaseUrl: string, supabaseKey: string) {
    this.client = createClient(supabaseUrl, supabaseKey);
  }

  /**
   * Get singleton instance
   */
  static getInstance(supabaseUrl?: string, supabaseKey?: string): IterationService {
    if (!IterationService.instance) {
      if (!supabaseUrl || !supabaseKey) {
        // Try to get from environment
        supabaseUrl = process.env.SUPABASE_URL;
        supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
      }
      if (!supabaseUrl || !supabaseKey) {
        throw new Error('Supabase credentials required to initialize IterationService');
      }
      IterationService.instance = new IterationService(supabaseUrl, supabaseKey);
    }
    return IterationService.instance;
  }

  /**
   * Track an iteration for a project phase
   */
  async trackIteration(
    projectId: string,
    phase: WorkflowPhase,
    reason?: string
  ): Promise<IterationCheckResult> {
    // Use database function to increment (atomic operation)
    const { data, error } = await this.client.rpc('increment_iteration', {
      p_project_id: projectId,
      p_phase: phase,
      p_reason: reason || null,
    });

    if (error) {
      // Fallback to manual tracking if function doesn't exist
      return this.trackIterationManual(projectId, phase, reason);
    }

    // Get updated record
    return this.checkIterationLimit(projectId, phase);
  }

  /**
   * Check if within iteration limit
   */
  async checkIterationLimit(
    projectId: string,
    phase: WorkflowPhase
  ): Promise<IterationCheckResult> {
    const { data, error } = await this.client
      .from('iteration_tracking')
      .select('*')
      .eq('project_id', projectId)
      .eq('phase', phase)
      .single();

    if (error && error.code !== 'PGRST116') {
      throw error;
    }

    if (!data) {
      // No record yet, first iteration
      return {
        within_limit: true,
        allowed: true,
        current_iteration: 0,
        max_iterations: DEFAULT_MAX_ITERATIONS[phase],
        remaining_iterations: DEFAULT_MAX_ITERATIONS[phase],
      };
    }

    const remaining = data.max_iterations - data.iteration_count;
    const withinLimit = data.iteration_count < data.max_iterations;

    return {
      within_limit: withinLimit,
      allowed: withinLimit,
      current_iteration: data.iteration_count,
      max_iterations: data.max_iterations,
      remaining_iterations: Math.max(0, remaining),
      reason: withinLimit ? undefined : 'iteration_limit_exceeded',
    };
  }

  /**
   * Reset iterations for a phase
   */
  async resetIterations(projectId: string, phase: WorkflowPhase): Promise<void> {
    const { error } = await this.client
      .from('iteration_tracking')
      .update({
        iteration_count: 0,
        last_iteration_reason: null,
        updated_at: new Date().toISOString(),
      })
      .eq('project_id', projectId)
      .eq('phase', phase);

    if (error) throw error;
  }

  /**
   * Get all iteration records for a project
   */
  async getProjectIterations(projectId: string): Promise<IterationRecord[]> {
    const { data, error } = await this.client
      .from('iteration_tracking')
      .select('*')
      .eq('project_id', projectId);

    if (error) throw error;

    return (data || []).map((record) => ({
      ...record,
      created_at: new Date(record.created_at),
      updated_at: new Date(record.updated_at),
    }));
  }

  /**
   * Update max iterations for a phase
   */
  async updateMaxIterations(
    projectId: string,
    phase: WorkflowPhase,
    maxIterations: number
  ): Promise<void> {
    // Try to update existing record
    const { error: updateError } = await this.client
      .from('iteration_tracking')
      .update({
        max_iterations: maxIterations,
        updated_at: new Date().toISOString(),
      })
      .eq('project_id', projectId)
      .eq('phase', phase);

    if (updateError && updateError.code === 'PGRST116') {
      // Record doesn't exist, create it
      const { error: insertError } = await this.client
        .from('iteration_tracking')
        .insert({
          project_id: projectId,
          phase,
          iteration_count: 0,
          max_iterations: maxIterations,
        });

      if (insertError) throw insertError;
    } else if (updateError) {
      throw updateError;
    }
  }

  /**
   * Check if any phase has exceeded limits
   */
  async hasExceededLimits(projectId: string): Promise<{
    exceeded: boolean;
    phases: WorkflowPhase[];
  }> {
    const iterations = await this.getProjectIterations(projectId);

    const exceededPhases = iterations
      .filter((record) => record.iteration_count >= record.max_iterations)
      .map((record) => record.phase as WorkflowPhase);

    return {
      exceeded: exceededPhases.length > 0,
      phases: exceededPhases,
    };
  }

  /**
   * Get iteration statistics
   */
  async getIterationStats(projectId: string): Promise<{
    total_iterations: number;
    phases_tracked: number;
    phases_at_limit: number;
    most_iterated_phase: { phase: WorkflowPhase; count: number } | null;
  }> {
    const iterations = await this.getProjectIterations(projectId);

    const totalIterations = iterations.reduce(
      (sum, record) => sum + record.iteration_count,
      0
    );

    const phasesAtLimit = iterations.filter(
      (record) => record.iteration_count >= record.max_iterations
    ).length;

    const mostIteratedPhase = iterations.reduce(
      (max, record) => {
        return record.iteration_count > (max?.count || 0)
          ? { phase: record.phase as WorkflowPhase, count: record.iteration_count }
          : max;
      },
      null as { phase: WorkflowPhase; count: number } | null
    );

    return {
      total_iterations: totalIterations,
      phases_tracked: iterations.length,
      phases_at_limit: phasesAtLimit,
      most_iterated_phase: mostIteratedPhase,
    };
  }

  /**
   * Manual iteration tracking (fallback)
   */
  private async trackIterationManual(
    projectId: string,
    phase: WorkflowPhase,
    reason?: string
  ): Promise<IterationCheckResult> {
    // Try to get existing record
    const { data: existing } = await this.client
      .from('iteration_tracking')
      .select('*')
      .eq('project_id', projectId)
      .eq('phase', phase)
      .single();

    if (existing) {
      // Update existing
      const newCount = existing.iteration_count + 1;

      await this.client
        .from('iteration_tracking')
        .update({
          iteration_count: newCount,
          last_iteration_reason: reason || existing.last_iteration_reason,
          updated_at: new Date().toISOString(),
        })
        .eq('project_id', projectId)
        .eq('phase', phase);

      const remaining = existing.max_iterations - newCount;

      return {
        within_limit: newCount < existing.max_iterations,
        current_iteration: newCount,
        max_iterations: existing.max_iterations,
        remaining_iterations: Math.max(0, remaining),
      };
    } else {
      // Create new record
      const maxIterations = DEFAULT_MAX_ITERATIONS[phase];

      await this.client.from('iteration_tracking').insert({
        project_id: projectId,
        phase,
        iteration_count: 1,
        max_iterations: maxIterations,
        last_iteration_reason: reason || null,
      });

      return {
        within_limit: true,
        current_iteration: 1,
        max_iterations: maxIterations,
        remaining_iterations: maxIterations - 1,
      };
    }
  }
}

/**
 * Singleton instance
 */
let iterationServiceInstance: IterationService | null = null;

export function getIterationService(
  supabaseUrl?: string,
  supabaseKey?: string
): IterationService {
  if (!iterationServiceInstance && (!supabaseUrl || !supabaseKey)) {
    throw new Error('Supabase config required to initialize IterationService');
  }

  if (supabaseUrl && supabaseKey && !iterationServiceInstance) {
    iterationServiceInstance = new IterationService(supabaseUrl, supabaseKey);
  }

  return iterationServiceInstance!;
}
