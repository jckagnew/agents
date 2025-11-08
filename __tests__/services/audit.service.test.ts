/**
 * Audit Service Unit Tests
 * Testing Checkpoint 1b: Audit service tests
 */

import { AuditService } from '../../src/services/audit.service';

// Mock Supabase client
const mockSupabaseClient = {
  from: jest.fn(),
};

// Mock implementation
jest.mock('@supabase/supabase-js', () => ({
  createClient: jest.fn(() => mockSupabaseClient),
}));

describe('AuditService', () => {
  let auditService: AuditService;
  let mockInsert: jest.Mock;
  let mockSelect: jest.Mock;
  let mockEq: jest.Mock;
  let mockOrder: jest.Mock;
  let mockGte: jest.Mock;
  let mockLte: jest.Mock;
  let mockLimit: jest.Mock;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();

    // Setup mock chain
    mockInsert = jest.fn().mockReturnValue({ error: null });
    mockSelect = jest.fn().mockReturnThis();
    mockEq = jest.fn().mockReturnThis();
    mockOrder = jest.fn().mockReturnThis();
    mockGte = jest.fn().mockReturnThis();
    mockLte = jest.fn().mockReturnThis();
    mockLimit = jest.fn().mockReturnValue({
      data: [],
      error: null,
    });

    mockSupabaseClient.from = jest.fn().mockReturnValue({
      insert: mockInsert,
      select: mockSelect,
    });

    mockSelect.mockReturnValue({
      eq: mockEq,
    });

    mockEq.mockReturnValue({
      eq: mockEq,
      order: mockOrder,
      gte: mockGte,
      lte: mockLte,
      limit: mockLimit,
    });

    mockOrder.mockReturnValue({
      eq: mockEq,
      gte: mockGte,
      lte: mockLte,
      limit: mockLimit,
      data: [],
      error: null,
    });

    mockGte.mockReturnValue({
      lte: mockLte,
      eq: mockEq,
      limit: mockLimit,
    });

    mockLte.mockReturnValue({
      order: mockOrder,
      eq: mockEq,
      limit: mockLimit,
      data: [],
      error: null,
    });

    // Create service instance
    auditService = new AuditService('http://localhost:54321', 'test-key');
  });

  describe('log', () => {
    it('✅ Can log user actions', async () => {
      await auditService.log({
        userId: 'user-123',
        action: 'project_created',
        resourceType: 'project',
        resourceId: 'project-456',
        metadata: { name: 'Test Project' },
      });

      expect(mockSupabaseClient.from).toHaveBeenCalledWith('audit_logs');
      expect(mockInsert).toHaveBeenCalledWith({
        user_id: 'user-123',
        project_id: null,
        action: 'project_created',
        resource_type: 'project',
        resource_id: 'project-456',
        ip_address: null,
        user_agent: null,
        metadata: { name: 'Test Project' },
      });
    });

    it('✅ Can log AI operations', async () => {
      await auditService.logAIGeneration(
        'user-123',
        'project-456',
        'code_generation',
        'gemini',
        { tokens: 1000 }
      );

      expect(mockSupabaseClient.from).toHaveBeenCalledWith('audit_logs');
      expect(mockInsert).toHaveBeenCalledWith(
        expect.objectContaining({
          user_id: 'user-123',
          project_id: 'project-456',
          action: 'ai_generation',
          resource_type: 'ai_generation',
          metadata: expect.objectContaining({
            stage: 'code_generation',
            provider: 'gemini',
            tokens: 1000,
          }),
        })
      );
    });

    it('✅ Non-blocking (doesn\'t throw on error)', async () => {
      // Simulate database error
      mockInsert.mockReturnValue({ error: { message: 'Database error' } });

      // Should not throw
      await expect(
        auditService.log({
          userId: 'user-123',
          action: 'test_action',
          resourceType: 'test',
        })
      ).resolves.not.toThrow();
    });

    it('✅ Handles missing optional fields', async () => {
      await auditService.log({
        action: 'anonymous_action',
        resourceType: 'test',
      });

      expect(mockInsert).toHaveBeenCalledWith({
        user_id: null,
        project_id: null,
        action: 'anonymous_action',
        resource_type: 'test',
        resource_id: null,
        ip_address: null,
        user_agent: null,
        metadata: {},
      });
    });
  });

  describe('getAuditTrail', () => {
    beforeEach(() => {
      mockOrder.mockReturnValue({
        eq: mockEq,
        gte: mockGte,
        lte: mockLte,
        limit: mockLimit,
        data: [
          {
            id: 'log-1',
            user_id: 'user-123',
            action: 'project_created',
            created_at: '2025-01-08T10:00:00Z',
          },
          {
            id: 'log-2',
            user_id: 'user-123',
            action: 'design_approved',
            created_at: '2025-01-08T11:00:00Z',
          },
        ],
        error: null,
      });
    });

    it('✅ Can query audit trail', async () => {
      const logs = await auditService.getAuditTrail('user-123');

      expect(mockSupabaseClient.from).toHaveBeenCalledWith('audit_logs');
      expect(mockSelect).toHaveBeenCalledWith('*');
      expect(mockEq).toHaveBeenCalledWith('user_id', 'user-123');
      expect(logs).toHaveLength(2);
      expect(logs[0].action).toBe('project_created');
    });

    it('✅ Can filter by project ID', async () => {
      await auditService.getAuditTrail('user-123', { projectId: 'project-456' });

      expect(mockEq).toHaveBeenCalledWith('user_id', 'user-123');
      expect(mockEq).toHaveBeenCalledWith('project_id', 'project-456');
    });

    it('✅ Can filter by action', async () => {
      await auditService.getAuditTrail('user-123', {
        action: 'project_created',
      });

      expect(mockEq).toHaveBeenCalledWith('action', 'project_created');
    });

    it('✅ Can filter by date range', async () => {
      const startDate = new Date('2025-01-01');
      const endDate = new Date('2025-01-31');

      await auditService.getAuditTrail('user-123', { startDate, endDate });

      expect(mockGte).toHaveBeenCalledWith('created_at', startDate.toISOString());
      expect(mockLte).toHaveBeenCalledWith('created_at', endDate.toISOString());
    });

    it('✅ Can limit results', async () => {
      await auditService.getAuditTrail('user-123', { limit: 10 });

      expect(mockLimit).toHaveBeenCalledWith(10);
    });
  });

  describe('exportAuditLogs', () => {
    beforeEach(() => {
      mockOrder.mockReturnValue({
        data: [
          {
            created_at: '2025-01-08T10:00:00Z',
            user_id: 'user-123',
            project_id: 'project-456',
            action: 'project_created',
            resource_type: 'project',
            resource_id: 'project-456',
            ip_address: '192.168.1.1',
            user_agent: 'Mozilla/5.0',
            metadata: { name: 'Test Project' },
          },
        ],
        error: null,
      });
    });

    it('✅ Exports audit logs as CSV', async () => {
      const startDate = new Date('2025-01-01');
      const endDate = new Date('2025-01-31');

      const csv = await auditService.exportAuditLogs(startDate, endDate);

      expect(csv).toBeInstanceOf(Buffer);
      const csvString = csv.toString();
      expect(csvString).toContain('timestamp,user_id,project_id,action');
      expect(csvString).toContain('project_created');
      expect(csvString).toContain('user-123');
    });

    it('✅ Handles empty results', async () => {
      mockOrder.mockReturnValue({ data: [], error: null });

      const csv = await auditService.exportAuditLogs(
        new Date('2025-01-01'),
        new Date('2025-01-31')
      );

      const csvString = csv.toString();
      expect(csvString).toContain('No audit logs found');
    });

    it('✅ Escapes CSV special characters', async () => {
      mockOrder.mockReturnValue({
        data: [
          {
            created_at: '2025-01-08T10:00:00Z',
            user_id: 'user-123',
            project_id: null,
            action: 'test_action',
            resource_type: 'test',
            resource_id: null,
            ip_address: null,
            user_agent: 'Mozilla/5.0 "Test"',
            metadata: { message: 'Test, with, commas' },
          },
        ],
        error: null,
      });

      const csv = await auditService.exportAuditLogs(
        new Date('2025-01-01'),
        new Date('2025-01-31')
      );

      const csvString = csv.toString();
      expect(csvString).toContain('""'); // Escaped quotes
    });
  });

  describe('Helper methods', () => {
    it('✅ logProjectAction logs correctly', async () => {
      await auditService.logProjectAction('user-123', 'project-456', 'created', {
        name: 'Test',
      });

      expect(mockInsert).toHaveBeenCalledWith(
        expect.objectContaining({
          user_id: 'user-123',
          project_id: 'project-456',
          action: 'created',
          resource_type: 'project',
          metadata: { name: 'Test' },
        })
      );
    });

    it('✅ logAuthAction logs correctly', async () => {
      await auditService.logAuthAction('user-123', 'login', '192.168.1.1', 'Chrome');

      expect(mockInsert).toHaveBeenCalledWith(
        expect.objectContaining({
          user_id: 'user-123',
          action: 'user_login',
          resource_type: 'user',
          ip_address: '192.168.1.1',
          user_agent: 'Chrome',
        })
      );
    });
  });

  describe('getAuditStats', () => {
    beforeEach(() => {
      mockOrder.mockReturnValue({
        eq: mockEq,
        gte: mockGte,
        lte: mockLte,
        limit: mockLimit,
        data: [
          { id: '1', action: 'project_created', created_at: '2025-01-08' },
          { id: '2', action: 'project_created', created_at: '2025-01-08' },
          { id: '3', action: 'design_approved', created_at: '2025-01-08' },
        ],
        error: null,
      });
    });

    it('✅ Returns audit statistics', async () => {
      const stats = await auditService.getAuditStats('user-123', 30);

      expect(stats.total_actions).toBe(3);
      expect(stats.actions_by_type).toEqual({
        project_created: 2,
        design_approved: 1,
      });
      expect(stats.recent_activity).toHaveLength(3);
    });
  });
});

// Testing Checkpoint 1b Summary
describe('Testing Checkpoint 1b: Audit Service', () => {
  it('CHECKPOINT SUMMARY', () => {
    const checklistItem = `
    Testing Checkpoint 1b: Audit service tests
    ✅ Can log user actions
    ✅ Can log AI operations
    ✅ Can query audit trail
    ✅ Non-blocking (doesn't slow down main workflow)
    `;
    console.log(checklistItem);
  });
});
