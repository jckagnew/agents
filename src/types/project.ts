/**
 * Type definitions for Design-First Software Factory
 * Stitch Workflow Integration
 */

export type ServiceTier = 'express' | 'concierge' | 'premium';

export type ProjectStatus =
  | 'intake'
  | 'problem_deconstruction'
  | 'screen_mapping'
  | 'design_generation'
  | 'design_review'
  | 'stitch_iteration'
  | 'html_upload'
  | 'code_generation'
  | 'code_review'
  | 'complete'
  | 'failed';

/**
 * Inspiration website for design guidance
 * Max 3 per project, 1 can be locked as brand guideline
 */
export interface InspirationWebsite {
  id?: string;
  url: string;
  locked: boolean; // True = must follow as brand guideline
  notes: string;
  screenshot_url?: string;
  analysis?: DesignAnalysis;
}

/**
 * Gemini's analysis of an inspiration website
 */
export interface DesignAnalysis {
  color_palette: string[];
  typography: {
    headings: string[];
    body: string[];
    sizes: {
      h1?: string;
      h2?: string;
      h3?: string;
      body?: string;
      small?: string;
    };
  };
  layout_patterns: string[];
  spacing_system: {
    base_unit?: number;
    scale?: number[];
  };
  component_styles: {
    buttons?: string[];
    cards?: string[];
    inputs?: string[];
  };
  overall_aesthetic: string;
  brand_guidelines?: {
    logo_usage?: string;
    color_dos_donts?: string[];
    typography_rules?: string[];
  };
}

/**
 * Enhanced project intake form data
 */
export interface ProjectIntake {
  appName: string;
  appConcept: string;
  serviceTier: ServiceTier;

  // Inspiration sources (max 3)
  inspirationWebsites: InspirationWebsite[];

  // Optional: Additional context
  targetAudience?: string;
  keyFeatures?: string[];
  designPreferences?: string;
}

/**
 * Problem deconstruction output from Gemini
 */
export interface ProblemDeconstruction {
  id: string;
  project_id: string;

  user_stories: UserStory[];
  features: Feature[];
  ux_requirements: UXRequirement[];
  design_system: DesignSystem;

  model_version: string;
  prompt_tokens: number;
  completion_tokens: number;
  created_at: string;
}

export interface UserStory {
  id: string;
  role: string;
  goal: string;
  benefit: string;
  acceptance_criteria: string[];
  priority: 'high' | 'medium' | 'low';
}

export interface Feature {
  id: string;
  name: string;
  description: string;
  user_stories: string[]; // User story IDs
  complexity: 'simple' | 'moderate' | 'complex';
  required_for_mvp: boolean;
}

export interface UXRequirement {
  category: 'navigation' | 'interaction' | 'feedback' | 'accessibility' | 'performance';
  requirement: string;
  rationale: string;
}

export interface DesignSystem {
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    surface: string;
    error: string;
    success: string;
    warning: string;
    text: {
      primary: string;
      secondary: string;
      disabled: string;
    };
  };
  typography: {
    fontFamily: {
      heading: string;
      body: string;
      mono: string;
    };
    scale: {
      h1: number;
      h2: number;
      h3: number;
      h4: number;
      body: number;
      small: number;
    };
    weights: {
      light: number;
      regular: number;
      medium: number;
      bold: number;
    };
  };
  spacing: {
    baseUnit: number;
    scale: number[];
  };
  borderRadius: {
    small: number;
    medium: number;
    large: number;
    full: number;
  };
  shadows: {
    small: string;
    medium: string;
    large: string;
  };
}

/**
 * Screen mapping: Features → Screens
 */
export interface ScreenMapping {
  id: string;
  project_id: string;
  problem_deconstruction_id: string;

  screen_name: string;
  screen_type: 'authentication' | 'onboarding' | 'main' | 'detail' | 'form' | 'settings';
  features: string[]; // Feature IDs

  stitch_prompt: string; // Prompt ready for Stitch

  navigation_context: {
    parent_screen?: string;
    child_screens?: string[];
    tab_bar_item?: boolean;
  };
  state_variations: string[]; // e.g., ['empty', 'loading', 'error', 'success']

  created_at: string;
}

/**
 * Stitch design: HTML export from Stitch
 */
export interface StitchDesign {
  id: string;
  project_id: string;
  screen_mapping_id: string;

  screen_name: string;
  state_variation?: string;
  html_content: string;
  html_storage_url?: string;

  approved: boolean;
  feedback?: string;

  iteration_number: number;
  parent_design_id?: string;

  created_at: string;
}

/**
 * Code generation job
 */
export interface CodeGenerationJob {
  id: string;
  project_id: string;

  status: 'queued' | 'processing' | 'completed' | 'failed';
  job_type: 'html_to_react_native' | 'full_project_generation';

  input_data: any;
  output_data?: any;

  error_message?: string;
  retry_count: number;
  max_retries: number;

  started_at?: string;
  completed_at?: string;
  created_at: string;
}

/**
 * Code artifact
 */
export interface CodeArtifact {
  id: string;
  project_id: string;
  code_generation_job_id: string;

  artifact_type: 'component' | 'screen' | 'navigation' | 'full_project';
  file_path: string;
  content: string;
  storage_url?: string;

  conversion_confidence?: number;
  warnings?: string[];

  created_at: string;
}

/**
 * Project with full details
 */
export interface Project {
  id: string;
  user_id: string;
  name: string;
  description?: string;
  app_concept: string;
  service_tier: ServiceTier;
  status: ProjectStatus;

  metadata: Record<string, any>;

  created_at: string;
  updated_at: string;
}

/**
 * Full project with relations
 */
export interface ProjectWithDetails extends Project {
  inspiration_websites: InspirationWebsite[];
  problem_deconstruction?: ProblemDeconstruction;
  screen_mappings?: ScreenMapping[];
  stitch_designs?: StitchDesign[];
  code_artifacts?: CodeArtifact[];
}
