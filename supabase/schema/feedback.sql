-- Feedback Table
-- Stores all feedback: client approvals, critic suggestions, QA errors

CREATE TABLE IF NOT EXISTS feedback (
  -- Primary identifier
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Foreign keys
  design_version_id UUID NOT NULL REFERENCES design_versions(id) ON DELETE CASCADE,
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

  -- Feedback source
  feedback_type TEXT NOT NULL,
  -- Possible values: client_approval, client_changes, critic_suggestion, qa_error, system_note

  -- Feedback content
  feedback_data JSONB NOT NULL DEFAULT '{}'::jsonb,
  -- Structure varies by type:
  --
  -- client_approval:
  -- {
  --   "approval_status": "approved",
  --   "comments": "Looks great!",
  --   "timestamp": "2025-10-27T12:00:00Z"
  -- }
  --
  -- client_changes:
  -- {
  --   "classification": "MINOR_CHANGES",
  --   "change_requests": [
  --     {"category": "color", "description": "...", "priority": "high"}
  --   ],
  --   "sentiment": {"tone": "positive", "satisfaction_level": 8}
  -- }
  --
  -- critic_suggestion:
  -- {
  --   "category": "accessibility",
  --   "issue": "...",
  --   "suggestion": "...",
  --   "priority": "high"
  -- }
  --
  -- qa_error:
  -- {
  --   "error_type": "lint_error",
  --   "message": "...",
  --   "file": "...",
  --   "line": 42
  -- }

  -- Processing status
  processed BOOLEAN DEFAULT FALSE,
  processed_at TIMESTAMP WITH TIME ZONE,
  processed_by TEXT, -- 'refinement_agent', 'planning_agent', 'human'

  -- Processing result
  processing_result JSONB DEFAULT '{}'::jsonb,
  -- Example:
  -- {
  --   "action_taken": "Applied color change to primary buttons",
  --   "changes_made": ["Updated design_spec.colors.primary"],
  --   "next_state": "DESIGN_GENERATION"
  -- }

  -- Priority and categorization
  priority TEXT DEFAULT 'medium',
  category TEXT, -- For filtering: "color", "layout", "accessibility", etc.

  -- Metadata
  created_by UUID REFERENCES clients(id), -- NULL for system-generated feedback
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Constraints
  CONSTRAINT valid_feedback_type CHECK (feedback_type IN (
    'client_approval',
    'client_changes',
    'critic_suggestion',
    'qa_error',
    'system_note'
  )),
  CONSTRAINT valid_priority CHECK (priority IN ('low', 'medium', 'high', 'critical'))
);

-- Indexes
CREATE INDEX idx_feedback_design_version_id ON feedback(design_version_id);
CREATE INDEX idx_feedback_project_id ON feedback(project_id);
CREATE INDEX idx_feedback_type ON feedback(feedback_type);
CREATE INDEX idx_feedback_processed ON feedback(processed);
CREATE INDEX idx_feedback_priority ON feedback(priority);
CREATE INDEX idx_feedback_created_at ON feedback(created_at DESC);

-- Composite index for common query pattern
CREATE INDEX idx_feedback_version_unprocessed ON feedback(design_version_id, processed)
  WHERE processed = FALSE;

-- Comments
COMMENT ON TABLE feedback IS 'All feedback types: client, critic, QA, system notes';
COMMENT ON COLUMN feedback.feedback_type IS 'Source/type of feedback (client, critic, QA, system)';
COMMENT ON COLUMN feedback.feedback_data IS 'JSONB containing structured feedback content (varies by type)';
COMMENT ON COLUMN feedback.processed IS 'Whether this feedback has been addressed by an agent';
COMMENT ON COLUMN feedback.processing_result IS 'What action was taken in response to this feedback';

-- Row Level Security
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view feedback for their projects
CREATE POLICY feedback_select_own
  ON feedback
  FOR SELECT
  USING (
    project_id IN (
      SELECT id FROM projects
      WHERE client_id IN (
        SELECT id FROM clients WHERE user_id = auth.uid()
      )
    )
  );

-- Policy: Users can insert feedback for their projects (client feedback)
CREATE POLICY feedback_insert_own
  ON feedback
  FOR INSERT
  WITH CHECK (
    created_by IN (
      SELECT id FROM clients WHERE user_id = auth.uid()
    )
  );

-- Grants
GRANT SELECT, INSERT, UPDATE ON feedback TO authenticated;
GRANT SELECT ON feedback TO anon;

-- Helper function: Get unprocessed feedback for a design version
CREATE OR REPLACE FUNCTION get_unprocessed_feedback(p_design_version_id UUID)
RETURNS SETOF feedback AS $$
  SELECT * FROM feedback
  WHERE design_version_id = p_design_version_id
    AND processed = FALSE
  ORDER BY
    CASE priority
      WHEN 'critical' THEN 1
      WHEN 'high' THEN 2
      WHEN 'medium' THEN 3
      WHEN 'low' THEN 4
    END,
    created_at ASC;
$$ LANGUAGE SQL STABLE;

-- Helper function: Mark feedback as processed
CREATE OR REPLACE FUNCTION mark_feedback_processed(
  p_feedback_id UUID,
  p_processed_by TEXT,
  p_processing_result JSONB
)
RETURNS feedback AS $$
  UPDATE feedback
  SET
    processed = TRUE,
    processed_at = NOW(),
    processed_by = p_processed_by,
    processing_result = p_processing_result
  WHERE id = p_feedback_id
  RETURNING *;
$$ LANGUAGE SQL VOLATILE;

-- Helper function: Get all high-priority unprocessed feedback for project
CREATE OR REPLACE FUNCTION get_high_priority_feedback(p_project_id UUID)
RETURNS SETOF feedback AS $$
  SELECT * FROM feedback
  WHERE project_id = p_project_id
    AND processed = FALSE
    AND priority IN ('high', 'critical')
  ORDER BY
    CASE priority
      WHEN 'critical' THEN 1
      WHEN 'high' THEN 2
    END,
    created_at ASC;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION get_unprocessed_feedback IS 'Returns unprocessed feedback for a design version, ordered by priority';
COMMENT ON FUNCTION mark_feedback_processed IS 'Marks feedback as processed with result details';
COMMENT ON FUNCTION get_high_priority_feedback IS 'Returns all high/critical unprocessed feedback for a project';
