-- Design-First Software Factory - Initial Schema
-- This migration creates the core database structure for the Stitch-integrated workflow

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- Projects: Main project tracking
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  app_concept TEXT NOT NULL,
  service_tier TEXT NOT NULL CHECK (service_tier IN ('express', 'concierge', 'premium')),

  -- Workflow status
  status TEXT NOT NULL DEFAULT 'intake' CHECK (status IN (
    'intake',
    'problem_deconstruction',
    'screen_mapping',
    'design_generation',
    'design_review',
    'stitch_iteration',
    'html_upload',
    'code_generation',
    'code_review',
    'complete',
    'failed'
  )),

  -- Metadata
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on user_id for fast user queries
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);

-- ============================================================================
-- INSPIRATION WEBSITES
-- ============================================================================

-- Inspiration websites for design guidance (max 3 per project)
CREATE TABLE inspiration_websites (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Website details
  url TEXT NOT NULL,
  locked BOOLEAN DEFAULT FALSE, -- True = must follow as brand guideline
  notes TEXT,

  -- AI analysis results
  screenshot_url TEXT, -- Stored in Supabase Storage
  analysis JSONB, -- Gemini's design analysis

  -- Extracted design tokens
  color_palette TEXT[],
  typography JSONB,
  layout_patterns TEXT[],

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_inspiration_websites_project_id ON inspiration_websites(project_id);

-- Constraint: Max 3 inspiration websites per project
CREATE OR REPLACE FUNCTION check_max_inspiration_websites()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT COUNT(*) FROM inspiration_websites WHERE project_id = NEW.project_id) >= 3 THEN
    RAISE EXCEPTION 'Maximum 3 inspiration websites per project';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_max_inspiration_websites
  BEFORE INSERT ON inspiration_websites
  FOR EACH ROW
  EXECUTE FUNCTION check_max_inspiration_websites();

-- ============================================================================
-- DESIGN GENERATION
-- ============================================================================

-- Problem deconstruction results from Gemini
CREATE TABLE problem_deconstructions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Generated artifacts
  user_stories JSONB NOT NULL, -- Array of user story objects
  features JSONB NOT NULL, -- Array of feature objects
  ux_requirements JSONB NOT NULL,
  design_system JSONB NOT NULL, -- High-level design system

  -- AI generation metadata
  model_version TEXT NOT NULL,
  prompt_tokens INTEGER,
  completion_tokens INTEGER,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_problem_deconstructions_project_id ON problem_deconstructions(project_id);

-- Screen mapping: Features → Screens
CREATE TABLE screen_mappings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  problem_deconstruction_id UUID REFERENCES problem_deconstructions(id) ON DELETE CASCADE,

  -- Screen definition
  screen_name TEXT NOT NULL,
  screen_type TEXT CHECK (screen_type IN ('authentication', 'onboarding', 'main', 'detail', 'form', 'settings')),
  features TEXT[], -- Which features are on this screen

  -- Stitch prompt for this screen
  stitch_prompt TEXT NOT NULL,

  -- Design metadata
  navigation_context JSONB,
  state_variations TEXT[], -- e.g., ['empty', 'loading', 'error', 'success']

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_screen_mappings_project_id ON screen_mappings(project_id);

-- Stitch designs: HTML exports from Stitch
CREATE TABLE stitch_designs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  screen_mapping_id UUID REFERENCES screen_mappings(id) ON DELETE CASCADE,

  -- Stitch export details
  screen_name TEXT NOT NULL,
  state_variation TEXT, -- e.g., 'empty', 'loading', 'error'
  html_content TEXT NOT NULL,
  html_storage_url TEXT, -- Supabase Storage URL for the HTML file

  -- User approval
  approved BOOLEAN DEFAULT FALSE,
  feedback TEXT,

  -- Iteration tracking
  iteration_number INTEGER DEFAULT 1,
  parent_design_id UUID REFERENCES stitch_designs(id), -- Previous iteration

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_stitch_designs_project_id ON stitch_designs(project_id);
CREATE INDEX idx_stitch_designs_screen_mapping_id ON stitch_designs(screen_mapping_id);
CREATE INDEX idx_stitch_designs_approved ON stitch_designs(approved);

-- ============================================================================
-- CODE GENERATION
-- ============================================================================

-- Code generation jobs (background processing)
CREATE TABLE code_generation_jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Job details
  status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
  job_type TEXT NOT NULL CHECK (job_type IN ('html_to_react_native', 'full_project_generation')),

  -- Input/output
  input_data JSONB NOT NULL,
  output_data JSONB,

  -- Error handling
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3,

  -- Timing
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_code_generation_jobs_project_id ON code_generation_jobs(project_id);
CREATE INDEX idx_code_generation_jobs_status ON code_generation_jobs(status);

-- Generated code artifacts
CREATE TABLE code_artifacts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  code_generation_job_id UUID REFERENCES code_generation_jobs(id) ON DELETE CASCADE,

  -- Artifact details
  artifact_type TEXT NOT NULL CHECK (artifact_type IN ('component', 'screen', 'navigation', 'full_project')),
  file_path TEXT NOT NULL, -- Relative path in the generated project
  content TEXT NOT NULL,
  storage_url TEXT, -- Supabase Storage URL for the file

  -- Conversion quality metrics
  conversion_confidence NUMERIC(3, 2), -- 0.00 to 1.00
  warnings TEXT[],

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_code_artifacts_project_id ON code_artifacts(project_id);
CREATE INDEX idx_code_artifacts_job_id ON code_artifacts(code_generation_job_id);

-- ============================================================================
-- AUDIT & COST TRACKING
-- ============================================================================

-- Audit logs for compliance
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Action details
  action TEXT NOT NULL,
  resource_type TEXT NOT NULL,
  resource_id UUID,

  -- Context
  ip_address INET,
  user_agent TEXT,
  metadata JSONB DEFAULT '{}',

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_project_id ON audit_logs(project_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- AI generation cost tracking
CREATE TABLE ai_generations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Generation stage
  stage TEXT NOT NULL CHECK (stage IN (
    'problem_deconstruction',
    'screen_mapping',
    'stitch_prompt_generation',
    'inspiration_analysis',
    'code_generation'
  )),

  -- Model details
  model_provider TEXT NOT NULL CHECK (model_provider IN ('gemini', 'anthropic', 'openai')),
  model_version TEXT NOT NULL,

  -- Token usage
  prompt_tokens INTEGER NOT NULL,
  completion_tokens INTEGER NOT NULL,
  total_tokens INTEGER GENERATED ALWAYS AS (prompt_tokens + completion_tokens) STORED,

  -- Cost tracking
  cost_usd NUMERIC(10, 6),

  -- Timing
  latency_ms INTEGER,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ai_generations_project_id ON ai_generations(project_id);
CREATE INDEX idx_ai_generations_stage ON ai_generations(stage);
CREATE INDEX idx_ai_generations_created_at ON ai_generations(created_at);

-- Usage quotas per user
CREATE TABLE usage_quotas (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Quota limits
  tier TEXT NOT NULL CHECK (tier IN ('free', 'pro', 'enterprise')),
  projects_per_month INTEGER NOT NULL,
  ai_tokens_per_month BIGINT NOT NULL,
  storage_gb NUMERIC(10, 2) NOT NULL,

  -- Current usage (reset monthly)
  current_projects INTEGER DEFAULT 0,
  current_ai_tokens BIGINT DEFAULT 0,
  current_storage_gb NUMERIC(10, 2) DEFAULT 0,

  -- Reset tracking
  period_start TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  period_end TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (NOW() + INTERVAL '1 month'),

  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_usage_quotas_user_id ON usage_quotas(user_id);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE inspiration_websites ENABLE ROW LEVEL SECURITY;
ALTER TABLE problem_deconstructions ENABLE ROW LEVEL SECURITY;
ALTER TABLE screen_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE stitch_designs ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_generation_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_generations ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_quotas ENABLE ROW LEVEL SECURITY;

-- Projects: Users can only access their own projects
CREATE POLICY "Users can view their own projects"
  ON projects FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own projects"
  ON projects FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own projects"
  ON projects FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own projects"
  ON projects FOR DELETE
  USING (auth.uid() = user_id);

-- Inspiration websites: Access through project ownership
CREATE POLICY "Users can access inspiration websites for their projects"
  ON inspiration_websites FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = inspiration_websites.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Problem deconstructions: Access through project ownership
CREATE POLICY "Users can access problem deconstructions for their projects"
  ON problem_deconstructions FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = problem_deconstructions.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Screen mappings: Access through project ownership
CREATE POLICY "Users can access screen mappings for their projects"
  ON screen_mappings FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = screen_mappings.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Stitch designs: Access through project ownership
CREATE POLICY "Users can access stitch designs for their projects"
  ON stitch_designs FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = stitch_designs.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Code generation jobs: Access through project ownership
CREATE POLICY "Users can access code generation jobs for their projects"
  ON code_generation_jobs FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = code_generation_jobs.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Code artifacts: Access through project ownership
CREATE POLICY "Users can access code artifacts for their projects"
  ON code_artifacts FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = code_artifacts.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Audit logs: Users can only view their own audit logs
CREATE POLICY "Users can view their own audit logs"
  ON audit_logs FOR SELECT
  USING (auth.uid() = user_id);

-- AI generations: Access through project ownership
CREATE POLICY "Users can view ai generations for their projects"
  ON ai_generations FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = ai_generations.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Usage quotas: Users can only view their own quotas
CREATE POLICY "Users can view their own usage quotas"
  ON usage_quotas FOR SELECT
  USING (auth.uid() = user_id);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_projects_updated_at
  BEFORE UPDATE ON projects
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_usage_quotas_updated_at
  BEFORE UPDATE ON usage_quotas
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Audit log trigger for projects
CREATE OR REPLACE FUNCTION audit_project_changes()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    INSERT INTO audit_logs (user_id, project_id, action, resource_type, resource_id, metadata)
    VALUES (auth.uid(), NEW.id, 'project_created', 'project', NEW.id, to_jsonb(NEW));
  ELSIF TG_OP = 'UPDATE' THEN
    INSERT INTO audit_logs (user_id, project_id, action, resource_type, resource_id, metadata)
    VALUES (auth.uid(), NEW.id, 'project_updated', 'project', NEW.id,
      jsonb_build_object('old', to_jsonb(OLD), 'new', to_jsonb(NEW)));
  ELSIF TG_OP = 'DELETE' THEN
    INSERT INTO audit_logs (user_id, project_id, action, resource_type, resource_id, metadata)
    VALUES (auth.uid(), OLD.id, 'project_deleted', 'project', OLD.id, to_jsonb(OLD));
  END IF;
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_projects
  AFTER INSERT OR UPDATE OR DELETE ON projects
  FOR EACH ROW
  EXECUTE FUNCTION audit_project_changes();

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Get project status summary
CREATE OR REPLACE FUNCTION get_project_status_summary(p_project_id UUID)
RETURNS JSONB AS $$
DECLARE
  result JSONB;
BEGIN
  SELECT jsonb_build_object(
    'project', (SELECT to_jsonb(p) FROM projects p WHERE id = p_project_id),
    'inspiration_count', (SELECT COUNT(*) FROM inspiration_websites WHERE project_id = p_project_id),
    'screens_mapped', (SELECT COUNT(*) FROM screen_mappings WHERE project_id = p_project_id),
    'designs_created', (SELECT COUNT(*) FROM stitch_designs WHERE project_id = p_project_id),
    'designs_approved', (SELECT COUNT(*) FROM stitch_designs WHERE project_id = p_project_id AND approved = TRUE),
    'total_cost_usd', (SELECT COALESCE(SUM(cost_usd), 0) FROM ai_generations WHERE project_id = p_project_id),
    'total_tokens', (SELECT COALESCE(SUM(total_tokens), 0) FROM ai_generations WHERE project_id = p_project_id)
  ) INTO result;

  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Check if user is within quota
CREATE OR REPLACE FUNCTION check_user_quota(p_user_id UUID, p_check_type TEXT)
RETURNS BOOLEAN AS $$
DECLARE
  quota_record usage_quotas;
BEGIN
  SELECT * INTO quota_record FROM usage_quotas WHERE user_id = p_user_id;

  IF NOT FOUND THEN
    RETURN FALSE;
  END IF;

  CASE p_check_type
    WHEN 'project' THEN
      RETURN quota_record.current_projects < quota_record.projects_per_month;
    WHEN 'tokens' THEN
      RETURN quota_record.current_ai_tokens < quota_record.ai_tokens_per_month;
    WHEN 'storage' THEN
      RETURN quota_record.current_storage_gb < quota_record.storage_gb;
    ELSE
      RETURN FALSE;
  END CASE;
END;
$$ LANGUAGE plpgsql;

-- Initialize usage quota for new users
CREATE OR REPLACE FUNCTION initialize_user_quota()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO usage_quotas (user_id, tier, projects_per_month, ai_tokens_per_month, storage_gb)
  VALUES (NEW.id, 'free', 3, 100000, 1.0);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to initialize quota when user signs up
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION initialize_user_quota();
