#!/bin/bash

# Web Frameworks Development Environment Setup Script
# Sets up Next.js, FastAPI, Flask, Gradio, and Streamlit

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${YELLOW}✨ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_info "Setting up Web Frameworks development environment..."

# 1. Install Node.js dependencies
log_info "Installing Node.js and npm..."
if ! command -v node &> /dev/null; then
    brew install node
    log_success "Node.js installed"
else
    log_info "Node.js already installed: $(node --version)"
fi

# 2. Install Python dependencies
log_info "Installing Python web frameworks..."

# FastAPI
log_info "Installing FastAPI..."
pip install fastapi>=0.104.0 uvicorn[standard]>=0.24.0 pydantic>=2.0.0

# Flask
log_info "Installing Flask..."
pip install Flask>=3.0.0 Flask-SQLAlchemy>=3.0.0 Flask-Migrate>=4.0.0 Flask-CORS>=4.0.0

# Gradio
log_info "Installing Gradio..."
pip install gradio>=5.23.3

# Streamlit
log_info "Installing Streamlit..."
pip install streamlit>=1.28.0 streamlit-option-menu>=0.3.0

# Additional dependencies
log_info "Installing additional dependencies..."
pip install python-dotenv>=1.0.0 requests>=2.31.0 pandas>=2.0.0 numpy>=1.24.0

# 3. Create web frameworks project templates
log_info "Creating web frameworks project templates..."

# Create Next.js template
if [ ! -d "templates/web-frameworks/nextjs" ]; then
    mkdir -p templates/web-frameworks/nextjs
    log_success "Next.js template directory created"
fi

# Create FastAPI template
if [ ! -d "templates/web-frameworks/fastapi" ]; then
    mkdir -p templates/web-frameworks/fastapi
    log_success "FastAPI template directory created"
fi

# Create Flask template
if [ ! -d "templates/web-frameworks/flask" ]; then
    mkdir -p templates/web-frameworks/flask
    log_success "Flask template directory created"
fi

# Create Gradio template
if [ ! -d "templates/web-frameworks/gradio" ]; then
    mkdir -p templates/web-frameworks/gradio
    log_success "Gradio template directory created"
fi

# Create Streamlit template
if [ ! -d "templates/web-frameworks/streamlit" ]; then
    mkdir -p templates/web-frameworks/streamlit
    log_success "Streamlit template directory created"
fi

# 4. Create web frameworks project creation script
log_info "Creating web frameworks project creation script..."

cat > scripts/create-web-project.sh << 'EOF'
#!/bin/bash

# Web Project Creation Script
# Creates a new web project using the templates

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${YELLOW}✨ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] PROJECT_NAME"
    echo ""
    echo "Options:"
    echo "  -f, --framework FRAMEWORK  Web framework (nextjs|fastapi|flask|gradio|streamlit)"
    echo "  -a, --author NAME          Author name"
    echo "  -e, --email EMAIL          Author email"
    echo "  -h, --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 MyWebApp --framework nextjs"
    echo "  $0 MyAPI --framework fastapi --author 'John Doe' --email 'john@example.com'"
}

# Default values
FRAMEWORK="nextjs"
AUTHOR_NAME="Your Name"
AUTHOR_EMAIL="you@example.com"
PROJECT_NAME=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--framework)
            FRAMEWORK="$2"
            shift 2
            ;;
        -a|--author)
            AUTHOR_NAME="$2"
            shift 2
            ;;
        -e|--email)
            AUTHOR_EMAIL="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            if [ -z "$PROJECT_NAME" ]; then
                PROJECT_NAME="$1"
            else
                log_error "Unknown option: $1"
                show_usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if project name is provided
if [ -z "$PROJECT_NAME" ]; then
    log_error "Project name is required"
    show_usage
    exit 1
fi

# Validate framework
case $FRAMEWORK in
    nextjs|fastapi|flask|gradio|streamlit)
        ;;
    *)
        log_error "Invalid framework: $FRAMEWORK"
        log_error "Valid frameworks: nextjs, fastapi, flask, gradio, streamlit"
        exit 1
        ;;
esac

# Create project slug
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

log_info "Creating web project: $PROJECT_NAME"
log_info "Framework: $FRAMEWORK"
log_info "Author: $AUTHOR_NAME <$AUTHOR_EMAIL>"

# Create project directory
PROJECT_DIR="$PROJECT_SLUG"
if [ -d "$PROJECT_DIR" ]; then
    log_error "Directory $PROJECT_DIR already exists"
    exit 1
fi

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Copy template files
log_info "Copying template files..."
cp -r "../templates/web-frameworks/$FRAMEWORK"/* .

# Setup environment variables
log_info "Setting up environment variables..."
if [ -f "/Users/jackagnew/projects/agents/env.master" ]; then
    cp "/Users/jackagnew/projects/agents/env.master" .env
    log_success "Environment variables copied from master"
    
    # For Next.js projects, also create .env.local
    if [ "$FRAMEWORK" = "nextjs" ]; then
        cp "/Users/jackagnew/projects/agents/env.master" .env.local
        log_success "Created .env.local for Next.js project"
    fi
else
    log_warning "Master .env file not found, creating basic .env"
    cat > .env << 'EOF'
# Environment Variables
NODE_ENV=development
PORT=3000
EOF
fi

# Replace placeholders in files
log_info "Replacing placeholders..."

# Find and replace placeholders
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.json" -o -name "*.md" -o -name "*.txt" \) | while read file; do
    if [ -f "$file" ]; then
        sed -i '' "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$file"
        sed -i '' "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g" "$file"
        sed -i '' "s/{{AUTHOR_NAME}}/$AUTHOR_NAME/g" "$file"
        sed -i '' "s/{{AUTHOR_EMAIL}}/$AUTHOR_EMAIL/g" "$file"
        sed -i '' "s/{{PROJECT_DESCRIPTION}}/Web application using $FRAMEWORK/g" "$file"
        sed -i '' "s/{{AUTHOR_URL}}/https:\/\/github.com\/$AUTHOR_NAME/g" "$file"
        sed -i '' "s/{{BASE_URL}}/http:\/\/localhost:3000/g" "$file"
        sed -i '' "s/{{DOMAIN}}/localhost/g" "$file"
        sed -i '' "s/{{KEYWORDS}}/web,app,$FRAMEWORK/g" "$file"
        sed -i '' "s/{{NEXTJS_VERSION}}/15.4.1/g" "$file"
    fi
done

# Create additional configuration files
log_info "Creating additional configuration files..."

# Create .env file
cat > .env << EOF
# Web Application Configuration
NODE_ENV=development
PORT=3000
HOST=0.0.0.0

# Database
DATABASE_URL=sqlite:///./app.db
REDIS_URL=redis://localhost:6379

# AI APIs
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Authentication
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Project Configuration
PROJECT_NAME=$PROJECT_NAME
PROJECT_VERSION=1.0.0
AUTHOR_NAME=$AUTHOR_NAME
AUTHOR_EMAIL=$AUTHOR_EMAIL
EOF

# Create .env.example
cp .env .env.example
sed -i '' 's/your_.*_here/your_value_here/g' .env.example

# Create README
cat > README.md << EOF
# 🚀 $PROJECT_NAME

Web application built with $FRAMEWORK.

## 🚀 Quick Start

### Prerequisites
- Node.js (for Next.js projects)
- Python 3.11+ (for Python projects)
- Git

### Installation

EOF

case $FRAMEWORK in
    nextjs)
        cat >> README.md << EOF
\`\`\`bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
\`\`\`
EOF
        ;;
    fastapi)
        cat >> README.md << EOF
\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn src.$PROJECT_SLUG.main:app --reload

# Run tests
pytest

# Build for production
pip install -e .
\`\`\`
EOF
        ;;
    flask)
        cat >> README.md << EOF
\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Start development server
python src/$PROJECT_SLUG/app.py

# Run tests
pytest

# Start production server
gunicorn src.$PROJECT_SLUG.app:app
\`\`\`
EOF
        ;;
    gradio)
        cat >> README.md << EOF
\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Start development server
python src/$PROJECT_SLUG/app.py

# Run tests
pytest
\`\`\`
EOF
        ;;
    streamlit)
        cat >> README.md << EOF
\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Start development server
streamlit run src/$PROJECT_SLUG/app.py

# Run tests
pytest
\`\`\`
EOF
        ;;
esac

cat >> README.md << EOF

## 📋 Available Commands

EOF

case $FRAMEWORK in
    nextjs)
        cat >> README.md << EOF
- \`npm run dev\` - Start development server
- \`npm run build\` - Build for production
- \`npm start\` - Start production server
- \`npm run lint\` - Run ESLint
- \`npm test\` - Run tests
- \`npm run test:e2e\` - Run E2E tests
EOF
        ;;
    fastapi)
        cat >> README.md << EOF
- \`uvicorn src.$PROJECT_SLUG.main:app --reload\` - Start development server
- \`pytest\` - Run tests
- \`black .\` - Format code
- \`isort .\` - Sort imports
- \`mypy .\` - Type checking
EOF
        ;;
    flask)
        cat >> README.md << EOF
- \`python src/$PROJECT_SLUG/app.py\` - Start development server
- \`pytest\` - Run tests
- \`flask db migrate\` - Create database migration
- \`flask db upgrade\` - Apply database migrations
EOF
        ;;
    gradio)
        cat >> README.md << EOF
- \`python src/$PROJECT_SLUG/app.py\` - Start Gradio app
- \`pytest\` - Run tests
EOF
        ;;
    streamlit)
        cat >> README.md << EOF
- \`streamlit run src/$PROJECT_SLUG/app.py\` - Start Streamlit app
- \`pytest\` - Run tests
EOF
        ;;
esac

cat >> README.md << EOF

## 🛠️ Development

- Edit source code in \`src/$PROJECT_SLUG/\`
- Configure environment variables in \`.env\`
- Add dependencies as needed

## 📚 Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Happy coding! 🚀**
EOF

# Create .gitignore
cat > .gitignore << EOF
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
ENV/
env.bak/
venv.bak/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Framework specific
.next/
out/
build/
dist/
*.egg-info/
.coverage
.pytest_cache/
.mypy_cache/

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Runtime
*.pid
*.seed
*.pid.lock
EOF

# Install dependencies and setup
log_info "Setting up project..."

case $FRAMEWORK in
    nextjs)
        log_info "Installing Node.js dependencies..."
        npm install
        ;;
    fastapi|flask|gradio|streamlit)
        log_info "Installing Python dependencies..."
        pip install -r requirements.txt
        ;;
esac

log_success "Web project '$PROJECT_NAME' created successfully!"
log_info "Project directory: $(pwd)"
log_info "Next steps:"
log_info "1. cd $PROJECT_DIR"
log_info "2. Edit .env with your configuration"
log_info "3. Start developing!"

case $FRAMEWORK in
    nextjs)
        log_info "4. Run: npm run dev"
        ;;
    fastapi)
        log_info "4. Run: uvicorn src.$PROJECT_SLUG.main:app --reload"
        ;;
    flask)
        log_info "4. Run: python src/$PROJECT_SLUG/app.py"
        ;;
    gradio)
        log_info "4. Run: python src/$PROJECT_SLUG/app.py"
        ;;
    streamlit)
        log_info "4. Run: streamlit run src/$PROJECT_SLUG/app.py"
        ;;
esac

EOF

chmod +x scripts/create-web-project.sh

log_success "Web Frameworks development environment setup completed!"
log_info "Next steps:"
log_info "1. Create a new web project: ./scripts/create-web-project.sh MyWebApp --framework nextjs"
log_info "2. Configure your environment variables in the .env file"
log_info "3. Start building web applications!"

log_info "Available web frameworks:"
log_info "- Next.js: Full-stack React with TypeScript"
log_info "- FastAPI: High-performance Python API"
log_info "- Flask: Lightweight Python web framework"
log_info "- Gradio: ML/AI demo interfaces"
log_info "- Streamlit: Data science dashboards"
