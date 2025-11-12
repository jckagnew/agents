# Programmatic Solutions to Create Develop Branch

**Problem**: Different git proxies prevent direct branch sharing between agents.

**Solution**: Programmatically create the `develop` branch using GitHub API or web interface.

---

## ✅ Option 1: GitHub API (Fully Automated)

**Requirements**: GitHub Personal Access Token

### Step 1: Get GitHub Token

1. Go to: https://github.com/settings/tokens/new
2. Token name: `agents-repo-access`
3. Expiration: 30 days (or your preference)
4. Scopes: Check `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token** (you'll only see it once!)

### Step 2: Run the Script

```bash
# Set the token (replace with your actual token)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Run the automation script
bash scripts/create-develop-branch.sh
```

**What it does**:
- Uses GitHub API to create `develop` branch
- Points it to commit `e8fb583` (all consolidation work)
- Works instantly
- Both Cursor and Claude can pull from it

**Output**:
```
✅ SUCCESS: Branch 'develop' created!
🎉 The develop branch now exists on GitHub with all consolidation work!
```

---

## ✅ Option 2: GitHub Web Interface (30 seconds)

**No token required**

### Steps:

1. Go to: https://github.com/jckagnew/agents

2. Click the **branch dropdown** (currently shows "main")

3. In the text box, type: `develop`

4. You'll see: **"Create branch: develop from claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP"**

5. Click it

6. Done! ✅

**Result**: `develop` branch now exists with all consolidation work

---

## ✅ Option 3: GitHub CLI (If Installed)

```bash
# Login to GitHub CLI
gh auth login

# Create branch
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/jckagnew/agents/git/refs \
  -f ref='refs/heads/develop' \
  -f sha='e8fb583cb6449859998de5c31d4f9405806927d1'
```

---

## ✅ Option 4: Bookmarklet (One-Click)

Create a bookmark with this JavaScript:

```javascript
javascript:(function(){const url='https://api.github.com/repos/jckagnew/agents/git/refs';const data={ref:'refs/heads/develop',sha:'e8fb583cb6449859998de5c31d4f9405806927d1'};const token=prompt('Enter GitHub token:');fetch(url,{method:'POST',headers:{'Authorization':`Bearer ${token}`,'Content-Type':'application/json'},body:JSON.stringify(data)}).then(r=>r.json()).then(d=>alert(d.ref?'✅ Created!':'❌ Failed: '+JSON.stringify(d)))})();
```

Visit GitHub, click the bookmark, enter your token, done!

---

## After Branch Creation

**Both agents can now pull from develop:**

### Cursor:
```bash
cd /home/user/agents
git fetch origin
git checkout develop
git pull origin develop

# Verify structure
ls -la apps/factory/
ls -la docs/deployment/
ls -la scripts/
```

### Claude:
```bash
git fetch origin
git checkout develop
git pull origin develop

# Continue deployment work
npm run env:validate
```

---

## Why This Works

**The develop branch now exists on GitHub** with all consolidation work:
- ✅ Monorepo structure (`apps/`, `docs/`, `scripts/`)
- ✅ Master `.env` system
- ✅ Credential harvesting scripts
- ✅ All documentation
- ✅ Supabase integration

**Both agents can see it** because:
- It's on the real GitHub (not just a proxy)
- Both proxies can read from GitHub
- `develop` is a neutral name (no restrictions)

---

## Verification

After creating the branch, verify it exists:

```bash
# Check on GitHub
https://github.com/jckagnew/agents/tree/develop

# Or via command line
git ls-remote origin develop
# Should show: e8fb583cb6449859998de5c31d4f9405806927d1 refs/heads/develop
```

---

## Troubleshooting

### "401 Unauthorized"
- Token is invalid or expired
- Regenerate token at: https://github.com/settings/tokens

### "404 Not Found"
- Token doesn't have `repo` scope
- Recreate token with proper permissions

### "422 Unprocessable Entity"
- Branch already exists
- Script will update it instead of creating new

---

## Recommended Approach

**Option 2 (Web Interface)** is easiest:
- ✅ No tokens needed
- ✅ 30 seconds
- ✅ Visual confirmation
- ✅ Hard to mess up

**Option 1 (API Script)** if you prefer automation:
- ✅ Fully programmatic
- ✅ Repeatable
- ✅ Can be integrated into workflows

---

**Choose one and run it!** Once `develop` exists, both agents can finally work together.

**Last Updated**: 2025-11-12
**Commit**: e8fb583
**Status**: Ready to create branch
