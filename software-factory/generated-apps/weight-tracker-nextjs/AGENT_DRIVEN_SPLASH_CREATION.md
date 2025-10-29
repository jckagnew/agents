# Agent-Driven Splash Screen Creation

## 🎯 Overview

This system uses AI agents and MCP servers to automatically source, curate, and create animated splash screens for the Weight Tracker app. The approach leverages multiple AI agents working in sequence to ensure commercial appeal and technical excellence.

## 🤖 Agent Architecture

### 1. **Image Sourcing Agent** (`image-sourcing-agent.py`)
**Purpose**: Source 100+ fitness cartoon image pairs using MCP servers

**Capabilities**:
- Uses **Brave Search MCP** for web image discovery
- Uses **Perplexity MCP** for AI-powered image research
- Searches 10+ targeted queries for fitness transformation content
- Validates image accessibility and quality
- Extracts before/after pairs from search results

**Output**: `image_pairs.json` with all discovered image pairs

### 2. **Design Curation Agent** (`design-curation-agent.py`)
**Purpose**: Evaluate and select the top 3 image pairs using AI analysis

**Capabilities**:
- Uses **Perplexity MCP** for AI-powered design analysis
- Scores on 3 criteria:
  - **Commercial Appeal** (40% weight): Professional quality, brand-friendly, emotional impact
  - **Animation Potential** (30% weight): Smooth transitions, character consistency, loop compatibility
  - **Design Quality** (30% weight): Visual clarity, color harmony, composition balance
- Provides implementation suggestions for each pair
- Ranks and selects top 3 candidates

**Output**: `top_image_pairs.json` with curated selections

### 3. **Animation Prototype Agent** (`animation-prototype-agent.py`)
**Purpose**: Create animated splash screen prototypes with selected image pairs

**Capabilities**:
- Generates React components for each top 3 image pair
- Creates smooth morphing animations (🧑‍💼 → 🏃‍♂️)
- Implements dynamic background gradients
- Adds commercial appeal elements (stats, CTAs)
- Creates comparison page for A/B testing
- Generates comprehensive documentation

**Output**: 
- `src/components/splash-prototypes/SplashScreenV1-3.tsx`
- `src/app/splash-comparison/page.tsx`
- `README.md` with implementation details

### 4. **Orchestration Agent** (`orchestrate-splash-creation.py`)
**Purpose**: Coordinate the complete workflow and ensure success

**Capabilities**:
- Runs all agents in proper sequence
- Validates prerequisites (API keys, MCP servers)
- Handles errors and provides detailed reporting
- Generates comprehensive workflow results
- Provides next steps and recommendations

## 🚀 Quick Start

### Prerequisites
1. **MCP Servers Configured**: Run `../../../enhanced-mcp-setup.sh`
2. **API Keys**: Configure `BRAVE_API_KEY` and `PERPLEXITY_API_KEY` in `utilities/env.master`
3. **Python Dependencies**: `aiohttp`, `asyncio`

### Run Complete Workflow
```bash
cd scripts
./setup-splash-agents.sh
python orchestrate-splash-creation.py
```

### Run Individual Agents
```bash
# 1. Source images
python image-sourcing-agent.py

# 2. Curate top 3
python design-curation-agent.py

# 3. Create prototypes
python animation-prototype-agent.py
```

## 📊 Workflow Results

### Phase 1: Image Sourcing
- **Input**: 10+ search queries for fitness transformation content
- **Process**: MCP servers search web and AI research
- **Output**: 100+ validated image pairs
- **Time**: ~5-10 minutes

### Phase 2: Design Curation
- **Input**: 100+ image pairs from Phase 1
- **Process**: AI analysis of commercial appeal, animation potential, design quality
- **Output**: Top 3 ranked image pairs with detailed scores
- **Time**: ~10-15 minutes

### Phase 3: Animation Prototyping
- **Input**: Top 3 image pairs from Phase 2
- **Process**: Generate React components with smooth animations
- **Output**: 3 animated splash screen prototypes + comparison page
- **Time**: ~2-3 minutes

## 🎨 Generated Prototypes

Each prototype includes:

### **Visual Elements**
- **Animated Character**: Smooth morphing from "before" to "after"
- **Dynamic Background**: Red-to-green gradient that responds to animation
- **Commercial Stats**: "67% Complete", "3 Days to Goal"
- **Professional Typography**: Poppins/Nunito font stack

### **Interactive Elements**
- **Dual CTAs**: "Create Profile" and "Log In" buttons
- **Smooth Animations**: 3-4 second loop with bounce effects
- **Responsive Design**: Mobile-first approach
- **Accessibility**: ARIA labels and keyboard navigation

### **Technical Features**
- **React 19 + Next.js 15**: Modern framework
- **CSS-in-JS**: Styled-components for dynamic styling
- **TypeScript**: Full type safety
- **Performance**: Optimized animations with GPU acceleration

## 🔍 Quality Assurance

### **AI-Powered Evaluation**
- **Commercial Appeal**: Analyzed for brand-friendliness and emotional impact
- **Animation Potential**: Evaluated for smooth transition capability
- **Design Quality**: Assessed for visual clarity and composition

### **Technical Validation**
- **Image Accessibility**: All images validated for loading and quality
- **Code Quality**: TypeScript interfaces and error handling
- **Performance**: Optimized for 60fps animations
- **Responsiveness**: Tested across device sizes

## 📈 Commercial Impact

### **Conversion Optimization**
- **Dual CTAs**: Both "Create Profile" and "Log In" options
- **Social Proof**: Progress indicators and success metrics
- **Emotional Connection**: Transformation narrative
- **Professional Appearance**: Builds trust and credibility

### **A/B Testing Ready**
- **Comparison Page**: Side-by-side testing of all 3 prototypes
- **Metrics Tracking**: Built-in analytics hooks
- **Easy Switching**: Simple component swapping
- **User Feedback**: Integrated feedback collection

## 🛠️ Customization

### **Animation Timing**
```typescript
// Adjust animation speed
const interval = setInterval(() => {
  setAnimationPhase(prev => (prev + 1) % 4);
}, 1000); // Change this value
```

### **Color Scheme**
```typescript
// Customize gradient colors
const getBackgroundGradient = () => {
  // Modify RGB values for different color schemes
  return `linear-gradient(135deg, rgb(220, 38, 38) 0%, rgb(34, 197, 94) 100%)`;
};
```

### **Character Selection**
```typescript
// Replace emoji characters
const getCharacter = () => {
  switch (animationPhase) {
    case 0: return '🧑‍💼'; // Before character
    case 2: return '🏃‍♂️'; // After character
  }
};
```

## 📁 File Structure

```
scripts/
├── image-sourcing-agent.py      # Phase 1: Source images
├── design-curation-agent.py     # Phase 2: Curate top 3
├── animation-prototype-agent.py # Phase 3: Create prototypes
├── orchestrate-splash-creation.py # Master orchestrator
├── setup-splash-agents.sh      # Setup script
├── image_pairs.json            # All sourced pairs
├── top_image_pairs.json        # Top 3 curated pairs
└── workflow_results.json       # Complete workflow results

src/components/splash-prototypes/
├── SplashScreenV1.tsx          # Prototype 1
├── SplashScreenV2.tsx          # Prototype 2
├── SplashScreenV3.tsx          # Prototype 3
└── README.md                   # Implementation guide

src/app/splash-comparison/
└── page.tsx                    # A/B testing page
```

## 🎯 Next Steps

1. **Run the Workflow**: Execute `python orchestrate-splash-creation.py`
2. **Test Prototypes**: Visit `/splash-comparison` to see all versions
3. **User Testing**: Gather feedback on commercial appeal
4. **A/B Testing**: Measure conversion rates
5. **Final Selection**: Choose the best-performing prototype
6. **Integration**: Replace static splash with animated version

## 🔧 Troubleshooting

### **MCP Server Issues**
- Ensure API keys are configured in `utilities/env.master`
- Check that MCP servers are running: `npx @modelcontextprotocol/server-brave-search --help`
- Verify network connectivity for external API calls

### **Image Loading Issues**
- Check image URLs are accessible
- Verify CORS settings for external images
- Consider downloading and hosting images locally

### **Animation Performance**
- Test on different devices and browsers
- Adjust animation timing for slower devices
- Consider reducing animation complexity for mobile

## 📊 Success Metrics

- **Image Sourcing**: 100+ valid image pairs discovered
- **Curation Quality**: Top 3 pairs score >0.7 overall
- **Animation Smoothness**: 60fps on target devices
- **Commercial Appeal**: User testing scores >4.0/5.0
- **Conversion Rate**: A/B testing shows improvement

---

**🎉 This agent-driven approach ensures your Weight Tracker splash screen has maximum commercial appeal while maintaining technical excellence!**
