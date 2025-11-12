# Environment Variable Management Strategy
**Monorepo Best Practices for Shared Credentials**

**Date**: 2025-11-12
**Problem**: Repeated requests for same credentials across projects
**Solution**: Single master `.env` with inheritance

---

## 🎯 The Problem

**Current inefficiency**:
- Factory needs Supabase credentials
- Admin Console needs THE SAME Supabase credentials
- Both need to be configured separately
- AI agents keep asking for the same keys repeatedly
- Risk of credentials getting out of sync

**Example of redundancy**:
```bash
# In Factory .env
SUPABASE_URL=https://design-factory-admin.supabase.co
SUPABASE_ANON_KEY=eyJhb...

# In Admin Console .env (DUPLICATE!)
SUPABASE_URL=https://design-factory-admin.supabase.co  # Same!
SUPABASE_ANON_KEY=eyJhb...                              # Same!
```

---

## ✅ The Solution: Single Master .env

### File Structure

```
agents/
├── .env                           ◄── MASTER - All shared credentials
├── .env.example                   ◄── Template for master .env
├── .env.local                     ◄── Local overrides (gitignored)
│
├── apps/
│   ├── factory/
│   │   └── .env.app              ◄── App-specific only (optional)
│   │
│   └── admin-console/
│       └── .env.app              ◄── App-specific only (optional)
│
└── scripts/
    └── setup-env.sh              ◄── Helper script to copy .env.example → .env
```

### What Goes Where

**Root `.env` (MASTER - 95% of credentials)**:
```bash
# ===================================================================
# MASTER ENVIRONMENT CONFIGURATION
# All projects inherit from this file
# ===================================================================

# === SHARED SUPABASE (Both Factory and Admin Console) ===
SUPABASE_URL=https://design-factory-admin.supabase.co
EXPO_PUBLIC_SUPABASE_URL=https://design-factory-admin.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# === SHARED REDIS (Factory uses directly, Admin Console may monitor) ===
REDIS_URL=redis://localhost:6379

# === SHARED AI SERVICES (Factory uses, Admin Console may display status) ===
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_AI_API_KEY=AIza-your-key-here

# === STRIPE (Shared payment processing) ===
STRIPE_SECRET_KEY=sk_test_your-key-here
STRIPE_WEBHOOK_SECRET=whsec_your-secret-here

# === FACTORY API (Admin Console needs this after Factory deploys) ===
EXPO_PUBLIC_FACTORY_API_URL=http://localhost:3000
EXPO_PUBLIC_FACTORY_WS_URL=ws://localhost:3000

# Production (update after deployment)
# EXPO_PUBLIC_FACTORY_API_URL=https://factory-api.up.railway.app
# EXPO_PUBLIC_FACTORY_WS_URL=wss://factory-api.up.railway.app

# === ENVIRONMENT ===
NODE_ENV=development
```

**App-specific `.env.app` (OPTIONAL - Only unique overrides)**:
```bash
# apps/factory/.env.app
# Only Factory-specific variables that Admin Console doesn't need
BULL_CONCURRENCY=5
JOB_RETRY_ATTEMPTS=3

# apps/admin-console/.env.app
# Only Admin Console-specific variables
ADMIN_SESSION_TIMEOUT=3600
```

---

## 🔧 Technical Implementation

### Option 1: Root .env with Dotenv (RECOMMENDED)

**For Express Backend (Factory)**:
```typescript
// apps/factory/src/api/server.ts
import dotenv from 'dotenv';
import path from 'path';

// Load from ROOT .env
dotenv.config({ path: path.resolve(__dirname, '../../../.env') });

// Optional: Load app-specific overrides
dotenv.config({ path: path.resolve(__dirname, '../.env.app') });

// Now use process.env.SUPABASE_URL, etc.
```

**For Expo Apps (Factory & Admin Console)**:
```typescript
// Expo automatically loads .env files from project root
// Just ensure your .env is in /home/user/agents/.env

// Access in code:
const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL;
```

**Update package.json scripts**:
```json
{
  "scripts": {
    "api": "node -r dotenv/config apps/factory/src/api/server.ts dotenv_config_path=.env",
    "api:dev": "nodemon -r dotenv/config --exec ts-node apps/factory/src/api/server.ts dotenv_config_path=.env"
  }
}
```

### Option 2: Environment Variable Loader Script

**Create `scripts/load-env.ts`**:
```typescript
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';

export function loadMonorepoEnv() {
  const rootEnvPath = path.resolve(__dirname, '../.env');
  const appEnvPath = path.resolve(process.cwd(), '.env.app');

  // Load root .env (master)
  if (fs.existsSync(rootEnvPath)) {
    dotenv.config({ path: rootEnvPath });
    console.log('✅ Loaded master .env from root');
  } else {
    console.warn('⚠️  No .env found at root - using defaults');
  }

  // Load app-specific overrides
  if (fs.existsSync(appEnvPath)) {
    dotenv.config({ path: appEnvPath, override: true });
    console.log('✅ Loaded app-specific .env.app');
  }
}
```

**Use in each app**:
```typescript
// apps/factory/src/api/server.ts
import { loadMonorepoEnv } from '../../../scripts/load-env';
loadMonorepoEnv();

// Now all env vars are loaded
```

---

## 📋 Setup Instructions for AI Agents

### First Time Setup

**Step 1: Copy template to master .env**
```bash
cd /home/user/agents
cp .env.example .env
```

**Step 2: Fill in credentials ONCE**
```bash
# Edit .env and add real credentials
nano .env

# Or use helper script (if we create it)
./scripts/setup-env.sh
```

**Step 3: All apps automatically inherit**
```bash
# No need to create separate .env files!
# Both Factory and Admin Console read from root .env
```

### When AI Agent Starts New Task

**Instead of asking for credentials, agent should**:
```bash
# 1. Check if .env exists
if [ -f .env ]; then
  echo "✅ Master .env found - credentials available"
else
  echo "⚠️  No .env found - copying from .env.example"
  cp .env.example .env
  echo "📝 Please fill in credentials in root .env file"
fi
```

---

## 🔐 Security Best Practices

### Gitignore Configuration

**Root `.gitignore`**:
```gitignore
# Environment files (DO NOT COMMIT)
.env
.env.local
.env.production
.env.*.local

# But DO commit templates
!.env.example
!.env.production.template

# App-specific env (if used)
apps/*/.env.app
```

### Credential Hierarchy

**Priority order (lowest to highest)**:
1. `.env.example` (template with placeholder values)
2. `.env` (root master with real credentials)
3. `.env.local` (local developer overrides)
4. `.env.app` (app-specific overrides)
5. Environment variables from hosting platform (Railway, Vercel)

---

## 🚀 Deployment Considerations

### Local Development
- Use root `.env` with local values
- All developers share same `.env.example` template
- Each developer has their own `.env` (gitignored)

### Production Deployment

**Railway (Backend)**:
```bash
# Set environment variables in Railway dashboard
# OR use Railway CLI to sync from .env
railway variables --set-from-env .env
```

**Vercel (Frontend)**:
```bash
# Set environment variables in Vercel dashboard
# OR use Vercel CLI to sync from .env
vercel env pull .env.production
```

**Expo EAS (Mobile)**:
```bash
# Use eas.json to reference environment variables
# Can read from .env automatically
eas build --profile production
```

---

## 📊 Benefits of This Approach

**✅ No Duplicate Credentials**:
- Enter Supabase URL once, used everywhere
- Single source of truth for all API keys

**✅ Easier for AI Agents**:
- Agent checks ONE file for credentials
- No repeated questions about same keys
- Clear template to follow

**✅ Consistent Across Projects**:
- Factory and Admin Console always in sync
- No risk of using wrong credentials

**✅ Simple Onboarding**:
- New developer: `cp .env.example .env` → fill in keys → done
- Works for all apps immediately

**✅ Secure by Default**:
- Root `.env` is gitignored
- Production secrets stay in hosting platform
- Local development isolated from production

---

## 🔄 Migration from Current Setup

### Step 1: Consolidate Existing .env Files

```bash
# If you have separate .env files in apps/factory/ and apps/admin-console/
# Merge them into root .env

cd /home/user/agents

# Backup existing
cp apps/factory/.env apps/factory/.env.backup 2>/dev/null || true
cp apps/admin-console/.env apps/admin-console/.env.backup 2>/dev/null || true

# Merge into root (manual review recommended)
cat apps/factory/.env >> .env 2>/dev/null || true
cat apps/admin-console/.env >> .env 2>/dev/null || true

# Remove duplicates (manual cleanup)
sort .env | uniq > .env.tmp && mv .env.tmp .env
```

### Step 2: Update Code to Load from Root

See "Technical Implementation" section above.

### Step 3: Remove Old App-Specific .env Files

```bash
# After verifying root .env works
rm apps/factory/.env 2>/dev/null || true
rm apps/admin-console/.env 2>/dev/null || true
```

---

## 📝 Template for .env.example

Updated root `.env.example` should include:
- ✅ All shared credentials (Supabase, AI services, Redis, Stripe)
- ✅ Comments indicating which apps use which variables
- ✅ Clear setup instructions
- ✅ Links to where to get each credential

---

## 🎯 For AI Agents: Quick Reference

**Before asking user for credentials**:
```bash
# 1. Check if root .env exists
if [ -f /home/user/agents/.env ]; then
  echo "✅ Credentials available in root .env"
  source /home/user/agents/.env
  # Use credentials
else
  echo "❌ No .env found"
  echo "📋 Please create .env from template:"
  echo "   cp .env.example .env"
  echo "   # Then fill in credentials"
fi
```

**When user provides credentials**:
```bash
# Add to ROOT .env, not app-specific .env
echo "SUPABASE_URL=$value" >> /home/user/agents/.env
```

**When checking environment setup**:
```bash
# Validate root .env has all required keys
required_keys=("SUPABASE_URL" "SUPABASE_ANON_KEY" "REDIS_URL")
for key in "${required_keys[@]}"; do
  if ! grep -q "^$key=" .env; then
    echo "❌ Missing required key: $key"
  fi
done
```

---

## 🔗 Related Documentation

- `.env.example` - Template with all variables
- `REPOSITORY_CONSOLIDATION_PLAN.md` - Monorepo structure
- `PHASE_1_DEPLOYMENT.md` - Deployment guide references .env
- `EXISTING_INFRASTRUCTURE_INTEGRATION.md` - Supabase credentials

---

**Last Updated**: 2025-11-12
**Status**: ✅ Strategy Defined - Ready for Implementation
