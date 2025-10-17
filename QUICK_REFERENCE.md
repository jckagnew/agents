# 🚀 Quick Reference - AI Safety Protocols

## ⚡ Before Every Session

1. **Read this reminder**: "Always show me exactly what you're about to do. Never assume anything. Always wait for my explicit approval."

2. **Check the safety protocols**: `AI_SAFETY_PROTOCOLS.md`

## 🛠️ Available Tools

### Git Hooks (Automatic)
- **Pre-commit**: Shows changes before committing
- **Pre-push**: Shows changes before pushing

### Safe Workflow Scripts
```bash
# Load safe aliases
source git-aliases.sh

# Safe operations
safe-commit -m "message"
safe-push origin branch-name
safe-status
safe-pr --title "Title" --body "Description"
```

### Manual Verification Commands
```bash
# Show current state
git status
git branch --show-current

# Show what would change
git diff --name-only HEAD~1 HEAD
git diff --stat HEAD~1 HEAD

# Show staged changes
git diff --cached --name-only
git diff --cached --stat
```

## 🚨 Emergency Stops

If I start acting without permission:
1. **Say "STOP"** - I will halt immediately
2. **Ask "What are you about to do?"** - I will explain
3. **Ask "Did you verify this?"** - I will show verification
4. **Ask "Do I have permission?"** - I will wait for approval

## ✅ Success Indicators

I'm following protocols when I:
- Show you exact commands before running them
- Display file changes before making them
- Wait for your explicit "yes" before proceeding
- Verify results match my claims
- Acknowledge when I'm uncertain

## ❌ Red Flags

Stop me if I:
- Act without showing you what I'm doing
- Make claims without verification
- Proceed without your explicit approval
- Assume anything about git state
- Create PRs without showing you the contents first

---

*Remember: Your credibility is at stake. Ed asked you to stop submitting PRs. I must verify everything.*
