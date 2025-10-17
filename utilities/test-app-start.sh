#!/bin/bash

echo "🚀 Testing AI Business Name Generator App"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Not in app directory. Please run from app/ directory"
    exit 1
fi

echo "✅ Found package.json"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found. Installing dependencies..."
    npm install
    echo ""
fi

echo "✅ Dependencies ready"
echo ""

# Check environment file
if [ -f ".env.local" ]; then
    echo "✅ Environment file found"
    if grep -q "NEXT_PUBLIC_SUPABASE_URL" .env.local; then
        echo "✅ Supabase URL configured"
    else
        echo "❌ Supabase URL missing"
    fi
    
    if grep -q "OPENAI_API_KEY" .env.local; then
        echo "✅ OpenAI API key configured"
    else
        echo "❌ OpenAI API key missing"
    fi
else
    echo "❌ .env.local not found"
fi

echo ""
echo "🚀 Starting development server..."
echo ""

# Start the app
npm run dev
