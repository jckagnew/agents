-- AI Requests Table
-- Tracks all AI model requests for analytics, cost tracking, and debugging

CREATE TABLE ai_requests (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

  -- Request details
  task_type TEXT NOT NULL CHECK (task_type IN (
    'problem_deconstruction',
    'screen_mapping',
    'design_generation',
    'code_generation',
    'code_review',
    'general'
  )),
  model TEXT NOT NULL CHECK (model IN (
    'gpt-4',
    'gpt-4-turbo',
    'gpt-3.5-turbo',
    'claude-3-5-sonnet',
    'claude-3-opus',
    'gemini-1.5-pro',
    'gemini-1.5-flash'
  )),

  -- Token usage
  prompt_tokens INTEGER NOT NULL,
  completion_tokens INTEGER NOT NULL,
  total_tokens INTEGER NOT NULL,

  -- Performance metrics
  latency_ms INTEGER NOT NULL,
  finish_reason TEXT NOT NULL CHECK (finish_reason IN (
    'stop',
    'length',
    'content_filter',
    'error'
  )),

  -- Audit
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for analytics queries
CREATE INDEX idx_ai_requests_user_id ON ai_requests(user_id);
CREATE INDEX idx_ai_requests_project_id ON ai_requests(project_id);
CREATE INDEX idx_ai_requests_task_type ON ai_requests(task_type);
CREATE INDEX idx_ai_requests_model ON ai_requests(model);
CREATE INDEX idx_ai_requests_created_at ON ai_requests(created_at);

-- Composite index for cost analysis
CREATE INDEX idx_ai_requests_user_created ON ai_requests(user_id, created_at);

-- Function to calculate AI costs for a user in a given period
CREATE OR REPLACE FUNCTION calculate_ai_cost(
  p_user_id UUID,
  p_start_date TIMESTAMP WITH TIME ZONE,
  p_end_date TIMESTAMP WITH TIME ZONE
)
RETURNS TABLE (
  total_requests BIGINT,
  total_tokens BIGINT,
  estimated_cost_usd NUMERIC(10, 4),
  breakdown_by_model JSONB
) AS $$
DECLARE
  -- Model costs per 1K tokens (average of prompt + completion)
  model_costs JSONB := '{
    "gpt-4": 0.045,
    "gpt-4-turbo": 0.02,
    "gpt-3.5-turbo": 0.001,
    "claude-3-5-sonnet": 0.009,
    "claude-3-opus": 0.045,
    "gemini-1.5-pro": 0.0031,
    "gemini-1.5-flash": 0.0003
  }'::jsonb;
BEGIN
  RETURN QUERY
  WITH request_stats AS (
    SELECT
      model,
      COUNT(*) as request_count,
      SUM(total_tokens) as tokens_sum,
      SUM(total_tokens::numeric / 1000 * (model_costs->>model)::numeric) as model_cost
    FROM ai_requests
    WHERE user_id = p_user_id
      AND created_at >= p_start_date
      AND created_at < p_end_date
    GROUP BY model
  )
  SELECT
    SUM(request_count)::bigint as total_requests,
    SUM(tokens_sum)::bigint as total_tokens,
    SUM(model_cost)::numeric(10, 4) as estimated_cost_usd,
    jsonb_object_agg(
      model,
      jsonb_build_object(
        'requests', request_count,
        'tokens', tokens_sum,
        'cost_usd', ROUND(model_cost::numeric, 4)
      )
    ) as breakdown_by_model
  FROM request_stats;
END;
$$ LANGUAGE plpgsql;

-- Function to get AI usage statistics for analytics dashboard
CREATE OR REPLACE FUNCTION get_ai_usage_stats(
  p_user_id UUID DEFAULT NULL,
  p_lookback_days INTEGER DEFAULT 30
)
RETURNS TABLE (
  period TEXT,
  requests BIGINT,
  tokens BIGINT,
  avg_latency_ms NUMERIC(10, 2),
  error_rate NUMERIC(5, 2)
) AS $$
BEGIN
  RETURN QUERY
  WITH daily_stats AS (
    SELECT
      DATE(created_at) as stat_date,
      COUNT(*) as request_count,
      SUM(total_tokens) as token_sum,
      AVG(latency_ms) as avg_latency,
      SUM(CASE WHEN finish_reason = 'error' THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100 as error_pct
    FROM ai_requests
    WHERE (p_user_id IS NULL OR user_id = p_user_id)
      AND created_at >= NOW() - (p_lookback_days || ' days')::interval
    GROUP BY DATE(created_at)
    ORDER BY stat_date DESC
  )
  SELECT
    stat_date::text as period,
    request_count as requests,
    token_sum as tokens,
    ROUND(avg_latency::numeric, 2) as avg_latency_ms,
    ROUND(error_pct::numeric, 2) as error_rate
  FROM daily_stats;
END;
$$ LANGUAGE plpgsql;

-- Function to detect anomalous AI usage (for fraud detection)
CREATE OR REPLACE FUNCTION detect_anomalous_usage(p_user_id UUID)
RETURNS TABLE (
  anomaly_type TEXT,
  severity TEXT,
  details TEXT
) AS $$
DECLARE
  recent_requests BIGINT;
  recent_tokens BIGINT;
  avg_requests_per_hour NUMERIC;
  max_tokens_single_request INTEGER;
BEGIN
  -- Count requests in last hour
  SELECT COUNT(*), SUM(total_tokens)
  INTO recent_requests, recent_tokens
  FROM ai_requests
  WHERE user_id = p_user_id
    AND created_at >= NOW() - INTERVAL '1 hour';

  -- Get average requests per hour over last 7 days
  SELECT AVG(hourly_count)
  INTO avg_requests_per_hour
  FROM (
    SELECT DATE_TRUNC('hour', created_at) as hour, COUNT(*) as hourly_count
    FROM ai_requests
    WHERE user_id = p_user_id
      AND created_at >= NOW() - INTERVAL '7 days'
    GROUP BY DATE_TRUNC('hour', created_at)
  ) hourly_stats;

  -- Get max tokens in a single request in last hour
  SELECT MAX(total_tokens)
  INTO max_tokens_single_request
  FROM ai_requests
  WHERE user_id = p_user_id
    AND created_at >= NOW() - INTERVAL '1 hour';

  -- Check for spike in request rate (10x normal)
  IF recent_requests > (COALESCE(avg_requests_per_hour, 10) * 10) THEN
    RETURN QUERY SELECT
      'request_spike'::text,
      'high'::text,
      format('%s requests in last hour (avg: %s)', recent_requests, ROUND(avg_requests_per_hour, 1))::text;
  END IF;

  -- Check for excessive tokens (>100K in single request)
  IF max_tokens_single_request > 100000 THEN
    RETURN QUERY SELECT
      'excessive_tokens'::text,
      'medium'::text,
      format('Single request used %s tokens', max_tokens_single_request)::text;
  END IF;

  -- Check for rapid token consumption (>500K in last hour)
  IF recent_tokens > 500000 THEN
    RETURN QUERY SELECT
      'token_consumption_spike'::text,
      'high'::text,
      format('%s tokens consumed in last hour', recent_tokens)::text;
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Comments
COMMENT ON TABLE ai_requests IS 'Logs all AI model requests for analytics, cost tracking, and fraud detection';
COMMENT ON FUNCTION calculate_ai_cost IS 'Calculates estimated AI costs for a user in a given period';
COMMENT ON FUNCTION get_ai_usage_stats IS 'Returns AI usage statistics for analytics dashboard';
COMMENT ON FUNCTION detect_anomalous_usage IS 'Detects anomalous AI usage patterns for fraud detection';
