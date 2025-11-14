#!/bin/bash

# ===================================================================
# COPY HARVESTED CREDENTIALS TO MASTER .ENV
# Copies credentials from design-first-software-factory to jckagnew-agents
# Also extracts and updates credentials intelligently
# ===================================================================

set -e

echo "📋 Copying Harvested Credentials"
echo "================================="
echo ""

# Paths
HARVESTED_ENV="/Users/jackagnew/projects/design-first-software-factory/.env"
HARVESTED_AGENTS_ENV="/Users/jackagnew/projects/jckagnew-agents/.env"
TARGET_ENV="/Users/jackagnew/projects/jckagnew-agents/.env"
SOURCE_REPO="/Users/jackagnew/projects/design-first-software-factory"
TARGET_REPO="/Users/jackagnew/projects/jckagnew-agents"

# Check if source repo exists
if [ ! -d "$SOURCE_REPO" ]; then
    echo "❌ Source repo not found: $SOURCE_REPO"
    exit 1
fi

# Check if target repo exists
if [ ! -d "$TARGET_REPO" ]; then
    echo "❌ Target repo not found: $TARGET_REPO"
    exit 1
fi

echo "📁 Source: $SOURCE_REPO"
echo "📁 Target: $TARGET_REPO"
echo ""

# Check which harvested file to use
if [ -f "$HARVESTED_ENV" ] && [ -s "$HARVESTED_ENV" ]; then
    SOURCE_ENV="$HARVESTED_ENV"
    echo "✅ Found harvested credentials at:"
    echo "   $HARVESTED_ENV"
elif [ -f "$HARVESTED_AGENTS_ENV" ] && [ -s "$HARVESTED_AGENTS_ENV" ]; then
    SOURCE_ENV="$HARVESTED_AGENTS_ENV"
    echo "✅ Using existing credentials at:"
    echo "   $HARVESTED_AGENTS_ENV"
else
    echo "❌ No harvested credentials found"
    echo "   Expected at: $HARVESTED_ENV"
    echo "   Or at: $HARVESTED_AGENTS_ENV"
    exit 1
fi

echo ""

# Copy .env file directly first
if [ -f "$SOURCE_ENV" ]; then
    echo "📄 Copying .env..."
    cp "$SOURCE_ENV" "$TARGET_ENV"
    echo "✅ .env copied"
else
    echo "⚠️  .env not found in source"
fi

# Copy CREDENTIAL_SOURCES.txt
if [ -f "$SOURCE_REPO/CREDENTIAL_SOURCES.txt" ]; then
    echo "📄 Copying CREDENTIAL_SOURCES.txt..."
    cp "$SOURCE_REPO/CREDENTIAL_SOURCES.txt" "$TARGET_REPO/CREDENTIAL_SOURCES.txt"
    echo "✅ CREDENTIAL_SOURCES.txt copied"
fi

# Copy HARVEST_REPORT.txt if it exists
if [ -f "$SOURCE_REPO/HARVEST_REPORT.txt" ]; then
    echo "📄 Copying HARVEST_REPORT.txt..."
    cp "$SOURCE_REPO/HARVEST_REPORT.txt" "$TARGET_REPO/HARVEST_REPORT.txt"
    echo "✅ HARVEST_REPORT.txt copied"
fi

echo ""
echo "✅ Copy complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Review .env file (not committed, gitignored)"
echo "  2. Commit CREDENTIAL_SOURCES.txt if needed"
echo "  3. Verify credentials: bash scripts/deployment-readiness-check.sh"
