#!/bin/bash
# Sync Environment Variables from env.master to Project .env files

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

print_header "Syncing Environment Variables from env.master"

# Check if env.master exists
if [ ! -f "env.master" ]; then
    print_error "env.master file not found. Please run from the agents directory."
    exit 1
fi

# Function to sync env to a project
sync_to_project() {
    local project_path="$1"
    local env_file="$project_path/.env"
    local env_local_file="$project_path/.env.local"
    
    if [ -d "$project_path" ]; then
        print_info "Syncing to: $project_path"
        
        # Create .env file
        cp env.master "$env_file"
        print_status "Created/updated $env_file"
        
        # If it's a Next.js project, also create .env.local
        if [ -f "$project_path/package.json" ] && grep -q "next" "$project_path/package.json"; then
            cp env.master "$env_local_file"
            print_status "Created/updated $env_local_file"
        fi
    else
        print_warning "Project directory not found: $project_path"
    fi
}

# Sync to known projects
print_info "Syncing to known projects..."

# Business Name Generator
sync_to_project "test-projects/test-projects/business-name-generator"

# C Level Sales Guy
sync_to_project "clevel-sales-guy"

# Job Search Assistant
sync_to_project "job-search-assistant"

# My New Project
sync_to_project "my_new_project"

# Crew projects
sync_to_project "3_crew/debate"
sync_to_project "3_crew/coder"
sync_to_project "3_crew/engineering_team"
sync_to_project "3_crew/financial_researcher"
sync_to_project "3_crew/stock_picker"

print_status "Environment sync completed!"
print_info "All projects now have access to the latest API keys from env.master"
print_warning "Remember to add project-specific variables as needed"
