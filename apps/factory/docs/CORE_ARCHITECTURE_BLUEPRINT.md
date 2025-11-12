# Core Architecture Blueprint

## Overview

All Expo development for the Design-First Software Factory follows a unified architecture that ensures:
- Single codebase targeting iOS, Android, and Web
- Platform-specific customization when necessary
- Consistent design system across platforms
- CI/CD enforcement of architectural principles

## Principles

### 1. Shared Codebase First (`src/`)

**All platform-agnostic code lives in `src/`:**

```
src/
├── screens/          # Screen components
├── components/       # Reusable UI components
├── services/         # Business logic, API clients
├── navigation/       # Navigation configuration
├── theme/            # Design tokens, theme configuration
└── utils/            # Helper functions, constants
```

**Key Rules:**
- Write platform-agnostic code by default
- Use React Native's built-in platform detection for minor variations
- Only create platform-overrides when absolutely necessary

### 2. Platform-Specific Adapters

**When platform-specific code is required:**

```typescript
// src/services/storage.ts
import { Platform } from 'react-native';

export const storage = Platform.select({
  web: () => require('./storage.web').default,
  default: () => require('./storage.native').default,
})();
```

**Or use file extensions:**
```
src/components/
├── Button.tsx           # Shared implementation
├── Button.ios.tsx       # iOS-specific (if needed)
├── Button.android.tsx   # Android-specific (if needed)
└── Button.web.tsx       # Web-specific (if needed)
```

### 3. Platform Overrides Directory

**Optional `/platform-overrides` for major platform differences:**

```
platform-overrides/
├── ios/
│   └── CustomNativeModule.swift
├── android/
│   └── CustomNativeModule.java
└── web/
    └── CustomWebComponent.tsx
```

**Activated by build-time flags:**
```json
{
  "expo": {
    "platforms": ["ios", "android", "web"],
    "ios": {
      "supportsTablet": true
    },
    "web": {
      "bundler": "metro"
    }
  }
}
```

### 4. Platform-Aware Design Tokens

**Theme configuration supports platform-specific values:**

```typescript
// src/theme/tokens.ts
import { Platform } from 'react-native';

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: Platform.select({
    web: 48,
    default: 32,
  }),
};

export const typography = {
  fontFamily: Platform.select({
    ios: 'System',
    android: 'Roboto',
    web: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  }),
};
```

### 5. CI Enforcement

**Automated checks in CI/CD:**

```yaml
# .github/workflows/architecture-compliance.yml
- name: Check Architecture Compliance
  run: |
    # Ensure no direct platform imports outside overrides
    npm run lint:architecture

    # Verify design tokens are used consistently
    npm run lint:design-tokens

    # Check for platform-specific code in shared directories
    npm run lint:platform-separation
```

## Testing Strategy

### Platform-Specific Testing

```typescript
// tests/platform-specific.test.ts
import { Platform } from 'react-native';

describe('Platform Behavior', () => {
  it('should use correct storage implementation', () => {
    if (Platform.OS === 'web') {
      expect(storage).toBeInstanceOf(WebStorage);
    } else {
      expect(storage).toBeInstanceOf(NativeStorage);
    }
  });
});
```

### Cross-Platform Visual Tests

```bash
# Run visual tests across platforms
npm run test:visual:ios
npm run test:visual:android
npm run test:visual:web
```

## Best Practices

### ✅ DO:
- Start with shared code in `src/`
- Use `Platform.select()` for minor variations
- Use file extensions (`.ios.tsx`, `.android.tsx`, `.web.tsx`) for component variants
- Keep design tokens in a centralized theme
- Write platform-agnostic tests first

### ❌ DON'T:
- Don't duplicate code across platforms without good reason
- Don't hardcode platform-specific values in components
- Don't bypass the theme system
- Don't create platform overrides prematurely

## Migration Guide

### From Platform-Specific to Shared

**Before:**
```typescript
// ios/CustomButton.tsx
export const CustomButton = () => { /* iOS code */ };

// android/CustomButton.tsx
export const CustomButton = () => { /* Android code */ };

// web/CustomButton.tsx
export const CustomButton = () => { /* Web code */ };
```

**After:**
```typescript
// src/components/CustomButton.tsx
import { Platform, Pressable } from 'react-native';

export const CustomButton = ({ onPress, children }) => (
  <Pressable
    onPress={onPress}
    style={Platform.select({
      ios: styles.ios,
      android: styles.android,
      web: styles.web,
    })}
  >
    {children}
  </Pressable>
);
```

## Validation

### Architecture Compliance Checklist

- [ ] All shared code in `src/` directory
- [ ] Platform-specific code uses `Platform.select()` or file extensions
- [ ] Design tokens centralized in `src/theme/`
- [ ] No hardcoded platform checks outside adapters
- [ ] CI checks pass for architecture compliance
- [ ] Tests cover all targeted platforms
- [ ] Documentation updated for platform-specific behavior

---

**Maintained by:** Claude (Foundation Architect)
**Last Updated:** 2025-11-06
