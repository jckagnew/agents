#!/bin/bash

# AI Agents Development Environment Setup Script
# Sets up AI agent frameworks: CrewAI, LangGraph, AutoGen, OpenAI Agents

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

log_info "Setting up AI Agents development environment..."

# 1. Install Python dependencies
log_info "Installing AI agent frameworks..."

# CrewAI
log_info "Installing CrewAI..."
pip install crewai[tools]>=0.108.0 gradio>=5.23.3

# LangGraph
log_info "Installing LangGraph..."
pip install langgraph>=0.2.0 langchain>=0.3.0 langchain-openai>=0.2.0 langchain-anthropic>=0.2.0 langchain-google-genai>=2.0.0

# AutoGen
log_info "Installing AutoGen..."
pip install autogen-core>=0.2.0 autogen-agentchat>=0.2.0 autogen-ext[openai]>=0.2.0 autogen-ext[anthropic]>=0.2.0

# OpenAI Agents
log_info "Installing OpenAI Agents dependencies..."
pip install openai>=1.0.0 anthropic>=0.7.0 google-generativeai>=0.3.0

# Additional dependencies
log_info "Installing additional dependencies..."
pip install playwright>=1.40.0 beautifulsoup4>=4.12.0 pandas>=2.0.0 numpy>=1.24.0 requests>=2.31.0

# 2. Install Playwright browsers
log_info "Installing Playwright browsers..."
playwright install

# 3. Create AI agents project templates
log_info "Creating AI agents project templates..."

# Create CrewAI template
if [ ! -d "templates/ai-agents/crewai" ]; then
    mkdir -p templates/ai-agents/crewai
    log_success "CrewAI template directory created"
fi

# Create LangGraph template
if [ ! -d "templates/ai-agents/langgraph" ]; then
    mkdir -p templates/ai-agents/langgraph
    log_success "LangGraph template directory created"
fi

# Create AutoGen template
if [ ! -d "templates/ai-agents/autogen" ]; then
    mkdir -p templates/ai-agents/autogen
    log_success "AutoGen template directory created"
fi

# Create OpenAI Agents template
if [ ! -d "templates/ai-agents/openai-agents" ]; then
    mkdir -p templates/ai-agents/openai-agents
    log_success "OpenAI Agents template directory created"
fi

# 4. Create AI agents project creation script
log_info "Creating AI agents project creation script..."

cat > scripts/create-ai-agent-project.sh << 'EOF'
#!/bin/bash

# AI Agent Project Creation Script
# Creates a new AI agent project using the templates

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
    echo "  -f, --framework FRAMEWORK  AI framework (crewai|langgraph|autogen|openai-agents)"
    echo "  -a, --author NAME          Author name"
    echo "  -e, --email EMAIL          Author email"
    echo "  -h, --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 MyAgent --framework crewai"
    echo "  $0 MyAgent --framework langgraph --author 'John Doe' --email 'john@example.com'"
}

# Default values
FRAMEWORK="crewai"
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
    crewai|langgraph|autogen|openai-agents)
        ;;
    *)
        log_error "Invalid framework: $FRAMEWORK"
        log_error "Valid frameworks: crewai, langgraph, autogen, openai-agents"
        exit 1
        ;;
esac

# Create project slug
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

log_info "Creating AI agent project: $PROJECT_NAME"
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
cp -r "../templates/ai-agents/$FRAMEWORK"/* .

# Replace placeholders in files
log_info "Replacing placeholders..."

# Find and replace placeholders
find . -type f -name "*.py" -o -name "*.yaml" -o -name "*.toml" -o -name "*.md" | while read file; do
    if [ -f "$file" ]; then
        sed -i '' "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$file"
        sed -i '' "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g" "$file"
        sed -i '' "s/{{AUTHOR_NAME}}/$AUTHOR_NAME/g" "$file"
        sed -i '' "s/{{AUTHOR_EMAIL}}/$AUTHOR_EMAIL/g" "$file"
        sed -i '' "s/{{PROJECT_DESCRIPTION}}/AI agent project using $FRAMEWORK/g" "$file"
    fi
done

# Create additional configuration files
log_info "Creating additional configuration files..."

# Create .env file
cat > .env << EOF
# AI Agent Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Project Configuration
PROJECT_NAME=$PROJECT_NAME
PROJECT_VERSION=0.1.0
AUTHOR_NAME=$AUTHOR_NAME
AUTHOR_EMAIL=$AUTHOR_EMAIL
EOF

# Create README
cat > README.md << EOF
# 🤖 $PROJECT_NAME

AI agent project using $FRAMEWORK framework.

## 🚀 Quick Start

1. **Install dependencies:**
   \`\`\`bash
   pip install -e .
   \`\`\`

2. **Configure environment:**
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your API keys
   \`\`\`

3. **Run the agent:**
   \`\`\`bash
   $PROJECT_SLUG run --inputs '{"message": "Hello, how can you help me?"}'
   \`\`\`

## 📋 Available Commands

- \`$PROJECT_SLUG run\` - Run the agent
- \`$PROJECT_SLUG train\` - Train the agent
- \`$PROJECT_SLUG replay\` - Replay a session
- \`$PROJECT_SLUG test\` - Test the agent

## 🛠️ Development

- Edit agent configuration in \`src/$PROJECT_SLUG/config/\`
- Modify agent behavior in \`src/$PROJECT_SLUG/\`
- Add custom tools as needed

## 📚 Documentation

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

**Happy agent building! 🤖**
EOF

# Create .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

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

# AI Agent specific
sessions/
logs/
outputs/
*.log
EOF

# Install the package
log_info "Installing package..."
pip install -e .

log_success "AI agent project '$PROJECT_NAME' created successfully!"
log_info "Project directory: $(pwd)"
log_info "Next steps:"
log_info "1. cd $PROJECT_DIR"
log_info "2. Edit .env with your API keys"
log_info "3. Run: $PROJECT_SLUG run --inputs '{\"message\": \"Hello!\"}'"
log_info "4. Start building your AI agent!"

EOF

chmod +x scripts/create-ai-agent-project.sh

log_success "AI Agents development environment setup completed!"
log_info "Next steps:"
log_info "1. Create a new AI agent project: ./scripts/create-ai-agent-project.sh MyAgent --framework crewai"
log_info "2. Configure your API keys in the .env file"
log_info "3. Start building AI agents!"

log_info "Available AI agent frameworks:"
log_info "- CrewAI: Multi-agent crews with specialized roles"
log_info "- LangGraph: State-based agent workflows"
log_info "- AutoGen: Conversational agent systems"
log_info "- OpenAI Agents: Function calling and tool use"
