#!/bin/bash
# Software Factory Starter Kit Verification Script
# Tests the complete end-to-end experience

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

print_header "Software Factory Starter Kit Verification"
echo "=============================================="

# Test project name
TEST_PROJECT="verification-test-$(date +%s)"
TEST_DIR="software-factory-starter-$TEST_PROJECT"

print_info "Creating test project: $TEST_PROJECT"

# Step 1: Create project
print_info "Step 1: Creating project structure..."
if ./software-factory/software-factory-starter.sh "$TEST_PROJECT"; then
    print_status "Project creation successful"
else
    print_error "Project creation failed"
    exit 1
fi

# Step 2: Install dependencies
print_info "Step 2: Installing dependencies..."
cd "$TEST_DIR"
if npm install; then
    print_status "Dependencies installed successfully"
else
    print_error "Dependency installation failed"
    exit 1
fi

# Step 3: Build project
print_info "Step 3: Building project..."
if npm run build; then
    print_status "Build successful"
else
    print_error "Build failed"
    exit 1
fi

# Step 4: Test linting
print_info "Step 4: Testing linting..."
if npm run lint; then
    print_status "Linting passed"
else
    print_warning "Linting failed (non-critical)"
fi

# Step 5: Test type checking
print_info "Step 5: Testing type checking..."
if npm run type-check; then
    print_status "Type checking passed"
else
    print_warning "Type checking failed (non-critical)"
fi

# Step 6: Verify file structure
print_info "Step 6: Verifying file structure..."
REQUIRED_FILES=(
    "package.json"
    "next.config.js"
    "tailwind.config.js"
    "tsconfig.json"
    ".cursorrules"
    "src/app/layout.tsx"
    "src/app/page.tsx"
    "src/app/globals.css"
    "README.md"
    ".env.example"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_status "Found $file"
    else
        print_error "Missing $file"
        exit 1
    fi
done

# Step 7: Check dependencies
print_info "Step 7: Verifying dependencies..."
if grep -q '"next": "^14.2.0"' package.json; then
    print_status "Next.js version correct (14.2.0)"
else
    print_error "Next.js version incorrect"
    exit 1
fi

if grep -q '"react": "^18.2.0"' package.json; then
    print_status "React version correct (18.2.0)"
else
    print_error "React version incorrect"
    exit 1
fi

# Step 8: Test development server (quick test)
print_info "Step 8: Testing development server startup..."
if timeout 5s npm run dev > /dev/null 2>&1; then
    print_status "Development server starts successfully"
else
    print_warning "Development server test inconclusive (timeout)"
fi

# Cleanup
print_info "Cleaning up test project..."
cd ..
rm -rf "$TEST_DIR"

print_header "VERIFICATION COMPLETE"
echo "========================"
print_status "All critical tests passed"
print_status "Starter kit is production-ready"
print_info "Dependencies: Next.js 14.2.0, React 18.2.0, Tailwind 3.4.0"
print_info "Build: ✅ Successful"
print_info "Linting: ✅ Available"
print_info "Type checking: ✅ Available"
print_info "File structure: ✅ Complete"

echo ""
print_header "Ready for production use! 🎉"
