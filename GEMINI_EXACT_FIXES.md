# GEMINI - EXACT FIXES FOR name-vetting.js

**STOP THE LOOP!** Here are the exact ESLint fixes you need to make using the `Edit` tool.

## CRITICAL: Use Edit Tool, NOT write_file

```javascript
// Example usage:
Edit({
  file_path: '/home/user/agents/scripts/name-vetting.js',
  old_string: "exact text from file",
  new_string: "replacement text"
})
```

---

## Fix #1: Remove unused `path` variable

**Location:** Line 28

**Use Edit tool:**
```javascript
old_string: "const path = require('path');"
new_string: ""
```

**This will delete the entire line.**

---

## Fix #2: Remove unused `industry` parameter

**Location:** Line 451

**Use Edit tool:**
```javascript
old_string: "async function checkTrademarkConflicts(businessName, industry = null) {"
new_string: "async function checkTrademarkConflicts(businessName) {"
```

---

## Fix #3: Remove unused `platform` parameter

**Location:** Line 1133

**Use Edit tool:**
```javascript
old_string: "function normalizeToHandle(name, platform) {"
new_string: "function normalizeToHandle(name) {"
```

---

## Fix #4: Check for no-useless-escape in normalizeToDomain

**Location:** Around line 399-410

**First, READ the file to see the current state of the normalizeToDomain function.**

If you see this pattern:
```javascript
.replace(/[^a-z0-9\-]/g, '')
```

Then the hyphen is unnecessarily escaped (ESLint error). Fix it with Edit:

```javascript
old_string: "    .replace(/[^a-z0-9\\-]/g, '')"
new_string: "    .replace(/[^a-z0-9-]/g, '')"
```

**Note:** Inside a character class `[...]`, hyphens at the end don't need escaping.

---

## STEP-BY-STEP PROCESS

1. **First, READ the file** to confirm current state:
   ```javascript
   Read('/home/user/agents/scripts/name-vetting.js')
   ```

2. **Make ONE fix at a time** using Edit tool

3. **After each Edit**, read the file again to verify the change worked

4. **Run ESLint** after all fixes:
   ```bash
   npm run lint scripts/name-vetting.js
   ```

---

## If Edit Tool Fails

If Edit fails with "old_string not found":
1. READ the file again
2. Copy the EXACT line (with all spaces/tabs) from the Read output
3. Look at the line number prefix (like `28→`) and copy everything AFTER the arrow
4. Try the Edit again with exact text

---

## Example Sequence

```javascript
// Step 1: Read file
Read('/home/user/agents/scripts/name-vetting.js')

// Step 2: Fix path import
Edit({
  file_path: '/home/user/agents/scripts/name-vetting.js',
  old_string: "const path = require('path');",
  new_string: ""
})

// Step 3: Read to verify
Read('/home/user/agents/scripts/name-vetting.js', { offset: 25, limit: 5 })

// Step 4: Fix industry parameter
Edit({
  file_path: '/home/user/agents/scripts/name-vetting.js',
  old_string: "async function checkTrademarkConflicts(businessName, industry = null) {",
  new_string: "async function checkTrademarkConflicts(businessName) {"
})

// Continue for other fixes...
```

---

## Summary

You need to make **3-4 simple fixes** using the Edit tool:
1. ✅ Remove `const path = require('path');`
2. ✅ Remove `industry` parameter from checkTrademarkConflicts
3. ✅ Remove `platform` parameter from normalizeToHandle
4. ✅ Fix escaped hyphen in normalizeToDomain (if present)

**DO NOT** rewrite the entire file. Just make these small targeted changes.

**Good luck!** 🚀
