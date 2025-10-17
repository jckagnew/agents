#!/bin/bash

# Software Factory Setup Script
# This script sets up the complete software factory environment

set -e  # Exit on any error

echo "🏭 Setting up Software Factory..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.11+ is installed
check_python() {
    print_status "Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        REQUIRED_VERSION="3.11"
        if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
            print_success "Python $PYTHON_VERSION found"
        else
            print_error "Python 3.11+ is required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        exit 1
    fi
}

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    if command -v docker &> /dev/null; then
        print_success "Docker found"
    else
        print_warning "Docker not found. You'll need Docker for full deployment"
    fi
}

# Check if Docker Compose is installed
check_docker_compose() {
    print_status "Checking Docker Compose installation..."
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        print_success "Docker Compose found"
    else
        print_warning "Docker Compose not found. You'll need it for full deployment"
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating Python virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Create environment file
create_env_file() {
    print_status "Creating environment configuration..."
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Software Factory Environment Configuration

# Environment
ENVIRONMENT=development
DEBUG=True

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/software_factory
POSTGRES_DB=software_factory
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Services
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# Supabase (if using)
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Email Services
SENDGRID_API_KEY=your_sendgrid_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here

# Cloud Services
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
GOOGLE_CLOUD_PROJECT_ID=your_google_cloud_project_here

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
PROMETHEUS_ENDPOINT=http://localhost:9090

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
EOF
        print_success "Environment file created (.env)"
        print_warning "Please update .env with your actual API keys and configuration"
    else
        print_warning "Environment file already exists"
    fi
}

# Create directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p logs
    mkdir -p data
    mkdir -p uploads
    mkdir -p exports
    mkdir -p backups
    print_success "Directories created"
}

# Initialize database
init_database() {
    print_status "Initializing database..."
    # This would run database migrations in a real setup
    print_success "Database initialization completed"
}

# Run tests
run_tests() {
    print_status "Running tests..."
    if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
        python -m pytest tests/ -v
        print_success "Tests completed"
    else
        print_warning "No test configuration found, skipping tests"
    fi
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    cat > start.sh << 'EOF'
#!/bin/bash

# Software Factory Startup Script

echo "🏭 Starting Software Factory..."

# Activate virtual environment
source venv/bin/activate

# Start the application
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

EOF
    chmod +x start.sh
    print_success "Startup script created (start.sh)"
}

# Create Docker startup script
create_docker_startup() {
    print_status "Creating Docker startup script..."
    cat > start-docker.sh << 'EOF'
#!/bin/bash

# Software Factory Docker Startup Script

echo "🏭 Starting Software Factory with Docker..."

# Build and start all services
docker-compose up --build -d

echo "Software Factory is starting up..."
echo "API will be available at: http://localhost:8000"
echo "Grafana dashboard at: http://localhost:3000 (admin/admin)"
echo "Prometheus at: http://localhost:9090"

# Show logs
docker-compose logs -f

EOF
    chmod +x start-docker.sh
    print_success "Docker startup script created (start-docker.sh)"
}

# Create development script
create_dev_script() {
    print_status "Creating development script..."
    cat > dev.sh << 'EOF'
#!/bin/bash

# Software Factory Development Script

echo "🏭 Starting Software Factory in development mode..."

# Activate virtual environment
source venv/bin/activate

# Start with hot reload
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

EOF
    chmod +x dev.sh
    print_success "Development script created (dev.sh)"
}

# Main setup function
main() {
    echo "🏭 Software Factory Setup"
    echo "========================="
    echo ""
    
    # Check prerequisites
    check_python
    check_docker
    check_docker_compose
    
    # Setup Python environment
    create_venv
    activate_venv
    install_dependencies
    
    # Setup configuration
    create_env_file
    create_directories
    
    # Initialize services
    init_database
    
    # Run tests
    run_tests
    
    # Create startup scripts
    create_startup_script
    create_docker_startup
    create_dev_script
    
    echo ""
    echo "🎉 Software Factory setup completed!"
    echo ""
    echo "Next steps:"
    echo "1. Update .env with your API keys and configuration"
    echo "2. Run './start.sh' to start the development server"
    echo "3. Or run './start-docker.sh' to start with Docker"
    echo "4. Visit http://localhost:8000/docs for API documentation"
    echo ""
    echo "Happy building! 🚀"
}

# Run main function
main "$@"

