#!/bin/bash

# ===================================================================
# DEPLOYMENT READINESS CHECK
# Validates all credentials and configuration for deployment
# ===================================================================

set -e

ENV_FILE="/Users/jackagnew/projects/jckagnew-agents/.env"
PASSED=0
FAILED=0
WARNINGS=0

echo "🔍 DEPLOYMENT READINESS CHECK"
echo "=============================="
echo ""

# Check if .env exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ FAILED: .env file not found"
    echo "   Run: bash scripts/copy-harvested-credentials.sh"
    exit 1
fi

echo "✅ .env file exists"
PASSED=$((PASSED + 1))

# Function to check if value is placeholder
is_placeholder() {
    local value="$1"
    if [[ "$value" =~ your-.*-here ]] || \
       [[ "$value" =~ \<.*\> ]] || \
       [[ "$value" == "" ]] || \
       [[ "$value" == "placeholder" ]] || \
       [[ "$value" == "your-local-anon-key" ]]; then
        return 0
    fi
    return 1
}

# Function to check credential
check_credential() {
    local key="$1"
    local required="${2:-false}"
    
    if grep -q "^$key=" "$ENV_FILE"; then
        local value=$(grep "^$key=" "$ENV_FILE" | head -1 | cut -d'=' -f2-)
        
        if is_placeholder "$value"; then
            if [ "$required" == "true" ]; then
                echo "❌ FAILED: $key is a placeholder"
                FAILED=$((FAILED + 1))
                return 1
            else
                echo "⚠️  WARNING: $key is a placeholder"
                WARNINGS=$((WARNINGS + 1))
                return 0
            fi
        else
            echo "✅ $key has real value"
            PASSED=$((PASSED + 1))
            return 0
        fi
    else
        if [ "$required" == "true" ]; then
            echo "❌ FAILED: $key not found"
            FAILED=$((FAILED + 1))
            return 1
        else
            echo "ℹ️  INFO: $key not found (optional)"
            return 0
        fi
    fi
}

echo ""
echo "📋 Checking Required Credentials"
echo "================================="
echo ""

# Required Supabase credentials (check multiple variants)
if grep -q "^EXPO_PUBLIC_SUPABASE_ANON_KEY=" "$ENV_FILE"; then
    check_credential "EXPO_PUBLIC_SUPABASE_ANON_KEY" true
elif grep -q "^NEXT_PUBLIC_SUPABASE_ANON_KEY=" "$ENV_FILE"; then
    check_credential "NEXT_PUBLIC_SUPABASE_ANON_KEY" true
elif grep -q "^FACTORY_SUPABASE_ANON_KEY=" "$ENV_FILE"; then
    check_credential "FACTORY_SUPABASE_ANON_KEY" true
else
    echo "❌ FAILED: No Supabase ANON_KEY found"
    FAILED=$((FAILED + 1))
fi

if grep -q "^EXPO_PUBLIC_SUPABASE_URL=" "$ENV_FILE"; then
    check_credential "EXPO_PUBLIC_SUPABASE_URL" true
elif grep -q "^NEXT_PUBLIC_SUPABASE_URL=" "$ENV_FILE"; then
    check_credential "NEXT_PUBLIC_SUPABASE_URL" true
elif grep -q "^FACTORY_SUPABASE_URL=" "$ENV_FILE"; then
    check_credential "FACTORY_SUPABASE_URL" true
else
    echo "❌ FAILED: No Supabase URL found"
    FAILED=$((FAILED + 1))
fi

check_credential "SUPABASE_SERVICE_ROLE_KEY" true

# Check for placeholder SUPABASE_ANON_KEY (local dev only)
if grep -q "^SUPABASE_ANON_KEY=your-local-anon-key" "$ENV_FILE"; then
    echo "ℹ️  INFO: SUPABASE_ANON_KEY is placeholder (local dev only, OK)"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "📋 Checking API Keys"
echo "===================="
echo ""

# API Keys
check_credential "ANTHROPIC_API_KEY" true
check_credential "OPENAI_API_KEY" false

echo ""
echo "📋 Checking Factory-Specific Credentials"
echo "========================================="
echo ""

# Factory-specific
check_credential "FACTORY_SUPABASE_URL" false
check_credential "FACTORY_SUPABASE_ANON_KEY" false
check_credential "EXPO_PUBLIC_FACTORY_SUPABASE_URL" false
check_credential "EXPO_PUBLIC_FACTORY_SUPABASE_ANON_KEY" false

echo ""
echo "📋 Checking Edge Function Credentials"
echo "====================================="
echo ""

# Edge Functions
check_credential "EDGE_FUNCTION_JWT_SECRET" false
check_credential "FILE_UPLOAD_SIGNING_SECRET" false

echo ""
echo "📋 Checking Stripe Credentials"
echo "=============================="
echo ""

# Stripe
check_credential "STRIPE_SECRET_KEY" false
check_credential "STRIPE_WEBHOOK_SECRET" false

echo ""
echo "📊 SUMMARY"
echo "=========="
echo "✅ Passed: $PASSED"
echo "⚠️  Warnings: $WARNINGS"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED!"
    echo ""
    echo "🚀 Ready for deployment!"
    exit 0
else
    echo "❌ SOME CHECKS FAILED"
    echo ""
    echo "Please fix the failed checks before deploying."
    exit 1
fi

