#!/bin/bash

# Quick API Keys Configuration Script
# Helps you set up all API keys for Design Decision Team

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

print_header "Complete API Keys Setup for Design Decision Team"

# Check if we're in the right directory
if [ ! -f "design_decision_team.py" ]; then
    print_error "Please run this script from the Design Decision Team directory"
    echo "Run: cd project-starter/templates/ai_agents/design_decision_team/"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating .env file..."
    cp env_template.txt .env
    print_status ".env file created"
else
    print_info ".env file already exists"
fi

print_header "API Keys Configuration"

echo ""
print_info "Let's set up all the API keys. You can press Enter to skip any you don't have yet."

# OpenAI API Key
echo ""
print_info "🔑 OpenAI DALL-E 3 API (You mentioned you already have this):"
echo "   Go to: https://platform.openai.com/api-keys"
echo "   Copy your existing key (starts with 'sk-')"
read -p "Enter your OpenAI API key: " OPENAI_KEY

if [ ! -z "$OPENAI_KEY" ]; then
    if grep -q "OPENAI_API_KEY=" .env; then
        sed -i '' "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" .env
    else
        echo "OPENAI_API_KEY=$OPENAI_KEY" >> .env
    fi
    print_status "OpenAI API key configured"
else
    print_warning "Skipped OpenAI API key"
fi

# Unsplash API Key
echo ""
print_info "🔑 Unsplash API (FREE - 2 minutes to get):"
echo "   1. Go to: https://unsplash.com/developers"
echo "   2. Sign up/Login (free)"
echo "   3. Click 'Your apps' → 'New Application'"
echo "   4. Fill form: name='Design Decision Team', description='AI design automation'"
echo "   5. Accept terms, create app"
echo "   6. Copy 'Access Key'"
read -p "Enter your Unsplash API key: " UNSPLASH_KEY

if [ ! -z "$UNSPLASH_KEY" ]; then
    if grep -q "UNSPLASH_API_KEY=" .env; then
        sed -i '' "s/UNSPLASH_API_KEY=.*/UNSPLASH_API_KEY=$UNSPLASH_KEY/" .env
    else
        echo "UNSPLASH_API_KEY=$UNSPLASH_KEY" >> .env
    fi
    print_status "Unsplash API key configured"
else
    print_warning "Skipped Unsplash API key"
fi

# Stability AI API Key
echo ""
print_info "🔑 Stability AI API (CHEAP - $0.002/image):"
echo "   1. Go to: https://platform.stability.ai/"
echo "   2. Sign up/Login (free account)"
echo "   3. Navigate to 'API Keys'"
echo "   4. Click 'Create API Key'"
echo "   5. Copy key (starts with 'sk-')"
echo "   6. Add $10 deposit (minimum)"
read -p "Enter your Stability AI API key: " STABILITY_KEY

if [ ! -z "$STABILITY_KEY" ]; then
    if grep -q "STABILITY_API_KEY=" .env; then
        sed -i '' "s/STABILITY_API_KEY=.*/STABILITY_API_KEY=$STABILITY_KEY/" .env
    else
        echo "STABILITY_API_KEY=$STABILITY_KEY" >> .env
    fi
    print_status "Stability AI API key configured"
else
    print_warning "Skipped Stability AI API key"
fi

# Pexels API Key
echo ""
print_info "🔑 Pexels API (FREE - 2 minutes to get):"
echo "   1. Go to: https://www.pexels.com/api/"
echo "   2. Sign up/Login (free)"
echo "   3. Click 'Request API Key'"
echo "   4. Fill form: project='Design Decision Team'"
echo "   5. Submit, get instant approval"
echo "   6. Copy API key"
read -p "Enter your Pexels API key: " PEXELS_KEY

if [ ! -z "$PEXELS_KEY" ]; then
    if grep -q "PEXELS_API_KEY=" .env; then
        sed -i '' "s/PEXELS_API_KEY=.*/PEXELS_API_KEY=$PEXELS_KEY/" .env
    else
        echo "PEXELS_API_KEY=$PEXELS_KEY" >> .env
    fi
    print_status "Pexels API key configured"
else
    print_warning "Skipped Pexels API key"
fi

# Test configuration
echo ""
print_info "Testing your API configuration..."
python3 test_api_keys.py

# Show summary
echo ""
print_header "Configuration Summary"

print_info "📁 Your .env file now contains:"
if [ ! -z "$OPENAI_KEY" ]; then
    echo "✅ OpenAI DALL-E 3 API"
fi
if [ ! -z "$UNSPLASH_KEY" ]; then
    echo "✅ Unsplash API (FREE)"
fi
if [ ! -z "$STABILITY_KEY" ]; then
    echo "✅ Stability AI API"
fi
if [ ! -z "$PEXELS_KEY" ]; then
    echo "✅ Pexels API (FREE)"
fi

echo ""
print_info "🚀 Next Steps:"
echo "1. Test with weight tracker: python3 test_weight_tracker_integration.py"
echo "2. Generate cartoon characters: python3 quick_start.py"
echo "3. Use in your projects!"

echo ""
print_info "💰 Cost Summary:"
echo "• Unsplash: FREE"
echo "• Pexels: FREE"
echo "• OpenAI: $0.040 per image"
echo "• Stability AI: $0.002 per image"
echo "• Total for weight tracker: ~$0.40-$0.80"

echo ""
print_status "Your Design Decision Team is ready to generate professional cartoon characters! 🎨"

echo ""
print_info "📚 Need help getting API keys? Check: COMPLETE_API_SETUP.md"
