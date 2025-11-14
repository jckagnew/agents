#!/bin/bash

# ===================================================================
# COPY HARVESTED CREDENTIALS TO MASTER .ENV
# Run this on your Mac after credential harvesting
# ===================================================================

set -e

echo "📋 Copying harvested credentials to master .env"
echo "================================================"
echo ""

# Paths
HARVESTED_ENV="/Users/jackagnew/projects/design-first-software-factory/.env"
HARVESTED_AGENTS_ENV="/Users/jackagnew/projects/jckagnew-agents/.env"
TARGET_ENV="/Users/jackagnew/projects/jckagnew-agents/.env"

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
echo "🔍 Extracting Supabase credentials..."

# Extract credentials from source
SUPABASE_URL=$(grep "^SUPABASE_URL=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")
EXPO_SUPABASE_URL=$(grep "^EXPO_PUBLIC_SUPABASE_URL=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")
SUPABASE_ANON=$(grep "^SUPABASE_ANON_KEY=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")
NEXT_SUPABASE_ANON=$(grep "^NEXT_PUBLIC_SUPABASE_ANON_KEY=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")
EXPO_SUPABASE_ANON=$(grep "^EXPO_PUBLIC_SUPABASE_ANON_KEY=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")
SUPABASE_SERVICE=$(grep "^SUPABASE_SERVICE_ROLE_KEY=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")

# Extract other common credentials
OPENAI_KEY=$(grep "^OPENAI_API_KEY=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")
ANTHROPIC_KEY=$(grep "^ANTHROPIC_API_KEY=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")
GOOGLE_KEY=$(grep "^GOOGLE_API_KEY=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")
REDIS_URL=$(grep "^UPSTASH_REDIS_URL=" "$SOURCE_ENV" 2>/dev/null | head -1 | cut -d'=' -f2- || echo "")

echo "Found credentials:"
[ -n "$SUPABASE_URL" ] && echo "  ✅ SUPABASE_URL"
[ -n "$EXPO_SUPABASE_URL" ] && echo "  ✅ EXPO_PUBLIC_SUPABASE_URL"
[ -n "$SUPABASE_ANON" ] && echo "  ✅ SUPABASE_ANON_KEY"
[ -n "$NEXT_SUPABASE_ANON" ] && echo "  ✅ NEXT_PUBLIC_SUPABASE_ANON_KEY"
[ -n "$EXPO_SUPABASE_ANON" ] && echo "  ✅ EXPO_PUBLIC_SUPABASE_ANON_KEY"
[ -n "$SUPABASE_SERVICE" ] && echo "  ✅ SUPABASE_SERVICE_ROLE_KEY"
[ -n "$OPENAI_KEY" ] && echo "  ✅ OPENAI_API_KEY"
[ -n "$ANTHROPIC_KEY" ] && echo "  ✅ ANTHROPIC_API_KEY"
[ -n "$GOOGLE_KEY" ] && echo "  ✅ GOOGLE_API_KEY"
[ -n "$REDIS_URL" ] && echo "  ✅ REDIS_URL"

echo ""

# Backup existing .env if it exists
if [ -f "$TARGET_ENV" ]; then
    BACKUP="$TARGET_ENV.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$TARGET_ENV" "$BACKUP"
    echo "💾 Backed up existing .env to:"
    echo "   $BACKUP"
    echo ""
fi

# Update .env with real credentials
cp "$TARGET_ENV" "${TARGET_ENV}.tmp" || cp .env.example "${TARGET_ENV}.tmp"

# Replace Supabase credentials
if [ -n "$SUPABASE_URL" ]; then
    sed -i '' "s|SUPABASE_URL=.*|SUPABASE_URL=$SUPABASE_URL|g" "${TARGET_ENV}.tmp"
fi
if [ -n "$EXPO_SUPABASE_URL" ]; then
    sed -i '' "s|EXPO_PUBLIC_SUPABASE_URL=.*|EXPO_PUBLIC_SUPABASE_URL=$EXPO_SUPABASE_URL|g" "${TARGET_ENV}.tmp"
else
    # Use SUPABASE_URL for EXPO_PUBLIC if not found
    [ -n "$SUPABASE_URL" ] && sed -i '' "s|EXPO_PUBLIC_SUPABASE_URL=.*|EXPO_PUBLIC_SUPABASE_URL=$SUPABASE_URL|g" "${TARGET_ENV}.tmp"
fi

if [ -n "$SUPABASE_ANON" ]; then
    sed -i '' "s|SUPABASE_ANON_KEY=.*|SUPABASE_ANON_KEY=$SUPABASE_ANON|g" "${TARGET_ENV}.tmp"
    sed -i '' "s|EXPO_PUBLIC_SUPABASE_ANON_KEY=.*|EXPO_PUBLIC_SUPABASE_ANON_KEY=$SUPABASE_ANON|g" "${TARGET_ENV}.tmp"
elif [ -n "$NEXT_SUPABASE_ANON" ]; then
    sed -i '' "s|SUPABASE_ANON_KEY=.*|SUPABASE_ANON_KEY=$NEXT_SUPABASE_ANON|g" "${TARGET_ENV}.tmp"
    sed -i '' "s|EXPO_PUBLIC_SUPABASE_ANON_KEY=.*|EXPO_PUBLIC_SUPABASE_ANON_KEY=$NEXT_SUPABASE_ANON|g" "${TARGET_ENV}.tmp"
elif [ -n "$EXPO_SUPABASE_ANON" ]; then
    sed -i '' "s|SUPABASE_ANON_KEY=.*|SUPABASE_ANON_KEY=$EXPO_SUPABASE_ANON|g" "${TARGET_ENV}.tmp"
    sed -i '' "s|EXPO_PUBLIC_SUPABASE_ANON_KEY=.*|EXPO_PUBLIC_SUPABASE_ANON_KEY=$EXPO_SUPABASE_ANON|g" "${TARGET_ENV}.tmp"
fi

if [ -n "$SUPABASE_SERVICE" ]; then
    sed -i '' "s|SUPABASE_SERVICE_ROLE_KEY=.*|SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE|g" "${TARGET_ENV}.tmp"
fi

# Replace AI API keys
if [ -n "$OPENAI_KEY" ]; then
    sed -i '' "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=$OPENAI_KEY|g" "${TARGET_ENV}.tmp"
fi
if [ -n "$ANTHROPIC_KEY" ]; then
    sed -i '' "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$ANTHROPIC_KEY|g" "${TARGET_ENV}.tmp"
fi
if [ -n "$GOOGLE_KEY" ]; then
    sed -i '' "s|GOOGLE_AI_API_KEY=.*|GOOGLE_AI_API_KEY=$GOOGLE_KEY|g" "${TARGET_ENV}.tmp"
    sed -i '' "s|GEMINI_API_KEY=.*|GEMINI_API_KEY=$GOOGLE_KEY|g" "${TARGET_ENV}.tmp"
fi

# Replace Redis URL
if [ -n "$REDIS_URL" ]; then
    sed -i '' "s|REDIS_URL=.*|REDIS_URL=$REDIS_URL|g" "${TARGET_ENV}.tmp"
fi

# Move temp to final
mv "${TARGET_ENV}.tmp" "$TARGET_ENV"

echo "✅ Updated .env with harvested credentials!"
echo ""
echo "📊 Summary:"
echo "   Source: $SOURCE_ENV"
echo "   Target: $TARGET_ENV"
echo ""
echo "🔍 Verify credentials:"
echo "   cat $TARGET_ENV | grep -E 'SUPABASE|OPENAI|ANTHROPIC'"
echo ""
echo "📋 Next steps:"
echo "   1. cd /Users/jackagnew/projects/jckagnew-agents"
echo "   2. git add .env"
echo "   3. # DO NOT COMMIT .env (it's gitignored)"
echo "   4. npm run env:validate"
echo "   5. Ready for deployment!"
echo ""
