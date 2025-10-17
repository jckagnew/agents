# Design System Usage Guide

## Overview

Our design system provides shared tokens and components across React Native and Next.js platforms, ensuring visual consistency and reducing duplication.

## 🎨 Shared Tokens

### Location
- **Source**: `design-system/googleTheme.ts`
- **React Native**: `weight-tracker/src/theme/index.ts`
- **Next.js**: `software-factory/generated-apps/weight-tracker-nextjs/src/app/globals.css`

### Token Structure
```typescript
// design-system/googleTheme.ts
export const googleTheme = {
  colors: {
    primary: { 50: '#eff6ff', 500: '#3b82f6', 600: '#2563eb' },
    // ... more colors
  },
  spacing: { xs: 4, sm: 8, md: 16 },
  typography: { fontFamily: 'Poppins', fontSize: { sm: 14 } },
  // ... more tokens
}
```

**Note**: Source tokens use numeric values (e.g., `16` for spacing), while CSS variables expose pixel strings (e.g., `16px`). The platform integrations handle this conversion automatically.

## 🔄 Platform Integration

### React Native Usage
```typescript
// weight-tracker/src/theme/index.ts
import { googleTheme } from '../../../design-system/googleTheme'

export const theme = {
  colors: googleTheme.colors,
  spacing: googleTheme.spacing,
  // Map tokens to React Native StyleSheet format
}
```

### Next.js Usage
```css
/* software-factory/generated-apps/weight-tracker-nextjs/src/app/globals.css */
:root {
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  /* ... more CSS variables */
}
```

## 🛠️ Making Changes

### 1. Update Source Tokens
Edit `design-system/googleTheme.ts` to modify shared values:

```typescript
export const googleTheme = {
  colors: {
    primary: {
      500: '#2563eb', // Changed from #3b82f6
    }
  }
}
```

### 2. Regenerate Platform Mappings

#### React Native
```bash
# Update theme mapping
cd weight-tracker
# Edit src/theme/index.ts to reflect new tokens
```

#### Next.js
```bash
# Update CSS variables
cd software-factory/generated-apps/weight-tracker-nextjs
# Edit src/app/globals.css to reflect new tokens
```

### 3. Test Both Platforms
- **React Native**: Run on iOS/Android simulators
- **Next.js**: Run `npm run dev` and test in browser

## 📱 Responsive Design

### Breakpoints
```css
/* Tailwind breakpoints for Next.js */
sm: '640px'   /* Mobile landscape */
md: '768px'   /* Tablet */
lg: '1024px'  /* Desktop */
xl: '1280px'  /* Large desktop */
```

### Typography Scale
```typescript
// Responsive typography tokens
typography: {
  fontSize: {
    xs: 12,    // Mobile small
    sm: 14,    // Mobile body
    base: 16,  // Mobile large / Desktop small
    lg: 18,    // Desktop body
    xl: 24,    // Desktop heading
    '2xl': 32, // Large heading
  }
}
```

## 🧩 Shared Components

### MetricCard Component
```typescript
// software-factory/generated-apps/weight-tracker-nextjs/src/components/design-system/MetricCard.tsx
interface MetricCardProps {
  title: string
  value: string | number
  trend?: 'up' | 'down' | 'neutral'
  className?: string
}

export function MetricCard({ title, value, trend, className }: MetricCardProps) {
  return (
    <div className={`metric-card ${className}`}>
      <h3 className="metric-card__title">{title}</h3>
      <div className="metric-card__value">{value}</div>
      {trend && <div className={`metric-card__trend metric-card__trend--${trend}`} />}
    </div>
  )
}
```

### PillButton Component
```typescript
// software-factory/generated-apps/weight-tracker-nextjs/src/components/design-system/PillButton.tsx
interface PillButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  onClick?: () => void
  className?: string
}

export function PillButton({ children, variant = 'primary', size = 'md', onClick, className }: PillButtonProps) {
  return (
    <button 
      className={`pill-button pill-button--${variant} pill-button--${size} ${className}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

## 🎯 Best Practices

### 1. Token Naming
- Use semantic names: `primary`, `secondary`, `success`, `warning`, `error`
- Include scale numbers: `50`, `100`, `200`, ..., `900`
- Be consistent across platforms

### 2. Component Design
- Accept `className` prop for customization
- Use CSS variables for styling
- Include TypeScript interfaces
- Export from index files

### 3. Testing
- Test on multiple screen sizes
- Verify color contrast ratios
- Check font loading performance
- Validate accessibility

## 🔍 Troubleshooting

### Common Issues

#### Fonts Not Loading
```typescript
// Check next/font configuration
import { Poppins, Nunito } from 'next/font/google'

const poppins = Poppins({ 
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-poppins'
})
```

#### CSS Variables Not Applied
```css
/* Ensure CSS variables are defined in :root */
:root {
  --color-primary-500: #3b82f6;
}

/* Use in components */
.button {
  background-color: var(--color-primary-500);
}
```

#### Token Drift Between Platforms
- Always update source tokens first
- Regenerate both platform mappings
- Test both platforms after changes
- Use automated tests to catch drift

## 📚 Resources

- [Design System Source](../design-system/googleTheme.ts)
- [React Native Theme](../weight-tracker/src/theme/index.ts)
- [Next.js CSS Variables](../software-factory/generated-apps/weight-tracker-nextjs/src/app/globals.css)
- [Component Library](../software-factory/generated-apps/weight-tracker-nextjs/src/components/design-system/)

## 🚀 Next Steps

1. **Extract Components**: Move duplicated styles to shared components
2. **Responsive QA**: Test across all breakpoints
3. **Documentation**: Update component stories and examples
4. **Automation**: Add tests to prevent token drift
5. **Validation**: Get design/product sign-off on final implementation
