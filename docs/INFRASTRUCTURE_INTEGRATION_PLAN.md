# Infrastructure Integration Plan: Zero to Scale

**Date:** 2025-11-07
**Purpose:** Integrate infrastructure from original Gemini plan + modern tech stack best practices
**Philosophy:** Start free/low-cost, preserve migration path to enterprise

---

## Executive Summary

This plan integrates the 10 critical infrastructure gaps identified in GEMINI_PLAN_COMPARISON.md with best practices from modern AI engineering (based on "The ONLY AI Tech Stack You Need in 2026").

**Three-Tier Approach:**
1. **Proof of Concept** ($0-20/month) - Validate workflow with free tiers
2. **MVP Launch** ($50-150/month) - Production-ready with generous free tiers
3. **Scale** ($500+/month) - Enterprise features when revenue justifies

**Core Principle:** Every technology choice has a free/cheap option for POC with a clear upgrade path.

---

## The 10 Critical Infrastructure Gaps

From GEMINI_PLAN_COMPARISON.md, these are MUST-HAVE for production:

1. ✅ Job Queue Architecture (long-running tasks)
2. ✅ Audit Logging (compliance, debugging)
3. ✅ AI Cost Tracking (actual token usage)
4. ✅ Usage Quotas (tier enforcement)
5. ✅ CI Enforcement (architecture compliance)
6. ✅ Multi-Layer Code Validation (security, quality)
7. ✅ Post-Handoff Checklist (user guidance)
8. ✅ Structured Iteration Limits (prevent infinite loops)
9. ✅ Error Recovery Strategies (resilience)
10. ✅ Background Job Progress (real-time updates)

---

## Technology Selection Matrix

### Core Infrastructure

| Category | Proof of Concept (FREE) | MVP ($) | Scale ($$) | Why This Path |
|----------|-------------------------|---------|-----------|---------------|
| **Database** | Supabase Free Tier (500MB) | Supabase Pro ($25/mo) | Supabase Team ($599/mo) or Neon Scale | Free tier perfect for POC, easy upgrade |
| **Caching** | Valkey (self-hosted, open source) | Redis Cloud Free (30MB) | Redis Cloud Paid ($7+/mo) | Valkey for POC, Redis Cloud for production |
| **Job Queue** | BullMQ + Valkey (open source) | Inngest Free (30K events/mo) | Inngest Pro ($25+/mo) | BullMQ for learning, Inngest for production ease |
| **Observability** | Langfuse (self-hosted, open source) | Langfuse Cloud Free (10K traces/mo) | Langfuse Cloud Pro ($49+/mo) | Open source wins, cloud when convenient |
| **Monitoring** | Sentry Free (5K errors/mo) | Sentry Team ($26/mo) | Sentry Business ($80+/mo) | Generous free tier, scales with usage |

### AI & Agent Infrastructure

| Category | Proof of Concept (FREE) | MVP ($) | Scale ($$) | Why This Path |
|----------|-------------------------|---------|-----------|---------------|
| **AI Framework** | Pydantic AI (open source) | Pydantic AI (open source) | Pydantic AI (open source) | Best balance of simplicity and power |
| **Multi-Agent** | LangGraph (open source) | LangGraph (open source) | LangGraph Cloud (when needed) | Industry standard, free to start |
| **Tool Auth** | Manual OAuth flow | Arcade ($99/mo when needed) | Arcade Enterprise | Not needed until user-specific tool access |
| **Cost Tracking** | Custom (track in DB) | Custom (track in DB) | LangSmith ($39+/mo) alternative | Build custom, upgrade if needed |

### Data & RAG (Future Features)

| Category | Proof of Concept (FREE) | MVP ($) | Scale ($$) | Why This Path |
|----------|-------------------------|---------|-----------|---------------|
| **Vector DB** | pgvector (in Supabase) | pgvector (in Supabase) | Pinecone/Qdrant ($70+/mo) | pgvector scales surprisingly well |
| **Document Parsing** | Docling (open source) | Docling (open source) | Docling (open source) | Free and excellent |
| **Web Scraping** | Crawl4AI (open source) | Crawl4AI (open source) | Firecrawl ($19+/mo) when needed | Start free, upgrade for reliability |
| **Long-term Memory** | Mem0 (open source) | Mem0 (open source) | Mem0 (open source) | Perfect open source solution |

### Full Stack & Deployment

| Category | Proof of Concept (FREE) | MVP ($) | Scale ($$) | Why This Path |
|----------|-------------------------|---------|-----------|---------------|
| **Backend API** | FastAPI (open source) | FastAPI (open source) | FastAPI (open source) | Free forever, just hosting costs |
| **Frontend** | React + Vite (open source) | React + Vite (open source) | React + Vite (open source) | Industry standard |
| **UI Components** | Shadcn + Tailwind (free) | Shadcn + Tailwind (free) | Shadcn + Tailwind (free) | Beautiful, free, customizable |
| **Prototyping UI** | Streamlit (open source) | Streamlit (open source) | Streamlit Cloud ($250/mo if needed) | Perfect for internal tools |
| **Auth (Simple)** | Supabase Auth (free tier) | Supabase Auth (included in Pro) | Supabase Auth + RLS | Built-in, battle-tested |
| **Auth (Enterprise)** | Not needed | Auth0 Free (7K users) | Auth0 Paid ($240+/mo) | Add only when enterprise customers demand |
| **Payments** | Stripe (2.9% + 30¢) | Stripe (2.9% + 30¢) | Stripe (negotiated rates) | Only costs when making money |
| **Deployment** | Render Free (static) | Render ($7+/mo) | Render or GCP | Render perfect for small scale |
| **Containerization** | Docker (open source) | Docker (open source) | Docker (open source) | Free, industry standard |
| **CI/CD** | GitHub Actions (free for public) | GitHub Actions (free for private) | GitHub Actions (generous) | Best integration, generous free tier |
| **Code Review** | CodeRabbit (free for OSS) | CodeRabbit ($12/user/mo) | CodeRabbit Team ($48/user/mo) | Worth it, catches real bugs |

### Testing & Quality

| Category | Proof of Concept (FREE) | MVP ($) | Scale ($$) | Why This Path |
|----------|-------------------------|---------|-----------|---------------|
| **Unit Tests** | Pytest/Jest (open source) | Pytest/Jest (open source) | Pytest/Jest (open source) | Free, industry standard |
| **E2E Tests** | Playwright (open source) | Playwright (open source) | Playwright (open source) | Best tool, completely free |
| **Security Scanning** | Semgrep (open source) | Semgrep (open source) | Semgrep Cloud ($39+/mo) | Open source CLI, cloud optional |
| **Dependency Audit** | npm audit (free) | Snyk Free (200 tests/mo) | Snyk Pro ($98+/mo) | Snyk when needed |
| **RAG Evaluation** | Ragas (open source) | Ragas (open source) | Ragas (open source) | Free, excellent for RAG |

---

## Three-Tier Deployment Strategy

### Tier 1: Proof of Concept (FREE - $20/month)

**Goal:** Validate workflow and core features with 10-20 test users

**Stack:**
- **Database:** Supabase Free (500MB, 50K users, 2GB bandwidth)
- **Caching:** Valkey (self-hosted on $5 Digital Ocean droplet)
- **Job Queue:** BullMQ + Valkey (open source, self-hosted)
- **Observability:** Langfuse (self-hosted with Supabase)
- **Backend:** FastAPI (self-hosted on same Digital Ocean droplet)
- **Frontend:** React + Vite (deployed on Render Free tier for static sites)
- **Monitoring:** Sentry Free (5K errors/month)
- **CI/CD:** GitHub Actions (free for public repo or limited private)
- **LLM Costs:** $10-15/month for light testing

**Total Cost:** $5-20/month (just the Digital Ocean droplet)

**What Works:**
- Complete workflow demonstration
- All 10 infrastructure features implemented
- Real user testing
- Learning what breaks

**Limitations:**
- Manual scaling needed
- Self-hosted reliability
- Limited to ~20 concurrent users
- No enterprise auth
- Basic monitoring

### Tier 2: MVP Launch ($50-150/month)

**Goal:** Serve 100-500 users, paying customers, reliable service

**Stack:**
- **Database:** Supabase Pro ($25/mo - 8GB, 100GB bandwidth)
- **Caching:** Redis Cloud Free or Paid ($7/mo for 250MB)
- **Job Queue:** Inngest Free (30K events/month) or Pro ($25/mo)
- **Observability:** Langfuse Cloud Free (10K traces/month)
- **Backend:** Render Standard ($7-25/mo depending on instances)
- **Frontend:** Render (free for static, $7 if dynamic)
- **Monitoring:** Sentry Free or Team ($26/mo)
- **Payments:** Stripe (free setup, 2.9% + 30¢ per transaction)
- **Code Review:** CodeRabbit ($12/user/month)
- **LLM Costs:** $50-100/month for real usage

**Total Cost:** $50-150/month + LLM costs + Stripe fees

**Upgrade Path:**
- Move from self-hosted to managed services
- Transition BullMQ to Inngest for reliability
- Add Sentry Team for better monitoring
- Keep everything else open source

**What Works:**
- Reliable uptime (Render SLA)
- Professional service level
- Paying customers
- Real revenue
- Manageable costs

**Limitations:**
- Still no enterprise features
- Limited customization of auth
- Manual customer support tools
- Basic analytics

### Tier 3: Scale ($500+/month)

**Goal:** 1,000+ users, enterprise customers, multi-region

**Stack:**
- **Database:** Supabase Team ($599/mo) or Neon Scale
- **Caching:** Redis Cloud Standard ($35+/mo)
- **Job Queue:** Inngest Pro ($25-100/mo)
- **Observability:** Langfuse Cloud Pro ($49+/mo) or self-hosted at scale
- **Backend:** Render Professional ($25-100/mo) or GCP Cloud Run
- **Frontend:** Render Professional or Vercel Pro ($20/user/mo)
- **Monitoring:** Sentry Business ($80-200/mo)
- **Auth:** Add Auth0 ($240+/mo) for enterprise customers
- **GPU Hosting:** RunPod ($0.34/hr for H100, ~$250/mo for 24/7)
- **Code Review:** CodeRabbit Team ($48/user/mo)
- **LLM Costs:** $500-2,000/month

**Total Cost:** $500-2,000/month + LLM usage

**Enterprise Features:**
- SSO/SAML (Auth0)
- SOC 2 compliance (audit logs ready)
- Multi-region deployment
- 99.9% uptime SLA
- Dedicated support
- Advanced analytics

---

## Phase-by-Phase Integration Plan

### Phase 1: Foundation (Week 1-2) - POC Tier

**Goal:** Get core infrastructure working with free/open source tools

#### Database Migrations

```bash
# Run these migrations in Supabase
cd supabase/migrations

# Create 002_infrastructure.sql
```

```sql
-- Job Queue Table
CREATE TABLE code_generation_jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id),
  status TEXT CHECK (status IN ('queued', 'processing', 'completed', 'failed')) DEFAULT 'queued',
  progress_pct INTEGER DEFAULT 0 CHECK (progress_pct >= 0 AND progress_pct <= 100),
  current_step TEXT,
  estimated_time_remaining INTEGER, -- seconds
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit Logging
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  project_id UUID REFERENCES projects(id),
  action TEXT NOT NULL,
  resource_type TEXT, -- 'project', 'design', 'code', etc.
  resource_id UUID,
  metadata JSONB,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Cost Tracking
CREATE TABLE ai_generations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id),
  user_id UUID REFERENCES auth.users(id),
  service TEXT CHECK (service IN ('gemini', 'codex', 'claude', 'anthropic')) NOT NULL,
  model_version TEXT NOT NULL,
  operation TEXT NOT NULL, -- 'prd_generation', 'design', 'code_validation', etc.
  prompt_tokens INTEGER NOT NULL,
  completion_tokens INTEGER NOT NULL,
  cost_usd NUMERIC(10,6) NOT NULL,
  latency_ms INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Usage Quotas
CREATE TABLE usage_quotas (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id),
  tier TEXT CHECK (tier IN ('free', 'pro', 'enterprise')) DEFAULT 'free',

  -- Monthly limits
  projects_used_this_month INTEGER DEFAULT 0,
  projects_limit INTEGER DEFAULT 3,
  monthly_spend_usd NUMERIC(10,2) DEFAULT 0.00,
  monthly_spend_limit NUMERIC(10,2) DEFAULT 5.00,

  -- Period tracking (auto-reset monthly)
  period_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  period_end TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '1 month'),

  -- Metadata
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Iteration Tracking
CREATE TABLE iteration_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  phase TEXT CHECK (phase IN ('prd', 'design', 'code')) NOT NULL,
  iteration_number INTEGER NOT NULL,
  feedback JSONB,
  approved BOOLEAN,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for Performance
CREATE INDEX idx_jobs_user_status ON code_generation_jobs(user_id, status);
CREATE INDEX idx_jobs_status_created ON code_generation_jobs(status, created_at);
CREATE INDEX idx_audit_user_created ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_project ON audit_logs(project_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_ai_gen_project ON ai_generations(project_id);
CREATE INDEX idx_ai_gen_user_created ON ai_generations(user_id, created_at DESC);
CREATE INDEX idx_ai_gen_service ON ai_generations(service);
CREATE INDEX idx_iterations_project_phase ON iteration_history(project_id, phase);

-- RLS Policies (Row Level Security)
ALTER TABLE code_generation_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_generations ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_quotas ENABLE ROW LEVEL SECURITY;
ALTER TABLE iteration_history ENABLE ROW LEVEL SECURITY;

-- Users can see their own data
CREATE POLICY "Users can view own jobs" ON code_generation_jobs
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own audit logs" ON audit_logs
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own AI costs" ON ai_generations
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own quota" ON usage_quotas
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own iterations" ON iteration_history
  FOR SELECT USING (
    project_id IN (SELECT id FROM projects WHERE user_id = auth.uid())
  );

-- Service role can do everything (for backend operations)
CREATE POLICY "Service role full access jobs" ON code_generation_jobs
  FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role full access audit" ON audit_logs
  FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role full access ai_gen" ON ai_generations
  FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role full access quotas" ON usage_quotas
  FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

CREATE POLICY "Service role full access iterations" ON iteration_history
  FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');
```

#### Service Implementation

**Step 1: Job Queue Service** (BullMQ for POC)

```bash
cd src/services
touch job-queue.service.ts
```

```typescript
// src/services/job-queue.service.ts
import { Queue, Worker, Job } from 'bullmq';
import IORedis from 'ioredis';

const connection = new IORedis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  maxRetriesPerRequest: null,
});

// Job types
interface CodeGenerationJobData {
  projectId: string;
  userId: string;
  approvedDesigns: any[];
  designSystem: any;
}

interface JobProgress {
  progress: number; // 0-100
  currentStep: string;
  estimatedTimeRemaining?: number;
}

// Create queue
export const codeGenerationQueue = new Queue<CodeGenerationJobData>('code-generation', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: {
      age: 24 * 3600, // Keep completed jobs for 24 hours
      count: 100,
    },
    removeOnFail: {
      age: 7 * 24 * 3600, // Keep failed jobs for 7 days
    },
  },
});

// Worker
export const createCodeGenerationWorker = (
  processFn: (job: Job<CodeGenerationJobData>) => Promise<void>
) => {
  return new Worker<CodeGenerationJobData>('code-generation', processFn, {
    connection,
    concurrency: 5, // Process 5 jobs concurrently
  });
};

// Helper to add job
export async function enqueueCodeGeneration(
  data: CodeGenerationJobData
): Promise<string> {
  const job = await codeGenerationQueue.add('generate-code', data, {
    jobId: `code-gen-${data.projectId}`,
  });

  return job.id!;
}

// Helper to update progress
export async function updateJobProgress(
  jobId: string,
  progress: JobProgress
): Promise<void> {
  const job = await Job.fromId(codeGenerationQueue, jobId);

  if (job) {
    await job.updateProgress(progress);

    // Also update database for persistence
    const { getSupabaseService } = await import('./supabase.service');
    const supabase = getSupabaseService({ /* config */ });

    await supabase.from('code_generation_jobs').update({
      progress_pct: progress.progress,
      current_step: progress.currentStep,
      estimated_time_remaining: progress.estimatedTimeRemaining,
    }).eq('id', jobId);
  }
}

// Helper to get job status
export async function getJobStatus(jobId: string) {
  const job = await Job.fromId(codeGenerationQueue, jobId);

  if (!job) {
    return { status: 'not_found' };
  }

  const state = await job.getState();
  const progress = job.progress as JobProgress | undefined;

  return {
    status: state,
    progress: progress?.progress || 0,
    currentStep: progress?.currentStep,
    estimatedTimeRemaining: progress?.estimatedTimeRemaining,
  };
}
```

**Step 2: Audit Service**

```typescript
// src/services/audit.service.ts
import { getSupabaseService } from './supabase.service';

interface AuditLogData {
  userId?: string;
  projectId?: string;
  action: string;
  resourceType?: string;
  resourceId?: string;
  metadata?: Record<string, any>;
  ipAddress?: string;
  userAgent?: string;
}

export class AuditService {
  private supabase: any;

  constructor(supabaseConfig: any) {
    this.supabase = getSupabaseService(supabaseConfig);
  }

  async log(data: AuditLogData): Promise<void> {
    try {
      await this.supabase.from('audit_logs').insert({
        user_id: data.userId,
        project_id: data.projectId,
        action: data.action,
        resource_type: data.resourceType,
        resource_id: data.resourceId,
        metadata: data.metadata,
        ip_address: data.ipAddress,
        user_agent: data.userAgent,
      });
    } catch (error) {
      // Audit logging should never break the app
      console.error('Failed to write audit log:', error);
    }
  }

  // Convenience methods
  async logProjectCreated(userId: string, projectId: string, metadata?: any) {
    await this.log({
      userId,
      projectId,
      action: 'project.created',
      resourceType: 'project',
      resourceId: projectId,
      metadata,
    });
  }

  async logDesignApproved(userId: string, projectId: string, designId: string) {
    await this.log({
      userId,
      projectId,
      action: 'design.approved',
      resourceType: 'design',
      resourceId: designId,
    });
  }

  async logCodeGenerated(userId: string, projectId: string, metadata?: any) {
    await this.log({
      userId,
      projectId,
      action: 'code.generated',
      resourceType: 'project',
      resourceId: projectId,
      metadata,
    });
  }

  async logAIGeneration(
    projectId: string,
    userId: string,
    service: string,
    modelVersion: string,
    operation: string,
    promptTokens: number,
    completionTokens: number,
    costUsd: number,
    latencyMs?: number
  ): Promise<void> {
    try {
      await this.supabase.from('ai_generations').insert({
        project_id: projectId,
        user_id: userId,
        service,
        model_version: modelVersion,
        operation,
        prompt_tokens: promptTokens,
        completion_tokens: completionTokens,
        cost_usd: costUsd,
        latency_ms: latencyMs,
      });

      // Also update user's monthly spend
      await this.supabase.rpc('increment_monthly_spend', {
        p_user_id: userId,
        p_amount: costUsd,
      });
    } catch (error) {
      console.error('Failed to log AI generation:', error);
    }
  }

  // Query methods
  async getProjectAuditLog(projectId: string, limit: number = 100) {
    const { data, error } = await this.supabase
      .from('audit_logs')
      .select('*')
      .eq('project_id', projectId)
      .order('created_at', { ascending: false })
      .limit(limit);

    if (error) throw error;
    return data;
  }

  async getUserAuditLog(userId: string, limit: number = 100) {
    const { data, error } = await this.supabase
      .from('audit_logs')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(limit);

    if (error) throw error;
    return data;
  }

  async getProjectCost(projectId: string): Promise<number> {
    const { data, error } = await this.supabase
      .from('ai_generations')
      .select('cost_usd')
      .eq('project_id', projectId);

    if (error) throw error;

    return data.reduce((sum, item) => sum + parseFloat(item.cost_usd), 0);
  }

  async getUserMonthlyCost(userId: string): Promise<number> {
    const { data, error } = await this.supabase
      .from('usage_quotas')
      .select('monthly_spend_usd')
      .eq('user_id', userId)
      .single();

    if (error) throw error;

    return parseFloat(data.monthly_spend_usd);
  }
}

// Supabase function for atomic increment
// Create this in Supabase SQL editor:
/*
CREATE OR REPLACE FUNCTION increment_monthly_spend(
  p_user_id UUID,
  p_amount NUMERIC
)
RETURNS VOID AS $$
BEGIN
  INSERT INTO usage_quotas (user_id, monthly_spend_usd, projects_used_this_month)
  VALUES (p_user_id, p_amount, 0)
  ON CONFLICT (user_id)
  DO UPDATE SET
    monthly_spend_usd = usage_quotas.monthly_spend_usd + p_amount,
    updated_at = NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
*/
```

**Step 3: Quota Service**

```typescript
// src/services/quota.service.ts
import { getSupabaseService } from './supabase.service';

export interface QuotaCheckResult {
  allowed: boolean;
  reason?: 'monthly_project_limit' | 'monthly_spend_limit' | 'tier_restriction';
  current: {
    projectsUsed: number;
    projectsLimit: number;
    monthlySpend: number;
    monthlySpendLimit: number;
  };
  upgradeRequired: boolean;
  nextTier?: 'pro' | 'enterprise';
}

const TIER_LIMITS = {
  free: {
    projectsPerMonth: 3,
    monthlySpendLimit: 5.00,
    features: ['express'],
  },
  pro: {
    projectsPerMonth: 50,
    monthlySpendLimit: 100.00,
    features: ['express', 'concierge', 'priority_support'],
  },
  enterprise: {
    projectsPerMonth: Infinity,
    monthlySpendLimit: Infinity,
    features: ['all'],
  },
};

export class QuotaService {
  private supabase: any;

  constructor(supabaseConfig: any) {
    this.supabase = getSupabaseService(supabaseConfig);
  }

  async checkQuota(userId: string): Promise<QuotaCheckResult> {
    // Get or create quota record
    let { data: quota, error } = await this.supabase
      .from('usage_quotas')
      .select('*')
      .eq('user_id', userId)
      .single();

    if (error && error.code === 'PGRST116') {
      // No quota record, create one
      const { data: newQuota, error: insertError } = await this.supabase
        .from('usage_quotas')
        .insert({
          user_id: userId,
          tier: 'free',
        })
        .select()
        .single();

      if (insertError) throw insertError;
      quota = newQuota;
    } else if (error) {
      throw error;
    }

    // Check if period has expired (monthly reset)
    const now = new Date();
    const periodEnd = new Date(quota.period_end);

    if (now > periodEnd) {
      // Reset monthly counters
      const { data: resetQuota } = await this.supabase
        .from('usage_quotas')
        .update({
          projects_used_this_month: 0,
          monthly_spend_usd: 0,
          period_start: now,
          period_end: new Date(now.setMonth(now.getMonth() + 1)),
        })
        .eq('user_id', userId)
        .select()
        .single();

      quota = resetQuota;
    }

    // Check limits
    const limits = TIER_LIMITS[quota.tier as keyof typeof TIER_LIMITS];

    if (quota.projects_used_this_month >= limits.projectsPerMonth) {
      return {
        allowed: false,
        reason: 'monthly_project_limit',
        current: {
          projectsUsed: quota.projects_used_this_month,
          projectsLimit: limits.projectsPerMonth,
          monthlySpend: parseFloat(quota.monthly_spend_usd),
          monthlySpendLimit: limits.monthlySpendLimit,
        },
        upgradeRequired: true,
        nextTier: quota.tier === 'free' ? 'pro' : 'enterprise',
      };
    }

    if (parseFloat(quota.monthly_spend_usd) >= limits.monthlySpendLimit) {
      return {
        allowed: false,
        reason: 'monthly_spend_limit',
        current: {
          projectsUsed: quota.projects_used_this_month,
          projectsLimit: limits.projectsPerMonth,
          monthlySpend: parseFloat(quota.monthly_spend_usd),
          monthlySpendLimit: limits.monthlySpendLimit,
        },
        upgradeRequired: true,
        nextTier: quota.tier === 'free' ? 'pro' : 'enterprise',
      };
    }

    return {
      allowed: true,
      current: {
        projectsUsed: quota.projects_used_this_month,
        projectsLimit: limits.projectsPerMonth,
        monthlySpend: parseFloat(quota.monthly_spend_usd),
        monthlySpendLimit: limits.monthlySpendLimit,
      },
      upgradeRequired: false,
    };
  }

  async incrementProjectCount(userId: string): Promise<void> {
    await this.supabase.rpc('increment_project_count', {
      p_user_id: userId,
    });
  }

  async getUserQuota(userId: string) {
    const { data, error } = await this.supabase
      .from('usage_quotas')
      .select('*')
      .eq('user_id', userId)
      .single();

    if (error) throw error;
    return data;
  }

  async upgradeTier(userId: string, newTier: 'pro' | 'enterprise', stripeSubscriptionId?: string): Promise<void> {
    const limits = TIER_LIMITS[newTier];

    await this.supabase
      .from('usage_quotas')
      .update({
        tier: newTier,
        projects_limit: limits.projectsPerMonth,
        monthly_spend_limit: limits.monthlySpendLimit,
        stripe_subscription_id: stripeSubscriptionId,
      })
      .eq('user_id', userId);
  }
}

// Add this SQL function to Supabase:
/*
CREATE OR REPLACE FUNCTION increment_project_count(p_user_id UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE usage_quotas
  SET projects_used_this_month = projects_used_this_month + 1,
      updated_at = NOW()
  WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
*/
```

#### Update master-workflow.service.ts

Add job queue integration:

```typescript
// src/services/master-workflow.service.ts (additions)
import { enqueueCodeGeneration, updateJobProgress } from './job-queue.service';
import { AuditService } from './audit.service';
import { QuotaService } from './quota.service';

export class MasterWorkflowService {
  private audit: AuditService;
  private quota: QuotaService;

  constructor(config: MasterWorkflowConfig) {
    // ... existing constructor
    this.audit = new AuditService(config.supabaseConfig);
    this.quota = new QuotaService(config.supabaseConfig);
  }

  async executeWorkflow(
    conversationHistory: ConversationMessage[],
    serviceTier: 'express' | 'concierge',
    userId: string,
    existingWebsiteUrl?: string
  ): Promise<WorkflowResult> {
    // Check quota BEFORE starting
    const quotaCheck = await this.quota.checkQuota(userId);

    if (!quotaCheck.allowed) {
      throw new Error(`Quota exceeded: ${quotaCheck.reason}. Please upgrade to ${quotaCheck.nextTier}.`);
    }

    // Audit: Project started
    const projectId = /* generate or get project id */;
    await this.audit.logProjectCreated(userId, projectId, {
      serviceTier,
      existingWebsiteUrl,
    });

    // For long-running operations, use job queue
    if (serviceTier === 'express') {
      // Enqueue job instead of running synchronously
      const jobId = await enqueueCodeGeneration({
        projectId,
        userId,
        approvedDesigns: [], // Will be populated by worker
        designSystem: {}, // Will be populated by worker
      });

      return {
        project_id: projectId,
        status: 'queued',
        job_id: jobId,
        // ... other fields
      };
    }

    // Rest of implementation...
  }
}
```

### Phase 2: Quality & Monitoring (Week 3) - POC Tier

**Goal:** Add multi-layer validation and basic monitoring

#### Add Langfuse for Observability

```bash
npm install langfuse
```

```typescript
// src/services/langfuse.service.ts
import { Langfuse } from 'langfuse';

const langfuse = new Langfuse({
  publicKey: process.env.LANGFUSE_PUBLIC_KEY,
  secretKey: process.env.LANGFUSE_SECRET_KEY,
  baseUrl: process.env.LANGFUSE_BASE_URL || 'https://cloud.langfuse.com', // or self-hosted
});

export function createTrace(name: string, userId?: string, metadata?: any) {
  return langfuse.trace({
    name,
    userId,
    metadata,
  });
}

export async function wrapAICall<T>(
  traceName: string,
  operation: string,
  fn: () => Promise<T>,
  metadata?: any
): Promise<T> {
  const trace = createTrace(traceName, metadata?.userId);

  const span = trace.span({
    name: operation,
    metadata,
  });

  const startTime = Date.now();

  try {
    const result = await fn();

    const latency = Date.now() - startTime;

    span.end({
      output: typeof result === 'string' ? result.substring(0, 1000) : result,
      metadata: {
        ...metadata,
        latency_ms: latency,
      },
    });

    // Also log to audit service if this is an AI generation
    // ... audit logging

    return result;
  } catch (error) {
    span.end({
      level: 'ERROR',
      statusMessage: error.message,
    });

    throw error;
  }
}

// Usage example:
/*
const result = await wrapAICall(
  'code-generation',
  'generate-screen',
  async () => {
    return await codex.generateScreen(screenMapping);
  },
  {
    userId: 'user-123',
    projectId: 'proj-456',
    screenName: 'HomeScreen',
  }
);
*/
```

#### Add Multi-Layer Code Validation

```typescript
// src/services/code-validation.service.ts
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface ValidationResult {
  passed: boolean;
  layer: string;
  issues: Array<{
    severity: 'error' | 'warning' | 'info';
    message: string;
    file?: string;
    line?: number;
  }>;
}

interface CodeQualityGate {
  static_analysis: {
    eslint: ValidationResult;
    typescript: ValidationResult;
  };
  security: {
    semgrep: ValidationResult;
    npm_audit: ValidationResult;
  };
  bundle_analysis?: {
    size_mb: number;
    threshold_mb: number;
    passed: boolean;
  };
  ai_validation?: {
    score: number;
    passed: boolean;
  };
  overall_status: 'passed' | 'failed' | 'warnings';
}

export class CodeValidationService {
  async validateGeneratedCode(projectPath: string): Promise<CodeQualityGate> {
    const results: Partial<CodeQualityGate> = {
      static_analysis: {
        eslint: await this.runESLint(projectPath),
        typescript: await this.runTypeScriptCheck(projectPath),
      },
      security: {
        semgrep: await this.runSemgrep(projectPath),
        npm_audit: await this.runNpmAudit(projectPath),
      },
    };

    // Determine overall status
    const hasErrors = [
      results.static_analysis.eslint,
      results.static_analysis.typescript,
      results.security.semgrep,
      results.security.npm_audit,
    ].some((r) => !r.passed && r.issues.some((i) => i.severity === 'error'));

    const hasWarnings = [
      results.static_analysis.eslint,
      results.static_analysis.typescript,
      results.security.semgrep,
      results.security.npm_audit,
    ].some((r) => r.issues.some((i) => i.severity === 'warning'));

    results.overall_status = hasErrors ? 'failed' : hasWarnings ? 'warnings' : 'passed';

    return results as CodeQualityGate;
  }

  private async runESLint(projectPath: string): Promise<ValidationResult> {
    try {
      const { stdout } = await execAsync(`cd ${projectPath} && npx eslint . --format json`);
      const results = JSON.parse(stdout);

      const issues = results.flatMap((file: any) =>
        file.messages.map((msg: any) => ({
          severity: msg.severity === 2 ? 'error' : 'warning',
          message: msg.message,
          file: file.filePath,
          line: msg.line,
        }))
      );

      return {
        passed: issues.filter((i) => i.severity === 'error').length === 0,
        layer: 'eslint',
        issues,
      };
    } catch (error) {
      return {
        passed: false,
        layer: 'eslint',
        issues: [{ severity: 'error', message: `ESLint failed: ${error.message}` }],
      };
    }
  }

  private async runTypeScriptCheck(projectPath: string): Promise<ValidationResult> {
    try {
      await execAsync(`cd ${projectPath} && npx tsc --noEmit`);

      return {
        passed: true,
        layer: 'typescript',
        issues: [],
      };
    } catch (error) {
      // Parse TypeScript errors
      const issues = error.stdout
        .split('\n')
        .filter((line) => line.includes('error TS'))
        .map((line) => ({
          severity: 'error' as const,
          message: line,
        }));

      return {
        passed: false,
        layer: 'typescript',
        issues,
      };
    }
  }

  private async runSemgrep(projectPath: string): Promise<ValidationResult> {
    try {
      const { stdout } = await execAsync(
        `cd ${projectPath} && semgrep --config auto --json .`
      );

      const results = JSON.parse(stdout);

      const issues = results.results.map((finding: any) => ({
        severity: finding.extra.severity === 'ERROR' ? 'error' : 'warning',
        message: finding.extra.message,
        file: finding.path,
        line: finding.start.line,
      }));

      return {
        passed: issues.filter((i) => i.severity === 'error').length === 0,
        layer: 'semgrep',
        issues,
      };
    } catch (error) {
      // Semgrep not installed or failed
      return {
        passed: true,
        layer: 'semgrep',
        issues: [{ severity: 'info', message: 'Semgrep not available, skipping security scan' }],
      };
    }
  }

  private async runNpmAudit(projectPath: string): Promise<ValidationResult> {
    try {
      const { stdout } = await execAsync(`cd ${projectPath} && npm audit --json`);
      const results = JSON.parse(stdout);

      const issues = Object.values(results.vulnerabilities || {}).map((vuln: any) => ({
        severity: vuln.severity === 'critical' || vuln.severity === 'high' ? 'error' : 'warning',
        message: `${vuln.name}: ${vuln.via[0]?.title || 'Vulnerability found'}`,
      }));

      return {
        passed: issues.filter((i) => i.severity === 'error').length === 0,
        layer: 'npm_audit',
        issues,
      };
    } catch (error) {
      return {
        passed: false,
        layer: 'npm_audit',
        issues: [{ severity: 'error', message: `npm audit failed: ${error.message}` }],
      };
    }
  }
}
```

#### Add Sentry for Error Tracking

```bash
npm install @sentry/node @sentry/react
```

```typescript
// src/services/sentry.service.ts
import * as Sentry from '@sentry/node';

export function initializeSentry() {
  if (process.env.SENTRY_DSN) {
    Sentry.init({
      dsn: process.env.SENTRY_DSN,
      environment: process.env.NODE_ENV || 'development',
      tracesSampleRate: 1.0, // Adjust in production
    });
  }
}

export function captureException(error: Error, context?: Record<string, any>) {
  Sentry.captureException(error, {
    extra: context,
  });
}

export function captureMessage(message: string, level: 'info' | 'warning' | 'error' = 'info') {
  Sentry.captureMessage(message, level);
}
```

### Phase 3: Frontend & CI/CD (Week 4) - MVP Transition

**Goal:** Professional deployment with CI/CD and monitoring

#### GitHub Actions Workflow

```yaml
# .github/workflows/test-and-deploy.yml
name: Test and Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run TypeScript check
        run: npm run type-check

      - name: Run unit tests
        run: npm test

      - name: Run Semgrep security scan
        uses: returntocorp/semgrep-action@v1
        with:
          config: auto

      - name: Run npm audit
        run: npm audit --audit-level=high

  build:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

#### Architecture Compliance Checks

```json
// .eslintrc.js (additions)
{
  "rules": {
    "no-restricted-imports": [
      "error",
      {
        "patterns": [
          {
            "group": ["react-native-*"],
            "message": "Use Expo modules instead of react-native- packages"
          }
        ]
      }
    ],
    "no-color-literals": "error" // Custom rule to enforce design tokens
  }
}
```

Custom ESLint rule:

```javascript
// .eslintrc-custom/no-color-literals.js
module.exports = {
  meta: {
    type: 'problem',
    docs: {
      description: 'Disallow hardcoded color values outside theme directory',
      category: 'Best Practices',
    },
  },
  create(context) {
    const colorPattern = /#[0-9a-fA-F]{3,6}|rgb\(|rgba\(/;
    const filename = context.getFilename();
    const isThemeFile = filename.includes('theme/') || filename.includes('tokens.');

    if (isThemeFile) {
      return {}; // Allow colors in theme files
    }

    return {
      Literal(node) {
        if (typeof node.value === 'string' && colorPattern.test(node.value)) {
          context.report({
            node,
            message: 'Use design tokens from theme instead of hardcoded colors',
          });
        }
      },
    };
  },
};
```

### Phase 4: Error Recovery & Iteration Limits (Week 5) - MVP Ready

Add error recovery to master workflow:

```typescript
// src/services/error-recovery.service.ts
interface RetryOptions {
  maxAttempts: number;
  baseDelay: number;
  maxDelay: number;
}

export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {
    maxAttempts: 3,
    baseDelay: 1000,
    maxDelay: 10000,
  }
): Promise<T> {
  let attempt = 0;
  let lastError: Error;

  while (attempt < options.maxAttempts) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      attempt++;

      if (attempt >= options.maxAttempts) {
        throw lastError;
      }

      const delay = Math.min(
        options.baseDelay * Math.pow(2, attempt - 1),
        options.maxDelay
      );

      console.log(`Attempt ${attempt} failed. Retrying in ${delay}ms...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}
```

Add iteration limits:

```typescript
// src/services/iteration.service.ts
const ITERATION_LIMITS = {
  express: { design: 0, code: 3 },
  concierge: { prd: 3, design: 5, code: 3 },
  premium: { prd: 5, design: 10, code: 5 },
};

export class IterationService {
  private supabase: any;

  constructor(supabaseConfig: any) {
    this.supabase = getSupabaseService(supabaseConfig);
  }

  async checkIterationLimit(
    projectId: string,
    phase: 'prd' | 'design' | 'code',
    tier: 'express' | 'concierge' | 'premium'
  ): Promise<{ allowed: boolean; current: number; limit: number }> {
    const { count } = await this.supabase
      .from('iteration_history')
      .select('*', { count: 'exact', head: true })
      .eq('project_id', projectId)
      .eq('phase', phase);

    const limit = ITERATION_LIMITS[tier][phase];

    return {
      allowed: count < limit,
      current: count,
      limit,
    };
  }

  async recordIteration(
    projectId: string,
    phase: 'prd' | 'design' | 'code',
    feedback: any,
    approved: boolean
  ): Promise<void> {
    const { count } = await this.supabase
      .from('iteration_history')
      .select('*', { count: 'exact', head: true })
      .eq('project_id', projectId)
      .eq('phase', phase);

    await this.supabase.from('iteration_history').insert({
      project_id: projectId,
      phase,
      iteration_number: count + 1,
      feedback,
      approved,
    });
  }
}
```

### Phase 5: Deployment to Render (Week 6) - Launch

Create `render.yaml` for infrastructure as code:

```yaml
# render.yaml
services:
  # Backend API
  - type: web
    name: design-factory-api
    env: node
    region: oregon
    plan: starter # $7/month
    buildCommand: npm install && npm run build
    startCommand: npm run start
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        sync: false # Set in Render dashboard
      - key: REDIS_URL
        sync: false
      - key: GEMINI_API_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
      - key: SENTRY_DSN
        sync: false
      - key: LANGFUSE_PUBLIC_KEY
        sync: false
      - key: LANGFUSE_SECRET_KEY
        sync: false

  # Frontend
  - type: web
    name: design-factory-frontend
    env: static
    region: oregon
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html

  # Background Worker
  - type: worker
    name: design-factory-worker
    env: node
    region: oregon
    plan: starter
    buildCommand: npm install && npm run build
    startCommand: npm run worker
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        sync: false
      - key: REDIS_URL
        sync: false
```

---

## Migration Paths

### When to Upgrade: Proof of Concept → MVP

**Trigger Points:**
- 20+ active users
- More than 10 projects/week
- Self-hosted infrastructure unreliable
- Need better support/SLA

**Migration Steps:**
1. **Day 1:** Upgrade Supabase Free → Pro ($25/mo)
2. **Day 1:** Deploy to Render ($7/mo for backend, free for frontend)
3. **Day 2:** Switch from Valkey to Redis Cloud Free tier
4. **Day 2:** Move BullMQ to Inngest Free tier (30K events/mo)
5. **Day 3:** Add Sentry Free tier for error tracking
6. **Day 3:** Switch Langfuse to cloud free tier (easier than self-hosted)
7. **Day 4-5:** Add CI/CD with GitHub Actions
8. **Day 6-7:** Add CodeRabbit for code review ($12/user/mo)

**Total Time:** 1 week
**New Monthly Cost:** $50-70/month (up from $5-20)
**Benefits:**
- 99.9% uptime SLA
- Managed infrastructure
- Better monitoring
- Professional deployment
- Code review automation

### When to Upgrade: MVP → Scale

**Trigger Points:**
- 500+ active users
- $5K+ monthly revenue
- Enterprise customer prospects
- Need SSO/SAML
- Multi-region requirements

**Migration Steps:**
1. **Week 1:** Upgrade Supabase Pro → Team ($599/mo)
2. **Week 1:** Add Auth0 Essentials ($240/mo) for enterprise auth
3. **Week 2:** Upgrade Render to Professional ($25-100/mo)
4. **Week 2:** Upgrade Redis Cloud to Standard ($35+/mo)
5. **Week 3:** Upgrade Inngest to Pro ($25-100/mo)
6. **Week 3:** Upgrade Sentry to Business ($80+/mo)
7. **Week 4:** Upgrade Langfuse to Pro ($49+/mo)
8. **Week 4:** Consider GCP for multi-region if needed

**Total Time:** 1 month
**New Monthly Cost:** $500-2,000/month (up from $50-150)
**Benefits:**
- Enterprise features (SSO, SAML)
- Better SLA (99.95%+)
- Multi-region support
- Dedicated support
- Advanced analytics
- SOC 2 ready

---

## Cost Projections

### Proof of Concept (FREE - $20/month)

```
Digital Ocean Droplet (1 CPU, 1GB RAM): $6/month
Gemini API (100 requests/day): $3/month
GPT-4o API (light testing): $10/month
Domain name: $12/year = $1/month
────────────────────────────────────────
TOTAL: ~$20/month

Can serve: 10-20 test users
Projects: 30-50/month total
Uptime: 95%+ (good enough for testing)
```

### MVP Launch ($50-150/month)

```
Supabase Pro: $25/month
Render Backend: $7/month
Redis Cloud: Free (or $7/mo for more space)
Inngest: Free (or $25/mo for more events)
CodeRabbit: $12/month
Sentry: Free (or $26/mo)
Langfuse: Free cloud tier
Gemini API: $20/month
GPT-4o API: $50/month
Domain + SSL: $1/month
────────────────────────────────────────
TOTAL: $50-150/month + $70/month LLM usage

Can serve: 100-500 users
Projects: 200-500/month
Uptime: 99.9%
```

### Scale ($500-2,000/month)

```
Supabase Team: $599/month
Render Professional: $50/month
Redis Cloud Standard: $35/month
Inngest Pro: $50/month
Auth0 Essentials: $240/month
CodeRabbit Team: $48/month
Sentry Business: $80/month
Langfuse Pro: $49/month
Gemini API: $200/month
GPT-4o API: $500/month
────────────────────────────────────────
TOTAL: $1,851/month + volume LLM usage

Can serve: 1,000-10,000 users
Projects: 1,000-5,000/month
Uptime: 99.95%
Enterprise ready: Yes
```

---

## Implementation Timeline

### Month 1: Foundation + POC Launch

**Week 1-2:** Core Infrastructure
- ✅ Database migrations
- ✅ Job queue (BullMQ)
- ✅ Audit service
- ✅ Cost tracking
- ✅ Quota service
- ✅ Deploy on $6 Digital Ocean droplet

**Week 3:** Quality & Monitoring
- ✅ Multi-layer validation
- ✅ Langfuse observability
- ✅ Sentry error tracking
- ✅ Basic monitoring dashboard

**Week 4:** Testing & Refinement
- ✅ End-to-end testing with 5 beta users
- ✅ Fix critical bugs
- ✅ Performance optimization
- ✅ Documentation

**Deliverable:** Working POC with all 10 infrastructure features

### Month 2: MVP Launch

**Week 1:** Migration to Managed Services
- ✅ Upgrade to Supabase Pro
- ✅ Deploy to Render
- ✅ Switch to managed Redis
- ✅ Inngest integration

**Week 2:** CI/CD & Quality
- ✅ GitHub Actions setup
- ✅ CodeRabbit integration
- ✅ Automated testing
- ✅ Architecture compliance checks

**Week 3:** Polish & UX
- ✅ Real-time progress UI
- ✅ Better error messages
- ✅ Onboarding flow
- ✅ Post-handoff checklist

**Week 4:** Launch Prep
- ✅ Load testing
- ✅ Security audit
- ✅ Legal (ToS, Privacy Policy)
- ✅ Payment integration (Stripe)

**Deliverable:** Production-ready MVP with paying customers

### Month 3+: Scale Features

- Enterprise auth (Auth0)
- Advanced analytics
- Multi-region deployment
- Custom model support
- API for third-party integrations
- Marketplace for templates

---

## Decision Matrix: Build vs Buy

For each technology, here's when to use free/open source vs paid:

| Technology | Use Free When... | Pay For When... |
|------------|------------------|-----------------|
| **Database** | < 500MB, < 50K users | Need more space, users, or support |
| **Caching** | Can self-host reliably | Want managed service & SLA |
| **Job Queue** | < 30K jobs/month | Need enterprise features |
| **Observability** | Can self-host | Want cloud convenience |
| **Monitoring** | < 5K errors/month | Need better retention/features |
| **Auth** | Simple email/password | Need SSO, SAML, MFA |
| **Payments** | Just starting | Making real revenue |
| **Deployment** | Static sites only | Need backend services |
| **Security** | CLI tools enough | Need compliance reports |
| **AI APIs** | Testing/development | Production with volume |

---

## Conclusion

This plan gives you:

1. **Zero-cost start:** Prove the concept with $20/month
2. **Clear upgrade path:** Know exactly when and why to upgrade each service
3. **No vendor lock-in:** Every choice has an open source alternative
4. **Production-ready:** All 10 critical infrastructure gaps addressed
5. **Scalable:** Clear path from POC ($20) → MVP ($150) → Scale ($2,000)

**Recommendation:** Start with Proof of Concept tier immediately. You can validate the entire workflow for under $20/month. Only upgrade to MVP tier once you have 20+ active users and consistent usage.

The beauty of this approach: **You're building the exact same architecture at all three tiers.** The only difference is managed vs self-hosted. Your code doesn't change, just your infrastructure provider.

---

**Next Steps:**
1. Run database migrations (Tier 1)
2. Implement job queue with BullMQ (Tier 1)
3. Add audit/cost tracking services (Tier 1)
4. Deploy to $6 Digital Ocean droplet (Tier 1)
5. Test with 5-10 beta users
6. Upgrade to MVP tier when ready

**Start Date:** Now
**POC Ready:** 3-4 weeks
**MVP Ready:** 6-8 weeks
**First Paying Customer:** Week 9-10
