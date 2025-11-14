# Code Review Action Plan - Prioritized Fixes

**Date**: 2025-11-14
**Status**: Ready for Implementation
**Total Estimated Time**: 37-55 hours

---

## Priority Level Definitions

- 🔴 **CRITICAL**: Security vulnerabilities, data corruption risks (Fix immediately)
- 🟡 **HIGH**: Production blockers, significant bugs (Fix before deployment)
- 🟠 **MEDIUM**: Code quality, performance optimizations (Fix in sprint 1)
- 🟢 **LOW**: Nice-to-haves, technical debt (Backlog)

---

## Phase 1: Critical Security & Data Integrity (10-14 hours)

### 🔴 CRITICAL-1: SQL Injection in Admin Endpoints
**Source**: Codex Review
**Severity**: CRITICAL - Security Vulnerability
**Impact**: Attackers can access/modify unauthorized data
**Time**: 2-3 hours

**Files to Fix**:
- `admin-console/supabase/functions/admin-customers/index.ts` (lines 71-80)
- `admin-console/supabase/functions/admin-projects/index.ts` (lines 62-75)

**Current Vulnerable Code**:
```typescript
.or(`full_name.ilike.%${search}%,email.ilike.%${search}%`)
```

**Fix**:
Replace with parameterized queries:
```typescript
let query = supabase.from('customers').select('*', { count: 'exact' });

if (search) {
  query = query.or(`full_name.ilike.%${search.replace(/[%_]/g, '\\$&')}%,email.ilike.%${search.replace(/[%_]/g, '\\$&')}%`);
  // Better: Use separate .ilike() calls
  query = query.or(
    supabase.filters.or([
      supabase.filters.ilike('full_name', `%${search}%`),
      supabase.filters.ilike('email', `%${search}%`)
    ])
  );
}
```

**Testing**:
- Test with malicious inputs: `foo%') or true --`
- Verify only authorized rows returned

---

### 🔴 CRITICAL-2: Race Condition in Quota Service
**Source**: Cursor Review (Factory)
**Severity**: CRITICAL - Data Integrity
**Impact**: Users can bypass quota limits with concurrent requests
**Time**: 3-4 hours

**File**: `apps/factory/src/services/quota.service.ts`

**Current Pattern** (Vulnerable):
```typescript
// 1. Fetch current value
const { data: current } = await this.client.from('usage_quotas').select(field).single();
const currentValue = current ? current[field] : 0;

// 2. Calculate new value
const newValue = currentValue + amount;

// 3. Update (another request could have incremented in between!)
await this.client.from('usage_quotas').update({ [field]: newValue });
```

**Fix - Option A: Database-Level Atomic Update**:
```typescript
async incrementUsage(userId: string, type: string, amount: number = 1): Promise<void> {
  const field = this.getFieldName(type);

  // Use PostgreSQL's atomic increment
  const { error } = await this.client.rpc('increment_usage', {
    p_user_id: userId,
    p_field: field,
    p_amount: amount
  });

  if (error) throw error;
}
```

**SQL Function to Create**:
```sql
CREATE OR REPLACE FUNCTION increment_usage(
  p_user_id UUID,
  p_field TEXT,
  p_amount INTEGER
)
RETURNS void AS $$
BEGIN
  UPDATE usage_quotas
  SET
    current_projects = CASE WHEN p_field = 'current_projects' THEN current_projects + p_amount ELSE current_projects END,
    current_ai_tokens = CASE WHEN p_field = 'current_ai_tokens' THEN current_ai_tokens + p_amount ELSE current_ai_tokens END,
    current_storage_gb = CASE WHEN p_field = 'current_storage_gb' THEN current_storage_gb + p_amount ELSE current_storage_gb END
  WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;
```

**Fix - Option B: Row-Level Locking**:
```typescript
async incrementUsage(userId: string, type: string, amount: number = 1): Promise<void> {
  const field = this.getFieldName(type);

  // Use FOR UPDATE to lock the row
  const { data, error: selectError } = await this.client
    .from('usage_quotas')
    .select(field)
    .eq('user_id', userId)
    .single();
    // Note: Supabase doesn't support FOR UPDATE directly, so use RPC

  // Better: Use RPC with explicit locking
  const { error } = await this.client.rpc('increment_usage_locked', {
    p_user_id: userId,
    p_field: field,
    p_amount: amount
  });
}
```

**Recommendation**: Use Option A (atomic RPC) for best performance

**Testing**:
- Send 100 concurrent increment requests
- Verify final count is exactly 100

---

### 🔴 CRITICAL-3: Unhandled Promise Rejections
**Source**: Cursor Review (Factory)
**Severity**: CRITICAL - Application Crashes
**Impact**: Crashes node process in production
**Time**: 2-3 hours

**Files**:
- `apps/factory/src/services/codex.service.ts` (JSON parsing)
- `apps/factory/src/services/gemini.service.ts` (JSON parsing)
- `apps/factory/src/services/ai-agent-orchestrator.service.ts`

**Current Code**:
```typescript
const result = await response.json() as any;
// If JSON parsing fails, unhandled rejection crashes process
```

**Fix**:
```typescript
async parseJSONSafely<T>(response: Response): Promise<T> {
  try {
    const text = await response.text();
    return JSON.parse(text) as T;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    throw new Error(`Failed to parse JSON response: ${errorMessage}. Response: ${text?.substring(0, 200)}`);
  }
}

// Usage:
const result = await this.parseJSONSafely<CodexResponse>(response);
```

**Global Handler** (add to main app):
```typescript
// In apps/factory/src/api/index.ts
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Don't crash, but log to monitoring service
  // Optionally: process.exit(1) in production with PM2 restart
});
```

**Testing**:
- Send malformed JSON responses
- Verify graceful error handling

---

### 🔴 CRITICAL-4: Missing External API Retry Logic
**Source**: Cursor Review (Factory)
**Severity**: CRITICAL - Reliability
**Impact**: Transient failures cause workflow failures
**Time**: 3-4 hours

**Files**:
- `apps/factory/src/services/gemini.service.ts`
- `apps/factory/src/services/codex.service.ts`
- `apps/factory/src/services/ai-agent-orchestrator.service.ts`

**Fix - Create Retry Utility**:
```typescript
// apps/factory/src/utils/retry.ts
export interface RetryConfig {
  maxRetries: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  retryableErrors?: string[];
}

export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  config: RetryConfig = {
    maxRetries: 3,
    initialDelayMs: 1000,
    maxDelayMs: 10000,
    backoffMultiplier: 2,
    retryableErrors: ['ECONNRESET', 'ETIMEDOUT', 'ENOTFOUND', '429', '500', '502', '503', '504']
  }
): Promise<T> {
  let lastError: Error;
  let delayMs = config.initialDelayMs;

  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      // Check if error is retryable
      const isRetryable = config.retryableErrors?.some(err =>
        lastError.message.includes(err) || (lastError as any).code === err
      );

      if (!isRetryable || attempt === config.maxRetries) {
        throw lastError;
      }

      console.warn(`Attempt ${attempt + 1}/${config.maxRetries} failed: ${lastError.message}. Retrying in ${delayMs}ms...`);

      await new Promise(resolve => setTimeout(resolve, delayMs));
      delayMs = Math.min(delayMs * config.backoffMultiplier, config.maxDelayMs);
    }
  }

  throw lastError!;
}
```

**Apply to Services**:
```typescript
// In gemini.service.ts
async generatePRD(conversation: ConversationMessage[]): Promise<PRD> {
  return retryWithBackoff(async () => {
    const result = await this.model.generateContent({
      contents: conversation.map(msg => ({
        role: msg.role === 'user' ? 'user' : 'model',
        parts: [{ text: msg.content }],
      })),
    });

    const response = await result.response;
    return this.parsePRD(response.text());
  });
}
```

**Testing**:
- Mock network failures
- Verify 3 retries with exponential backoff
- Verify non-retryable errors fail immediately

---

## Phase 2: High Priority Production Blockers (15-23 hours)

### 🟡 HIGH-1: Production CORS Domains Not Configured
**Source**: Cursor Review (Admin Console)
**Severity**: HIGH - Production Blocker
**Impact**: Production web app won't work
**Time**: 1-2 hours

**File**: `admin-console/supabase/functions/_shared/cors.ts`

**Current**:
```typescript
const ALLOWED_ORIGINS = [
  'http://localhost:8081', // Expo dev
  'exp://localhost:8081',  // Expo dev
  // Production domains configured here
];
```

**Fix**:
```typescript
const ALLOWED_ORIGINS = [
  // Development
  'http://localhost:8081',
  'exp://localhost:8081',
  'http://localhost:19006', // Expo web

  // Production (ADD THESE)
  'https://admin.designfirstfactory.com',
  'https://admin-console.designfirstfactory.com',
  'https://app.designfirstfactory.com',

  // Staging
  'https://staging-admin.designfirstfactory.com',
];

// More restrictive validation
export function getCorsHeaders(req: Request) {
  const origin = req.headers.get('origin') || '';

  // Exact match only (no startsWith for production)
  const isAllowed = ALLOWED_ORIGINS.includes(origin);

  if (!isAllowed && process.env.NODE_ENV === 'production') {
    console.warn(`Blocked CORS request from unauthorized origin: ${origin}`);
  }

  return {
    'Access-Control-Allow-Origin': isAllowed ? origin : '',
    'Access-Control-Allow-Headers': 'authorization, content-type, x-client-info',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
    'Access-Control-Max-Age': '86400',
  };
}
```

**Action**: User needs to provide production domains

---

### 🟡 HIGH-2: Rate Limiter Needs Redis Migration
**Source**: Cursor Review (Admin Console)
**Severity**: HIGH - Scalability
**Impact**: Won't work with multiple instances
**Time**: 4-6 hours

**File**: `admin-console/supabase/functions/_shared/rate-limit.ts`

**Current**: In-memory Map (doesn't scale)

**Fix - Upstash Redis**:
```typescript
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: Deno.env.get('UPSTASH_REDIS_URL')!,
  token: Deno.env.get('UPSTASH_REDIS_TOKEN')!,
});

export async function checkRateLimit(
  userId: string,
  limit: RateLimitConfig
): Promise<RateLimitInfo> {
  const key = `ratelimit:${userId}`;
  const now = Date.now();
  const windowStart = now - limit.windowMs;

  // Use Redis sorted set for sliding window
  const pipeline = redis.pipeline();

  // Remove old entries
  pipeline.zremrangebyscore(key, 0, windowStart);

  // Count current requests
  pipeline.zcard(key);

  // Add current request
  pipeline.zadd(key, { score: now, member: `${now}:${Math.random()}` });

  // Set expiry
  pipeline.expire(key, Math.ceil(limit.windowMs / 1000));

  const results = await pipeline.exec();
  const count = results[1] as number;

  return {
    allowed: count < limit.maxRequests,
    remaining: Math.max(0, limit.maxRequests - count - 1),
    resetAt: now + limit.windowMs,
  };
}
```

**Environment Setup**:
1. Create Upstash Redis account
2. Add `UPSTASH_REDIS_URL` and `UPSTASH_REDIS_TOKEN` to env
3. Update all edge functions to use new rate limiter

**Testing**:
- Deploy to multiple instances
- Send concurrent requests
- Verify rate limit enforced globally

---

### 🟡 HIGH-3: Excessive `as any` Type Assertions
**Source**: Cursor Review (Factory)
**Severity**: HIGH - Type Safety
**Impact**: Type safety compromised, potential runtime errors
**Time**: 3-4 hours

**Files**:
- `apps/factory/src/services/codex.service.ts` (3 instances)
- `apps/factory/src/services/playwright.service.ts` (1 instance)
- `apps/factory/src/services/supabase.service.ts` (2 instances)

**Fix - Define Proper Types**:
```typescript
// codex.service.ts - Instead of:
const result = await response.json() as any;

// Define interface:
interface OpenAIResponse {
  choices: Array<{
    message: {
      content: string;
      role: string;
    };
    finish_reason: string;
  }>;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
  };
}

const result = await response.json() as OpenAIResponse;
```

**All Files to Update**:
1. Create `apps/factory/src/types/external-apis.ts` with all API response types
2. Replace all `as any` with proper interfaces
3. Add runtime validation for critical paths

---

### 🟡 HIGH-4: Missing Input Validation (Factory)
**Source**: Cursor Review (Factory)
**Severity**: HIGH - Security
**Impact**: XSS, injection risks
**Time**: 4-6 hours

**Files**: All API endpoints in `apps/factory/src/api/`

**Fix - Create Validation Middleware**:
```typescript
// apps/factory/src/middleware/validation.ts
import { z } from 'zod';
import { Request, Response, NextFunction } from 'express';

export const safeTextSchema = (maxLength = 500) =>
  z.string()
    .max(maxLength)
    .trim()
    .refine(
      str => !/<script|javascript:|on\w+=/i.test(str),
      'Invalid characters detected'
    );

export const validateBody = (schema: z.ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors,
        });
      }
      next(error);
    }
  };
};

// Define schemas for each endpoint
export const createProjectSchema = z.object({
  name: safeTextSchema(255),
  description: safeTextSchema(1000).optional(),
  tier: z.enum(['express', 'concierge']),
  intake: z.object({
    // ... intake fields
  }),
});
```

**Apply to Routes**:
```typescript
// apps/factory/src/api/projects.ts
router.post('/projects', validateBody(createProjectSchema), async (req, res) => {
  // req.body is now validated and typed
});
```

---

### 🟡 HIGH-5: Validation Only on Customers Endpoint
**Source**: Cursor Review (Admin Console)
**Severity**: HIGH - Security
**Impact**: Projects/invoices endpoints vulnerable
**Time**: 3-5 hours

**Files to Create**:
- `admin-console/supabase/functions/admin-projects/index.ts` (add validation)
- `admin-console/supabase/functions/admin-invoices/index.ts` (add validation)
- `admin-console/supabase/functions/admin-notes/index.ts` (add validation)

**Fix - Extend Validation Schemas**:
```typescript
// In validation.ts, add:
export const createProjectSchema = z.object({
  customer_id: uuidSchema,
  name: safeTextSchema(255),
  description: safeTextSchema(1000).optional(),
  status: z.enum(['planning', 'in_progress', 'review', 'completed', 'cancelled']),
  start_date: dateSchema,
  end_date: dateSchema.optional(),
  budget: z.number().min(0).optional(),
  tier: z.enum(['express', 'concierge']),
}).refine(
  data => !data.end_date || data.end_date >= data.start_date,
  'End date must be after start date'
);

export const updateProjectSchema = createProjectSchema.partial();
```

**Apply to All Endpoints**:
Update each endpoint's POST/PATCH handlers to validate input

---

## Phase 3: Medium Priority Code Quality (12-18 hours)

### 🟠 MEDIUM-1: Missing Rate Limiting (Factory)
**Time**: 3-4 hours
**Fix**: Add rate limiting middleware to all API routes

### 🟠 MEDIUM-2: Missing Error Boundary Wrapper
**Time**: 2-3 hours
**Fix**: Add global error handler to admin console

### 🟠 MEDIUM-3: Type Safety Issues
**Time**: 3-4 hours
**Fix**: Add strict null checks, improve type definitions

### 🟠 MEDIUM-4: Performance Optimizations
**Time**: 2-3 hours
**Fix**: Add caching, optimize queries

### 🟠 MEDIUM-5: Code Organization
**Time**: 2-4 hours
**Fix**: Refactor duplicate code, improve structure

---

## Phase 4: Low Priority Technical Debt (6-10 hours)

### 🟢 LOW-1: Add JSDoc Comments
**Time**: 2-3 hours

### 🟢 LOW-2: Improve Logging
**Time**: 2-3 hours

### 🟢 LOW-3: Code Style Consistency
**Time**: 1-2 hours

### 🟢 LOW-4: Unused Code Cleanup
**Time**: 1-2 hours

---

## Implementation Order

**Day 1** (8-10 hours):
1. ✅ CRITICAL-1: SQL Injection fix
2. ✅ CRITICAL-2: Race condition fix
3. ✅ CRITICAL-3: Unhandled promises fix

**Day 2** (8-10 hours):
4. ✅ CRITICAL-4: Retry logic
5. ✅ HIGH-1: CORS configuration
6. ✅ HIGH-2: Redis migration (start)

**Day 3** (8-10 hours):
7. ✅ HIGH-2: Redis migration (complete)
8. ✅ HIGH-3: Remove `as any` assertions
9. ✅ HIGH-4: Input validation (start)

**Day 4** (8-10 hours):
10. ✅ HIGH-4: Input validation (complete)
11. ✅ HIGH-5: Extend validation to all endpoints
12. ✅ MEDIUM items (start)

**Day 5** (5-7 hours):
13. ✅ MEDIUM items (complete)
14. ✅ LOW items (as time permits)

---

## Testing Strategy

After each fix:
1. **Unit Tests**: Test the specific fix
2. **Integration Tests**: Test with related components
3. **Manual Testing**: Verify in development environment
4. **Commit**: Commit the fix with clear message

After each phase:
1. **Full Regression**: Run all tests
2. **Code Review**: Self-review changes
3. **Documentation**: Update docs

After all fixes:
1. **Full E2E Tests**: Test complete workflows
2. **Load Testing**: Verify performance
3. **Security Scan**: Run security tools
4. **Final Review**: Get approval from Cursor/Gemini

---

## Success Criteria

- [ ] All CRITICAL issues fixed and tested
- [ ] All HIGH issues fixed and tested
- [ ] TypeScript compilation: 0 errors
- [ ] No security vulnerabilities
- [ ] All tests passing
- [ ] Code review approval
- [ ] Ready for production deployment

---

**Status**: Ready to Start
**Next Action**: Begin CRITICAL-1 (SQL Injection fix)
