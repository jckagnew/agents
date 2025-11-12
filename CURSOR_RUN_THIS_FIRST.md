# 🎯 CURSOR: RUN THIS FIRST

**Purpose**: Consolidate ALL credentials from anywhere on your system into the master `.env` file.

---

## 🚀 Quick Start

```bash
cd /home/user/agents
bash scripts/cursor-harvest-all-credentials.sh
```

**That's it!** The script will:
1. Search your entire workspace for ANY `.env` files
2. Extract ALL credentials (not just the ones we think we need)
3. Consolidate into `/home/user/agents/.env`
4. Create backup of existing `.env`
5. Generate report of what was found

---

## 📊 What It Does

### Searches For:
- `.env` files
- `.env.local`, `.env.production`, etc.
- `secrets.*` files
- `config.env` files
- ANY file with credentials

### Extracts:
- **ALL** key-value pairs (not just known ones)
- Supabase keys
- AI API keys (OpenAI, Anthropic, Google)
- Redis URLs
- Stripe keys
- Database credentials
- **Everything else it finds**

### Safely Handles:
- ✅ Creates backup before modifying
- ✅ Skips placeholder values (`your-key-here`)
- ✅ Deduplicates (keeps most recent)
- ✅ Generates report of changes

---

## 🔍 After Running

Check the results:

```bash
# View master .env
cat /home/user/agents/.env

# Read harvest report
cat /home/user/agents/HARVEST_REPORT.txt

# Validate credentials
npm run env:validate
```

---

## 📋 Expected Output

```
🔍 COMPREHENSIVE CREDENTIAL HARVESTING
=======================================

Found X .env file(s)

📄 Processing: /home/user/some-project/.env
  ✅ Added: SUPABASE_ANON_KEY
  ✅ Added: OPENAI_API_KEY
  ...

📊 Consolidation Summary
Total credentials found: 25
New credentials added: 15
Existing credentials updated: 3
Placeholder values skipped: 7

✅ HARVEST COMPLETE!
```

---

## 🔒 Security

- ✅ `.env` is gitignored (never committed)
- ✅ Creates timestamped backup
- ✅ Report shows key names only (no values)
- ✅ Safe to commit: `HARVEST_REPORT.txt`

---

## 🤝 Benefits for All Agents

Once you run this, the master `.env` becomes the **single source of truth**:

- ✅ Claude checks: `/home/user/agents/.env`
- ✅ Cursor checks: `/home/user/agents/.env`
- ✅ Codex checks: `/home/user/agents/.env`
- ✅ Gemini checks: `/home/user/agents/.env`

**No more:**
- ❌ "What's your Supabase key?" (it's in the master .env)
- ❌ "What's your OpenAI key?" (it's in the master .env)
- ❌ Searching multiple locations
- ❌ Duplicate credentials

---

## 🎯 After This Script Succeeds

You'll have a **complete master `.env`** with:
- All Supabase credentials
- All AI API keys
- All database credentials
- All service URLs
- **Everything found on your system**

Then all agents can:
```bash
npm run env:validate  # Check what's configured
npm run api:dev       # Run Factory backend (auto-loads .env)
npm run start         # Run Frontend (auto-loads .env)
```

**One file. One source of truth. All agents synchronized.**

---

## 🔧 Troubleshooting

**Script says "No .env files found"**
- You may not have any other projects with .env files
- The master .env.example will be used as the base
- You'll need to get credentials from service dashboards

**Script found credentials but they're old**
- Manual review needed: `nano /home/user/agents/.env`
- Get fresh credentials from service dashboards
- Run `npm run env:validate` to check what's needed

**Want to see what was found?**
```bash
cat /home/user/agents/HARVEST_REPORT.txt
```

---

## ⚡ TL;DR

```bash
# Run this ONE command:
bash /home/user/agents/scripts/cursor-harvest-all-credentials.sh

# Then all agents have access to ALL credentials
npm run env:validate
```

**This solves the "repeated credential requests" problem permanently.**

---

**Created**: 2025-11-12
**For**: Cursor (and any agent that finds credentials first)
**Purpose**: Create single source of truth for ALL credentials
