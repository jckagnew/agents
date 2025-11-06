# Agent Collaboration Guide - No Manual Syncing Required

**Problem Solved:** All agents work in the SAME repository with automatic coordination via git.

---

## 🎯 Single Source of Truth

**Repository:** `jckagnew/agents`
**Workspace Path:** `/home/user/agents/`
**Project Path:** `/home/user/agents/design-first-software-factory/`

**All agents (Claude, Codex, Gemini, Cursor) work in THIS location.**

---

## 📋 Agent Workflow - Seamless Collaboration

### For ALL Agents:

**1. Always Work in the Same Directory**
```bash
cd /home/user/agents
# Or for project-specific work:
cd /home/user/agents/design-first-software-factory
```

**2. Check Latest Changes (Before Starting)**
```bash
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

**3. Do Your Work**
- Claude: Architecture, documentation, code review
- Codex: Supabase schema, Edge Functions, API integrations
- Gemini: Project coordination, design integration, requirements
- Cursor: Full-stack implementation, testing, deployment

**4. Commit Your Changes**
```bash
git add .
git commit -m "Descriptive message of what you did"
```

**5. Push to Shared Branch**
```bash
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

**6. Other Agents Pull Your Changes**
```bash
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

---

## ✅ Benefits - No Manual Sync!

✅ **Single workspace** - All agents at `/home/user/agents/`
✅ **Automatic coordination** - Git handles file syncing
✅ **Full history** - See all changes from all agents
✅ **No conflicts** - Agents work on different files naturally
✅ **Zero manual work** - Just pull, work, commit, push

---

## 🤝 File Ownership by Agent

### Claude (Principal Architect + Tech Lead)
**Owns:**
- `docs/ARCHITECTURE.md`
- `docs/COMPREHENSIVE_CRITIQUE.md`
- `docs/CORE_ARCHITECTURE_BLUEPRINT.md`
- Architecture decisions documentation

**Workflow:**
```bash
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Edit architecture files
vim docs/ARCHITECTURE.md

git add docs/ARCHITECTURE.md
git commit -m "Update architecture: Add multi-framework support"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

---

### Codex (Infrastructure + API Specialist)
**Owns:**
- `supabase/migrations/*.sql`
- `supabase/functions/*/index.ts`
- `lib/gemini.ts`, `lib/figma.ts`
- `docs/API_INTEGRATIONS.md`

**Workflow:**
```bash
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Create new migration
supabase migration new add_audit_tables

# Edit migration
vim supabase/migrations/20251106_add_audit_tables.sql

git add supabase/migrations/
git commit -m "Add audit_logs and ai_generations tables"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Other agents automatically get your changes when they pull
```

---

### Gemini (Creative Director + Project Orchestrator)
**Owns:**
- `PROJECT_STATUS.md` (project tracking)
- `SPRINT_PLAN.md` (current sprint)
- `docs/REQUIREMENTS.md`
- `docs/DESIGN_TOKENS.md`

**Workflow:**
```bash
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Update project status
vim PROJECT_STATUS.md

git add PROJECT_STATUS.md
git commit -m "Update sprint progress: Phase 1 complete"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

---

### Cursor (Full-Stack Implementation Lead)
**Owns:**
- `src/**/*` (all application code)
- `tests/**/*` (all test files)
- `package.json`, `tsconfig.json`
- CI/CD configuration

**Workflow:**
```bash
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Implement feature
mkdir -p src/screens
vim src/screens/IntakeScreen.tsx

git add src/screens/IntakeScreen.tsx
git commit -m "Implement intake screen with form validation"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

---

## 🔄 Typical Collaboration Flow

### Example: Codex Creates Schema, Cursor Uses It

**Monday 9am - Codex:**
```bash
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Create schema
vim supabase/migrations/20251106_initial_schema.sql

git add supabase/migrations/
git commit -m "Add initial database schema"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

**Monday 10am - Cursor:**
```bash
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
# ✅ Cursor now has Codex's schema!

# Read schema to understand structure
cat supabase/migrations/20251106_initial_schema.sql

# Build UI using that schema
vim src/services/supabase.ts

git add src/services/
git commit -m "Add Supabase client using Codex's schema"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

**Monday 11am - Claude:**
```bash
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
# ✅ Claude now has both Codex's schema and Cursor's client!

# Review both for architecture compliance
git log --oneline -5
git diff HEAD~2

# Provide feedback
vim docs/CODE_REVIEW.md

git add docs/CODE_REVIEW.md
git commit -m "Code review: Schema and client look good, minor suggestions"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

**Monday 12pm - Gemini:**
```bash
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
# ✅ Gemini sees everyone's work!

# Update project tracker
vim PROJECT_STATUS.md
# Mark schema and client as complete

git add PROJECT_STATUS.md
git commit -m "Update status: Schema and client complete ✓"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

**Result:** All agents coordinated seamlessly without Jack doing anything!

---

## 🚨 Common Mistakes to Avoid

❌ **Don't work in multiple directories**
```bash
# WRONG - Creates sync problems
/Users/jackagnew/projects/design-first-software-factory/  ❌
/home/user/agents/design-first-software-factory/          ✅
```

❌ **Don't forget to pull before starting**
```bash
# WRONG - Work on stale code
cd /home/user/agents/design-first-software-factory
vim src/file.ts  ❌

# RIGHT - Always pull first
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR  ✅
vim src/file.ts
```

❌ **Don't work on the same file simultaneously**
```bash
# If Cursor is editing src/App.tsx,
# Codex should work on supabase/functions instead
# Natural file ownership prevents conflicts
```

---

## 📞 Communication Between Agents

### Async Communication (Preferred)
Use git commit messages and markdown files:

```bash
# Codex leaves note for Cursor:
echo "## API Ready\n\nThe /intake-processor endpoint is live. See supabase/functions/intake-processor/README.md for usage." > CODEX_TO_CURSOR.md
git add CODEX_TO_CURSOR.md
git commit -m "Codex: API endpoint ready for integration"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

### Questions/Blockers
Create markdown files for discussions:

```bash
# Cursor has a question:
vim QUESTIONS.md
# Add: "Q for Codex: What's the rate limit on /design-generator?"

git add QUESTIONS.md
git commit -m "Cursor: Question about rate limiting"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Codex answers:
vim QUESTIONS.md
# Add answer

git add QUESTIONS.md
git commit -m "Codex: Rate limit is 100 req/hour"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

---

## 🎯 Jack's Role - Monitor, Don't Manage

**Jack should:**
- ✅ Review git history to see progress
- ✅ Pull the repo to see latest state
- ✅ Provide high-level direction
- ✅ Make final decisions on architecture changes

**Jack should NOT:**
- ❌ Manually copy files between directories
- ❌ Sync repositories
- ❌ Coordinate agent tasks (Gemini does this)
- ❌ Merge agent work manually (git does this)

**Jack's workflow:**
```bash
# Check what agents have done
cd /home/user/agents/design-first-software-factory
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
git log --oneline --graph --all --decorate

# See current state
ls -la
cat PROJECT_STATUS.md

# Provide direction
vim JACK_DECISIONS.md
# "Decision: Proceed with 2-week re-architecture"

git add JACK_DECISIONS.md
git commit -m "Jack: Approve re-architecture plan"
git push origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

---

## ✅ Summary - Zero Manual Work

1. **All agents work at:** `/home/user/agents/design-first-software-factory/`
2. **All agents use git:** Pull → Work → Commit → Push
3. **Git coordinates everything:** No manual file copying
4. **Natural file ownership:** Agents work on different files
5. **Async communication:** Via commit messages and markdown files
6. **Jack monitors:** Via git log, not manual coordination

**This is scalable, seamless, and requires zero manual syncing.**

---

## 🚀 Getting Started Right Now

**For Codex (and all other agents):**

```bash
# Step 1: Navigate to shared workspace
cd /home/user/agents/design-first-software-factory

# Step 2: Pull latest
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Step 3: Read critique documents
cat CODEX_SUMMARY.md
cat EXECUTIVE_SUMMARY.md
cat docs/COMPREHENSIVE_CRITIQUE.md

# Step 4: Start your work
# (All files are right here, no syncing needed!)
```

**You're all working in the same place. It just works.™**
