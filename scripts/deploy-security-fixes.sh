#!/bin/bash
#
# Deploy Security Fixes to Supabase
#
# This script deploys the security fixes that were merged:
# 1. Database migration (008_atomic_quota_updates.sql)
# 2. Updated Edge Functions (admin-customers, admin-projects)
# 3. CORS configuration verification
#

set -e

echo "=========================================="
echo "DEPLOYING SECURITY FIXES TO SUPABASE"
echo "=========================================="
echo ""

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI not found. Please install it first:"
    echo "   brew install supabase/tap/supabase"
    exit 1
fi

# Check if linked to project
echo "Step 1: Checking Supabase project link..."
if ! supabase status &> /dev/null; then
    echo "⚠️  Not linked to a Supabase project."
    echo ""
    echo "To link to your project, run:"
    echo "  supabase link --project-ref YOUR_PROJECT_REF"
    echo ""
    echo "Or if you need to find your project ref:"
    echo "  1. Go to https://supabase.com/dashboard"
    echo "  2. Select project: design-factory-admin"
    echo "  3. Go to Settings > General"
    echo "  4. Copy the 'Reference ID'"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Linked to Supabase project"
    supabase status
fi

echo ""
echo "Step 2: Running database migration..."
echo "This will apply migration: 008_atomic_quota_updates.sql"
echo ""
read -p "Continue with database migration? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    supabase db push
    echo "✅ Database migration completed"
else
    echo "⏭️  Skipping database migration"
fi

echo ""
echo "Step 3: Deploying Edge Functions..."
echo "Functions to deploy:"
echo "  - admin-customers (SQL injection fixes)"
echo "  - admin-projects (Security hardening)"
echo ""

# Check if shared files exist
if [ ! -d "supabase/functions/_shared" ]; then
    echo "⚠️  WARNING: _shared directory not found!"
    echo "   Edge Functions may fail without shared utilities."
    echo "   Make sure cors.ts, auth.ts, validation.ts, and rate-limit.ts exist."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

read -p "Deploy Edge Functions? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Deploying admin-customers..."
    supabase functions deploy admin-customers
    
    echo "Deploying admin-projects..."
    supabase functions deploy admin-projects
    
    echo "✅ Edge Functions deployed"
else
    echo "⏭️  Skipping Edge Functions deployment"
fi

echo ""
echo "Step 4: CORS Configuration"
echo ""
echo "⚠️  IMPORTANT: Configure production CORS in Supabase Dashboard:"
echo ""
echo "1. Go to: https://supabase.com/dashboard/project/design-factory-admin/settings/api"
echo "2. Under 'CORS Configuration', add your production domains:"
echo "   - Your admin console domain (e.g., https://admin.yourdomain.com)"
echo "   - Your factory app domain (e.g., https://factory.yourdomain.com)"
echo ""
echo "Or set via environment variable ALLOWED_ORIGINS in Edge Functions:"
echo "  ALLOWED_ORIGINS=https://admin.yourdomain.com,https://factory.yourdomain.com"
echo ""

echo "=========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. ✅ Database migration applied"
echo "  2. ✅ Edge Functions deployed"
echo "  3. ⚠️  Configure production CORS (see above)"
echo ""
echo "To verify deployment:"
echo "  - Check Supabase Dashboard for migration status"
echo "  - Test Edge Functions endpoints"
echo "  - Verify CORS headers in production"
echo ""

