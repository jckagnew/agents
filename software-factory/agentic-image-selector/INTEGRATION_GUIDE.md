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
