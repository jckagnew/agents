#!/bin/bash
# Weight Tracker Design Review Command
# Triggers comprehensive visual QA using Playwright MCP

echo "🎨 Starting Weight Tracker Design Review..."
echo ""

# Check if dev server is running
if ! curl -s http://localhost:3000 > /dev/null; then
    echo "❌ Dev server not running at localhost:3000"
    echo "Start it first: npm run dev"
    exit 1
fi

# Create output directories
mkdir -p reports screenshots

# Run the visual QA test suite
echo "🧪 Running visual QA tests..."
node tests/visual/weight-tracker-qa.spec.js

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Design review complete! All quality checks passed."
    echo "📊 Check reports/ for detailed results"
    echo "📸 Check screenshots/ for visual artifacts"
else
    echo ""
    echo "⚠️  Design review found issues"
    echo "Review the report above for specific problems"
fi

echo ""
echo "💡 Tip: Compare screenshots with previous baseline to detect regressions"
