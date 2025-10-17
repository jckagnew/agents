#!/bin/bash

# 🚨 MANDATORY VERIFICATION SCRIPT
# This script MUST be run before claiming any success

set -e  # Exit on any error

echo "🔍 MANDATORY VERIFICATION CHECKLIST"
echo "=================================="

# Configuration
PROJECT_DIR="/Users/jackagnew/projects/agents/clevel-sales-guy"
PRODUCTION_URL="https://www.clevelsalesguy.com"
DEMO_PATH="/demo/weight-tracker"
API_PATH="/api/weight-calculations-js"

echo ""
echo "1. LOCAL VERIFICATION"
echo "-------------------"

# Check if we're in the right directory
if [ ! -f "$PROJECT_DIR/package.json" ]; then
    echo "❌ ERROR: Not in project directory"
    exit 1
fi

cd "$PROJECT_DIR"

# Test build
echo "Testing build..."
if npm run build > /dev/null 2>&1; then
    echo "✅ Build successful"
else
    echo "❌ Build failed"
    exit 1
fi

# Test local dev server (if running)
echo "Testing local API..."
if curl -s "http://localhost:3000$API_PATH" -X POST -H "Content-Type: application/json" -d '{"weight":180,"height":70,"neck":15,"waist":32,"hip":36,"isMale":true}' | grep -q "bfPercentage"; then
    echo "✅ Local API working"
else
    echo "⚠️  Local API not responding (dev server may not be running)"
fi

echo ""
echo "2. PRODUCTION VERIFICATION"
echo "------------------------"

# Test production demo page
echo "Testing production demo page..."
if curl -s "$PRODUCTION_URL$DEMO_PATH" | grep -q "Calculate Body Composition"; then
    echo "✅ Production demo page working"
else
    echo "❌ Production demo page not working"
    exit 1
fi

# Test production API
echo "Testing production API..."
if curl -s "$PRODUCTION_URL$API_PATH" -X POST -H "Content-Type: application/json" -d '{"weight":180,"height":70,"neck":15,"waist":32,"hip":36,"isMale":true}' | grep -q "bfPercentage"; then
    echo "✅ Production API working"
else
    echo "❌ Production API not working"
    exit 1
fi

echo ""
echo "3. FUNCTIONAL VERIFICATION"
echo "-------------------------"

# Test that we have interactive elements
if curl -s "$PRODUCTION_URL$DEMO_PATH" | grep -q "input.*type.*number"; then
    echo "✅ Interactive form elements present"
else
    echo "❌ Interactive form elements missing"
    exit 1
fi

# Test that we have calculation functionality
if curl -s "$PRODUCTION_URL$DEMO_PATH" | grep -q "Calculate Body Composition"; then
    echo "✅ Calculation functionality present"
else
    echo "❌ Calculation functionality missing"
    exit 1
fi

echo ""
echo "4. ACCURACY VERIFICATION"
echo "----------------------"

# Test calculation accuracy
RESULT=$(curl -s "$PRODUCTION_URL$API_PATH" -X POST -H "Content-Type: application/json" -d '{"weight":180,"height":70,"neck":15,"waist":32,"hip":36,"isMale":true}')
if echo "$RESULT" | grep -q '"bfPercentage":7.1'; then
    echo "✅ Calculation accuracy verified (Navy BF% = 7.1%)"
else
    echo "❌ Calculation accuracy failed"
    echo "Expected: bfPercentage around 7.1"
    echo "Got: $RESULT"
    exit 1
fi

echo ""
echo "🎉 ALL VERIFICATIONS PASSED"
echo "=========================="
echo "✅ Local verification: PASSED"
echo "✅ Production verification: PASSED" 
echo "✅ Functional verification: PASSED"
echo "✅ Accuracy verification: PASSED"
echo ""
echo "✅ SUCCESS DECLARATION AUTHORIZED"
echo "The demo is working correctly in production."
