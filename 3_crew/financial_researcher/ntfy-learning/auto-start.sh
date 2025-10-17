#!/bin/bash

# Automated ntfy.sh startup script with dynamic IP detection
# This script detects the current IP address and updates the configuration

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

echo "🐳 ntfy.sh Auto-Start Script"
echo "=============================="

# Function to get the current IP address
get_current_ip() {
    # Try multiple methods to get the IP address
    local ip=""
    
    # Method 1: Get IP from ifconfig
    ip=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
    
    # Method 2: If ifconfig fails, try route command
    if [ -z "$ip" ]; then
        ip=$(route get default | grep interface | awk '{print $2}' | xargs ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}')
    fi
    
    # Method 3: If still no IP, try network utility
    if [ -z "$ip" ]; then
        ip=$(networksetup -getinfo "Wi-Fi" | grep "IP address" | awk '{print $3}')
    fi
    
    echo "$ip"
}

# Function to update docker-compose.yml with new IP
update_docker_compose() {
    local new_ip="$1"
    local compose_file="docker-compose.yml"
    
    print_info "Updating docker-compose.yml with IP: $new_ip"
    
    # Update the base URL in the command
    sed -i.bak "s|--base-url=http://[0-9.]*:8080|--base-url=http://$new_ip:8080|g" "$compose_file"
    
    # Update the environment variable
    sed -i.bak "s|NTFY_BASE_URL=http://[0-9.]*:8080|NTFY_BASE_URL=http://$new_ip:8080|g" "$compose_file"
    
    # Clean up backup files
    rm -f "$compose_file.bak"
    
    print_status "Docker Compose configuration updated"
}

# Function to update .env file
update_env_file() {
    local new_ip="$1"
    local env_file=".env"
    
    print_info "Updating .env file with IP: $new_ip"
    
    # Create or update .env file
    cat > "$env_file" << EOF
# ntfy.sh Configuration
NTFY_SERVER_IP=$new_ip
NTFY_SERVER_URL=http://$new_ip:8080
NTFY_TOPIC=mytopic

# Docker Configuration
DOCKER_COMPOSE_FILE=docker-compose.yml
EOF
    
    print_status ".env file updated"
}

# Function to start ntfy service
start_ntfy_service() {
    print_info "Starting ntfy service..."
    
    # Stop any existing service
    docker compose down 2>/dev/null || true
    
    # Start the service
    docker compose up -d
    
    # Wait for service to be healthy
    print_info "Waiting for service to be ready..."
    sleep 5
    
    # Check if service is running
    if docker ps | grep -q "ntfy"; then
        print_status "ntfy service is running"
        return 0
    else
        print_error "Failed to start ntfy service"
        return 1
    fi
}

# Function to test the service
test_service() {
    local ip="$1"
    print_info "Testing service at http://$ip:8080"
    
    if curl -s "http://$ip:8080/health" > /dev/null; then
        print_status "Service is accessible"
        return 0
    else
        print_warning "Service may not be accessible from network"
        return 1
    fi
}

# Function to send test notification
send_test_notification() {
    local ip="$1"
    print_info "Sending test notification..."
    
    local response=$(curl -s -d "Hello from automated ntfy! 🚀" "http://$ip:8080/mytopic")
    
    if echo "$response" | grep -q "id"; then
        print_status "Test notification sent successfully"
        echo "Response: $response"
    else
        print_warning "Test notification may have failed"
    fi
}

# Main execution
main() {
    # Get current IP address
    print_info "Detecting current IP address..."
    CURRENT_IP=$(get_current_ip)
    
    if [ -z "$CURRENT_IP" ]; then
        print_error "Could not detect IP address"
        exit 1
    fi
    
    print_status "Current IP address: $CURRENT_IP"
    
    # Update configuration files
    update_docker_compose "$CURRENT_IP"
    update_env_file "$CURRENT_IP"
    
    # Start the service
    if start_ntfy_service; then
        # Test the service
        if test_service "$CURRENT_IP"; then
            print_status "Service is ready and accessible"
            
            # Send test notification
            send_test_notification "$CURRENT_IP"
            
            echo ""
            echo "🎉 ntfy.sh is now running!"
            echo "📱 Update your iPhone app to use: http://$CURRENT_IP:8080"
            echo "🌐 Web interface: http://$CURRENT_IP:8080"
            echo "📋 Topic: mytopic"
            echo ""
            echo "To stop the service: docker compose down"
            echo "To restart with new IP: ./auto-start.sh"
        else
            print_warning "Service started but may not be accessible from network"
            print_info "Check your router settings or firewall configuration"
        fi
    else
        print_error "Failed to start ntfy service"
        exit 1
    fi
}

# Run main function
main "$@"
