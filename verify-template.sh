#!/bin/bash

# Universal Implementation Verification Script
# Copy this to any project and customize for your specific needs

echo "🔍 Verifying Implementation..."
echo "=============================="

# Configuration
BASE_URL=${BASE_URL:-"http://localhost:3000"}
HEALTH_ENDPOINT=${HEALTH_ENDPOINT:-"/health"}
VERIFY_SCRIPT=${VERIFY_SCRIPT:-"verify-implementation.js"}

# Check if service is running
echo "📡 Checking if service is running on $BASE_URL..."
if ! curl -s "$BASE_URL$HEALTH_ENDPOINT" > /dev/null 2>&1; then
    echo "❌ Service not running on $BASE_URL"
    echo "   Please start the service first"
    echo "   Example: npm run dev, npm start, or docker-compose up"
    exit 1
fi

echo "✅ Service is running"

# Check if verification script exists
if [ ! -f "$VERIFY_SCRIPT" ]; then
    echo "❌ Verification script not found: $VERIFY_SCRIPT"
    echo "   Please create $VERIFY_SCRIPT or update VERIFY_SCRIPT variable"
    exit 1
fi

echo "✅ Verification script found"

# Run comprehensive verification
echo "🧪 Running comprehensive verification..."
node "$VERIFY_SCRIPT"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 VERIFICATION PASSED!"
    echo "✅ Implementation is fully working"
    echo "✅ Ready for production use"
    exit 0
else
    echo ""
    echo "💥 VERIFICATION FAILED!"
    echo "❌ Implementation needs fixes before celebrating"
    echo "❌ Not ready for production"
    exit 1
fi
