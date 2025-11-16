# Deployment Architecture

## Overview

HydroTrack follows a **continuous deployment** strategy with automated testing and zero-downtime deployments.

**Platform**: Vercel (recommended)
**Alternative**: Netlify, Cloudflare Pages, or self-hosted

---

## Local Development Setup

### Prerequisites
```bash
# Required
node >= 18.0.0
npm >= 9.0.0

# Recommended
git >= 2.30.0
VS Code (with ESLint + Prettier extensions)
```

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourorg/hydrotrack.git
cd hydrotrack

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser
open http://localhost:3000
```

### Environment Variables
Create `.env.local`:
```bash
# App
NEXT_PUBLIC_APP_NAME="HydroTrack"
NEXT_PUBLIC_APP_URL="http://localhost:3000"

# Optional: If backend exists
# DATABASE_URL="postgresql://user:pass@localhost:5432/db"
# NEXTAUTH_SECRET="generate-with-openssl-rand-base64-32"
# NEXTAUTH_URL="http://localhost:3000"
```

**Generate Secrets**:
```bash
# NextAuth secret
openssl rand -base64 32

# API keys (store in 1Password/Vault)
openssl rand -hex 32
```

---

## Docker Development (Optional)

### Dockerfile
```dockerfile
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
```

### Docker Compose
```yaml
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
  #     POSTGRES_DB: hydrotrack
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data

# volumes:
#   postgres_data:
```

**Run**:
```bash
docker-compose up -d
```

---

## CI/CD Pipeline

### GitHub Actions Workflow
**File**: `.github/workflows/deploy.yml`

```yaml
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
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          scope: ${{ secrets.VERCEL_SCOPE }}

  deploy-production:
    runs-on: ubuntu-latest
    needs: visual-qa
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Vercel (Production)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          scope: ${{ secrets.VERCEL_SCOPE }}

      - name: Notify on success
        if: success()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"✅ HydroTrack deployed to production"}'

      - name: Notify on failure
        if: failure()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"❌ HydroTrack deployment failed"}'
```

---

## Vercel Deployment

### Setup
```bash
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
```

### Environment Variables (Vercel Dashboard)
Navigate to: **Project Settings → Environment Variables**

**Production**:
```
NEXT_PUBLIC_APP_NAME="HydroTrack"
NEXT_PUBLIC_APP_URL="https://hydrotrack.vercel.app"
# Add database/auth secrets if backend exists
```

**Preview**:
- Inherits production variables
- Override with preview-specific values if needed

### Custom Domain
**Settings → Domains**:
1. Add domain: `hydrotrack.com`
2. Configure DNS:
   ```
   CNAME @ cname.vercel-dns.com
   ```
3. Wait for SSL certificate (automatic)

---

## Monitoring & Observability

### Vercel Analytics
**Setup**:
```typescript
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
```

**Metrics Tracked**:
- Page views, unique visitors
- Core Web Vitals (LCP, FID, CLS)
- Device/browser distribution
- Geographic distribution

**Dashboard**: https://vercel.com/yourorg/hydrotrack/analytics

---

### Sentry Error Tracking
**Setup**:
```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

**Configuration**: `sentry.client.config.ts`
```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

**Alerts**:
- Slack webhook for critical errors
- Email for new error types
- Weekly digest

---

### Uptime Monitoring
**Service**: UptimeRobot (free tier)

**Monitors**:
1. **Homepage**: `https://hydrotrack.com`
   - Interval: 5 minutes
   - Alert: Email + Slack

2. **API Health**: `https://hydrotrack.com/api/healthz`
   - Interval: 5 minutes
   - Expected: 200 status

**Alerting**:
- Down for 2+ checks → Immediate alert
- Slow response (>3s) → Warning

---

## Database Migrations (If Backend Exists)

### Prisma Migrations
```bash
# Create migration
npx prisma migrate dev --name add_sync_fields

# Apply to production
npx prisma migrate deploy

# Generate client
npx prisma generate
```

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
```bash
# Dump database
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql

# Upload to S3
aws s3 cp backup-$(date +%Y%m%d).sql s3://backups/hydrotrack/
```

**Retention**:
- Daily: 7 days
- Weekly: 4 weeks
- Monthly: 12 months

### Code Backups
**Git**: All code in GitHub
- Private repository
- Branch protection on `main`
- Required PR reviews

**Disaster Recovery**:
1. Restore database from backup
2. Deploy previous working version (`git revert`)
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
- **Development**: `.env.local` (gitignored)
- **Production**: Vercel environment variables
- **Team**: 1Password/Vault

### SSL/TLS
- **Automatic**: Vercel provides free SSL
- **Renewal**: Automatic (Let's Encrypt)
- **Enforcement**: HTTPS redirect enabled

### Security Headers
```typescript
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
```

---

## Performance Optimization

### Build Optimization
```javascript
// next.config.js
module.exports = {
  output: 'standalone', // Smaller Docker images
  images: {
    domains: ['cdn.hydrotrack.com'],
    formats: ['image/avif', 'image/webp']
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  }
};
```

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
```bash
git checkout main
git pull origin main
git tag v1.0.1
git push --tags
# Vercel auto-deploys from main
```

#### Rollback Deployment
```bash
# Via Vercel CLI
vercel rollback

# Or redeploy previous commit
git checkout <previous-commit-sha>
vercel --prod
```

#### Check Logs
```bash
# Via Vercel CLI
vercel logs

# Or dashboard
open https://vercel.com/yourorg/hydrotrack/logs
```

#### Database Connection Issues
```bash
# Check database status
curl https://api.supabase.com/v1/projects/<project-id>/health

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Restart database (Supabase dashboard)
```

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
- See `prd/03-acceptance-criteria.md` for deployment requirements
- See `architecture-tech-stack.md` for infrastructure choices
