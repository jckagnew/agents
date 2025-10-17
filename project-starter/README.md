# 🚀 Project Starter Template

A comprehensive template for starting new development projects with all essential configurations, scripts, and best practices pre-configured.

## 📁 Project Structure

```
project-starter/
├── .env                     # Environment variables (from master)
├── .gitignore              # Comprehensive gitignore
├── .env.example            # Example environment file
├── README.md               # This file
├── package.json            # Node.js dependencies
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Python project configuration
├── setup.sh               # Project setup script
├── scripts/                # Utility scripts
│   ├── dev.sh             # Development server
│   ├── test.sh            # Run tests
│   ├── deploy.sh          # Deployment script
│   └── github.sh          # GitHub operations
├── src/                    # Source code
│   ├── main.py            # Python entry point
│   ├── app.js             # Node.js entry point
│   └── components/        # Reusable components
├── tests/                  # Test files
├── docs/                   # Documentation
├── .vscode/                # VS Code settings
│   └── settings.json
└── templates/              # Code templates
    ├── python/
    ├── javascript/
    ├── markdown/
    ├── ai/                 # AI collaboration templates
    ├── agents/             # Specialized UI agents
    ├── ai-agents/          # AI agent frameworks
    │   ├── crewai/
    │   ├── langgraph/
    │   ├── autogen/
    │   └── openai-agents/
    ├── web-frameworks/     # Web development frameworks
    │   ├── nextjs/
    │   ├── fastapi/
    │   ├── flask/
    │   ├── gradio/
    │   └── streamlit/
    ├── ai-planning/        # AI planning layer templates
    │   ├── cursor-instructions.md
    │   ├── prompt-templates.md
    │   └── cursor-workflows.md
    ├── mobile/             # Mobile development templates
    │   ├── react-native/
    │   ├── expo/
    │   ├── native/
    │   ├── components/     # Mobile UI components
    │   │   └── SmoothDateInput.tsx
    │   └── services/       # Mobile services
    │       └── DateUtilityService.ts
    ├── fitness-app/        # AI-powered fitness tracking app
    │   ├── mobile/         # React Native mobile app
    │   ├── web/            # Next.js dashboard
    │   ├── backend/        # FastAPI backend
    │   ├── ai/             # AI agents for voice & analytics
    │   └── config/         # App configuration
    └── mcp/                # MCP integration templates
        ├── README.md
        ├── setup-mcp.sh
        ├── prompts/
        └── examples/
├── guides/                 # Deployment and best practices
    ├── VERCEL_DEPLOYMENT_GUIDE.md
    └── DEPLOYMENT_LEARNINGS.md
├── checklists/             # Troubleshooting and maintenance
    └── DEPLOYMENT_TROUBLESHOOTING.md
```

## 🚀 Quick Start

1. **Clone the template:**
   ```bash
   cp -r /Users/jackagnew/projects/agents/project-starter /path/to/your/new-project
   cd /path/to/your/new-project
   ```

2. **Run setup:**
   ```bash
   ./setup.sh
   ```

3. **Start developing:**
   ```bash
   ./scripts/dev.sh
   ```

## 🛠️ What's Included

- ✅ **Environment Setup** - All API keys and tokens
- ✅ **Git Configuration** - Proper .gitignore and hooks
- ✅ **Development Tools** - VS Code settings, linting, formatting
- ✅ **Scripts** - Development, testing, deployment automation
- ✅ **Templates** - Code templates for common patterns
- ✅ **Documentation** - Comprehensive guides and API docs
- ✅ **Testing** - Complete test framework with coverage
- ✅ **Deployment** - Ready for various platforms
- ✅ **CI/CD** - GitHub Actions workflows
- ✅ **Docker** - Multi-stage Dockerfile and compose
- ✅ **Monitoring** - Prometheus and Grafana configs
- ✅ **Security** - Pre-commit hooks and security scanning
- ✅ **Code Quality** - Linting, formatting, and type checking
- ✅ **AI Agents** - CrewAI, LangGraph, AutoGen, OpenAI Agents
- ✅ **Web Frameworks** - Next.js, FastAPI, Flask, Gradio, Streamlit
- ✅ **AI Planning Layer** - Tracer-like planning using Cursor AI
- ✅ **Mobile Development** - React Native, Expo, iOS/Android testing
- ✅ **US Date Input Components** - Smooth, non-jumpy date inputs with MM/DD/YYYY format
- ✅ **MCP Integration** - Model Context Protocol for AI agent automation

## 📋 Features

### Environment Management
- Master .env file with all API keys
- Environment validation
- Secure token handling

### Development Tools
- VS Code workspace configuration
- ESLint, Prettier, Black, isort
- Pre-commit hooks with security scanning
- Debugging configurations
- TypeScript support
- MyPy type checking

### Automation Scripts
- One-command project setup
- Development server management
- Testing and deployment
- GitHub operations

### Code Templates
- Python project structure
- Node.js/React components
- API endpoints
- Database models
- Documentation templates
- **US Date Input Components** - Smooth, non-jumpy date inputs with MM/DD/YYYY format
- **AI Collaboration** - Enhanced AI agents with Stanford research best practices
- **ShadCN UI Agents** - Specialized agents for shadcn/ui component development

### CI/CD & DevOps
- GitHub Actions workflows
- Automated testing and deployment
- Docker multi-stage builds
- Docker Compose for local development
- Security scanning and vulnerability checks

### Monitoring & Observability
- Prometheus metrics collection
- Grafana dashboards
- Application performance monitoring
- Infrastructure monitoring
- Log aggregation and analysis

### Security & Quality
- Pre-commit hooks with security scanning
- Automated dependency updates
- Vulnerability scanning (Bandit, Safety, Semgrep)
- Code quality gates
- Secret detection and prevention

### AI Agents Development
- **CrewAI Templates** - Multi-agent crews with specialized roles
- **LangGraph Templates** - State-based agent workflows
- **AutoGen Templates** - Conversational agent systems
- **OpenAI Agents Templates** - Function calling and tool use
- **Agent Configuration** - YAML configs for different agent types
- **Tool Integration** - Web search, file operations, data analysis
- **Multi-Provider Support** - OpenAI, Anthropic, Google AI

### Web Frameworks Development
- **Next.js Templates** - Full-stack React with TypeScript, Tailwind CSS, Radix UI
- **FastAPI Templates** - High-performance Python APIs with Pydantic, SQLAlchemy
- **Flask Templates** - Lightweight Python web framework with extensions
- **Gradio Templates** - ML/AI demo interfaces with multiple AI providers
- **Streamlit Templates** - Data science dashboards with interactive components
- **Modern UI Components** - Pre-built components for rapid development
- **API Integration** - Built-in support for OpenAI, Anthropic, Google AI

### AI Planning Layer
- **Tracer-like Planning** - Gap analysis and requirement clarification using Cursor AI
- **Architecture Planning** - Detailed system design and technology recommendations
- **Implementation Phases** - Structured project breakdown and development phases
- **Code Verification** - Automated review and issue identification
- **Project Templates** - AI agent, web app, and mobile app planning workflows
- **Cost-Effective** - Uses existing Cursor subscription without additional costs

### Mobile Development
- React Native project templates
- Expo development environment
- iOS Simulator integration
- Android Studio emulator setup
- Cross-platform testing tools
- Mobile-specific UI components
- Native device feature access
- App Store deployment ready

### AI-Powered Fitness App
- **Voice-Powered Workout Logging** - Natural language workout tracking
- **Cross-Platform Mobile App** - React Native with iOS/Android support
- **Health Data Integration** - Apple HealthKit, Google Fit, Health Connect
- **AI Analytics Dashboard** - Recharts-powered data visualization
- **Real-time Sync** - Supabase-powered data synchronization
- **Voice Processing** - OpenAI Whisper for speech recognition
- **Workout Analytics** - AI-driven insights and recommendations
- **Apple Watch Support** - Native watchOS integration

### MCP Integration
- **Model Context Protocol** - Direct AI agent integration with external services
- **Supabase MCP** - Automated database and backend setup
- **ShadCN MCP** - UI component generation and integration
- **Stripe MCP** - Payment processing automation
- **Full-Stack Automation** - Complete app development with prompts only
- **Service Integration** - Connect to external APIs and services automatically
- **Prompt Templates** - Pre-built prompts for different MCP workflows
- **Workflow Automation** - Streamlined development processes

## 🤖 AI Collaboration Features

Based on Stanford research, this template includes advanced AI collaboration techniques:

### Enhanced AI Agents
- **Chain of Thought Reasoning** - Get AI to think step-by-step
- **Reverse Prompting** - Let AI ask questions before proceeding
- **Critical Feedback** - Enable honest, constructive criticism
- **Role Assignment** - Assign specific personas for better outputs
- **Context Engineering** - Provide comprehensive context for better results

### Prompt Engineering Toolkit
- Ready-to-use prompt templates
- Conversation simulators for difficult discussions
- Feedback analyzers for content review
- Creative brainstorming tools
- Problem-solving frameworks

### Best Practices Integration
- Based on Jeremy Utley's Stanford research
- Implements "AI as teammate" paradigm
- Focuses on coaching techniques over coding
- Includes conversation roleplay tools
- Emphasizes critical thinking and iteration

## 🚀 Deployment Intelligence

The project starter now includes comprehensive deployment learnings and troubleshooting guides:

### Deployment Guides
- **Vercel Deployment Guide** - Complete best practices for Next.js deployments
- **Deployment Learnings** - Real-world experience from Weight Tracker demo
- **Troubleshooting Checklist** - Systematic approach to fixing deployment issues

### Key Learnings
- **Progressive Enhancement** - Deploy basic versions first, then add complexity
- **Build Environment Differences** - Local vs production environment considerations
- **TypeScript Best Practices** - Proper type definitions to prevent build failures
- **Bundle Optimization** - Performance targets and optimization strategies
- **Error Recovery Patterns** - Graceful degradation and fallback strategies

### Software Factory Intelligence
- **Learning Integration** - Every deployment issue becomes a learning opportunity
- **Pattern Recognition** - Identify common failure patterns and solutions
- **Automated Checks** - Pre-deployment validation and testing
- **Continuous Improvement** - Update practices based on real-world experience

## 🎨 ShadCN UI Agent Features

Specialized agents for building UI components with shadcn/ui and MCP:

### Agent Collection
- **Requirements Analysis Agent** - Breaks down complex UI features into components
- **Component Research Agent** - Researches shadcn components and examples
- **Implementation Agent** - Builds complete TypeScript/React implementations
- **Express Agent** - Quick single-component additions

### MCP Integration
- **Model Context Protocol** - Works with both Claude and Cursor
- **shadcn/ui Integration** - Direct access to component registries
- **TypeScript Ready** - Generates properly typed React components
- **Workflow Automation** - Streamlined development process

### Use Cases
- **Complex UI Features** - Multi-component features with proper hierarchy
- **Quick Component Additions** - Single components ready to use
- **Component Research** - Understanding shadcn components and examples
- **Implementation Generation** - Complete, working React components

## 🔧 Customization

Edit the templates in the `templates/` directory to match your preferred coding style and project structure.

## 📚 Documentation

See the `docs/` directory for detailed guides on:
- Setting up different types of projects
- Using the included scripts
- Customizing templates
- Best practices
- **Mobile Development** - Complete mobile development guide

---

**Happy coding! 🚀**
