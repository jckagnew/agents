#!/bin/bash

# ===================================================================
# Credential Harvesting Script
# Consolidates existing credentials from various locations
# ===================================================================

set -e

ROOT_DIR="/home/user/agents"
TARGET_ENV="$ROOT_DIR/.env"

echo "🔍 Credential Harvesting Tool"
echo "=============================="
echo ""
echo "This script helps consolidate existing credentials into master .env"
echo ""

# Check if target .env exists
if [ ! -f "$TARGET_ENV" ]; then
    echo "❌ Master .env not found. Run: npm run env:setup first"
    exit 1
fi

echo "📋 Where are your credentials currently stored?"
echo ""
echo "Common locations:"
echo "  1. Supabase Dashboard (online)"
echo "  2. Other repository .env file"
echo "  3. Vercel environment variables"
echo "  4. Railway environment variables"
echo "  5. Local file elsewhere"
echo ""
echo "This script will help you:"
echo "  - Extract from Supabase CLI (if linked)"
echo "  - Copy from other .env files"
echo "  - Show what's already in master .env"
echo ""

# Function to check if credential exists
check_credential() {
    local key=$1
    if grep -q "^$key=" "$TARGET_ENV" && ! grep "^$key=.*-here" "$TARGET_ENV" | grep -q "^$key="; then
        local value=$(grep "^$key=" "$TARGET_ENV" | cut -d'=' -f2 | cut -c1-20)
        echo "  ✅ $key (${value}...)"
        return 0
    else
        echo "  ❌ $key (needs value)"
        return 1
    fi
}

echo "🔍 Checking current .env status:"
echo "--------------------------------"

MISSING=0

# Check Supabase
echo ""
echo "Supabase:"
check_credential "SUPABASE_URL" || MISSING=$((MISSING+1))
check_credential "SUPABASE_ANON_KEY" || MISSING=$((MISSING+1))
check_credential "SUPABASE_SERVICE_ROLE_KEY" || MISSING=$((MISSING+1))

# Check Redis
echo ""
echo "Redis:"
check_credential "REDIS_URL" || MISSING=$((MISSING+1))

# Check AI Services
echo ""
echo "AI Services:"
check_credential "OPENAI_API_KEY" || MISSING=$((MISSING+1))
check_credential "ANTHROPIC_API_KEY" || MISSING=$((MISSING+1))
check_credential "GOOGLE_AI_API_KEY" || MISSING=$((MISSING+1))

echo ""
echo "================================"

if [ $MISSING -eq 0 ]; then
    echo "✅ All credentials configured!"
    exit 0
fi

echo "⚠️  Missing $MISSING credential(s)"
echo ""
echo "📚 Where to find them:"
echo ""
echo "Supabase:"
echo "  Dashboard: https://supabase.com/dashboard/project/design-factory-admin"
echo "  Path: Settings → API"
echo ""
echo "Redis:"
echo "  If you already provisioned Redis, check:"
echo "    - Upstash dashboard: https://console.upstash.com"
echo "    - Redis Cloud: https://app.redislabs.com"
echo "    - Railway project dashboard"
echo ""
echo "AI Services (if you already have keys):"
echo "  - OpenAI: https://platform.openai.com/api-keys"
echo "  - Anthropic: https://console.anthropic.com/settings/keys"
echo "  - Google AI: https://makersuite.google.com/app/apikey"
echo ""
echo "📝 To add credentials:"
echo "  nano $TARGET_ENV"
echo ""
echo "💡 Or if credentials are in another file:"
echo "  cat /path/to/other/.env >> $TARGET_ENV"
echo "  # Then clean up duplicates manually"
echo ""
