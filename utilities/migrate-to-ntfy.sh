#!/bin/bash

# Universal Migration Script: Pushover → ntfy.sh
# This script migrates all projects from Pushover to ntfy.sh

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

echo "🔄 Universal Migration: Pushover → ntfy.sh"
echo "=========================================="

# Get current IP address
get_current_ip() {
    ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}'
}

CURRENT_IP=$(get_current_ip)
NTFY_SERVER_URL="http://${CURRENT_IP}:8080"
NTFY_TOPIC="mytopic"

print_info "Current IP: $CURRENT_IP"
print_info "ntfy.sh Server: $NTFY_SERVER_URL"
print_info "Default Topic: $NTFY_TOPIC"

# Function to update environment files
update_env_files() {
    local project_dir="$1"
    local env_file="$2"
    
    if [ -f "$project_dir/$env_file" ]; then
        print_info "Updating $project_dir/$env_file"
        
        # Remove old Pushover variables
        sed -i.bak '/PUSHOVER_/d' "$project_dir/$env_file"
        
        # Add ntfy.sh variables
        cat >> "$project_dir/$env_file" << EOF

# ntfy.sh Configuration
NTFY_SERVER_URL=$NTFY_SERVER_URL
NTFY_TOPIC=$NTFY_TOPIC
EOF
        
        print_status "Updated $env_file"
    fi
}

# Function to update Python files
update_python_files() {
    local project_dir="$1"
    
    print_info "Updating Python files in $project_dir"
    
    # Find Python files that might contain Pushover references
    find "$project_dir" -name "*.py" -type f | while read -r file; do
        if grep -q "pushover\|Pushover" "$file"; then
            print_info "Updating $file"
            
            # Create backup
            cp "$file" "$file.backup"
            
            # Replace Pushover references with ntfy.sh
            sed -i.tmp 's/pushover/ntfy/g' "$file"
            sed -i.tmp 's/Pushover/ntfy.sh/g' "$file"
            sed -i.tmp 's/PUSHOVER_/NTFY_/g' "$file"
            
            # Remove temporary file
            rm -f "$file.tmp"
            
            print_status "Updated $file"
        fi
    done
}

# Function to create ntfy.sh integration
create_ntfy_integration() {
    local project_dir="$1"
    local integration_file="$project_dir/ntfy_integration.py"
    
    print_info "Creating ntfy.sh integration for $project_dir"
    
    cat > "$integration_file" << 'EOF'
#!/usr/bin/env python3
"""
ntfy.sh Integration Module
Universal notification service for all projects
"""

import os
import requests
from typing import Optional

class NtfyService:
    """Universal ntfy.sh notification service"""
    
    def __init__(self, server_url: str = None, topic: str = None):
        self.server_url = server_url or os.getenv('NTFY_SERVER_URL', 'http://192.168.0.146:8080')
        self.topic = topic or os.getenv('NTFY_TOPIC', 'mytopic')
    
    def send(self, message: str, title: str = None, priority: int = 3, url: str = None) -> bool:
        """Send a notification via ntfy.sh"""
        try:
            headers = {'Content-Type': 'text/plain'}
            if title:
                headers['X-Title'] = title
            if priority:
                headers['X-Priority'] = str(priority)
            if url:
                headers['X-Actions'] = f'view, Open Link, {url}'
            
            response = requests.post(
                f"{self.server_url}/{self.topic}",
                headers=headers,
                data=message,
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Failed to send notification: {e}")
            return False

# Global instance
ntfy = NtfyService()

# Convenience functions
def notify(message: str, title: str = None, priority: int = 3, url: str = None):
    """Send a notification"""
    return ntfy.send(message, title, priority, url)

def notify_success(message: str, title: str = "Success"):
    """Send a success notification"""
    return ntfy.send(message, title, 3)

def notify_error(message: str, title: str = "Error"):
    """Send an error notification"""
    return ntfy.send(message, title, 5)

def notify_info(message: str, title: str = "Info"):
    """Send an info notification"""
    return ntfy.send(message, title, 2)
EOF
    
    print_status "Created ntfy.sh integration: $integration_file"
}

# Main migration process
migrate_project() {
    local project_dir="$1"
    local project_name="$2"
    
    print_info "Migrating project: $project_name"
    
    if [ ! -d "$project_dir" ]; then
        print_warning "Project directory not found: $project_dir"
        return
    fi
    
    # Update environment files
    update_env_files "$project_dir" ".env"
    update_env_files "$project_dir" ".env.local"
    update_env_files "$project_dir" ".env.example"
    
    # Update Python files
    update_python_files "$project_dir"
    
    # Create ntfy.sh integration
    create_ntfy_integration "$project_dir"
    
    print_status "Migration completed for $project_name"
}

# Migrate all projects
echo ""
print_info "Starting migration of all projects..."

# Deep Research projects
migrate_project "2_openai/community_contributions/deep_research_with_pushover_report" "Deep Research with Pushover"

# Career Chatbot
migrate_project "1_foundations/community_contributions/amirna2_contributions/personal-ai" "Career Chatbot"

# C-Level Sales Guy (already has ntfy.sh integration)
print_info "C-Level Sales Guy already has ntfy.sh integration ✅"

# Financial Researcher
migrate_project "3_crew/financial_researcher" "Financial Researcher"

# Any other projects with notification modules
find . -name "notification.py" -type f | while read -r file; do
    project_dir=$(dirname "$file")
    project_name=$(basename "$project_dir")
    migrate_project "$project_dir" "$project_name"
done

# Create a global ntfy.sh configuration
print_info "Creating global ntfy.sh configuration..."

cat > "ntfy-global-config.env" << EOF
# Global ntfy.sh Configuration
# Copy this to your project's .env file

# ntfy.sh Server Configuration
NTFY_SERVER_URL=$NTFY_SERVER_URL
NTFY_TOPIC=$NTFY_TOPIC

# Alternative topics for different projects
NTFY_TOPIC_RESEARCH=mytopic
NTFY_TOPIC_CAREER=career
NTFY_TOPIC_FINANCIAL=financial
NTFY_TOPIC_SALES=sales

# Priority levels
NTFY_PRIORITY_LOW=1
NTFY_PRIORITY_NORMAL=3
NTFY_PRIORITY_HIGH=4
NTFY_PRIORITY_URGENT=5
EOF

print_status "Created global configuration: ntfy-global-config.env"

# Create a test script
cat > "test-ntfy-migration.sh" << 'EOF'
#!/bin/bash

# Test script for ntfy.sh migration
echo "🧪 Testing ntfy.sh migration..."

# Test basic notification
curl -d "Migration test successful! 🎉" http://192.168.0.146:8080/mytopic

# Test with title and priority
curl -d "High priority test" \
  -H "X-Title: Migration Test" \
  -H "X-Priority: 5" \
  http://192.168.0.146:8080/mytopic

echo "✅ Test notifications sent!"
EOF

chmod +x test-ntfy-migration.sh

print_status "Created test script: test-ntfy-migration.sh"

echo ""
print_status "🎉 Migration completed successfully!"
echo ""
print_info "Next steps:"
echo "1. Update your iPhone app with: $NTFY_SERVER_URL"
echo "2. Subscribe to topic: $NTFY_TOPIC"
echo "3. Test the migration: ./test-ntfy-migration.sh"
echo "4. Update your projects to use the new ntfy.sh integration"
echo ""
print_info "All projects now have ntfy.sh integration available!"
print_info "Use: from ntfy_integration import notify, notify_success, notify_error"
