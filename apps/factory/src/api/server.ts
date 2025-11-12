/**
 * REST API Server
 *
 * Express-based API server that exposes the Design-First Software Factory services.
 *
 * Endpoints:
 * - POST /api/v1/workflows - Start a new workflow
 * - GET /api/v1/workflows/:id - Get workflow status
 * - POST /api/v1/workflows/:id/pause - Pause workflow
 * - POST /api/v1/workflows/:id/resume - Resume workflow
 * - GET /api/v1/projects - List user's projects
 * - GET /api/v1/projects/:id - Get project details
 * - GET /api/v1/projects/:id/progress - Get project progress
 * - GET /api/v1/usage - Get usage statistics
 * - GET /api/v1/health - Health check
 */

import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { createServer } from 'http';
import { Server as WebSocketServer } from 'ws';

import { WorkflowOrchestratorService, WorkflowInput } from '../services/workflow-orchestrator.service';
import { WorkflowStateMachineService } from '../services/workflow-state-machine.service';
import { ProgressTrackerService } from '../services/progress-tracker.service';
import { QuotaService } from '../services/quota.service';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

// Initialize services
const workflowOrchestrator = WorkflowOrchestratorService.getInstance();
const workflowStateMachine = WorkflowStateMachineService.getInstance();
const progressTracker = ProgressTrackerService.getInstance();
const quotaService = QuotaService.getInstance();

// Initialize Supabase
const supabaseUrl = process.env.SUPABASE_URL || '';
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || '';
const supabase = createClient(supabaseUrl, supabaseKey);

// Create Express app
const app = express();

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  credentials: true,
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
});
app.use('/api/', limiter);

// Request logging
app.use((req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
  });
  next();
});

// Authentication middleware (simplified for demo - replace with proper auth)
interface AuthRequest extends Request {
  userId?: string;
}

const authenticate = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
      return res.status(401).json({ error: 'No authorization header' });
    }

    const token = authHeader.replace('Bearer ', '');

    // Verify token with Supabase
    const { data: { user }, error } = await supabase.auth.getUser(token);

    if (error || !user) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    req.userId = user.id;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Authentication failed' });
  }
};

// ============================================================================
// WORKFLOW ENDPOINTS
// ============================================================================

/**
 * POST /api/v1/workflows
 * Start a new workflow
 */
app.post('/api/v1/workflows', authenticate, async (req: AuthRequest, res: Response) => {
  try {
    const input: WorkflowInput = {
      userId: req.userId!,
      projectName: req.body.projectName,
      projectDescription: req.body.projectDescription,
      targetPlatforms: req.body.targetPlatforms,
      designPreferences: req.body.designPreferences,
      metadata: req.body.metadata,
    };

    // Validate input
    if (!input.projectName || !input.projectDescription) {
      return res.status(400).json({
        error: 'Missing required fields: projectName, projectDescription',
      });
    }

    // Execute workflow in background
    workflowOrchestrator.executeWorkflow(input)
      .then((result) => {
        console.log(`Workflow ${result.projectId} completed with status: ${result.status}`);
      })
      .catch((error) => {
        console.error('Workflow execution error:', error);
      });

    // Return immediately with project ID
    const { data: project } = await supabase
      .from('projects')
      .select('id, name, status, created_at')
      .eq('user_id', req.userId)
      .order('created_at', { ascending: false })
      .limit(1)
      .single();

    res.status(202).json({
      message: 'Workflow started',
      project,
    });
  } catch (error: any) {
    console.error('Workflow start error:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/v1/workflows/:projectId
 * Get workflow status
 */
app.get('/api/v1/workflows/:projectId', authenticate, async (req: AuthRequest, res: Response) => {
  try {
    const { projectId } = req.params;

    // Verify user owns project
    const { data: project } = await supabase
      .from('projects')
      .select('*')
      .eq('id', projectId)
      .eq('user_id', req.userId)
      .single();

    if (!project) {
      return res.status(404).json({ error: 'Project not found' });
    }

    // Get workflow state
    const workflowState = await workflowStateMachine.getWorkflowState(projectId);

    if (!workflowState) {
      return res.status(404).json({ error: 'Workflow not found' });
    }

    // Get latest progress
    const latestProgress = await progressTracker.getLatestProgress(projectId);

    res.json({
      project,
      workflow: workflowState,
      latestProgress,
    });
  } catch (error: any) {
    console.error('Get workflow error:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/v1/workflows/:projectId/pause
 * Pause a workflow
 */
app.post('/api/v1/workflows/:projectId/pause', authenticate, async (req: AuthRequest, res: Response) => {
  try {
    const { projectId } = req.params;

    // Verify user owns project
    const { data: project } = await supabase
      .from('projects')
      .select('id')
      .eq('id', projectId)
      .eq('user_id', req.userId)
      .single();

    if (!project) {
      return res.status(404).json({ error: 'Project not found' });
    }

    const workflowState = await workflowStateMachine.pauseWorkflow(projectId);

    res.json({
      message: 'Workflow paused',
      workflow: workflowState,
    });
  } catch (error: any) {
    console.error('Pause workflow error:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/v1/workflows/:projectId/resume
 * Resume a paused workflow
 */
app.post('/api/v1/workflows/:projectId/resume', authenticate, async (req: AuthRequest, res: Response) => {
  try {
    const { projectId } = req.params;

    // Verify user owns project
    const { data: project } = await supabase
      .from('projects')
      .select('id')
      .eq('id', projectId)
      .eq('user_id', req.userId)
      .single();

    if (!project) {
      return res.status(404).json({ error: 'Project not found' });
    }

    const workflowState = await workflowStateMachine.resumeWorkflow(projectId);

    res.json({
      message: 'Workflow resumed',
      workflow: workflowState,
    });
  } catch (error: any) {
    console.error('Resume workflow error:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// PROJECT ENDPOINTS
// ============================================================================

/**
 * GET /api/v1/projects
 * List user's projects
 */
app.get('/api/v1/projects', authenticate, async (req: AuthRequest, res: Response) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
    const offset = (page - 1) * limit;

    const { data: projects, error, count } = await supabase
      .from('projects')
      .select('*', { count: 'exact' })
      .eq('user_id', req.userId)
      .order('created_at', { ascending: false })
      .range(offset, offset + limit - 1);

    if (error) {
      throw error;
    }

    res.json({
      projects,
      pagination: {
        page,
        limit,
        total: count || 0,
        totalPages: Math.ceil((count || 0) / limit),
      },
    });
  } catch (error: any) {
    console.error('List projects error:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/v1/projects/:id
 * Get project details
 */
app.get('/api/v1/projects/:id', authenticate, async (req: AuthRequest, res: Response) => {
  try {
    const { id } = req.params;

    const { data: project, error } = await supabase
      .from('projects')
      .select('*')
      .eq('id', id)
      .eq('user_id', req.userId)
      .single();

    if (error || !project) {
      return res.status(404).json({ error: 'Project not found' });
    }

    res.json({ project });
  } catch (error: any) {
    console.error('Get project error:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * GET /api/v1/projects/:id/progress
 * Get project progress
 */
app.get('/api/v1/projects/:id/progress', authenticate, async (req: AuthRequest, res: Response) => {
  try {
    const { id } = req.params;

    // Verify user owns project
    const { data: project } = await supabase
      .from('projects')
      .select('id')
      .eq('id', id)
      .eq('user_id', req.userId)
      .single();

    if (!project) {
      return res.status(404).json({ error: 'Project not found' });
    }

    const history = await progressTracker.getProgressHistory(id);
    const latestProgress = await progressTracker.getLatestProgress(id);
    const overallProgress = await progressTracker.calculateWorkflowProgress(id);

    res.json({
      history,
      latest: latestProgress,
      overallProgress,
    });
  } catch (error: any) {
    console.error('Get progress error:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// USAGE & QUOTA ENDPOINTS
// ============================================================================

/**
 * GET /api/v1/usage
 * Get usage statistics and quota
 */
app.get('/api/v1/usage', authenticate, async (req: AuthRequest, res: Response) => {
  try {
    const quotaStatus = await quotaService.getQuotaStatus(req.userId!);

    // Get current period usage
    const { data: usageData } = await supabase
      .from('usage_quotas')
      .select('*')
      .eq('user_id', req.userId)
      .single();

    res.json({
      quota: quotaStatus,
      usage: usageData,
    });
  } catch (error: any) {
    console.error('Get usage error:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// HEALTH & STATUS ENDPOINTS
// ============================================================================

/**
 * GET /api/v1/health
 * Health check endpoint
 */
app.get('/api/v1/health', async (req: Request, res: Response) => {
  try {
    // Check database connectivity
    const { error } = await supabase.from('projects').select('id').limit(1);

    if (error) {
      throw new Error('Database connection failed');
    }

    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: 'ok',
        api: 'ok',
      },
    });
  } catch (error: any) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * GET /api/v1/stats
 * System-wide statistics (admin only)
 */
app.get('/api/v1/stats', async (req: Request, res: Response) => {
  try {
    const { data: projectCount } = await supabase
      .from('projects')
      .select('*', { count: 'exact', head: true });

    const { data: workflowCount } = await supabase
      .from('workflow_states')
      .select('*', { count: 'exact', head: true });

    const { data: activeWorkflows } = await supabase
      .from('workflow_states')
      .select('*', { count: 'exact', head: true })
      .eq('status', 'active');

    res.json({
      projects: {
        total: projectCount || 0,
      },
      workflows: {
        total: workflowCount || 0,
        active: activeWorkflows || 0,
      },
      timestamp: new Date().toISOString(),
    });
  } catch (error: any) {
    console.error('Get stats error:', error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Global error handler
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Unhandled error:', error);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? error.message : undefined,
  });
});

// ============================================================================
// SERVER INITIALIZATION
// ============================================================================

const PORT = parseInt(process.env.PORT || '3000', 10);
const httpServer = createServer(app);

// WebSocket server for real-time progress updates
const wss = new WebSocketServer({ server: httpServer, path: '/ws' });

wss.on('connection', (ws, req) => {
  console.log('WebSocket client connected');

  // Extract project ID from query string
  const url = new URL(req.url || '', `http://${req.headers.host}`);
  const projectId = url.searchParams.get('projectId');

  if (!projectId) {
    ws.close(1008, 'Missing projectId parameter');
    return;
  }

  // Subscribe to progress updates
  const channel = progressTracker.subscribeRealtime(projectId, (event) => {
    ws.send(JSON.stringify(event));
  });

  ws.on('close', async () => {
    console.log('WebSocket client disconnected');
    // Unsubscribe from realtime updates
    await supabase.removeChannel(channel);
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });
});

// Start server
if (require.main === module) {
  httpServer.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 API Server running on http://0.0.0.0:${PORT}`);
    console.log(`📡 WebSocket server running on ws://0.0.0.0:${PORT}/ws`);
    console.log(`🏥 Health check: http://0.0.0.0:${PORT}/api/v1/health`);
  });
}

export { app, httpServer, wss };
