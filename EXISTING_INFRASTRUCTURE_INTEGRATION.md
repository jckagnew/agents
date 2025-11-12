# Existing Infrastructure Integration Guide
**Design-First Software Factory**

**Date**: 2025-11-12
**Status**: ✅ Ready to Integrate
**Existing Project**: `design-factory-admin`

---

## Critical Discovery

🎯 **We are NOT creating new infrastructure** - we're integrating with existing Supabase project!

**Existing Supabase Project**: `design-factory-admin`
- **Region**: us-east-1
- **URL**: https://design-factory-admin.supabase.co
- **Dashboard**: https://supabase.com/dashboard/project/design-factory-admin

---

## What Already Exists

### ✅ Database Schema (Complete)

**Location**: `design-first-software-factory/supabase/migrations/001_core_schema.sql`

**Tables**:
1. **admin_users**
   - Roles: owner, manager, support
   - Fields: id, email, role, created_at

2. **customers**
   - Tiers: starter, growth, enterprise
   - Fields: id, name, email, tier, created_at, admin_user_id

3. **projects**
   - Status: intake, in_review, in_progress, awaiting_client, delivered, archived
   - Fields: id, name, description, status, customer_id, created_at

4. **project_notes**
   - Author types: admin, customer
   - Fields: id, project_id, content, author_type, author_id, created_at

5. **invoices**
   - Status: draft, sent, partial, paid, void
   - Fields: id, customer_id, amount, status, due_date, created_at

### ✅ Storage Buckets

1. **designs** (private)
   - Design files uploaded by admins
   - Access: Admin users only

2. **deliverables** (public)
   - Final deliverables for customers
   - Access: Public (with signed URLs)

3. **avatars** (public)
   - User profile images
   - Access: Public

### ✅ Edge Functions

**Location**: `design-first-software-factory/supabase/functions/`

1. **admin-customers**
   - CRUD operations for customers
   - Endpoint: `/functions/v1/admin-customers`

2. **admin-projects**
   - CRUD operations for projects
   - Endpoint: `/functions/v1/admin-projects`

3. **upload-design**
   - Design file uploads to storage
   - Endpoint: `/functions/v1/upload-design`

4. **stripe-webhook**
   - Stripe payment webhooks
   - Endpoint: `/functions/v1/stripe-webhook`

**API Base URL**: https://design-factory-admin.supabase.co/functions/v1

---

## Integration Steps

### Step 1: Get Credentials ✅

```bash
# Go to Supabase Dashboard
https://supabase.com/dashboard/project/design-factory-admin

# Navigate to: Settings → API
# Copy:
# - Project URL: https://design-factory-admin.supabase.co
# - Anon key (public)
# - Service role key (secret)
```

### Step 2: Update Environment Files ✅

File: `/home/user/agents/.env.example` (already updated!)

```bash
# Supabase (EXISTING PROJECT)
SUPABASE_URL=https://design-factory-admin.supabase.co
EXPO_PUBLIC_SUPABASE_URL=https://design-factory-admin.supabase.co

SUPABASE_ANON_KEY=your-anon-key-here
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here

SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

### Step 3: Link Supabase CLI ⏳

```bash
cd /home/user/agents

# Login (if not already)
supabase login

# Link to EXISTING project
supabase link --project-ref design-factory-admin

# Verify link
supabase status
# Should show: Linked to project design-factory-admin
```

### Step 4: Deploy/Update Edge Functions ⏳

```bash
cd supabase/functions

# Deploy each function
supabase functions deploy admin-customers --no-verify-jwt
supabase functions deploy admin-projects --no-verify-jwt
supabase functions deploy upload-design --no-verify-jwt
supabase functions deploy stripe-webhook --no-verify-jwt
```

### Step 5: Verify Database Schema ⏳

```bash
# Check for schema differences
supabase db diff

# Expected output:
# "No schema changes detected"
# (because schema already exists!)
```

### Step 6: Test Edge Functions ⏳

```bash
# Test admin-customers endpoint
curl https://design-factory-admin.supabase.co/functions/v1/admin-customers \
  -H "Authorization: Bearer YOUR_ANON_KEY"

# Should return customers list or 401 if auth required
```

---

## What NOT to Do

❌ **DO NOT**:
1. Create a new Supabase project
2. Run database migrations (schema exists!)
3. Create storage buckets (they exist!)
4. Delete or modify existing Edge Functions without testing

✅ **DO**:
1. Link to existing `design-factory-admin` project
2. Update/deploy existing Edge Functions
3. Use existing database schema
4. Add new features incrementally

---

## Deployment Checklist

### Infrastructure (Existing - Just Link)
- [ ] Get Supabase credentials from `design-factory-admin`
- [ ] Link Supabase CLI: `supabase link --project-ref design-factory-admin`
- [ ] Verify database schema: `supabase db diff`
- [ ] Update/deploy Edge Functions
- [ ] Test Edge Function endpoints

### New Components (Need to Deploy)
- [ ] Provision Redis (Upstash/Redis Cloud/Railway)
- [ ] Get AI API keys (OpenAI, Anthropic, Google)
- [ ] Deploy Express backend to Railway/Render
- [ ] Deploy Expo frontend to Vercel
- [ ] Configure environment variables
- [ ] Test end-to-end workflow

---

## Environment Variable Reference

### Backend (.env for Railway/Render)

```bash
# Existing Supabase
SUPABASE_URL=https://design-factory-admin.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# New Infrastructure
REDIS_URL=redis://...
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_AI_API_KEY=AIza...

# Backend Config
NODE_ENV=production
PORT=3000
ALLOWED_ORIGINS=https://factory.yourdomain.com
```

### Frontend (.env for Vercel)

```bash
# Existing Supabase (PUBLIC keys)
EXPO_PUBLIC_SUPABASE_URL=https://design-factory-admin.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Backend API (after deploying)
EXPO_PUBLIC_API_URL=https://factory-api.up.railway.app
EXPO_PUBLIC_WS_URL=wss://factory-api.up.railway.app
```

---

## Benefits of Using Existing Infrastructure

✅ **Faster Setup**
- No waiting for new project provisioning
- Database schema already exists
- Storage buckets configured

✅ **Data Continuity**
- Existing customer data preserved
- No migration required
- Historical data intact

✅ **Cost Efficiency**
- Single Supabase project
- Shared resources
- No duplicate infrastructure

✅ **Simplified Management**
- One dashboard to manage
- Centralized monitoring
- Unified backup strategy

---

## Next Steps

**Immediate**:
1. Get Supabase credentials from project owner
2. Link Supabase CLI to `design-factory-admin`
3. Deploy/update Edge Functions
4. Follow updated PHASE_1_DEPLOYMENT.md

**After Phase 1**:
1. Deploy Express backend to Railway
2. Deploy Expo frontend to Vercel
3. Integrate Admin Console with Factory API
4. Test end-to-end workflows

---

## Support & Documentation

**Existing Project Docs**:
- API Reference: `design-first-software-factory/docs/admin-console/API_REFERENCE.md`
- Database Schema: `design-first-software-factory/supabase/migrations/001_core_schema.sql`
- Integration Guide: Created by Cursor (see CLAUDE_INTEGRATION_GUIDE.md)

**New Documentation**:
- PHASE_1_DEPLOYMENT.md (updated for existing infrastructure)
- WEB_DEPLOYMENT.md (comprehensive deployment guide)
- INTEGRATION_ROADMAP.md (overall integration strategy)

---

**Last Updated**: 2025-11-12
**Status**: ✅ Ready for Phase 1 Deployment with Existing Infrastructure
**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`
