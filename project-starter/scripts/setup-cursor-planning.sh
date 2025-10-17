#!/bin/bash

# Cursor AI Planning Layer Setup Script
# Sets up Tracer-like planning capabilities using Cursor's built-in features

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

log_info "Setting up Cursor AI Planning Layer..."

# 1. Create planning templates directory
log_info "Creating planning templates directory..."
mkdir -p templates/ai-planning
log_success "Planning templates directory created"

# 2. Create Cursor configuration directory
log_info "Creating Cursor configuration directory..."
mkdir -p .cursor
log_success "Cursor configuration directory created"

# 3. Create Cursor settings file
log_info "Creating Cursor settings file..."
cat > .cursor/settings.json << 'EOF'
{
  "cursor.ai.instructions": "You are an AI planning specialist that helps developers create comprehensive, gap-free project plans before implementation begins. Your role is to analyze requirements for missing technical details, ask specific clarifying questions, create detailed implementation plans, and provide verification and review capabilities. Always start with gap analysis before implementation, provide clear reasoning for recommendations, and use visual indicators (✅, ⚠️, ❌) for status.",
  "cursor.ai.model": "gpt-4",
  "cursor.ai.temperature": 0.3,
  "cursor.ai.maxTokens": 4000,
  "cursor.ai.enableCodeGeneration": true,
  "cursor.ai.enableCodeReview": true,
  "cursor.ai.enablePlanning": true
}
EOF
log_success "Cursor settings file created"

# 4. Create planning workflow scripts
log_info "Creating planning workflow scripts..."

# Gap Analysis Script
cat > scripts/gap-analysis.sh << 'EOF'
#!/bin/bash

# Gap Analysis Script for Cursor AI Planning
# Helps identify missing requirements and technical details

echo "🔍 Cursor AI Gap Analysis Workflow"
echo "=================================="
echo ""
echo "This script will help you use Cursor's AI to analyze your project requirements"
echo "and identify missing technical details before implementation begins."
echo ""
echo "Steps:"
echo "1. Open Cursor and start a new chat"
echo "2. Copy the gap analysis prompt from templates/ai-planning/prompt-templates.md"
echo "3. Replace [PROJECT_DESCRIPTION] with your requirements"
echo "4. Paste into Cursor chat and follow the structured response"
echo ""
echo "Gap Analysis Prompt:"
echo "===================="
echo ""
cat templates/ai-planning/prompt-templates.md | sed -n '/### 1. Technical Stack Clarification/,/```/p' | head -n -1 | tail -n +4
echo ""
echo "Next Steps:"
echo "- Answer the clarifying questions"
echo "- Use the architecture planning prompt"
echo "- Create implementation phases"
echo "- Start implementation with clear requirements"
EOF

chmod +x scripts/gap-analysis.sh

# Architecture Planning Script
cat > scripts/architecture-planning.sh << 'EOF'
#!/bin/bash

# Architecture Planning Script for Cursor AI Planning
# Helps create detailed system architecture plans

echo "🏗️ Cursor AI Architecture Planning Workflow"
echo "==========================================="
echo ""
echo "This script will help you use Cursor's AI to create detailed system architecture"
echo "plans based on your clarified requirements."
echo ""
echo "Steps:"
echo "1. Open Cursor and start a new chat"
echo "2. Copy the architecture planning prompt from templates/ai-planning/prompt-templates.md"
echo "3. Replace [REQUIREMENTS] with your clarified requirements"
echo "4. Paste into Cursor chat and follow the structured response"
echo ""
echo "Architecture Planning Prompt:"
echo "============================"
echo ""
cat templates/ai-planning/prompt-templates.md | sed -n '/### 2. Architecture Planning/,/```/p' | head -n -1 | tail -n +4
echo ""
echo "Next Steps:"
echo "- Review the architecture plan"
echo "- Use the implementation phases prompt"
echo "- Start implementing phase by phase"
echo "- Use verification prompts for each phase"
EOF

chmod +x scripts/architecture-planning.sh

# Implementation Planning Script
cat > scripts/implementation-planning.sh << 'EOF'
#!/bin/bash

# Implementation Planning Script for Cursor AI Planning
# Helps create detailed implementation phases

echo "🚀 Cursor AI Implementation Planning Workflow"
echo "============================================="
echo ""
echo "This script will help you use Cursor's AI to create detailed implementation"
echo "phases based on your architecture plan."
echo ""
echo "Steps:"
echo "1. Open Cursor and start a new chat"
echo "2. Copy the implementation phases prompt from templates/ai-planning/prompt-templates.md"
echo "3. Replace [PROJECT_DETAILS] with your project details"
echo "4. Paste into Cursor chat and follow the structured response"
echo ""
echo "Implementation Planning Prompt:"
echo "=============================="
echo ""
cat templates/ai-planning/prompt-templates.md | sed -n '/### 3. Implementation Phases/,/```/p' | head -n -1 | tail -n +4
echo ""
echo "Next Steps:"
echo "- Review the implementation plan"
echo "- Start implementing Phase 1"
echo "- Use verification prompts after each phase"
echo "- Iterate and refine as needed"
EOF

chmod +x scripts/implementation-planning.sh

# Verification Script
cat > scripts/verification.sh << 'EOF'
#!/bin/bash

# Verification Script for Cursor AI Planning
# Helps review and verify implemented code

echo "🔍 Cursor AI Verification Workflow"
echo "=================================="
echo ""
echo "This script will help you use Cursor's AI to review and verify your"
echo "implemented code against the original requirements."
echo ""
echo "Steps:"
echo "1. Open Cursor and start a new chat"
echo "2. Copy the verification prompt from templates/ai-planning/prompt-templates.md"
echo "3. Replace [CODE_TO_REVIEW] with your implemented code"
echo "4. Paste into Cursor chat and follow the structured response"
echo ""
echo "Verification Prompt:"
echo "==================="
echo ""
cat templates/ai-planning/prompt-templates.md | sed -n '/### 1. Code Review Template/,/```/p' | head -n -1 | tail -n +4
echo ""
echo "Next Steps:"
echo "- Review identified issues"
echo "- Fix critical and major issues first"
echo "- Address minor issues for code quality"
echo "- Re-verify after fixes"
EOF

chmod +x scripts/verification.sh

# 5. Create quick start guide
log_info "Creating quick start guide..."
cat > CURSOR_PLANNING_GUIDE.md << 'EOF'
# 🎯 Cursor AI Planning Layer - Quick Start Guide

## Overview

This planning layer replicates Tracer's functionality using Cursor's built-in AI capabilities, providing gap-filling, project breakdown, and verification without additional costs.

## Quick Start

### 1. Setup
```bash
./scripts/setup-cursor-planning.sh
```

### 2. Basic Workflow
1. **Gap Analysis**: `./scripts/gap-analysis.sh`
2. **Architecture Planning**: `./scripts/architecture-planning.sh`
3. **Implementation Planning**: `./scripts/implementation-planning.sh`
4. **Verification**: `./scripts/verification.sh`

### 3. Using in Cursor
1. Open Cursor and start a new chat
2. Copy the relevant prompt from `templates/ai-planning/prompt-templates.md`
3. Replace placeholders with your project details
4. Paste into Cursor chat and follow the structured response

## Available Templates

- **Gap Analysis**: Identify missing requirements and technical details
- **Architecture Planning**: Create detailed system architecture plans
- **Implementation Phases**: Break down projects into manageable phases
- **Code Review**: Verify implemented code against requirements
- **Project-Specific**: AI agents, web apps, mobile apps

## Best Practices

1. **Always start with gap analysis** - Don't jump into implementation
2. **Use structured responses** - Follow the template formats
3. **Iterate and refine** - Review plans before implementation
4. **Test and verify** - Review code at each phase
5. **Maintain context** - Reference previous decisions

## Integration with Project Starter

This planning layer works seamlessly with:
- AI agent frameworks (CrewAI, LangGraph, AutoGen)
- Web frameworks (Next.js, FastAPI, Flask)
- Mobile development (React Native, Expo)
- Database integration (Supabase, PostgreSQL)
- Authentication systems (NextAuth, JWT)

## Troubleshooting

- **Vague Requirements**: Use gap analysis prompts to clarify
- **Missing Dependencies**: Use architecture planning to identify
- **Implementation Gaps**: Use verification prompts to catch
- **Performance Issues**: Use performance planning to address
- **Security Concerns**: Use security planning to mitigate

## Getting Help

- Check `templates/ai-planning/` for detailed templates
- Use `scripts/` for automated workflows
- Reference `cursor-workflows.md` for complete workflows
- Follow the structured response formats for best results
EOF

log_success "Quick start guide created"

# 6. Create VS Code workspace settings
log_info "Creating VS Code workspace settings..."
cat > .vscode/settings.json << 'EOF'
{
  "cursor.ai.instructions": "You are an AI planning specialist that helps developers create comprehensive, gap-free project plans before implementation begins. Your role is to analyze requirements for missing technical details, ask specific clarifying questions, create detailed implementation plans, and provide verification and review capabilities. Always start with gap analysis before implementation, provide clear reasoning for recommendations, and use visual indicators (✅, ⚠️, ❌) for status.",
  "cursor.ai.model": "gpt-4",
  "cursor.ai.temperature": 0.3,
  "cursor.ai.maxTokens": 4000,
  "cursor.ai.enableCodeGeneration": true,
  "cursor.ai.enableCodeReview": true,
  "cursor.ai.enablePlanning": true,
  "files.associations": {
    "*.md": "markdown"
  },
  "markdown.preview.breaks": true,
  "markdown.preview.linkify": true
}
EOF
log_success "VS Code workspace settings created"

# 7. Create example project
log_info "Creating example project..."
mkdir -p examples/cursor-planning-example
cat > examples/cursor-planning-example/README.md << 'EOF'
# Cursor Planning Example

This example demonstrates how to use the Cursor AI Planning Layer for a real project.

## Project: AI-Powered Task Manager

### Step 1: Gap Analysis
Use the gap analysis prompt to identify missing requirements:

```
I want to build an AI-powered task manager that can:
- Create and manage tasks
- Use AI to suggest task priorities
- Integrate with calendar systems
- Send notifications and reminders
- Provide productivity insights

Please use the gap analysis template to help me clarify all technical details.
```

### Step 2: Architecture Planning
Based on clarified requirements, create system architecture:

```
Based on our clarified requirements, please create a detailed system architecture plan using the architecture planning template.
```

### Step 3: Implementation Phases
Break down into detailed phases:

```
Now that we have the architecture, please break this down into detailed implementation phases using the implementation phases template.
```

### Step 4: Phase Implementation
Implement each phase with verification:

```
Let's implement Phase 1. Please provide specific implementation steps, code examples, and testing approach.
```

### Step 5: Verification
Review implemented code:

```
Please review the implemented code using the code review template to identify any issues.
```

## Expected Outcomes

- Complete project requirements clarification
- Detailed system architecture plan
- Phased implementation roadmap
- Working code with proper verification
- Documentation of decisions and trade-offs

## Learning Objectives

- How to use Cursor for project planning
- Gap analysis and requirement clarification
- Architecture planning and design
- Implementation phase breakdown
- Code verification and review
EOF
log_success "Example project created"

log_success "Cursor AI Planning Layer setup completed!"
log_info "Next steps:"
log_info "1. Open Cursor and start using the planning workflows"
log_info "2. Try the example project in examples/cursor-planning-example/"
log_info "3. Use the scripts in scripts/ for automated workflows"
log_info "4. Reference templates/ai-planning/ for detailed prompts"
log_info "5. Follow the best practices in CURSOR_PLANNING_GUIDE.md"

log_info "Available workflows:"
log_info "- Gap Analysis: ./scripts/gap-analysis.sh"
log_info "- Architecture Planning: ./scripts/architecture-planning.sh"
log_info "- Implementation Planning: ./scripts/implementation-planning.sh"
log_info "- Verification: ./scripts/verification.sh"
