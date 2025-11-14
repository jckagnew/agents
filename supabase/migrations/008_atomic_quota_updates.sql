-- Migration: Atomic Quota Updates
-- Fixes race condition in quota increment/decrement operations
-- Created: 2025-11-14

-- Function: Atomically increment quota usage
-- Prevents race conditions when multiple requests increment simultaneously
CREATE OR REPLACE FUNCTION increment_quota_usage(
  p_user_id UUID,
  p_field TEXT,
  p_amount INTEGER
)
RETURNS void AS $$
BEGIN
  -- Atomic update using SQL
  UPDATE usage_quotas
  SET
    current_projects = CASE
      WHEN p_field = 'current_projects' THEN current_projects + p_amount
      ELSE current_projects
    END,
    current_ai_tokens = CASE
      WHEN p_field = 'current_ai_tokens' THEN current_ai_tokens + p_amount
      ELSE current_ai_tokens
    END,
    current_storage_gb = CASE
      WHEN p_field = 'current_storage_gb' THEN current_storage_gb + p_amount
      ELSE current_storage_gb
    END
  WHERE user_id = p_user_id;

  -- If no row exists, insert default quota
  IF NOT FOUND THEN
    INSERT INTO usage_quotas (
      user_id,
      current_projects,
      current_ai_tokens,
      current_storage_gb,
      max_projects,
      max_ai_tokens,
      max_storage_gb
    ) VALUES (
      p_user_id,
      CASE WHEN p_field = 'current_projects' THEN p_amount ELSE 0 END,
      CASE WHEN p_field = 'current_ai_tokens' THEN p_amount ELSE 0 END,
      CASE WHEN p_field = 'current_storage_gb' THEN p_amount ELSE 0 END,
      10,  -- Default max projects
      1000000,  -- Default max tokens
      5  -- Default max storage GB
    );
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Atomically decrement quota usage
-- Prevents race conditions when multiple requests decrement simultaneously
-- Ensures value never goes below zero
CREATE OR REPLACE FUNCTION decrement_quota_usage(
  p_user_id UUID,
  p_field TEXT,
  p_amount INTEGER
)
RETURNS void AS $$
BEGIN
  -- Atomic update using SQL with GREATEST to prevent negative values
  UPDATE usage_quotas
  SET
    current_projects = CASE
      WHEN p_field = 'current_projects' THEN GREATEST(0, current_projects - p_amount)
      ELSE current_projects
    END,
    current_ai_tokens = CASE
      WHEN p_field = 'current_ai_tokens' THEN GREATEST(0, current_ai_tokens - p_amount)
      ELSE current_ai_tokens
    END,
    current_storage_gb = CASE
      WHEN p_field = 'current_storage_gb' THEN GREATEST(0, current_storage_gb - p_amount)
      ELSE current_storage_gb
    END
  WHERE user_id = p_user_id;

  -- If no row exists, create one (decrementing from 0 stays at 0)
  IF NOT FOUND THEN
    INSERT INTO usage_quotas (
      user_id,
      current_projects,
      current_ai_tokens,
      current_storage_gb,
      max_projects,
      max_ai_tokens,
      max_storage_gb
    ) VALUES (
      p_user_id,
      0, 0, 0,  -- All current usage at 0
      10, 1000000, 5  -- Default limits
    );
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permissions to authenticated users
GRANT EXECUTE ON FUNCTION increment_quota_usage(UUID, TEXT, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION decrement_quota_usage(UUID, TEXT, INTEGER) TO authenticated;

-- Add comment for documentation
COMMENT ON FUNCTION increment_quota_usage IS 'Atomically increment usage quota - prevents race conditions';
COMMENT ON FUNCTION decrement_quota_usage IS 'Atomically decrement usage quota - prevents race conditions and negative values';
