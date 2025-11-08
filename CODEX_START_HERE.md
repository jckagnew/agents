# Codex: Landing Page Implementation - Start Here

**The files you need are in this repository!** They were just committed on branch `claude/incomplete-description-011CUqTznbQhS98PNjB294jR`.

## 📍 Step 1: Make Sure You're on the Correct Branch

```bash
cd /home/user/agents/design-first-software-factory

# Check current branch
git branch --show-current

# If not on the correct branch, switch to it:
git fetch origin
git checkout claude/incomplete-description-011CUqTznbQhS98PNjB294jR

# Pull latest changes
git pull origin claude/incomplete-description-011CUqTznbQhS98PNjB294jR
```

## 📂 Step 2: File Locations (All files are HERE in this repo!)

### Main Implementation Guide
**File:** `CODEX_LANDING_PAGE_README.md` (in root directory)
```bash
cat CODEX_LANDING_PAGE_README.md
```

### Component Specifications (27 pages)
**File:** `docs/LANDING_PAGE_COMPONENT_SPECS.md`
```bash
cat docs/LANDING_PAGE_COMPONENT_SPECS.md
```

### Copy Variations (22 pages)
**File:** `docs/LANDING_PAGE_COPY_VARIATIONS.md`
```bash
cat docs/LANDING_PAGE_COPY_VARIATIONS.md
```

### Design Tokens
**File:** `src/constants/design-tokens.ts` (NEW - 560 lines)
```bash
cat src/constants/design-tokens.ts
```

**Note:** If you have an existing `src/designTokens.ts`, you can either:
- Use the new tokens at `src/constants/design-tokens.ts` (recommended - platform-aware)
- Or integrate the new tokens into your existing file

## ✅ Step 3: Verify Files Exist

Run this to confirm all files are present:

```bash
cd /home/user/agents/design-first-software-factory

echo "Checking for landing page files..."
ls -lh CODEX_LANDING_PAGE_README.md
ls -lh docs/LANDING_PAGE_COMPONENT_SPECS.md
ls -lh docs/LANDING_PAGE_COPY_VARIATIONS.md
ls -lh src/constants/design-tokens.ts

echo "✅ All files found!"
```

## 🚀 Step 4: Start Implementing CTAPrimary

Once you have the files, follow these steps:

### A. Read the Implementation Guide
```bash
cat CODEX_LANDING_PAGE_README.md | less
# Or open in your editor
```

### B. Review CTAPrimary Specification
```bash
# The spec starts at line 745 in the component specs
sed -n '745,850p' docs/LANDING_PAGE_COMPONENT_SPECS.md
```

### C. Review Design Tokens Usage
```bash
# See how to use the design tokens
sed -n '1,100p' src/constants/design-tokens.ts
```

### D. Create the Component File
```bash
mkdir -p src/components/landing-page/ctas
touch src/components/landing-page/ctas/CTAPrimary.tsx
```

### E. Basic Template to Start

```typescript
// src/components/landing-page/ctas/CTAPrimary.tsx
import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator, View } from 'react-native';
import { colors, typography, spacing, borderRadius, shadows, touchTargets } from '../../../constants/design-tokens';

interface CTAPrimaryProps {
  text: string;
  onPress: () => void;
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;
  loading?: boolean;
  disabled?: boolean;
  icon?: string;
  iconPosition?: 'left' | 'right';
  ariaLabel?: string;
}

export const CTAPrimary: React.FC<CTAPrimaryProps> = ({
  text,
  onPress,
  size = 'medium',
  fullWidth = false,
  loading = false,
  disabled = false,
  icon,
  iconPosition = 'left',
  ariaLabel,
}) => {
  // Implementation here - follow spec at docs/LANDING_PAGE_COMPONENT_SPECS.md:745
  
  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled || loading}
      accessible={true}
      accessibilityLabel={ariaLabel || text}
      accessibilityRole="button"
      style={{
        backgroundColor: colors.primary.main,
        paddingHorizontal: spacing.lg,
        paddingVertical: spacing.md,
        borderRadius: borderRadius.md,
        minHeight: touchTargets.minimum,
        // Add more styles based on spec
      }}
    >
      {loading ? (
        <ActivityIndicator color={colors.text.inverse} />
      ) : (
        <Text style={{
          color: colors.text.inverse,
          fontSize: typography.fontSize.body.medium,
          fontWeight: typography.fontWeight.semibold,
        }}>
          {text}
        </Text>
      )}
    </TouchableOpacity>
  );
};
```

## 🔍 Troubleshooting

### "I still can't find the files"

Run this diagnostic:
```bash
cd /home/user/agents/design-first-software-factory
git status
git log --oneline -5
git branch -a
ls -la | head -20
```

Then share the output and we'll help you locate them.

### "The design tokens don't match my existing tokens"

The new tokens at `src/constants/design-tokens.ts` are **platform-aware** and include:
- iOS HIG values
- Material Design values  
- Web-optimized values

They're more comprehensive than basic tokens. You can:
1. Use them as-is (recommended)
2. Merge them with your existing tokens
3. Ask for help migrating

## 📞 Questions?

If you can't find the files or need help:
1. Share your `git status` output
2. Share your `pwd` output
3. Share result of: `git log --oneline -5`

We'll help you locate everything! All files definitely exist in commit `975abe7` on branch `claude/incomplete-description-011CUqTznbQhS98PNjB294jR`.

---

**Ready to build! 🚀**
