/**
 * Supabase Service
 * Handles all database operations and integrates with Gemini service
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';
import {
  Project,
  ProjectIntake,
  InspirationWebsite,
  ProblemDeconstruction,
  ScreenMapping,
  StitchDesign,
  CodeGenerationJob,
  ProjectWithDetails,
} from '../types/project';
import { getGeminiService } from './gemini.service';

interface SupabaseConfig {
  url: string;
  anonKey: string;
  geminiApiKey: string;
}

/**
 * Main service for interacting with Supabase backend
 */
export class SupabaseService {
  private client: SupabaseClient;
  private geminiApiKey: string;

  constructor(config: SupabaseConfig) {
    this.client = createClient(config.url, config.anonKey);
    this.geminiApiKey = config.geminiApiKey;
  }

  /**
   * Get authenticated user
   */
  async getCurrentUser() {
    const {
      data: { user },
      error,
    } = await this.client.auth.getUser();

    if (error) throw error;
    return user;
  }

  /**
   * MAIN WORKFLOW: Create project from intake form
   * This orchestrates the entire Stitch workflow:
   * 1. Create project record
   * 2. Analyze inspiration websites
   * 3. Generate problem deconstruction
   * 4. Generate screen mappings with Stitch prompts
   */
  async createProjectFromIntake(intake: ProjectIntake): Promise<string> {
    const user = await this.getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    // Check quota
    const hasQuota = await this.checkUserQuota(user.id, 'project');
    if (!hasQuota) {
      throw new Error('Project quota exceeded for this month');
    }

    try {
      // STEP 1: Create project record
      const { data: project, error: projectError } = await this.client
        .from('projects')
        .insert({
          user_id: user.id,
          name: intake.appName,
          app_concept: intake.appConcept,
          service_tier: intake.serviceTier,
          status: 'problem_deconstruction',
          metadata: {
            target_audience: intake.targetAudience,
            design_preferences: intake.designPreferences,
          },
        })
        .select()
        .single();

      if (projectError) throw projectError;

      // STEP 2: Analyze inspiration websites
      const gemini = getGeminiService(this.geminiApiKey);
      const inspirationAnalyses = [];

      for (const website of intake.inspirationWebsites) {
        // Capture screenshot (using Edge Function)
        const screenshot = await this.captureWebsiteScreenshot(website.url);

        // Analyze with Gemini
        const analysis = await gemini.analyzeInspirationWebsite(
          screenshot,
          website.url,
          website.locked
        );

        // Save to database
        const { data: savedWebsite, error: websiteError } = await this.client
          .from('inspiration_websites')
          .insert({
            project_id: project.id,
            url: website.url,
            locked: website.locked,
            notes: website.notes,
            screenshot_url: await this.uploadScreenshot(project.id, screenshot),
            analysis,
            color_palette: analysis.color_palette,
            typography: analysis.typography,
            layout_patterns: analysis.layout_patterns,
          })
          .select()
          .single();

        if (websiteError) throw websiteError;

        inspirationAnalyses.push(analysis);

        // Track AI cost
        await this.trackAIGeneration(project.id, 'inspiration_analysis', 'gemini');
      }

      // STEP 3: Generate problem deconstruction
      const problemDeconstruction = await gemini.generateProblemDeconstruction(
        intake,
        inspirationAnalyses
      );

      const { data: savedDeconstruction, error: deconstructionError } =
        await this.client
          .from('problem_deconstructions')
          .insert({
            project_id: project.id,
            ...problemDeconstruction,
          })
          .select()
          .single();

      if (deconstructionError) throw deconstructionError;

      // Track AI cost
      await this.trackAIGeneration(project.id, 'problem_deconstruction', 'gemini');

      // STEP 4: Generate screen mappings
      const screenMappings = await gemini.generateScreenMappings({
        features: problemDeconstruction.features,
        user_stories: problemDeconstruction.user_stories,
        design_system: problemDeconstruction.design_system,
      });

      for (const mapping of screenMappings) {
        await this.client.from('screen_mappings').insert({
          project_id: project.id,
          problem_deconstruction_id: savedDeconstruction.id,
          ...mapping,
        });
      }

      // Track AI cost
      await this.trackAIGeneration(project.id, 'screen_mapping', 'gemini');

      // Update project status
      await this.client
        .from('projects')
        .update({ status: 'stitch_iteration' })
        .eq('id', project.id);

      // Update quota usage
      await this.incrementQuotaUsage(user.id, 'project');

      return project.id;
    } catch (error) {
      console.error('Error creating project:', error);
      throw error;
    }
  }

  /**
   * Get project with full details
   */
  async getProjectWithDetails(projectId: string): Promise<ProjectWithDetails> {
    const { data: project, error: projectError } = await this.client
      .from('projects')
      .select('*')
      .eq('id', projectId)
      .single();

    if (projectError) throw projectError;

    // Get related data
    const [
      { data: inspiration_websites },
      { data: problem_deconstruction },
      { data: screen_mappings },
      { data: stitch_designs },
      { data: code_artifacts },
    ] = await Promise.all([
      this.client
        .from('inspiration_websites')
        .select('*')
        .eq('project_id', projectId),
      this.client
        .from('problem_deconstructions')
        .select('*')
        .eq('project_id', projectId)
        .single(),
      this.client.from('screen_mappings').select('*').eq('project_id', projectId),
      this.client.from('stitch_designs').select('*').eq('project_id', projectId),
      this.client.from('code_artifacts').select('*').eq('project_id', projectId),
    ]);

    return {
      ...project,
      inspiration_websites: inspiration_websites || [],
      problem_deconstruction: problem_deconstruction || undefined,
      screen_mappings: screen_mappings || [],
      stitch_designs: stitch_designs || [],
      code_artifacts: code_artifacts || [],
    };
  }

  /**
   * Upload Stitch HTML export
   */
  async uploadStitchDesign(
    projectId: string,
    screenMappingId: string,
    screenName: string,
    htmlContent: string,
    stateVariation?: string
  ): Promise<string> {
    // Upload HTML to storage
    const fileName = `${projectId}/${screenName}${stateVariation ? `-${stateVariation}` : ''}.html`;
    const { data: uploadData, error: uploadError } = await this.client.storage
      .from('stitch-designs')
      .upload(fileName, htmlContent, {
        contentType: 'text/html',
        upsert: true,
      });

    if (uploadError) throw uploadError;

    // Save to database
    const { data: design, error: designError } = await this.client
      .from('stitch_designs')
      .insert({
        project_id: projectId,
        screen_mapping_id: screenMappingId,
        screen_name: screenName,
        state_variation: stateVariation,
        html_content: htmlContent,
        html_storage_url: uploadData.path,
        approved: false,
      })
      .select()
      .single();

    if (designError) throw designError;

    return design.id;
  }

  /**
   * Approve Stitch design
   */
  async approveStitchDesign(designId: string, feedback?: string): Promise<void> {
    const { error } = await this.client
      .from('stitch_designs')
      .update({ approved: true, feedback })
      .eq('id', designId);

    if (error) throw error;
  }

  /**
   * Generate code from approved Stitch designs
   */
  async generateCodeFromStitchDesigns(projectId: string): Promise<string> {
    // Get all approved designs
    const { data: designs, error: designsError } = await this.client
      .from('stitch_designs')
      .select('*')
      .eq('project_id', projectId)
      .eq('approved', true);

    if (designsError) throw designsError;

    if (!designs || designs.length === 0) {
      throw new Error('No approved designs found');
    }

    // Create code generation job
    const { data: job, error: jobError } = await this.client
      .from('code_generation_jobs')
      .insert({
        project_id: projectId,
        status: 'queued',
        job_type: 'full_project_generation',
        input_data: {
          design_ids: designs.map((d) => d.id),
        },
      })
      .select()
      .single();

    if (jobError) throw jobError;

    // Trigger background job (via Edge Function or webhook)
    await this.triggerCodeGenerationJob(job.id);

    return job.id;
  }

  /**
   * Get user's projects
   */
  async getUserProjects(): Promise<Project[]> {
    const user = await this.getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { data, error } = await this.client
      .from('projects')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });

    if (error) throw error;
    return data || [];
  }

  // ============================================================================
  // HELPER METHODS
  // ============================================================================

  /**
   * Capture website screenshot (via Edge Function)
   */
  private async captureWebsiteScreenshot(url: string): Promise<string> {
    const { data, error } = await this.client.functions.invoke('capture-screenshot', {
      body: { url },
    });

    if (error) throw error;
    return data.screenshot; // Base64 encoded
  }

  /**
   * Upload screenshot to storage
   */
  private async uploadScreenshot(
    projectId: string,
    screenshot: string
  ): Promise<string> {
    const fileName = `${projectId}/inspiration-${Date.now()}.png`;
    const buffer = Buffer.from(screenshot, 'base64');

    const { data, error } = await this.client.storage
      .from('screenshots')
      .upload(fileName, buffer, {
        contentType: 'image/png',
      });

    if (error) throw error;

    // Return public URL
    const { data: publicData } = this.client.storage
      .from('screenshots')
      .getPublicUrl(fileName);

    return publicData.publicUrl;
  }

  /**
   * Track AI generation for cost monitoring
   */
  private async trackAIGeneration(
    projectId: string,
    stage: string,
    modelProvider: string
  ): Promise<void> {
    await this.client.from('ai_generations').insert({
      project_id: projectId,
      stage,
      model_provider: modelProvider,
      model_version: 'gemini-1.5-pro',
      prompt_tokens: 0, // TODO: Get from actual API response
      completion_tokens: 0,
      cost_usd: 0,
    });
  }

  /**
   * Check user quota
   */
  private async checkUserQuota(
    userId: string,
    checkType: 'project' | 'tokens' | 'storage'
  ): Promise<boolean> {
    const { data, error } = await this.client.rpc('check_user_quota', {
      p_user_id: userId,
      p_check_type: checkType,
    });

    if (error) throw error;
    return data;
  }

  /**
   * Increment quota usage
   */
  private async incrementQuotaUsage(userId: string, type: string): Promise<void> {
    const field =
      type === 'project'
        ? 'current_projects'
        : type === 'tokens'
          ? 'current_ai_tokens'
          : 'current_storage_gb';

    const { error } = await this.client
      .from('usage_quotas')
      .update({
        [field]: this.client.raw(`${field} + 1`),
      })
      .eq('user_id', userId);

    if (error) throw error;
  }

  /**
   * Trigger background code generation job
   */
  private async triggerCodeGenerationJob(jobId: string): Promise<void> {
    // Call Edge Function to process the job
    const { error } = await this.client.functions.invoke('process-code-generation', {
      body: { job_id: jobId },
    });

    if (error) {
      console.error('Failed to trigger code generation:', error);
      // Don't throw - job will be picked up by worker
    }
  }

  /**
   * Create a new project (simplified version for Express tier)
   */
  async createProject(projectData: {
    name: string;
    app_concept: string;
    service_tier: string;
    status: string;
    metadata?: any;
  }): Promise<Project> {
    const user = await this.getCurrentUser();
    if (!user) throw new Error('User not authenticated');

    const { data, error } = await this.client
      .from('projects')
      .insert({
        user_id: user.id,
        ...projectData,
      })
      .select()
      .single();

    if (error) throw error;
    if (!data) throw new Error('Failed to create project');

    return data as Project;
  }

  /**
   * Update an existing project
   */
  async updateProject(
    projectId: string,
    updates: Partial<Project>
  ): Promise<Project> {
    const { data, error } = await this.client
      .from('projects')
      .update(updates)
      .eq('id', projectId)
      .select()
      .single();

    if (error) throw error;
    if (!data) throw new Error('Failed to update project');

    return data as Project;
  }

  /**
   * Save a code artifact (screen, component, config file, etc.)
   */
  async saveCodeArtifact(artifact: {
    project_id: string;
    artifact_type: string;
    file_path: string;
    content: string;
    conversion_confidence?: number;
    metadata?: any;
  }): Promise<any> {
    const { data, error } = await this.client
      .from('code_artifacts')
      .insert(artifact)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  /**
   * Package all project artifacts into a downloadable ZIP file
   */
  async packageProjectAsZip(projectId: string): Promise<string> {
    // Get all code artifacts for the project
    const { data: artifacts, error: artifactsError } = await this.client
      .from('code_artifacts')
      .select('*')
      .eq('project_id', projectId);

    if (artifactsError) throw artifactsError;
    if (!artifacts || artifacts.length === 0) {
      throw new Error('No code artifacts found for project');
    }

    // Call Edge Function to create ZIP
    const { data, error } = await this.client.functions.invoke('package-project-zip', {
      body: { project_id: projectId },
    });

    if (error) throw error;
    if (!data || !data.zip_url) {
      throw new Error('Failed to create project ZIP');
    }

    return data.zip_url;
  }
}

/**
 * Singleton instance
 */
let supabaseServiceInstance: SupabaseService | null = null;

export function getSupabaseService(config?: SupabaseConfig): SupabaseService {
  if (!supabaseServiceInstance && !config) {
    throw new Error('Supabase config required to initialize service');
  }

  if (config && !supabaseServiceInstance) {
    supabaseServiceInstance = new SupabaseService(config);
  }

  return supabaseServiceInstance!;
}
