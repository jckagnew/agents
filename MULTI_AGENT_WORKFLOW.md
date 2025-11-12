# Multi-Agent Repository Strategy
**Based on Claude Code Best Practices**

---

## 🎯 Branch-Per-Agent Model

### Active Agent Branches

**Claude Sessions:**
- `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP` - Current: Monorepo consolidation & deployment
- `claude/security-fixes-011CV4GmG4H3M7Seg9KC2ZcP` - Admin Console security hardening

**Cursor Sessions:**
- `cursor/*` - To be created as Cursor works

**Other Agents:**
- `codex/*` - For Codex work
- `gemini/*` - For Gemini work

### Integration Branch

**`develop`** - Integration branch where agent work merges
- All agent branches merge here
- Tested and validated
- Source for production deployments

---

## 📋 Workflow

### For Each Agent

1. **Work on your branch:**
   ```bash
   # Claude
   git checkout claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP

   # Cursor
   git checkout -b cursor/feature-name-{date}

   # Others
   git checkout -b {agent}/task-name
   ```

2. **Read centralized context:**
   - `AGENT_MANIFEST.md` - What exists, what's in progress
   - `.env` - Shared credentials
   - `COLLABORATION_STRATEGY.md` - How we work together

3. **Update manifest with your work:**
   ```markdown
   ### Claude - Session 011CV4GmG4H3M7Seg9KC2ZcP
   **Status**: In Progress
   **Task**: Monorepo consolidation
   **Branch**: claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
   **Files**: apps/, docs/, scripts/, .env system
   ```

4. **Push to your branch:**
   ```bash
   git push origin {agent}/{branch-name}
   ```

### Integration Process

**When work is ready:**

```bash
# User or designated integrator merges to develop
git checkout develop
git merge claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP --no-edit
git merge cursor/feature-name --no-edit
git push origin develop
```

---

## 📊 Single Source of Truth

### Centralized Context Files

**`AGENT_MANIFEST.md`** - Primary coordination file
- What each agent is working on
- What's completed
- What's blocked
- Where work lives (which branch)

**`.env`** - Shared credentials
- Single master file
- All agents read from here
- No duplicate credentials

**`COLLABORATION_STRATEGY.md`** - Collaboration rules
- How agents coordinate
- Conflict resolution
- Communication patterns

---

## 🔀 Git Worktree Approach (Optional)

For advanced isolation:

```bash
# Main repository
cd /home/user/agents

# Create worktree for Claude's work
git worktree add ../agents-claude claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP

# Create worktree for Cursor's work
git worktree add ../agents-cursor cursor/feature-name

# Each agent works in isolated directory
# Changes stay separate until merge
```

---

## 👥 Agent Roles

### Claude
**Role**: Infrastructure & Architecture
- Monorepo structure
- Deployment configuration
- Documentation
- Backend services

### Cursor
**Role**: Credential Management & Setup
- Harvest existing credentials
- Environment configuration
- Local development setup

### Codex
**Role**: Code Generation
- Design implementation
- Component generation
- UI code

### Gemini
**Role**: Testing & Review
- Code review
- Test generation
- Quality assurance

---

## 🔄 Merge Strategy

### Continuous Integration to Develop

```bash
# Agent completes work
git push origin {agent}/{branch}

# Update manifest
# Commit: "Complete task X - ready for integration"

# Integrator (user or designated agent) merges
git checkout develop
git fetch --all
git merge origin/{agent}/{branch} --no-edit
git push origin develop

# Other agents pull latest
git checkout {their-branch}
git merge develop  # Get latest integrated work
```

### When Conflicts Occur

1. **Detect**: Merge fails with conflicts
2. **Coordinate**: Check AGENT_MANIFEST.md to see who owns files
3. **Resolve**: File owner resolves conflicts
4. **Document**: Update manifest with resolution

---

## 📁 Shared Resources

### Read by All Agents

```
agents/
├── AGENT_MANIFEST.md       ← Central coordination
├── .env                    ← Shared credentials
├── COLLABORATION_STRATEGY.md
├── package.json            ← Shared dependencies
└── README.md
```

### Written by Specific Agents

```
agents/
├── apps/factory/           ← Claude (infrastructure)
├── apps/admin-console/     ← Claude (security fixes)
├── scripts/                ← Cursor (tooling)
└── docs/                   ← All agents (documentation)
```

---

## ✅ Benefits of This Approach

**Isolation:**
- ✅ Each agent works on separate branch
- ✅ No accidental overwrites
- ✅ Clear ownership

**Integration:**
- ✅ All work merges to `develop`
- ✅ Single tested integration point
- ✅ Easy to see what's included

**Coordination:**
- ✅ AGENT_MANIFEST.md shows all work
- ✅ Clear communication channel
- ✅ Conflict resolution process

**Flexibility:**
- ✅ Agents work independently
- ✅ Merge when ready
- ✅ Roll back if needed

---

## 🎯 Current State

### Active Work

**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`
**Contains**:
- ✅ Monorepo structure (`apps/`, `docs/`, `scripts/`)
- ✅ Master `.env` system
- ✅ Credential harvesting scripts
- ✅ All deployment documentation
- ✅ Supabase integration configs

**Status**: Ready to merge to `develop`

### Next Steps

1. **Create `develop` branch on GitHub** (user action)
2. **Merge Claude's work** → `develop`
3. **Cursor creates** `cursor/credential-harvest` branch
4. **Cursor runs** credential harvesting
5. **Merge to** `develop`
6. **All agents pull** from `develop` for latest

---

## 📝 For New Agents

When you join:

1. **Read centralized context:**
   ```bash
   cat AGENT_MANIFEST.md
   cat COLLABORATION_STRATEGY.md
   cat .env  # Check credentials
   ```

2. **Create your branch:**
   ```bash
   git checkout develop
   git checkout -b {agent-name}/task-description
   ```

3. **Do your work**

4. **Update manifest:**
   ```markdown
   ### {Agent} - {Date}
   **Task**: Description
   **Branch**: {agent}/task
   **Status**: In Progress
   ```

5. **Request merge when ready**

---

**Last Updated**: 2025-11-12
**Model**: Branch-per-agent with integration branch
**Status**: ✅ Implemented
