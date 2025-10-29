#!/bin/bash
# Weight Tracker Splash Screen Agents Setup

set -e

echo "🎯 Setting up Weight Tracker Splash Screen Creation Agents"
echo "=========================================================="

# Make scripts executable
chmod +x image-sourcing-agent.py
chmod +x design-curation-agent.py
chmod +x animation-prototype-agent.py
chmod +x orchestrate-splash-creation.py

echo "✅ Made all agent scripts executable"

# Create necessary directories
mkdir -p ../src/components/splash-prototypes
mkdir -p ../src/app/splash-comparison

echo "✅ Created necessary directories"

# Check if MCP servers are configured
if [ ! -f "../../../../utilities/env.master" ]; then
    echo "❌ Environment file not found. Please run the MCP setup first:"
    echo "   cd ../../../../ && ./enhanced-mcp-setup.sh"
    exit 1
fi

echo "✅ Environment file found"

# Check for required API keys
if ! grep -q "BRAVE_API_KEY=" ../../../../utilities/env.master || grep -q "BRAVE_API_KEY=your_" ../../../../utilities/env.master; then
    echo "⚠️  BRAVE_API_KEY not configured. Please add it to utilities/env.master"
fi

if ! grep -q "PERPLEXITY_API_KEY=" ../../../../utilities/env.master || grep -q "PERPLEXITY_API_KEY=your_" ../../../../utilities/env.master; then
    echo "⚠️  PERPLEXITY_API_KEY not configured. Please add it to utilities/env.master"
fi

echo ""
echo "🚀 Setup complete! You can now run:"
echo "   python orchestrate-splash-creation.py"
echo ""
echo "This will:"
echo "1. Source 100+ fitness cartoon image pairs"
echo "2. Curate the top 3 using AI analysis"
echo "3. Generate animated splash screen prototypes"
echo "4. Create a comparison page for testing"
echo ""
echo "📁 Results will be saved in:"
echo "   - image_pairs.json (all sourced pairs)"
echo "   - top_image_pairs.json (top 3 curated pairs)"
echo "   - src/components/splash-prototypes/ (React components)"
echo "   - src/app/splash-comparison/ (comparison page)"
