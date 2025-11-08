# Landing Page Implementation Guide for Codex

**Status:** Ready to implement ✅
**Gemini Deliverables:** Complete (Claude stepped in)
**Your Role:** Implement 15 landing page components
**Timeline:** ~2 weeks (prioritized implementation schedule provided)

---

## ✅ What's Been Delivered for You

### 1. Platform-Aware Design Tokens
**File:** `/src/constants/design-tokens.ts`

Complete design system with:
- ✅ Colors (iOS HIG, Material Design, Web-optimized)
- ✅ Typography (platform-specific font sizes)
- ✅ Spacing system (4px base unit)
- ✅ Border radius, shadows, animations
- ✅ Breakpoints for responsive design
- ✅ Accessibility specifications (touch targets, contrast ratios)

**Usage:**
```typescript
import { colors, typography, spacing, borderRadius } from './constants/design-tokens';

<View style={{
  backgroundColor: colors.primary.main,
  padding: spacing.xl,
  borderRadius: borderRadius.lg,
}}>
  <Text style={{
    fontSize: typography.fontSize.h1,
    fontWeight: typography.fontWeight.bold,
  }}>
    Hello World
  </Text>
</View>
```

---

### 2. Component Specifications
**File:** `/docs/LANDING_PAGE_COMPONENT_SPECS.md` (27 pages)

Detailed specs for all 15 components:
- **4 Hero Components:** HeroSplit, HeroCentered, HeroMinimal, HeroVideo
- **4 Value Props:** ValuePropBento, ValuePropCards, ValuePropList, ValuePropComparison
- **4 Social Proof:** Testimonials, Logos, Metrics, Cases
- **3 CTAs:** CTAPrimary, CTASecondary, CTAEmailCapture

Each spec includes:
- ✅ TypeScript Props interface
- ✅ Layout specifications (mobile/tablet/desktop breakpoints)
- ✅ Design token usage
- ✅ Accessibility requirements
- ✅ Stitch validation criteria (for agent-in-the-loop testing)

---

### 3. Conversion-Optimized Copy
**File:** `/docs/LANDING_PAGE_COPY_VARIATIONS.md` (22 pages)

45+ copy variations with conversion scores:
- ✅ 5 hero variations (scored 7.5-9.2/10)
- ✅ 12 value prop variations
- ✅ 3 complete testimonials
- ✅ 2 metric sets
- ✅ 3 detailed case studies
- ✅ 12 CTA variations
- ✅ Recommended A/B tests

---

## 🎯 Your Implementation Plan

### Phase 1 (Days 1-3): Foundation Components

**Priority 1: CTAPrimary** (Day 1)
- Spec: `/docs/LANDING_PAGE_COMPONENT_SPECS.md` (Line 745)
- Copy: Use CTA Variation 1 ("Start Free Project")
- File: `/src/components/landing-page/ctas/CTAPrimary.tsx`

**Priority 2: CTASecondary** (Day 1)
- Spec: `/docs/LANDING_PAGE_COMPONENT_SPECS.md` (Line 819)
- Copy: Use Secondary CTA Variation 1 ("Watch 2-Min Demo")
- File: `/src/components/landing-page/ctas/CTASecondary.tsx`

**Priority 3: HeroSplit** (Days 2-3)
- Spec: `/docs/LANDING_PAGE_COMPONENT_SPECS.md` (Line 67)
- Copy: Use Hero Variation 1 (Score 9.2/10)
- File: `/src/components/landing-page/heroes/HeroSplit.tsx`
- **Dependencies:** CTAPrimary, CTASecondary (build these first)

**Validation Checkpoint:**
- Create Stitch reference designs for these 3 components
- Render components at 375px, 768px, 1440px
- Run agent-in-the-loop validation
- Iterate until 98%+ visual match

---

### Phase 2 (Days 4-7): Core Landing Sections

**Priority 4: HeroCentered** (Days 4-5)
- Spec: Line 144
- Copy: Hero Variation 2 or 4
- File: `/src/components/landing-page/heroes/HeroCentered.tsx`

**Priority 5: ValuePropCards** (Days 5-6)
- Spec: Line 349
- Copy: Value Prop Section 1 variations
- File: `/src/components/landing-page/value-props/ValuePropCards.tsx`

**Priority 6: SocialProofLogos** (Day 7)
- Spec: Line 520
- Copy: Logo Section Heading Variation 4
- File: `/src/components/landing-page/social-proof/SocialProofLogos.tsx`

---

### Phase 3 (Days 8-11): Advanced Components

**Priority 7: HeroMinimal** (Day 8)
- Spec: Line 220
- File: `/src/components/landing-page/heroes/HeroMinimal.tsx`

**Priority 8: ValuePropBento** (Days 8-9)
- Spec: Line 301
- Copy: Value Prop Section 1-4 (mix and match)
- File: `/src/components/landing-page/value-props/ValuePropBento.tsx`

**Priority 9: SocialProofTestimonials** (Days 10-11)
- Spec: Line 447
- Copy: All 3 testimonials provided
- File: `/src/components/landing-page/social-proof/SocialProofTestimonials.tsx`

**Priority 10: CTAEmailCapture** (Day 11)
- Spec: Line 869
- Copy: Email Capture Variation 2 (Lead Magnet)
- File: `/src/components/landing-page/ctas/CTAEmailCapture.tsx`

---

### Phase 4 (Days 12-14): Specialty Components

**Priority 11: HeroVideo** (Day 12)
- Spec: Line 280
- File: `/src/components/landing-page/heroes/HeroVideo.tsx`

**Priority 12: ValuePropList** (Day 12)
- Spec: Line 392
- File: `/src/components/landing-page/value-props/ValuePropList.tsx`

**Priority 13: ValuePropComparison** (Day 13)
- Spec: Line 432
- Copy: Express vs Concierge comparison table
- File: `/src/components/landing-page/value-props/ValuePropComparison.tsx`

**Priority 14: SocialProofMetrics** (Day 13)
- Spec: Line 580
- Copy: Metric Set A (Growth Focus)
- File: `/src/components/landing-page/social-proof/SocialProofMetrics.tsx`

**Priority 15: SocialProofCases** (Day 14)
- Spec: Line 632
- Copy: All 3 case studies provided
- File: `/src/components/landing-page/social-proof/SocialProofCases.tsx`

---

## 🔄 Agent-in-the-Loop Workflow

This is the CORRECT Stitch workflow (not API-based):

### Step 1: Create Stitch Reference Design

**Express Tier (Fully Automated):**
1. User provides prompt/requirements
2. AI generates single design in Stitch
3. AI proceeds immediately to code generation
4. Output: Complete app in 4-6 days

**Concierge Tier (Human-in-the-Loop Selection):**
1. User provides prompt/requirements
2. AI generates **3 design variations** in Stitch
3. **User selects winner** from the 3 options
4. AI proceeds to code generation with selected design
5. Output: Complete app in 2-3 weeks (extra time for selection + refinement)

**Both tiers use the same AI design generation process—Concierge just adds a selection step.**

### Step 2: Implement Component
- Follow spec in `LANDING_PAGE_COMPONENT_SPECS.md`
- Use design tokens from `design-tokens.ts`
- Use copy from `LANDING_PAGE_COPY_VARIATIONS.md`

### Step 3: Agent Validates
- Render your component at 375px, 768px, 1440px
- Agent compares screenshots to Stitch reference
- Agent calculates pixel-difference percentage
- Agent provides feedback: "Button padding off by 4px" etc.

### Step 4: Iterate
- Adjust code based on agent feedback
- Re-render and re-validate
- Repeat until agent reports ≥98% match

**No Stitch API required** - Just UI tool + agent orchestration!

---

## 📦 File Structure to Create

```
src/
  components/
    landing-page/
      heroes/
        HeroSplit.tsx          ← Priority 3
        HeroCentered.tsx       ← Priority 4
        HeroMinimal.tsx        ← Priority 7
        HeroVideo.tsx          ← Priority 11
      value-props/
        ValuePropBento.tsx     ← Priority 8
        ValuePropCards.tsx     ← Priority 5
        ValuePropList.tsx      ← Priority 12
        ValuePropComparison.tsx ← Priority 13
      social-proof/
        SocialProofTestimonials.tsx ← Priority 9
        SocialProofLogos.tsx        ← Priority 6
        SocialProofMetrics.tsx      ← Priority 14
        SocialProofCases.tsx        ← Priority 15
      ctas/
        CTAPrimary.tsx         ← Priority 1
        CTASecondary.tsx       ← Priority 2
        CTAEmailCapture.tsx    ← Priority 10

__tests__/
  landing-page/
    heroes/
      HeroSplit.test.tsx
      HeroSplit.visual.test.ts    (Playwright)
      HeroSplit.a11y.test.ts      (Accessibility)
    # ... same pattern for all components
```

---

## 🎨 Design Token Quick Reference

### Colors
```typescript
colors.primary.main      // Platform-aware blue/purple
colors.secondary.main    // Accent color
colors.text.primary      // Black/gray-900
colors.text.secondary    // Gray-500
colors.background.primary // White
colors.surface.elevated  // Card backgrounds
```

### Typography
```typescript
typography.fontSize.display.large  // 48-56px (platform-aware)
typography.fontSize.h1             // 34-36px
typography.fontSize.body.medium    // 16-17px
typography.fontWeight.bold         // 700
typography.lineHeight.relaxed      // 1.75
```

### Spacing
```typescript
spacing.xs   // 4px
spacing.sm   // 8px
spacing.md   // 12-16px (platform-aware)
spacing.lg   // 20-24px
spacing.xl   // 28-32px
spacing['2xl'] // 40-48px
```

### Responsive Breakpoints
```typescript
breakpoints.mobile   // 375px
breakpoints.tablet   // 768px
breakpoints.desktop  // 1024px
breakpoints.wide     // 1440px
```

---

## ✅ Acceptance Criteria

Each component must pass:
1. **Visual Validation:** ≥98% match to Stitch reference (agent-validated)
2. **Responsive:** Correct layout at 375px, 768px, 1440px
3. **Accessibility:**
   - Color contrast ≥4.5:1
   - Touch targets ≥44px
   - ARIA labels correct
   - Keyboard navigation works
4. **Performance:** Time to Interactive <1s
5. **Code Quality:**
   - TypeScript (no `any` types)
   - ESLint clean
   - Follows spec exactly

---

## 🚀 Getting Started (Day 1)

### Morning
1. ✅ Read this README (you're here!)
2. ✅ Review `/src/constants/design-tokens.ts`
3. ✅ Skim `/docs/LANDING_PAGE_COMPONENT_SPECS.md`

### Afternoon
4. Create Stitch reference for CTAPrimary
5. Implement `/src/components/landing-page/ctas/CTAPrimary.tsx`
6. Test at all breakpoints
7. Run agent validation

### Evening
8. Iterate on CTAPrimary until 98%+ match
9. Create Stitch reference for CTASecondary
10. Start implementing CTASecondary

---

## 📞 Questions or Blockers?

If you need:
- **Clarification on specs:** Ask Claude (me) - I wrote them
- **Design decisions:** Check LANDING_PAGE_COPY_VARIATIONS.md for guidance
- **Stitch workflow help:** See "Agent-in-the-Loop Workflow" section above
- **Technical help:** Cursor can assist with debugging

---

## 🎯 Success Metrics

**By End of Week 1:**
- ✅ 6 components complete (Priorities 1-6)
- ✅ Agent validation passing on all 6
- ✅ Visual regression test suite set up

**By End of Week 2:**
- ✅ All 15 components complete
- ✅ Full landing page assembled
- ✅ 98%+ visual match on all components
- ✅ All accessibility checks passing
- ✅ Ready for production deployment

---

**Let's build a landing page that converts! 🚀**

**- Claude** (stepping in for Gemini, who is currently stuck on ESLint fixes)

**P.S.** All design tokens respect platform conventions (iOS HIG, Material Design, Web best practices), so the components will feel native on each platform while maintaining visual consistency.
