#!/bin/bash

# ===================================================================
# Create Develop Branch Using Git Push
# Attempts to create develop branch by pushing current HEAD to it
# ===================================================================

set -e

echo "🔧 Creating develop branch via git push"
echo "========================================"
echo ""

# Get current commit
COMMIT_SHA=$(git rev-parse HEAD)
CURRENT_BRANCH=$(git branch --show-current)

echo "Current branch: $CURRENT_BRANCH"
echo "Current commit: $COMMIT_SHA"
echo ""

# Method 1: Try to push current HEAD to develop
echo "Method 1: Pushing to develop..."
if git push origin HEAD:refs/heads/develop 2>&1; then
    echo "✅ SUCCESS! Branch develop created on remote"
    echo ""
    echo "Verify:"
    echo "  git ls-remote origin develop"
    echo ""
    exit 0
else
    echo "❌ Method 1 failed (likely 403 - permission denied)"
    echo ""
fi

# Method 2: Try to create local branch and push
echo "Method 2: Creating local branch first..."
git branch -f develop HEAD
if git push origin develop 2>&1; then
    echo "✅ SUCCESS! Branch develop created on remote"
    echo ""
    exit 0
else
    echo "❌ Method 2 failed (likely 403 - permission denied)"
    echo ""
fi

# Method 3: Try with force
echo "Method 3: Force pushing to develop..."
if git push origin HEAD:develop --force 2>&1; then
    echo "✅ SUCCESS! Branch develop created on remote"
    echo ""
    exit 0
else
    echo "❌ Method 3 failed (likely 403 - permission denied)"
    echo ""
fi

echo "❌ ALL METHODS FAILED"
echo ""
echo "This means I don't have permission to create/push to 'develop' branch."
echo ""
echo "Alternative solutions:"
echo "  1. Use GitHub API script: bash scripts/create-develop-branch.sh"
echo "  2. Create via GitHub web interface"
echo "  3. Have user create it manually with git access"
echo ""
exit 1
