# 🚀 IMPORTANT UPDATE: Repository Consolidation Complete

**Date**: 2025-11-12
**From**: Claude
**To**: Cursor, Codex, Gemini
**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`

---

## ⚠️ CRITICAL CHANGES - READ BEFORE STARTING WORK

The repository structure has been **completely reorganized** into a unified monorepo layout. This affects ALL work going forward.

---

## 🎯 What Changed

### 1. Repository Consolidation ✅

**OLD Structure** (Fragmented):
```
agents/
├── src/                    # Factory code
├── docs/                   # Factory docs
├── admin-console/          # Different branch
└── Multiple .env files
```

**NEW Structure** (Consolidated):
```
agents/ ◄── ONE MASTER REPOSITORY
├── apps/
│   ├── factory/            # Factory code (was src/)
│   │   ├── src/
│   │   └── docs/
│   └── admin-console/      # Admin Console
│
├── supabase/
│   ├── config.toml         # Links to design-factory-admin
│   ├── migrations/
│   └── functions/
│
├── docs/                   # Centralized docs
│   └── deployment/
│
├── scripts/                # Helper scripts
│   ├── setup-env.sh
│   └── validate-env.sh
│
└── .env                    # MASTER environment file
```

### 2. Path Changes 🔄

**UPDATE YOUR REFERENCES:**

| Old Path | New Path |
|----------|----------|
| `src/api/server.ts` | `apps/factory/src/api/server.ts` |
| `src/screens/` | `apps/factory/src/screens/` |
| `src/services/` | `apps/factory/src/services/` |
| `docs/MASTER_WORKFLOW.md` | `apps/factory/docs/MASTER_WORKFLOW.md` |
| `WEB_DEPLOYMENT.md` | `docs/deployment/WEB_DEPLOYMENT.md` |
| `PHASE_1_DEPLOYMENT.md` | `docs/deployment/PHASE_1_DEPLOYMENT.md` |

### 3. Single Master .env File 🔐

**STOP asking for credentials repeatedly!**

All credentials are now in **ONE** master `.env` file at repository root:

```bash
# Check if .env exists BEFORE asking for credentials
if [ -f .env ]; then
  echo "✅ Credentials available"
  # Load and use them
else
  echo "📋 Run: npm run env:setup"
fi
```

**What's in master .env:**
- Supabase credentials (shared by Factory + Admin Console)
- AI API keys (OpenAI, Anthropic, Google)
- Redis URL
- Stripe keys
- All configuration

**Scripts:**
```bash
npm run env:setup      # Create .env from template
npm run env:validate   # Check all required variables
```

---

## 📋 MANDATORY CHECKLIST - Before Starting ANY Work

### Step 1: Read Documentation
- [ ] Read `AGENT_MANIFEST.md` - Single source of truth for all work
- [ ] Read `AGENT_COLLABORATION_PROTOCOL.md` - How we work together
- [ ] Read `ENV_MANAGEMENT_STRATEGY.md` - Environment configuration

### Step 2: Check Environment
```bash
# Run this first!
npm run env:validate
```

If validation fails, run:
```bash
npm run env:setup
# Then edit .env and add real credentials
```

### Step 3: Check Existing Work
- [ ] Review `AGENT_MANIFEST.md` "COMPLETED WORK" section
- [ ] Review `AGENT_MANIFEST.md` "WORK IN PROGRESS" section
- [ ] Check if work already exists before creating new code

### Step 4: Update Manifest When Done
- [ ] Update `AGENT_MANIFEST.md` with what you completed
- [ ] Update "Last Updated" date
- [ ] Commit manifest with your changes

---

## 🗺️ Current State of Project

### ✅ COMPLETED (Don't recreate these!)

1. **Supabase Backend** - EXISTING `design-factory-admin` project
   - Database schema (5 tables)
   - Storage buckets (3)
   - Edge Functions (4)
   - **DO NOT create new Supabase project!**

2. **Expo Factory** - Code complete at `apps/factory/`
   - Express backend with AI orchestration
   - Expo frontend (iOS/Android/Web)
   - Ready for deployment

3. **Admin Console** - Code complete on `claude/security-fixes-*` branch
   - Security hardened
   - Ready to merge into `apps/admin-console/`

4. **Deployment Configs** - Ready to use
   - `railway.json` - Backend deployment
   - `vercel.json` - Frontend deployment
   - `.env.example` - Master environment template

5. **Documentation** - Comprehensive guides in `docs/deployment/`
   - Phase 1 deployment guide
   - Web deployment guide
   - Integration roadmap
   - Repository consolidation plan
   - Environment management strategy

### 🚧 WORK IN PROGRESS

**Current Task**: Phase 1 Deployment
- Status: Ready to execute
- **BLOCKER**: Need Supabase credentials from `design-factory-admin`

**Next Steps**:
1. Get Supabase credentials
2. Link to existing project: `supabase link --project-ref design-factory-admin`
3. Deploy Express backend to Railway
4. Deploy Expo frontend to Vercel
5. Merge Admin Console code

---

## 🚨 ANTI-PATTERNS - Don't Do These!

### ❌ DON'T:
1. Create new Supabase project (use existing `design-factory-admin`)
2. Run database migrations (schema exists!)
3. Create duplicate .env files in apps/
4. Ask for credentials without checking root .env first
5. Work without reading AGENT_MANIFEST.md
6. Recreate documentation that exists in `docs/deployment/`
7. Use old paths (`src/` instead of `apps/factory/src/`)

### ✅ DO:
1. Check AGENT_MANIFEST.md before starting
2. Use master .env at repository root
3. Update AGENT_MANIFEST.md when you complete work
4. Follow new consolidated structure
5. Link to existing infrastructure
6. Reference existing documentation

---

## 📚 Key Documentation Files

**Read these in order:**

1. **`AGENT_MANIFEST.md`** - What exists, what's in progress, what's planned
2. **`AGENT_COLLABORATION_PROTOCOL.md`** - How to coordinate with other agents
3. **`ENV_MANAGEMENT_STRATEGY.md`** - How environment variables work
4. **`docs/deployment/REPOSITORY_CONSOLIDATION_PLAN.md`** - Why we consolidated
5. **`docs/deployment/EXISTING_INFRASTRUCTURE_INTEGRATION.md`** - Supabase integration

**Deployment Guides:**
- `docs/deployment/PHASE_1_DEPLOYMENT.md` - Step-by-step deployment
- `docs/deployment/WEB_DEPLOYMENT.md` - Comprehensive web deployment
- `docs/deployment/INTEGRATION_ROADMAP.md` - Overall strategy

**Factory Documentation:**
- `apps/factory/docs/MASTER_WORKFLOW.md` - Factory workflow
- `apps/factory/docs/EXPO_UNIVERSAL_ARCHITECTURE.md` - Universal deployment

---

## 🔄 Updated Package Scripts

```json
{
  "api": "ts-node apps/factory/src/api/server.ts",
  "api:dev": "nodemon --exec ts-node apps/factory/src/api/server.ts",
  "env:setup": "bash scripts/setup-env.sh",
  "env:validate": "bash scripts/validate-env.sh"
}
```

---

## 🎯 Quick Start for AI Agents

```bash
# 1. Check environment
npm run env:validate

# 2. If no .env exists, create it
npm run env:setup
# Edit .env and add credentials

# 3. Read manifest to see what exists
cat AGENT_MANIFEST.md

# 4. Start development
npm run api:dev    # Factory backend
npm run start      # Factory frontend
```

---

## 🤝 Collaboration Rules

**Format for updates**: `[AGENT_NAME] [DATE] [ACTION] [LOCATION]`

Example:
```
Cursor 2025-11-12 COMPLETED: Merged Admin Console into apps/admin-console/
Codex 2025-11-12 IN PROGRESS: Deploying Factory backend to Railway
Gemini 2025-11-12 REVIEWING: Security fixes in Admin Console
```

**When you complete work:**
1. Update `AGENT_MANIFEST.md`
2. Commit manifest with your changes
3. Push to your branch

---

## 💡 TL;DR - Quick Summary

1. **Repository consolidated** into monorepo: `apps/`, `supabase/`, `docs/`
2. **Factory code moved** from `src/` to `apps/factory/`
3. **Single .env file** at root - no duplicates
4. **Read AGENT_MANIFEST.md first** - it's the source of truth
5. **Check environment** before asking for credentials: `npm run env:validate`
6. **Use existing Supabase** project: `design-factory-admin`
7. **Update manifest** when you complete work

---

## 🚀 Ready to Work?

**Checklist:**
- [ ] I've read `AGENT_MANIFEST.md`
- [ ] I've run `npm run env:validate`
- [ ] I understand the new structure
- [ ] I know to use `apps/factory/` not `src/`
- [ ] I won't create new Supabase project
- [ ] I'll update manifest when done

**If all checked, you're ready to go!**

---

**Questions?** Check these files:
- `AGENT_MANIFEST.md` - What exists
- `AGENT_COLLABORATION_PROTOCOL.md` - How to collaborate
- `ENV_MANAGEMENT_STRATEGY.md` - Environment setup
- `docs/deployment/` - All deployment guides

**Last Updated**: 2025-11-12 by Claude
**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`
