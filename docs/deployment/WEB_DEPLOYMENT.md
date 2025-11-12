# Web Deployment Guide
**Design-First Software Factory - Expo Universal App**

**Date**: 2025-11-12
**Status**: ✅ Web Support Configured
**Architecture**: Expo Frontend + Express Backend + Job Queue

---

## Overview

The Design-First Software Factory is a full-stack Expo application with:
- **Frontend**: Expo universal app (iOS/Android/Web)
- **Backend API**: Express server with WebSocket support
- **Job Queue**: BullMQ with Redis
- **AI Services**: OpenAI, Anthropic Claude, Google Gemini
- **Database**: Supabase PostgreSQL
- **Storage**: Supabase Storage

This guide covers deploying all components for web access.

---

## Architecture Components

### 1. Frontend (Expo Web)
- Project intake screens
- Design upload/iteration UI
- Real-time progress tracking
- Responsive design (phone → tablet → desktop)

### 2. Backend API (Express)
- RESTful endpoints for workflow management
- WebSocket server for real-time updates
- AI service orchestration
- Job queue management

### 3. Infrastructure
- **Redis**: Job queue and caching
- **Supabase**: Database, auth, storage
- **AI APIs**: OpenAI, Anthropic, Google Generative AI

---

## Prerequisites

### Required Accounts & Services

1. **Hosting Platform** (choose one):
   - Vercel (recommended for frontend)
   - Railway or Render (recommended for backend)
   - AWS or DigitalOcean (full control)

2. **Infrastructure**:
   - Redis instance (Upstash, Redis Cloud, or self-hosted)
   - Supabase project (https://supabase.com)

3. **AI Services**:
   - OpenAI API key (https://platform.openai.com)
   - Anthropic API key (https://console.anthropic.com)
   - Google AI API key (https://makersuite.google.com)

---

## Part 1: Frontend Deployment (Expo Web)

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run web
# Opens at http://localhost:19006
```

### Production Build

```bash
# Build for web
npx expo export:web

# Output in /web-build directory
ls -la web-build/
```

### Deploy to Vercel

**1. Install Vercel CLI**:
```bash
npm install -g vercel
```

**2. Create `vercel.json`**:

```json
{
  "version": 2,
  "name": "design-first-software-factory",
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "web-build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "EXPO_PUBLIC_API_URL": "@api_url",
    "EXPO_PUBLIC_SUPABASE_URL": "@supabase_url",
    "EXPO_PUBLIC_SUPABASE_ANON_KEY": "@supabase_anon_key",
    "EXPO_PUBLIC_WS_URL": "@ws_url"
  }
}
```

**3. Add build script** to `package.json`:
```json
{
  "scripts": {
    "build": "expo export:web"
  }
}
```

**4. Deploy**:
```bash
vercel --prod
```

**5. Configure Environment Variables**:
```bash
vercel env add EXPO_PUBLIC_API_URL production
# Enter: https://api.yourdomain.com

vercel env add EXPO_PUBLIC_SUPABASE_URL production
# Enter: https://your-project.supabase.co

vercel env add EXPO_PUBLIC_SUPABASE_ANON_KEY production
# Enter: your-anon-key

vercel env add EXPO_PUBLIC_WS_URL production
# Enter: wss://api.yourdomain.com
```

---

## Part 2: Backend API Deployment

The backend requires:
- Long-running Node.js process
- WebSocket support
- Redis connection
- AI API access

### Option A: Railway (Recommended)

**Why Railway?**
- Simple deployment from GitHub
- Built-in Redis
- WebSocket support
- Automatic HTTPS
- Free tier available

**Step-by-Step**:

1. **Create `railway.json`**:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm install && npm run build"
  },
  "deploy": {
    "startCommand": "npm run api",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. **Create Procfile**:

```
web: npm run api
```

3. **Deploy**:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add Redis service
railway add redis

# Deploy
railway up
```

4. **Configure Environment Variables** in Railway Dashboard:

```bash
# AI Services
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_AI_API_KEY=...

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key

# Redis (automatically provided by Railway)
REDIS_URL=redis://...

# App Config
NODE_ENV=production
PORT=3000
```

5. **Get your API URL**:
```bash
railway status
# Note the deployment URL: https://your-app.railway.app
```

---

### Option B: Render

**Step-by-Step**:

1. **Create `render.yaml`**:

```yaml
services:
  # Backend API
  - type: web
    name: factory-api
    env: node
    buildCommand: npm install
    startCommand: npm run api
    envVars:
      - key: NODE_ENV
        value: production
      - key: OPENAI_API_KEY
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: GOOGLE_AI_API_KEY
        sync: false
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_SERVICE_KEY
        sync: false
      - key: REDIS_URL
        fromService:
          type: redis
          name: factory-redis
          property: connectionString

  # Redis
  - type: redis
    name: factory-redis
    plan: starter
    maxmemoryPolicy: allkeys-lru
```

2. **Deploy**:
- Connect GitHub repository in Render dashboard
- Render auto-detects `render.yaml`
- Configure environment variables in dashboard
- Deploy

---

### Option C: AWS (ECS + Fargate)

**For production-scale deployments**:

1. **Create Dockerfile**:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "run", "api"]
```

2. **Deploy with AWS CDK** (example):

```typescript
import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as elasticache from 'aws-cdk-lib/aws-elasticache';

export class FactoryStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create ECS cluster
    const cluster = new ecs.Cluster(this, 'FactoryCluster', {
      vpc: vpc,
    });

    // Create Fargate service
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'FactoryTask');

    taskDefinition.addContainer('api', {
      image: ecs.ContainerImage.fromAsset('.'),
      memoryLimitMiB: 512,
      environment: {
        NODE_ENV: 'production',
        REDIS_URL: redis.attrRedisEndpointAddress,
      },
      secrets: {
        OPENAI_API_KEY: ecs.Secret.fromSecretsManager(openAiSecret),
        ANTHROPIC_API_KEY: ecs.Secret.fromSecretsManager(anthropicSecret),
      },
      logging: new ecs.AwsLogDriver({ streamPrefix: 'factory' }),
    });

    // Create service with load balancer
    new ecs.ApplicationLoadBalancedFargateService(this, 'FactoryService', {
      cluster,
      taskDefinition,
      publicLoadBalancer: true,
    });
  }
}
```

---

## Part 3: Redis Setup

### Option A: Upstash (Serverless Redis)

**Why Upstash?**
- Serverless (pay per request)
- Global edge caching
- Free tier: 10K requests/day
- Perfect for moderate traffic

**Setup**:

1. Create account at https://upstash.com
2. Create Redis database
3. Get REST URL and token
4. Add to environment variables:

```bash
REDIS_URL=redis://default:your-password@your-endpoint.upstash.io:6379
```

---

### Option B: Redis Cloud

**Why Redis Cloud?**
- Fully managed
- High availability
- Production-ready
- Free tier: 30MB

**Setup**:

1. Create account at https://redis.com/try-free
2. Create database
3. Get connection string
4. Add to environment:

```bash
REDIS_URL=redis://default:password@redis-12345.c123.us-east-1-1.ec2.cloud.redislabs.com:12345
```

---

### Option C: Self-Hosted (Docker)

**For development or full control**:

```yaml
# docker-compose.yml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

volumes:
  redis-data:
```

```bash
docker-compose up -d redis
```

---

## Part 4: Supabase Configuration

### Database Setup

1. **Run Migrations**:

```bash
# Link to production project
supabase link --project-ref your-production-ref

# Push migrations
supabase db push
```

2. **Configure Row Level Security (RLS)**:

The Factory needs RLS policies for:
- Projects table
- Workflows table
- Generated apps table
- Design iterations table

Example policy:
```sql
CREATE POLICY "Users can view their own projects"
  ON projects FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create projects"
  ON projects FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

3. **Deploy Edge Functions**:

```bash
cd supabase/functions

# Deploy all functions
supabase functions deploy project-intake
supabase functions deploy workflow-status
supabase functions deploy design-upload
```

4. **Configure Storage Buckets**:

```sql
-- Create buckets
INSERT INTO storage.buckets (id, name, public)
VALUES
  ('designs', 'designs', false),
  ('generated-apps', 'generated-apps', true),
  ('assets', 'assets', true);

-- Set up storage policies
CREATE POLICY "Users can upload designs"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (bucket_id = 'designs' AND auth.uid()::text = (storage.foldername(name))[1]);
```

### Environment Variables

Add to backend environment:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key  # NOT anon key!
```

---

## Part 5: AI Services Configuration

### OpenAI

```bash
# Get API key from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-...

# Optional: Specify model
OPENAI_MODEL=gpt-4-turbo-preview
```

### Anthropic Claude

```bash
# Get API key from https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional: Specify model
ANTHROPIC_MODEL=claude-3-5-sonnet-20250219
```

### Google Gemini

```bash
# Get API key from https://makersuite.google.com/app/apikey
GOOGLE_AI_API_KEY=AIza...

# Optional: Specify model
GOOGLE_AI_MODEL=gemini-pro
```

---

## Part 6: WebSocket Configuration

### CORS for WebSocket

Update backend `src/api/server.ts`:

```typescript
import cors from 'cors';
import { WebSocketServer } from 'ws';

const app = express();

// CORS configuration
const allowedOrigins = [
  'http://localhost:19006',  // Local development
  'https://factory.yourdomain.com',  // Production frontend
];

app.use(cors({
  origin: allowedOrigins,
  credentials: true,
}));

// WebSocket server
const wss = new WebSocketServer({
  server,
  path: '/ws',
  // Verify origin for WebSocket connections
  verifyClient: (info) => {
    const origin = info.origin;
    return allowedOrigins.includes(origin);
  },
});
```

### Frontend WebSocket Client

```typescript
// src/services/websocket.service.ts
const WS_URL = process.env.EXPO_PUBLIC_WS_URL || 'ws://localhost:3000/ws';

export function connectWebSocket() {
  const ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    console.log('WebSocket connected');
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // Handle progress updates
    handleProgressUpdate(data);
  };

  return ws;
}
```

---

## Part 7: Environment Variables Summary

### Frontend (.env for local, Vercel for prod)

```bash
# API endpoints
EXPO_PUBLIC_API_URL=https://api.yourdomain.com
EXPO_PUBLIC_WS_URL=wss://api.yourdomain.com

# Supabase (client-side)
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### Backend (.env for local, Railway/Render for prod)

```bash
# Server
NODE_ENV=production
PORT=3000

# Supabase (server-side)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key

# Redis
REDIS_URL=redis://...

# AI Services
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_AI_API_KEY=AIza...

# Optional: Model configuration
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-5-sonnet-20250219
GOOGLE_AI_MODEL=gemini-pro
```

---

## Part 8: Complete Deployment Workflow

### Step 1: Deploy Infrastructure

```bash
# 1. Create Supabase project
# 2. Create Redis instance (Upstash/Redis Cloud)
# 3. Note all connection strings
```

### Step 2: Configure Supabase

```bash
# Run migrations
supabase db push

# Deploy Edge Functions
cd supabase/functions
supabase functions deploy --no-verify-jwt

# Create storage buckets (via Supabase dashboard)
```

### Step 3: Deploy Backend API

```bash
# Using Railway
railway init
railway add redis
railway up

# Or using Render
# Push to GitHub, connect in Render dashboard

# Configure all environment variables
```

### Step 4: Deploy Frontend

```bash
# Build
npx expo export:web

# Deploy to Vercel
vercel --prod

# Configure environment variables pointing to backend
```

### Step 5: Verify Deployment

```bash
# Test API health
curl https://api.yourdomain.com/health

# Test WebSocket
wscat -c wss://api.yourdomain.com/ws

# Test frontend
open https://factory.yourdomain.com
```

---

## Part 9: Monitoring & Logging

### Backend Monitoring

**Railway/Render built-in**:
- View logs in dashboard
- Monitor CPU/memory usage
- Set up alerts

**Sentry for Error Tracking**:

```bash
npm install @sentry/node

# In src/api/server.ts
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: 'your-sentry-dsn',
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});

app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.errorHandler());
```

### Frontend Monitoring

```bash
npm install @sentry/react-native

# In App.tsx
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'your-sentry-dsn',
  enableNative: false, // Web doesn't need native SDK
});
```

### Redis Monitoring

**Upstash Dashboard**:
- Request count
- Latency metrics
- Memory usage

**Self-hosted**:
```bash
redis-cli INFO
redis-cli MONITOR
```

---

## Part 10: Scaling Considerations

### Horizontal Scaling

**Backend API**:
- Deploy multiple instances behind load balancer
- Use sticky sessions for WebSocket
- Share Redis connection across instances

**Job Queue**:
- Run multiple worker processes
- BullMQ automatically distributes jobs

### Vertical Scaling

**Railway/Render**:
- Upgrade to higher tier plans
- Increase memory/CPU allocation

**Redis**:
- Upgrade to Redis Cloud Pro tier
- Enable replication for high availability

### Cost Optimization

**Development**:
- Frontend: Vercel Hobby (Free)
- Backend: Railway Hobby ($5/month)
- Redis: Upstash Free tier
- Supabase: Free tier
- **Total: ~$5/month**

**Production (Small)**:
- Frontend: Vercel Pro ($20/month)
- Backend: Railway Pro ($20/month)
- Redis: Redis Cloud ($10/month)
- Supabase: Pro ($25/month)
- AI APIs: Pay-per-use (~$50-200/month depending on usage)
- **Total: ~$125-300/month**

---

## Part 11: Security Checklist

- [ ] **HTTPS enabled** on all services
- [ ] **Environment variables** stored securely (not in code)
- [ ] **API keys** use least-privilege access
- [ ] **CORS configured** with explicit origins (no wildcards)
- [ ] **Rate limiting** enabled on API endpoints
- [ ] **WebSocket** origin verification enabled
- [ ] **Supabase RLS** policies configured
- [ ] **Input validation** on all API endpoints
- [ ] **Error messages** don't leak sensitive info
- [ ] **Secrets rotation** process documented
- [ ] **Dependency scanning** enabled (Dependabot)
- [ ] **Security headers** configured (Helmet.js)

---

## Part 12: Troubleshooting

### Issue 1: WebSocket Connection Fails

**Symptom**: `WebSocket connection to 'wss://...' failed`

**Solutions**:
1. Check CORS origin includes frontend domain
2. Verify WebSocket path (`/ws`)
3. Check Railway/Render supports WebSocket (they do)
4. Ensure using `wss://` not `ws://` in production

### Issue 2: Redis Connection Timeout

**Symptom**: `Error: Redis connection timeout`

**Solutions**:
1. Check `REDIS_URL` is correct
2. Verify Redis instance is running
3. Check firewall rules allow connections
4. Test connection: `redis-cli -u $REDIS_URL ping`

### Issue 3: AI API Rate Limits

**Symptom**: `429 Too Many Requests`

**Solutions**:
1. Implement exponential backoff
2. Use job queue to throttle requests
3. Upgrade AI service tier
4. Cache frequent requests

### Issue 4: Build Fails on Vercel

**Symptom**: `Error: Command "expo export:web" failed`

**Solutions**:
1. Check Node.js version matches local (18+)
2. Verify all dependencies in package.json
3. Check build logs for specific errors
4. Test build locally: `npx expo export:web`

---

## Part 13: CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Factory

on:
  push:
    branches: [main]

jobs:
  # Deploy Backend
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up --service backend
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

  # Deploy Frontend
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npx expo export:web
        env:
          EXPO_PUBLIC_API_URL: ${{ secrets.API_URL }}
          EXPO_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          EXPO_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## Part 14: Deployment Checklist

### Pre-Deployment

- [ ] All environment variables documented
- [ ] Local build succeeds (`npm run build`)
- [ ] All tests passing (`npm test`)
- [ ] TypeScript compilation successful (`npm run type-check`)
- [ ] Supabase migrations tested
- [ ] Redis connection tested
- [ ] AI API keys validated
- [ ] WebSocket functionality tested locally

### Deployment

- [ ] Supabase project created and configured
- [ ] Redis instance provisioned
- [ ] Backend deployed with all env vars
- [ ] Backend health check passing
- [ ] Frontend deployed with backend URL
- [ ] Frontend loads in browser
- [ ] WebSocket connection established
- [ ] Job queue processing jobs
- [ ] AI services responding

### Post-Deployment

- [ ] Monitor error rates (Sentry)
- [ ] Check API response times
- [ ] Verify WebSocket stability
- [ ] Test end-to-end workflow
- [ ] Configure custom domains
- [ ] Set up SSL certificates
- [ ] Enable monitoring alerts
- [ ] Document deployment process
- [ ] Train team on deployment

---

## Summary

You now have a complete guide for deploying the Design-First Software Factory to production:

1. ✅ **Frontend**: Deployed to Vercel (Expo Web)
2. ✅ **Backend**: Deployed to Railway/Render (Express + WebSocket)
3. ✅ **Redis**: Provisioned with Upstash/Redis Cloud
4. ✅ **Supabase**: Configured with migrations and Edge Functions
5. ✅ **AI Services**: Integrated with secure API keys
6. ✅ **Monitoring**: Sentry for errors, platform dashboards for metrics
7. ✅ **CI/CD**: GitHub Actions for automated deployments

**Next Steps**:
1. Choose hosting providers
2. Provision infrastructure (Redis, Supabase)
3. Deploy backend first, then frontend
4. Verify all services communicating
5. Test end-to-end workflows
6. Set up monitoring and alerts
7. Document for your team

---

**Last Updated**: 2025-11-12
**Branch**: `claude/design-first-implementation-011CUqTznbQhS98PNjB294jR`
**Status**: ✅ Production Deployment Ready
