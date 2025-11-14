/**
 * Quota Service
 * Enforces usage limits based on subscription tier
 *
 * Features:
 * - Tier-based enforcement (free, pro, enterprise)
 * - Monthly quota resets
 * - Resource tracking (projects, AI tokens, storage)
 * - Over-quota detection and blocking
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';

export type SubscriptionTier = 'free' | 'pro' | 'enterprise';

export interface QuotaLimits {
  tier: SubscriptionTier;
  projects_per_month: number;
  ai_tokens_per_month: number;
  storage_gb: number;
}

export interface QuotaUsage {
  current_projects: number;
  current_ai_tokens: number;
  current_storage_gb: number;
  period_start: Date;
  period_end: Date;
}

export interface QuotaCheckResult {
  allowed: boolean;
  reason?: string;
  current_usage?: number;
  limit?: number;
  percentage_used?: number;
}

export interface QuotaStatus {
  tier: SubscriptionTier;
  limits: QuotaLimits;
  usage: QuotaUsage;
  projects: QuotaCheckResult;
  tokens: QuotaCheckResult;
  storage: QuotaCheckResult;
}

/**
 * Quota tiers configuration
 */
export const QUOTA_TIERS: Record<SubscriptionTier, QuotaLimits> = {
  free: {
    tier: 'free',
    projects_per_month: 3,
    ai_tokens_per_month: 100_000,
    storage_gb: 1.0,
  },
  pro: {
    tier: 'pro',
    projects_per_month: 50,
    ai_tokens_per_month: 5_000_000,
    storage_gb: 10.0,
  },
  enterprise: {
    tier: 'enterprise',
    projects_per_month: Number.MAX_SAFE_INTEGER, // Unlimited
    ai_tokens_per_month: Number.MAX_SAFE_INTEGER, // Unlimited
    storage_gb: Number.MAX_SAFE_INTEGER, // Unlimited
  },
};

/**
 * Quota Service for tier enforcement
 */
export class QuotaService {
  private static instance: QuotaService;
  private client: SupabaseClient;

  constructor(supabaseUrl: string, supabaseKey: string) {
    this.client = createClient(supabaseUrl, supabaseKey);
  }

  /**
   * Get singleton instance
   */
  static getInstance(supabaseUrl?: string, supabaseKey?: string): QuotaService {
    if (!QuotaService.instance) {
      if (!supabaseUrl || !supabaseKey) {
        // Try to get from environment
        supabaseUrl = process.env.SUPABASE_URL;
        supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
      }
      if (!supabaseUrl || !supabaseKey) {
        throw new Error('Supabase credentials required to initialize QuotaService');
      }
      QuotaService.instance = new QuotaService(supabaseUrl, supabaseKey);
    }
    return QuotaService.instance;
  }

  /**
   * Check if user is within quota for a specific resource
   */
  async checkQuota(
    userId: string,
    resourceType: 'project' | 'tokens' | 'storage'
  ): Promise<QuotaCheckResult> {
    // Get user's quota record
    const { data: quota, error } = await this.client
      .from('usage_quotas')
      .select('*')
      .eq('user_id', userId)
      .single();

    if (error) {
      // If quota doesn't exist, create default free tier
      if (error.code === 'PGRST116') {
        await this.initializeUserQuota(userId, 'free');
        return this.checkQuota(userId, resourceType);
      }
      throw error;
    }

    if (!quota) {
      throw new Error(`Quota not found for user ${userId}`);
    }

    // Check if period has expired (monthly reset)
    const now = new Date();
    const periodEnd = new Date(quota.period_end);
    if (now > periodEnd) {
      await this.resetMonthlyQuota(userId);
      return this.checkQuota(userId, resourceType);
    }

    // Get limits for tier
    const limits = QUOTA_TIERS[quota.tier as SubscriptionTier];

    // Check specific resource
    switch (resourceType) {
      case 'project': {
        const allowed = quota.current_projects < limits.projects_per_month;
        return {
          allowed,
          reason: allowed ? undefined : 'monthly_project_limit_exceeded',
          current_usage: quota.current_projects,
          limit: limits.projects_per_month,
          percentage_used: (quota.current_projects / limits.projects_per_month) * 100,
        };
      }
      case 'tokens': {
        const allowed = quota.current_ai_tokens < limits.ai_tokens_per_month;
        return {
          allowed,
          reason: allowed ? undefined : 'monthly_token_limit_exceeded',
          current_usage: quota.current_ai_tokens,
          limit: limits.ai_tokens_per_month,
          percentage_used: (quota.current_ai_tokens / limits.ai_tokens_per_month) * 100,
        };
      }
      case 'storage': {
        const allowed = quota.current_storage_gb < limits.storage_gb;
        return {
          allowed,
          reason: allowed ? undefined : 'storage_limit_exceeded',
          current_usage: quota.current_storage_gb,
          limit: limits.storage_gb,
          percentage_used: (quota.current_storage_gb / limits.storage_gb) * 100,
        };
      }
      default:
        throw new Error(`Unknown resource type: ${resourceType}`);
    }
  }

  /**
   * Increment usage for a resource
   */
  async incrementUsage(
    userId: string,
    resourceType: 'project' | 'tokens' | 'storage',
    amount: number = 1
  ): Promise<void> {
    const field =
      resourceType === 'project'
        ? 'current_projects'
        : resourceType === 'tokens'
          ? 'current_ai_tokens'
          : 'current_storage_gb';

    const { error } = await this.client.rpc('increment_quota_usage', {
      p_user_id: userId,
      p_field: field,
      p_amount: amount,
    });

    if (error) {
      // If function doesn't exist, do manual update
      const { data: current } = await this.client
        .from('usage_quotas')
        .select(field)
        .eq('user_id', userId)
        .single();

      const currentValue = current ? (current as any)[field] : 0;
      const newValue = currentValue + amount;

      const { error: updateError } = await this.client
        .from('usage_quotas')
        .update({
          [field]: newValue,
        })
        .eq('user_id', userId);

      if (updateError) throw updateError;
    }
  }

  /**
   * Decrement usage for a resource (e.g., when project is deleted)
   */
  async decrementUsage(
    userId: string,
    resourceType: 'project' | 'tokens' | 'storage',
    amount: number = 1
  ): Promise<void> {
    const field =
      resourceType === 'project'
        ? 'current_projects'
        : resourceType === 'tokens'
          ? 'current_ai_tokens'
          : 'current_storage_gb';

    // Get current value first
    const { data: current } = await this.client
      .from('usage_quotas')
      .select(field)
      .eq('user_id', userId)
      .single();

    const currentValue = current ? (current as any)[field] : 0;
    const newValue = Math.max(0, currentValue - amount);

    const { error } = await this.client
      .from('usage_quotas')
      .update({
        [field]: newValue,
      })
      .eq('user_id', userId);

    if (error) throw error;
  }

  /**
   * Reset monthly quota (called automatically when period expires)
   */
  async resetMonthlyQuota(userId: string): Promise<void> {
    const now = new Date();
    const nextPeriodEnd = new Date(now);
    nextPeriodEnd.setMonth(nextPeriodEnd.getMonth() + 1);

    const { error } = await this.client
      .from('usage_quotas')
      .update({
        current_projects: 0,
        current_ai_tokens: 0,
        // Note: storage is NOT reset monthly
        period_start: now.toISOString(),
        period_end: nextPeriodEnd.toISOString(),
      })
      .eq('user_id', userId);

    if (error) throw error;
  }

  /**
   * Get full quota status for a user
   */
  async getQuotaStatus(userId: string): Promise<QuotaStatus> {
    const { data: quota, error } = await this.client
      .from('usage_quotas')
      .select('*')
      .eq('user_id', userId)
      .single();

    if (error) throw error;
    if (!quota) throw new Error(`Quota not found for user ${userId}`);

    const tier = quota.tier as SubscriptionTier;
    const limits = QUOTA_TIERS[tier];

    // Check each resource
    const [projects, tokens, storage] = await Promise.all([
      this.checkQuota(userId, 'project'),
      this.checkQuota(userId, 'tokens'),
      this.checkQuota(userId, 'storage'),
    ]);

    return {
      tier,
      limits,
      usage: {
        current_projects: quota.current_projects,
        current_ai_tokens: quota.current_ai_tokens,
        current_storage_gb: quota.current_storage_gb,
        period_start: new Date(quota.period_start),
        period_end: new Date(quota.period_end),
      },
      projects,
      tokens,
      storage,
    };
  }

  /**
   * Update user's subscription tier
   */
  async updateTier(userId: string, newTier: SubscriptionTier): Promise<void> {
    const newLimits = QUOTA_TIERS[newTier];

    const { error } = await this.client
      .from('usage_quotas')
      .update({
        tier: newTier,
        projects_per_month: newLimits.projects_per_month,
        ai_tokens_per_month: newLimits.ai_tokens_per_month,
        storage_gb: newLimits.storage_gb,
      })
      .eq('user_id', userId);

    if (error) throw error;
  }

  /**
   * Initialize quota for new user
   */
  async initializeUserQuota(
    userId: string,
    tier: SubscriptionTier = 'free'
  ): Promise<void> {
    const limits = QUOTA_TIERS[tier];
    const now = new Date();
    const periodEnd = new Date(now);
    periodEnd.setMonth(periodEnd.getMonth() + 1);

    const { error } = await this.client.from('usage_quotas').insert({
      user_id: userId,
      tier,
      projects_per_month: limits.projects_per_month,
      ai_tokens_per_month: limits.ai_tokens_per_month,
      storage_gb: limits.storage_gb,
      current_projects: 0,
      current_ai_tokens: 0,
      current_storage_gb: 0,
      period_start: now.toISOString(),
      period_end: periodEnd.toISOString(),
    });

    if (error && error.code !== '23505') {
      // Ignore duplicate key error
      throw error;
    }
  }

  /**
   * Check if user needs to upgrade (soft limit warning)
   */
  async checkUpgradeNeeded(userId: string): Promise<{
    should_upgrade: boolean;
    reason?: string;
    resource?: string;
  }> {
    const status = await this.getQuotaStatus(userId);

    // Warn at 80% usage
    const WARNING_THRESHOLD = 80;

    if (status.projects.percentage_used && status.projects.percentage_used >= WARNING_THRESHOLD) {
      return {
        should_upgrade: true,
        reason: 'approaching_project_limit',
        resource: 'projects',
      };
    }

    if (status.tokens.percentage_used && status.tokens.percentage_used >= WARNING_THRESHOLD) {
      return {
        should_upgrade: true,
        reason: 'approaching_token_limit',
        resource: 'tokens',
      };
    }

    if (status.storage.percentage_used && status.storage.percentage_used >= WARNING_THRESHOLD) {
      return {
        should_upgrade: true,
        reason: 'approaching_storage_limit',
        resource: 'storage',
      };
    }

    return { should_upgrade: false };
  }
}

/**
 * Singleton instance
 */
let quotaServiceInstance: QuotaService | null = null;

export function getQuotaService(
  supabaseUrl?: string,
  supabaseKey?: string
): QuotaService {
  if (!quotaServiceInstance && (!supabaseUrl || !supabaseKey)) {
    throw new Error('Supabase config required to initialize QuotaService');
  }

  if (supabaseUrl && supabaseKey && !quotaServiceInstance) {
    quotaServiceInstance = new QuotaService(supabaseUrl, supabaseKey);
  }

  return quotaServiceInstance!;
}
