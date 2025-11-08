-- Workflow State Machine Table
-- Tracks the current state and history of the Design-First Software Factory workflow

CREATE TABLE workflow_states (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  current_phase TEXT NOT NULL CHECK (current_phase IN (
    'problem_deconstruction',
    'screen_mapping',
    'design_generation',
    'stitch_iteration',
    'code_generation',
    'code_review'
  )),
  status TEXT NOT NULL CHECK (status IN (
    'active',
    'completed',
    'failed',
    'paused'
  )),

  -- Phase-specific data (JSON with completion status, timestamps, results)
  phase_data JSONB NOT NULL DEFAULT '{}',

  -- Workflow timestamps
  started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE,

  -- Error tracking
  error_message TEXT,

  -- Audit fields
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for efficient queries
CREATE INDEX idx_workflow_states_project_id ON workflow_states(project_id);
CREATE INDEX idx_workflow_states_status ON workflow_states(status);
CREATE INDEX idx_workflow_states_current_phase ON workflow_states(current_phase);

-- Only one active workflow per project
CREATE UNIQUE INDEX idx_workflow_states_project_active
  ON workflow_states(project_id)
  WHERE status = 'active';

-- Update timestamp trigger
CREATE TRIGGER update_workflow_states_updated_at
  BEFORE UPDATE ON workflow_states
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Helper function to get workflow progress percentage
CREATE OR REPLACE FUNCTION get_workflow_progress(p_project_id UUID)
RETURNS INTEGER AS $$
DECLARE
  phase_order TEXT[] := ARRAY[
    'problem_deconstruction',
    'screen_mapping',
    'design_generation',
    'stitch_iteration',
    'code_generation',
    'code_review'
  ];
  current_state workflow_states;
  current_index INTEGER;
  total_phases INTEGER := 6;
BEGIN
  SELECT * INTO current_state
  FROM workflow_states
  WHERE project_id = p_project_id
  ORDER BY started_at DESC
  LIMIT 1;

  IF NOT FOUND THEN
    RETURN 0;
  END IF;

  -- If completed, return 100
  IF current_state.status = 'completed' THEN
    RETURN 100;
  END IF;

  -- Find current phase index
  FOR i IN 1..array_length(phase_order, 1) LOOP
    IF phase_order[i] = current_state.current_phase THEN
      current_index := i;
      EXIT;
    END IF;
  END LOOP;

  -- Calculate percentage (phases start at 0%, complete at 100%)
  RETURN ((current_index - 1) * 100) / total_phases;
END;
$$ LANGUAGE plpgsql;

-- Helper function to get current workflow status
CREATE OR REPLACE FUNCTION get_workflow_summary(p_project_id UUID)
RETURNS TABLE (
  workflow_id UUID,
  current_phase TEXT,
  status TEXT,
  progress_pct INTEGER,
  phases_completed INTEGER,
  total_phases INTEGER,
  started_at TIMESTAMP WITH TIME ZONE,
  estimated_completion TIMESTAMP WITH TIME ZONE
) AS $$
DECLARE
  current_state workflow_states;
  completed_count INTEGER := 0;
  phase_key TEXT;
BEGIN
  SELECT * INTO current_state
  FROM workflow_states ws
  WHERE ws.project_id = p_project_id
  ORDER BY ws.started_at DESC
  LIMIT 1;

  IF NOT FOUND THEN
    RETURN;
  END IF;

  -- Count completed phases
  FOR phase_key IN SELECT jsonb_object_keys(current_state.phase_data) LOOP
    IF (current_state.phase_data->phase_key->>'status') = 'completed' THEN
      completed_count := completed_count + 1;
    END IF;
  END LOOP;

  RETURN QUERY SELECT
    current_state.id,
    current_state.current_phase,
    current_state.status,
    get_workflow_progress(p_project_id),
    completed_count,
    6 as total_phases,
    current_state.started_at,
    -- Rough estimate: 10 minutes per remaining phase
    current_state.started_at + ((6 - completed_count) * interval '10 minutes') as estimated_completion;
END;
$$ LANGUAGE plpgsql;

-- Comment on the table
COMMENT ON TABLE workflow_states IS 'Tracks workflow state for Design-First Software Factory projects through 6 phases: problem_deconstruction → screen_mapping → design_generation → stitch_iteration → code_generation → code_review';
