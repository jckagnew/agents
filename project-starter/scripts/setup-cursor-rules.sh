#!/bin/bash
# =============================================================================
# CURSOR RULES SETUP SCRIPT
# =============================================================================
# Sets up Cursor with optimal configuration based on Lee Robinson's best practices
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
print_header() {
    echo -e "${BLUE}=============================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=============================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# =============================================================================
# CURSOR RULES SETUP
# =============================================================================
setup_cursor_rules() {
    print_header "CURSOR RULES SETUP"
    
    # Check if .cursorrules exists
    if [ ! -f ".cursorrules" ]; then
        print_error ".cursorrules file not found!"
        echo "Please ensure you're in the project root directory."
        return 1
    fi
    
    print_success "Found .cursorrules file"
    
    # Check if Cursor is installed
    if ! command -v cursor &> /dev/null; then
        print_warning "Cursor not found in PATH"
        echo "Please install Cursor from https://cursor.com/"
        echo "Or add Cursor to your PATH"
        return 1
    fi
    
    print_success "Cursor is installed"
    
    # Create Cursor configuration directory
    CURSOR_CONFIG_DIR="$HOME/.cursor"
    if [ ! -d "$CURSOR_CONFIG_DIR" ]; then
        mkdir -p "$CURSOR_CONFIG_DIR"
        print_success "Created Cursor config directory"
    fi
    
    # Copy .cursorrules to project root (if not already there)
    if [ ! -f ".cursorrules" ]; then
        print_error ".cursorrules file not found in current directory"
        return 1
    fi
    
    print_success "Cursor rules are ready to use"
    
    # Display usage instructions
    echo ""
    print_header "USAGE INSTRUCTIONS"
    echo "1. Open Cursor in this project directory"
    echo "2. The .cursorrules file will be automatically loaded"
    echo "3. Use custom commands like @code-review, @fix-lint-errors"
    echo "4. Use @mentions for specific files or functions"
    echo "5. Start new chats for discrete features"
    echo ""
    echo "Custom commands available:"
    echo "  @code-review     - Review all changes for quality issues"
    echo "  @fix-lint-errors - Fix linting errors automatically"
    echo "  @security-scan   - Run security checks"
    echo "  @test-coverage   - Check test coverage"
    echo "  @refactor-suggestions - Get refactoring suggestions"
    echo ""
    echo "Context management:"
    echo "  @branch          - Reference current git branch"
    echo "  @commit          - Reference specific commit"
    echo "  @filename        - Reference specific file"
    echo "  @function        - Reference specific function"
    echo ""
}

# =============================================================================
# VS CODE EXTENSIONS SETUP
# =============================================================================
setup_vscode_extensions() {
    print_header "VS CODE EXTENSIONS SETUP"
    
    # Check if .vscode/extensions.json exists
    if [ ! -f ".vscode/extensions.json" ]; then
        print_warning ".vscode/extensions.json not found"
        echo "Creating recommended extensions list..."
        
        # Create .vscode directory if it doesn't exist
        mkdir -p ".vscode"
        
        # Create extensions.json
        cat > ".vscode/extensions.json" << 'EOF'
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.mypy-type-checker",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-typescript-next",
    "ms-azuretools.vscode-docker",
    "eamodio.gitlens"
  ]
}
EOF
        print_success "Created .vscode/extensions.json"
    else
        print_success "Found .vscode/extensions.json"
    fi
    
    # Check if .vscode/settings.json exists
    if [ ! -f ".vscode/settings.json" ]; then
        print_warning ".vscode/settings.json not found"
        echo "Creating VS Code settings..."
        
        cat > ".vscode/settings.json" << 'EOF'
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "eslint.enable": true,
  "prettier.enable": true
}
EOF
        print_success "Created .vscode/settings.json"
    else
        print_success "Found .vscode/settings.json"
    fi
}

# =============================================================================
# PRE-COMMIT HOOKS SETUP
# =============================================================================
setup_precommit_hooks() {
    print_header "PRE-COMMIT HOOKS SETUP"
    
    # Check if pre-commit is installed
    if ! command -v pre-commit &> /dev/null; then
        print_warning "pre-commit not installed"
        echo "Installing pre-commit..."
        pip install pre-commit
        print_success "Installed pre-commit"
    else
        print_success "pre-commit is installed"
    fi
    
    # Check if .pre-commit-config.yaml exists
    if [ ! -f ".pre-commit-config.yaml" ]; then
        print_warning ".pre-commit-config.yaml not found"
        echo "Creating basic pre-commit configuration..."
        
        cat > ".pre-commit-config.yaml" << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
EOF
        print_success "Created .pre-commit-config.yaml"
    else
        print_success "Found .pre-commit-config.yaml"
    fi
    
    # Install pre-commit hooks
    if [ -f ".pre-commit-config.yaml" ]; then
        pre-commit install
        print_success "Installed pre-commit hooks"
    fi
}

# =============================================================================
# LINTING SETUP
# =============================================================================
setup_linting() {
    print_header "LINTING SETUP"
    
    # Check if package.json exists (JavaScript/TypeScript project)
    if [ -f "package.json" ]; then
        print_success "Found package.json - setting up JavaScript/TypeScript linting"
        
        # Install ESLint and Prettier if not already installed
        if ! npm list eslint &> /dev/null; then
            npm install --save-dev eslint prettier eslint-config-prettier eslint-plugin-prettier
            print_success "Installed ESLint and Prettier"
        fi
        
        # Create .eslintrc.js if it doesn't exist
        if [ ! -f ".eslintrc.js" ]; then
            print_warning "Creating .eslintrc.js..."
            # This would be created by the main setup script
        fi
        
        # Create .prettierrc if it doesn't exist
        if [ ! -f ".prettierrc" ]; then
            print_warning "Creating .prettierrc..."
            # This would be created by the main setup script
        fi
    fi
    
    # Check if pyproject.toml exists (Python project)
    if [ -f "pyproject.toml" ]; then
        print_success "Found pyproject.toml - setting up Python linting"
        
        # Install Python linting tools if not already installed
        if ! command -v black &> /dev/null; then
            pip install black isort flake8 mypy bandit safety
            print_success "Installed Python linting tools"
        fi
    fi
    
    print_success "Linting setup complete"
}

# =============================================================================
# GIT SETUP
# =============================================================================
setup_git() {
    print_header "GIT SETUP"
    
    # Check if git is initialized
    if [ ! -d ".git" ]; then
        print_warning "Git not initialized"
        echo "Initializing git repository..."
        git init
        print_success "Initialized git repository"
    else
        print_success "Git repository found"
    fi
    
    # Create .gitignore if it doesn't exist
    if [ ! -f ".gitignore" ]; then
        print_warning "Creating .gitignore..."
        cat > ".gitignore" << 'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Build outputs
dist/
build/
*.egg-info/

# Coverage
coverage/
.nyc_output/
.coverage

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Linting
.eslintcache
.mypy_cache/
.pytest_cache/
bandit-report.json
EOF
        print_success "Created .gitignore"
    else
        print_success "Found .gitignore"
    fi
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================
main() {
    print_header "CURSOR RULES SETUP SCRIPT"
    echo "Setting up Cursor with optimal configuration based on Lee Robinson's best practices"
    echo ""
    
    # Run setup functions
    setup_cursor_rules
    echo ""
    
    setup_vscode_extensions
    echo ""
    
    setup_precommit_hooks
    echo ""
    
    setup_linting
    echo ""
    
    setup_git
    echo ""
    
    # Final instructions
    print_header "SETUP COMPLETE!"
    echo ""
    print_success "🎉 Cursor rules setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Open Cursor in this project directory"
    echo "2. Install recommended extensions when prompted"
    echo "3. Start using custom commands like @code-review"
    echo "4. Create new chats for discrete features"
    echo "5. Use @mentions for specific context"
    echo ""
    echo "Custom commands available:"
    echo "  @code-review     - Review all changes for quality issues"
    echo "  @fix-lint-errors - Fix linting errors automatically"
    echo "  @security-scan   - Run security checks"
    echo "  @test-coverage   - Check test coverage"
    echo "  @refactor-suggestions - Get refactoring suggestions"
    echo ""
    echo "Happy coding with Cursor! 🚀"
}

# =============================================================================
# SCRIPT EXECUTION
# =============================================================================
main "$@"
