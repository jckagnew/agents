#!/bin/bash
# Quick command to trigger full design review

echo "🎨 Starting Design Review..."
echo ""

# Check if dev server is running
if ! curl -s http://localhost:3000 > /dev/null; then
    echo "❌ Dev server not running at localhost:3000"
    echo "Start it first: npm run dev"
    exit 1
fi

# Create reports directory if it doesn't exist
mkdir -p reports

# Trigger the design reviewer agent
claude "Please run a comprehensive design review on http://localhost:3000. Take screenshots at desktop (1440x900), tablet (768x1024), and mobile (375x667) viewports. Analyze against the design principles in .claude/templates/design-principles-splash.md and provide a quality score out of 100 with detailed recommendations. Save the report to ./reports/design-review-$(date +%Y%m%d-%H%M%S).md"

echo ""
echo "✅ Review complete! Check ./reports/ for results."
