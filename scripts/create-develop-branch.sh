#!/bin/bash

# ===================================================================
# Create Develop Branch Programmatically
# Uses GitHub API to create develop branch from Claude's work
# ===================================================================

set -e

REPO_OWNER="jckagnew"
REPO_NAME="agents"
SOURCE_BRANCH="claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP"
TARGET_BRANCH="develop"
COMMIT_SHA="0fc4a1ddc2e9514ee6371065410c2fb0ae255418"

echo "🔧 Creating develop branch programmatically"
echo "============================================"
echo ""
echo "Repo: $REPO_OWNER/$REPO_NAME"
echo "Source: $SOURCE_BRANCH"
echo "Target: $TARGET_BRANCH"
echo "Commit: $COMMIT_SHA"
echo ""

# Check if GitHub token is available
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN environment variable not set"
    echo ""
    echo "To use this script, you need a GitHub Personal Access Token with 'repo' scope."
    echo ""
    echo "Get one from: https://github.com/settings/tokens/new"
    echo "Scopes needed: repo (Full control of private repositories)"
    echo ""
    echo "Then run:"
    echo "  export GITHUB_TOKEN=your_token_here"
    echo "  bash $0"
    echo ""
    exit 1
fi

echo "✅ GitHub token found"
echo ""

# Create the branch using GitHub API
echo "📡 Creating branch via GitHub API..."
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/git/refs \
  -d "{\"ref\":\"refs/heads/$TARGET_BRANCH\",\"sha\":\"$COMMIT_SHA\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ SUCCESS: Branch '$TARGET_BRANCH' created!"
    echo ""
    echo "Details:"
    echo "$BODY" | jq '.'
    echo ""
    echo "🎉 The develop branch now exists on GitHub with all consolidation work!"
    echo ""
    echo "Next steps:"
    echo "  1. Cursor: git fetch origin && git checkout develop"
    echo "  2. Claude: git fetch origin && git checkout develop"
    echo "  3. Both agents can now work from develop"
    echo ""
elif [ "$HTTP_CODE" = "422" ]; then
    echo "⚠️  Branch already exists, updating it instead..."
    echo ""

    # Update existing branch
    UPDATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X PATCH \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/git/refs/heads/$TARGET_BRANCH \
      -d "{\"sha\":\"$COMMIT_SHA\",\"force\":true}")

    UPDATE_HTTP_CODE=$(echo "$UPDATE_RESPONSE" | tail -n1)
    UPDATE_BODY=$(echo "$UPDATE_RESPONSE" | head -n-1)

    if [ "$UPDATE_HTTP_CODE" = "200" ]; then
        echo "✅ SUCCESS: Branch '$TARGET_BRANCH' updated!"
        echo ""
        echo "🎉 The develop branch now points to the consolidation work!"
        echo ""
    else
        echo "❌ FAILED to update branch"
        echo "HTTP Code: $UPDATE_HTTP_CODE"
        echo "Response: $UPDATE_BODY"
        exit 1
    fi
else
    echo "❌ FAILED to create branch"
    echo "HTTP Code: $HTTP_CODE"
    echo "Response:"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    echo ""

    if [ "$HTTP_CODE" = "401" ]; then
        echo "Authentication failed. Check your GITHUB_TOKEN."
    elif [ "$HTTP_CODE" = "404" ]; then
        echo "Repository not found or token doesn't have access."
    fi

    exit 1
fi
