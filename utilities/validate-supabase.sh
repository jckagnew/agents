#!/bin/bash

# Supabase Setup Validation Script
# This script validates that Supabase is properly configured and working

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
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

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "supabase-setup.sql" ]; then
    print_error "supabase-setup.sql not found. Please run this script from the project root."
    exit 1
fi

print_header "Supabase Setup Validation"

# Step 1: Check environment variables
print_header "1. Checking Environment Variables"

if [ -f "app/.env.local" ]; then
    print_success "Found app/.env.local"
    
    # Check Supabase URL
    if grep -q "NEXT_PUBLIC_SUPABASE_URL=https://mamfaakxnfczmcbmqtgg.supabase.co" app/.env.local; then
        print_success "Supabase URL is configured"
    else
        print_error "Supabase URL not found or incorrect"
    fi
    
    # Check Supabase Anon Key
    if grep -q "NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ" app/.env.local; then
        print_success "Supabase Anon Key is configured"
    else
        print_error "Supabase Anon Key not found or incorrect"
    fi
    
    # Check Service Role Key
    if grep -q "SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here" app/.env.local; then
        print_warning "Service Role Key is still placeholder - needs to be updated"
    elif grep -q "SUPABASE_SERVICE_ROLE_KEY=eyJ" app/.env.local; then
        print_success "Service Role Key is configured"
    else
        print_error "Service Role Key not found"
    fi
else
    print_error "app/.env.local not found"
fi

# Step 2: Check if SQL file exists and is valid
print_header "2. Checking SQL Setup File"

if [ -f "supabase-setup.sql" ]; then
    print_success "supabase-setup.sql found"
    
    # Check for key components in SQL
    if grep -q "CREATE TABLE users" supabase-setup.sql; then
        print_success "Users table definition found"
    else
        print_error "Users table definition missing"
    fi
    
    if grep -q "CREATE TABLE generations" supabase-setup.sql; then
        print_success "Generations table definition found"
    else
        print_error "Generations table definition missing"
    fi
    
    if grep -q "CREATE TABLE payments" supabase-setup.sql; then
        print_success "Payments table definition found"
    else
        print_error "Payments table definition missing"
    fi
    
    if grep -q "CREATE TABLE subscriptions" supabase-setup.sql; then
        print_success "Subscriptions table definition found"
    else
        print_error "Subscriptions table definition missing"
    fi
    
    if grep -q "ROW LEVEL SECURITY" supabase-setup.sql; then
        print_success "Row Level Security policies found"
    else
        print_error "Row Level Security policies missing"
    fi
else
    print_error "supabase-setup.sql not found"
fi

# Step 3: Check if app can start
print_header "3. Checking Application Dependencies"

if [ -d "app" ]; then
    print_success "App directory found"
    
    if [ -f "app/package.json" ]; then
        print_success "package.json found"
        
        # Check if node_modules exists
        if [ -d "app/node_modules" ]; then
            print_success "Dependencies installed"
        else
            print_warning "Dependencies not installed - run 'cd app && npm install'"
        fi
    else
        print_error "package.json not found in app directory"
    fi
else
    print_error "App directory not found"
fi

# Step 4: Manual validation steps
print_header "4. Manual Validation Steps Required"

print_info "To complete Supabase validation, you need to:"
echo ""
echo "1. Go to https://supabase.com/dashboard"
echo "2. Open your project: mamfaakxnfczmcbmqtgg"
echo "3. Go to SQL Editor"
echo "4. Copy and paste the contents of supabase-setup.sql"
echo "5. Click 'Run' to execute the SQL"
echo "6. Go to Settings > API"
echo "7. Copy the 'service_role' key"
echo "8. Update app/.env.local with the real service role key"
echo ""

# Step 5: Test connection (if service role key is set)
print_header "5. Testing Supabase Connection"

if grep -q "SUPABASE_SERVICE_ROLE_KEY=eyJ" app/.env.local; then
    print_info "Service role key found, testing connection..."
    
    # Try to start the app to test connection
    if [ -d "app/node_modules" ]; then
        print_info "Starting app to test Supabase connection..."
        cd app
        timeout 10s npm run dev > /dev/null 2>&1 &
        APP_PID=$!
        sleep 5
        
        # Check if app started successfully
        if kill -0 $APP_PID 2>/dev/null; then
            print_success "App started successfully - Supabase connection working"
            kill $APP_PID
        else
            print_warning "App failed to start - check Supabase configuration"
        fi
        cd ..
    else
        print_warning "Dependencies not installed - cannot test connection"
    fi
else
    print_warning "Service role key not set - cannot test connection"
    print_info "Complete the manual steps above to get your service role key"
fi

# Summary
print_header "Validation Summary"

echo ""
print_info "Next steps:"
echo "1. Run the SQL in Supabase dashboard (if not done already)"
echo "2. Get your service role key from Supabase"
echo "3. Update app/.env.local with the real service role key"
echo "4. Run 'cd app && npm install' (if not done already)"
echo "5. Run 'cd app && npm run dev' to start the app"
echo "6. Test user registration and name generation"
echo ""

print_info "For detailed setup instructions, see:"
echo "- QUICK_SUPABASE_SETUP.md"
echo "- STRIPE_SETUP_GUIDE.md"
echo ""

print_success "Validation complete!"
