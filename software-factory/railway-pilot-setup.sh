#!/bin/bash
# Railway Pilot Setup Script
# Controlled evaluation of Railway deployment platform

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

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🚀 $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header "Setting up Railway Pilot Evaluation..."

# Create pilot project directory
mkdir -p railway-pilot
cd railway-pilot

# Create pilot project (weight tracker)
print_info "Creating pilot project: weight-tracker-railway..."

# Copy weight tracker as base (from software-factory directory)
cp -r ../generated-apps/weight-tracker-nextjs ./weight-tracker-railway
cd weight-tracker-railway

# Create Railway configuration
print_info "Creating Railway configuration..."

cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm run start",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# Create nixpacks.toml for better build control
cat > nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["nodejs", "npm"]

[phases.install]
cmds = ["npm ci"]

[phases.build]
cmds = ["npm run build"]

[start]
cmd = "npm run start"
EOF

# Create Railway deployment script
cat > deploy-railway.sh << 'EOF'
#!/bin/bash
# Railway Deployment Script

set -e

echo "🚀 Deploying to Railway..."

# Check if Railway CLI is available
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it manually:"
    echo "   npm install -g @railway/cli"
    echo "   Then run this script again."
    exit 1
fi

# Login to Railway
echo "Logging into Railway..."
railway login

# Create new project
echo "Creating Railway project..."
railway project create weight-tracker-pilot

# Link to existing project
echo "Linking to project..."
railway link

# Set environment variables
echo "Setting environment variables..."
railway variables set NODE_ENV=production
railway variables set PORT=3000

# Deploy
echo "Deploying application..."
railway up

echo "✅ Deployment complete!"
echo "Your app is available at: https://weight-tracker-pilot-production.up.railway.app"
EOF

chmod +x deploy-railway.sh

# Create evaluation checklist
cat > RAILWAY_EVALUATION.md << 'EOF'
# Railway Pilot Evaluation Checklist

## Setup Phase
- [ ] Install Railway CLI
- [ ] Create Railway account
- [ ] Link project to Railway
- [ ] Configure environment variables
- [ ] Deploy application

## Functionality Testing
- [ ] Application starts successfully
- [ ] All routes work correctly
- [ ] Database connections work
- [ ] Environment variables are loaded
- [ ] Static assets are served

## Performance Testing
- [ ] Cold start time < 10 seconds
- [ ] Response time < 500ms
- [ ] Memory usage < 512MB
- [ ] CPU usage reasonable

## Deployment Experience
- [ ] One-command deployment works
- [ ] Environment variable management
- [ ] Log access and monitoring
- [ ] Rollback capability
- [ ] Custom domain support

## Cost Analysis
- [ ] Monthly cost estimate
- [ ] Resource usage tracking
- [ ] Scaling costs
- [ ] Comparison to current setup

## Integration Testing
- [ ] Supabase connection works
- [ ] MCP servers can be deployed
- [ ] GitHub integration
- [ ] CI/CD pipeline compatibility

## Decision Criteria
- [ ] Deployment simplicity (1-5)
- [ ] Performance (1-5)
- [ ] Cost effectiveness (1-5)
- [ ] Developer experience (1-5)
- [ ] Integration ease (1-5)

**Overall Recommendation**: [ ] Adopt / [ ] Reject / [ ] Further testing needed
EOF

# Create comparison analysis
cat > RAILWAY_VS_ALTERNATIVES.md << 'EOF'
# Railway vs Alternatives Analysis

## Current Setup (GitHub Actions + Docker)
**Pros:**
- Full control over build process
- No vendor lock-in
- Free for public repos
- Extensive customization

**Cons:**
- Complex setup
- Manual deployment steps
- No built-in monitoring
- Requires separate hosting

## Railway
**Pros:**
- One-command deployment
- Built-in monitoring
- Automatic scaling
- Simple configuration
- Good free tier

**Cons:**
- Vendor lock-in
- Less customization
- Pricing can scale quickly
- Limited to supported stacks

## Vercel (Current Alternative)
**Pros:**
- Excellent Next.js integration
- Great performance
- Simple deployment
- Good free tier

**Cons:**
- Limited to frontend/static
- No backend services
- Limited database options

## AWS/GCP/Azure
**Pros:**
- Full control
- Enterprise features
- Extensive services
- No vendor lock-in

**Cons:**
- Complex setup
- Steep learning curve
- High costs
- Overkill for most projects

## Recommendation Matrix

| Criteria | GitHub Actions | Railway | Vercel | AWS |
|----------|---------------|---------|---------|-----|
| Simplicity | 2/5 | 5/5 | 5/5 | 1/5 |
| Control | 5/5 | 3/5 | 2/5 | 5/5 |
| Cost | 5/5 | 4/5 | 5/5 | 2/5 |
| Performance | 4/5 | 4/5 | 5/5 | 5/5 |
| Integration | 3/5 | 4/5 | 5/5 | 3/5 |
EOF

print_status "Railway pilot setup complete!"
print_info "Next steps:"
print_info "1. Run: cd railway-pilot/weight-tracker-railway"
print_info "2. Run: ./deploy-railway.sh"
print_info "3. Follow evaluation checklist in RAILWAY_EVALUATION.md"
print_info "4. Complete comparison analysis in RAILWAY_VS_ALTERNATIVES.md"
