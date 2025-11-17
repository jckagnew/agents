# 🔄 Repository Separation Plan

## Current Situation

### Repository: `jckagnew-agents` (GitHub: `jckagnew/agents`)

**Location**: `/Users/jackagnew/projects/jckagnew-agents`

**Contains**:
- ✅ Course Materials (Ed Donner's course):
  - `1_foundations/`
  - `2_openai/`
  - `3_crew/`
  - `4_langgraph/`
  - `5_autogen/`
  - `6_mcp/`
  
- ✅ Business Systems (Your actual business):
  - `apps/factory/` - Software Factory backend
  - `apps/admin-console/` - Admin Console
  - `supabase/` - Database and Edge Functions
  - `.github/workflows/` - Multi-agent PR reviews, market research
  - `scripts/run_research.js` - Market research automation
  - `AGENT_HANDOFF_SUMMARY.md` - Business documentation
  - `CLAUDE_ACCESS_OPTIONS.md` - Business access guide

### Repository: `agents` (Ed Donner's original course)

**Location**: `/Users/jackagnew/projects/agents`

**Contains**: 
- Course materials only
- Upstream: `ed-donner/agents`
- Origin: `jckagnew/agents` (your fork)

---

## The Problem

**Business-specific files** (PR reviews, market research, Supabase integration) are mixed with **course materials** in `jckagnew-agents`.

**Security Concern**: 
- Supabase project ID exposed: `mamfaakxnfczmcbmqtgg`
- Business architecture details in course repo

---

## Decision Required

### Option A: Separate Business Repository (Recommended)

**Create a new repository** for business systems only:

```
Repository Name: [USER TO PROVIDE]
GitHub URL: [USER TO PROVIDE]
Local Path: [USER TO PROVIDE]
```

**Move these files**:
- `apps/` (entire directory)
- `supabase/` (entire directory)
- `.github/workflows/multi_agent_review.yml`
- `.github/workflows/market_research.yml`
- `.github/workflows/market_research_interactive.yml`
- `scripts/run_research.js`
- `scripts/market_config.json`
- `AGENT_HANDOFF_SUMMARY.md`
- `CLAUDE_ACCESS_OPTIONS.md`
- All other business-specific documentation

**Keep in course repo**:
- Course materials (`1_foundations/`, `2_openai/`, etc.)
- Generic guides (if any)

---

### Option B: Keep Mixed, But Organize

**Keep everything in `jckagnew-agents`** but clearly separate:

```
jckagnew-agents/
├── course/              # All course materials
│   ├── 1_foundations/
│   ├── 2_openai/
│   └── ...
├── business/            # All business systems
│   ├── apps/
│   ├── supabase/
│   └── ...
└── README.md            # Explains structure
```

**Pros**: No migration needed
**Cons**: Still mixed, harder to maintain separation

---

### Option C: Remove Course Materials

**Remove course materials** from `jckagnew-agents`, keep only business:

- Delete: `1_foundations/`, `2_openai/`, `3_crew/`, `4_langgraph/`, `5_autogen/`, `6_mcp/`
- Keep: All business systems

**Pros**: Clean business repo
**Cons**: Lose course materials (but they're in `/Users/jackagnew/projects/agents`)

---

## Files to Move (If Option A)

### Business-Specific Files:

1. **Documentation**:
   - `AGENT_HANDOFF_SUMMARY.md`
   - `CLAUDE_ACCESS_OPTIONS.md`
   - `DEPLOYMENT_STATUS.md`
   - `GITHUB_SECRETS_SETUP.md`
   - `MARKET_RESEARCH_STORAGE.md`
   - All other business docs

2. **Code**:
   - `apps/` (entire directory)
   - `supabase/` (entire directory)
   - `scripts/run_research.js`
   - `scripts/market_config.json`
   - `scripts/deploy-security-fixes.sh`

3. **Workflows**:
   - `.github/workflows/multi_agent_review.yml`
   - `.github/workflows/market_research.yml`
   - `.github/workflows/market_research_interactive.yml`

4. **Configuration**:
   - `.env.example` (business-specific)
   - `package.json` (if business-specific)
   - `tsconfig.json` (if business-specific)

### Files to Keep in Course Repo:

- `1_foundations/`
- `2_openai/`
- `3_crew/`
- `4_langgraph/`
- `5_autogen/`
- `6_mcp/`
- Course-specific READMEs

---

## Security Fixes Needed

Once files are moved to business repo:

1. **Redact Supabase Project ID** in `AGENT_HANDOFF_SUMMARY.md`:
   ```diff
   - View database: https://supabase.com/dashboard/project/mamfaakxnfczmcbmqtgg
   + View database: Check SUPABASE_URL environment variable
   ```

2. **Update Repository References**:
   ```diff
   - **Repository**: `jckagnew/agents`
   + **Repository**: `jckagnew/[NEW_BUSINESS_REPO]`
   ```

3. **Verify No API Keys** in git history:
   ```bash
   git log --all --full-history --source -- .env
   ```

---

## Action Plan (After User Decision)

### If Option A (Separate Repo):

1. User provides business repository location
2. Create business repo structure
3. Copy business files to new repo
4. Update all file references
5. Commit and push to business repo
6. Remove business files from `jckagnew-agents`
7. Clean up course repo

### If Option B (Organize):

1. Create `course/` and `business/` directories
2. Move files to appropriate directories
3. Update all paths in code/docs
4. Update README

### If Option C (Remove Course):

1. Delete course material directories
2. Update README
3. Clean up references

---

## Questions for User

1. **What is the correct business repository?**
   - Name: `[?]`
   - GitHub URL: `[?]`
   - Local path: `[?]`

2. **Which option do you prefer?**
   - [ ] Option A: Separate business repository
   - [ ] Option B: Keep mixed, but organize
   - [ ] Option C: Remove course materials

3. **On Linux machine (`/home/user/agents/`):**
   - Is this the course repo or business repo?
   - Should we sync separation there too?

---

**Status**: ⏳ Waiting for user decision on repository structure

**Priority**: 🔥 URGENT - Business files mixed with course materials

