#!/bin/bash

# =============================================================================
# PROJECT STARTER SETUP SCRIPT
# =============================================================================
# This script sets up a new project from the starter template
# =============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Get project name from current directory
PROJECT_NAME=$(basename "$(pwd)")
PROJECT_DIR="$(pwd)"

print_header "Setting up project: $PROJECT_NAME"

# =============================================================================
# STEP 1: ENVIRONMENT SETUP
# =============================================================================
print_info "Setting up environment variables..."

# Copy master .env file
if [ -f "/Users/jackagnew/projects/agents/env.master" ]; then
    cp "/Users/jackagnew/projects/agents/env.master" .env
    print_status "Environment variables copied from master"
    
    # For Next.js projects, also create .env.local
    if [ -f "package.json" ] && grep -q "next" package.json; then
        cp "/Users/jackagnew/projects/agents/env.master" .env.local
        print_status "Created .env.local for Next.js project"
    fi
    
    # For Python projects, also create .env in src/ if it exists
    if [ -d "src" ] && [ -f "pyproject.toml" ]; then
        cp "/Users/jackagnew/projects/agents/env.master" src/.env
        print_status "Created src/.env for Python project"
    fi
    
else
    print_warning "Master .env file not found, using example"
    cp env.example .env
fi

# =============================================================================
# STEP 2: GIT INITIALIZATION
# =============================================================================
print_info "Initializing Git repository..."

if [ ! -d ".git" ]; then
    git init
    print_status "Git repository initialized"
else
    print_info "Git repository already exists"
fi

# Add .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_warning "No .gitignore found, using template"
fi

# =============================================================================
# STEP 3: PACKAGE MANAGEMENT
# =============================================================================
print_info "Setting up package management..."

# Check if package.json exists
if [ ! -f "package.json" ]; then
    print_info "Creating package.json..."
    cat > package.json << EOF
{
  "name": "$PROJECT_NAME",
  "version": "1.0.0",
  "description": "A new project created from project-starter template",
  "main": "src/app.js",
  "scripts": {
    "dev": "./scripts/dev.sh",
    "test": "./scripts/test.sh",
    "deploy": "./scripts/deploy.sh",
    "github": "./scripts/github.sh"
  },
  "keywords": [],
  "author": "Jack Agnew",
  "license": "MIT",
  "dependencies": {
    "dotenv": "^16.0.0"
  },
  "devDependencies": {
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
EOF
    print_status "package.json created"
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_info "Creating requirements.txt..."
    cat > requirements.txt << EOF
# Core dependencies
python-dotenv>=1.0.0
requests>=2.31.0

# AI/ML libraries
openai>=1.0.0
anthropic>=0.7.0
google-generativeai>=0.3.0

# Web frameworks
fastapi>=0.104.0
uvicorn>=0.24.0
flask>=3.0.0

# Database
supabase>=2.0.0
sqlalchemy>=2.0.0

# Development tools
pytest>=7.4.0
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
EOF
    print_status "requirements.txt created"
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    print_info "Creating pyproject.toml..."
    cat > pyproject.toml << EOF
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$PROJECT_NAME"
version = "1.0.0"
description = "A new project created from project-starter template"
authors = [{name = "Jack Agnew", email = "jack@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "python-dotenv>=1.0.0",
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
EOF
    print_status "pyproject.toml created"
fi

# =============================================================================
# STEP 4: CREATE DIRECTORY STRUCTURE
# =============================================================================
print_info "Creating directory structure..."

# Create directories
mkdir -p src/components
mkdir -p tests
mkdir -p docs
mkdir -p scripts
mkdir -p templates/python
mkdir -p templates/javascript
mkdir -p templates/markdown
mkdir -p templates/ai
mkdir -p templates/agents
mkdir -p .vscode
mkdir -p .github/workflows
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources

print_status "Directory structure created"

# =============================================================================
# STEP 5: CREATE SCRIPTS
# =============================================================================
print_info "Creating utility scripts..."

# Development script
cat > scripts/dev.sh << 'EOF'
#!/bin/bash
# Development server script

echo "🚀 Starting development server..."

# Check if Python project
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "🐍 Python project detected"
    if [ -f "src/main.py" ]; then
        python src/main.py
    else
        echo "📝 Creating Python entry point..."
        cat > src/main.py << 'PYEOF'
#!/usr/bin/env python3
"""
Main entry point for the application
"""

import os
from dotenv import load_dotenv

def main():
    """Main function"""
    load_dotenv()
    print("🚀 Application started!")
    print(f"Project: {os.getenv('PROJECT_NAME', 'Unknown')}")
    print("Environment loaded successfully!")

if __name__ == "__main__":
    main()
PYEOF
        python src/main.py
    fi
fi

# Check if Node.js project
if [ -f "package.json" ]; then
    echo "📦 Node.js project detected"
    if [ -f "src/app.js" ]; then
        node src/app.js
    else
        echo "📝 Creating Node.js entry point..."
        cat > src/app.js << 'NEOF'
#!/usr/bin/env node
/**
 * Main entry point for the application
 */

require('dotenv').config();

function main() {
    console.log('🚀 Application started!');
    console.log(`Project: ${process.env.PROJECT_NAME || 'Unknown'}`);
    console.log('Environment loaded successfully!');
}

main();
NEOF
        node src/app.js
    fi
fi
EOF

# Test script
cat > scripts/test.sh << 'EOF'
#!/bin/bash
# Test runner script

echo "🧪 Running tests..."

# Python tests
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "🐍 Running Python tests..."
    if command -v pytest &> /dev/null; then
        pytest
    else
        echo "⚠️  pytest not installed, installing..."
        pip install pytest
        pytest
    fi
fi

# Node.js tests
if [ -f "package.json" ]; then
    echo "📦 Running Node.js tests..."
    if [ -f "package.json" ] && grep -q '"test"' package.json; then
        npm test
    else
        echo "⚠️  No test script found in package.json"
    fi
fi
EOF

# Deploy script
cat > scripts/deploy.sh << 'EOF'
#!/bin/bash
# Deployment script

echo "🚀 Deploying application..."

# Check for Vercel
if [ -f "vercel.json" ] || [ -d ".vercel" ]; then
    echo "▲ Deploying to Vercel..."
    if command -v vercel &> /dev/null; then
        vercel --prod
    else
        echo "⚠️  Vercel CLI not installed"
    fi
fi

# Check for other deployment configs
if [ -f "Dockerfile" ]; then
    echo "🐳 Docker deployment detected"
fi

if [ -f "docker-compose.yml" ]; then
    echo "🐳 Docker Compose deployment detected"
fi

echo "✅ Deployment complete!"
EOF

# GitHub script
cat > scripts/github.sh << 'EOF'
#!/bin/bash
# GitHub operations script

echo "🐙 GitHub operations..."

# Load environment
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI available"
    
    # Check authentication
    if gh auth status &> /dev/null; then
        echo "✅ GitHub authenticated"
        
        # Show available commands
        echo ""
        echo "Available commands:"
        echo "  gh pr create --repo owner/repo --title 'Title' --body 'Description'"
        echo "  gh pr status"
        echo "  gh pr list"
        echo "  gh repo create $PROJECT_NAME --public"
    else
        echo "⚠️  GitHub not authenticated"
        echo "Run: gh auth login"
    fi
else
    echo "⚠️  GitHub CLI not installed"
    echo "Install with: brew install gh"
fi
EOF

# Make scripts executable
chmod +x scripts/*.sh

print_status "Utility scripts created"

# =============================================================================
# STEP 6: CREATE VS CODE CONFIGURATION
# =============================================================================
print_info "Creating VS Code configuration..."

cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/node_modules": true,
        "**/.git": true,
        "**/.DS_Store": true
    },
    "terminal.integrated.defaultProfile.osx": "zsh"
}
EOF

print_status "VS Code configuration created"

# =============================================================================
# STEP 7: CREATE INITIAL FILES
# =============================================================================
print_info "Creating initial project files..."

# Create main Python file
if [ ! -f "src/main.py" ]; then
    cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main entry point for the application
"""

import os
from dotenv import load_dotenv

def main():
    """Main function"""
    load_dotenv()
    print("🚀 Application started!")
    print(f"Project: {os.getenv('PROJECT_NAME', 'Unknown')}")
    print("Environment loaded successfully!")

if __name__ == "__main__":
    main()
EOF
fi

# Create main Node.js file
if [ ! -f "src/app.js" ]; then
    cat > src/app.js << 'EOF'
#!/usr/bin/env node
/**
 * Main entry point for the application
 */

require('dotenv').config();

function main() {
    console.log('🚀 Application started!');
    console.log(`Project: ${process.env.PROJECT_NAME || 'Unknown'}`);
    console.log('Environment loaded successfully!');
}

main();
EOF
fi

# Create test file
cat > tests/test_basic.py << 'EOF'
"""
Basic tests for the application
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestBasic(unittest.TestCase):
    """Basic test cases"""
    
    def test_import(self):
        """Test that main module can be imported"""
        try:
            import main
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import main: {e}")
    
    def test_environment(self):
        """Test that environment variables are loaded"""
        from dotenv import load_dotenv
        load_dotenv()
        # Add your environment tests here
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
EOF

print_status "Initial project files created"

# =============================================================================
# STEP 7.5: CREATE AI AGENTS TEMPLATES
# =============================================================================
print_info "Creating AI agents templates..."

# Copy AI agents templates
if [ -d "/Users/jackagnew/projects/agents/project-starter/templates/ai-agents" ]; then
    cp -r "/Users/jackagnew/projects/agents/project-starter/templates/ai-agents" templates/
    print_status "AI agents templates copied"
fi

# Copy AI agents setup scripts
if [ -f "/Users/jackagnew/projects/agents/project-starter/scripts/setup-ai-agents.sh" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/scripts/setup-ai-agents.sh" scripts/
    chmod +x scripts/setup-ai-agents.sh
    print_status "AI agents setup script copied"
fi

# =============================================================================
# STEP 7.6: CREATE WEB FRAMEWORKS TEMPLATES
# =============================================================================
print_info "Creating web frameworks templates..."

# Copy web frameworks templates
if [ -d "/Users/jackagnew/projects/agents/project-starter/templates/web-frameworks" ]; then
    cp -r "/Users/jackagnew/projects/agents/project-starter/templates/web-frameworks" templates/
    print_status "Web frameworks templates copied"
fi

# Copy web frameworks setup scripts
if [ -f "/Users/jackagnew/projects/agents/project-starter/scripts/setup-web-frameworks.sh" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/scripts/setup-web-frameworks.sh" scripts/
    chmod +x scripts/setup-web-frameworks.sh
    print_status "Web frameworks setup script copied"
fi

# =============================================================================
# STEP 7.7: CREATE AI PLANNING TEMPLATES
# =============================================================================
print_info "Creating AI planning templates..."

# Copy AI planning templates
if [ -d "/Users/jackagnew/projects/agents/project-starter/templates/ai-planning" ]; then
    cp -r "/Users/jackagnew/projects/agents/project-starter/templates/ai-planning" templates/
    print_status "AI planning templates copied"
fi

# Copy AI planning setup scripts
if [ -f "/Users/jackagnew/projects/agents/project-starter/scripts/setup-cursor-planning.sh" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/scripts/setup-cursor-planning.sh" scripts/
    chmod +x scripts/setup-cursor-planning.sh
    print_status "AI planning setup script copied"
fi

# =============================================================================
# STEP 7.8: CREATE MOBILE DEVELOPMENT TEMPLATES
# =============================================================================
print_info "Creating mobile development templates..."

# Copy mobile development templates
if [ -d "/Users/jackagnew/projects/agents/project-starter/templates/mobile" ]; then
    cp -r "/Users/jackagnew/projects/agents/project-starter/templates/mobile" templates/
    print_status "Mobile development templates copied"
fi

# Copy mobile setup scripts
if [ -f "/Users/jackagnew/projects/agents/project-starter/scripts/setup-mobile.sh" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/scripts/setup-mobile.sh" scripts/
    chmod +x scripts/setup-mobile.sh
    print_status "Mobile setup script copied"
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/scripts/create-mobile-project.sh" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/scripts/create-mobile-project.sh" scripts/
    chmod +x scripts/create-mobile-project.sh
    print_status "Mobile project creation script copied"
fi

# =============================================================================
# STEP 7.9: CREATE MCP INTEGRATION TEMPLATES
# =============================================================================
print_info "Creating MCP integration templates..."

# Copy MCP templates
if [ -d "/Users/jackagnew/projects/agents/project-starter/templates/mcp" ]; then
    cp -r "/Users/jackagnew/projects/agents/project-starter/templates/mcp" templates/
    print_status "MCP integration templates copied"
fi

# Copy MCP setup scripts
if [ -f "/Users/jackagnew/projects/agents/project-starter/templates/mcp/setup-mcp.sh" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/templates/mcp/setup-mcp.sh" scripts/
    chmod +x scripts/setup-mcp.sh
    print_status "MCP setup script copied"
fi

# Copy date components setup script
if [ -f "/Users/jackagnew/projects/agents/project-starter/scripts/setup-date-components.sh" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/scripts/setup-date-components.sh" scripts/
    chmod +x scripts/setup-date-components.sh
    print_status "Date components setup script copied"
fi

# =============================================================================
# STEP 7.6: CREATE AI COLLABORATION TEMPLATES
# =============================================================================
print_info "Creating AI collaboration templates..."

# Copy AI collaboration templates
if [ -f "/Users/jackagnew/projects/agents/project-starter/templates/ai/ai_collaboration_guide.md" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/templates/ai/ai_collaboration_guide.md" templates/ai/
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/templates/python/enhanced_ai_agent.py" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/templates/python/enhanced_ai_agent.py" templates/python/
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/templates/python/prompt_engineering_toolkit.py" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/templates/python/prompt_engineering_toolkit.py" templates/python/
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/templates/markdown/ai_collaboration_workflow.md" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/templates/markdown/ai_collaboration_workflow.md" templates/markdown/
fi

# Copy ShadCN UI agent templates
if [ -f "/Users/jackagnew/projects/agents/project-starter/templates/agents/shadcn_ui_agents.md" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/templates/agents/shadcn_ui_agents.md" templates/agents/
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/templates/python/shadcn_ui_agents.py" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/templates/python/shadcn_ui_agents.py" templates/python/
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/templates/markdown/shadcn_ui_workflow.md" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/templates/markdown/shadcn_ui_workflow.md" templates/markdown/
fi

# Copy additional configuration files
if [ -f "/Users/jackagnew/projects/agents/project-starter/.pre-commit-config.yaml" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/.pre-commit-config.yaml" .
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/Dockerfile" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/Dockerfile" .
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/docker-compose.yml" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/docker-compose.yml" .
fi

# Copy CI/CD workflows
if [ -d "/Users/jackagnew/projects/agents/project-starter/.github/workflows" ]; then
    cp -r "/Users/jackagnew/projects/agents/project-starter/.github/workflows" .github/
fi

# Copy monitoring configurations
if [ -d "/Users/jackagnew/projects/agents/project-starter/monitoring" ]; then
    cp -r "/Users/jackagnew/projects/agents/project-starter/monitoring" .
fi

# Copy documentation
if [ -f "/Users/jackagnew/projects/agents/project-starter/docs/DEVELOPMENT.md" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/docs/DEVELOPMENT.md" docs/
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/docs/API.md" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/docs/API.md" docs/
fi

# Copy additional configuration files
if [ -f "/Users/jackagnew/projects/agents/project-starter/tailwind.config.js" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/tailwind.config.js" .
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/next.config.js" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/next.config.js" .
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/jest.config.js" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/jest.config.js" .
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/jest.setup.js" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/jest.setup.js" .
fi

if [ -f "/Users/jackagnew/projects/agents/project-starter/playwright.config.ts" ]; then
    cp "/Users/jackagnew/projects/agents/project-starter/playwright.config.ts" .
fi

print_status "AI collaboration, ShadCN UI agent templates, and comprehensive tool configurations created"

# =============================================================================
# STEP 8: FINAL SETUP
# =============================================================================
print_info "Finalizing setup..."

# Update .env with project name
if [ -f ".env" ]; then
    # Add project name to .env
    if ! grep -q "PROJECT_NAME" .env; then
        echo "" >> .env
        echo "# Project Information" >> .env
        echo "PROJECT_NAME=$PROJECT_NAME" >> .env
        echo "PROJECT_VERSION=1.0.0" >> .env
    fi
fi

# Create initial commit
if [ -d ".git" ]; then
    git add .
    git commit -m "Initial commit: Project setup from template"
    print_status "Initial commit created"
fi

# =============================================================================
# COMPLETION
# =============================================================================
print_header "Project setup complete!"
echo ""
print_info "Your project '$PROJECT_NAME' is ready!"
echo ""
print_info "Next steps:"
echo "  1. Review and customize .env file"
echo "  2. Install dependencies:"
echo "     - Python: pip install -r requirements.txt"
echo "     - Node.js: npm install"
echo "  3. Start developing: ./scripts/dev.sh"
echo "  4. Run tests: ./scripts/test.sh"
echo "  5. Deploy: ./scripts/deploy.sh"
echo "  6. AI Agents development:"
echo "     - Setup AI agents environment: ./scripts/setup-ai-agents.sh"
echo "     - Create AI agent project: ./scripts/create-ai-agent-project.sh MyAgent --framework crewai"
echo "  7. Web Frameworks development:"
echo "     - Setup web frameworks environment: ./scripts/setup-web-frameworks.sh"
echo "     - Create web project: ./scripts/create-web-project.sh MyWebApp --framework nextjs"
echo "  8. AI Planning Layer:"
echo "     - Setup Cursor planning: ./scripts/setup-cursor-planning.sh"
echo "     - Use planning workflows: ./scripts/gap-analysis.sh"
echo "  9. Mobile development:"
echo "     - Setup mobile environment: ./scripts/setup-mobile.sh"
echo "     - Create mobile project: ./scripts/create-mobile-project.sh MyApp --type expo"
echo "  10. MCP Integration (NEW!):"
echo "     - Setup MCP integration: ./scripts/setup-mcp.sh"
echo "     - Setup US date components: ./scripts/setup-date-components.sh"
echo "     - Follow setup instructions: templates/mcp/SETUP_INSTRUCTIONS.md"
echo "     - Use MCP workflows: templates/mcp/workflow.sh"
echo ""
print_info "Happy coding! 🚀"
