-- State Transitions Table
-- Audit log tracking all orchestrator state machine transitions

CREATE TABLE IF NOT EXISTS state_transitions (
  -- Primary identifier
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Foreign keys
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

  -- State transition details
  from_state TEXT,
  to_state TEXT NOT NULL,
  transition_reason TEXT, -- Human-readable explanation

  -- Trigger information
  trigger_event TEXT NOT NULL,
  -- Examples:
  -- - "Client approved design"
  -- - "Critic score below threshold (7.2/10)"
  -- - "QA tests passed"
  -- - "Error in Figma generation: API timeout"
  -- - "Max iterations reached (3/3)"

  -- Transition data (context-specific)
  transition_data JSONB DEFAULT '{}'::jsonb,
  -- Examples:
  --
  -- Planning → Design Generation:
  -- {
  --   "design_spec_created": true,
  --   "component_count": 12,
  --   "screen_count": 6
  -- }
  --
  -- Design Critique → Refinement:
  -- {
  --   "overall_score": 7.2,
  --   "iteration_count": 1,
  --   "high_priority_issues": 3
  -- }
  --
  -- Client Review → Approved:
  -- {
  --   "client_feedback": "Looks perfect!",
  --   "design_version_id": "uuid",
  --   "approval_timestamp": "2025-10-27T12:00:00Z"
  -- }

  -- Success/failure tracking
  success BOOLEAN DEFAULT TRUE,
  error_message TEXT,
  error_details JSONB,

  -- Performance metrics
  duration_ms INTEGER, -- Time spent in previous state
  agent_used TEXT, -- Which agent performed the work: planning_agent, critic_agent, etc.

  -- Metadata
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_by TEXT DEFAULT 'orchestrator'
);

-- Indexes
CREATE INDEX idx_state_transitions_project_id ON state_transitions(project_id);
CREATE INDEX idx_state_transitions_to_state ON state_transitions(to_state);
CREATE INDEX idx_state_transitions_success ON state_transitions(success);
CREATE INDEX idx_state_transitions_created_at ON state_transitions(created_at DESC);

-- Composite index for project timeline queries
CREATE INDEX idx_state_transitions_project_timeline
  ON state_transitions(project_id, created_at DESC);

-- Comments
COMMENT ON TABLE state_transitions IS 'Audit log of all orchestrator state machine transitions';
COMMENT ON COLUMN state_transitions.from_state IS 'Previous state (NULL for initial INTAKE)';
COMMENT ON COLUMN state_transitions.to_state IS 'New state after transition';
COMMENT ON COLUMN state_transitions.trigger_event IS 'What caused this transition (human-readable)';
COMMENT ON COLUMN state_transitions.transition_data IS 'Context-specific data about the transition';
COMMENT ON COLUMN state_transitions.duration_ms IS 'Milliseconds spent in the previous state';
COMMENT ON COLUMN state_transitions.agent_used IS 'Which agent executed the previous state work';

-- Row Level Security
ALTER TABLE state_transitions ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view transition history for their projects
CREATE POLICY state_transitions_select_own
  ON state_transitions
  FOR SELECT
  USING (
    project_id IN (
      SELECT id FROM projects
      WHERE client_id IN (
        SELECT id FROM clients WHERE user_id = auth.uid()
      )
    )
  );

-- Grants
GRANT SELECT, INSERT ON state_transitions TO authenticated;
GRANT SELECT ON state_transitions TO anon;

-- Helper function: Get project timeline
CREATE OR REPLACE FUNCTION get_project_timeline(p_project_id UUID)
RETURNS SETOF state_transitions AS $$
  SELECT * FROM state_transitions
  WHERE project_id = p_project_id
  ORDER BY created_at ASC;
$$ LANGUAGE SQL STABLE;

-- Helper function: Get error transitions for debugging
CREATE OR REPLACE FUNCTION get_error_transitions(p_project_id UUID)
RETURNS SETOF state_transitions AS $$
  SELECT * FROM state_transitions
  WHERE project_id = p_project_id
    AND success = FALSE
  ORDER BY created_at DESC;
$$ LANGUAGE SQL STABLE;

-- Helper function: Calculate average state duration
CREATE OR REPLACE FUNCTION get_average_state_duration(p_state TEXT)
RETURNS INTERVAL AS $$
  SELECT AVG(duration_ms) * INTERVAL '1 millisecond'
  FROM state_transitions
  WHERE from_state = p_state
    AND success = TRUE
    AND duration_ms IS NOT NULL;
$$ LANGUAGE SQL STABLE;

-- Helper function: Log a state transition
CREATE OR REPLACE FUNCTION log_state_transition(
  p_project_id UUID,
  p_from_state TEXT,
  p_to_state TEXT,
  p_trigger_event TEXT,
  p_transition_data JSONB DEFAULT '{}'::jsonb,
  p_success BOOLEAN DEFAULT TRUE,
  p_error_message TEXT DEFAULT NULL,
  p_duration_ms INTEGER DEFAULT NULL,
  p_agent_used TEXT DEFAULT NULL
)
RETURNS state_transitions AS $$
  INSERT INTO state_transitions (
    project_id,
    from_state,
    to_state,
    trigger_event,
    transition_data,
    success,
    error_message,
    duration_ms,
    agent_used
  ) VALUES (
    p_project_id,
    p_from_state,
    p_to_state,
    p_trigger_event,
    p_transition_data,
    p_success,
    p_error_message,
    p_duration_ms,
    p_agent_used
  )
  RETURNING *;
$$ LANGUAGE SQL VOLATILE;

-- Helper function: Get state transition statistics
CREATE OR REPLACE FUNCTION get_state_statistics(p_project_id UUID)
RETURNS TABLE (
  state TEXT,
  visit_count BIGINT,
  avg_duration_ms NUMERIC,
  success_rate NUMERIC
) AS $$
  SELECT
    from_state AS state,
    COUNT(*) AS visit_count,
    ROUND(AVG(duration_ms)::numeric, 2) AS avg_duration_ms,
    ROUND((COUNT(*) FILTER (WHERE success = TRUE)::numeric / COUNT(*)::numeric * 100), 2) AS success_rate
  FROM state_transitions
  WHERE project_id = p_project_id
    AND from_state IS NOT NULL
  GROUP BY from_state
  ORDER BY visit_count DESC;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION get_project_timeline IS 'Returns chronological timeline of all state transitions for a project';
COMMENT ON FUNCTION get_error_transitions IS 'Returns all failed transitions for debugging';
COMMENT ON FUNCTION get_average_state_duration IS 'Calculates average time spent in a given state across all projects';
COMMENT ON FUNCTION log_state_transition IS 'Records a new state transition in the audit log';
COMMENT ON FUNCTION get_state_statistics IS 'Returns statistics about state visits, duration, and success rate';

-- Trigger: Update project state when transition logged
CREATE OR REPLACE FUNCTION update_project_state()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE projects
  SET
    current_state = NEW.to_state,
    previous_state = NEW.from_state,
    state_updated_at = NEW.created_at
  WHERE id = NEW.project_id;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_project_state_on_transition
  AFTER INSERT ON state_transitions
  FOR EACH ROW
  EXECUTE FUNCTION update_project_state();

COMMENT ON FUNCTION update_project_state IS 'Automatically updates projects.current_state when a transition is logged';
