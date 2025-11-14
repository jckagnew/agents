# AGENT MANIFEST
**Single Source of Truth for Multi-Agent Collaboration**

**Last Updated**: 2025-11-14 by Claude (Credential Harvesting Complete)
**Purpose**: Prevent duplicate work across Claude, Cursor, Codex, and Gemini

**🎉 LATEST MILESTONE**: Successfully harvested 116 credentials from 25 projects. Multi-agent git workflow operational with develop branch on GitHub.

---

## 🎯 THE PROBLEM WE'RE SOLVING

**Issue**: Multiple AI agents working on the same project across multiple repos/branches without coordination.

**Result**:
- ❌ Duplicate work being created
- ❌ Time wasted searching for "latest version"
- ❌ Conflicting plans and implementations
- ❌ No single source of truth

**Solution**: This manifest - READ IT FIRST, UPDATE IT WHEN YOU COMPLETE WORK.

---

## 📍 SINGLE SOURCE OF TRUTH

### Primary Repository
**Repository**: `jckagnew/agents` (THIS REPO - you're reading it now!)
**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`
**Purpose**: Unified workspace for ALL Factory and Admin Console work

### Other Repositories (Reference Only - DO NOT DUPLICATE)
1. **c-level-sales-guy**: Docker templates, DevOps scaffolding
2. **clevel-sales-guy**: Next.js website (marketing site)
3. **design-first-software-factory**: Supabase backend config (`design-factory-admin` project)

---

## 🗺️ WHAT EXISTS WHERE

### ✅ COMPLETED WORK

#### 1. Supabase Backend Infrastructure (DEPLOYED)
**Location**: Existing Supabase project `design-factory-admin`
**Created By**: Cursor (based on repository analysis)
**Status**: ✅ Production-ready
**Components**:
- Database schema (5 tables): admin_users, customers, projects, project_notes, invoices
- Storage buckets (3): designs, deliverables, avatars
- Edge Functions (4): admin-customers, admin-projects, upload-design, stripe-webhook

**Access**:
- Dashboard: https://supabase.com/dashboard/project/design-factory-admin
- API Base: https://design-factory-admin.supabase.co

#### 2. Admin Console (Expo React Native)
**Location**: `agents/admin-console/`
**Branch**: `claude/security-fixes-011CV4GmG4H3M7Seg9KC2ZcP`
**Created By**: Claude (previous session)
**Status**: ✅ Security-hardened, ready for deployment
**Platforms**: iOS, Android, Web
**Key Features**:
- Customer CRUD operations
- Project management
- Invoice tracking
- Project notes
- Security fixes: CORS validation, input sanitization, rate limiting, soft deletes, audit logging

**Documentation**:
- `/admin-console/WEB_DEPLOYMENT.md` (850+ lines)
- `/admin-console/DEPLOYMENT.md` (iOS/Android/Web)
- `/admin-console/SECURITY_FIXES_SUMMARY.md` (492 lines)

#### 3. Expo Software Factory (Universal App)
**Location**: `agents/apps/factory/` ◄── CONSOLIDATED LOCATION
**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP` (THIS BRANCH)
**Created By**: Claude (previous session: design-first-implementation)
**Status**: ✅ Code complete, ready for deployment, **structure consolidated**
**Platforms**: iOS, Android, Web
**Components**:
- Frontend: Expo app with Expo Router
- Backend: Express server (`apps/factory/src/api/server.ts`)
- Services: AI orchestration (OpenAI, Anthropic, Google Gemini)
- Job Queue: BullMQ with Redis
- Screens: ProjectIntakeScreen, StitchUploadScreen

**Documentation**:
- `/docs/deployment/WEB_DEPLOYMENT.md` (14-part deployment guide)
- `/apps/factory/docs/EXPO_UNIVERSAL_ARCHITECTURE.md`
- `/apps/factory/docs/MASTER_WORKFLOW.md`
- `/README.md`

#### 4. Deployment Configurations
**Location**: `agents/` (root)
**Created By**: Claude (this session)
**Status**: ✅ Ready to use
**Files**:
- `railway.json` - Railway deployment config
- `vercel.json` - Vercel deployment config
- `.env.example` - Complete environment template (references existing Supabase)
- `.env.production.template` - Production environment template

#### 5. Integration Documentation
**Location**: `agents/docs/deployment/` ◄── CONSOLIDATED LOCATION
**Created By**: Claude (this session)
**Status**: ✅ Complete and organized
**Files**:
- `docs/deployment/INTEGRATION_ROADMAP.md` - Overall integration strategy
- `docs/deployment/PHASE_1_DEPLOYMENT.md` - Step-by-step deployment guide
- `docs/deployment/EXISTING_INFRASTRUCTURE_INTEGRATION.md` - How to use existing Supabase
- `docs/deployment/REPOSITORY_CONSOLIDATION_PLAN.md` - Repository consolidation guide
- `docs/deployment/WEB_DEPLOYMENT.md` - Comprehensive web deployment guide

#### 6. Next.js Legacy Code (TO BE DEPRECATED)
**Location**: `agents/software-factory/`
**Created By**: Unknown (early work)
**Status**: ⚠️ To be deprecated after migration
**Components**:
- `software-factory/admin/` - Next.js admin dashboard
- `software-factory/splash-creator/` - Next.js splash creator

**Preserved Logic**: `software-factory/NEXTJS_LOGIC_PRESERVATION.md` (Agent created comprehensive preservation doc)

---

## 🚧 WORK IN PROGRESS

### Current Task: Phase 1 Deployment - Credential Validation
**Owner**: Claude + Cursor (multi-agent)
**Status**: 🔄 In Progress - Blocked on Supabase Credentials
**Branch**: `develop` (multi-agent integration branch)
**Progress**:
- ✅ Repository consolidation complete (apps/, docs/, scripts/, supabase/)
- ✅ Multi-agent git workflow established (develop branch on GitHub)
- ✅ Credential harvesting complete (116 credentials from 25 projects)
- ✅ Master .env system created with template
- ✅ Deployment readiness checks created
- ✅ OPENAI_API_KEY, ANTHROPIC_API_KEY, REDIS_URL configured
- ❌ **BLOCKING**: SUPABASE_ANON_KEY still has placeholder value
- ❌ **BLOCKING**: SUPABASE_SERVICE_ROLE_KEY still has placeholder value
- ⏳ **NEXT**: Copy Supabase credentials from harvested files to master .env
- ⏳ Link Supabase CLI and deploy Edge Functions
- ⏳ Deploy Express backend to Railway
- ⏳ Deploy Expo frontend to Vercel

**Blocking**: Supabase credentials exist in harvested files but need to be copied to master .env
**See**: `DEPLOYMENT_STATUS.md` for detailed status and fix options

---

## 📋 PLANNED WORK (Not Started)

### Phase 2: Deploy Admin Console
**Owner**: Unassigned
**Status**: ⏳ Waiting for Phase 1 completion
**Dependencies**: Factory backend must be deployed first
**Tasks**:
1. Configure Admin Console with Factory API URL
2. Deploy to Vercel (web)
3. Build iOS/Android with EAS
4. Test "Generate App" integration

### Phase 3: Merge Branches & Monorepo
**Owner**: Unassigned
**Status**: ⏳ Planned
**Tasks**:
1. Merge security-fixes branch into expo-factory-web-deployment
2. Create unified monorepo structure
3. Set up shared component library
4. Apply security fixes to Factory backend

### Phase 4: Feature Migration from Next.js
**Owner**: Unassigned
**Status**: ⏳ Planned
**Tasks**:
1. Migrate health monitoring system
2. Migrate design token editing
3. Migrate splash creator workflow
4. Deprecate old Next.js code

---

## 🔍 HOW TO USE THIS MANIFEST

### Before Starting Any Work
1. **READ THIS MANIFEST** - Check if work already exists
2. **CHECK ENVIRONMENT** - Verify master .env exists (see below)
3. **CHECK BRANCHES** - Review what's on each branch
4. **REVIEW DOCUMENTATION** - Read existing docs before creating new ones
5. **ASK THE USER** - If unclear, ask rather than duplicate

### Environment Configuration (Critical!)
**⚠️ STOP asking for credentials repeatedly!**

All credentials are in **ONE master .env file** at repository root.

**Before requesting API keys, CHECK**:
```bash
# Does .env exist?
if [ -f .env ]; then
  echo "✅ Credentials available"
  # Load and use them
else
  echo "📋 Run: npm run env:setup"
fi
```

**What's in master .env**:
- Supabase credentials (shared by Factory + Admin Console)
- AI API keys (OpenAI, Anthropic, Google)
- Redis URL
- Stripe keys
- All configuration

**Documentation**: [`ENV_MANAGEMENT_STRATEGY.md`](./ENV_MANAGEMENT_STRATEGY.md)

**Scripts**:
- `npm run env:setup` - Create .env from template
- `npm run env:validate` - Check all required variables

### When You Complete Work
1. **UPDATE THIS MANIFEST** - Add your completed work
2. **UPDATE LAST MODIFIED** - Change date and agent name at top
3. **COMMIT CHANGES** - Ensure manifest is committed with your work
4. **DOCUMENT LOCATION** - Be specific about branch, directory, file names

### Communication Protocol
**Format**: `[AGENT_NAME] [DATE] [ACTION] [LOCATION]`

Example:
```
Claude 2025-11-12 COMPLETED: Admin Console security fixes on branch claude/security-fixes-011CV4GmG4H3M7Seg9KC2ZcP
Cursor 2025-11-09 DEPLOYED: Supabase backend design-factory-admin with 5 tables and 4 Edge Functions
```

---

## 🎯 DECISION LOG

### Key Architectural Decisions

**Decision 1: Use Existing Supabase Project**
- **Date**: 2025-11-12
- **Decided By**: Claude (based on Cursor's repository analysis)
- **Decision**: Use existing `design-factory-admin` Supabase project, DO NOT create new
- **Rationale**: Infrastructure already deployed, schema exists, avoid duplication

**Decision 2: Factory Must Deploy First**
- **Date**: 2025-11-12
- **Decided By**: User + Claude
- **Decision**: Admin Console depends on Factory API, deploy Factory first
- **Rationale**: Admin Console cannot generate apps without Factory backend

**Decision 3: Deprecate Next.js Implementations**
- **Date**: 2025-11-12
- **Decided By**: User
- **Decision**: Move from Next.js to Expo for universal deployment
- **Rationale**: Expo provides iOS/Android/Web from single codebase

**Decision 4: Single Repository as Source of Truth**
- **Date**: 2025-11-12
- **Decided By**: User
- **Decision**: Use `jckagnew/agents` as primary repo, consolidate all work here
- **Rationale**: Prevent duplicate work across multiple repos and AI agents

---

## 🚨 ANTI-PATTERNS TO AVOID

### ❌ DON'T DO THESE THINGS

1. **Don't create new Supabase project** - Use existing `design-factory-admin`
2. **Don't run database migrations** - Schema already exists
3. **Don't recreate Edge Functions** - Update existing ones
4. **Don't create duplicate deployment configs** - Check manifest first
5. **Don't work in isolation** - Update manifest when you complete work
6. **Don't assume nothing exists** - READ THIS MANIFEST FIRST
7. **Don't create new documentation** - Update existing docs
8. **Don't deploy Admin Console first** - Factory must deploy first

### ✅ DO THESE THINGS

1. **Read manifest before starting** - Avoid duplicate work
2. **Update manifest when done** - Help next agent
3. **Reference existing work** - Build on what exists
4. **Commit manifest with changes** - Keep it current
5. **Ask user if unclear** - Better to clarify than duplicate
6. **Follow deployment order** - Factory → Admin Console
7. **Use existing infrastructure** - Don't recreate

---

## 📞 AGENT HANDOFF CHECKLIST

When handing off to another agent (Cursor, Codex, Gemini):

- [ ] Updated this AGENT_MANIFEST.md
- [ ] Committed all changes to git
- [ ] Documented what was completed
- [ ] Documented what's next
- [ ] Noted any blockers
- [ ] Listed any credentials needed
- [ ] Updated project status

---

## 🎓 FOR NEW AGENTS JOINING

**If you're Claude, Cursor, Codex, or Gemini starting fresh**:

1. **READ THIS FILE FIRST** - It's the source of truth
2. **Check INTEGRATION_ROADMAP.md** - Understand overall strategy
3. **Review branch structure** - Know what's where
4. **Read existing documentation** - Don't recreate
5. **Update manifest when done** - Help the next agent

**Current branch strategy**:
- `claude/security-fixes-*` - Admin Console work
- `claude/expo-factory-web-deployment-*` - Factory deployment work
- `claude/comprehensive-technical-review-guide-*` - Documentation
- `main` - Udemy course materials (DO NOT MODIFY)

---

## 📊 REPOSITORY STRUCTURE (CONSOLIDATED)

```
agents/ ◄── ONE MASTER REPOSITORY
├── AGENT_MANIFEST.md ◄── YOU ARE HERE (READ ME FIRST!)
├── AGENT_COLLABORATION_PROTOCOL.md (how agents work together)
├── README.md (project overview with agent warnings)
│
├── apps/ ◄── ALL APPLICATIONS (MONOREPO STRUCTURE)
│   ├── factory/ (Expo Factory - iOS/Android/Web)
│   │   ├── src/
│   │   │   ├── api/server.ts (Express backend)
│   │   │   ├── screens/ (Factory UI)
│   │   │   └── services/ (AI orchestration)
│   │   └── docs/ (Factory-specific docs)
│   │
│   └── admin-console/ (Admin Console - iOS/Android/Web)
│       ├── app/ (screens) [on branch: claude/security-fixes-*]
│       ├── WEB_DEPLOYMENT.md
│       ├── DEPLOYMENT.md
│       └── SECURITY_FIXES_SUMMARY.md
│
├── supabase/ (Backend for design-factory-admin project)
│   ├── config.toml ◄── Links to EXISTING project
│   ├── migrations/ (database schema)
│   └── functions/ (Edge Functions)
│       ├── capture-screenshot/
│       ├── process-code-generation/
│       └── convert-html-to-react-native/
│
├── docs/ ◄── CENTRALIZED DOCUMENTATION
│   ├── deployment/
│   │   ├── PHASE_1_DEPLOYMENT.md
│   │   ├── WEB_DEPLOYMENT.md
│   │   ├── INTEGRATION_ROADMAP.md
│   │   ├── EXISTING_INFRASTRUCTURE_INTEGRATION.md
│   │   └── REPOSITORY_CONSOLIDATION_PLAN.md
│   ├── architecture/ (architectural docs)
│   └── api/ (API documentation)
│
├── software-factory/ (LEGACY - to be deprecated)
│   ├── admin/ (Next.js)
│   ├── splash-creator/ (Next.js)
│   └── NEXTJS_LOGIC_PRESERVATION.md
│
├── railway.json (backend deployment config)
├── vercel.json (frontend deployment config)
├── .env.example (environment template)
├── app.json (Expo config)
└── package.json (shared dependencies)
```

**✅ Consolidation Status**: Phase 1 Complete (2025-11-12)
- Factory code moved to `apps/factory/`
- Admin Console placeholder created at `apps/admin-console/`
- Supabase configs centralized with `config.toml`
- Documentation organized in `docs/`
- Single source of truth established

---

## 🔗 EXTERNAL REFERENCES

**Supabase Project**:
- Name: design-factory-admin
- Dashboard: https://supabase.com/dashboard/project/design-factory-admin
- Created by: Cursor
- Schema: design-first-software-factory/supabase/migrations/001_core_schema.sql

**Other Repos (Reference Only)**:
- jckagnew/c-level-sales-guy - Docker templates
- jckagnew/clevel-sales-guy - Marketing website
- jckagnew/design-first-software-factory - Supabase backend config

---

## ✅ QUICK STATUS CHECK

**Can we deploy Phase 1?** ⏳ Almost - need Supabase credentials
**Can we deploy Admin Console?** ❌ No - Factory must deploy first
**Is database ready?** ✅ Yes - schema exists in design-factory-admin
**Are Edge Functions ready?** ✅ Yes - 4 functions exist, just need to update
**Is backend code ready?** ✅ Yes - Express server in src/api/server.ts
**Is frontend code ready?** ✅ Yes - Expo app with screens
**Do we have deployment configs?** ✅ Yes - railway.json, vercel.json
**Do we have documentation?** ✅ Yes - comprehensive guides exist

**BLOCKER**: Supabase ANON_KEY and SERVICE_ROLE_KEY have placeholder values in .env
**Fix**: Run `scripts/copy-harvested-credentials.sh` on Mac (Cursor) to copy real values from harvested files
**Status Report**: See `DEPLOYMENT_STATUS.md` for detailed fix options

---

**🤝 Remember**: We're all working on the SAME project. Update this manifest to help each other!

**Last Updated**: 2025-11-14 by Claude (Credential Harvesting Complete, Multi-Agent Workflow Operational)
**Next Agent**: Please update this file when you make changes!

---

## 🎉 CONSOLIDATION COMPLETED

**Date**: 2025-11-12
**Completed By**: Claude
**What Was Done**:
- ✅ Restructured Factory code: `src/` → `apps/factory/`
- ✅ Created Admin Console placeholder: `apps/admin-console/`
- ✅ Centralized Supabase configs with `config.toml`
- ✅ Organized documentation: `docs/deployment/`
- ✅ Updated all path references in `package.json`
- ✅ Established single source of truth

**Next Steps for Other Agents**:
1. Merge Admin Console code from `claude/security-fixes-*` branch into `apps/admin-console/`
2. Continue Phase 1 deployment with consolidated structure
3. Migrate additional repos (website, devops) as needed
