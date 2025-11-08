/**
 * Audit Service
 * Provides compliance-ready logging of all user actions and AI operations
 *
 * Features:
 * - Non-blocking async logging
 * - Structured audit trail
 * - Compliance export capabilities
 * - IP and user agent tracking
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';

export interface AuditLogData {
  userId?: string;
  projectId?: string;
  action: string;
  resourceType: string;
  resourceId?: string;
  metadata?: Record<string, any>;
  ipAddress?: string;
  userAgent?: string;
}

export interface AuditLog {
  id: string;
  user_id: string | null;
  project_id: string | null;
  action: string;
  resource_type: string;
  resource_id: string | null;
  ip_address: string | null;
  user_agent: string | null;
  metadata: Record<string, any>;
  created_at: string;
}

export interface AuditFilters {
  userId?: string;
  projectId?: string;
  action?: string;
  resourceType?: string;
  startDate?: Date;
  endDate?: Date;
  limit?: number;
}

/**
 * Audit Service for compliance logging
 */
export class AuditService {
  private client: SupabaseClient;

  constructor(supabaseUrl: string, supabaseKey: string) {
    this.client = createClient(supabaseUrl, supabaseKey);
  }

  /**
   * Log an audit event (non-blocking)
   * Errors are logged but don't throw to avoid disrupting main workflow
   */
  async log(data: AuditLogData): Promise<void> {
    try {
      const { error } = await this.client.from('audit_logs').insert({
        user_id: data.userId || null,
        project_id: data.projectId || null,
        action: data.action,
        resource_type: data.resourceType,
        resource_id: data.resourceId || null,
        ip_address: data.ipAddress || null,
        user_agent: data.userAgent || null,
        metadata: data.metadata || {},
      });

      if (error) {
        console.error('Audit log failed:', error);
        // Don't throw - logging should never break the main workflow
      }
    } catch (error) {
      console.error('Audit log exception:', error);
      // Swallow errors to ensure non-blocking behavior
    }
  }

  /**
   * Get audit trail with optional filters
   */
  async getAuditTrail(userId: string, filters?: AuditFilters): Promise<AuditLog[]> {
    let query = this.client
      .from('audit_logs')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    if (filters) {
      if (filters.projectId) {
        query = query.eq('project_id', filters.projectId);
      }
      if (filters.action) {
        query = query.eq('action', filters.action);
      }
      if (filters.resourceType) {
        query = query.eq('resource_type', filters.resourceType);
      }
      if (filters.startDate) {
        query = query.gte('created_at', filters.startDate.toISOString());
      }
      if (filters.endDate) {
        query = query.lte('created_at', filters.endDate.toISOString());
      }
      if (filters.limit) {
        query = query.limit(filters.limit);
      }
    }

    const { data, error } = await query;

    if (error) throw error;
    return data || [];
  }

  /**
   * Export audit logs for compliance (CSV format)
   * Useful for SOC2, ISO27001, GDPR compliance
   */
  async exportAuditLogs(startDate: Date, endDate: Date): Promise<Buffer> {
    const { data, error } = await this.client
      .from('audit_logs')
      .select('*')
      .gte('created_at', startDate.toISOString())
      .lte('created_at', endDate.toISOString())
      .order('created_at', { ascending: true });

    if (error) throw error;

    // Convert to CSV
    const logs = data || [];
    if (logs.length === 0) {
      return Buffer.from('No audit logs found for this period\n');
    }

    // CSV headers
    const headers = [
      'timestamp',
      'user_id',
      'project_id',
      'action',
      'resource_type',
      'resource_id',
      'ip_address',
      'user_agent',
      'metadata',
    ];

    // CSV rows
    const rows = logs.map((log) => [
      log.created_at,
      log.user_id || '',
      log.project_id || '',
      log.action,
      log.resource_type,
      log.resource_id || '',
      log.ip_address || '',
      log.user_agent || '',
      JSON.stringify(log.metadata || {}),
    ]);

    // Build CSV
    const csvLines = [
      headers.join(','),
      ...rows.map((row) =>
        row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(',')
      ),
    ];

    return Buffer.from(csvLines.join('\n'));
  }

  /**
   * Get audit statistics for a user
   */
  async getAuditStats(userId: string, days: number = 30): Promise<{
    total_actions: number;
    actions_by_type: Record<string, number>;
    recent_activity: AuditLog[];
  }> {
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    const logs = await this.getAuditTrail(userId, {
      startDate,
      limit: 1000,
    });

    // Count by action type
    const actionsByType: Record<string, number> = {};
    logs.forEach((log) => {
      actionsByType[log.action] = (actionsByType[log.action] || 0) + 1;
    });

    return {
      total_actions: logs.length,
      actions_by_type: actionsByType,
      recent_activity: logs.slice(0, 10),
    };
  }

  /**
   * Helper: Log project action
   */
  async logProjectAction(
    userId: string,
    projectId: string,
    action: string,
    metadata?: Record<string, any>
  ): Promise<void> {
    await this.log({
      userId,
      projectId,
      action,
      resourceType: 'project',
      resourceId: projectId,
      metadata,
    });
  }

  /**
   * Helper: Log AI generation action
   */
  async logAIGeneration(
    userId: string,
    projectId: string,
    stage: string,
    provider: string,
    metadata?: Record<string, any>
  ): Promise<void> {
    await this.log({
      userId,
      projectId,
      action: 'ai_generation',
      resourceType: 'ai_generation',
      metadata: {
        stage,
        provider,
        ...metadata,
      },
    });
  }

  /**
   * Helper: Log user authentication action
   */
  async logAuthAction(
    userId: string,
    action: 'login' | 'logout' | 'signup' | 'password_reset',
    ipAddress?: string,
    userAgent?: string
  ): Promise<void> {
    await this.log({
      userId,
      action: `user_${action}`,
      resourceType: 'user',
      resourceId: userId,
      ipAddress,
      userAgent,
    });
  }
}

/**
 * Singleton instance
 */
let auditServiceInstance: AuditService | null = null;

export function getAuditService(
  supabaseUrl?: string,
  supabaseKey?: string
): AuditService {
  if (!auditServiceInstance && (!supabaseUrl || !supabaseKey)) {
    throw new Error('Supabase config required to initialize AuditService');
  }

  if (supabaseUrl && supabaseKey && !auditServiceInstance) {
    auditServiceInstance = new AuditService(supabaseUrl, supabaseKey);
  }

  return auditServiceInstance!;
}
