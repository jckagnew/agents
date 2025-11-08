-- Add progress tracking to code_generation_jobs
-- This enables real-time progress updates for users

ALTER TABLE code_generation_jobs
ADD COLUMN progress_pct INTEGER DEFAULT 0 CHECK (progress_pct >= 0 AND progress_pct <= 100),
ADD COLUMN current_step TEXT;

-- Create index for querying jobs by progress
CREATE INDEX idx_code_generation_jobs_progress ON code_generation_jobs(progress_pct)
WHERE status = 'processing';

-- Add comment for documentation
COMMENT ON COLUMN code_generation_jobs.progress_pct IS 'Job completion percentage (0-100)';
COMMENT ON COLUMN code_generation_jobs.current_step IS 'Current step description for user feedback';
