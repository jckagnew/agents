# Landing Page Component Specifications

**Purpose:** Technical specifications for 15 landing page components for the Design-First Software Factory
**For:** Codex (Implementation)
**Validation:** Agent-in-the-loop visual comparison against Stitch references

---

## Architecture Overview

### Workflow
1. **Reference Design**: Create/import design in Stitch (manual or automated)
2. **Code Generation**: Codex implements component per these specs
3. **Validation**: Agent compares rendered output to Stitch reference
4. **Iteration**: Agent provides feedback, Codex adjusts, repeat until pixel-perfect

### File Structure
```
src/
  components/
    landing-page/
      heroes/
        HeroSplit.tsx
        HeroCentered.tsx
        HeroMinimal.tsx
        HeroVideo.tsx
      value-props/
        ValuePropBento.tsx
        ValuePropCards.tsx
        ValuePropList.tsx
        ValuePropComparison.tsx
      social-proof/
        SocialProofTestimonials.tsx
        SocialProofLogos.tsx
        SocialProofMetrics.tsx
        SocialProofCases.tsx
      ctas/
        CTAPrimary.tsx
        CTASecondary.tsx
        CTAEmailCapture.tsx
```

---

## Hero Components (4)

### 1. HeroSplit

**Purpose:** Above-the-fold section with image/content split layout

**Props Interface:**
```typescript
interface HeroSplitProps {
  headline: string;
  subheadline: string;
  ctaPrimary: {
    text: string;
    onPress: () => void;
    ariaLabel?: string;
  };
  ctaSecondary?: {
    text: string;
    onPress: () => void;
    ariaLabel?: string;
  };
  image: {
    uri: string;
    alt: string;
    aspectRatio?: number;
  };
  imagePosition?: 'left' | 'right';
  backgroundColor?: string;
}
```

**Layout Specifications:**

| Breakpoint | Layout | Image Position | Content Padding |
|------------|--------|----------------|-----------------|
| Mobile (≤375px) | Vertical stack | Top | spacing.xl |
| Tablet (768px) | 50/50 horizontal | Left or Right | spacing['2xl'] |
| Desktop (≥1024px) | 60/40 horizontal | Left or Right | spacing['3xl'] |

**Design Token Usage:**
- Headline: `typography.fontSize.display.large`, `typography.fontWeight.bold`
- Subheadline: `typography.fontSize.body.large`, `colors.text.secondary`
- CTA Primary: `colors.primary.main`, `spacing.md` padding, `borderRadius.md`
- CTA Secondary: Outlined, `colors.primary.main` border, transparent background
- Spacing between elements: `spacing.lg`

**Accessibility Requirements:**
- Headline must use `accessibilityRole="header"` and `accessibilityLevel={1}`
- Image must have `accessibleLabel={image.alt}`
- CTA buttons minimum 44x44px (use `touchTargets.minimum`)
- Color contrast ≥ 4.5:1 for all text
- Focus visible on interactive elements

**Stitch Validation Criteria:**
```javascript
{
  "layout": {
    "mobile": "vertical-stack",
    "tablet": "50-50-split",
    "desktop": "60-40-split"
  },
  "spacing": {
    "headline-to-subheadline": "spacing.md",
    "subheadline-to-cta": "spacing.lg",
    "section-padding": "spacing.xl"
  },
  "visual": {
    "image-aspect-ratio": "16:9 or 4:3",
    "cta-prominence": "primary > secondary",
    "text-readability": "line-length < 70 chars"
  }
}
```

---

### 2. HeroCentered

**Purpose:** Centered hero with optional video background

**Props Interface:**
```typescript
interface HeroCenteredProps {
  headline: string;
  subheadline: string;
  ctaPrimary: {
    text: string;
    onPress: () => void;
  };
  backgroundType: 'color' | 'gradient' | 'video' | 'image';
  background: {
    color?: string;
    gradient?: string[];
    videoUri?: string;
    imageUri?: string;
  };
  overlay?: {
    enabled: boolean;
    color: string;
    opacity: number;
  };
  textAlign?: 'center' | 'left';
}
```

**Layout Specifications:**

| Breakpoint | Max Content Width | Vertical Position | Text Align |
|------------|-------------------|-------------------|------------|
| Mobile | 90% | Center | Center |
| Tablet | 640px | Center | Center |
| Desktop | 800px | Center | Center or Left |

**Design Token Usage:**
- Headline: `typography.fontSize.display.large`, `colors.text.inverse` (if dark background)
- Subheadline: `typography.fontSize.h3`, `colors.text.inverse` with `opacity.divider`
- CTA: `colors.primary.main`, `shadows.lg` for prominence
- Background overlay: `colors.surface.overlay` at `opacity.disabled`

**Accessibility Requirements:**
- If video background: must be muted, autoplay, loop, with pause button
- High contrast mode support (switch to solid background)
- Video alternative: static image fallback
- Keyboard navigation for CTA

**Stitch Validation Criteria:**
```javascript
{
  "layout": {
    "alignment": "center",
    "max-width": "800px",
    "vertical-center": true
  },
  "background": {
    "video-plays": true,
    "overlay-visible": true,
    "contrast-sufficient": "≥4.5:1"
  },
  "cta": {
    "prominence": "elevated-shadow",
    "size": "large",
    "position": "below-subheadline"
  }
}
```

---

### 3. HeroMinimal

**Purpose:** Text-only hero with gradient background

**Props Interface:**
```typescript
interface HeroMinimalProps {
  headline: string;
  subheadline?: string;
  badge?: {
    text: string;
    icon?: string;
  };
  ctaPrimary: {
    text: string;
    onPress: () => void;
  };
  gradient: {
    colors: string[];
    start: { x: number; y: number };
    end: { x: number; y: number };
  };
}
```

**Layout Specifications:**

| Breakpoint | Content Width | Vertical Padding | Headline Size |
|------------|---------------|------------------|---------------|
| Mobile | 90% | spacing['2xl'] | display.medium |
| Tablet | 70% | spacing['3xl'] | display.large |
| Desktop | 60% | spacing['4xl'] | display.large |

**Design Token Usage:**
- Badge: `typography.fontSize.caption`, `borderRadius.full`, `spacing.sm` padding
- Headline: `typography.fontSize.display.large`, `typography.lineHeight.tight`
- Gradient: Use two colors from `colors.primary` and `colors.secondary`
- CTA: Ghost style (transparent background, white text, white border)

**Accessibility Requirements:**
- Badge icon decorative only (hidden from screen readers)
- Sufficient contrast on gradient (test at lightest and darkest points)
- Focus ring visible on CTA

**Stitch Validation Criteria:**
```javascript
{
  "layout": {
    "text-only": true,
    "centered": true,
    "breathing-room": "ample-padding"
  },
  "visual": {
    "gradient-smooth": true,
    "headline-dominant": true,
    "cta-subtle": "ghost-style"
  }
}
```

---

### 4. HeroVideo

**Purpose:** Full-screen video with overlay text

**Props Interface:**
```typescript
interface HeroVideoProps {
  headline: string;
  subheadline: string;
  video: {
    uri: string;
    posterUri: string;
    alt: string;
  };
  controls?: {
    showPlayPause: boolean;
    showMute: boolean;
  };
  overlay: {
    color: string;
    opacity: number;
  };
  ctaPrimary: {
    text: string;
    onPress: () => void;
  };
}
```

**Layout Specifications:**

| Breakpoint | Video Aspect | Text Position | Controls |
|------------|--------------|---------------|----------|
| Mobile | 9:16 | Center | Minimal |
| Tablet | 16:9 | Center-left | Standard |
| Desktop | 16:9 | Left third | Full |

**Design Token Usage:**
- Video overlay: `colors.surface.overlay` at 40-60% opacity
- Headline: `typography.fontSize.display.large`, `colors.text.inverse`
- Controls: `colors.text.inverse`, `borderRadius.full`, `shadows.md`

**Accessibility Requirements:**
- Video must have captions/subtitles
- Pause button accessible via keyboard (Tab)
- Alternative static image on prefers-reduced-motion
- ARIA labels on all video controls

**Stitch Validation Criteria:**
```javascript
{
  "video": {
    "aspect-ratio": "16:9",
    "autoplay": true,
    "muted-default": true,
    "loop": true
  },
  "overlay": {
    "darkness": "40-60%",
    "text-readable": "≥4.5:1 contrast"
  },
  "controls": {
    "accessible": true,
    "prominent": "visible-on-hover"
  }
}
```

---

## Value Prop Components (4)

### 5. ValuePropBento

**Purpose:** Bento box grid layout showcasing 4-6 value propositions

**Props Interface:**
```typescript
interface ValuePropBentoProps {
  items: Array<{
    id: string;
    title: string;
    description: string;
    icon?: string;
    iconColor?: string;
    size?: 'small' | 'medium' | 'large';
  }>;
  layout?: '2x2' | '3x2' | '2x3';
  gap?: number;
  backgroundColor?: string;
}
```

**Layout Specifications:**

| Breakpoint | Grid | Gap | Min Item Height |
|------------|------|-----|-----------------|
| Mobile | 1 column | spacing.md | 120px |
| Tablet | 2x2 or 2x3 | spacing.lg | 160px |
| Desktop | 3x2 or flexible | spacing.xl | 200px |

**Design Token Usage:**
- Grid gap: `spacing.lg` to `spacing.xl`
- Item background: `colors.surface.elevated` with `shadows.md`
- Icon size: 32px (small), 48px (medium), 64px (large)
- Title: `typography.fontSize.h4`, `typography.fontWeight.semibold`
- Description: `typography.fontSize.body.medium`, `colors.text.secondary`

**Accessibility Requirements:**
- Each item must be individually focusable
- Icon colors meet contrast requirements
- Grid maintains logical tab order (left-to-right, top-to-bottom)

**Stitch Validation Criteria:**
```javascript
{
  "layout": {
    "grid-consistent": true,
    "gaps-uniform": true,
    "responsive-collapse": "mobile-single-column"
  },
  "items": {
    "visual-hierarchy": "icon > title > description",
    "background-elevated": true,
    "hover-state": "subtle-lift"
  }
}
```

---

### 6. ValuePropCards

**Purpose:** 3-4 icon cards in horizontal row

**Props Interface:**
```typescript
interface ValuePropCardsProps {
  cards: Array<{
    id: string;
    icon: string;
    title: string;
    description: string;
    iconBackground?: string;
  }>;
  columns?: 3 | 4;
  cardStyle?: 'filled' | 'outlined' | 'elevated';
}
```

**Layout Specifications:**

| Breakpoint | Columns | Card Width | Icon Position |
|------------|---------|------------|---------------|
| Mobile | 1 | 100% | Left or Top |
| Tablet | 2 | 50% | Top |
| Desktop | 3 or 4 | Equal | Top |

**Design Token Usage:**
- Card padding: `spacing.xl`
- Card border: `borderRadius.lg`, `colors.border.light` (outlined style)
- Card shadow: `shadows.md` (elevated style)
- Icon background: Circle with `borderRadius.full`, 64px diameter
- Icon color: `colors.primary.main` or custom
- Title: `typography.fontSize.h5`, center-aligned
- Description: `typography.fontSize.body.small`, center-aligned

**Accessibility Requirements:**
- Icon decorative (use `accessibilityLabel` on card, not icon)
- Card as single focusable unit
- Hover/focus states visible

**Stitch Validation Criteria:**
```javascript
{
  "layout": {
    "columns-equal": true,
    "responsive-stack": "mobile-vertical"
  },
  "cards": {
    "icon-prominent": "64px-circle",
    "text-centered": true,
    "spacing-consistent": true
  }
}
```

---

### 7. ValuePropList

**Purpose:** Vertical list with icon bullets

**Props Interface:**
```typescript
interface ValuePropListProps {
  items: Array<{
    id: string;
    icon: string;
    title: string;
    description: string;
  }>;
  iconStyle?: 'circle' | 'square' | 'none';
  dividers?: boolean;
  compact?: boolean;
}
```

**Layout Specifications:**

| Breakpoint | Max Width | Item Spacing | Icon Size |
|------------|-----------|--------------|-----------|
| Mobile | 100% | spacing.lg | 24px |
| Tablet | 640px | spacing.xl | 28px |
| Desktop | 800px | spacing.xl | 32px |

**Design Token Usage:**
- Icon background (if circle): `colors.primary.light`, 48px diameter
- Icon color: `colors.primary.main`
- Title: `typography.fontSize.h5`, `typography.fontWeight.medium`
- Description: `typography.fontSize.body.medium`, `colors.text.secondary`
- Divider (if enabled): `colors.border.light`, 1px height
- Spacing between items: `spacing.lg` (compact) or `spacing.xl` (default)

**Accessibility Requirements:**
- Each item is a list item (semantic HTML/RN equivalent)
- Icon does not convey meaning (title does)
- Keyboard navigation through list items

**Stitch Validation Criteria:**
```javascript
{
  "layout": {
    "vertical-list": true,
    "left-aligned": true,
    "max-width": "800px"
  },
  "items": {
    "icon-title-description": "horizontal-layout",
    "spacing-consistent": true,
    "dividers-subtle": "if-enabled"
  }
}
```

---

### 8. ValuePropComparison

**Purpose:** Before/After or Free/Pro comparison table

**Props Interface:**
```typescript
interface ValuePropComparisonProps {
  columns: Array<{
    id: string;
    label: string;
    highlighted?: boolean;
    badge?: string;
  }>;
  rows: Array<{
    id: string;
    feature: string;
    values: Array<boolean | string | number>;
  }>;
  comparisonType?: 'before-after' | 'tier-comparison';
}
```

**Layout Specifications:**

| Breakpoint | Display | Column Width | Row Height |
|------------|---------|--------------|------------|
| Mobile | Stacked cards | 100% | Auto |
| Tablet | 2-column table | 50% | 60px |
| Desktop | Full table | Equal | 72px |

**Design Token Usage:**
- Table border: `colors.border.light`
- Highlighted column: `colors.primary.light` background with 10% opacity
- Badge: `colors.primary.main`, `typography.fontSize.caption`, `borderRadius.sm`
- Feature text: `typography.fontSize.body.medium`
- Checkmarks/X: `colors.success` / `colors.error`, 20px size
- Row hover: `colors.background.secondary`

**Accessibility Requirements:**
- Proper table semantics (headers, rows, cells)
- Checkmark/X have text alternatives ("Included"/"Not included")
- Highlighted column has `aria-label="Recommended"`

**Stitch Validation Criteria:**
```javascript
{
  "table": {
    "columns-clear": true,
    "rows-scannable": true,
    "highlighted-prominent": "if-enabled"
  },
  "responsive": {
    "mobile-cards": true,
    "desktop-table": true
  },
  "visual": {
    "checkmarks-green": true,
    "x-marks-red": true,
    "hover-state": true
  }
}
```

---

## Social Proof Components (4)

### 9. SocialProofTestimonials

**Purpose:** Testimonial carousel with customer photos

**Props Interface:**
```typescript
interface SocialProofTestimonialsProps {
  testimonials: Array<{
    id: string;
    quote: string;
    author: {
      name: string;
      title: string;
      company: string;
      avatarUri: string;
    };
    rating?: number;
  }>;
  layout?: 'carousel' | 'grid';
  autoplay?: boolean;
  autoplayInterval?: number;
}
```

**Layout Specifications:**

| Breakpoint | Display | Items Visible | Navigation |
|------------|---------|---------------|------------|
| Mobile | Carousel | 1 | Dots |
| Tablet | Carousel | 2 | Dots + Arrows |
| Desktop | Grid or Carousel | 3 | Arrows |

**Design Token Usage:**
- Quote text: `typography.fontSize.h5`, `typography.lineHeight.relaxed`
- Author name: `typography.fontSize.body.medium`, `typography.fontWeight.semibold`
- Author title: `typography.fontSize.body.small`, `colors.text.secondary`
- Avatar: 56px circle, `borderRadius.full`, `shadows.sm`
- Card background: `colors.surface.elevated`, `shadows.md`, `borderRadius.lg`
- Card padding: `spacing.xl`
- Rating stars: `colors.warning` (gold)

**Accessibility Requirements:**
- Carousel controls keyboard accessible (arrow keys)
- Autoplay pausable
- Current slide announced to screen readers
- Avatar images have alt text

**Stitch Validation Criteria:**
```javascript
{
  "testimonials": {
    "quote-prominent": true,
    "author-credible": "photo-name-title",
    "visual-hierarchy": "quote > author"
  },
  "carousel": {
    "navigation-clear": true,
    "transition-smooth": "animation.duration.normal",
    "controls-accessible": true
  }
}
```

---

### 10. SocialProofLogos

**Purpose:** Grid of client/partner logos

**Props Interface:**
```typescript
interface SocialProofLogosProps {
  logos: Array<{
    id: string;
    imageUri: string;
    companyName: string;
    websiteUrl?: string;
  }>;
  columns?: number;
  grayscale?: boolean;
  heading?: string;
}
```

**Layout Specifications:**

| Breakpoint | Columns | Logo Size | Spacing |
|------------|---------|-----------|---------|
| Mobile | 2 | 80px width | spacing.md |
| Tablet | 4 | 100px width | spacing.lg |
| Desktop | 5-6 | 120px width | spacing.xl |

**Design Token Usage:**
- Heading: `typography.fontSize.h4`, `typography.fontWeight.semibold`, center
- Logo container: 120px × 80px, `colors.background.secondary` background
- Logo filter: grayscale(100%) with opacity.disabled (if grayscale mode)
- Logo hover: grayscale(0%) with full opacity
- Grid gap: `spacing.lg`

**Accessibility Requirements:**
- Each logo has alt text with company name
- If clickable, links have accessible labels
- Grayscale logos still have sufficient contrast with background

**Stitch Validation Criteria:**
```javascript
{
  "layout": {
    "grid-centered": true,
    "columns-consistent": true,
    "responsive-collapse": "fewer-columns-mobile"
  },
  "logos": {
    "uniform-size": true,
    "grayscale-default": "if-enabled",
    "color-on-hover": true
  }
}
```

---

### 11. SocialProofMetrics

**Purpose:** Animated counter bar with key statistics

**Props Interface:**
```typescript
interface SocialProofMetricsProps {
  metrics: Array<{
    id: string;
    value: number;
    label: string;
    suffix?: string;
    prefix?: string;
    icon?: string;
  }>;
  animateOnScroll?: boolean;
  duration?: number;
}
```

**Layout Specifications:**

| Breakpoint | Layout | Metric Width | Font Size |
|------------|--------|--------------|-----------|
| Mobile | Vertical | 100% | display.medium |
| Tablet | 2x2 grid | 50% | display.large |
| Desktop | Horizontal | Equal | display.large |

**Design Token Usage:**
- Value: `typography.fontSize.display.large`, `typography.fontWeight.bold`, `colors.primary.main`
- Label: `typography.fontSize.body.large`, `colors.text.secondary`
- Icon (optional): 32px, `colors.primary.main`
- Divider (between metrics): `colors.border.light`, 1px vertical
- Animation: `animation.duration.slow`, `animation.easing.easeOut`

**Accessibility Requirements:**
- Counter animation respects prefers-reduced-motion
- Final values visible even if animation disabled
- Metrics have semantic meaning (not just decorative)

**Stitch Validation Criteria:**
```javascript
{
  "metrics": {
    "value-prominent": true,
    "label-clear": true,
    "spacing-balanced": true
  },
  "animation": {
    "counter-animates": "if-enabled",
    "duration-appropriate": "animation.duration.slow",
    "reduced-motion-respected": true
  }
}
```

---

### 12. SocialProofCases

**Purpose:** Case study cards with results

**Props Interface:**
```typescript
interface SocialProofCasesProps {
  cases: Array<{
    id: string;
    companyName: string;
    industry: string;
    challenge: string;
    result: string;
    metrics: Array<{
      value: string;
      label: string;
    }>;
    logoUri?: string;
    imageUri?: string;
  }>;
  layout?: 'cards' | 'list';
  readMoreAction?: (caseId: string) => void;
}
```

**Layout Specifications:**

| Breakpoint | Display | Card Width | Image Position |
|------------|---------|------------|----------------|
| Mobile | Vertical list | 100% | Top |
| Tablet | 2-column grid | 50% | Left |
| Desktop | 3-column grid | 33% | Left |

**Design Token Usage:**
- Card background: `colors.surface.elevated`, `shadows.md`
- Card border: `borderRadius.xl`
- Card padding: `spacing.xl`
- Company name: `typography.fontSize.h4`, `typography.fontWeight.semibold`
- Industry: `typography.fontSize.caption`, `colors.text.tertiary`, uppercase
- Challenge/Result: `typography.fontSize.body.medium`, `typography.lineHeight.relaxed`
- Metric value: `typography.fontSize.h3`, `typography.fontWeight.bold`, `colors.primary.main`
- Metric label: `typography.fontSize.body.small`, `colors.text.secondary`
- "Read More" link: `colors.primary.main`, underline on hover

**Accessibility Requirements:**
- Card as single focusable unit or multiple focusable elements within
- Image decorative (information in text)
- "Read More" action keyboard accessible

**Stitch Validation Criteria:**
```javascript
{
  "cards": {
    "visual-hierarchy": "company > challenge > result > metrics",
    "image-supporting": true,
    "elevated": "shadow-visible"
  },
  "metrics": {
    "prominent": "large-font",
    "scannable": "value-above-label"
  }
}
```

---

## CTA Components (3)

### 13. CTAPrimary

**Purpose:** Primary call-to-action button

**Props Interface:**
```typescript
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
```

**Layout Specifications:**

| Size | Min Height | Padding Horizontal | Font Size |
|------|------------|-------------------|-----------|
| Small | 36px | spacing.md | body.small |
| Medium | 44px | spacing.lg | body.medium |
| Large | 56px | spacing.xl | h5 |

**Design Token Usage:**
- Background: `colors.primary.main`
- Text: `colors.text.inverse`
- Border radius: `borderRadius.md` (small/medium), `borderRadius.lg` (large)
- Shadow: `shadows.sm` (default), `shadows.md` (hover), `shadows.none` (pressed)
- Icon size: 20px (small), 24px (medium), 28px (large)
- Loading spinner: `colors.text.inverse`, 20-24px
- Disabled: `opacity.disabled`
- Hover: Darken by 8% (`colors.primary.dark`)
- Active: Darken by 16%

**Accessibility Requirements:**
- Minimum touch target 44x44px (use `touchTargets.minimum`)
- Focus ring visible (2px `colors.primary.main` outline with 2px offset)
- Disabled state communicated to screen readers
- Loading state announced

**Stitch Validation Criteria:**
```javascript
{
  "button": {
    "min-height": "44px",
    "prominent": "primary-color",
    "rounded": "borderRadius.md-lg"
  },
  "states": {
    "default": "primary-color",
    "hover": "darker-8%",
    "active": "darker-16%",
    "disabled": "opacity-38%",
    "loading": "spinner-visible"
  },
  "accessibility": {
    "touch-target": "≥44px",
    "focus-visible": true
  }
}
```

---

### 14. CTASecondary

**Purpose:** Secondary call-to-action button (outlined style)

**Props Interface:**
```typescript
interface CTASecondaryProps {
  text: string;
  onPress: () => void;
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;
  disabled?: boolean;
  icon?: string;
  iconPosition?: 'left' | 'right';
}
```

**Layout Specifications:**
Same as CTAPrimary

**Design Token Usage:**
- Background: Transparent
- Border: 2px solid `colors.primary.main`
- Text: `colors.primary.main`
- Border radius: `borderRadius.md` (small/medium), `borderRadius.lg` (large)
- Shadow: None (default), `shadows.sm` (hover)
- Hover: Background `colors.primary.main` with `opacity.hover`, text `colors.text.inverse`
- Active: Background `colors.primary.main` with `opacity.selected`
- Disabled: Border and text at `opacity.disabled`

**Accessibility Requirements:**
Same as CTAPrimary

**Stitch Validation Criteria:**
```javascript
{
  "button": {
    "min-height": "44px",
    "outlined": "2px-border",
    "transparent-background": true
  },
  "states": {
    "default": "transparent-outlined",
    "hover": "filled-background",
    "active": "filled-background-selected",
    "disabled": "opacity-38%"
  }
}
```

---

### 15. CTAEmailCapture

**Purpose:** Email input with inline CTA button

**Props Interface:**
```typescript
interface CTAEmailCaptureProps {
  placeholder?: string;
  buttonText?: string;
  onSubmit: (email: string) => void;
  validation?: {
    required?: boolean;
    pattern?: RegExp;
  };
  size?: 'medium' | 'large';
  layout?: 'inline' | 'stacked';
  helpText?: string;
  errorText?: string;
}
```

**Layout Specifications:**

| Breakpoint | Layout | Input Width | Button Width |
|------------|--------|-------------|--------------|
| Mobile | Stacked | 100% | 100% |
| Tablet | Inline | 60% | 40% |
| Desktop | Inline | 70% | 30% |

**Design Token Usage:**
- Container: Flexbox row (inline) or column (stacked), `spacing.sm` gap
- Input background: `colors.background.primary`
- Input border: 2px `colors.border.medium`, `borderRadius.md`
- Input text: `typography.fontSize.body.medium`, `colors.text.primary`
- Input padding: `spacing.md` vertical, `spacing.lg` horizontal
- Input focus: Border `colors.primary.main`, `shadows.sm`
- Button: Same as CTAPrimary
- Help text: `typography.fontSize.caption`, `colors.text.secondary`
- Error text: `typography.fontSize.caption`, `colors.error`

**Accessibility Requirements:**
- Input has `accessibilityLabel="Email address"`
- Input has `keyboardType="email-address"`
- Input has `autoCompleteType="email"`
- Error announced to screen readers on validation fail
- Focus management (move to button after valid input)
- ARIA labels link input and error message

**Stitch Validation Criteria:**
```javascript
{
  "layout": {
    "responsive": "stacked-mobile-inline-desktop",
    "input-prominent": "70%-width-desktop"
  },
  "input": {
    "border-visible": "2px",
    "focus-state": "primary-color-border",
    "placeholder-readable": "contrast-sufficient"
  },
  "validation": {
    "error-visible": "red-text-below",
    "error-announced": "screen-reader"
  }
}
```

---

## Testing Requirements

### Visual Validation (Agent-in-the-Loop)

For each component, the validation agent will:

1. **Screenshot Comparison**
   - Capture rendered component at 375px, 768px, 1440px
   - Compare to Stitch reference designs
   - Calculate pixel difference percentage
   - Flag differences > 2% for review

2. **Layout Validation**
   - Verify responsive breakpoints match specs
   - Verify spacing using design tokens
   - Verify alignment and positioning

3. **Accessibility Validation**
   - Run axe-core or similar tool
   - Verify color contrast ratios
   - Verify touch target sizes
   - Verify ARIA labels and roles

4. **Interactive State Validation**
   - Capture hover states
   - Capture focus states
   - Capture disabled states
   - Verify state transitions

### Acceptance Criteria

Each component passes when:
- ✅ Visual match to Stitch reference ≥ 98%
- ✅ All responsive breakpoints correct
- ✅ All accessibility checks pass
- ✅ All interactive states match specs
- ✅ Performance: Time to Interactive < 1s

---

## Implementation Priority

### Phase 1 (Week 1): Foundation
1. CTAPrimary
2. CTASecondary
3. HeroSplit

### Phase 2 (Week 1-2): Core Sections
4. HeroCentered
5. ValuePropCards
6. SocialProofLogos

### Phase 3 (Week 2): Advanced
7. HeroMinimal
8. ValuePropBento
9. SocialProofTestimonials
10. CTAEmailCapture

### Phase 4 (Week 3): Specialty
11. HeroVideo
12. ValuePropList
13. ValuePropComparison
14. SocialProofMetrics
15. SocialProofCases

---

## Next Steps for Codex

1. **Create Stitch references** for Phase 1 components (or use provided)
2. **Implement CTAPrimary** following spec
3. **Test with validation agent** - get feedback
4. **Iterate until 98%+ match**
5. **Repeat for remaining components**

All design tokens are available in `/src/constants/design-tokens.ts`
