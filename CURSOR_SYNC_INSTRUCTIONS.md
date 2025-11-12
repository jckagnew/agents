# 🔄 Cursor Sync Instructions

**Date**: 2025-11-12
**Issue**: Cursor's workspace doesn't have the monorepo structure yet
**Solution**: Pull latest changes from Claude's branch

---

## ✅ Monorepo Structure EXISTS on Branch

The monorepo consolidation **has been completed** and pushed to:

**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`

**Commits**:
- `3d114b1` - Add comprehensive update prompt for Cursor, Codex, and Gemini
- `d338c5e` - Implement master .env management system for monorepo
- `dfeea06` - Consolidate repository structure into unified monorepo layout ← **THE KEY COMMIT**
- `7aca7d0` - Create multi-agent collaboration system to prevent duplicate work
- `866def2` - Integrate with existing design-factory-admin Supabase project

---

## 🚀 CURSOR: Pull Latest Changes

### Step 1: Check Current Branch

```bash
cd /home/user/agents
git branch --show-current
```

**Expected**: Should show current branch name
**If different from** `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`, switch to it:

```bash
git fetch origin
git checkout claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
```

### Step 2: Pull Latest Changes

```bash
git pull origin claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
```

### Step 3: Verify Structure

```bash
# Should see apps/ directory
ls -la apps/

# Should see:
# apps/
#   ├── factory/
#   │   ├── src/
#   │   └── docs/
#   └── admin-console/
#       └── README.md
```

### Step 4: Verify Files Exist

```bash
# Check these files exist:
ls -la AGENT_MANIFEST.md
ls -la ENV_MANAGEMENT_STRATEGY.md
ls -la CURSOR_CODEX_GEMINI_UPDATE.md
ls -la scripts/setup-env.sh
ls -la scripts/validate-env.sh
```

---

## 📊 What You Should See After Pull

### Directory Structure

```
agents/
├── apps/                           ← NEW
│   ├── factory/                    ← Moved from src/
│   │   ├── src/
│   │   │   ├── api/server.ts
│   │   │   ├── screens/
│   │   │   └── services/
│   │   └── docs/
│   └── admin-console/              ← NEW (placeholder)
│       └── README.md
│
├── supabase/
│   ├── config.toml                 ← NEW (links to design-factory-admin)
│   ├── migrations/
│   └── functions/
│
├── docs/                           ← NEW
│   └── deployment/                 ← Deployment guides moved here
│       ├── PHASE_1_DEPLOYMENT.md
│       ├── WEB_DEPLOYMENT.md
│       ├── INTEGRATION_ROADMAP.md
│       ├── EXISTING_INFRASTRUCTURE_INTEGRATION.md
│       └── REPOSITORY_CONSOLIDATION_PLAN.md
│
├── scripts/                        ← NEW
│   ├── setup-env.sh               ← Environment setup
│   └── validate-env.sh            ← Environment validation
│
├── AGENT_MANIFEST.md              ← UPDATED (consolidated structure)
├── ENV_MANAGEMENT_STRATEGY.md     ← NEW (env management guide)
├── CURSOR_CODEX_GEMINI_UPDATE.md  ← NEW (update prompt)
├── .env                            ← NEW (created from template)
├── .env.example                    ← UPDATED (master template)
├── README.md                       ← UPDATED (env config section)
└── package.json                    ← UPDATED (new paths, new scripts)
```

### Updated package.json Scripts

After pulling, you should see:

```json
{
  "scripts": {
    "api": "ts-node apps/factory/src/api/server.ts",          // ← Updated path
    "api:dev": "nodemon --exec ts-node apps/factory/src/api/server.ts",
    "env:setup": "bash scripts/setup-env.sh",                  // ← NEW
    "env:validate": "bash scripts/validate-env.sh",            // ← NEW
    "predev": "npm run env:validate"                           // ← NEW
  }
}
```

---

## 🔍 Troubleshooting

### Issue: "apps/ directory not found"

**Cause**: Haven't pulled latest changes
**Solution**:
```bash
git fetch origin
git pull origin claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
```

### Issue: "AGENT_MANIFEST.md not found"

**Cause**: On wrong branch or haven't pulled
**Solution**:
```bash
git checkout claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
git pull origin claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
```

### Issue: "Still see src/ directory"

**Cause**: Git hasn't updated working directory
**Solution**:
```bash
# Verify you're on correct branch
git branch --show-current

# Hard reset to remote state (CAUTION: loses uncommitted changes)
git fetch origin
git reset --hard origin/claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
```

### Issue: "package.json has old paths"

**Cause**: Need to pull latest changes
**Solution**: Pull and verify package.json shows `apps/factory/src/api/server.ts`

---

## ✅ Verification Checklist

After pulling, verify these changes exist:

- [ ] `apps/factory/` directory exists
- [ ] `apps/factory/src/api/server.ts` exists
- [ ] `apps/admin-console/README.md` exists
- [ ] `supabase/config.toml` exists
- [ ] `docs/deployment/` directory exists
- [ ] `scripts/setup-env.sh` exists (executable)
- [ ] `scripts/validate-env.sh` exists (executable)
- [ ] `AGENT_MANIFEST.md` has "CONSOLIDATION MILESTONE" in header
- [ ] `ENV_MANAGEMENT_STRATEGY.md` exists
- [ ] `CURSOR_CODEX_GEMINI_UPDATE.md` exists
- [ ] `.env` file exists (created from template)
- [ ] `package.json` has `"api": "ts-node apps/factory/src/api/server.ts"`
- [ ] `package.json` has `"env:setup"` and `"env:validate"` scripts
- [ ] No `src/` directory at root (moved to `apps/factory/`)

---

## 🎯 Quick Verification Command

Run this to check everything:

```bash
cd /home/user/agents

echo "Branch: $(git branch --show-current)"
echo "Latest commit: $(git log -1 --oneline)"
echo ""
echo "Structure check:"
[ -d "apps/factory" ] && echo "✅ apps/factory exists" || echo "❌ apps/factory missing"
[ -d "apps/admin-console" ] && echo "✅ apps/admin-console exists" || echo "❌ apps/admin-console missing"
[ -d "docs/deployment" ] && echo "✅ docs/deployment exists" || echo "❌ docs/deployment missing"
[ -d "scripts" ] && echo "✅ scripts exists" || echo "❌ scripts missing"
[ -f "supabase/config.toml" ] && echo "✅ supabase/config.toml exists" || echo "❌ supabase/config.toml missing"
[ -f "AGENT_MANIFEST.md" ] && echo "✅ AGENT_MANIFEST.md exists" || echo "❌ AGENT_MANIFEST.md missing"
[ -f "ENV_MANAGEMENT_STRATEGY.md" ] && echo "✅ ENV_MANAGEMENT_STRATEGY.md exists" || echo "❌ ENV_MANAGEMENT_STRATEGY.md missing"
[ -f ".env" ] && echo "✅ .env exists" || echo "❌ .env missing"
echo ""
echo "package.json check:"
grep -q "apps/factory/src/api/server.ts" package.json && echo "✅ package.json has new paths" || echo "❌ package.json has old paths"
grep -q "env:setup" package.json && echo "✅ package.json has env scripts" || echo "❌ package.json missing env scripts"
```

---

## 📚 After Sync: Read These Files

Once you've pulled and verified, read in this order:

1. **AGENT_MANIFEST.md** - What exists, what's in progress
2. **ENV_MANAGEMENT_STRATEGY.md** - How environment variables work
3. **CURSOR_CODEX_GEMINI_UPDATE.md** - Summary of all changes
4. **docs/deployment/PHASE_1_DEPLOYMENT.md** - Next deployment steps

---

## 🚀 After Verification: Next Steps

Once you've confirmed the structure exists:

```bash
# 1. Validate environment
npm run env:validate

# 2. If .env needs credentials, setup:
npm run env:setup
# Edit .env and add credentials

# 3. Ready to continue deployment!
```

---

## 💡 Summary for Cursor

**The monorepo structure IS COMPLETE** on branch `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`.

**You need to**:
1. Checkout the correct branch
2. Pull latest changes (3 commits with consolidation)
3. Verify structure with checklist above
4. Read AGENT_MANIFEST.md and ENV_MANAGEMENT_STRATEGY.md
5. Continue with deployment

**All files exist. You just need to sync your workspace.**

---

**Last Updated**: 2025-11-12
**Branch**: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`
**Status**: ✅ Monorepo consolidation complete and pushed
