# GEMINI RESCUE PROMPT - Fix ESLint Errors in name-vetting.js

**URGENT:** You're stuck in a loop trying to fix ESLint errors. Stop using `write_file` and switch to the `Edit` tool which is more reliable.

## The Problem

You're trying to fix these ESLint errors in `design-first-software-factory/src/services/name-vetting.js`:
1. **no-unused-vars**: Variables declared but never used (path, industry, headError, _, availableCount, platform, error)
2. **no-useless-escape**: Unnecessary escape character in `normalizeToDomain` function

## The Solution

**STOP using `write_file`**. Use the `Edit` tool instead, which does exact string replacement.

### Step 1: Fix the no-useless-escape error first

Use the `Edit` tool to find and replace the problematic line in `normalizeToDomain`:

**Old string (find this EXACT text):**
```javascript
  return name.toLowerCase().replace(/[^a-z0-9\-]/g, '-');
```

**New string (replace with):**
```javascript
  return name.toLowerCase().replace(/[^a-z0-9-]/g, '-');
```

### Step 2: Remove unused variables one at a time

For each unused variable, use `Edit` to remove the ENTIRE line where it's declared:

**Example for `path`:**
```javascript
// OLD (remove this line):
const path = require('path');

// Just delete the entire line - don't replace with anything
```

**For the destructuring line with `_` and `availableCount`:**
```javascript
// OLD:
const { available, _, availableCount } = await checkDomainAvailability(domain);

// NEW (remove unused vars):
const { available } = await checkDomainAvailability(domain);
```

### Step 3: Important Rules

1. **Use `Edit` tool, NOT `write_file`**
2. **Match EXACT indentation** (including spaces/tabs)
3. **Copy the old string EXACTLY** from the file
4. **Make ONE change at a time**
5. **If Edit fails, read the file again to get exact text**

## Example Edit Tool Usage

```javascript
// Read the file first
Read('design-first-software-factory/src/services/name-vetting.js')

// Then use Edit with EXACT text matching
Edit({
  file_path: 'design-first-software-factory/src/services/name-vetting.js',
  old_string: "const path = require('path');",  // EXACT text from file
  new_string: ""  // Empty string to delete the line
})
```

## Order of Operations

Fix in this order:
1. Fix `no-useless-escape` in `normalizeToDomain` (the backslash before hyphen)
2. Remove `const path = require('path');`
3. Remove `const industry` from destructuring if unused
4. Remove `const headError` if unused
5. Remove `_` and `availableCount` from destructuring
6. Remove `const platform` if unused
7. Remove `const error` if unused

## If You're Still Stuck

**DO NOT:**
- ❌ Use `write_file` (it's causing the loop)
- ❌ Try to rewrite the whole file
- ❌ Guess at the exact text

**DO:**
- ✅ Read the file first to see current state
- ✅ Use `Edit` tool with exact text matching
- ✅ Make one change at a time
- ✅ Verify each change by reading the file after

## Expected Final State

After all fixes, run:
```bash
npm run lint src/services/name-vetting.js
```

Should show **0 errors**.

## Need Help?

If you're still stuck after trying Edit tool:
1. Read the file and share the exact lines with errors
2. We'll provide the EXACT old_string/new_string for Edit tool
3. Make sure you're in the right directory: `design-first-software-factory/`

**Remember:** Edit tool is your friend. It does exact string replacement and is much more reliable than write_file for fixing specific lines.

Good luck! 🚀
