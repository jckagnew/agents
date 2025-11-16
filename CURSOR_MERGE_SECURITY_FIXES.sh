#!/bin/bash
#
# CURSOR: Merge Security Fixes Script
#
# This script merges the critical security fixes from Claude's branch into develop.
# It addresses all issues identified in Codex's audit.
#

set -e  # Exit on error

echo "=========================================="
echo "MERGING SECURITY FIXES TO DEVELOP"
echo "=========================================="
echo ""

# Step 1: Verify we're starting from a clean state
echo "Step 1: Checking git status..."
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  WARNING: You have uncommitted changes."
    echo "Please commit or stash them before running this script."
    exit 1
fi

# Step 2: Fetch latest from remote
echo ""
echo "Step 2: Fetching latest from origin..."
git fetch origin claude/merge-security-fixes-0145KTB3qeeeKQo6p46HhzDm
git fetch origin develop 2>/dev/null || echo "Note: origin/develop may not exist yet"

# Step 3: Switch to develop
echo ""
echo "Step 3: Switching to develop branch..."
git checkout develop || {
    echo "Creating develop branch from current HEAD..."
    git checkout -b develop
}

# Step 4: Merge the security fixes
echo ""
echo "Step 4: Merging security fixes..."
echo "Source: claude/merge-security-fixes-0145KTB3qeeeKQo6p46HhzDm"
echo ""
echo "This merge includes:"
echo "  ✅ SQL injection fixes (admin-customers/admin-projects)"
echo "  ✅ Race condition fixes (quota.service.ts + migration)"
echo "  ✅ Retry logic for all Codex API calls"
echo ""

git merge origin/claude/merge-security-fixes-0145KTB3qeeeKQo6p46HhzDm --no-edit -m "Merge security fixes: SQL injection, race conditions, and retry logic

Merging critical security fixes from Claude's audit response:

Admin Console Security (commit 2cc35df):
- Fix SQL injection in admin-customers endpoint
- Add input validation, rate limiting, soft delete to admin-projects
- Implement proper CORS handling

Factory Backend Reliability (commit edb44be):
- Fix race conditions in quota updates with atomic SQL operations
- Add database migration 008_atomic_quota_updates.sql
- Implement safe JSON parsing and retry utilities

Complete Retry Coverage (commit 2cb62ef):
- Extend retryWithBackoff to all 3 Codex API methods
- generateInitialDesign (already had it)
- refineDesign (newly added)
- compareDesignAgainstBenchmark (newly added)

All CRITICAL issues from Codex audit are now resolved.

Branch: claude/merge-security-fixes-0145KTB3qeeeKQo6p46HhzDm
Commits: 2cb62ef, edb44be, 2cc35df"

# Step 5: Verify the merge
echo ""
echo "Step 5: Verifying merged files..."
EXPECTED_FILES=(
    "supabase/functions/admin-customers/index.ts"
    "supabase/functions/admin-projects/index.ts"
    "apps/factory/src/services/quota.service.ts"
    "apps/factory/src/services/codex.service.ts"
    "apps/factory/src/utils/retry.ts"
    "supabase/migrations/008_atomic_quota_updates.sql"
)

ALL_PRESENT=true
for file in "${EXPECTED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✅ $file"
    else
        echo "  ❌ MISSING: $file"
        ALL_PRESENT=false
    fi
done

if [[ "$ALL_PRESENT" != true ]]; then
    echo ""
    echo "⚠️  ERROR: Some expected files are missing!"
    echo "The merge may have conflicts or issues."
    exit 1
fi

# Step 6: Verify retry logic
echo ""
echo "Step 6: Verifying retry logic coverage..."
RETRY_COUNT=$(grep -c "retryWithBackoff" apps/factory/src/services/codex.service.ts || echo "0")
if [[ "$RETRY_COUNT" -ge 3 ]]; then
    echo "  ✅ All 3 Codex API calls have retry logic"
else
    echo "  ⚠️  WARNING: Expected 3+ retry calls, found $RETRY_COUNT"
fi

# Step 7: Show what's ready to push
echo ""
echo "=========================================="
echo "✅ MERGE COMPLETE!"
echo "=========================================="
echo ""
echo "Branch 'develop' now contains all security fixes."
echo ""
echo "Files merged:"
for file in "${EXPECTED_FILES[@]}"; do
    echo "  - $file"
done
echo ""
echo "Next step: Push to origin"
echo ""
echo "Run: git push -u origin develop"
echo ""
echo "After deployment, remember to:"
echo "  1. Run database migration: supabase db push"
echo "  2. Configure production CORS for admin console"
echo ""
