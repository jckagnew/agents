-- Migration: Market Research Reports
-- Stores daily market intelligence reports for review in admin console
-- Created: 2025-11-17

CREATE TABLE IF NOT EXISTS market_research_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_date DATE NOT NULL DEFAULT CURRENT_DATE,
  report_timestamp TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
  
  -- Report content
  executive_summary TEXT,
  full_report TEXT NOT NULL,
  market_count INTEGER NOT NULL DEFAULT 0,
  
  -- Market configuration snapshot (for historical reference)
  market_config JSONB NOT NULL DEFAULT '[]'::jsonb,
  
  -- Metadata
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
  
  -- Ensure one report per day
  CONSTRAINT unique_report_date UNIQUE (report_date)
);

-- Index for date-based queries
CREATE INDEX IF NOT EXISTS market_research_reports_date_idx 
  ON market_research_reports (report_date DESC);

-- Index for full-text search on reports
CREATE INDEX IF NOT EXISTS market_research_reports_fulltext_idx 
  ON market_research_reports USING gin (to_tsvector('english', full_report));

-- Table for individual market insights (normalized from reports)
CREATE TABLE IF NOT EXISTS market_insights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID NOT NULL REFERENCES market_research_reports(id) ON DELETE CASCADE,
  
  -- Market identification
  market_id TEXT NOT NULL,
  market_name TEXT NOT NULL,
  
  -- Insights
  sentiment_analysis TEXT,
  key_trends TEXT[],
  opportunities TEXT[],
  threats TEXT[],
  competitor_activity TEXT,
  
  -- Search metadata
  search_keywords TEXT[],
  competitors_tracked TEXT[],
  
  created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

CREATE INDEX IF NOT EXISTS market_insights_report_id_idx 
  ON market_insights (report_id);

CREATE INDEX IF NOT EXISTS market_insights_market_id_idx 
  ON market_insights (market_id);

-- RLS Policies
ALTER TABLE market_research_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE market_insights ENABLE ROW LEVEL SECURITY;

-- Admin users can read all reports
CREATE POLICY "Admin users can view all market research reports"
  ON market_research_reports
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM admin_users
      WHERE admin_users.user_id = auth.uid()
      AND admin_users.is_active = true
      AND admin_users.role IN ('super_admin', 'admin')
    )
  );

-- Admin users can insert reports (for automated workflows)
CREATE POLICY "Admin users and service role can insert market research reports"
  ON market_research_reports
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM admin_users
      WHERE admin_users.user_id = auth.uid()
      AND admin_users.is_active = true
    )
    OR auth.jwt()->>'role' = 'service_role'
  );

-- Admin users can view all insights
CREATE POLICY "Admin users can view all market insights"
  ON market_insights
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM admin_users
      WHERE admin_users.user_id = auth.uid()
      AND admin_users.is_active = true
      AND admin_users.role IN ('super_admin', 'admin')
    )
  );

-- Service role can insert insights (for automated workflows)
CREATE POLICY "Service role can insert market insights"
  ON market_insights
  FOR INSERT
  WITH CHECK (auth.jwt()->>'role' = 'service_role');

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION set_market_research_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = timezone('utc', now());
  RETURN NEW;
END;
$$;

CREATE TRIGGER set_market_research_reports_updated_at
  BEFORE UPDATE ON market_research_reports
  FOR EACH ROW
  EXECUTE FUNCTION set_market_research_updated_at();

-- Function to get latest report
CREATE OR REPLACE FUNCTION get_latest_market_research_report()
RETURNS TABLE (
  id UUID,
  report_date DATE,
  executive_summary TEXT,
  full_report TEXT,
  market_count INTEGER,
  created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  SELECT 
    mrr.id,
    mrr.report_date,
    mrr.executive_summary,
    mrr.full_report,
    mrr.market_count,
    mrr.created_at
  FROM market_research_reports mrr
  ORDER BY mrr.report_date DESC
  LIMIT 1;
END;
$$;

-- Function to get reports by date range
CREATE OR REPLACE FUNCTION get_market_research_reports(
  start_date DATE DEFAULT NULL,
  end_date DATE DEFAULT NULL,
  limit_count INTEGER DEFAULT 30
)
RETURNS TABLE (
  id UUID,
  report_date DATE,
  executive_summary TEXT,
  full_report TEXT,
  market_count INTEGER,
  created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  SELECT 
    mrr.id,
    mrr.report_date,
    mrr.executive_summary,
    mrr.full_report,
    mrr.market_count,
    mrr.created_at
  FROM market_research_reports mrr
  WHERE 
    (start_date IS NULL OR mrr.report_date >= start_date)
    AND (end_date IS NULL OR mrr.report_date <= end_date)
  ORDER BY mrr.report_date DESC
  LIMIT limit_count;
END;
$$;

-- Grant permissions
GRANT SELECT ON market_research_reports TO authenticated;
GRANT SELECT ON market_insights TO authenticated;
GRANT EXECUTE ON FUNCTION get_latest_market_research_report() TO authenticated;
GRANT EXECUTE ON FUNCTION get_market_research_reports(DATE, DATE, INTEGER) TO authenticated;

