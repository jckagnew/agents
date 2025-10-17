#!/bin/bash

# Quick API Keys Setup Script for Design Decision Team
# Helps you configure the essential API keys

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

print_header "Design Decision Team - API Keys Quick Setup"

# Check if we're in the right directory
if [ ! -f "design_decision_team.py" ]; then
    print_error "Please run this script from the Design Decision Team directory"
    echo "Run: cd project-starter/templates/ai_agents/design_decision_team/"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating .env file from template..."
    cp env_template.txt .env
    print_status ".env file created"
else
    print_info ".env file already exists"
fi

print_header "Essential API Keys Setup"

echo ""
print_info "To get the Design Decision Team working, you need at least 2 API keys:"
echo "1. OpenAI DALL-E 3 API (for custom cartoon characters)"
echo "2. Unsplash API (for free stock images)"

echo ""
print_warning "Let's set up these essential APIs:"

# OpenAI API Key Setup
echo ""
print_info "🔑 OpenAI DALL-E 3 API Setup:"
echo "1. Go to: https://platform.openai.com/"
echo "2. Sign up/Login to your account"
echo "3. Navigate to 'API Keys' section"
echo "4. Click 'Create new secret key'"
echo "5. Copy the key (starts with 'sk-')"
echo ""
read -p "Enter your OpenAI API key (or press Enter to skip): " OPENAI_KEY

if [ ! -z "$OPENAI_KEY" ]; then
    # Update .env file
    if grep -q "OPENAI_API_KEY=" .env; then
        sed -i '' "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" .env
    else
        echo "OPENAI_API_KEY=$OPENAI_KEY" >> .env
    fi
    print_status "OpenAI API key added to .env"
else
    print_warning "Skipped OpenAI API key"
fi

# Unsplash API Key Setup
echo ""
print_info "🔑 Unsplash API Setup:"
echo "1. Go to: https://unsplash.com/developers"
echo "2. Sign up/Login to Unsplash"
echo "3. Click 'Your apps' → 'New Application'"
echo "4. Fill out application form:"
echo "   - Application name: 'Design Decision Team'"
echo "   - Description: 'AI-powered design automation'"
echo "   - Website: Your website or GitHub"
echo "5. Accept terms and create application"
echo "6. Copy 'Access Key'"
echo ""
read -p "Enter your Unsplash API key (or press Enter to skip): " UNSPLASH_KEY

if [ ! -z "$UNSPLASH_KEY" ]; then
    # Update .env file
    if grep -q "UNSPLASH_API_KEY=" .env; then
        sed -i '' "s/UNSPLASH_API_KEY=.*/UNSPLASH_API_KEY=$UNSPLASH_KEY/" .env
    else
        echo "UNSPLASH_API_KEY=$UNSPLASH_KEY" >> .env
    fi
    print_status "Unsplash API key added to .env"
else
    print_warning "Skipped Unsplash API key"
fi

# Optional APIs
echo ""
print_info "🔑 Optional APIs (for enhanced functionality):"
echo "• Stability AI API - Alternative AI image generation"
echo "• Pexels API - Additional free images"
echo "• Shutterstock API - Premium commercial images"

echo ""
read -p "Do you want to set up optional APIs? (y/n): " SETUP_OPTIONAL

if [ "$SETUP_OPTIONAL" = "y" ] || [ "$SETUP_OPTIONAL" = "Y" ]; then
    # Stability AI
    echo ""
    read -p "Enter Stability AI API key (or press Enter to skip): " STABILITY_KEY
    if [ ! -z "$STABILITY_KEY" ]; then
        if grep -q "STABILITY_API_KEY=" .env; then
            sed -i '' "s/STABILITY_API_KEY=.*/STABILITY_API_KEY=$STABILITY_KEY/" .env
        else
            echo "STABILITY_API_KEY=$STABILITY_KEY" >> .env
        fi
        print_status "Stability AI API key added"
    fi
    
    # Pexels
    echo ""
    read -p "Enter Pexels API key (or press Enter to skip): " PEXELS_KEY
    if [ ! -z "$PEXELS_KEY" ]; then
        if grep -q "PEXELS_API_KEY=" .env; then
            sed -i '' "s/PEXELS_API_KEY=.*/PEXELS_API_KEY=$PEXELS_KEY/" .env
        else
            echo "PEXELS_API_KEY=$PEXELS_KEY" >> .env
        fi
        print_status "Pexels API key added"
    fi
fi

# Test API keys
echo ""
print_info "Testing configured API keys..."
python3 test_api_keys.py

# Final instructions
echo ""
print_header "Setup Complete!"

print_info "📁 Your .env file is configured with:"
if [ ! -z "$OPENAI_KEY" ]; then
    echo "✅ OpenAI DALL-E 3 API"
fi
if [ ! -z "$UNSPLASH_KEY" ]; then
    echo "✅ Unsplash API"
fi
if [ ! -z "$STABILITY_KEY" ]; then
    echo "✅ Stability AI API"
fi
if [ ! -z "$PEXELS_KEY" ]; then
    echo "✅ Pexels API"
fi

echo ""
print_info "🚀 Next Steps:"
echo "1. Test your setup: python3 test_api_keys.py"
echo "2. Run weight tracker test: python3 test_weight_tracker_integration.py"
echo "3. Use Design Decision Team in your projects!"

echo ""
print_info "📚 Documentation:"
echo "• API Keys Setup Guide: API_KEYS_SETUP_GUIDE.md"
echo "• Implementation Summary: IMPLEMENTATION_SUMMARY.md"
echo "• Quick Start: python3 quick_start.py"

echo ""
print_status "Your Design Decision Team is ready to generate professional-grade designs! 🎨"
