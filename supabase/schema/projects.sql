-- Projects Table
-- Stores client project information and current orchestrator state

CREATE TABLE IF NOT EXISTS projects (
  -- Primary identifier
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Foreign keys
  client_id UUID REFERENCES clients(id) ON DELETE CASCADE,

  -- Project metadata
  project_name TEXT NOT NULL,
  project_description TEXT,
  target_audience TEXT,

  -- State machine tracking
  current_state TEXT NOT NULL DEFAULT 'INTAKE',
  previous_state TEXT,
  state_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Intake data (stored as JSONB for flexibility)
  intake_data JSONB DEFAULT '{}'::jsonb,
  -- Example structure:
  -- {
  --   "brand_colors": ["#3B82F6", "#10B981", "#F59E0B"],
  --   "design_style": "modern",
  --   "key_features": ["dashboard", "analytics", "user-management"],
  --   "screens_required": ["home", "dashboard", "settings"]
  -- }

  -- Status tracking
  status TEXT DEFAULT 'active',
  -- Possible values: active, paused, completed, cancelled, error

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,

  -- Constraints
  CONSTRAINT valid_state CHECK (current_state IN (
    'INTAKE',
    'PLANNING',
    'DESIGN_GENERATION',
    'DESIGN_CRITIQUE',
    'DESIGN_REFINEMENT',
    'CLIENT_REVIEW',
    'FEEDBACK_PROCESSING',
    'APPROVED',
    'IMPLEMENTATION',
    'QA',
    'DEPLOYMENT',
    'COMPLETE',
    'ERROR'
  )),
  CONSTRAINT valid_status CHECK (status IN (
    'active',
    'paused',
    'completed',
    'cancelled',
    'error'
  ))
);

-- Indexes for performance
CREATE INDEX idx_projects_client_id ON projects(client_id);
CREATE INDEX idx_projects_current_state ON projects(current_state);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);

-- Updated_at trigger
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

-- Comments for documentation
COMMENT ON TABLE projects IS 'Client projects with orchestrator state machine tracking';
COMMENT ON COLUMN projects.current_state IS 'Current state in the design automation workflow';
COMMENT ON COLUMN projects.intake_data IS 'JSONB containing client requirements and preferences from intake form';
COMMENT ON COLUMN projects.status IS 'Overall project status independent of state machine position';

-- Row Level Security (RLS)
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only view their own projects
CREATE POLICY projects_select_own
  ON projects
  FOR SELECT
  USING (auth.uid() IN (
    SELECT user_id FROM clients WHERE id = client_id
  ));

-- Policy: Users can update their own projects (for feedback)
CREATE POLICY projects_update_own
  ON projects
  FOR UPDATE
  USING (auth.uid() IN (
    SELECT user_id FROM clients WHERE id = client_id
  ));

-- Grant permissions
GRANT SELECT, INSERT, UPDATE ON projects TO authenticated;
GRANT SELECT ON projects TO anon;
