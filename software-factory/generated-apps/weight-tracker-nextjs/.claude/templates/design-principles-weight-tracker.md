# Design Principles - Weight Tracker App
## Health & Fitness Dashboard Application

## Section 1: Brand Foundation

### Color System
**Primary Colors (Google-Inspired):**
- Brand Primary: #4285F4 (Google Blue) - Usage: CTAs, headers, primary actions
- Success: #0F9D58 (Google Green) - Usage: positive trends, weight loss indicators
- Secondary: #FBBC04 (Google Yellow) - Usage: warnings, neutral indicators
- Error: #EF4444 (Red) - Usage: weight gain indicators, errors

**Neutral Palette:**
- Background: #F9FAFB (gray-50)
- Surface: #FFFFFF
- Border: #E5E7EB (gray-200)
- Text Primary: #111827 (gray-900)
- Text Secondary: #6C757D (gray-600)
- Text Tertiary: #9CA3AF (gray-400)

**Chart Colors:**
- Chart Primary: #4285F4 (Blue)
- Chart Secondary: #0F9D58 (Green)
- Chart Accent: #FBBC04 (Yellow)
- Chart Gradient: Blue → Green for progress indicators

**Tint Colors:**
- Tint Blue: #E3F2FD
- Tint Green: #E6F4EA
- Tint Yellow: #FEEFC3

**Validation Rules:**
- All text must meet WCAG AA contrast requirements (4.5:1)
- Use semantic colors appropriately (green for loss, red for gain)
- Progress bars use full-spectrum gradient (red → yellow → green)

### Typography System
**Font Families:**
- Heading Font: Poppins (600 SemiBold)
  - Fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif
- Body Font: Nunito (400 Regular, 500 Medium, 600 SemiBold)
  - Fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif

**Type Scale (Desktop):**
- h1: 36px / 1.2 / 600 (Poppins)
- h2: 28px / 1.3 / 600 (Poppins)
- h3: 24px / 1.4 / 600 (Poppins)
- Body Large: 18px / 1.6 / 400 (Nunito)
- Body: 16px / 1.5 / 400 (Nunito)
- Label: 14px / 1.5 / 500 (Nunito)
- Small: 12px / 1.5 / 400 (Nunito)

**Type Scale (Mobile):**
- h1: 32px / 1.2 / 600
- h2: 24px / 1.3 / 600
- h3: 20px / 1.4 / 600
- Body Large: 16px / 1.6 / 400
- Body: 14px / 1.5 / 400

### Spacing System
**Base Unit:** 4px
**Scale:** 4px, 8px, 12px, 16px, 20px, 24px, 32px, 40px, 48px

**Spacing Tokens:**
- xs: 4px
- sm: 8px
- md: 12px
- lg: 16px
- xl: 20px
- 2xl: 24px
- 3xl: 32px
- 4xl: 40px
- 5xl: 48px

**Component Padding:**
- Button: 12px / 24px (vertical / horizontal)
- Card: 24px
- Card Compact: 16px
- Page Container: 24px (mobile) / 32px (desktop)
- Section: 24px vertical spacing

### Border Radius System
- sm: 4px
- md: 8px
- lg: 12px
- xl: 16px
- 2xl: 20px
- full: 9999px (pills)

## Section 2: Component Standards

### PillButton Component
**Variants:**
1. **Primary Button:**
   - Background: Linear gradient (primary → success)
   - Text: White (#FFFFFF)
   - Padding: 12px / 24px
   - Border Radius: full (9999px)
   - Font: 16px / 600 (Nunito)
   - Shadow: 0 4px 12px rgba(66, 133, 244, 0.3)
   - States: Default, Hover (scale 1.02), Active, Disabled (opacity 0.5)

2. **Secondary Button:**
   - Background: transparent
   - Border: 2px solid primary (#4285F4)
   - Text: Primary color
   - Same dimensions as Primary
   - Hover: Light blue background (#E3F2FD)

3. **Tertiary Button:**
   - Background: gray-100
   - Border: none
   - Text: gray-700
   - Hover: gray-200 background

4. **Accent Buttons:**
   - Success: Green background for positive actions
   - Danger: Red background for destructive actions

### MetricCard Component
**Variants:**
1. **Default Card:**
   - Background: White
   - Border: 1px solid gray-200
   - Border Radius: 12px
   - Padding: 24px
   - Shadow: 0 1px 3px rgba(0, 0, 0, 0.1)

2. **Summary Card:**
   - Background: Linear gradient tint (blue-to-tint)
   - No border
   - Enhanced shadow: 0 4px 12px rgba(66, 133, 244, 0.2)

3. **Chart Card:**
   - Background: Linear gradient tint (blue-to-green-tint)
   - Increased padding: 32px
   - Chart-specific spacing

4. **Compact Card:**
   - Reduced padding: 16px
   - Smaller font sizes
   - Used in grid layouts

### Progress Bar
**Full-Spectrum Gradient Progress:**
- Track: gray-200 background
- Fill: Full-spectrum gradient (red → amber → lime → green)
- Height: 16px (desktop) / 12px (mobile)
- Border Radius: full
- Runner Emoji: 🏃 positioned at progress point
- Animation: Bounce animation on runner

**Color Stops:**
- 0-25%: Red (#DC2626)
- 25-50%: Amber (#F59E0B)
- 50-75%: Lime (#84CC16)
- 75-100%: Green (#22C55E)

### Input Fields
**Text Input:**
- Height: 44px (touch-friendly)
- Padding: 12px / 16px
- Border: 2px solid gray-300
- Border Radius: 8px
- Font: 16px / 400 (Nunito)
- Focus: 3px blue ring (#4285F4)

### Cards & Lists
**Card List:**
- Gap between items: 12px
- Each card: white background, 1px border
- Hover state: subtle shadow increase

**History Card:**
- Weight delta badge (green for loss, red for gain)
- Date formatting: "Oct 15, 2025"
- Trend indicator with color coding

## Section 3: Responsive Design

### Breakpoint Strategy
**Mobile First Approach:**
- Base styles: 375px (mobile)
- Tablet: @media (min-width: 768px)
- Desktop: @media (min-width: 1024px)

**Responsive Behaviors:**
- Grid: 1 column → 2 columns (768px+) → 4 columns (1024px+)
- Typography: Mobile scale → Desktop scale at 768px+
- Spacing: 16-24px mobile → 24-32px desktop
- Charts: Full width mobile → contained desktop

### Touch Targets
**Minimum Touch Target:** 44x44px
**Button Minimum:** 44px height, 100px width
**Icon Buttons:** 44x44px minimum

## Section 4: Accessibility Requirements

### WCAG Compliance Level
**Target:** AA
**Minimum:** AA for all text and interactive elements

### Color Contrast
**Body Text (16px):**
- Minimum Ratio: 4.5:1
- Actual: 7:1+ (gray-900 on white)

**Large Text (24px+):**
- Minimum Ratio: 3:1
- Actual: 4.5:1+

**Interactive Elements:**
- Button text: 4.5:1 minimum
- Focus indicators: 3:1 minimum

### Keyboard Navigation
**Requirements:**
- All buttons keyboard accessible
- Visible focus indicators (3px blue ring)
- Logical tab order
- No keyboard traps
- Skip navigation for screen readers

### Screen Reader Support
- Semantic HTML (h1, h2, section, article)
- ARIA labels on icon-only buttons
- Alt text on all images
- Form labels properly associated

## Section 5: Dashboard-Specific Requirements

### Header Component
**Today's Summary Header:**
- Gradient background: primary → success
- White text with shadow for readability
- Responsive padding: 24px mobile / 32px desktop
- Contains: Date, greeting, current stats

### Metrics Display
**Key Metrics:**
- Current Weight (large, prominent)
- Body Fat % (secondary emphasis)
- Weekly Loss (with trend indicator)
- Days to Goal (motivational)

**12-Week Progress:**
- 4-metric grid (2x2 mobile, 4x1 desktop)
- Each metric: Label, value, unit
- Color-coded based on progress

### Charts
**30-Day Weight Trend:**
- Line chart with Recharts
- Chart height: 300px
- Grid styling: subtle gray lines
- Tooltip: Custom with weight data
- Axis labels: dates and weight values
- Colors: Primary blue line, tint background

### Navigation
**Screen Tabs:**
- Dashboard, Log, History, Analytics, Settings
- Active state: Primary color
- Inactive state: Gray
- Underline indicator on active tab

## Section 6: Performance Targets

### Core Web Vitals
**Largest Contentful Paint (LCP):**
- Target: <2.0 seconds
- Acceptable: <2.5 seconds

**First Input Delay (FID):**
- Target: <100ms
- Acceptable: <300ms

**Cumulative Layout Shift (CLS):**
- Target: <0.1
- Acceptable: <0.25

### Bundle Size
**Target:**
- Initial JS bundle: <200KB gzipped
- Total page weight: <1MB
- Images: Optimized WebP/AVIF

### Lighthouse Scores
**Target:**
- Performance: 90+
- Accessibility: 95+
- Best Practices: 95+
- SEO: 90+

## Section 7: Quality Score Breakdown

**Brand Compliance (25 points):**
- Color palette adherence: 10 pts
- Typography consistency: 10 pts
- Spacing system usage: 5 pts

**Responsive Design (20 points):**
- All breakpoints functional: 10 pts
- Touch targets meet minimums: 5 pts
- Charts responsive: 5 pts

**Accessibility (25 points):**
- Color contrast passing: 10 pts
- Keyboard navigation working: 10 pts
- Screen reader support: 5 pts

**Performance (15 points):**
- Page load under 2s: 10 pts
- No console errors: 5 pts

**Visual Polish (15 points):**
- All screens have H1: 5 pts
- Interactive states present: 5 pts
- Progress indicators working: 5 pts

**Total: 100 points**
**Acceptance Threshold: 85+ points**

## Section 8: Screen-Specific Guidelines

### Dashboard Screen
- Must have clear date/time
- Current weight prominently displayed
- 30-day chart visible
- Progress bar with runner animation
- All metrics loaded without errors

### Log Entry Screen
- Quick entry buttons functional
- Form validation working
- Success feedback after entry
- Loading state during save

### History Screen
- Search functionality working
- List items properly formatted
- Delete confirmation working
- Empty state if no entries

### Analytics Screen
- Multiple chart types
- Trend analysis visible
- No chart rendering errors
- Responsive chart sizing

### Settings Screen
- All settings accessible
- Toggle switches functional
- Save confirmation
- Clear visual feedback

## Section 9: Animation & Motion

### Animation Tokens
**Duration:**
- fast: 200ms
- normal: 300ms
- slow: 500ms

**Easing:**
- easeOut: cubic-bezier(0, 0, 0.2, 1)
- easeInOut: cubic-bezier(0.4, 0, 0.2, 1)

### Progress Runner Animation
**@keyframes run:**
- Bounce effect: translateY variation
- Duration: 1.2s
- Infinite loop
- Smooth transitions

### Button Hover
- Scale: 1.02
- Duration: 200ms
- Ease: easeOut

## Section 10: Data Visualization Standards

### Recharts Configuration
**Line Chart:**
- Stroke width: 2px
- Stroke color: Primary blue
- Dot size: 4px
- Grid: subtle gray
- Tooltip: custom styled

**Area under line:**
- Fill: tint-blue with opacity
- Smooth curve enabled

**Axes:**
- X-axis: dates, rotated for readability
- Y-axis: weight values with unit label
- Font: 12px Nunito

---

**This design system ensures:**
✅ Visual consistency across all screens
✅ Accessibility compliance (WCAG AA)
✅ Responsive design for all devices
✅ Performance optimization
✅ Brand alignment with Google-inspired palette
✅ Smooth animations and interactions

**Last Updated**: October 23, 2025
**Version**: 1.0
**Status**: Production
