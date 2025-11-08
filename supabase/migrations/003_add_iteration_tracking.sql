-- Iteration tracking to prevent infinite loops
-- Tracks iterations per workflow phase with configurable limits

CREATE TABLE iteration_tracking (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Workflow phase being iterated
  phase TEXT NOT NULL CHECK (phase IN (
    'problem_deconstruction',
    'screen_mapping',
    'design_generation',
    'stitch_iteration',
    'code_generation',
    'code_review'
  )),

  -- Iteration details
  iteration_count INTEGER NOT NULL DEFAULT 1,
  max_iterations INTEGER NOT NULL DEFAULT 5,

  -- Metadata
  last_iteration_reason TEXT,
  metadata JSONB DEFAULT '{}',

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_iteration_tracking_project_id ON iteration_tracking(project_id);
CREATE INDEX idx_iteration_tracking_phase ON iteration_tracking(phase);
CREATE UNIQUE INDEX idx_iteration_tracking_project_phase ON iteration_tracking(project_id, phase);

-- Enable RLS
ALTER TABLE iteration_tracking ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Access through project ownership
CREATE POLICY "Users can access iteration tracking for their projects"
  ON iteration_tracking FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = iteration_tracking.project_id
      AND projects.user_id = auth.uid()
    )
  );

-- Trigger to update updated_at
CREATE TRIGGER update_iteration_tracking_updated_at
  BEFORE UPDATE ON iteration_tracking
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Helper function: Check if iteration limit reached
CREATE OR REPLACE FUNCTION check_iteration_limit(p_project_id UUID, p_phase TEXT)
RETURNS BOOLEAN AS $$
DECLARE
  current_iteration iteration_tracking;
BEGIN
  SELECT * INTO current_iteration
  FROM iteration_tracking
  WHERE project_id = p_project_id AND phase = p_phase;

  IF NOT FOUND THEN
    -- First iteration, create tracking record
    INSERT INTO iteration_tracking (project_id, phase, iteration_count)
    VALUES (p_project_id, p_phase, 1);
    RETURN TRUE; -- Within limit
  END IF;

  -- Check if we've exceeded max iterations
  RETURN current_iteration.iteration_count < current_iteration.max_iterations;
END;
$$ LANGUAGE plpgsql;

-- Helper function: Increment iteration count
CREATE OR REPLACE FUNCTION increment_iteration(p_project_id UUID, p_phase TEXT, p_reason TEXT DEFAULT NULL)
RETURNS INTEGER AS $$
DECLARE
  new_count INTEGER;
BEGIN
  INSERT INTO iteration_tracking (project_id, phase, iteration_count, last_iteration_reason)
  VALUES (p_project_id, p_phase, 1, p_reason)
  ON CONFLICT (project_id, phase)
  DO UPDATE SET
    iteration_count = iteration_tracking.iteration_count + 1,
    last_iteration_reason = COALESCE(p_reason, iteration_tracking.last_iteration_reason),
    updated_at = NOW()
  RETURNING iteration_count INTO new_count;

  RETURN new_count;
END;
$$ LANGUAGE plpgsql;

COMMENT ON TABLE iteration_tracking IS 'Tracks iterations per workflow phase to prevent infinite loops';
COMMENT ON FUNCTION check_iteration_limit IS 'Returns TRUE if within iteration limit for the phase';
COMMENT ON FUNCTION increment_iteration IS 'Increments iteration count and returns new count';
