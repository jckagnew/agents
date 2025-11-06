# Design-First Software Factory

> A sophisticated, auditable, and user-centric workflow that accelerates the journey from idea to production-ready code.

## 🎯 Mission

Enforce a "design-approved before code" principle by leveraging AI for key steps, reducing ambiguity, minimizing rework, and ensuring the final product aligns perfectly with a validated design.

## 🏗️ Architecture

**Platform:** Expo (React Native)
**Backend:** Supabase
**Target Platforms:** iOS, Android, Web

### Service Tiers

1. **Express Tier:** Fully-automated path - provide requirements, get notified upon completion
2. **Concierge Tier:** Collaborative path with explicit approval steps for prompt engineering and design review

### Division of Labor

- **Gemini (Orchestrator):** Project management, task delegation, communication
- **Codex (Backend Specialist):** Supabase schema, Edge Functions, service integrations
- **Cursor (Frontend/UI Specialist):** User-facing Expo application
- **Claude (Foundation Architect):** Initial project structure, documentation, architecture

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
