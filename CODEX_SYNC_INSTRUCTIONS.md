# Codex Sync Instructions

**Issue**: Codex is seeing different commits (`45d2307`, `abd63f3`, `6f5fe15`) than what exists in the repository.

**Root Cause**: Codex may be in a different repository directory or needs to pull latest changes.

## Verification Steps for Codex

1. **Check Current Directory**:
   ```bash
   pwd
   # Should be: /Users/jackagnew/projects/jckagnew-agents
   ```

2. **Check Current Branch**:
   ```bash
   git branch --show-current
   # Should be: develop
   ```

3. **Check Remote URL**:
   ```bash
   git remote get-url origin
   # Should be: https://github.com/jckagnew/agents.git
   ```

4. **Pull Latest Changes**:
   ```bash
   git fetch origin
   git checkout develop
   git pull origin develop
   ```

5. **Verify Commits Exist**:
   ```bash
   git log --oneline -n 5
   # Should show:
   # 701b52d Add comprehensive summary of all critical fixes completed
   # 7244f44 CRITICAL: Fix race conditions, promise rejections, and add retry logic
   # 6aa3200 Add comprehensive code review summaries for Cursor and Gemini
   ```

6. **Verify Files Exist**:
   ```bash
   ls -la CODE_REVIEW_FIXES_COMPLETE.md
   ls -la apps/factory/src/utils/retry.ts
   ls -la supabase/migrations/008_atomic_quota_updates.sql
   ```

## If Commits Still Don't Exist

If Codex still sees `45d2307`, `abd63f3`, `6f5fe15` after pulling:

1. **Check if in Different Repository**:
   ```bash
   git remote -v
   # Verify it's pointing to the correct repository
   ```

2. **Check All Branches**:
   ```bash
   git branch -a
   # Verify develop branch exists
   ```

3. **Force Sync**:
   ```bash
   git fetch origin --prune
   git reset --hard origin/develop
   ```

## Current Repository State (From Cursor)

**Repository**: `/Users/jackagnew/projects/jckagnew-agents`  
**Branch**: `develop`  
**Remote**: `https://github.com/jckagnew/agents.git`  
**Latest Commits**:
- `701b52d` - Add comprehensive summary of all critical fixes completed
- `7244f44` - CRITICAL: Fix race conditions, promise rejections, and add retry logic
- `6aa3200` - Add comprehensive code review summaries for Cursor and Gemini

**Files Present**:
- ✅ `CODE_REVIEW_FIXES_COMPLETE.md`
- ✅ `apps/factory/src/utils/retry.ts`
- ✅ `supabase/migrations/008_atomic_quota_updates.sql`
- ✅ `apps/factory/src/services/codex.service.ts` (updated)
- ✅ `apps/factory/src/services/quota.service.ts` (updated)

