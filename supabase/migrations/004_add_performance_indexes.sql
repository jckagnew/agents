-- Additional performance indexes for infrastructure components
-- These indexes optimize common query patterns for job queues, auditing, and cost tracking

-- Code generation jobs: Optimize queue processing
CREATE INDEX idx_code_generation_jobs_status_created
  ON code_generation_jobs(status, created_at)
  WHERE status IN ('queued', 'processing');

-- Code generation jobs: Failed jobs for retry analysis
CREATE INDEX idx_code_generation_jobs_failed
  ON code_generation_jobs(created_at DESC)
  WHERE status = 'failed';

-- Audit logs: Time-range queries for compliance exports
CREATE INDEX idx_audit_logs_created_at_desc ON audit_logs(created_at DESC);

-- Audit logs: Action-based filtering
CREATE INDEX idx_audit_logs_action_created ON audit_logs(action, created_at DESC);

-- AI generations: Cost tracking queries
CREATE INDEX idx_ai_generations_cost ON ai_generations(created_at DESC, cost_usd);

-- AI generations: Provider/model analysis
CREATE INDEX idx_ai_generations_provider_model
  ON ai_generations(model_provider, model_version, created_at DESC);

-- Usage quotas: Fast quota lookups
CREATE UNIQUE INDEX idx_usage_quotas_user_unique ON usage_quotas(user_id);

-- Projects: Active projects query optimization
CREATE INDEX idx_projects_status_updated
  ON projects(status, updated_at DESC)
  WHERE status NOT IN ('complete', 'failed');

-- Add composite index for project status dashboard
CREATE INDEX idx_projects_user_status
  ON projects(user_id, status, created_at DESC);

COMMENT ON INDEX idx_code_generation_jobs_status_created IS 'Optimize queue processing queries';
COMMENT ON INDEX idx_audit_logs_created_at_desc IS 'Optimize compliance export queries';
COMMENT ON INDEX idx_ai_generations_cost IS 'Optimize cost analysis queries';
