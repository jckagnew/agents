#!/bin/bash

# ===================================================================
# RECREATE MONOREPO STRUCTURE
# This script recreates the consolidation work on develop branch
# ===================================================================

set -e

echo "🔧 RECREATING MONOREPO STRUCTURE"
echo "================================="
echo ""
echo "This will transform the repository into the consolidated structure."
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

# Make sure we're on develop
git checkout develop || git checkout -b develop

echo ""
echo "Step 1: Create directory structure..."
mkdir -p apps/factory/src
mkdir -p apps/factory/docs
mkdir -p apps/admin-console
mkdir -p docs/deployment
mkdir -p docs/architecture
mkdir -p docs/api
mkdir -p scripts

echo "Step 2: Move existing src/ to apps/factory/..."
if [ -d "src" ]; then
    git mv src/* apps/factory/src/ 2>/dev/null || mv src/* apps/factory/src/
    rmdir src 2>/dev/null || true
fi

echo "Step 3: Move existing docs/ to apps/factory/..."
if [ -d "docs" ] && [ ! -d "apps/factory/docs" ]; then
    # docs exists but not as factory docs
    if [ "$(ls -A docs)" ]; then
        mv docs apps/factory/docs.tmp
        mkdir -p docs/deployment docs/architecture docs/api
        mv apps/factory/docs.tmp apps/factory/docs
    fi
fi

echo "Step 4: Move deployment docs to centralized location..."
if [ -f "WEB_DEPLOYMENT.md" ]; then
    git mv WEB_DEPLOYMENT.md docs/deployment/ 2>/dev/null || mv WEB_DEPLOYMENT.md docs/deployment/
fi

if [ -f "PHASE_1_DEPLOYMENT.md" ]; then
    git mv PHASE_1_DEPLOYMENT.md docs/deployment/ 2>/dev/null || mv PHASE_1_DEPLOYMENT.md docs/deployment/
fi

if [ -f "INTEGRATION_ROADMAP.md" ]; then
    git mv INTEGRATION_ROADMAP.md docs/deployment/ 2>/dev/null || mv INTEGRATION_ROADMAP.md docs/deployment/
fi

if [ -f "EXISTING_INFRASTRUCTURE_INTEGRATION.md" ]; then
    git mv EXISTING_INFRASTRUCTURE_INTEGRATION.md docs/deployment/ 2>/dev/null || mv EXISTING_INFRASTRUCTURE_INTEGRATION.md docs/deployment/
fi

if [ -f "REPOSITORY_CONSOLIDATION_PLAN.md" ]; then
    git mv REPOSITORY_CONSOLIDATION_PLAN.md docs/deployment/ 2>/dev/null || mv REPOSITORY_CONSOLIDATION_PLAN.md docs/deployment/
fi

echo "Step 5: Create Supabase config..."
if [ ! -f "supabase/config.toml" ]; then
    mkdir -p supabase
    cat > supabase/config.toml << 'EOF'
# Supabase Configuration
# Project: design-factory-admin (EXISTING PROJECT)
# Dashboard: https://supabase.com/dashboard/project/design-factory-admin

project_id = "design-factory-admin"

[api]
enabled = true
port = 54321
schemas = ["public", "storage", "graphql_public"]

[db]
port = 54322
major_version = 15

[studio]
enabled = true
port = 54323

[auth]
enabled = true
site_url = "http://localhost:19006"
enable_signup = true
EOF
fi

echo "Step 6: Create admin-console placeholder..."
cat > apps/admin-console/README.md << 'EOF'
# Admin Console

The Admin Console code exists on branch `claude/security-fixes-*`.

To integrate:
1. Checkout the security-fixes branch
2. Move admin-console/* here
3. Merge back to develop

**Status**: Security-hardened, ready for deployment
**Platforms**: iOS, Android, Web
EOF

echo "Step 7: Create environment scripts..."

# setup-env.sh
cat > scripts/setup-env.sh << 'SETUP_EOF'
#!/bin/bash
set -e
ENV_FILE="/home/user/agents/.env"
EXAMPLE_FILE="/home/user/agents/.env.example"

echo "🔧 Environment Setup"
if [ -f "$ENV_FILE" ]; then
    echo "⚠️  .env already exists"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo ""
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
fi

cp "$EXAMPLE_FILE" "$ENV_FILE"
echo "✅ Created .env from template"
echo "📝 Edit .env and add real credentials"
SETUP_EOF

chmod +x scripts/setup-env.sh

# validate-env.sh
cat > scripts/validate-env.sh << 'VALIDATE_EOF'
#!/bin/bash
set -e
ENV_FILE="/home/user/agents/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ No .env file found"
    exit 1
fi

echo "✅ .env file exists"
grep -q "SUPABASE_URL=" "$ENV_FILE" && echo "✅ SUPABASE_URL" || echo "❌ SUPABASE_URL"
grep -q "SUPABASE_ANON_KEY=" "$ENV_FILE" && echo "✅ SUPABASE_ANON_KEY" || echo "❌ SUPABASE_ANON_KEY"
VALIDATE_EOF

chmod +x scripts/validate-env.sh

echo "Step 8: Update package.json..."
# Update package.json paths
if [ -f "package.json" ]; then
    # Create backup
    cp package.json package.json.bak

    # Update paths (if they exist)
    sed -i 's|"api": "ts-node src/api/server.ts"|"api": "ts-node apps/factory/src/api/server.ts"|g' package.json 2>/dev/null || true
    sed -i 's|"api:dev": "nodemon --exec ts-node src/api/server.ts"|"api:dev": "nodemon --exec ts-node apps/factory/src/api/server.ts"|g' package.json 2>/dev/null || true

    # Add env scripts if not present
    if ! grep -q "env:setup" package.json; then
        # Add after other scripts (this is a simple approach)
        echo "Note: Manually add to package.json scripts:"
        echo '  "env:setup": "bash scripts/setup-env.sh",'
        echo '  "env:validate": "bash scripts/validate-env.sh"'
    fi
fi

echo ""
echo "✅ STRUCTURE CREATED"
echo ""
echo "Verify:"
echo "  ls -la apps/factory/"
echo "  ls -la docs/deployment/"
echo "  ls -la scripts/"
echo ""
echo "Commit:"
echo "  git add -A"
echo '  git commit -m "Consolidate to monorepo structure"'
echo "  git push origin develop"
echo ""
