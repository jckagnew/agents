#!/bin/bash
# Agentic Image Selector Setup Script

set -e

echo "🎯 Setting up Agentic Image Selector for Splash Screens"
echo "======================================================"

# Make scripts executable
chmod +x agents/*.py

echo "✅ Made all agent scripts executable"

# Create necessary directories
mkdir -p templates/{fitness,finance,productivity,ecommerce,education,gaming,social,custom}
mkdir -p components
mkdir -p utils

echo "✅ Created template directories"

# Check if MCP servers are configured
if [ ! -f "../../utilities/env.master" ]; then
    echo "❌ Environment file not found. Please run the MCP setup first:"
    echo "   cd ../../ && ./enhanced-mcp-setup.sh"
    exit 1
fi

echo "✅ Environment file found"

# Check for required API keys
echo "🔑 Checking API key configuration..."

# Check open source repository keys (primary)
if ! grep -q "UNSPLASH_API_KEY=" ../../utilities/env.master || grep -q "UNSPLASH_API_KEY=your_" ../../utilities/env.master; then
    echo "⚠️  UNSPLASH_API_KEY not configured. Get free key at: https://unsplash.com/developers"
fi

if ! grep -q "PIXABAY_API_KEY=" ../../utilities/env.master || grep -q "PIXABAY_API_KEY=your_" ../../utilities/env.master; then
    echo "⚠️  PIXABAY_API_KEY not configured. Get free key at: https://pixabay.com/api/docs/"
fi

# Check MCP server keys (backup)
if ! grep -q "BRAVE_API_KEY=" ../../utilities/env.master || grep -q "BRAVE_API_KEY=your_" ../../utilities/env.master; then
    echo "⚠️  BRAVE_API_KEY not configured. Get free key at: https://brave.com/search/api/"
fi

if ! grep -q "PERPLEXITY_API_KEY=" ../../utilities/env.master || grep -q "PERPLEXITY_API_KEY=your_" ../../utilities/env.master; then
    echo "⚠️  PERPLEXITY_API_KEY not configured. Get free key at: https://www.perplexity.ai/settings/api"
fi

echo "✅ API key check completed"

# Create example usage script
cat > example-usage.sh << 'EOF'
#!/bin/bash
# Example usage of Agentic Image Selector

echo "🎯 Agentic Image Selector - Example Usage"
echo "========================================="

# Example 1: Fitness app
echo "1. Creating splash screens for a fitness app..."
python agents/orchestration-agent.py --init \
  --project-type fitness \
  --app-name "MyFitnessApp" \
  --theme "transformation"

python agents/orchestration-agent.py --run

# Example 2: Finance app
echo "2. Creating splash screens for a finance app..."
python agents/orchestration-agent.py --init \
  --project-type finance \
  --app-name "WealthBuilder" \
  --theme "wealth-building" \
  --colors "blue-to-gold"

python agents/orchestration-agent.py --run

# Example 3: Custom project
echo "3. Creating splash screens for a custom project..."
python agents/orchestration-agent.py --init \
  --project-type custom \
  --app-name "MyCustomApp" \
  --theme "innovation" \
  --colors "purple-to-pink" \
  --animation "fade" \
  --cta-primary "Get Started" \
  --cta-secondary "Learn More"

python agents/orchestration-agent.py --run

echo "✅ All examples completed!"
EOF

chmod +x example-usage.sh

echo "✅ Created example usage script"

# Create integration guide
cat > INTEGRATION_GUIDE.md << 'EOF'
# Software Factory Integration Guide

## Quick Integration

### 1. Add to New Project
```bash
# When creating a new project
software-factory create-project --template agentic-splash \
  --project-type fitness \
  --app-name "MyFitnessApp"
```

### 2. Add to Existing Project
```bash
# Copy capability to existing project
cp -r agentic-image-selector/ my-project/splash-generator/

# Navigate to project
cd my-project/splash-generator/

# Initialize for your project type
python agents/orchestration-agent.py --init \
  --project-type productivity \
  --app-name "MyProductivityApp"

# Generate splash screens
python agents/orchestration-agent.py --run
```

### 3. Custom Configuration
```bash
# Create custom project type
python agents/orchestration-agent.py --init \
  --project-type custom \
  --app-name "MyCustomApp" \
  --theme "innovation" \
  --colors "purple-to-pink" \
  --animation "fade" \
  --cta-primary "Get Started" \
  --cta-secondary "Learn More"
```

## Supported Project Types

- **fitness**: Weight tracking, workout apps, health monitoring
- **finance**: Investment apps, budgeting tools, wealth management
- **productivity**: Task managers, project tools, workflow optimization
- **ecommerce**: Online stores, marketplaces, product catalogs
- **education**: Learning platforms, skill development, courses
- **gaming**: Video games, mobile games, gaming platforms
- **social**: Social networks, community platforms, messaging apps
- **custom**: Any other project type with custom configuration

## Output Files

After running the workflow, you'll get:

- `src/components/splash-prototypes/` - React components for each prototype
- `src/app/splash-comparison/` - A/B testing comparison page
- `splash-generation-results.json` - Complete workflow results
- `image_pairs.json` - All sourced image pairs
- `top_image_pairs.json` - Top 3 curated pairs

## Next Steps

1. **Test Prototypes**: Visit `/splash-comparison` to see all versions
2. **User Testing**: Gather feedback on commercial appeal
3. **A/B Testing**: Measure conversion rates
4. **Integration**: Replace static splash with animated version
5. **Customization**: Modify colors, animations, and content as needed

## Troubleshooting

### MCP Server Issues
- Ensure API keys are configured in `utilities/env.master`
- Check that MCP servers are running
- Verify network connectivity

### Image Loading Issues
- Check image URLs are accessible
- Verify CORS settings for external images
- Consider downloading and hosting images locally

### Animation Performance
- Test on different devices and browsers
- Adjust animation timing for slower devices
- Consider reducing animation complexity for mobile
EOF

echo "✅ Created integration guide"

# Create copyright compliance reminder
cat > COPYRIGHT_REMINDER.md << 'EOF'
# Copyright Compliance Reminder

## 🛡️ Important: Image Licensing

This system is designed to use **only open source and free-to-use images** to avoid copyright issues:

### ✅ Approved Sources
- **Unsplash**: Free for commercial use, no attribution required
- **Pixabay**: Free for commercial use, no attribution required  
- **Pexels**: Free for commercial use, no attribution required
- **Freepik**: Free with attribution required
- **OpenClipart**: Public domain, no restrictions

### 🚫 Avoided Sources
- Stock photo sites requiring payment
- Social media images without permission
- Branded content or copyrighted material
- Images with unclear licensing

### 📋 What This Means
- All images are sourced from free repositories
- Commercial use is explicitly allowed
- No copyright infringement risk
- No additional licensing costs

For complete details, see: COPYRIGHT_COMPLIANCE.md
EOF

echo "✅ Created copyright compliance reminder"

echo ""
echo "🚀 Setup complete! You can now use the Agentic Image Selector:"
echo ""
echo "📖 Quick Start:"
echo "   python agents/orchestration-agent.py --init --project-type fitness --app-name 'MyApp'"
echo "   python agents/orchestration-agent.py --run"
echo ""
echo "📚 Examples:"
echo "   ./example-usage.sh"
echo ""
echo "📖 Documentation:"
echo "   README.md - Complete documentation"
echo "   INTEGRATION_GUIDE.md - Software factory integration"
echo "   COPYRIGHT_COMPLIANCE.md - Legal and licensing information"
echo ""
echo "🎯 Supported Project Types:"
echo "   fitness, finance, productivity, ecommerce, education, gaming, social, custom"
echo ""
echo "🛡️ Copyright Compliance:"
echo "   All images are sourced from free, open source repositories"
echo "   No copyright infringement risk"
echo "   Commercial use explicitly allowed"
