#!/bin/bash

# Partner Showcase UI - Next Steps Script
# This script provides guidance for the next steps in the showcase-ui session

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Session directory
SESSION_DIR=".claude/idea-to-design/showcase-ui"

echo -e "${BLUE}🚀 Partner Showcase UI - Next Steps${NC}"
echo "=================================="
echo ""

# Check if session directory exists
if [ ! -d "$SESSION_DIR" ]; then
    echo -e "${RED}❌ Session directory not found: $SESSION_DIR${NC}"
    echo "Please run the session setup first."
    exit 1
fi

echo -e "${GREEN}✅ Session directory found: $SESSION_DIR${NC}"
echo ""

# Check current session status
echo -e "${CYAN}📊 Current Session Status${NC}"
echo "=========================="

# Check requirements
if [ -f "$SESSION_DIR/requirements/iteration-0.json" ]; then
    echo -e "${GREEN}✅ Requirements: Ready${NC}"
else
    echo -e "${RED}❌ Requirements: Missing${NC}"
fi

# Check PRD
if [ -d "$SESSION_DIR/prd" ] && [ "$(ls -A $SESSION_DIR/prd 2>/dev/null)" ]; then
    echo -e "${GREEN}✅ PRD Generation: Complete${NC}"
else
    echo -e "${YELLOW}⏳ PRD Generation: Pending${NC}"
fi

# Check AI Studio Research
if [ -d "$SESSION_DIR/ai-studio-research" ] && [ "$(ls -A $SESSION_DIR/ai-studio-research 2>/dev/null)" ]; then
    echo -e "${GREEN}✅ AI Studio Research: Complete${NC}"
else
    echo -e "${YELLOW}⏳ AI Studio Research: Pending${NC}"
fi

# Check Architecture
if [ -d "$SESSION_DIR/architecture" ] && [ "$(ls -A $SESSION_DIR/architecture 2>/dev/null)" ]; then
    echo -e "${GREEN}✅ Architecture Generation: Complete${NC}"
else
    echo -e "${YELLOW}⏳ Architecture Generation: Pending${NC}"
fi

# Check UX
if [ -d "$SESSION_DIR/ux" ] && [ "$(ls -A $SESSION_DIR/ux 2>/dev/null)" ]; then
    echo -e "${GREEN}✅ UX Generation: Complete${NC}"
else
    echo -e "${YELLOW}⏳ UX Generation: Pending${NC}"
fi

# Check Design
if [ -d "$SESSION_DIR/design" ] && [ "$(ls -A $SESSION_DIR/design 2>/dev/null)" ]; then
    echo -e "${GREEN}✅ Design Generation: Complete${NC}"
else
    echo -e "${YELLOW}⏳ Design Generation: Pending${NC}"
fi

# Check Code
if [ -d "$SESSION_DIR/code" ] && [ "$(ls -A $SESSION_DIR/code 2>/dev/null)" ]; then
    echo -e "${GREEN}✅ Code Generation: Complete${NC}"
else
    echo -e "${YELLOW}⏳ Code Generation: Pending${NC}"
fi

echo ""

# Determine next steps
echo -e "${PURPLE}🎯 Recommended Next Steps${NC}"
echo "========================="

# Check what's missing and suggest next steps
if [ ! -d "$SESSION_DIR/prd" ] || [ ! "$(ls -A $SESSION_DIR/prd 2>/dev/null)" ]; then
    echo -e "${YELLOW}1. Run PRD Generation${NC}"
    echo "   Command: node scripts/generate-prd.js --requirements $SESSION_DIR/requirements/iteration-0.json --output-dir $SESSION_DIR/prd"
    echo ""
fi

if [ ! -d "$SESSION_DIR/ai-studio-research" ] || [ ! "$(ls -A $SESSION_DIR/ai-studio-research 2>/dev/null)" ]; then
    echo -e "${YELLOW}2. Run AI Studio Research${NC}"
    echo "   Commands:"
    echo "   - Market Analysis: node workspaces/c-level-business-discovery/tools/ai-studio-integration.js --analyze-market 'Partner Showcase UI' 'B2B Software' 'C-Level'"
    echo "   - Competitive Analysis: node workspaces/c-level-business-discovery/tools/ai-studio-integration.js --evaluate-opportunity 'Partner-facing marketing experiences for B2B software companies'"
    echo "   - Strategic Planning: node workspaces/c-level-business-discovery/tools/ai-studio-integration.js --strategic-plan"
    echo ""
fi

if [ ! -d "$SESSION_DIR/architecture" ] || [ ! "$(ls -A $SESSION_DIR/architecture 2>/dev/null)" ]; then
    echo -e "${YELLOW}3. Run Architecture Generation${NC}"
    echo "   Command: node scripts/generate-architecture.js --prd-dir $SESSION_DIR/prd --output-dir $SESSION_DIR/architecture"
    echo ""
fi

if [ ! -d "$SESSION_DIR/ux" ] || [ ! "$(ls -A $SESSION_DIR/ux 2>/dev/null)" ]; then
    echo -e "${YELLOW}4. Run UX Generation${NC}"
    echo "   Command: node scripts/generate-ux.js --prd-dir $SESSION_DIR/prd --architecture-dir $SESSION_DIR/architecture --output-dir $SESSION_DIR/ux"
    echo ""
fi

if [ ! -d "$SESSION_DIR/design" ] || [ ! "$(ls -A $SESSION_DIR/design 2>/dev/null)" ]; then
    echo -e "${YELLOW}5. Run Design Generation${NC}"
    echo "   Command: node scripts/generate-design.js --ux-dir $SESSION_DIR/ux --output-dir $SESSION_DIR/design"
    echo ""
fi

if [ ! -d "$SESSION_DIR/code" ] || [ ! "$(ls -A $SESSION_DIR/code 2>/dev/null)" ]; then
    echo -e "${YELLOW}6. Run Code Generation${NC}"
    echo "   Command: node scripts/generate-code.js --session-dir $SESSION_DIR --output-dir $SESSION_DIR/code"
    echo ""
fi

# Check if all phases are complete
if [ -d "$SESSION_DIR/prd" ] && [ -d "$SESSION_DIR/architecture" ] && [ -d "$SESSION_DIR/ux" ] && [ -d "$SESSION_DIR/design" ] && [ -d "$SESSION_DIR/code" ]; then
    echo -e "${GREEN}🎉 All phases complete! Ready for deployment.${NC}"
    echo ""
    echo -e "${CYAN}Deployment Commands:${NC}"
    echo "==================="
    echo "1. Test local build:"
    echo "   cd $SESSION_DIR/code && npm run build"
    echo ""
    echo "2. Deploy to Vercel:"
    echo "   cd $SESSION_DIR/code && vercel --prod"
    echo ""
    echo "3. Verify deployment:"
    echo "   Check https://partner-showcase-ui.vercel.app"
    echo ""
fi

# Show session summary
echo -e "${BLUE}📋 Session Summary${NC}"
echo "=================="
echo "Session ID: showcase-ui"
echo "Target: Partner Showcase UI for clevelsalesguy.com/partners"
echo "Framework: Next.js"
echo "Deployment: Vercel"
echo ""

# Show key requirements
echo -e "${CYAN}🎯 Key Requirements${NC}"
echo "==================="
echo "• Strategic Partner Lead persona (quick understanding)"
echo "• Technical Due-Diligence Lead persona (technical depth)"
echo "• Software Factory workflow visualization"
echo "• AI Studio research outcomes and ROI"
echo "• Case studies with metrics"
echo "• Prominent partnership CTAs"
echo "• Responsive design (desktop, tablet, mobile)"
echo "• < 2 second load time"
echo "• WCAG AA accessibility"
echo ""

# Show success criteria
echo -e "${GREEN}✅ Success Criteria${NC}"
echo "=================="
echo "• Partners understand value proposition within 60 seconds"
echo "• Demo highlights key automation phases with proof points"
echo "• Conversation requests increase by 25% within 30 days"
echo ""

# Show deployment target
echo -e "${PURPLE}🚀 Deployment Target${NC}"
echo "===================="
echo "Primary Domain: clevelsalesguy.com/partners"
echo "Staging Domain: partner-showcase-ui.vercel.app"
echo "Vercel Project: partner-showcase-ui"
echo ""

echo -e "${GREEN}Ready to proceed with the next phase!${NC}"