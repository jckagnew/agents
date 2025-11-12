# CURSOR: Next Step - Merge Consolidation

**Status**: `develop` branch created ✅
**Next**: Merge Claude's consolidation work into `develop`

---

## 🚀 Run This One Command

```bash
bash scripts/cursor-merge-consolidation.sh
```

**That's it!** The script will:
1. Fetch Claude's consolidation branch
2. Merge it into `develop`
3. Push to `origin/develop`
4. Verify the structure

---

## What You'll Get

After running the script, `develop` will have:

```
agents/
├── apps/
│   ├── factory/              ✅ Factory code (moved from src/)
│   │   ├── src/
│   │   └── docs/
│   └── admin-console/        ✅ Admin console placeholder
│
├── docs/
│   └── deployment/           ✅ All deployment guides
│       ├── PHASE_1_DEPLOYMENT.md
│       ├── WEB_DEPLOYMENT.md
│       ├── INTEGRATION_ROADMAP.md
│       └── ...
│
├── scripts/                  ✅ Environment & credential scripts
│   ├── setup-env.sh
│   ├── validate-env.sh
│   ├── cursor-harvest-all-credentials.sh
│   └── ...
│
├── supabase/
│   └── config.toml          ✅ Links to design-factory-admin
│
├── .env                     ✅ Master credentials file
├── AGENT_MANIFEST.md        ✅ Work tracking
└── package.json             ✅ Updated paths
```

---

## After Merge: Harvest Credentials

Once the merge is complete:

```bash
# Run credential harvesting
bash scripts/cursor-harvest-all-credentials.sh

# Check what was found
cat HARVEST_REPORT.txt

# Validate
npm run env:validate
```

---

## Verification

After merge, check that structure exists:

```bash
ls -la apps/factory/
ls -la docs/deployment/
ls -la scripts/
cat AGENT_MANIFEST.md | head -20
```

Should see complete monorepo structure.

---

## If Script Fails

If the merge script fails with "branch not found":

```bash
# Manually fetch and merge
git fetch origin claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
git merge origin/claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP --no-edit
git push origin develop
```

---

## Timeline

1. ✅ **DONE**: Create `develop` branch
2. **NOW**: Run merge script (2 minutes)
3. **NEXT**: Harvest credentials (2 minutes)
4. **THEN**: Both agents work from `develop`

---

**TL;DR**: Run `bash scripts/cursor-merge-consolidation.sh` and you're done!
