# Quick Start: Multi-Agent Setup

## 🚀 TL;DR

### You (30 seconds):
```bash
cd /home/user/agents
git checkout -b develop main
git push origin develop
git merge origin/claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP --no-edit
git push origin develop
```

### Cursor (2 minutes):
```bash
git fetch origin
git checkout develop
git checkout -b cursor/harvest-$(date +%Y%m%d)
bash scripts/cursor-harvest-all-credentials.sh
git add .env HARVEST_REPORT.txt AGENT_MANIFEST.md
git commit -m "Harvest credentials"
git push origin cursor/harvest-$(date +%Y%m%d)
```

### You (30 seconds):
```bash
git checkout develop
git merge origin/cursor/harvest-20251112 --no-edit
git push origin develop
```

### Everyone (10 seconds):
```bash
git checkout develop
git pull origin develop
# Ready to work!
```

---

## 📋 Full Instructions
See: `SETUP_MULTI_AGENT.md`

## 🤝 Workflow Reference
See: `MULTI_AGENT_WORKFLOW.md`

## 📊 Current Status
See: `AGENT_MANIFEST.md`
