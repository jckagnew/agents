# GitHub Private Repository Setup

## Quick Setup Instructions

### 1. Create Private Repository on GitHub

1. Go to https://github.com/new
2. **Repository name:** `design-first-software-factory`
3. **Description:** "A sophisticated, auditable, and user-centric workflow for design-first code generation"
4. **Visibility:** ⚠️ **Private** (This is proprietary IP)
5. **Initialize:** Leave unchecked (we already have files)
6. Click "Create repository"

### 2. Connect Your Local Repository

```bash
cd /home/user/agents/design-first-software-factory

# Add GitHub remote
git remote add origin git@github.com:jckagnew/design-first-software-factory.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 3. Verify Repository

```bash
# Check remote configuration
git remote -v

# Expected output:
# origin  git@github.com:jckagnew/design-first-software-factory.git (fetch)
# origin  git@github.com:jckagnew/design-first-software-factory.git (push)
```

### 4. Repository Settings Recommendations

#### Branch Protection (Settings → Branches)
- [ ] Require pull request reviews before merging
- [ ] Require status checks to pass before merging
- [ ] Require conversation resolution before merging
- [ ] Do not allow bypassing the above settings

#### Secrets Management (Settings → Secrets and variables → Actions)
Add these secrets for CI/CD:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `GEMINI_API_KEY`
- `STITCH_API_KEY`
- `FIGMA_API_TOKEN`

#### Collaborators (Settings → Collaborators and teams)
Add your AI agents as collaborators (if applicable):
- Gemini (orchestrator)
- Codex (backend specialist)
- Cursor (frontend specialist)

### 5. Daily Workflow

```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, then:
git add .
git commit -m "Descriptive commit message"
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# After review and approval, merge to main
```

### 6. Sync with Local Machine (if working outside agents/)

If you also have the project at `/Users/jackagnew/projects/design-first-software-factory/`:

```bash
# In your local directory
cd /Users/jackagnew/projects/design-first-software-factory

# Add same remote
git remote add origin git@github.com:jckagnew/design-first-software-factory.git

# Pull from GitHub
git pull origin main

# Now both locations are synced via GitHub
```

---

## Alternative: Work Directly in This Workspace

If Claude Code maps to your local filesystem, you can work directly in:
```
/home/user/agents/design-first-software-factory/
```

And push changes to GitHub from here.

---

## Troubleshooting

### SSH Key Not Configured

If you get "Permission denied (publickey)":

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

### HTTPS Instead of SSH

If you prefer HTTPS:

```bash
git remote set-url origin https://github.com/jckagnew/design-first-software-factory.git
```

---

**Ready to collaborate!** 🚀
