# Agentic Image Selector for Splash Screens

## 🎯 Overview

A reusable AI-powered system for automatically sourcing, curating, and generating commercial-grade animated splash screens for any project. This capability leverages MCP servers and AI agents to create compelling landing pages that maximize conversion rates.

## 🚀 Key Features

- **Open Source Image Sourcing**: Uses Unsplash, Pixabay, and other free repositories to avoid copyright issues
- **AI-Powered Image Discovery**: MCP servers discover 100+ relevant image pairs from open source repositories
- **Intelligent Curation**: AI evaluates commercial appeal, animation potential, and design quality
- **Copyright Compliance**: All images are sourced from free-to-use repositories with proper licensing
- **Template System**: Configurable for different project types and industries
- **Animation Generation**: Creates smooth, professional animations
- **A/B Testing Ready**: Built-in comparison and testing capabilities
- **Commercial Focus**: Optimized for conversion and user engagement

## 🏗️ Architecture

```
agentic-image-selector/
├── agents/
│   ├── image-sourcing-agent.py      # Generic image discovery
│   ├── design-curation-agent.py     # AI-powered curation
│   ├── animation-generator-agent.py # Template-based animation creation
│   └── orchestration-agent.py       # Workflow coordination
├── templates/
│   ├── fitness/                     # Weight tracker template
│   ├── finance/                     # Financial app template
│   ├── productivity/                # Productivity app template
│   └── ecommerce/                   # E-commerce template
├── components/
│   ├── SplashScreenBase.tsx         # Base React component
│   ├── AnimationEngine.tsx          # Animation system
│   └── ComparisonView.tsx           # A/B testing component
├── config/
│   ├── project-types.json           # Project type configurations
│   └── industry-themes.json         # Industry-specific themes
└── utils/
    ├── mcp-client.py                # MCP server utilities
    └── template-engine.py           # Template processing
```

## 🎨 Supported Project Types

### **Fitness & Health**
- Weight tracking, workout apps, nutrition trackers
- Before/after transformation themes
- Progress indicators and goal tracking

### **Finance & Fintech**
- Investment apps, budgeting tools, crypto trackers
- Wealth building and financial growth themes
- Security and trust indicators

### **Productivity & Business**
- Task managers, project tools, CRM systems
- Efficiency and success themes
- Professional and corporate aesthetics

### **E-commerce & Retail**
- Online stores, marketplaces, product catalogs
- Shopping and discovery themes
- Conversion-focused design elements

### **Education & Learning**
- Online courses, skill development, training platforms
- Knowledge and growth themes
- Achievement and progress indicators

## 🔑 API Key Setup

### **Required API Keys**
Add these to your `utilities/env.master` file:

```bash
# Open Source Image Repositories (Free)
UNSPLASH_API_KEY=your_unsplash_api_key_here
PIXABAY_API_KEY=your_pixabay_api_key_here

# MCP Servers (Backup)
BRAVE_API_KEY=your_brave_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

### **Getting API Keys**
- **Unsplash**: https://unsplash.com/developers (Free, 50 requests/hour)
- **Pixabay**: https://pixabay.com/api/docs/ (Free, 5000 requests/hour)
- **Brave Search**: https://brave.com/search/api/ (Free tier available)
- **Perplexity**: https://www.perplexity.ai/settings/api (Free tier available)

## 🛠️ Usage

### **Quick Start**
```bash
# 1. Initialize for your project
python orchestration-agent.py --init --project-type fitness --app-name "MyFitnessApp"

# 2. Run the complete workflow
python orchestration-agent.py --run

# 3. Test the generated splash screens
npm run dev
# Visit /splash-comparison
```

### **Custom Configuration**
```bash
# Custom project type
python orchestration-agent.py --init \
  --project-type custom \
  --theme "meditation" \
  --colors "purple,blue" \
  --animation "fade" \
  --cta-primary "Start Meditating" \
  --cta-secondary "Learn More"
```

### **Template Customization**
```json
{
  "projectType": "fitness",
  "theme": "transformation",
  "colors": {
    "primary": "#dc2626",
    "secondary": "#22c55e",
    "gradient": "red-to-green"
  },
  "animation": {
    "type": "morphing",
    "duration": 3000,
    "easing": "ease-in-out"
  },
  "content": {
    "title": "Transform Your Life",
    "subtitle": "Track. Transform. Triumph.",
    "ctaPrimary": "Create Profile",
    "ctaSecondary": "Log In"
  },
  "searchQueries": [
    "fitness transformation before after",
    "weight loss journey cartoon",
    "fitness motivation character"
  ]
}
```

## 🤖 Agent Capabilities

### **1. Image Sourcing Agent**
- **Open Source Priority**: Unsplash, Pixabay, Pexels, Freepik as primary sources
- **MCP Server Backup**: Brave Search, Perplexity for additional discovery
- **Copyright Validation**: Automatic verification of open source licensing
- **Query Generation**: AI-generated search terms based on project type
- **Quality Validation**: Automatic image accessibility and quality checks
- **Pair Extraction**: Intelligent before/after pair identification

### **2. Design Curation Agent**
- **AI Analysis**: Perplexity-powered commercial appeal evaluation
- **Multi-Criteria Scoring**: Commercial appeal, animation potential, design quality
- **Industry Adaptation**: Scoring weights adjusted by project type
- **Implementation Guidance**: Specific recommendations for each image pair

### **3. Animation Generator Agent**
- **Template System**: Project-type specific animation templates
- **Dynamic Styling**: Color schemes and themes applied automatically
- **Responsive Design**: Mobile-first approach with device optimization
- **Performance Optimization**: 60fps animations with GPU acceleration

### **4. Orchestration Agent**
- **Workflow Management**: Coordinates all agents in proper sequence
- **Error Handling**: Comprehensive error recovery and reporting
- **Prerequisites Validation**: MCP servers, API keys, dependencies
- **Results Aggregation**: Complete workflow reporting and next steps

## 📊 Commercial Optimization

### **Conversion Elements**
- **Dual CTAs**: Primary and secondary action buttons
- **Social Proof**: Progress indicators and success metrics
- **Emotional Connection**: Narrative-driven design
- **Trust Signals**: Professional appearance and branding

### **A/B Testing Framework**
- **Multiple Variants**: Generate 3+ versions for testing
- **Comparison Interface**: Side-by-side testing capabilities
- **Metrics Tracking**: Built-in analytics hooks
- **Easy Switching**: Simple component swapping

### **Industry Adaptations**
- **Fitness**: Progress bars, before/after transformations
- **Finance**: Wealth indicators, security badges
- **Productivity**: Efficiency metrics, achievement badges
- **E-commerce**: Product showcases, shopping indicators

## 🔧 Configuration Options

### **Project Types**
```json
{
  "fitness": {
    "searchQueries": ["fitness transformation", "weight loss journey"],
    "colorScheme": "red-to-green",
    "animationType": "morphing",
    "commercialWeight": 0.4
  },
  "finance": {
    "searchQueries": ["wealth building", "financial growth"],
    "colorScheme": "blue-to-gold",
    "animationType": "scale",
    "commercialWeight": 0.5
  }
}
```

### **Animation Types**
- **Morphing**: Character transformation (fitness, health)
- **Scale**: Growth and expansion (finance, business)
- **Fade**: Smooth transitions (education, productivity)
- **Slide**: Movement and progress (e-commerce, travel)

### **Color Schemes**
- **Red-to-Green**: Health, fitness, progress
- **Blue-to-Gold**: Finance, wealth, premium
- **Purple-to-Pink**: Creativity, innovation, tech
- **Orange-to-Yellow**: Energy, productivity, growth

## 📁 Integration

### **Software Factory Integration**
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

### **Manual Integration**
```bash
# Copy capability to project
cp -r agentic-image-selector/ my-project/splash-generator/

# Configure for project
cd my-project/splash-generator/
python orchestration-agent.py --init --project-type my-type

# Run generation
python orchestration-agent.py --run
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
