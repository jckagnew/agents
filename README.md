# Design-First Software Factory

> A sophisticated, auditable, and user-centric workflow that accelerates the journey from idea to production-ready code.

## 🎯 Mission

Enforce a "design-approved before code" principle by leveraging AI for key steps, reducing ambiguity, minimizing rework, and ensuring the final product aligns perfectly with a validated design.

## 🏗️ Architecture

**Platform:** Expo (React Native)
**Backend:** Supabase
**Target Platforms:** iOS, Android, Web

### Service Tiers

1. **Express Tier:** Fully-automated with **agent-in-the-loop** validation
   - Codex generates designs and validates them automatically
   - AI compares against benchmark screenshots iteratively
   - No human approval needed
   - ~4-5 minutes from intake to code
   - Best for: MVPs, prototypes, internal tools

2. **Concierge Tier:** Collaborative with **human-in-the-loop** design
   - User iterates designs in Stitch (stitch.withgoogle.com)
   - Human approval gates throughout workflow
   - Full creative control
   - ~15-30 minutes from intake to code
   - Best for: Client projects, brand-critical apps

3. **Premium Tier:** Hybrid approach
   - Stitch rapid prototype → Figma professional refinement
   - Human + agent collaboration
   - Maximum quality and control
   - Best for: Enterprise applications

## 🔄 Design Validation Approaches

### Human-in-the-Loop (Concierge Tier)

Uses **Google Stitch** for iterative human-guided design:

```
Intake → Gemini Analysis → Stitch Prompts → Human Iterates in Stitch →
Human Approves → HTML Export → Code Generation → Complete
```

**Key Feature**: Human creative control with Stitch's AI-assisted design tool

### Agent-in-the-Loop (Express Tier)

Uses **Codex multimodal capabilities** for automated validation:

```
Intake → Gemini Analysis → Codex Generates → Playwright Renders →
Codex Compares vs Benchmark → Codex Iterates (max 5x) → Code Generation → Complete
```

**Key Feature**: AI validates its own work visually, no human needed

### Comparison

| Feature | Express (Agent) | Concierge (Human) | Premium (Hybrid) |
|---------|----------------|-------------------|------------------|
| **Speed** | ~5 minutes | ~20 minutes | ~40 minutes |
| **Cost** | $1-2 per project | $2-3 per project | $5-10 per project |
| **Human Time** | 0 minutes | 15-25 minutes | 30-60 minutes |
| **Creative Control** | Limited | Full | Maximum |
| **Consistency** | High | Varies | High |
| **Best For** | MVPs, prototypes | Client work | Enterprise apps |

For detailed technical documentation, see:
- [Stitch Workflow (Human)](docs/STITCH_WORKFLOW_IMPLEMENTATION.md)
- [Agent-in-the-Loop (Codex)](docs/AGENT_IN_THE_LOOP.md)

### Division of Labor

- **Gemini:** Requirements analysis, design system generation, screen mapping
- **Codex (Express Tier):** Automated design generation with visual validation
- **Claude:** HTML→React Native conversion, code quality validation
- **Cursor:** Local development, final integration, deployment

## 📋 Phased Execution

### Phase 1: Project Foundation & Architecture ✅
- [x] Initialize project structure
- [x] Create documentation
- [ ] Initialize Expo project with Core Architecture Blueprint (Cursor)
- [ ] Set up Supabase project and schema (Codex)

### Phase 2: Intake & Auditable Prompt Engineering
- [ ] Build multi-platform intake UI (Cursor)
- [ ] Implement backend logic for intake and LLM processing (Codex)
- [ ] Build UI for prompt review and approval (Cursor)

### Phase 3: Visual Design Generation (Stitch → Figma)
- [ ] Implement backend Edge Function for Stitch-to-Figma pipeline (Codex)
- [ ] Implement UI to trigger design generation (Cursor)

### Phase 4: Design Validation & Code Generation
- [ ] Build UI for final design review and approval (Cursor)
- [ ] Implement backend validation script (Codex)
- [ ] Implement Expo application generation with testing scaffolding (Codex)

### Phase 5: Project Packaging & Handoff
- [ ] Implement backend service to bundle final project (Codex)
- [ ] Create final download screen (Cursor)

## 🚀 Quick Start

```bash
# Clone the repository
git clone git@github.com:jckagnew/design-first-software-factory.git
cd design-first-software-factory

# Install dependencies
npm install

# Start the Expo development server
npm start
```

## 📁 Project Structure

```
design-first-software-factory/
├── src/                          # Shared codebase (iOS, Android, Web)
│   ├── screens/                  # Screen components
│   ├── components/               # Reusable components
│   ├── services/                 # API and business logic
│   ├── navigation/               # Navigation setup
│   ├── theme/                    # Design tokens
│   └── utils/                    # Utilities
├── platform-overrides/           # Platform-specific code (when needed)
│   ├── ios/
│   ├── android/
│   └── web/
├── supabase/                     # Backend configuration
│   ├── migrations/               # Database migrations
│   ├── functions/                # Edge Functions
│   └── schema.sql               # Database schema
├── docs/                         # Documentation
│   ├── AGENT_SUMMARIES.md       # Agent task summaries
│   ├── ARCHITECTURE.md          # Architecture documentation
│   └── CORE_ARCHITECTURE_BLUEPRINT.md
├── PLAN.md                       # Comprehensive execution plan
└── README.md                     # This file
```

## 🔒 Privacy

This is **proprietary IP** and should remain in a private repository.

## 📝 License

Proprietary and Confidential - All Rights Reserved

---

**Current Status:** Foundation phase in progress
**Last Updated:** 2025-11-06
