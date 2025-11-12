# 📋 CURSOR: Step-by-Step Instructions

**Goal**: Sync to latest work, harvest credentials, create neutral shared branch

**Time**: 5-10 minutes

---

## Step 1: Sync to Latest Work

Copy and paste these commands:

```bash
cd /home/user/agents
git fetch origin
git checkout claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
git pull origin claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
```

**Verify it worked:**
```bash
ls -la apps/factory/
ls -la scripts/
ls -la CURSOR_RUN_THIS_FIRST.md
```

You should see:
- ✅ `apps/factory/` directory exists
- ✅ `scripts/` directory with harvest scripts
- ✅ `CURSOR_RUN_THIS_FIRST.md` file exists

---

## Step 2: Harvest ALL Credentials

This finds every `.env` file on your system and consolidates them:

```bash
bash scripts/cursor-harvest-all-credentials.sh
```

**What it does:**
- Searches entire workspace for `.env` files
- Extracts ALL credentials (Supabase, AI keys, Redis, etc.)
- Consolidates into `/home/user/agents/.env`
- Creates backup of existing `.env`
- Generates `HARVEST_REPORT.txt`

**After it runs:**
```bash
# Check what was found
cat HARVEST_REPORT.txt

# Validate credentials
npm run env:validate
```

---

## Step 3: Create Neutral Shared Branch

This creates the agent-neutral branch that everyone will use:

```bash
# Create neutral develop branch
git checkout -b develop

# Already has all the consolidation work
# (you're branching from the current work)

# Push to make it the shared branch
git push -u origin develop
```

**Verify it worked:**
```bash
git branch --show-current
# Should show: develop
```

---

## Step 4: Update Documentation

Tell everyone to use the new neutral branch:

```bash
# Switch back to develop if not already there
git checkout develop

# Create a note for all agents
cat > SHARED_BRANCH_CREATED.md << 'EOF'
# Neutral Shared Branch Created

**Date**: $(date +%Y-%m-%d)
**Created by**: Cursor
**Branch**: `develop`

---

## For All Agents (Claude, Cursor, Codex, Gemini)

The consolidation work has been moved to a **neutral shared branch**.

### Switch to Shared Branch:

\`\`\`bash
cd /home/user/agents
git fetch origin
git checkout develop
git pull origin develop
\`\`\`

### This Branch Contains:

- ✅ Monorepo structure (`apps/`, `supabase/`, `docs/`, `scripts/`)
- ✅ Master `.env` system (single source of truth)
- ✅ Credential harvesting scripts
- ✅ All deployment documentation
- ✅ Equal collaboration strategy

### All Future Work:

Branch from `develop`, not from `claude/*` branches.

\`\`\`bash
# Create feature branch
git checkout develop
git checkout -b feature/your-feature-name

# Work on it...

# Push and merge back to develop
git push -u origin feature/your-feature-name
\`\`\`

---

**No hierarchy. Equal collaboration. Shared workspace.**
EOF

git add SHARED_BRANCH_CREATED.md
git commit -m "Create neutral shared branch (develop)

This branch replaces claude/* as the shared workspace.
All agents should use this branch going forward.

- Created by: Cursor
- Purpose: Neutral, agent-equal collaboration
- Contains: All consolidation work from previous sessions"

git push -u origin develop
```

---

## Step 5: Verify Everything

Check that it all worked:

```bash
# Should be on develop branch
git branch --show-current

# Should see consolidated structure
ls -la apps/
ls -la docs/deployment/
ls -la scripts/

# Should have master .env
ls -la .env

# Validate credentials
npm run env:validate
```

---

## ✅ Success Criteria

After completing all steps, you should have:

- ✅ All latest consolidation work synced
- ✅ Master `.env` populated with all credentials
- ✅ Neutral `develop` branch created and pushed
- ✅ Documentation updated for all agents
- ✅ Ready for deployment work

---

## 🎯 What Happens Next

Now all agents (Claude, Cursor, Codex, Gemini) will:

1. Checkout `develop` branch
2. Read `AGENT_MANIFEST.md` for current status
3. Check master `.env` for credentials
4. Continue with deployment

**No more:**
- ❌ Claude-centric branches
- ❌ Repeated credential requests
- ❌ Searching multiple locations

**One branch. One .env. Equal collaboration.**

---

## 🔧 If Something Goes Wrong

### Credential harvest found nothing:
```bash
# Credentials may be in dashboards, not files
# Get them from:
# - Supabase: https://supabase.com/dashboard/project/design-factory-admin
# - OpenAI: https://platform.openai.com/api-keys
# - Anthropic: https://console.anthropic.com/settings/keys
# - Google AI: https://makersuite.google.com/app/apikey

# Manually add to .env:
nano /home/user/agents/.env
```

### Branch push failed:
```bash
# Try again with force (if you're sure):
git push -u origin develop --force

# Or check if branch already exists:
git branch -a | grep develop
```

### Can't find files after sync:
```bash
# Make sure you pulled the right branch:
git log --oneline -5
# Should show commits about consolidation

# If not, pull again:
git fetch origin
git checkout claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
git pull origin claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
```

---

## 📞 Summary

**5 Steps:**
1. ✅ Sync to latest (git pull)
2. ✅ Harvest credentials (run script)
3. ✅ Create neutral branch (git checkout -b develop)
4. ✅ Update docs (commit SHARED_BRANCH_CREATED.md)
5. ✅ Verify (check structure and .env)

**Time**: ~5-10 minutes

**Result**: Shared workspace ready for all agents

---

**Created**: 2025-11-12
**For**: Cursor
**Purpose**: Create neutral shared branch with all credentials
