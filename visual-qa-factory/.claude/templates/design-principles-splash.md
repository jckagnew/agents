# Design Principles - Splash Pages
## Universal Foundation for Visual QA

## Section 1: Brand Foundation

### Color System
**Primary Colors:**
- Brand Primary: #0066FF (Usage: CTAs, key actions, headers)
- Brand Secondary: #00CC88 (Usage: accents, highlights, secondary actions)

**Neutral Palette:**
- Background: #F8F9FA
- Surface: #FFFFFF
- Border: #E5E7EB
- Text Primary: #212529
- Text Secondary: #6C757D
- Text Tertiary: #ADB5BD

**Semantic Colors:**
- Success: #00CC88
- Warning: #FFC107
- Error: #DC3545
- Info: #17A2B8

**Validation Rules:**
- All colors must pass WCAG AA contrast requirements (4.5:1 for body, 3:1 for large text)
- No arbitrary hex codes—use defined palette only
- Semantic colors reserved for their designated purposes

### Typography System
**Font Families:**
- Primary (UI): Inter
  - Fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- Secondary (Headings): Space Grotesk
  - Fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif

**Type Scale (Desktop):**
- Display: 48px / 1.2 / 700
- H1: 36px / 1.2 / 700
- H2: 28px / 1.3 / 600
- H3: 24px / 1.4 / 600
- Body Large: 18px / 1.6 / 400
- Body: 16px / 1.5 / 400
- Body Small: 14px / 1.5 / 400

**Type Scale (Mobile):**
- Display: 40px / 1.2 / 700
- H1: 32px / 1.2 / 700
- H2: 24px / 1.3 / 600
- H3: 20px / 1.4 / 600
- Body Large: 16px / 1.6 / 400
- Body: 14px / 1.5 / 400

### Spacing System
**Base Unit:** 4px
**Scale:** 8px increments (4, 8, 16, 24, 32, 40, 48, 64, 80, 96, 128)

**Spacing Tokens:**
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px

**Component Padding:**
- Button: 12px / 24px
- Input: 12px / 16px
- Card: 24px
- Modal: 32px
- Section: 48px (mobile) / 96px (desktop)

## Section 2: Component Standards

### Buttons
**Primary Button:**
- Height: 44px (touch-friendly)
- Padding: 12px / 24px
- Border Radius: 8px
- Font: 16px / 600
- Colors: #0066FF (bg) / #FFFFFF (text) / none (border)
- States: Default, Hover (opacity 0.9), Active (opacity 0.95), Disabled (opacity 0.5)

**Secondary Button:**
- Same dimensions as Primary
- Colors: transparent (bg) / #0066FF (text) / #0066FF (1px border)
- Hover: light blue background (#F0F7FF)

### Cards
**Card:**
- Padding: 24px
- Border: 1px solid #E5E7EB
- Border Radius: 8px
- Shadow: 0 1px 3px rgba(0, 0, 0, 0.1)
- Background: #FFFFFF

## Section 3: Responsive Design

### Breakpoint Strategy
**Mobile First Approach:**
- Base styles: 375px (mobile)
- Tablet: @media (min-width: 768px)
- Desktop: @media (min-width: 1024px)
- Large Desktop: @media (min-width: 1440px)

**Responsive Behaviors:**
- Navigation: Bottom tabs → sidebar (768px+)
- Grid: 1 column → 2 columns (768px+) → 3 columns (1024px+)
- Typography: 85% of desktop sizes on mobile
- Spacing: 50-75% compression on mobile (48px → 24px)

### Touch Targets
**Minimum Touch Target:** 44x44px (iOS) / 48x48px (Android)
**Spacing Between Targets:** 8px minimum

## Section 4: Accessibility Requirements

### WCAG Compliance Level
**Target:** AA

### Color Contrast
**Body Text (16px):**
- Minimum Ratio: 4.5:1
- Target: 7:1 (AAA)

**Large Text (24px+):**
- Minimum Ratio: 3:1
- Target: 4.5:1 (AAA)

### Keyboard Navigation
**Requirements:**
- All interactive elements must be keyboard accessible
- Visible focus indicators (2px outline, high contrast)
- Logical tab order follows visual flow
- No keyboard traps

## Section 5: Performance Targets

### Core Web Vitals
**First Contentful Paint (FCP):**
- Target: <1.5 seconds
- Acceptable: <2.5 seconds

**Largest Contentful Paint (LCP):**
- Target: <2.0 seconds
- Acceptable: <2.5 seconds

**Cumulative Layout Shift (CLS):**
- Target: <0.1
- Acceptable: <0.25

### Lighthouse Scores
**Target:**
- Performance: 90+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 90+

## Section 6: Quality Score Breakdown

**Brand Compliance (25 points):**
- Color palette adherence: 10 pts
- Typography consistency: 10 pts
- Spacing system usage: 5 pts

**Responsive Design (20 points):**
- All breakpoints functional: 10 pts
- Touch targets meet minimums: 5 pts
- Content reflows properly: 5 pts

**Accessibility (25 points):**
- Color contrast passing: 10 pts
- Keyboard navigation working: 10 pts
- Screen reader support: 5 pts

**Performance (15 points):**
- Core Web Vitals passing: 10 pts
- Bundle size under target: 5 pts

**Visual Polish (15 points):**
- All interaction states present: 5 pts
- Empty/error states designed: 5 pts
- Loading indicators present: 5 pts

**Total: 100 points**
**Acceptance Threshold: 85+ points**
