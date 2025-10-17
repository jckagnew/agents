#!/bin/bash

# Design Decision Team Setup Script
# State-of-the-Art 2025 Design Automation for Software Factory

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🚀 $1${NC}"
}

print_header "Setting up Design Decision Team - State-of-the-Art 2025 Design Automation"

# Check if we're in the right directory
if [ ! -f "software-factory/README.md" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Create design decision team directory structure
print_info "Creating Design Decision Team directory structure..."
mkdir -p project-starter/templates/ai_agents/design_decision_team/{agents,tasks,tools,configs,examples}
print_status "Directory structure created"

# Install required dependencies
print_info "Installing Design Decision Team dependencies..."

# Python dependencies
pip install crewai[all] requests pillow opencv-python svglib reportlab

# Node.js dependencies for image processing
npm install -g sharp imagemin imagemin-pngquant imagemin-mozjpeg

print_status "Dependencies installed"

# Create environment configuration
print_info "Creating environment configuration..."
cat > project-starter/templates/ai_agents/design_decision_team/.env.template << 'EOF'
# Design Decision Team Environment Variables

# Image Source API Keys
SHUTTERSTOCK_API_KEY=your_shutterstock_api_key_here
ADOBE_STOCK_API_KEY=your_adobe_stock_api_key_here
UNSPLASH_API_KEY=your_unsplash_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here

# AI Image Generation APIs
OPENAI_API_KEY=your_openai_api_key_here
STABILITY_API_KEY=your_stability_api_key_here
RUNWAYML_API_KEY=your_runwayml_api_key_here

# Design Tools APIs
FIGMA_API_KEY=your_figma_api_key_here
CANVA_API_KEY=your_canva_api_key_here
ADOBE_CREATIVE_API_KEY=your_adobe_creative_api_key_here

# Quality Metrics Configuration
DESIGN_QUALITY_THRESHOLD=85
UX_SCORE_THRESHOLD=80
BRAND_CONSISTENCY_THRESHOLD=90
PERFORMANCE_THRESHOLD=75

# Budget Tiers
PREMIUM_BUDGET_LIMIT=500
AI_GENERATED_BUDGET_LIMIT=100
FREE_BUDGET_LIMIT=0

# Timeline Configuration
URGENT_TIMELINE_HOURS=2
STANDARD_TIMELINE_HOURS=8
EXTENDED_TIMELINE_HOURS=24
EOF

print_status "Environment configuration created"

# Create setup instructions
print_info "Creating setup instructions..."
cat > project-starter/templates/ai_agents/design_decision_team/SETUP_INSTRUCTIONS.md << 'EOF'
# Design Decision Team Setup Instructions

## Overview
The Design Decision Team is a state-of-the-art 2025 AI agent system that handles all design decisions (UI, UX, branding) for the Software Factory. It uses cutting-edge image sources and morphing techniques to deliver professional-grade design solutions.

## Prerequisites
- Python 3.9+
- Node.js 16+
- CrewAI framework
- Access to image source APIs
- Design tool accounts (optional)

## Setup Steps

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your API keys
nano .env
```

### 2. API Key Setup
You'll need API keys for:
- **Image Sources**: Shutterstock, Adobe Stock, Unsplash, Pexels
- **AI Generation**: OpenAI DALL-E, Stability AI, RunwayML
- **Design Tools**: Figma, Canva, Adobe Creative (optional)

### 3. Test Installation
```bash
# Test Design Decision Team
python design_decision_team.py

# Test Software Factory Integration
python software_factory_integration.py
```

### 4. Integration with Software Factory
```bash
# Add to your existing Software Factory
from design_decision_team.software_factory_integration import EnhancedSoftwareFactoryOrchestrator

# Use enhanced orchestrator
orchestrator = EnhancedSoftwareFactoryOrchestrator()
result = await orchestrator.process_idea_with_design(idea_description, owner_id, design_requirements)
```

## Usage Examples

### Basic Design Request
```python
from design_decision_team.design_decision_team import DesignDecisionTeam, DesignRequest, DesignRequestType

# Create design request
request = DesignRequest(
    id="weight_tracker_splash_001",
    project_id="weight_tracker_mobile",
    request_type=DesignRequestType.SPLASH_SCREEN,
    description="Create morphing transformation splash screen",
    requirements={"quality": "high", "animation_type": "morphing"},
    budget_tier="ai_generated",
    timeline="urgent",
    target_platform="mobile"
)

# Process request
design_team = DesignDecisionTeam()
decision = await design_team.process_design_request(request)
```

### Software Factory Integration
```python
from design_decision_team.software_factory_integration import EnhancedSoftwareFactoryOrchestrator

# Enhanced orchestrator with design capabilities
orchestrator = EnhancedSoftwareFactoryOrchestrator()

# Process idea with design integration
result = await orchestrator.process_idea_with_design(
    idea_description="AI-powered fitness app",
    owner_id="user_123",
    design_requirements={
        "brand_guidelines": {"colors": ["#667eea", "#4CAF50"]},
        "user_personas": [{"age": "25-45", "interests": "fitness"}]
    }
)
```

## Agent Roles

### Design Chief Agent
- **Role**: Master coordinator and final decision maker
- **Responsibilities**: Synthesizes all recommendations, makes final design decisions
- **Tools**: Image source research, morphing technique research, design evaluation

### Image Research Sub-Team
1. **Copyright Research Agent**: Legal compliance and licensing
2. **Image Discovery Agent**: Source identification and quality assessment
3. **Source Connection Agent**: API integration and workflow management

### Specialized Agents
- **Morphing Specialist Agent**: Animation technique research and implementation
- **UX Evaluation Agent**: User experience quality and coherence
- **Brand Manager Agent**: Brand consistency and visual identity

## Quality Metrics

### Design Quality Scores (0-100)
- **Overall Quality**: Comprehensive design assessment
- **UX Score**: User experience quality
- **Brand Consistency**: Brand alignment and consistency
- **Technical Implementation**: Technical feasibility and performance

### Success Criteria
- **Design Decision Time**: < 2 hours
- **Image Source Resolution**: < 30 minutes
- **Morphing Implementation**: < 4 hours
- **Overall Design Cycle**: < 1 day

## Troubleshooting

### Common Issues
1. **API Key Errors**: Verify all API keys are correctly set in .env
2. **CrewAI Errors**: Ensure CrewAI is properly installed with all dependencies
3. **Image Source Failures**: Check API rate limits and quotas
4. **Morphing Technique Issues**: Verify platform compatibility

### Performance Optimization
1. **Cache API Responses**: Implement caching for frequently used image sources
2. **Parallel Processing**: Use async/await for concurrent agent processing
3. **Resource Management**: Monitor memory usage for large image processing
4. **Error Handling**: Implement robust error handling and retry logic

## Support
For issues and questions:
1. Check the troubleshooting section
2. Review agent logs for detailed error information
3. Verify API key permissions and quotas
4. Test individual agents before full team processing
EOF

print_status "Setup instructions created"

# Create example configurations
print_info "Creating example configurations..."

# Weight Tracker Example
cat > project-starter/templates/ai_agents/design_decision_team/examples/weight_tracker_example.py << 'EOF'
"""
Weight Tracker Design Request Example
Demonstrates Design Decision Team for morphing transformation splash screen
"""

import asyncio
from design_decision_team.design_decision_team import DesignDecisionTeam, DesignRequest, DesignRequestType

async def weight_tracker_design_example():
    """Example design request for weight tracker morphing splash screen"""
    
    # Create design request for weight tracker
    request = DesignRequest(
        id="weight_tracker_splash_001",
        project_id="weight_tracker_mobile",
        request_type=DesignRequestType.SPLASH_SCREEN,
        description="Create morphing transformation splash screen showing cartoon people transforming from overweight to fit",
        requirements={
            "quality": "high",
            "performance": "high",
            "animation_type": "morphing",
            "character_style": "cartoon",
            "transformation": "overweight_to_fit",
            "motivational": True,
            "engaging": True
        },
        budget_tier="ai_generated",
        timeline="urgent",
        target_platform="mobile",
        brand_guidelines={
            "colors": ["#667eea", "#4CAF50", "#fff"],
            "style": "modern",
            "tone": "motivational",
            "target_audience": "fitness_enthusiasts"
        },
        user_personas=[
            {
                "age": "25-45",
                "interests": "fitness",
                "tech_savvy": "high",
                "goals": "weight_tracking",
                "motivation": "transformation"
            }
        ]
    )
    
    # Process design request
    design_team = DesignDecisionTeam()
    decision = await design_team.process_design_request(request)
    
    print(f"Design Decision for Weight Tracker:")
    print(f"Project ID: {decision.request_id}")
    print(f"Recommended Morphing: {decision.recommended_morphing.technique.value}")
    print(f"Quality Scores: {decision.quality_scores}")
    print(f"Estimated Timeline: {decision.estimated_timeline}")
    print(f"Estimated Cost: {decision.estimated_cost}")
    
    return decision

if __name__ == "__main__":
    asyncio.run(weight_tracker_design_example())
EOF

print_status "Example configurations created"

# Create validation script
print_info "Creating validation script..."
cat > project-starter/templates/ai_agents/design_decision_team/validate_setup.py << 'EOF'
"""
Design Decision Team Setup Validation
Validates that all components are properly configured
"""

import os
import sys
from pathlib import Path

def validate_environment():
    """Validate environment configuration"""
    print("🔍 Validating Design Decision Team Setup...")
    
    # Check Python dependencies
    required_packages = [
        'crewai',
        'requests',
        'PIL',
        'cv2',
        'reportlab'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    # Check environment file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Environment file exists")
    else:
        print("❌ Environment file missing")
        print("   Run: cp .env.template .env")
    
    # Check API keys
    required_keys = [
        'OPENAI_API_KEY',
        'UNSPLASH_API_KEY',
        'PEXELS_API_KEY'
    ]
    
    missing_keys = []
    for key in required_keys:
        if os.getenv(key):
            print(f"✅ {key} - Set")
        else:
            missing_keys.append(key)
            print(f"❌ {key} - Missing")
    
    # Summary
    print("\n📊 Validation Summary:")
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install crewai[all] requests pillow opencv-python reportlab")
    
    if missing_keys:
        print(f"❌ Missing API keys: {', '.join(missing_keys)}")
        print("   Add keys to .env file")
    
    if not missing_packages and not missing_keys:
        print("✅ All components properly configured!")
        return True
    else:
        print("❌ Setup incomplete. Please fix issues above.")
        return False

if __name__ == "__main__":
    success = validate_environment()
    sys.exit(0 if success else 1)
EOF

print_status "Validation script created"

# Create quick start script
print_info "Creating quick start script..."
cat > project-starter/templates/ai_agents/design_decision_team/quick_start.py << 'EOF'
"""
Design Decision Team Quick Start
Demonstrates the team with a simple design request
"""

import asyncio
import os
from design_decision_team.design_decision_team import DesignDecisionTeam, DesignRequest, DesignRequestType

async def quick_start():
    """Quick start example"""
    
    print("🎨 Design Decision Team Quick Start")
    print("=" * 50)
    
    # Check if we have required API keys
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Please set your OpenAI API key in .env file")
        return
    
    # Create a simple design request
    request = DesignRequest(
        id="quick_start_001",
        project_id="demo_project",
        request_type=DesignRequestType.SPLASH_SCREEN,
        description="Create a simple splash screen for a fitness app",
        requirements={
            "quality": "medium",
            "style": "modern",
            "colors": "blue_green"
        },
        budget_tier="free",
        timeline="standard",
        target_platform="mobile"
    )
    
    print(f"📋 Processing design request: {request.description}")
    
    try:
        # Initialize design team
        design_team = DesignDecisionTeam()
        
        # Process request
        decision = await design_team.process_design_request(request)
        
        print("\n🎉 Design Decision Complete!")
        print(f"Request ID: {decision.request_id}")
        print(f"Quality Scores: {decision.quality_scores}")
        print(f"Timeline: {decision.estimated_timeline}")
        print(f"Cost: {decision.estimated_cost}")
        
    except Exception as e:
        print(f"❌ Error processing design request: {e}")
        print("   Please check your setup and API keys")

if __name__ == "__main__":
    asyncio.run(quick_start())
EOF

print_status "Quick start script created"

# Final setup summary
print_header "Design Decision Team Setup Complete!"

print_info "📁 Directory Structure:"
echo "   project-starter/templates/ai_agents/design_decision_team/"
echo "   ├── agents.yaml                    # CrewAI agent configuration"
echo "   ├── design_decision_team.py       # Main team implementation"
echo "   ├── software_factory_integration.py # Software Factory integration"
echo "   ├── .env.template                 # Environment configuration template"
echo "   ├── SETUP_INSTRUCTIONS.md         # Detailed setup instructions"
echo "   ├── validate_setup.py             # Setup validation script"
echo "   ├── quick_start.py                # Quick start example"
echo "   └── examples/                     # Example configurations"

print_info "🚀 Next Steps:"
echo "   1. Copy .env.template to .env and add your API keys"
echo "   2. Run: python validate_setup.py"
echo "   3. Run: python quick_start.py"
echo "   4. Test with weight tracker: python examples/weight_tracker_example.py"

print_info "🔧 Integration with Software Factory:"
echo "   from design_decision_team.software_factory_integration import EnhancedSoftwareFactoryOrchestrator"
echo "   orchestrator = EnhancedSoftwareFactoryOrchestrator()"
echo "   result = await orchestrator.process_idea_with_design(idea_description, owner_id, design_requirements)"

print_status "Design Decision Team is ready for state-of-the-art 2025 design automation!"

print_warning "Remember to:"
echo "   - Set up API keys for image sources"
echo "   - Configure budget tiers based on your needs"
echo "   - Test with small projects before full deployment"
echo "   - Monitor API usage and costs"

print_header "🎨 Your Software Factory now has professional-grade design automation!"
