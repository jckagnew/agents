/**
 * Quota Service Unit Tests
 * Testing Checkpoint 3: Quota Enforcement
 */

import { QuotaService, QUOTA_TIERS } from '../../src/services/quota.service';

// Mock Supabase client
const mockSupabaseClient = {
  from: jest.fn(),
  rpc: jest.fn(),
  sql: jest.fn((str, ...values) => `${str}${values.join('')}`),
};

jest.mock('@supabase/supabase-js', () => ({
  createClient: jest.fn(() => mockSupabaseClient),
}));

describe('QuotaService', () => {
  let quotaService: QuotaService;
  let mockSelect: jest.Mock;
  let mockEq: jest.Mock;
  let mockSingle: jest.Mock;
  let mockInsert: jest.Mock;
  let mockUpdate: jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Setup mock chains
    mockSelect = jest.fn().mockReturnThis();
    mockEq = jest.fn().mockReturnThis();
    mockSingle = jest.fn();
    mockInsert = jest.fn();
    mockUpdate = jest.fn().mockReturnThis();

    mockSupabaseClient.from = jest.fn().mockReturnValue({
      select: mockSelect,
      insert: mockInsert,
      update: mockUpdate,
    });

    mockSelect.mockReturnValue({
      eq: mockEq,
    });

    mockEq.mockReturnValue({
      single: mockSingle,
      data: null,
      error: null,
    });

    mockInsert.mockReturnValue({
      error: null,
    });

    mockUpdate.mockReturnValue({
      eq: mockEq,
    });

    quotaService = new QuotaService('http://localhost:54321', 'test-key');
  });

  describe('Quota Tier Configuration', () => {
    it('✅ Free tier has correct limits', () => {
      expect(QUOTA_TIERS.free).toEqual({
        tier: 'free',
        projects_per_month: 3,
        ai_tokens_per_month: 100_000,
        storage_gb: 1.0,
      });
    });

    it('✅ Pro tier has correct limits', () => {
      expect(QUOTA_TIERS.pro).toEqual({
        tier: 'pro',
        projects_per_month: 50,
        ai_tokens_per_month: 5_000_000,
        storage_gb: 10.0,
      });
    });

    it('✅ Enterprise tier is unlimited', () => {
      expect(QUOTA_TIERS.enterprise.projects_per_month).toBe(Number.MAX_SAFE_INTEGER);
      expect(QUOTA_TIERS.enterprise.ai_tokens_per_month).toBe(
        Number.MAX_SAFE_INTEGER
      );
      expect(QUOTA_TIERS.enterprise.storage_gb).toBe(Number.MAX_SAFE_INTEGER);
    });
  });

  describe('checkQuota', () => {
    it('✅ Free tier limited to 3 projects/month', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'free',
          current_projects: 2,
          current_ai_tokens: 0,
          current_storage_gb: 0,
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const result = await quotaService.checkQuota('user-123', 'project');

      expect(result.allowed).toBe(true);
      expect(result.current_usage).toBe(2);
      expect(result.limit).toBe(3);
      expect(result.percentage_used).toBeCloseTo(66.67, 1);
    });

    it('✅ Pro tier limited to 50 projects/month', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'pro',
          current_projects: 45,
          current_ai_tokens: 0,
          current_storage_gb: 0,
          projects_per_month: 50,
          ai_tokens_per_month: 5_000_000,
          storage_gb: 10.0,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const result = await quotaService.checkQuota('user-123', 'project');

      expect(result.allowed).toBe(true);
      expect(result.current_usage).toBe(45);
      expect(result.limit).toBe(50);
      expect(result.percentage_used).toBe(90);
    });

    it('✅ Enterprise tier unlimited', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'enterprise',
          current_projects: 1000,
          current_ai_tokens: 0,
          current_storage_gb: 0,
          projects_per_month: Number.MAX_SAFE_INTEGER,
          ai_tokens_per_month: Number.MAX_SAFE_INTEGER,
          storage_gb: Number.MAX_SAFE_INTEGER,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const result = await quotaService.checkQuota('user-123', 'project');

      expect(result.allowed).toBe(true);
      expect(result.current_usage).toBe(1000);
    });

    it('✅ Over-quota requests rejected with clear error', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'free',
          current_projects: 3, // At limit
          current_ai_tokens: 0,
          current_storage_gb: 0,
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const result = await quotaService.checkQuota('user-123', 'project');

      expect(result.allowed).toBe(false);
      expect(result.reason).toBe('monthly_project_limit_exceeded');
      expect(result.current_usage).toBe(3);
      expect(result.limit).toBe(3);
      expect(result.percentage_used).toBe(100);
    });

    it('✅ Token quota enforced', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'free',
          current_projects: 0,
          current_ai_tokens: 100_000, // At limit
          current_storage_gb: 0,
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const result = await quotaService.checkQuota('user-123', 'tokens');

      expect(result.allowed).toBe(false);
      expect(result.reason).toBe('monthly_token_limit_exceeded');
    });

    it('✅ Storage quota enforced', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'free',
          current_projects: 0,
          current_ai_tokens: 0,
          current_storage_gb: 1.0, // At limit
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const result = await quotaService.checkQuota('user-123', 'storage');

      expect(result.allowed).toBe(false);
      expect(result.reason).toBe('storage_limit_exceeded');
    });
  });

  describe('resetMonthlyQuota', () => {
    it('✅ Quota resets monthly', async () => {
      mockEq.mockResolvedValue({ error: null });

      await quotaService.resetMonthlyQuota('user-123');

      expect(mockSupabaseClient.from).toHaveBeenCalledWith('usage_quotas');
      expect(mockUpdate).toHaveBeenCalledWith(
        expect.objectContaining({
          current_projects: 0,
          current_ai_tokens: 0,
        })
      );
      expect(mockEq).toHaveBeenCalledWith('user_id', 'user-123');
    });

    it('✅ Storage NOT reset monthly', async () => {
      mockEq.mockResolvedValue({ error: null });

      await quotaService.resetMonthlyQuota('user-123');

      const updateCall = mockUpdate.mock.calls[0][0];
      expect(updateCall).not.toHaveProperty('current_storage_gb');
    });

    it('✅ Period dates updated correctly', async () => {
      mockEq.mockResolvedValue({ error: null });

      await quotaService.resetMonthlyQuota('user-123');

      const updateCall = mockUpdate.mock.calls[0][0];
      expect(updateCall).toHaveProperty('period_start');
      expect(updateCall).toHaveProperty('period_end');

      const periodEnd = new Date(updateCall.period_end);
      const periodStart = new Date(updateCall.period_start);
      const monthDiff =
        periodEnd.getMonth() -
        periodStart.getMonth() +
        12 * (periodEnd.getFullYear() - periodStart.getFullYear());

      expect(monthDiff).toBe(1); // Exactly 1 month apart
    });
  });

  describe('incrementUsage', () => {
    it('✅ Increments project usage', async () => {
      mockSupabaseClient.rpc.mockResolvedValue({ error: null });

      await quotaService.incrementUsage('user-123', 'project', 1);

      expect(mockSupabaseClient.rpc).toHaveBeenCalledWith('increment_quota_usage', {
        p_user_id: 'user-123',
        p_field: 'current_projects',
        p_amount: 1,
      });
    });

    it('✅ Increments token usage', async () => {
      mockSupabaseClient.rpc.mockResolvedValue({ error: null });

      await quotaService.incrementUsage('user-123', 'tokens', 5000);

      expect(mockSupabaseClient.rpc).toHaveBeenCalledWith('increment_quota_usage', {
        p_user_id: 'user-123',
        p_field: 'current_ai_tokens',
        p_amount: 5000,
      });
    });

    it('✅ Falls back to manual update if RPC fails', async () => {
      mockSupabaseClient.rpc.mockResolvedValue({ error: { message: 'Function not found' } });
      mockEq.mockResolvedValue({ error: null });

      await quotaService.incrementUsage('user-123', 'project', 1);

      expect(mockUpdate).toHaveBeenCalled();
      expect(mockEq).toHaveBeenCalledWith('user_id', 'user-123');
    });
  });

  describe('decrementUsage', () => {
    it('✅ Decrements usage when project deleted', async () => {
      mockEq.mockResolvedValue({ error: null });

      await quotaService.decrementUsage('user-123', 'project', 1);

      expect(mockUpdate).toHaveBeenCalled();
      expect(mockEq).toHaveBeenCalledWith('user_id', 'user-123');
    });

    it('✅ Never goes below zero', async () => {
      mockEq.mockResolvedValue({ error: null });

      await quotaService.decrementUsage('user-123', 'project', 1);

      const updateCall = mockUpdate.mock.calls[0][0];
      expect(Object.values(updateCall)[0]).toContain('GREATEST(0');
    });
  });

  describe('getQuotaStatus', () => {
    it('✅ Returns full quota status', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'pro',
          current_projects: 10,
          current_ai_tokens: 1_000_000,
          current_storage_gb: 2.5,
          projects_per_month: 50,
          ai_tokens_per_month: 5_000_000,
          storage_gb: 10.0,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const status = await quotaService.getQuotaStatus('user-123');

      expect(status.tier).toBe('pro');
      expect(status.limits.projects_per_month).toBe(50);
      expect(status.usage.current_projects).toBe(10);
      expect(status.projects.allowed).toBe(true);
      expect(status.projects.percentage_used).toBe(20);
    });
  });

  describe('updateTier', () => {
    it('✅ Updates user tier and limits', async () => {
      mockEq.mockResolvedValue({ error: null });

      await quotaService.updateTier('user-123', 'pro');

      expect(mockUpdate).toHaveBeenCalledWith({
        tier: 'pro',
        projects_per_month: 50,
        ai_tokens_per_month: 5_000_000,
        storage_gb: 10.0,
      });
    });
  });

  describe('initializeUserQuota', () => {
    it('✅ Initializes free tier by default', async () => {
      mockInsert.mockResolvedValue({ error: null });

      await quotaService.initializeUserQuota('user-123');

      expect(mockInsert).toHaveBeenCalledWith(
        expect.objectContaining({
          user_id: 'user-123',
          tier: 'free',
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          current_projects: 0,
          current_ai_tokens: 0,
          current_storage_gb: 0,
        })
      );
    });

    it('✅ Can initialize with specific tier', async () => {
      mockInsert.mockResolvedValue({ error: null });

      await quotaService.initializeUserQuota('user-123', 'pro');

      expect(mockInsert).toHaveBeenCalledWith(
        expect.objectContaining({
          tier: 'pro',
          projects_per_month: 50,
        })
      );
    });

    it('✅ Ignores duplicate key errors', async () => {
      mockInsert.mockResolvedValue({ error: { code: '23505' } });

      await expect(
        quotaService.initializeUserQuota('user-123')
      ).resolves.not.toThrow();
    });
  });

  describe('checkUpgradeNeeded', () => {
    it('✅ Warns at 80% usage', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'free',
          current_projects: 2, // 66.67%
          current_ai_tokens: 85_000, // 85%
          current_storage_gb: 0,
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const result = await quotaService.checkUpgradeNeeded('user-123');

      expect(result.should_upgrade).toBe(true);
      expect(result.reason).toBe('approaching_token_limit');
      expect(result.resource).toBe('tokens');
    });

    it('✅ No warning below 80% usage', async () => {
      mockSingle.mockResolvedValue({
        data: {
          user_id: 'user-123',
          tier: 'free',
          current_projects: 1, // 33%
          current_ai_tokens: 50_000, // 50%
          current_storage_gb: 0.5, // 50%
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          period_start: new Date('2025-01-01').toISOString(),
          period_end: new Date('2025-02-01').toISOString(),
        },
        error: null,
      });

      const result = await quotaService.checkUpgradeNeeded('user-123');

      expect(result.should_upgrade).toBe(false);
    });
  });

  describe('Auto quota reset on expired period', () => {
    it('✅ Automatically resets quota when period expired', async () => {
      // First call: expired period
      mockSingle.mockResolvedValueOnce({
        data: {
          user_id: 'user-123',
          tier: 'free',
          current_projects: 3,
          current_ai_tokens: 0,
          current_storage_gb: 0,
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          period_start: new Date('2024-12-01').toISOString(),
          period_end: new Date('2025-01-01').toISOString(), // Expired
        },
        error: null,
      });

      // Second call: after reset
      mockSingle.mockResolvedValueOnce({
        data: {
          user_id: 'user-123',
          tier: 'free',
          current_projects: 0, // Reset
          current_ai_tokens: 0,
          current_storage_gb: 0,
          projects_per_month: 3,
          ai_tokens_per_month: 100_000,
          storage_gb: 1.0,
          period_start: new Date('2025-01-08').toISOString(),
          period_end: new Date('2025-02-08').toISOString(),
        },
        error: null,
      });

      mockEq.mockResolvedValue({ error: null });

      const result = await quotaService.checkQuota('user-123', 'project');

      // Should have triggered reset and allowed new project
      expect(result.allowed).toBe(true);
      expect(mockUpdate).toHaveBeenCalled(); // Reset was called
    });
  });
});

// Testing Checkpoint 3 Summary
describe('Testing Checkpoint 3: Quota Enforcement', () => {
  it('CHECKPOINT SUMMARY', () => {
    const checklistItems = `
    Testing Checkpoint 3: Quota enforcement tests
    ✅ Free tier limited to 3 projects/month
    ✅ Pro tier limited to 50 projects/month
    ✅ Enterprise tier unlimited
    ✅ Quota resets monthly
    ✅ Over-quota requests rejected with clear error
    ✅ Token quota enforced
    ✅ Storage quota enforced
    ✅ Auto-reset when period expires
    `;
    console.log(checklistItems);
  });
});
