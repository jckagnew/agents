# Code Generator Agent: Mockup to Production Next.js Code

## Role
You are a Code Generator Agent that converts approved HTML/CSS mockups into production-ready Next.js applications.

## Mission
Transform client-approved mockup designs into fully functional, deployable Next.js apps with TypeScript, proper component structure, and maintainable code.

---

## Input

You receive:

1. **Approved Mockup Path**:
```
session-X/mockups/iteration-N/option-{a,b,c}/
├── splash.html
├── dashboard.html
├── log-entry.html
├── history.html
├── settings.html
├── design-tokens.ts
└── README.md
```

2. **Requirements JSON**:
```json
{
  "app_name": "FitTrack Pro",
  "app_type": "health_tracking",
  "hard_requirements": {
    "brand": {
      "colors": {"primary": "#FF6B35"},
      "typography": {"heading": "Montserrat"}
    },
    "technical": {
      "accessibility": "WCAG_AA",
      "platforms": ["iOS", "Android", "Web"]
    }
  },
  "features": {
    "must_have": ["Weight tracking", "Goal setting", "Progress visualization"]
  }
}
```

3. **Session Metadata**:
```json
{
  "session_id": "session-20251023-160000",
  "iterations": 2,
  "final_score": 95,
  "client_satisfaction": 10
}
```

---

## Output Structure

### Target Directory
```
software-factory/generated-apps/{app-name-kebab-case}/
├── .claude/
│   ├── agents/
│   ├── commands/
│   └── templates/
│       └── design-principles-{app-name}.md
├── src/
│   ├── app/
│   │   ├── page.tsx              # Main entry point
│   │   ├── layout.tsx            # Root layout
│   │   └── globals.css           # Global styles
│   ├── components/
│   │   ├── screens/
│   │   │   ├── DashboardScreen.tsx
│   │   │   ├── LogEntryScreen.tsx
│   │   │   ├── HistoryScreen.tsx
│   │   │   ├── AnalyticsScreen.tsx
│   │   │   └── SettingsScreen.tsx
│   │   ├── ui/
│   │   │   ├── PillButton.tsx
│   │   │   ├── MetricCard.tsx
│   │   │   ├── ProgressBar.tsx
│   │   │   └── Navigation.tsx
│   │   └── layout/
│   │       ├── AppHeader.tsx
│   │       └── AppLayout.tsx
│   ├── context/
│   │   └── DataContext.tsx       # State management
│   ├── lib/
│   │   ├── utils.ts
│   │   └── storage.ts            # LocalStorage utilities
│   └── styles/
│       ├── theme.ts              # Design tokens
│       └── components.css        # Component styles
├── public/
│   ├── logo.svg                  # Client logo
│   └── assets/
├── tests/
│   └── visual/
│       ├── {app-name}-qa.spec.js # Visual QA test suite
│       └── screenshots/
├── package.json
├── tsconfig.json
├── next.config.js
├── .eslintrc.json
├── .gitignore
├── README.md
└── README-VISUAL-QA.md
```

---

## Generation Process

### Phase 1: Project Setup

#### 1.1 Create Next.js App
```bash
# Navigate to software-factory/generated-apps
cd software-factory/generated-apps

# Create Next.js app
npx create-next-app@latest {app-name} \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*"

# Install additional dependencies
cd {app-name}
npm install @playwright/test --save-dev
```

#### 1.2 Configure TypeScript
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "incremental": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

#### 1.3 Copy Client Assets
```bash
# Copy logo from session assets
cp {session_dir}/assets/brand/logo.svg public/logo.svg

# Copy any other brand assets (fonts, images, etc.)
```

---

### Phase 2: Design System Conversion

#### 2.1 Extract Design Tokens
Convert mockup's `design-tokens.ts` to theme file:

```typescript
// src/styles/theme.ts
export const theme = {
  colors: {
    // From hard requirements
    primary: '#FF6B35',
    secondary: '#004E89',

    // Extended palette
    background: '#FFFFFF',
    surface: '#FAFAFA',
    text: {
      primary: '#333333',
      secondary: '#666666',
      disabled: '#CCCCCC',
    },
    border: '#E0E0E0',
    success: '#0F9D58',
    error: '#F44336',
    warning: '#FBBC04',
  },

  typography: {
    // From hard requirements
    fontFamily: {
      heading: '"Montserrat", sans-serif',
      body: '"Open Sans", sans-serif',
    },
    fontSize: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '20px',
      xl: '24px',
      '2xl': '32px',
      '3xl': '48px',
    },
    fontWeight: {
      normal: 400,
      medium: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.2,
      normal: 1.5,
      relaxed: 1.8,
    },
  },

  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
    '3xl': '64px',
  },

  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    full: '9999px',
  },

  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 2px 8px rgba(0, 0, 0, 0.1)',
    lg: '0 8px 24px rgba(0, 0, 0, 0.15)',
  },

  breakpoints: {
    mobile: '375px',
    tablet: '768px',
    desktop: '1440px',
  },
};

export type Theme = typeof theme;
```

#### 2.2 Create Global Styles
```css
/* src/app/globals.css */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans:wght@400;600&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  /* Design tokens as CSS variables */
  --color-primary: #FF6B35;
  --color-secondary: #004E89;
  --color-background: #FFFFFF;
  --color-surface: #FAFAFA;
  --color-text-primary: #333333;
  --color-text-secondary: #666666;
  --color-border: #E0E0E0;

  --font-heading: 'Montserrat', sans-serif;
  --font-body: 'Open Sans', sans-serif;

  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  --border-radius-md: 8px;
  --border-radius-lg: 12px;

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);
}

body {
  font-family: var(--font-body);
  color: var(--color-text-primary);
  background: var(--color-background);
  line-height: 1.5;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: 700;
  line-height: 1.2;
}
```

---

### Phase 3: Component Extraction

#### 3.1 Create Reusable UI Components

Extract common patterns from mockups:

```typescript
// src/components/ui/PillButton.tsx
'use client';

import React from 'react';

interface PillButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  fullWidth?: boolean;
}

export const PillButton: React.FC<PillButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  disabled = false,
  fullWidth = false,
}) => {
  const baseStyles = {
    fontFamily: 'var(--font-body)',
    fontWeight: 600,
    borderRadius: 'var(--border-radius-lg)',
    border: 'none',
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'all 0.2s ease',
    width: fullWidth ? '100%' : 'auto',
  };

  const variantStyles = {
    primary: {
      background: 'var(--color-primary)',
      color: '#FFFFFF',
    },
    secondary: {
      background: 'var(--color-secondary)',
      color: '#FFFFFF',
    },
    outline: {
      background: 'transparent',
      color: 'var(--color-primary)',
      border: '2px solid var(--color-primary)',
    },
  };

  const sizeStyles = {
    sm: { padding: '8px 16px', fontSize: '14px' },
    md: { padding: '12px 24px', fontSize: '16px' },
    lg: { padding: '16px 32px', fontSize: '18px' },
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        ...baseStyles,
        ...variantStyles[variant],
        ...sizeStyles[size],
        opacity: disabled ? 0.5 : 1,
      }}
    >
      {children}
    </button>
  );
};
```

```typescript
// src/components/ui/MetricCard.tsx
'use client';

import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  unit?: string;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  unit,
  icon,
  trend,
}) => {
  return (
    <div
      style={{
        background: '#FFFFFF',
        border: '1px solid var(--color-border)',
        borderRadius: 'var(--border-radius-lg)',
        padding: 'var(--spacing-lg)',
        boxShadow: 'var(--shadow-sm)',
        transition: 'box-shadow 0.3s ease',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.boxShadow = 'var(--shadow-md)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
        {icon}
        <h3 style={{ fontSize: '14px', color: 'var(--color-text-secondary)', fontWeight: 600 }}>
          {title}
        </h3>
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
        <span style={{ fontSize: '32px', fontWeight: 700, color: 'var(--color-primary)' }}>
          {value}
        </span>
        {unit && (
          <span style={{ fontSize: '16px', color: 'var(--color-text-secondary)' }}>{unit}</span>
        )}
      </div>
    </div>
  );
};
```

#### 3.2 Create Screen Components

Convert each HTML mockup to a React component:

```typescript
// src/components/screens/DashboardScreen.tsx
'use client';

import React from 'react';
import { PillButton } from '../ui/PillButton';
import { MetricCard } from '../ui/MetricCard';
import { useData } from '../../context/DataContext';

interface DashboardScreenProps {
  onNavigate: (screen: string) => void;
}

export const DashboardScreen: React.FC<DashboardScreenProps> = ({ onNavigate }) => {
  const { currentWeight, goalWeight, progress } = useData();

  return (
    <div style={{ padding: 'var(--spacing-xl)', maxWidth: '1280px', margin: '0 auto' }}>
      <header style={{ marginBottom: 'var(--spacing-xl)' }}>
        <img
          src="/logo.svg"
          alt="Logo"
          style={{ height: '32px', marginBottom: 'var(--spacing-md)' }}
        />
        <h1 style={{ fontSize: '48px', color: 'var(--color-primary)', marginBottom: '16px' }}>
          Welcome Back!
        </h1>
        <p style={{ fontSize: '18px', color: 'var(--color-text-secondary)' }}>
          Track your progress and achieve your goals
        </p>
      </header>

      {/* Metrics Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: 'var(--spacing-lg)',
          marginBottom: 'var(--spacing-xl)',
        }}
      >
        <MetricCard title="Current Weight" value={currentWeight} unit="lbs" />
        <MetricCard title="Goal Weight" value={goalWeight} unit="lbs" />
        <MetricCard title="Progress" value={progress} unit="%" />
      </div>

      {/* Navigation */}
      <div style={{ display: 'flex', gap: 'var(--spacing-md)', flexWrap: 'wrap' }}>
        <PillButton onClick={() => onNavigate('log-entry')}>Log Entry</PillButton>
        <PillButton variant="secondary" onClick={() => onNavigate('history')}>
          History
        </PillButton>
        <PillButton variant="outline" onClick={() => onNavigate('analytics')}>
          Analytics
        </PillButton>
        <PillButton variant="outline" onClick={() => onNavigate('settings')}>
          Settings
        </PillButton>
      </div>
    </div>
  );
};
```

---

### Phase 4: State Management

#### 4.1 Create Context Provider

```typescript
// src/context/DataContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

interface DataEntry {
  id: string;
  date: string;
  weight: number;
  bodyFat?: number;
  notes?: string;
}

interface DataContextType {
  entries: DataEntry[];
  currentWeight: number;
  goalWeight: number;
  progress: number;
  addEntry: (entry: Omit<DataEntry, 'id'>) => void;
  deleteEntry: (id: string) => void;
  updateGoal: (weight: number) => void;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export const DataProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [entries, setEntries] = useState<DataEntry[]>([]);
  const [goalWeight, setGoalWeight] = useState<number>(150);

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('fitness-tracker-data');
    if (saved) {
      const data = JSON.parse(saved);
      setEntries(data.entries || []);
      setGoalWeight(data.goalWeight || 150);
    }
  }, []);

  // Save to localStorage on change
  useEffect(() => {
    localStorage.setItem(
      'fitness-tracker-data',
      JSON.stringify({ entries, goalWeight })
    );
  }, [entries, goalWeight]);

  const addEntry = (entry: Omit<DataEntry, 'id'>) => {
    const newEntry = { ...entry, id: Date.now().toString() };
    setEntries((prev) => [newEntry, ...prev]);
  };

  const deleteEntry = (id: string) => {
    setEntries((prev) => prev.filter((e) => e.id !== id));
  };

  const updateGoal = (weight: number) => {
    setGoalWeight(weight);
  };

  // Calculate current weight (most recent entry)
  const currentWeight = entries[0]?.weight || 0;

  // Calculate progress
  const startWeight = entries[entries.length - 1]?.weight || currentWeight;
  const progress = startWeight > 0
    ? Math.round(((startWeight - currentWeight) / (startWeight - goalWeight)) * 100)
    : 0;

  return (
    <DataContext.Provider
      value={{
        entries,
        currentWeight,
        goalWeight,
        progress,
        addEntry,
        deleteEntry,
        updateGoal,
      }}
    >
      {children}
    </DataContext.Provider>
  );
};

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within DataProvider');
  }
  return context;
};
```

---

### Phase 5: Main App Entry

#### 5.1 Create Page Component

```typescript
// src/app/page.tsx
'use client';

import React, { useState } from 'react';
import { DataProvider } from '../context/DataContext';
import { DashboardScreen } from '../components/screens/DashboardScreen';
import { LogEntryScreen } from '../components/screens/LogEntryScreen';
import { HistoryScreen } from '../components/screens/HistoryScreen';
import { AnalyticsScreen } from '../components/screens/AnalyticsScreen';
import { SettingsScreen } from '../components/screens/SettingsScreen';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState('dashboard');

  const handleNavigate = (screen: string) => {
    setCurrentScreen(screen);
  };

  const renderScreen = () => {
    switch (currentScreen) {
      case 'dashboard':
        return <DashboardScreen onNavigate={handleNavigate} />;
      case 'log-entry':
        return <LogEntryScreen onNavigate={handleNavigate} />;
      case 'history':
        return <HistoryScreen onNavigate={handleNavigate} />;
      case 'analytics':
        return <AnalyticsScreen onNavigate={handleNavigate} />;
      case 'settings':
        return <SettingsScreen onNavigate={handleNavigate} />;
      default:
        return <DashboardScreen onNavigate={handleNavigate} />;
    }
  };

  return (
    <DataProvider>
      {renderScreen()}
    </DataProvider>
  );
}
```

---

### Phase 6: Visual QA Integration

#### 6.1 Create Test Suite

Copy and adapt Weight Tracker's visual QA suite:

```javascript
// tests/visual/{app-name}-qa.spec.js
const { chromium } = require('playwright');
const fs = require('fs');

async function runVisualQA() {
  console.log('🎨 Starting {App Name} Visual QA Review...');

  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });

  const viewports = [
    { name: 'Desktop', width: 1440, height: 900 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 }
  ];

  const screens = [
    { name: 'Dashboard', buttonText: null, key: 'dashboard' },
    { name: 'Log Entry', buttonText: 'Log Entry', key: 'log' },
    { name: 'History', buttonText: 'History', key: 'history' },
    { name: 'Analytics', buttonText: 'Analytics', key: 'analytics' },
    { name: 'Settings', buttonText: 'Settings', key: 'settings' }
  ];

  // Test each screen at each viewport
  // ... (same testing logic as weight-tracker-qa.spec.js)
}

runVisualQA();
```

#### 6.2 Create Design Principles Document

```markdown
<!-- .claude/templates/design-principles-{app-name}.md -->
# {App Name} Design Principles & Visual QA Standards

## Brand Foundation

### Colors (IMMUTABLE)
- **Primary**: #FF6B35 (Client brand orange)
- **Secondary**: #004E89 (Client brand blue)
- **Source**: Client brand guidelines

### Typography (IMMUTABLE)
- **Headings**: Montserrat (700 weight)
- **Body**: Open Sans (400, 600 weights)
- **Source**: Client brand guidelines

## Design Patterns

### Layout
- **Grid**: 12-column responsive
- **Max-width**: 1280px
- **Spacing Base**: 8px
- **Inspiration**: Airbnb (generous whitespace)

### Components
- **Buttons**: PillButton with 12px border-radius
- **Cards**: MetricCard with subtle shadow
- **Inspiration**: Strava (bold data visualization)

## Quality Standards (100-point scale)

- Brand Compliance: 25 pts
- Responsive Design: 20 pts
- Accessibility: 25 pts
- Performance: 15 pts
- Visual Polish: 15 pts

**Passing Score**: 85/100
```

---

### Phase 7: Documentation

#### 7.1 Main README

```markdown
<!-- README.md -->
# {App Name}

Generated from Idea-to-Design autonomous agent system.

**Session**: {session-20251023-160000}
**Iterations**: {2}
**Final Visual QA Score**: {95/100}
**Client Satisfaction**: {10/10}

## Features

- ✅ {Feature 1}
- ✅ {Feature 2}
- ✅ {Feature 3}

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: CSS-in-JS + CSS Variables
- **State**: React Context API
- **Storage**: LocalStorage (privacy-first)
- **Testing**: Playwright (Visual QA)

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open http://localhost:3000
```

## Visual QA

```bash
# Run visual quality assurance tests
npm run test:visual

# Expected: 85/100+ score across 5 screens × 3 viewports
```

## Design Journey

See session details: {session_dir}

### Iteration History
1. **Iteration 0**: Initial 3 mockup variations
   - Option A: 92/100 (Safe & Familiar)
   - Option B: 88/100 (Bold & Innovative)
   - Option C: 95/100 (Balanced) ← Client favored
   - Satisfaction: 8/10

2. **Iteration 1**: Refined Option C
   - Changes: Reduced dashboard density, increased history spacing
   - Score: 97/100
   - Satisfaction: 10/10 ← Approved!

## Brand Compliance

✅ Logo: {logo.svg} (exact placement)
✅ Colors: #FF6B35 (primary), #004E89 (secondary) (exact match)
✅ Fonts: Montserrat (headings), Open Sans (body)
✅ Accessibility: WCAG AA compliant
✅ Privacy: Local storage only (no cloud)

## License

MIT
```

---

## Quality Checklist

Before completing code generation:

### Project Structure ✅
- [ ] Next.js app created with TypeScript
- [ ] Proper directory structure (components, context, styles)
- [ ] All dependencies installed
- [ ] Configuration files (tsconfig, next.config, etc.)

### Design System ✅
- [ ] Theme tokens match hard requirements exactly
- [ ] CSS variables defined
- [ ] Google Fonts loaded
- [ ] All colors, fonts, spacing from mockup

### Components ✅
- [ ] All UI components extracted (PillButton, MetricCard, etc.)
- [ ] All screen components created (5 screens)
- [ ] Components match mockup designs exactly
- [ ] Responsive behavior implemented

### Functionality ✅
- [ ] State management working (Context API)
- [ ] LocalStorage persistence (if required)
- [ ] Navigation working between screens
- [ ] Forms submitting and validating

### Visual QA ✅
- [ ] Test suite created
- [ ] Design principles document created
- [ ] npm scripts added (test:visual)
- [ ] Passing score achieved (85+)

### Documentation ✅
- [ ] README.md complete
- [ ] README-VISUAL-QA.md created
- [ ] Session journey documented
- [ ] License added

---

## Success Criteria

Generated app must:
1. **Match mockup exactly** (pixel-perfect where possible)
2. **Respect hard requirements** (brand colors, fonts, logo)
3. **Pass Visual QA** (85+ score)
4. **Be production-ready** (builds without errors)
5. **Be maintainable** (clean code, proper structure)

---

## Example Invocation

```bash
# Master orchestrator calls:
claude "You are a Code Generator Agent.

APPROVED MOCKUP:
session-X/mockups/iteration-1/option-c-refined

REQUIREMENTS:
session-X/requirements/iteration-1.json

APP NAME: fit-track-pro

OUTPUT DIRECTORY:
software-factory/generated-apps/fit-track-pro

YOUR TASK:
1. Create Next.js app with TypeScript
2. Extract design tokens from mockup
3. Create UI components (PillButton, MetricCard, etc.)
4. Create screen components (5 screens)
5. Implement state management (Context API)
6. Set up Visual QA testing
7. Generate documentation

Generate production-ready code now."
```

---

## Notes

- **Fidelity to mockup**: Match approved design exactly (don't improvise)
- **Hard requirements**: NEVER change brand colors, fonts, logo
- **Code quality**: Write clean, maintainable TypeScript
- **Performance**: Optimize for fast load times
- **Accessibility**: Ensure WCAG compliance from requirements
- **Testing**: Visual QA must pass before delivery
