#!/usr/bin/env node
/**
 * API & Deployment Documentation Generator
 * Generates remaining architecture documents: API spec and deployment guide
 *
 * Usage:
 *   node scripts/generate-api-deployment.js \
 *     --requirements session-X/requirements/iteration-0.json \
 *     --output-dir session-X/architecture
 */

const fs = require('fs');
const path = require('path');

// Parse arguments
const args = process.argv.slice(2);
const getArg = (flag) => {
    const index = args.indexOf(flag);
    return index !== -1 ? args[index + 1] : null;
};

const requirementsFile = getArg('--requirements');
const outputDir = getArg('--output-dir');

if (!requirementsFile || !outputDir) {
    console.error('Usage: node generate-api-deployment.js --requirements <path> --output-dir <path>');
    process.exit(1);
}

// Read requirements
const requirements = JSON.parse(fs.readFileSync(requirementsFile, 'utf8'));

console.log('🔧 Generating API & Deployment Docs...');
console.log(`   App: ${requirements.app_name}\n`);

// ============================================================================
// API SPECIFICATION
// ============================================================================

function generateAPI(requirements) {
    const appName = requirements.app_name;
    const features = requirements.features?.must_have || [];

    const needsBackend = features.some(f =>
        f.toLowerCase().includes('sync') ||
        f.toLowerCase().includes('share') ||
        f.toLowerCase().includes('api')
    );

    const needsAuth = features.some(f =>
        f.toLowerCase().includes('account') ||
        f.toLowerCase().includes('user')
    );

    return `# API Specification

## Overview

${needsBackend ? `
${appName} provides a **REST API** for cloud sync and optional features. The API follows REST principles with JSON payloads.

**Base URL**: \`https://api.${appName.toLowerCase()}.com/v1\` (production)
**Base URL**: \`http://localhost:3000/api\` (development)

**Authentication**: ${needsAuth ? 'Bearer tokens (JWT via NextAuth.js)' : 'Not required (local-only app)'}
**Rate Limiting**: 100 requests/minute per user
**Versioning**: URL-based (\`/v1/\`)
` : `
${appName} is a **local-first application** with no backend API in the MVP.

**Decision**: No API endpoints required for core functionality
**Rationale**: All ${features.length} must-have features work offline with localStorage

**Future Consideration**: API may be added if users request:
- Cloud sync across devices
- Team collaboration features
- Analytics beyond local data
`}

---

${needsBackend ? `
## Authentication

### Login
**Endpoint**: \`POST /api/auth/login\`

**Purpose**: Authenticate user and create session

**Request**:
\`\`\`http
POST /api/auth/login HTTP/1.1
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123"
}
\`\`\`

**Response** (200 OK):
\`\`\`json
{
  "user": {
    "id": "uuid-v4",
    "email": "user@example.com",
    "name": "Jane Doe"
  },
  "token": "jwt-token-here",
  "expiresAt": "2025-10-25T12:00:00Z"
}
\`\`\`

**Errors**:
- \`401 Unauthorized\`: Invalid credentials
- \`429 Too Many Requests\`: Rate limit exceeded
- \`500 Internal Server Error\`: Server error

---

### Signup
**Endpoint**: \`POST /api/auth/signup\`

**Purpose**: Create new user account

**Request**:
\`\`\`http
POST /api/auth/signup HTTP/1.1
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "Jane Doe"
}
\`\`\`

**Response** (201 Created):
\`\`\`json
{
  "user": {
    "id": "uuid-v4",
    "email": "user@example.com",
    "name": "Jane Doe",
    "emailVerified": null
  },
  "message": "Verification email sent"
}
\`\`\`

**Validation**:
- Email: Valid format, unique, max 255 chars
- Password: Min 8 chars, requires number + letter
- Name: Optional, max 100 chars

**Errors**:
- \`400 Bad Request\`: Validation failed
- \`409 Conflict\`: Email already registered

---

## Data Sync

### Sync Entries
**Endpoint**: \`POST /api/sync\`

**Purpose**: Sync local entries to cloud (bidirectional)

**Authentication**: Required (Bearer token)

**Request**:
\`\`\`http
POST /api/sync HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "clientLastSync": "2025-10-23T12:00:00Z",
  "entries": [
    {
      "id": "uuid-v4",
      "timestamp": "2025-10-24T08:00:00Z",
      "value": 250,
      "unit": "ml",
      "notes": "Morning water",
      "goalId": "uuid-v4",
      "createdAt": "2025-10-24T08:00:00Z",
      "updatedAt": "2025-10-24T08:00:00Z"
    }
  ],
  "goals": [
    {
      "id": "uuid-v4",
      "name": "Daily Water",
      "target": 2000,
      "unit": "ml",
      "frequency": "daily",
      "startDate": "2025-10-01",
      "active": true
    }
  ]
}
\`\`\`

**Response** (200 OK):
\`\`\`json
{
  "serverLastSync": "2025-10-24T12:00:00Z",
  "conflicts": [],
  "newEntries": [
    {
      "id": "uuid-v4-from-another-device",
      "timestamp": "2025-10-24T09:00:00Z",
      "value": 500,
      "unit": "ml"
    }
  ],
  "deletedEntries": [],
  "message": "Sync complete"
}
\`\`\`

**Conflict Resolution**:
- **Strategy**: Last-write-wins (by \`updatedAt\`)
- **Conflicts**: Returned in response, client decides
- **Deletions**: Soft-delete on server, tombstone records

**Errors**:
- \`401 Unauthorized\`: Invalid token
- \`400 Bad Request\`: Invalid data format
- \`413 Payload Too Large\`: >1000 entries (batch required)

---

### Export Data
**Endpoint**: \`GET /api/export\`

**Purpose**: Export all user data as JSON (GDPR compliance)

**Authentication**: Required

**Request**:
\`\`\`http
GET /api/export HTTP/1.1
Authorization: Bearer <token>
\`\`\`

**Response** (200 OK):
\`\`\`json
{
  "version": 1,
  "exportedAt": "2025-10-24T12:00:00Z",
  "user": {
    "id": "uuid-v4",
    "email": "user@example.com",
    "createdAt": "2025-10-01T12:00:00Z"
  },
  "entries": [ /* all entries */ ],
  "goals": [ /* all goals */ ],
  "checksum": "sha256-hash"
}
\`\`\`

**Headers**:
\`\`\`
Content-Disposition: attachment; filename="hydrotrack-export-20251024.json"
\`\`\`

---

## Health Check

### API Health
**Endpoint**: \`GET /api/healthz\`

**Purpose**: Check API availability (no auth required)

**Response** (200 OK):
\`\`\`json
{
  "status": "healthy",
  "timestamp": "2025-10-24T12:00:00Z",
  "version": "1.0.0",
  "uptime": 864000
}
\`\`\`

**Response** (503 Service Unavailable):
\`\`\`json
{
  "status": "unhealthy",
  "errors": ["Database connection failed"]
}
\`\`\`

---

## Error Handling

### Standard Error Response
\`\`\`json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid entry data",
    "details": [
      {
        "field": "value",
        "issue": "Must be positive number"
      }
    ],
    "requestId": "req-uuid-v4",
    "timestamp": "2025-10-24T12:00:00Z"
  }
}
\`\`\`

### Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| \`VALIDATION_ERROR\` | 400 | Request data invalid |
| \`UNAUTHORIZED\` | 401 | Missing/invalid token |
| \`FORBIDDEN\` | 403 | Valid token but no permission |
| \`NOT_FOUND\` | 404 | Resource doesn't exist |
| \`CONFLICT\` | 409 | Resource already exists |
| \`RATE_LIMIT_EXCEEDED\` | 429 | Too many requests |
| \`INTERNAL_ERROR\` | 500 | Server error |
| \`SERVICE_UNAVAILABLE\` | 503 | Temporary outage |

---

## Rate Limiting

**Limits**:
- **Authenticated**: 100 requests/minute
- **Unauthenticated**: 10 requests/minute (healthz only)
- **Sync**: 10 syncs/minute (large payloads)

**Headers**:
\`\`\`
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1698148800
\`\`\`

**Response** (429):
\`\`\`json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 60
  }
}
\`\`\`

---

## Pagination

For endpoints returning lists (future):

**Query Parameters**:
- \`limit\`: Items per page (default: 50, max: 100)
- \`cursor\`: Opaque cursor for next page
- \`sortBy\`: Field to sort by
- \`order\`: \`asc\` or \`desc\`

**Response**:
\`\`\`json
{
  "data": [ /* items */ ],
  "pagination": {
    "hasMore": true,
    "nextCursor": "base64-encoded-cursor",
    "total": 1250
  }
}
\`\`\`

` : `
## No API Required

${appName} operates entirely client-side with no backend API.

**Data Flow**:
\`\`\`
User Action → React State → localStorage → UI Update
\`\`\`

**Benefits**:
- ✅ Zero latency (no network calls)
- ✅ Offline-first (always works)
- ✅ Privacy (no data leaves device)
- ✅ Cost (no server hosting)

**If API Added Later**:
Would follow REST conventions:
- \`POST /api/sync\` - Cloud sync
- \`GET /api/export\` - Data export
- \`POST /api/auth/login\` - Authentication

See \`architecture-tech-stack.md\` for migration path.
`}

---

## External Integrations

### Current (MVP)
**None** - No third-party API dependencies

### Future Consideration

${requirements.app_type === 'health_tracking' ? `
#### Apple Health / Google Fit
**Purpose**: Import health data from wearables

**Implementation**:
- OAuth 2.0 for user authorization
- Webhooks for real-time updates
- Rate limits: Vendor-specific

**Data Mapping**:
\`\`\`typescript
// Apple Health → HydroTrack
{
  "HKQuantityTypeIdentifierDietaryWater": "water intake (ml)",
  "HKQuantityTypeIdentifierStepCount": "steps (count)"
}
\`\`\`

**Privacy**: All data stored locally, sync opt-in only
` : ''}

#### AI Insights (Claude API)
**Purpose**: Generate personalized recommendations

**Endpoint**: \`https://api.anthropic.com/v1/messages\`
**Authentication**: API key (server-side only)
**Rate Limit**: 1000 requests/day (free tier)

**Example Request**:
\`\`\`typescript
const prompt = \`Based on this tracking data: \${JSON.stringify(entries)},
provide 3 actionable recommendations to improve consistency.\`;

fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: {
    'x-api-key': process.env.ANTHROPIC_API_KEY,
    'anthropic-version': '2023-06-01',
    'content-type': 'application/json'
  },
  body: JSON.stringify({
    model: 'claude-3-haiku-20240307',
    max_tokens: 500,
    messages: [{ role: 'user', content: prompt }]
  })
});
\`\`\`

**Cost**: ~$0.001 per insight

---

## API Testing

### Development
\`\`\`bash
# Start dev server
npm run dev

# Test healthz endpoint
curl http://localhost:3000/api/healthz

# Test auth (if backend exists)
curl -X POST http://localhost:3000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email":"test@example.com","password":"test123"}'
\`\`\`

### Automated Testing
\`\`\`bash
# Unit tests (API routes)
npm run test:api

# Integration tests (full request/response)
npm run test:integration

# Load testing (optional)
npm run test:load
\`\`\`

---

## API Versioning

**Strategy**: URL-based versioning

**Versions**:
- \`/v1/\`: Initial release (current)
- \`/v2/\`: Breaking changes (future)

**Deprecation Policy**:
- New version released 6 months before old deprecated
- Old version supported 12 months after deprecation
- Sunset notices in response headers

**Header**:
\`\`\`
X-API-Version: 1.0.0
X-API-Deprecated: false
\`\`\`

---

## References

**Standards**:
- [REST API Design](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [OAuth 2.0](https://oauth.net/2/)

**PRD Cross-References**:
- See \`prd/03-acceptance-criteria.md\` for API requirements
- See \`architecture-data-model.md\` for payload schemas
`;
}

// ============================================================================
// DEPLOYMENT DOCUMENTATION
// ============================================================================

function generateDeployment(requirements) {
    const appName = requirements.app_name;

    return `# Deployment Architecture

## Overview

${appName} follows a **continuous deployment** strategy with automated testing and zero-downtime deployments.

**Platform**: Vercel (recommended)
**Alternative**: Netlify, Cloudflare Pages, or self-hosted

---

## Local Development Setup

### Prerequisites
\`\`\`bash
# Required
node >= 18.0.0
npm >= 9.0.0

# Recommended
git >= 2.30.0
VS Code (with ESLint + Prettier extensions)
\`\`\`

### Quick Start
\`\`\`bash
# Clone repository
git clone https://github.com/yourorg/${appName.toLowerCase()}.git
cd ${appName.toLowerCase()}

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser
open http://localhost:3000
\`\`\`

### Environment Variables
Create \`.env.local\`:
\`\`\`bash
# App
NEXT_PUBLIC_APP_NAME="${appName}"
NEXT_PUBLIC_APP_URL="http://localhost:3000"

# Optional: If backend exists
# DATABASE_URL="postgresql://user:pass@localhost:5432/db"
# NEXTAUTH_SECRET="generate-with-openssl-rand-base64-32"
# NEXTAUTH_URL="http://localhost:3000"
\`\`\`

**Generate Secrets**:
\`\`\`bash
# NextAuth secret
openssl rand -base64 32

# API keys (store in 1Password/Vault)
openssl rand -hex 32
\`\`\`

---

## Docker Development (Optional)

### Dockerfile
\`\`\`dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

# Build application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
\`\`\`

### Docker Compose
\`\`\`yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    restart: unless-stopped

  # Optional: Add database if backend exists
  # postgres:
  #   image: postgres:15-alpine
  #   environment:
  #     POSTGRES_USER: user
  #     POSTGRES_PASSWORD: password
  #     POSTGRES_DB: ${appName.toLowerCase()}
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data

# volumes:
#   postgres_data:
\`\`\`

**Run**:
\`\`\`bash
docker-compose up -d
\`\`\`

---

## CI/CD Pipeline

### GitHub Actions Workflow
**File**: \`.github/workflows/deploy.yml\`

\`\`\`yaml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Run tests
        run: npm run test

      - name: Build
        run: npm run build

  visual-qa:
    runs-on: ubuntu-latest
    needs: lint-and-test
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run Visual QA
        run: npm run test:visual

      - name: Upload screenshots
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: visual-qa-screenshots
          path: screenshots/

  deploy-preview:
    runs-on: ubuntu-latest
    needs: visual-qa
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel (Preview)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: \${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: \${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: \${{ secrets.VERCEL_PROJECT_ID }}
          scope: \${{ secrets.VERCEL_SCOPE }}

  deploy-production:
    runs-on: ubuntu-latest
    needs: visual-qa
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel (Production)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: \${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: \${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: \${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          scope: \${{ secrets.VERCEL_SCOPE }}

      - name: Notify on success
        if: success()
        run: |
          curl -X POST \${{ secrets.SLACK_WEBHOOK }} \\
            -H 'Content-Type: application/json' \\
            -d '{"text":"✅ ${appName} deployed to production"}'

      - name: Notify on failure
        if: failure()
        run: |
          curl -X POST \${{ secrets.SLACK_WEBHOOK }} \\
            -H 'Content-Type: application/json' \\
            -d '{"text":"❌ ${appName} deployment failed"}'
\`\`\`

---

## Vercel Deployment

### Setup
\`\`\`bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link project
vercel link

# Deploy preview
vercel

# Deploy production
vercel --prod
\`\`\`

### Environment Variables (Vercel Dashboard)
Navigate to: **Project Settings → Environment Variables**

**Production**:
\`\`\`
NEXT_PUBLIC_APP_NAME="${appName}"
NEXT_PUBLIC_APP_URL="https://${appName.toLowerCase()}.vercel.app"
# Add database/auth secrets if backend exists
\`\`\`

**Preview**:
- Inherits production variables
- Override with preview-specific values if needed

### Custom Domain
**Settings → Domains**:
1. Add domain: \`${appName.toLowerCase()}.com\`
2. Configure DNS:
   \`\`\`
   CNAME @ cname.vercel-dns.com
   \`\`\`
3. Wait for SSL certificate (automatic)

---

## Monitoring & Observability

### Vercel Analytics
**Setup**:
\`\`\`typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
\`\`\`

**Metrics Tracked**:
- Page views, unique visitors
- Core Web Vitals (LCP, FID, CLS)
- Device/browser distribution
- Geographic distribution

**Dashboard**: https://vercel.com/yourorg/${appName.toLowerCase()}/analytics

---

### Sentry Error Tracking
**Setup**:
\`\`\`bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
\`\`\`

**Configuration**: \`sentry.client.config.ts\`
\`\`\`typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
\`\`\`

**Alerts**:
- Slack webhook for critical errors
- Email for new error types
- Weekly digest

---

### Uptime Monitoring
**Service**: UptimeRobot (free tier)

**Monitors**:
1. **Homepage**: \`https://${appName.toLowerCase()}.com\`
   - Interval: 5 minutes
   - Alert: Email + Slack

2. **API Health**: \`https://${appName.toLowerCase()}.com/api/healthz\`
   - Interval: 5 minutes
   - Expected: 200 status

**Alerting**:
- Down for 2+ checks → Immediate alert
- Slow response (>3s) → Warning

---

## Database Migrations (If Backend Exists)

### Prisma Migrations
\`\`\`bash
# Create migration
npx prisma migrate dev --name add_sync_fields

# Apply to production
npx prisma migrate deploy

# Generate client
npx prisma generate
\`\`\`

### Migration Strategy
1. **Development**: Run migrations locally
2. **Staging**: Deploy + test migrations
3. **Production**: Run during low-traffic window
4. **Rollback**: Keep previous schema version ready

**Safety**:
- Always backup database before migrations
- Test on staging environment first
- Use transactions for atomic changes
- Have rollback SQL ready

---

## Backup & Disaster Recovery

### Database Backups (If Backend)
**Supabase**: Automatic daily backups (retained 7 days)

**Manual Backup**:
\`\`\`bash
# Dump database
pg_dump \$DATABASE_URL > backup-$(date +%Y%m%d).sql

# Upload to S3
aws s3 cp backup-$(date +%Y%m%d).sql s3://backups/${appName.toLowerCase()}/
\`\`\`

**Retention**:
- Daily: 7 days
- Weekly: 4 weeks
- Monthly: 12 months

### Code Backups
**Git**: All code in GitHub
- Private repository
- Branch protection on \`main\`
- Required PR reviews

**Disaster Recovery**:
1. Restore database from backup
2. Deploy previous working version (\`git revert\`)
3. Verify health checks pass
4. Notify users of downtime

---

## Security

### Secrets Management
**Never Commit**:
- API keys
- Database passwords
- JWT secrets
- OAuth client secrets

**Storage**:
- **Development**: \`.env.local\` (gitignored)
- **Production**: Vercel environment variables
- **Team**: 1Password/Vault

### SSL/TLS
- **Automatic**: Vercel provides free SSL
- **Renewal**: Automatic (Let's Encrypt)
- **Enforcement**: HTTPS redirect enabled

### Security Headers
\`\`\`typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin'
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-inline';"
          }
        ]
      }
    ];
  }
};
\`\`\`

---

## Performance Optimization

### Build Optimization
\`\`\`javascript
// next.config.js
module.exports = {
  output: 'standalone', // Smaller Docker images
  images: {
    domains: ['cdn.${appName.toLowerCase()}.com'],
    formats: ['image/avif', 'image/webp']
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  }
};
\`\`\`

### Caching Strategy
- **Static Assets**: CDN cached (1 year)
- **API Responses**: No cache (always fresh)
- **Pages**: ISR (Incremental Static Regeneration)

### CDN Configuration
**Vercel Edge Network**:
- 100+ locations globally
- Automatic cache invalidation
- Brotli compression

---

## Runbook

### Common Operations

#### Deploy New Version
\`\`\`bash
git checkout main
git pull origin main
git tag v1.0.1
git push --tags
# Vercel auto-deploys from main
\`\`\`

#### Rollback Deployment
\`\`\`bash
# Via Vercel CLI
vercel rollback

# Or redeploy previous commit
git checkout <previous-commit-sha>
vercel --prod
\`\`\`

#### Check Logs
\`\`\`bash
# Via Vercel CLI
vercel logs

# Or dashboard
open https://vercel.com/yourorg/${appName.toLowerCase()}/logs
\`\`\`

#### Database Connection Issues
\`\`\`bash
# Check database status
curl https://api.supabase.com/v1/projects/<project-id>/health

# Test connection
psql \$DATABASE_URL -c "SELECT 1"

# Restart database (Supabase dashboard)
\`\`\`

---

## Cost Estimate

### Vercel
- **Hobby**: $0/month (100GB bandwidth, 100 builds/day)
- **Pro**: $20/month (1TB bandwidth, unlimited builds)

### Supabase (If Backend)
- **Free**: $0/month (500MB database, 50K auth users)
- **Pro**: $25/month (8GB database, 100K auth users)

### Sentry
- **Developer**: $0/month (5K errors/month)
- **Team**: $26/month (50K errors/month)

### UptimeRobot
- **Free**: $0/month (50 monitors, 5-min checks)

**Total MVP Cost**: **$0/month**
**Total At Scale**: **~$50/month** (Pro tiers)

---

## References

**Deployment**:
- [Vercel Deployment](https://vercel.com/docs)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

**Monitoring**:
- [Sentry Documentation](https://docs.sentry.io/)
- [Web Vitals](https://web.dev/vitals/)

**PRD Cross-References**:
- See \`prd/03-acceptance-criteria.md\` for deployment requirements
- See \`architecture-tech-stack.md\` for infrastructure choices
`;
}

// ============================================================================
// GENERATE DOCUMENTS
// ============================================================================

console.log('📄 Generating API specification...');
const apiDoc = generateAPI(requirements);
fs.writeFileSync(path.join(outputDir, 'architecture-api.md'), apiDoc);
console.log('   ✅ architecture-api.md');

console.log('📄 Generating deployment documentation...');
const deploymentDoc = generateDeployment(requirements);
fs.writeFileSync(path.join(outputDir, 'architecture-deployment.md'), deploymentDoc);
console.log('   ✅ architecture-deployment.md');

console.log('\n✅ API & Deployment docs generated!');
console.log(`📂 Output: ${outputDir}/`);
console.log('\nArchitecture documentation complete (5/5):');
console.log('  ✅ architecture-tech-stack.md');
console.log('  ✅ architecture-services.md');
console.log('  ✅ architecture-data-model.md');
console.log('  ✅ architecture-api.md');
console.log('  ✅ architecture-deployment.md');

process.exit(0);
