#!/bin/bash

# ===================================================================
# CURSOR: Merge Consolidation Work into Develop
# Run this to get all of Claude's monorepo consolidation
# ===================================================================

set -e

echo "🔄 Merging consolidation work into develop"
echo "=========================================="
echo ""

# Make sure we're on develop
git checkout develop
git pull origin develop

echo "✅ On develop branch"
echo ""

# Fetch Claude's consolidation branch
echo "📡 Fetching consolidation work..."
git fetch origin claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP

echo "✅ Fetched consolidation branch"
echo ""

# Merge it
echo "🔀 Merging consolidation work..."
git merge origin/claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP --no-edit

echo "✅ Merge complete!"
echo ""

# Push to remote
echo "📤 Pushing to remote..."
git push origin develop

echo "✅ Pushed to origin/develop"
echo ""

echo "🎉 SUCCESS! The develop branch now has:"
echo "  ✅ Monorepo structure (apps/, docs/, scripts/)"
echo "  ✅ Master .env system"
echo "  ✅ Credential harvesting scripts"
echo "  ✅ All deployment documentation"
echo "  ✅ Supabase integration configs"
echo ""

echo "📋 Verify structure:"
ls -la apps/ 2>/dev/null || echo "  ⚠️  apps/ not found - merge may have failed"
ls -la docs/deployment/ 2>/dev/null || echo "  ⚠️  docs/deployment/ not found"
ls -la scripts/ 2>/dev/null || echo "  ✅ scripts/ exists"
ls -la supabase/config.toml 2>/dev/null || echo "  ⚠️  supabase/config.toml not found"

echo ""
echo "✅ DONE! Next step: Harvest credentials"
echo "  bash scripts/cursor-harvest-all-credentials.sh"
echo ""
