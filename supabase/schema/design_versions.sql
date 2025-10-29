-- Design Versions Table
-- Stores each iteration of design with Figma URLs and quality scores

CREATE TABLE IF NOT EXISTS design_versions (
  -- Primary identifier
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Foreign keys
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

  -- Version tracking
  version_number INTEGER NOT NULL,
  version_label TEXT, -- e.g., "Initial Draft", "Client Revision 1", "Final"

  -- Figma integration
  figma_file_url TEXT,
  figma_file_id TEXT,
  figma_pages JSONB DEFAULT '[]'::jsonb,
  -- Example: [{"page_name": "Mobile", "page_id": "123:456", "frames": ["Home", "Dashboard"]}]

  -- Design specification (from planning agent)
  design_spec JSONB NOT NULL DEFAULT '{}'::jsonb,
  -- Complete design specification JSON with:
  -- - project_metadata
  -- - design_system (colors, typography, spacing)
  -- - component_library
  -- - screens
  -- - navigation_structure

  -- Quality evaluation (from critic agent)
  critic_scores JSONB DEFAULT '{}'::jsonb,
  -- Example structure:
  -- {
  --   "overall_score": 7.5,
  --   "rubric_scores": {
  --     "visual_hierarchy": 8,
  --     "consistency": 7,
  --     "accessibility": 6,
  --     "responsive_design": 9,
  --     "user_experience": 8,
  --     "brand_alignment": 7,
  --     "technical_feasibility": 9,
  --     "polish": 6
  --   },
  --   "strengths": ["..."],
  --   "improvement_suggestions": [...]
  -- }

  -- Iteration tracking
  iteration_count INTEGER DEFAULT 0,
  parent_version_id UUID REFERENCES design_versions(id),
  -- Links to the version this was refined from

  -- Status
  status TEXT DEFAULT 'draft',
  -- Possible values: draft, under_review, approved, rejected, superseded

  -- Approval tracking
  approved_by UUID REFERENCES clients(id),
  approved_at TIMESTAMP WITH TIME ZONE,
  rejection_reason TEXT,

  -- Metadata
  created_by TEXT DEFAULT 'system', -- 'system', 'planning_agent', 'refinement_agent'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Constraints
  CONSTRAINT valid_status CHECK (status IN (
    'draft',
    'under_review',
    'approved',
    'rejected',
    'superseded'
  )),
  CONSTRAINT unique_project_version UNIQUE (project_id, version_number)
);

-- Indexes
CREATE INDEX idx_design_versions_project_id ON design_versions(project_id);
CREATE INDEX idx_design_versions_status ON design_versions(status);
CREATE INDEX idx_design_versions_version_number ON design_versions(project_id, version_number DESC);
CREATE INDEX idx_design_versions_created_at ON design_versions(created_at DESC);

-- Index on JSONB fields for efficient queries
CREATE INDEX idx_design_versions_critic_overall_score ON design_versions((critic_scores->>'overall_score'));

-- Updated_at trigger
CREATE TRIGGER update_design_versions_updated_at
  BEFORE UPDATE ON design_versions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Comments
COMMENT ON TABLE design_versions IS 'Design iterations with Figma files and quality scores';
COMMENT ON COLUMN design_versions.version_number IS 'Incremental version number per project (1, 2, 3...)';
COMMENT ON COLUMN design_versions.design_spec IS 'Complete design specification JSON from planning/refinement agent';
COMMENT ON COLUMN design_versions.critic_scores IS 'Quality evaluation scores from critic agent';
COMMENT ON COLUMN design_versions.iteration_count IS 'Number of refinement cycles this version went through';
COMMENT ON COLUMN design_versions.parent_version_id IS 'Links to previous version if this is a refinement';

-- Row Level Security
ALTER TABLE design_versions ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view design versions for their projects
CREATE POLICY design_versions_select_own
  ON design_versions
  FOR SELECT
  USING (
    project_id IN (
      SELECT id FROM projects
      WHERE client_id IN (
        SELECT id FROM clients WHERE user_id = auth.uid()
      )
    )
  );

-- Policy: Users can update design versions (for approval/rejection)
CREATE POLICY design_versions_update_own
  ON design_versions
  FOR UPDATE
  USING (
    project_id IN (
      SELECT id FROM projects
      WHERE client_id IN (
        SELECT id FROM clients WHERE user_id = auth.uid()
      )
    )
  );

-- Grants
GRANT SELECT, INSERT, UPDATE ON design_versions TO authenticated;
GRANT SELECT ON design_versions TO anon;

-- Helper function: Get latest version for a project
CREATE OR REPLACE FUNCTION get_latest_design_version(p_project_id UUID)
RETURNS design_versions AS $$
  SELECT * FROM design_versions
  WHERE project_id = p_project_id
  ORDER BY version_number DESC
  LIMIT 1;
$$ LANGUAGE SQL STABLE;

-- Helper function: Get approved version for a project
CREATE OR REPLACE FUNCTION get_approved_design_version(p_project_id UUID)
RETURNS design_versions AS $$
  SELECT * FROM design_versions
  WHERE project_id = p_project_id
    AND status = 'approved'
  ORDER BY version_number DESC
  LIMIT 1;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION get_latest_design_version IS 'Returns the most recent design version for a project';
COMMENT ON FUNCTION get_approved_design_version IS 'Returns the latest approved design version for a project';
