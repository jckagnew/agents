#!/bin/bash

# Cloud deployment script for ntfy.sh integration
# This script helps deploy ntfy.sh to the cloud for a resilient solution

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo "🌐 ntfy.sh Cloud Deployment Script"
echo "=================================="

# Function to deploy to Railway
deploy_railway() {
    print_info "Deploying to Railway..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI not found. Please install it first:"
        echo "npm install -g @railway/cli"
        echo "railway login"
        return 1
    fi
    
    # Create railway.json configuration
    cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "ntfy serve --base-url=$RAILWAY_PUBLIC_DOMAIN",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

    # Create Dockerfile for Railway
    cat > Dockerfile << 'EOF'
FROM binwiederhier/ntfy:latest

# Expose port
EXPOSE 8080

# Set environment variables
ENV NTFY_BASE_URL=""
ENV NTFY_LISTEN_HTTP=":8080"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Start ntfy
CMD ["ntfy", "serve", "--base-url=$RAILWAY_PUBLIC_DOMAIN"]
EOF

    print_info "Deploying to Railway..."
    railway up
    
    print_status "Deployment initiated! Check Railway dashboard for progress."
    print_info "Once deployed, update your iPhone app with the Railway URL."
}

# Function to deploy to Render
deploy_render() {
    print_info "Deploying to Render..."
    
    # Create render.yaml configuration
    cat > render.yaml << 'EOF'
services:
  - type: web
    name: ntfy-notifications
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: NTFY_BASE_URL
        sync: false
    healthCheckPath: /health
EOF

    print_info "Render configuration created!"
    print_info "1. Push this code to GitHub"
    print_info "2. Connect your GitHub repo to Render"
    print_info "3. Deploy using the render.yaml configuration"
}

# Function to update Vercel integration
update_vercel() {
    print_info "Updating Vercel integration..."
    
    # Navigate to clevel-sales-guy directory
    if [ -d "../../clevel-sales-guy" ]; then
        cd ../../clevel-sales-guy
        
        # Add environment variables
        echo "" >> .env.local
        echo "# ntfy.sh Configuration" >> .env.local
        echo "NTFY_SERVER_URL=https://ntfy.sh" >> .env.local
        echo "NEXT_PUBLIC_APP_URL=https://clevelsalesguy.com" >> .env.local
        
        print_status "Vercel integration updated!"
        print_info "Deploy to Vercel: vercel --prod"
    else
        print_warning "clevel-sales-guy directory not found"
    fi
}

# Function to show deployment options
show_options() {
    echo ""
    echo "🚀 Deployment Options:"
    echo ""
    echo "1. Railway (Recommended for ntfy.sh)"
    echo "   - Free tier available"
    echo "   - Easy Docker deployment"
    echo "   - Automatic HTTPS"
    echo ""
    echo "2. Render"
    echo "   - Free tier available"
    echo "   - Good for Docker apps"
    echo "   - Custom domain support"
    echo ""
    echo "3. Vercel Integration (Use public ntfy.sh)"
    echo "   - Use existing ntfy.sh service"
    echo "   - Integrate with your website"
    echo "   - No additional hosting needed"
    echo ""
    echo "4. Hybrid (Local + Cloud)"
    echo "   - Keep local Docker for development"
    echo "   - Use cloud for production"
    echo "   - Best of both worlds"
}

# Main menu
echo ""
echo "Choose deployment option:"
echo "1) Railway"
echo "2) Render"
echo "3) Vercel Integration"
echo "4) Show all options"
echo "5) Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        deploy_railway
        ;;
    2)
        deploy_render
        ;;
    3)
        update_vercel
        ;;
    4)
        show_options
        ;;
    5)
        print_info "Exiting..."
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
print_status "Deployment process completed!"
print_info "Next steps:"
echo "1. Update your iPhone app with the new server URL"
echo "2. Test notifications from the admin panel"
echo "3. Configure your apps to use the new notification system"
