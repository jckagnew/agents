#!/bin/bash

# ===================================================================
# Environment Validation Script
# Checks if all required environment variables are set
# ===================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

echo "🔍 Validating Environment Configuration"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: Master .env file not found at: $ENV_FILE"
    echo ""
    echo "📋 Run setup script first:"
    echo "   ./scripts/setup-env.sh"
    exit 1
fi

echo "✅ Found master .env file"
echo ""

# Load .env file
set -a
source "$ENV_FILE"
set +a

# Define required variables
REQUIRED_VARS=(
    "SUPABASE_URL"
    "EXPO_PUBLIC_SUPABASE_URL"
    "SUPABASE_ANON_KEY"
    "EXPO_PUBLIC_SUPABASE_ANON_KEY"
    "SUPABASE_SERVICE_ROLE_KEY"
)

OPTIONAL_VARS=(
    "REDIS_URL"
    "OPENAI_API_KEY"
    "ANTHROPIC_API_KEY"
    "GOOGLE_AI_API_KEY"
    "STRIPE_SECRET_KEY"
    "EXPO_PUBLIC_FACTORY_API_URL"
)

# Validate required variables
echo "📋 Checking Required Variables:"
echo "--------------------------------"
MISSING_REQUIRED=0

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ] || [[ "${!var}" == *"your-"* ]] || [[ "${!var}" == *"-here"* ]]; then
        echo "❌ $var - MISSING or uses placeholder value"
        MISSING_REQUIRED=1
    else
        # Show first 20 characters
        value="${!var}"
        preview="${value:0:20}..."
        echo "✅ $var - Set ($preview)"
    fi
done

echo ""
echo "📋 Checking Optional Variables:"
echo "--------------------------------"
MISSING_OPTIONAL=0

for var in "${OPTIONAL_VARS[@]}"; do
    if [ -z "${!var}" ] || [[ "${!var}" == *"your-"* ]] || [[ "${!var}" == *"-here"* ]]; then
        echo "⚠️  $var - Not configured (may be needed for some features)"
        MISSING_OPTIONAL=1
    else
        value="${!var}"
        preview="${value:0:20}..."
        echo "✅ $var - Set ($preview)"
    fi
done

echo ""
echo "========================================"

if [ $MISSING_REQUIRED -eq 1 ]; then
    echo ""
    echo "❌ VALIDATION FAILED: Missing required environment variables"
    echo ""
    echo "📝 Please edit .env and add real credentials:"
    echo "   nano $ENV_FILE"
    echo ""
    echo "🔗 Get credentials from:"
    echo "   - Supabase: https://supabase.com/dashboard/project/design-factory-admin"
    echo "   - Redis: Your Redis provider (Upstash, Redis Cloud, Railway)"
    echo "   - OpenAI: https://platform.openai.com/api-keys"
    echo "   - Anthropic: https://console.anthropic.com/"
    echo "   - Google AI: https://makersuite.google.com/app/apikey"
    exit 1
fi

if [ $MISSING_OPTIONAL -eq 1 ]; then
    echo ""
    echo "⚠️  WARNING: Some optional variables are not configured"
    echo "   The application may run with limited functionality"
    echo ""
fi

echo ""
echo "✅ VALIDATION PASSED: All required variables are configured"
echo ""
echo "🚀 You're ready to start development!"
echo ""
echo "📚 Next steps:"
echo "   - Factory: npm run api:dev"
echo "   - Admin Console: npm run start"
echo ""
