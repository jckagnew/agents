#!/bin/bash
# =============================================================================
# LINT ALL SCRIPT
# =============================================================================
# Comprehensive linting script for all supported technologies
# =============================================================================

set -e  # Exit on any error

# =============================================================================
# CONFIGURATION
# =============================================================================
PYTHON_SRC_DIRS="src/ tests/"
JAVASCRIPT_SRC_DIRS="src/ tests/"
PYTHON_MIN_COVERAGE=80
JAVASCRIPT_MIN_COVERAGE=80

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
# PYTHON LINTING
# =============================================================================
lint_python() {
    print_header "PYTHON LINTING"
    
    # Check if Python files exist
    if ! find . -name "*.py" -path "./src/*" -o -path "./tests/*" | grep -q .; then
        print_warning "No Python files found in src/ or tests/"
        return 0
    fi
    
    echo "🔍 Running Black (code formatting)..."
    if command -v black &> /dev/null; then
        black --check $PYTHON_SRC_DIRS || {
            print_error "Black formatting issues found. Run: black $PYTHON_SRC_DIRS"
            return 1
        }
        print_success "Black formatting check passed"
    else
        print_warning "Black not installed. Install with: pip install black"
    fi
    
    echo "🔍 Running isort (import sorting)..."
    if command -v isort &> /dev/null; then
        isort --check-only $PYTHON_SRC_DIRS || {
            print_error "isort import sorting issues found. Run: isort $PYTHON_SRC_DIRS"
            return 1
        }
        print_success "isort import sorting check passed"
    else
        print_warning "isort not installed. Install with: pip install isort"
    fi
    
    echo "🔍 Running flake8 (style guide)..."
    if command -v flake8 &> /dev/null; then
        flake8 $PYTHON_SRC_DIRS || {
            print_error "flake8 style issues found"
            return 1
        }
        print_success "flake8 style check passed"
    else
        print_warning "flake8 not installed. Install with: pip install flake8"
    fi
    
    echo "🔍 Running MyPy (type checking)..."
    if command -v mypy &> /dev/null; then
        mypy $PYTHON_SRC_DIRS || {
            print_error "MyPy type checking issues found"
            return 1
        }
        print_success "MyPy type checking passed"
    else
        print_warning "MyPy not installed. Install with: pip install mypy"
    fi
    
    echo "🔍 Running Bandit (security scan)..."
    if command -v bandit &> /dev/null; then
        bandit -r $PYTHON_SRC_DIRS -f json -o bandit-report.json || {
            print_error "Bandit security issues found. Check bandit-report.json"
            return 1
        }
        print_success "Bandit security scan passed"
    else
        print_warning "Bandit not installed. Install with: pip install bandit"
    fi
    
    echo "🔍 Running Safety (dependency vulnerabilities)..."
    if command -v safety &> /dev/null; then
        safety check || {
            print_error "Safety dependency vulnerabilities found"
            return 1
        }
        print_success "Safety dependency check passed"
    else
        print_warning "Safety not installed. Install with: pip install safety"
    fi
    
    print_success "Python linting completed successfully"
}

# =============================================================================
# JAVASCRIPT/TYPESCRIPT LINTING
# =============================================================================
lint_javascript() {
    print_header "JAVASCRIPT/TYPESCRIPT LINTING"
    
    # Check if package.json exists
    if [ ! -f "package.json" ]; then
        print_warning "No package.json found. Skipping JavaScript linting."
        return 0
    fi
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_warning "node_modules not found. Run: npm install"
        return 1
    fi
    
    echo "🔍 Running ESLint (code quality)..."
    if npm list eslint &> /dev/null; then
        npm run lint || {
            print_error "ESLint issues found"
            return 1
        }
        print_success "ESLint check passed"
    else
        print_warning "ESLint not installed. Install with: npm install eslint"
    fi
    
    echo "🔍 Running Prettier (code formatting)..."
    if npm list prettier &> /dev/null; then
        npm run format:check || {
            print_error "Prettier formatting issues found. Run: npm run format"
            return 1
        }
        print_success "Prettier formatting check passed"
    else
        print_warning "Prettier not installed. Install with: npm install prettier"
    fi
    
    echo "🔍 Running TypeScript type checking..."
    if npm list typescript &> /dev/null; then
        npx tsc --noEmit || {
            print_error "TypeScript type checking issues found"
            return 1
        }
        print_success "TypeScript type checking passed"
    else
        print_warning "TypeScript not installed. Install with: npm install typescript"
    fi
    
    echo "🔍 Running NPM audit (security)..."
    npm audit --audit-level=moderate || {
        print_error "NPM audit found security vulnerabilities"
        return 1
    }
    print_success "NPM audit passed"
    
    print_success "JavaScript/TypeScript linting completed successfully"
}

# =============================================================================
# SECURITY LINTING
# =============================================================================
lint_security() {
    print_header "SECURITY LINTING"
    
    echo "🔍 Running detect-secrets (secret detection)..."
    if command -v detect-secrets &> /dev/null; then
        detect-secrets scan --baseline .secrets.baseline || {
            print_error "detect-secrets found potential secrets"
            return 1
        }
        print_success "detect-secrets scan passed"
    else
        print_warning "detect-secrets not installed. Install with: pip install detect-secrets"
    fi
    
    print_success "Security linting completed successfully"
}

# =============================================================================
# DOCUMENTATION LINTING
# =============================================================================
lint_documentation() {
    print_header "DOCUMENTATION LINTING"
    
    echo "🔍 Running Prettier on documentation..."
    if command -v prettier &> /dev/null; then
        prettier --check "*.md" "docs/**/*.md" || {
            print_error "Documentation formatting issues found. Run: prettier --write *.md docs/**/*.md"
            return 1
        }
        print_success "Documentation formatting check passed"
    else
        print_warning "Prettier not installed. Install with: npm install prettier"
    fi
    
    print_success "Documentation linting completed successfully"
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================
main() {
    print_header "COMPREHENSIVE LINTING SCRIPT"
    echo "Starting comprehensive linting for all supported technologies..."
    echo ""
    
    local exit_code=0
    
    # Run Python linting
    if ! lint_python; then
        exit_code=1
    fi
    echo ""
    
    # Run JavaScript/TypeScript linting
    if ! lint_javascript; then
        exit_code=1
    fi
    echo ""
    
    # Run security linting
    if ! lint_security; then
        exit_code=1
    fi
    echo ""
    
    # Run documentation linting
    if ! lint_documentation; then
        exit_code=1
    fi
    echo ""
    
    # Final result
    if [ $exit_code -eq 0 ]; then
        print_success "🎉 All linting completed successfully!"
        echo ""
        echo "Next steps:"
        echo "  • Run tests: npm test (or pytest)"
        echo "  • Build project: npm run build (or python setup.py build)"
        echo "  • Deploy: npm run deploy (or your deployment script)"
    else
        print_error "❌ Linting failed. Please fix the issues above and try again."
        echo ""
        echo "Quick fixes:"
        echo "  • Python: black src/ tests/ && isort src/ tests/"
        echo "  • JavaScript: npm run lint:fix && npm run format"
        echo "  • Security: npm audit fix"
    fi
    
    exit $exit_code
}

# =============================================================================
# SCRIPT EXECUTION
# =============================================================================
main "$@"
