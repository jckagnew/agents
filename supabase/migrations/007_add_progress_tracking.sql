-- Progress Tracking Tables
-- Stores real-time progress checkpoints and events for workflow monitoring

-- Progress Checkpoints: Discrete steps within each phase
CREATE TABLE progress_checkpoints (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Phase and step information
  phase TEXT NOT NULL CHECK (phase IN (
    'problem_deconstruction',
    'screen_mapping',
    'design_generation',
    'stitch_iteration',
    'code_generation',
    'code_review'
  )),
  step_name TEXT NOT NULL,
  step_index INTEGER NOT NULL,
  total_steps INTEGER NOT NULL,
  progress_pct INTEGER NOT NULL CHECK (progress_pct >= 0 AND progress_pct <= 100),

  -- Optional message and metadata
  message TEXT,
  metadata JSONB DEFAULT '{}',

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Progress Events: All progress-related events (broader than checkpoints)
CREATE TABLE progress_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Event details
  event_type TEXT NOT NULL CHECK (event_type IN (
    'phase_start',
    'phase_progress',
    'phase_complete',
    'phase_error',
    'workflow_complete'
  )),
  phase TEXT NOT NULL CHECK (phase IN (
    'problem_deconstruction',
    'screen_mapping',
    'design_generation',
    'stitch_iteration',
    'code_generation',
    'code_review'
  )),
  progress_pct INTEGER NOT NULL CHECK (progress_pct >= 0 AND progress_pct <= 100),

  -- Optional step, message, and error
  step TEXT,
  message TEXT,
  error TEXT,
  metadata JSONB DEFAULT '{}',

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for efficient queries
CREATE INDEX idx_progress_checkpoints_project_id ON progress_checkpoints(project_id);
CREATE INDEX idx_progress_checkpoints_phase ON progress_checkpoints(phase);
CREATE INDEX idx_progress_checkpoints_created_at ON progress_checkpoints(created_at);

CREATE INDEX idx_progress_events_project_id ON progress_events(project_id);
CREATE INDEX idx_progress_events_event_type ON progress_events(event_type);
CREATE INDEX idx_progress_events_created_at ON progress_events(created_at);

-- Composite index for timeline queries
CREATE INDEX idx_progress_events_project_timeline
  ON progress_events(project_id, created_at DESC);

-- Function to get progress summary for a project
CREATE OR REPLACE FUNCTION get_progress_summary(p_project_id UUID)
RETURNS TABLE (
  overall_progress_pct INTEGER,
  current_phase TEXT,
  current_step TEXT,
  current_step_progress INTEGER,
  phases_completed INTEGER,
  total_phases INTEGER,
  estimated_time_remaining_minutes INTEGER
) AS $$
DECLARE
  latest_checkpoint progress_checkpoints;
  completed_phases INTEGER;
  phase_order TEXT[] := ARRAY[
    'problem_deconstruction',
    'screen_mapping',
    'design_generation',
    'stitch_iteration',
    'code_generation',
    'code_review'
  ];
  phase_index INTEGER;
BEGIN
  -- Get the latest checkpoint
  SELECT * INTO latest_checkpoint
  FROM progress_checkpoints
  WHERE project_id = p_project_id
  ORDER BY created_at DESC
  LIMIT 1;

  IF NOT FOUND THEN
    -- No progress yet
    RETURN QUERY SELECT 0, NULL::TEXT, NULL::TEXT, 0, 0, 6, 60;
    RETURN;
  END IF;

  -- Count completed phases
  SELECT COUNT(DISTINCT phase) INTO completed_phases
  FROM progress_events
  WHERE project_id = p_project_id
    AND event_type = 'phase_complete';

  -- Find current phase index
  FOR i IN 1..array_length(phase_order, 1) LOOP
    IF phase_order[i] = latest_checkpoint.phase THEN
      phase_index := i;
      EXIT;
    END IF;
  END LOOP;

  -- Calculate overall progress
  RETURN QUERY SELECT
    -- Overall progress: (completed_phases + current_phase_progress) / 6 * 100
    ((completed_phases * 100) + latest_checkpoint.progress_pct) / 6 as overall_progress,
    latest_checkpoint.phase as current_phase,
    latest_checkpoint.step_name as current_step,
    latest_checkpoint.progress_pct as step_progress,
    completed_phases as phases_completed,
    6 as total_phases,
    -- Estimate: 10 minutes per remaining phase
    ((6 - completed_phases) * 10 - (latest_checkpoint.progress_pct * 10 / 100)) as est_time_remaining;
END;
$$ LANGUAGE plpgsql;

-- Function to get progress timeline (for UI visualization)
CREATE OR REPLACE FUNCTION get_progress_timeline(
  p_project_id UUID,
  p_limit INTEGER DEFAULT 50
)
RETURNS TABLE (
  event_id UUID,
  event_type TEXT,
  phase TEXT,
  progress_pct INTEGER,
  step TEXT,
  message TEXT,
  error TEXT,
  elapsed_seconds INTEGER,
  created_at TIMESTAMP WITH TIME ZONE
) AS $$
DECLARE
  start_time TIMESTAMP WITH TIME ZONE;
BEGIN
  -- Get workflow start time
  SELECT ws.started_at INTO start_time
  FROM workflow_states ws
  WHERE ws.project_id = p_project_id
  ORDER BY ws.started_at DESC
  LIMIT 1;

  RETURN QUERY
  SELECT
    pe.id,
    pe.event_type,
    pe.phase,
    pe.progress_pct,
    pe.step,
    pe.message,
    pe.error,
    EXTRACT(EPOCH FROM (pe.created_at - start_time))::INTEGER as elapsed_seconds,
    pe.created_at
  FROM progress_events pe
  WHERE pe.project_id = p_project_id
  ORDER BY pe.created_at DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Function to detect stalled workflows (no progress in 30 minutes)
CREATE OR REPLACE FUNCTION detect_stalled_workflows()
RETURNS TABLE (
  project_id UUID,
  last_phase TEXT,
  last_step TEXT,
  last_progress_pct INTEGER,
  minutes_since_last_update INTEGER,
  workflow_status TEXT
) AS $$
BEGIN
  RETURN QUERY
  WITH latest_progress AS (
    SELECT DISTINCT ON (pc.project_id)
      pc.project_id,
      pc.phase,
      pc.step_name,
      pc.progress_pct,
      pc.created_at
    FROM progress_checkpoints pc
    ORDER BY pc.project_id, pc.created_at DESC
  )
  SELECT
    lp.project_id,
    lp.phase as last_phase,
    lp.step_name as last_step,
    lp.progress_pct as last_progress,
    EXTRACT(EPOCH FROM (NOW() - lp.created_at)) / 60 as minutes_since,
    ws.status as workflow_status
  FROM latest_progress lp
  JOIN workflow_states ws ON ws.project_id = lp.project_id
  WHERE lp.created_at < NOW() - INTERVAL '30 minutes'
    AND ws.status = 'active'
  ORDER BY lp.created_at ASC;
END;
$$ LANGUAGE plpgsql;

-- Function to cleanup old progress data (data retention)
CREATE OR REPLACE FUNCTION cleanup_old_progress_data(p_retention_days INTEGER DEFAULT 90)
RETURNS TABLE (
  checkpoints_deleted BIGINT,
  events_deleted BIGINT
) AS $$
DECLARE
  checkpoint_count BIGINT;
  event_count BIGINT;
BEGIN
  -- Delete old checkpoints
  WITH deleted_checkpoints AS (
    DELETE FROM progress_checkpoints
    WHERE created_at < NOW() - (p_retention_days || ' days')::INTERVAL
    RETURNING *
  )
  SELECT COUNT(*) INTO checkpoint_count FROM deleted_checkpoints;

  -- Delete old events
  WITH deleted_events AS (
    DELETE FROM progress_events
    WHERE created_at < NOW() - (p_retention_days || ' days')::INTERVAL
    RETURNING *
  )
  SELECT COUNT(*) INTO event_count FROM deleted_events;

  RETURN QUERY SELECT checkpoint_count, event_count;
END;
$$ LANGUAGE plpgsql;

-- Comments
COMMENT ON TABLE progress_checkpoints IS 'Stores discrete progress checkpoints for each workflow phase and step';
COMMENT ON TABLE progress_events IS 'Stores all progress events including phase starts, completions, and errors';
COMMENT ON FUNCTION get_progress_summary IS 'Returns a comprehensive progress summary for a project';
COMMENT ON FUNCTION get_progress_timeline IS 'Returns a chronological timeline of progress events';
COMMENT ON FUNCTION detect_stalled_workflows IS 'Identifies workflows that have not made progress in 30+ minutes';
COMMENT ON FUNCTION cleanup_old_progress_data IS 'Removes progress data older than specified retention period';
