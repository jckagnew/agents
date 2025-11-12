# Setup Instructions: Multi-Agent Workflow

**Goal**: Establish branch-per-agent model with `develop` as integration branch

**Time**: 10 minutes

---

## Step 1: Create Integration Branch (You Run This)

On your local machine or GitHub web interface:

### Option A: GitHub Web Interface (Easiest)

1. Go to: https://github.com/jckagnew/agents
2. Click the branch dropdown (currently shows "main")
3. Type: `develop`
4. Click "Create branch: develop from main"
5. Done! ✅

### Option B: Command Line

```bash
cd /home/user/agents
git fetch origin
git checkout main
git checkout -b develop
git push origin develop
```

---

## Step 2: Merge Claude's Consolidation Work (You Run This)

Now merge the consolidation work into `develop`:

```bash
cd /home/user/agents
git checkout develop
git fetch origin
git merge origin/claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP --no-edit
git push origin develop
```

**This gives `develop` the complete monorepo structure:**
- ✅ `apps/factory/` - Factory source code
- ✅ `apps/admin-console/` - Admin console placeholder
- ✅ `docs/deployment/` - All deployment guides
- ✅ `scripts/` - Environment management scripts
- ✅ `supabase/config.toml` - Supabase integration
- ✅ `.env` - Master credentials file
- ✅ All documentation

**Verify the merge worked:**
```bash
ls -la apps/factory/
ls -la docs/deployment/
ls -la scripts/
```

---

## Step 3: Instructions for Cursor

**Copy/paste this to Cursor:**

```bash
# Fetch latest
cd /home/user/agents
git fetch origin

# Checkout develop (now has all consolidation work)
git checkout develop
git pull origin develop

# Verify structure exists
ls -la apps/factory/
ls -la docs/deployment/
ls -la scripts/

# Create your working branch
git checkout -b cursor/credential-harvest-$(date +%Y%m%d)

# Run credential harvesting
bash scripts/cursor-harvest-all-credentials.sh

# Review what was found
cat HARVEST_REPORT.txt
npm run env:validate

# Commit your work
git add .env HARVEST_REPORT.txt
git commit -m "Harvest and consolidate all credentials

Found credentials from:
- [list locations]

All credentials now in master .env file.
Ready for all agents to use."

# Push your branch
git push origin cursor/credential-harvest-$(date +%Y%m%d)

# Update manifest
# Edit AGENT_MANIFEST.md to add:
# - Cursor's work
# - Status: Complete
# - Branch: cursor/credential-harvest-YYYYMMDD

git add AGENT_MANIFEST.md
git commit -m "Update manifest with credential harvest completion"
git push origin cursor/credential-harvest-$(date +%Y%m%d)
```

**After Cursor completes this, Cursor reports back with:**
- What credentials were found
- What's still missing
- Branch name (e.g., `cursor/credential-harvest-20251112`)

---

## Step 4: Merge Cursor's Work (You Run This)

Once Cursor completes credential harvesting:

```bash
cd /home/user/agents
git checkout develop
git fetch origin
git merge origin/cursor/credential-harvest-20251112 --no-edit
git push origin develop
```

**Now `develop` has:**
- ✅ Complete monorepo structure (from Claude)
- ✅ All harvested credentials (from Cursor)
- ✅ Ready for deployment work

---

## Step 5: All Agents Pull Latest

**For Claude (me):**
```bash
git fetch origin
git checkout develop
git pull origin develop
# Can now continue deployment with full .env
```

**For Cursor:**
```bash
git checkout develop
git pull origin develop
# Has complete consolidated structure
```

**For future agents (Codex, Gemini):**
```bash
git fetch origin
git checkout develop
git pull origin develop
# Ready to work
```

---

## 🎯 Ongoing Workflow

### When Any Agent Wants to Work

1. **Pull latest from develop:**
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create your branch:**
   ```bash
   # Claude
   git checkout -b claude/task-description-{sessionID}

   # Cursor
   git checkout -b cursor/task-description-$(date +%Y%m%d)

   # Others
   git checkout -b {agent}/task-description
   ```

3. **Do your work, read shared context:**
   - Check `AGENT_MANIFEST.md` - What exists
   - Check `.env` - Shared credentials
   - Check `MULTI_AGENT_WORKFLOW.md` - How we collaborate

4. **Update manifest with your work:**
   ```bash
   # Edit AGENT_MANIFEST.md
   # Add your task, status, branch name
   git add AGENT_MANIFEST.md
   git commit -m "Update manifest: Starting [task description]"
   ```

5. **Push your branch:**
   ```bash
   git push origin {agent}/{branch-name}
   ```

6. **When ready, request merge to develop**

### When Ready to Integrate

**You (or designated integrator) run:**
```bash
git checkout develop
git fetch origin
git merge origin/{agent}/{branch-name} --no-edit
git push origin develop
```

**Other agents pull the update:**
```bash
git checkout develop
git pull origin develop
```

---

## 📊 Branch Overview

After setup, GitHub will show:

```
main                  ← Original (stable releases)
develop               ← Integration branch (active development)
│
├─ claude/expo-factory-web-deployment-* ← Claude's consolidation
├─ claude/security-fixes-*              ← Claude's admin console work
├─ cursor/credential-harvest-*          ← Cursor's credential work
└─ [future agent branches]
```

**develop** contains merged work from all agents.

---

## ✅ Success Criteria

After completing all steps:

- [ ] `develop` branch exists on GitHub
- [ ] `develop` has monorepo structure (apps/, docs/, scripts/)
- [ ] `develop` has complete .env with all credentials
- [ ] AGENT_MANIFEST.md shows current status
- [ ] Cursor has completed credential harvest
- [ ] All agents can pull from `develop` and see complete structure

---

## 🔍 Verification Commands

**Check branch exists:**
```bash
git ls-remote origin | grep develop
# Should show: refs/heads/develop
```

**Check structure in develop:**
```bash
git checkout develop
ls -la apps/ docs/ scripts/ supabase/
cat AGENT_MANIFEST.md | grep -A5 "CONSOLIDATION"
```

**Check credentials:**
```bash
npm run env:validate
cat HARVEST_REPORT.txt  # After Cursor runs harvest
```

**Check agent branches:**
```bash
git branch -a | grep -E "claude/|cursor/"
```

---

## 🚀 What Happens Next

Once setup is complete:

1. **Claude continues deployment work**
   - Link to Supabase design-factory-admin
   - Deploy Factory backend to Railway
   - Deploy Factory frontend to Vercel

2. **Cursor can assist with:**
   - Local development setup
   - Testing deployment steps
   - Documentation updates

3. **All agents work from develop**
   - Single source of truth
   - Shared credentials
   - Clear coordination

---

## 📞 If Something Goes Wrong

### Merge conflict during Step 2
```bash
# Likely means develop has changes
git checkout develop
git pull origin develop
git merge origin/claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
# Resolve conflicts manually
git commit
git push origin develop
```

### Cursor can't find scripts
```bash
# Make sure you merged Claude's work first
git checkout develop
git pull origin develop
ls -la scripts/
# Should see: cursor-harvest-all-credentials.sh
```

### .env already has credentials
```bash
# Good! Cursor's harvest script will add to existing
# Creates backup before modifying
# Check: ls -la .env.backup.*
```

---

## 📝 Summary

**5 Steps:**
1. ✅ Create `develop` branch (you)
2. ✅ Merge Claude's consolidation → `develop` (you)
3. ✅ Cursor pulls `develop`, harvests credentials, pushes to `cursor/*` (Cursor)
4. ✅ Merge Cursor's work → `develop` (you)
5. ✅ All agents pull from `develop` (everyone)

**Result**:
- One integration branch (`develop`)
- Complete monorepo structure
- All credentials harvested
- All agents synchronized
- Ready for deployment

---

**Created**: 2025-11-12
**Model**: Branch-per-agent with integration branch
**Status**: Ready to execute
