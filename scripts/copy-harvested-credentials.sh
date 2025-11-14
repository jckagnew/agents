#!/bin/bash

# ===================================================================
# COPY HARVESTED CREDENTIALS
# Copies credentials from design-first-software-factory to jckagnew-agents
# ===================================================================

set -e

echo "📋 Copying Harvested Credentials"
echo "================================="
echo ""

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

# Copy .env file
if [ -f "$SOURCE_REPO/.env" ]; then
    echo "📄 Copying .env..."
    cp "$SOURCE_REPO/.env" "$TARGET_REPO/.env"
    echo "✅ .env copied"
else
    echo "⚠️  .env not found in source repo"
fi

# Copy CREDENTIAL_SOURCES.txt
if [ -f "$SOURCE_REPO/CREDENTIAL_SOURCES.txt" ]; then
    echo "📄 Copying CREDENTIAL_SOURCES.txt..."
    cp "$SOURCE_REPO/CREDENTIAL_SOURCES.txt" "$TARGET_REPO/CREDENTIAL_SOURCES.txt"
    echo "✅ CREDENTIAL_SOURCES.txt copied"
else
    echo "⚠️  CREDENTIAL_SOURCES.txt not found in source repo"
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
echo "  3. Verify credentials are correct"

