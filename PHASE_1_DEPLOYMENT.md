# Phase 1 Deployment Guide
**Design-First Software Factory - Infrastructure & Backend**

**Date Started**: 2025-11-12
**Status**: 🚀 IN PROGRESS
**Goal**: Deploy Factory backend infrastructure so it's ready for Admin Console integration

---

## Overview

Phase 1 deploys the **core Factory infrastructure** that the Admin Console will depend on:
- ✅ Supabase database and Edge Functions
- ✅ Redis for job queue
- ✅ Express backend API with WebSocket
- ✅ AI service integration

**Timeline**: Week 1 (5-7 days)

---

## Prerequisites Checklist

Before starting, you need:

### Accounts
- [ ] Supabase account (https://supabase.com - free tier OK for dev)
- [ ] Redis provider account (Upstash or Redis Cloud - free tier OK)
- [ ] Railway account (https://railway.app - $5/month hobby tier)
  - OR Render account (https://render.com - free tier)
- [ ] Vercel account (https://vercel.com - free tier OK)

### API Keys
- [ ] OpenAI API key (https://platform.openai.com/api-keys)
- [ ] Anthropic API key (https://console.anthropic.com/)
- [ ] Google AI API key (https://makersuite.google.com/app/apikey)

### Development Tools
- [ ] Supabase CLI installed (`npm install -g supabase`)
- [ ] Railway CLI installed (`npm install -g @railway/cli`)
- [ ] Node.js 18+ installed
- [ ] Git access to repository

---

## Step 1: Supabase Production Project Setup

### 1.1 Create Supabase Project

```bash
# Go to https://supabase.com/dashboard
# Click "New Project"
# Fill in:
#   - Name: design-first-factory-prod
#   - Database Password: [Generate strong password - SAVE THIS]
#   - Region: Choose closest to your users
#   - Pricing Plan: Free (upgrade later if needed)

# Wait 2-3 minutes for project to be ready
```

### 1.2 Note Your Project Credentials

```bash
# From Supabase Dashboard → Settings → API
# Copy these values:

SUPABASE_URL=https://[your-project-ref].supabase.co
SUPABASE_ANON_KEY=[public-anon-key]
SUPABASE_SERVICE_KEY=[secret-service-role-key]  # Keep this secret!
```

### 1.3 Link Supabase CLI to Project

```bash
# In your local repository
cd /home/user/agents

# Login to Supabase
supabase login

# Link to your production project
supabase link --project-ref [your-project-ref]

# You'll be prompted for the database password you created
```

### 1.4 Push Database Migrations

```bash
# Check what migrations exist
ls -la supabase/migrations/

# Push all migrations to production
supabase db push

# Expected output:
# Applying migration 001_initial_schema.sql...
# Applying migration 002_projects_table.sql...
# Applying migration 003_security_improvements.sql...
# ✓ All migrations applied successfully
```

### 1.5 Verify Database Schema

```bash
# Connect to database
supabase db reset --linked

# Or check in Supabase Dashboard → Table Editor
# Should see tables:
# - customers
# - projects
# - project_notes
# - workflows
# - generated_apps
# - audit_log
```

### 1.6 Configure Storage Buckets

In Supabase Dashboard → Storage:

```sql
-- Create buckets
INSERT INTO storage.buckets (id, name, public)
VALUES
  ('designs', 'designs', false),
  ('generated-apps', 'generated-apps', true),
  ('assets', 'assets', true);

-- Storage policies
CREATE POLICY "Authenticated users can upload designs"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (
    bucket_id = 'designs' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can read their own designs"
  ON storage.objects FOR SELECT
  TO authenticated
  USING (
    bucket_id = 'designs' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Anyone can read generated apps"
  ON storage.objects FOR SELECT
  TO public
  USING (bucket_id = 'generated-apps');
```

### 1.7 Deploy Edge Functions

```bash
cd supabase/functions

# Deploy each Edge Function
supabase functions deploy project-intake --no-verify-jwt
supabase functions deploy workflow-status --no-verify-jwt
supabase functions deploy design-upload --no-verify-jwt

# If functions don't exist yet, we'll create them in the next step
```

**Status**: ✅ Step 1 Complete
**Time**: ~30 minutes

---

## Step 2: Redis Provisioning

### Option A: Upstash (Recommended for Serverless)

**Why Upstash?**
- Serverless (pay per request)
- Free tier: 10K requests/day
- Global edge caching
- Perfect for development

**Setup**:

```bash
# 1. Go to https://console.upstash.com/
# 2. Create account
# 3. Click "Create Database"
# 4. Choose:
#    - Name: factory-redis-prod
#    - Type: Regional
#    - Region: Same as Supabase
#    - Primary Region: True
#    - Eviction: True (allkeys-lru)

# 5. Get connection details from dashboard
# Copy these values:

REDIS_URL=redis://default:[password]@[endpoint].upstash.io:6379
UPSTASH_REDIS_REST_URL=https://[endpoint].upstash.io
UPSTASH_REDIS_REST_TOKEN=[token]
```

**Test Connection**:

```bash
# Install redis-cli
brew install redis  # Mac
# or
sudo apt-get install redis-tools  # Linux

# Test connection
redis-cli -u $REDIS_URL ping
# Expected: PONG
```

### Option B: Redis Cloud

**Why Redis Cloud?**
- Fully managed
- Free tier: 30MB storage
- High availability
- Production-ready

**Setup**:

```bash
# 1. Go to https://redis.com/try-free/
# 2. Create account
# 3. Create subscription:
#    - Cloud: AWS (or GCP/Azure)
#    - Region: Same as Supabase
#    - Plan: Free 30MB

# 4. Create database:
#    - Name: factory-prod
#    - Port: 12000 (or auto)
#    - Password: [auto-generated]

# 5. Copy connection string
REDIS_URL=redis://default:[password]@redis-12345.c123.us-east-1-1.ec2.cloud.redislabs.com:12345
```

**Status**: ✅ Step 2 Complete
**Time**: ~15 minutes

---

## Step 3: Prepare Backend for Deployment

### 3.1 Review Backend Configuration

```bash
cd /home/user/agents

# Check backend server exists
ls -la src/api/server.ts

# Check dependencies
cat package.json | grep -A 20 '"dependencies"'
```

### 3.2 Create Production Environment Template

Create `.env.production.template`:

```bash
# === Factory Backend Production Environment ===

# Server Configuration
NODE_ENV=production
PORT=3000

# Supabase (Backend - use SERVICE KEY)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key

# Redis (Job Queue)
REDIS_URL=redis://default:password@endpoint:6379

# AI Services
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_AI_API_KEY=AIza...

# Optional: Model Configuration
OPENAI_MODEL=gpt-4-turbo-preview
ANTHROPIC_MODEL=claude-3-5-sonnet-20250219
GOOGLE_AI_MODEL=gemini-pro

# Optional: Job Queue Configuration
BULL_CONCURRENCY=5
BULL_MAX_RETRIES=3

# Optional: CORS Origins (update after deploying frontend)
ALLOWED_ORIGINS=http://localhost:19006,https://factory.yourdomain.com
```

### 3.3 Add Health Check Endpoint

Check if health endpoint exists in `src/api/server.ts`:

```typescript
// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    services: {
      database: 'connected',  // Test Supabase connection
      redis: 'connected',     // Test Redis connection
      version: process.env.npm_package_version || '0.1.0',
    },
  });
});
```

**Status**: ✅ Step 3 Complete
**Time**: ~10 minutes

---

## Step 4: Deploy Backend to Railway

### 4.1 Install Railway CLI

```bash
npm install -g @railway/cli

# Login
railway login
# Opens browser for authentication
```

### 4.2 Create Railway Project

```bash
cd /home/user/agents

# Initialize Railway project
railway init

# Choose:
# - Project name: design-first-factory
# - Start from: Empty project
```

### 4.3 Add Redis Service (Optional if using Upstash)

```bash
# Add Redis to Railway
railway add redis

# Railway provides REDIS_URL automatically
# No need to configure if using Railway Redis
```

### 4.4 Configure Environment Variables

```bash
# Set all environment variables
railway variables set NODE_ENV=production
railway variables set PORT=3000

railway variables set SUPABASE_URL=https://your-project.supabase.co
railway variables set SUPABASE_SERVICE_KEY=your-service-role-key

# If using Upstash (external Redis):
railway variables set REDIS_URL=redis://default:password@endpoint.upstash.io:6379

railway variables set OPENAI_API_KEY=sk-proj-...
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set GOOGLE_AI_API_KEY=AIza...
```

### 4.5 Create Railway Configuration

Create `railway.json`:

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

### 4.6 Deploy to Railway

```bash
# Deploy
railway up

# Expected output:
# Building...
# Deploying...
# ✓ Deployment successful
# URL: https://design-first-factory-production.up.railway.app

# Save this URL!
FACTORY_API_URL=https://design-first-factory-production.up.railway.app
```

### 4.7 Verify Deployment

```bash
# Test health endpoint
curl https://design-first-factory-production.up.railway.app/health

# Expected response:
# {
#   "status": "ok",
#   "timestamp": "2025-11-12T...",
#   "services": {
#     "database": "connected",
#     "redis": "connected",
#     "version": "0.1.0"
#   }
# }

# Check logs
railway logs

# Should see:
# Server listening on port 3000
# Redis connected
# Supabase connected
```

**Status**: ✅ Step 4 Complete
**Time**: ~20 minutes

---

## Step 5: Test Backend Services

### 5.1 Test WebSocket Connection

```bash
# Install wscat
npm install -g wscat

# Connect to WebSocket
wscat -c wss://design-first-factory-production.up.railway.app/ws

# Should connect successfully
# Type: {"type": "ping"}
# Should receive: {"type": "pong"}
```

### 5.2 Test Job Queue

Create test script `test-job-queue.js`:

```javascript
const { Queue } = require('bullmq');

const connection = {
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  password: process.env.REDIS_PASSWORD,
};

const testQueue = new Queue('workflow-queue', { connection });

async function testJobQueue() {
  // Add test job
  const job = await testQueue.add('test-workflow', {
    projectId: 'test-123',
    tier: 'express',
  });

  console.log('Job added:', job.id);

  // Wait for completion
  const result = await job.waitUntilFinished();
  console.log('Job completed:', result);
}

testJobQueue().catch(console.error);
```

```bash
node test-job-queue.js
```

### 5.3 Test AI Services Integration

```bash
# Test OpenAI connection
curl https://design-first-factory-production.up.railway.app/api/test/openai

# Test Anthropic connection
curl https://design-first-factory-production.up.railway.app/api/test/anthropic

# Test Gemini connection
curl https://design-first-factory-production.up.railway.app/api/test/gemini
```

**Status**: ✅ Step 5 Complete
**Time**: ~15 minutes

---

## Step 6: Deploy Factory Frontend

### 6.1 Configure Frontend Environment

Create `.env.production` in project root:

```bash
# Factory Frontend Production Environment

# Backend API
EXPO_PUBLIC_API_URL=https://design-first-factory-production.up.railway.app
EXPO_PUBLIC_WS_URL=wss://design-first-factory-production.up.railway.app

# Supabase (Frontend - use ANON KEY)
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 6.2 Build for Web

```bash
cd /home/user/agents

# Install dependencies
npm install

# Build for web
npx expo export:web

# Verify build
ls -la web-build/
# Should see: index.html, static/, manifest.json
```

### 6.3 Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod

# When prompted:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name: design-first-factory
# - Directory: ./
# - Override settings? No

# Note deployment URL
FACTORY_FRONTEND_URL=https://design-first-factory.vercel.app
```

### 6.4 Configure Environment Variables in Vercel

```bash
# Add environment variables
vercel env add EXPO_PUBLIC_API_URL production
# Enter: https://design-first-factory-production.up.railway.app

vercel env add EXPO_PUBLIC_WS_URL production
# Enter: wss://design-first-factory-production.up.railway.app

vercel env add EXPO_PUBLIC_SUPABASE_URL production
# Enter: https://your-project.supabase.co

vercel env add EXPO_PUBLIC_SUPABASE_ANON_KEY production
# Enter: your-anon-key

# Redeploy with new env vars
vercel --prod
```

### 6.5 Update Backend CORS

Update backend environment on Railway:

```bash
railway variables set ALLOWED_ORIGINS=https://design-first-factory.vercel.app

# Redeploy
railway up
```

**Status**: ✅ Step 6 Complete
**Time**: ~20 minutes

---

## Step 7: End-to-End Testing

### 7.1 Test Frontend Loads

```bash
# Open in browser
open https://design-first-factory.vercel.app

# Should see:
# - Factory UI loads
# - No CORS errors in console
# - WebSocket connects
```

### 7.2 Test Workflow Submission

```bash
# In browser console:
# Navigate to Project Intake screen
# Fill out form:
#   - Project name: Test Project
#   - Description: Testing Phase 1 deployment
#   - Tier: Express

# Click "Start Generation"
# Should see:
#   - Progress indicators
#   - Real-time updates via WebSocket
#   - Job processing in queue
```

### 7.3 Monitor Backend Logs

```bash
# Watch Railway logs
railway logs --tail

# Should see:
# - Workflow started
# - PRD generation in progress
# - AI service calls
# - Job queue updates
```

### 7.4 Verify Database Records

```bash
# Check Supabase Table Editor
# workflows table should have new record with status 'in_progress'

# Or query via CLI:
supabase db --linked --execute "SELECT * FROM workflows ORDER BY created_at DESC LIMIT 1;"
```

**Status**: ✅ Step 7 Complete
**Time**: ~30 minutes

---

## Phase 1 Completion Checklist

### Infrastructure
- [ ] Supabase project created and configured
- [ ] Database migrations applied successfully
- [ ] Storage buckets created with policies
- [ ] Edge Functions deployed
- [ ] Redis instance provisioned and tested

### Backend
- [ ] Express backend deployed to Railway
- [ ] All environment variables configured
- [ ] Health endpoint responding
- [ ] WebSocket server operational
- [ ] Job queue processing jobs
- [ ] AI services integrated and tested

### Frontend
- [ ] Factory Expo Web built successfully
- [ ] Deployed to Vercel
- [ ] Environment variables configured
- [ ] CORS configured correctly
- [ ] Frontend communicates with backend

### Testing
- [ ] Health check passes
- [ ] WebSocket connection established
- [ ] Job queue accepts and processes jobs
- [ ] End-to-end workflow test successful
- [ ] Database records created correctly
- [ ] Logs show no critical errors

---

## Next Steps

**Phase 1 Complete?** ✅

**Proceed to Phase 2**: Deploy Admin Console
1. Configure Admin Console with Factory API URL
2. Deploy Admin Console to Vercel
3. Test "Generate App" integration

---

## Troubleshooting

### Issue: Database migrations fail

**Solution**:
```bash
# Reset and try again
supabase db reset --linked
supabase db push
```

### Issue: Redis connection timeout

**Solution**:
```bash
# Test Redis locally
redis-cli -u $REDIS_URL ping

# Check firewall rules
# Verify REDIS_URL is correct
```

### Issue: Railway deployment fails

**Solution**:
```bash
# Check logs
railway logs

# Common issues:
# - Missing dependencies in package.json
# - Node version mismatch
# - Build script errors

# Fix and redeploy
railway up --force
```

### Issue: CORS errors on frontend

**Solution**:
```bash
# Update ALLOWED_ORIGINS on Railway
railway variables set ALLOWED_ORIGINS=https://your-vercel-domain.vercel.app

# Redeploy
railway up
```

---

## Cost Summary (Development)

- **Supabase**: Free tier (500MB database, 1GB bandwidth)
- **Redis (Upstash)**: Free tier (10K requests/day)
- **Railway**: $5/month (Hobby plan)
- **Vercel**: Free tier (100GB bandwidth)
- **AI APIs**: Pay-per-use (~$50-200/month depending on usage)

**Total**: ~$55-205/month for development

---

**Last Updated**: 2025-11-12
**Status**: 🚀 Phase 1 Deployment In Progress
**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`
