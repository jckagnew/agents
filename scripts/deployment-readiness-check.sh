#!/bin/bash

# ===================================================================
# DEPLOYMENT READINESS CHECK
# Verifies all prerequisites before deployment
# ===================================================================

set -e

echo "🔍 DEPLOYMENT READINESS CHECK"
echo "=============================="
echo ""

READY=true
WARNINGS=0

# Check 1: Repository structure
echo "📁 Repository Structure"
echo "----------------------"

if [ -d "apps/factory/src" ]; then
    echo "  ✅ apps/factory/src exists"
else
    echo "  ❌ apps/factory/src missing"
    READY=false
fi

if [ -d "docs/deployment" ]; then
    echo "  ✅ docs/deployment exists"
else
    echo "  ⚠️  docs/deployment missing"
    WARNINGS=$((WARNINGS + 1))
fi

if [ -d "scripts" ]; then
    echo "  ✅ scripts directory exists"
else
    echo "  ❌ scripts directory missing"
    READY=false
fi

if [ -d "supabase" ]; then
    echo "  ✅ supabase directory exists"
else
    echo "  ⚠️  supabase directory missing"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""

# Check 2: Environment configuration
echo "🔐 Environment Configuration"
echo "---------------------------"

if [ ! -f ".env" ]; then
    echo "  ❌ .env file missing"
    echo "     Run: npm run env:setup"
    READY=false
else
    echo "  ✅ .env file exists"

    # Check for placeholder values
    if grep -q "your-.*-here" .env 2>/dev/null; then
        echo "  ⚠️  .env contains placeholder values"
        echo "     Update with real credentials"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "  ✅ .env has real values (no placeholders)"
    fi

    # Check critical environment variables
    echo ""
    echo "  Critical Environment Variables:"

    if grep -q "^SUPABASE_URL=https://" .env 2>/dev/null; then
        echo "    ✅ SUPABASE_URL configured"
    else
        echo "    ❌ SUPABASE_URL missing or invalid"
        READY=false
    fi

    if grep -q "^SUPABASE_ANON_KEY=eyJ" .env 2>/dev/null; then
        echo "    ✅ SUPABASE_ANON_KEY configured"
    else
        echo "    ❌ SUPABASE_ANON_KEY missing or invalid"
        READY=false
    fi

    if grep -q "^SUPABASE_SERVICE_ROLE_KEY=eyJ" .env 2>/dev/null; then
        echo "    ✅ SUPABASE_SERVICE_ROLE_KEY configured"
    else
        echo "    ⚠️  SUPABASE_SERVICE_ROLE_KEY missing"
        WARNINGS=$((WARNINGS + 1))
    fi

    if grep -q "^OPENAI_API_KEY=sk-" .env 2>/dev/null; then
        echo "    ✅ OPENAI_API_KEY configured"
    else
        echo "    ⚠️  OPENAI_API_KEY missing"
        WARNINGS=$((WARNINGS + 1))
    fi

    if grep -q "^ANTHROPIC_API_KEY=sk-ant-" .env 2>/dev/null; then
        echo "    ✅ ANTHROPIC_API_KEY configured"
    else
        echo "    ⚠️  ANTHROPIC_API_KEY missing"
        WARNINGS=$((WARNINGS + 1))
    fi

    if grep -q "^REDIS_URL=redis://" .env 2>/dev/null; then
        echo "    ✅ REDIS_URL configured"
    else
        echo "    ⚠️  REDIS_URL missing (required for production)"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

echo ""

# Check 3: Dependencies
echo "📦 Dependencies"
echo "--------------"

if [ -f "package.json" ]; then
    echo "  ✅ package.json exists"

    if [ -d "node_modules" ]; then
        echo "  ✅ node_modules installed"
    else
        echo "  ⚠️  node_modules missing (run: npm install)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ❌ package.json missing"
    READY=false
fi

echo ""

# Check 4: Git status
echo "📋 Git Status"
echo "-------------"

if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "  ✅ Git repository initialized"

    CURRENT_BRANCH=$(git branch --show-current)
    echo "  Current branch: $CURRENT_BRANCH"

    if [ "$CURRENT_BRANCH" = "develop" ]; then
        echo "  ✅ On develop branch"
    else
        echo "  ⚠️  Not on develop branch"
        WARNINGS=$((WARNINGS + 1))
    fi

    # Check if .env is gitignored
    if git check-ignore .env > /dev/null 2>&1; then
        echo "  ✅ .env is gitignored (secure)"
    else
        echo "  ⚠️  .env is NOT gitignored (security risk!)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ❌ Not a git repository"
    READY=false
fi

echo ""

# Check 5: Required tools
echo "🔧 Required Tools"
echo "----------------"

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "  ✅ Node.js installed ($NODE_VERSION)"
else
    echo "  ❌ Node.js not installed"
    READY=false
fi

if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo "  ✅ npm installed ($NPM_VERSION)"
else
    echo "  ❌ npm not installed"
    READY=false
fi

if command -v supabase &> /dev/null; then
    SUPABASE_VERSION=$(supabase --version 2>&1 | head -1)
    echo "  ✅ Supabase CLI installed ($SUPABASE_VERSION)"
else
    echo "  ⚠️  Supabase CLI not installed"
    echo "     Install: npm install -g supabase"
    WARNINGS=$((WARNINGS + 1))
fi

if command -v expo &> /dev/null; then
    echo "  ✅ Expo CLI installed"
else
    echo "  ⚠️  Expo CLI not installed"
    echo "     Install: npm install -g expo-cli"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "=============================="
echo "📊 SUMMARY"
echo "=============================="
echo ""

if [ "$READY" = true ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED!"
    echo ""
    echo "🚀 Ready for deployment!"
    echo ""
    echo "Next steps:"
    echo "  1. supabase login"
    echo "  2. supabase link --project-ref design-factory-admin"
    echo "  3. Deploy backend to Railway"
    echo "  4. Deploy frontend to Vercel"
    echo ""
    exit 0
elif [ "$READY" = true ]; then
    echo "⚠️  READY WITH WARNINGS ($WARNINGS warnings)"
    echo ""
    echo "You can proceed with deployment, but some optional features may not work."
    echo ""
    exit 0
else
    echo "❌ NOT READY FOR DEPLOYMENT"
    echo ""
    echo "Fix the issues marked with ❌ above before deploying."
    echo ""
    exit 1
fi
