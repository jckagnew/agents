#!/bin/bash

# Setup Universal Verification Framework
# Run this in any project to add systematic verification

echo "🔧 Setting up Universal Verification Framework..."
echo "================================================"

# Check if we're in a project directory
if [ ! -f "package.json" ]; then
    echo "❌ No package.json found. Please run this in a project directory."
    exit 1
fi

echo "✅ Found project directory"

# Copy verification templates
echo "📋 Copying verification templates..."

# Copy the verification script template
if [ ! -f "verify-implementation.js" ]; then
    cp ../verify-template.js verify-implementation.js
    echo "✅ Created verify-implementation.js"
else
    echo "⚠️  verify-implementation.js already exists, skipping"
fi

# Copy the verification shell script
if [ ! -f "verify.sh" ]; then
    cp ../verify-template.sh verify.sh
    chmod +x verify.sh
    echo "✅ Created verify.sh"
else
    echo "⚠️  verify.sh already exists, skipping"
fi

# Add verification scripts to package.json
echo "📦 Adding verification scripts to package.json..."

# Check if scripts already exist
if grep -q '"verify"' package.json; then
    echo "⚠️  Verification scripts already exist in package.json"
else
    # Add verification scripts
    node -e "
    const fs = require('fs');
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    pkg.scripts = pkg.scripts || {};
    pkg.scripts.verify = './verify.sh';
    pkg.scripts['test:integration'] = 'node verify-implementation.js';
    pkg.scripts['test:all'] = 'npm run test && npm run test:integration && npm run verify';
    fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
    console.log('✅ Added verification scripts to package.json');
    "
fi

# Create .env.example for verification configuration
if [ ! -f ".env.example" ]; then
    cat > .env.example << 'EOF'
# Verification Configuration
BASE_URL=http://localhost:3000
HEALTH_ENDPOINT=/health
TIMEOUT=30000
EOF
    echo "✅ Created .env.example with verification config"
fi

# Create verification documentation
if [ ! -f "VERIFICATION_GUIDE.md" ]; then
    cat > VERIFICATION_GUIDE.md << 'EOF'
# Verification Guide

## Quick Start

```bash
# Run comprehensive verification
npm run verify

# Or run just the integration test
npm run test:integration

# Run all tests including verification
npm run test:all
```

## Customization

1. Edit `verify-implementation.js` to add your specific tests
2. Update `verify.sh` if you need different health check endpoints
3. Set environment variables in `.env` for configuration

## What Gets Tested

- ✅ Basic connectivity
- ✅ Core functionality  
- ✅ Integration points
- ✅ End-to-end workflows
- ✅ Error handling

## Remember

**Only celebrate when ALL tests pass!**
EOF
    echo "✅ Created VERIFICATION_GUIDE.md"
fi

echo ""
echo "🎉 Verification framework setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit verify-implementation.js to add your specific tests"
echo "2. Update verify.sh if needed for your health check endpoint"
echo "3. Run 'npm run verify' to test your implementation"
echo ""
echo "Remember: Only celebrate when verification passes! 🎯"
