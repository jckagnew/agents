#!/bin/bash

# Verification Script for Splash Creator Implementation
# Run this after any changes to ensure the implementation actually works

echo "🔍 Verifying Splash Creator Implementation..."
echo "=============================================="

# Check if server is running
if ! curl -s http://localhost:3001/api/projects > /dev/null 2>&1; then
    echo "❌ Server not running on port 3001"
    echo "   Please start with: npm run dev"
    exit 1
fi

echo "✅ Server is running"

# Run comprehensive integration test
echo "🧪 Running comprehensive integration test..."
node test-integration.js

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 VERIFICATION PASSED!"
    echo "✅ Implementation is fully working and ready for production"
    exit 0
else
    echo ""
    echo "💥 VERIFICATION FAILED!"
    echo "❌ Implementation needs fixes before celebrating"
    exit 1
fi
