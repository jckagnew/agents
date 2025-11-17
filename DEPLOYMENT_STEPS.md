# 🚀 Deployment Steps for Security Fixes

This guide walks you through deploying the security fixes to your Supabase production project.

## Prerequisites

1. ✅ Supabase CLI installed (`brew install supabase/tap/supabase`)
2. ✅ Linked to your Supabase project (`design-factory-admin`)
3. ✅ Environment variables configured in `.env`
4. ✅ Docker running (for local testing, optional for production)

## Step 1: Fix Config File

The `supabase/config.toml` has been fixed (experimental section commented out).

## Step 2: Link to Supabase Project

If not already linked, you need to link to your remote project:

```bash
# Get your project reference ID from:
# https://supabase.com/dashboard/project/design-factory-admin/settings/general
# Look for "Reference ID"

supabase link --project-ref YOUR_PROJECT_REF
```

**Note**: The project reference is NOT "design-factory-admin" - it's a 20-character alphanumeric string.

## Step 3: Check for Missing Shared Files

The Edge Functions reference `_shared/cors.ts`, `_shared/auth.ts`, etc. These files need to exist.

**Check if they exist:**
```bash
ls -la supabase/functions/_shared/
```

**If missing**, you'll need to create them or they may be in a different location. Check the actual Edge Function files to see what they import.

## Step 4: Run Database Migration

Deploy the atomic quota updates migration:

```bash
cd /Users/jackagnew/projects/jckagnew-agents
supabase db push
```

This will apply `008_atomic_quota_updates.sql` which fixes race conditions in quota updates.

## Step 5: Deploy Edge Functions

Deploy the updated Edge Functions with security fixes:

```bash
# Deploy admin-customers (SQL injection fixes)
supabase functions deploy admin-customers

# Deploy admin-projects (Security hardening)
supabase functions deploy admin-projects
```

**If you get errors about missing `_shared` files**, you may need to:
1. Create the `_shared` directory
2. Add the required shared utilities (cors.ts, auth.ts, validation.ts, rate-limit.ts)
3. Or check if they're imported from a different location

## Step 6: Configure Production CORS

### Option A: Via Supabase Dashboard (Recommended)

1. Go to: https://supabase.com/dashboard/project/design-factory-admin/settings/api
2. Under **CORS Configuration**, add your production domains:
   - Your admin console domain (e.g., `https://admin.yourdomain.com`)
   - Your factory app domain (e.g., `https://factory.yourdomain.com`)
   - Local development: `http://localhost:19006`

### Option B: Via Environment Variables

Set `ALLOWED_ORIGINS` in your Edge Function environment variables:

```bash
supabase secrets set ALLOWED_ORIGINS="https://admin.yourdomain.com,https://factory.yourdomain.com"
```

Or set it in the Supabase Dashboard:
- Go to: Project Settings > Edge Functions > Environment Variables
- Add: `ALLOWED_ORIGINS` = `https://admin.yourdomain.com,https://factory.yourdomain.com`

## Step 7: Verify Deployment

### Check Migration Status

```bash
supabase db remote list
```

You should see `008_atomic_quota_updates.sql` in the list.

### Test Edge Functions

Test the endpoints to ensure they're working:

```bash
# Test admin-customers endpoint
curl -X GET https://YOUR_PROJECT_REF.supabase.co/functions/v1/admin-customers \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Origin: https://yourdomain.com"

# Test admin-projects endpoint  
curl -X GET https://YOUR_PROJECT_REF.supabase.co/functions/v1/admin-projects \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Origin: https://yourdomain.com"
```

### Check CORS Headers

Verify CORS headers are present in responses:

```bash
curl -I -X OPTIONS https://YOUR_PROJECT_REF.supabase.co/functions/v1/admin-customers \
  -H "Origin: https://yourdomain.com" \
  -H "Access-Control-Request-Method: GET"
```

You should see:
- `Access-Control-Allow-Origin: https://yourdomain.com`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Authorization, Content-Type`

## Troubleshooting

### "Failed to link project"

- Make sure you're using the correct project reference ID (20 characters)
- Check that you have access to the project
- Verify your Supabase CLI is authenticated: `supabase login`

### "Missing _shared files"

The Edge Functions import from `../_shared/` but these files may not exist. Options:

1. **Check if they're in a different location:**
   ```bash
   find supabase -name "cors.ts" -o -name "auth.ts"
   ```

2. **Create the shared directory and files** (if they're missing from the merge)

3. **Check the actual imports** in the Edge Function files to see what's needed

### "Docker not running"

For local development, Docker needs to be running. For production deployment, Docker is not required.

### "Migration already applied"

If you see "Migration already applied", that's fine - it means the migration was already run.

## Quick Deployment Script

You can also use the automated script:

```bash
bash scripts/deploy-security-fixes.sh
```

This script will:
- Check prerequisites
- Prompt for confirmation at each step
- Deploy migrations
- Deploy Edge Functions
- Provide CORS configuration instructions

## Summary

✅ **Config fixed** - `supabase/config.toml` experimental section commented out  
⏳ **Link project** - `supabase link --project-ref YOUR_PROJECT_REF`  
⏳ **Push migration** - `supabase db push`  
⏳ **Deploy functions** - `supabase functions deploy admin-customers admin-projects`  
⏳ **Configure CORS** - Via Dashboard or environment variables  

---

**Status**: Ready for deployment  
**Next**: Link to project and run migrations

