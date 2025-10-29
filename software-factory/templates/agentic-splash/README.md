# Agentic Splash Screen Template

## 🎯 Overview

This template adds AI-powered splash screen generation capabilities to any project. It uses MCP servers and AI agents to automatically source, curate, and create commercial-grade animated splash screens.

## 🚀 Features

- **AI-Powered Image Sourcing**: Uses MCP servers to discover 100+ relevant image pairs
- **Intelligent Curation**: AI evaluates commercial appeal, animation potential, and design quality
- **Template System**: Configurable for different project types and industries
- **Animation Generation**: Creates smooth, professional animations
- **A/B Testing Ready**: Built-in comparison and testing capabilities
- **Commercial Focus**: Optimized for conversion and user engagement

## 🏗️ Project Structure

```
project-root/
├── splash-generator/
│   ├── agents/
│   │   ├── image-sourcing-agent.py
│   │   ├── design-curation-agent.py
│   │   ├── animation-generator-agent.py
│   │   └── orchestration-agent.py
│   ├── config/
│   │   └── project-types.json
│   ├── templates/
│   │   └── [project-type]/
│   └── setup.sh
├── src/
│   ├── components/
│   │   └── splash-prototypes/
│   └── app/
│       └── splash-comparison/
└── splash-config.json
```

## 🎨 Supported Project Types

- **fitness**: Weight tracking, workout apps, health monitoring
- **finance**: Investment apps, budgeting tools, wealth management
- **productivity**: Task managers, project tools, workflow optimization
- **ecommerce**: Online stores, marketplaces, product catalogs
- **education**: Learning platforms, skill development, courses
- **gaming**: Video games, mobile games, gaming platforms
- **social**: Social networks, community platforms, messaging apps
- **custom**: Any other project type with custom configuration

## 🛠️ Usage

### Factory CLI (recommended)
```bash
cd software-factory/
python create_splash.py \
  --project-type fitness \
  --app-name "MyFitnessApp" \
  --project-root ../path-to-next-app
```

This command orchestrates sourcing, curation, and animation, and drops React components plus a comparison page into the provided Next.js project. If MCP or image APIs are not configured, the workflow falls back to an offline creative library so you can still generate prototypes.

### Quick Start
```bash
# 1. Initialize for your project
cd splash-generator/
python agents/orchestration-agent.py --init --project-type fitness --app-name "MyFitnessApp"

# 2. Run the complete workflow
python agents/orchestration-agent.py --run

# 3. Test the generated splash screens
npm run dev
# Visit /splash-comparison
```

### Custom Configuration
```bash
# Custom project type
python agents/orchestration-agent.py --init \
  --project-type custom \
  --theme "meditation" \
  --colors "purple,blue" \
  --animation "fade" \
  --cta-primary "Start Meditating" \
  --cta-secondary "Learn More"
```

## 📊 Generated Output

After running the workflow, you'll get:

- **3 Animated Prototypes**: Each with different character designs and animations
- **Comparison Page**: Side-by-side testing at `/splash-comparison`
- **Complete Documentation**: Implementation guides and customization options
- **A/B Testing Ready**: Easy switching between prototypes

## 🎯 Commercial Optimization

### Conversion Elements
- **Dual CTAs**: Primary and secondary action buttons
- **Social Proof**: Progress indicators and success metrics
- **Emotional Connection**: Narrative-driven design
- **Trust Signals**: Professional appearance and branding

### A/B Testing Framework
- **Multiple Variants**: Generate 3+ versions for testing
- **Comparison Interface**: Side-by-side testing capabilities
- **Metrics Tracking**: Built-in analytics hooks
- **Easy Switching**: Simple component swapping

## 🔧 Customization

### Animation Types
- **Morphing**: Character transformation (fitness, health)
- **Scale**: Growth and expansion (finance, business)
- **Fade**: Smooth transitions (education, productivity)
- **Slide**: Movement and progress (e-commerce, travel)

### Color Schemes
- **Red-to-Green**: Health, fitness, progress
- **Blue-to-Gold**: Finance, wealth, premium
- **Purple-to-Pink**: Creativity, innovation, tech
- **Orange-to-Yellow**: Energy, productivity, growth

## 📁 Integration

### Software Factory Integration
```bash
# Add to new project
software-factory create-project --template agentic-splash \
  --project-type fitness \
  --app-name "MyApp"

# Or add to existing project
cd my-existing-project
software-factory add-capability agentic-splash \
  --project-type productivity \
  --customize
```

### Manual Integration
```bash
# Copy capability to project
cp -r agentic-image-selector/ my-project/splash-generator/

# Configure for project
cd my-project/splash-generator/
python agents/orchestration-agent.py --init --project-type my-type

# Run generation
python agents/orchestration-agent.py --run
```

## 🎯 Success Metrics

- **Image Discovery**: 100+ relevant image pairs per project
- **Curation Quality**: Top 3 pairs score >0.7 overall
- **Animation Performance**: 60fps on target devices
- **Commercial Appeal**: User testing scores >4.0/5.0
- **Conversion Rate**: A/B testing shows measurable improvement

## 🔮 Future Enhancements

- **Video Support**: Animated GIF and video splash screens
- **3D Animations**: Three.js integration for 3D effects
- **Voice Integration**: Audio feedback and narration
- **AI Personalization**: Dynamic content based on user data
- **Multi-Language**: Internationalization support
- **Accessibility**: Enhanced screen reader and keyboard support

---

**🎉 Transform any project into a commercial success with AI-powered splash screens!**
