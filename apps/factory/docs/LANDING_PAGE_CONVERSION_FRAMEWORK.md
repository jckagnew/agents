# Landing Page Conversion Framework

**Date:** 2025-11-07
**Purpose:** High-converting landing pages for the factory AND all generated apps
**Based on:** Sean's AI Landing Page Workflow + Conversion Best Practices

---

## Executive Summary

Every app needs a landing page that converts visitors into users. This framework ensures both the Design-First Software Factory's own landing page AND every app we generate follows proven conversion principles.

**Dual Purpose:**
1. **Factory Landing Page** - Convert prospects into factory customers
2. **Generated App Landing Pages** - Every app gets a high-converting landing page

**Core Innovation:** Integrate landing page generation into our unified workflow so every project includes conversion-optimized marketing pages, not just the app itself.

---

## Sean's 4-Step Workflow

### Step 1: Clarify Buyer Pains & Psychographics

**Problem:** Generic landing pages don't convert. You need to speak directly to buyer pains.

**Solution:** Targeted prompts that extract:
- **Avatar:** Who is the ideal customer?
- **Pains:** What problems keep them up at night?
- **Aspirations:** What transformation do they seek?
- **Objections:** What stops them from buying?
- **Language:** How do they describe their problems?

**Smart Market Questions:**
```
1. Who is your ideal customer? (role, industry, company size)
2. What's their biggest pain point related to [product category]?
3. What have they tried that didn't work?
4. What would success look like for them?
5. What's their biggest objection to trying a new solution?
6. How do they talk about this problem? (exact phrases)
7. What's their budget/authority/need/timeline?
```

### Step 2: Generate Section-by-Section Copy

**Problem:** Writing copy from scratch is slow and often misses key pain points.

**Solution:** Generate multiple options for each section, tied to specific pains.

**Standard Landing Page Structure:**
1. **Hero** - Hook them in 3 seconds
2. **Problem Agitation** - Make the pain real
3. **Solution Introduction** - Present your offer
4. **Core Value Props** - 3-4 key benefits
5. **Feature Demos** - Show, don't tell
6. **Social Proof** - Testimonials, logos, metrics
7. **Objection Handling** - Address concerns head-on
8. **Final CTA** - Clear call to action

**Copy Options Per Section:**
- Generate 3-5 variations per section
- Each variation emphasizes different pain/benefit angle
- User can mix and match or iterate

### Step 3: Map to Component Library

**Problem:** Great copy with bad design doesn't convert.

**Solution:** Map each section to high-quality components following 7 conversion principles.

**The 7 Conversion Principles:**
1. **Focus** - One clear primary action per page
2. **Structure** - Logical flow from problem → solution → action
3. **Consistency** - Visual hierarchy, brand voice, design system
4. **Benefits** - Features tell, benefits sell (always lead with benefit)
5. **Attention** - Guide eye to CTA with contrast, size, position
6. **Trust** - Social proof, authority, risk reversal
7. **Low Friction** - Remove steps, reduce form fields, clear process

**Component Library (Expo/Web):**
- Hero sections (video background, animated gradient, split with image)
- Bento grids (showcase features in visual grid)
- Feature cards (icon + headline + description)
- Testimonial carousels
- Pricing tables (3-tier with highlight)
- FAQ accordions
- CTA blocks (various styles)

### Step 4: Design QA Checklist

**Problem:** Small design issues kill conversion (poor contrast, hierarchy, spacing).

**Solution:** Automated checks before launch.

**QA Checklist:**
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 graphics)
- [ ] Typography hierarchy clear (h1 > h2 > h3 > body)
- [ ] Consistent spacing (8px grid system)
- [ ] CTA buttons stand out (high contrast, sufficient size)
- [ ] Mobile responsive (test 375px, 768px, 1440px)
- [ ] Load time < 3 seconds
- [ ] Images optimized (WebP, lazy load)
- [ ] Forms minimal (only essential fields)
- [ ] Clear value proposition above fold
- [ ] Social proof visible without scroll

---

## Part 1: Factory Landing Page

**Audience:** Developers, agencies, product managers who need to ship apps fast

### Avatar Definition

**Primary Avatar:** Solo Developer / Small Agency
- **Pain:** Client projects take too long, scope creep kills profit
- **Aspiration:** Ship beautiful apps in days, not months
- **Budget:** $100-500/project initially, scaling to $50K+ for enterprise
- **Language:** "Design first", "no code/low code", "rapid prototyping"
- **Objection:** "AI-generated code is low quality / won't match my designs"

**Secondary Avatar:** Product Manager at Startup
- **Pain:** Can't afford full dev team, need MVP fast to validate with investors
- **Aspiration:** Professional MVP in 2 weeks for < $5K
- **Budget:** $2-10K for MVP
- **Language:** "Investor-ready", "production-ready", "design validation"
- **Objection:** "This won't scale / lock-in to your platform"

### Landing Page Structure

#### 1. Hero Section

**Headline (3 options):**
```
Option A: "Ship Production-Ready Apps in Days, Not Months"
- Subhead: "Design-first workflow + AI agents = Beautiful apps that match your vision perfectly"

Option B: "Stop Wasting Time on Code That Doesn't Match the Design"
- Subhead: "Our AI validates every line of code against your approved design. Pixel-perfect, guaranteed."

Option C: "From Figma to Production in Under a Week"
- Subhead: "The only AI software factory that guarantees your code matches your design. No surprises, no rework."
```

**CTA:**
- Primary: "Start Free Project" (leads to intake)
- Secondary: "See How It Works" (video demo)

**Visual:**
- Split screen: Messy codebase vs clean factory output
- OR: Animated workflow showing design → validation → code
- OR: Side-by-side Figma and rendered app (perfect match)

#### 2. Problem Agitation

**Copy:**
```
You've been there before:

❌ Client approves the design, but the developer "interprets" it differently
❌ You spend days in code review saying "that's not what we agreed on"
❌ Simple changes require complete rewrites
❌ The final product looks nothing like the mockup

Traditional development is broken. Even with the best intentions, human
interpretation creates drift between design and code.

What if every single line of code was validated against your approved design?
```

#### 3. Solution Introduction

**Headline:** "Introducing Design-First Software Factory"

**Copy:**
```
The only AI workflow that:
1. Captures your exact requirements through intelligent conversation
2. Generates designs with your brand guidelines locked in
3. Validates every component against the approved design using multimodal AI
4. Ships production-ready Expo apps (iOS, Android, Web from one codebase)

Your code WILL match your design. Guaranteed.
```

**Visual:**
- Animated workflow diagram
- "Before/After" with competitor approach

#### 4. Core Value Props (Bento Grid)

```
┌─────────────────────┬─────────────────────┐
│  Design-First       │  AI Validation      │
│  Approval Gate      │  Pixel-Perfect Code │
│                     │                     │
│  ✓ Review designs   │  ✓ Agent compares   │
│    before ANY code  │    code vs design   │
│  ✓ Lock brand       │  ✓ Iterates until   │
│    guidelines       │    match score >85% │
│  ✓ Iterate fast in  │  ✓ No human         │
│    Stitch           │    interpretation   │
└─────────────────────┴─────────────────────┘
┌─────────────────────┬─────────────────────┐
│  Universal Apps     │  Production Ready   │
│  One Codebase       │  Real Code, Tests   │
│                     │                     │
│  ✓ iOS, Android,    │  ✓ TypeScript +     │
│    Web from Expo    │    React Native     │
│  ✓ Platform-aware   │  ✓ Jest + Detox     │
│    design tokens    │    testing scaffold │
│  ✓ Mobile-first     │  ✓ Deployment ready │
│    responsive       │    (not prototypes) │
└─────────────────────┴─────────────────────┘
```

#### 5. Feature Demos (Interactive)

**Demo 1: Express Tier (Auto)**
- Video: "Watch AI generate and validate 12 screens in 4 minutes"
- Show: Codex generating design → Playwright rendering → Comparison → Iteration
- Result: "Score: 0.89 - Code matches design"

**Demo 2: Concierge Tier (Human Approval)**
- Video: "Iterate designs in Stitch, AI ensures code matches"
- Show: Human refining design in Stitch → Export HTML → AI converts to Expo → Validation
- Result: "Your design, perfectly implemented"

**Demo 3: Website Refresh**
- Video: "Point at existing site, get modernized version with brand preserved"
- Show: Existing site analysis → Brand extraction → Modern redesign → Code validation
- Result: "Same brand, modern UX"

#### 6. Social Proof

**Testimonials (need to collect):**
```
"We shipped our MVP in 6 days. Investors were shocked it was AI-generated."
- Sarah K., YC-backed founder

"Finally, code that actually matches the Figma file. This is a game changer."
- Mike R., Design agency owner

"The AI validation step is genius. No more 'that's not what I designed' conversations."
- Lisa T., Product manager
```

**Metrics (when we have them):**
- "4.3 minutes average generation time"
- "0.89 average design match score"
- "97% of projects pass validation on first try"
- "$1.40 average AI cost per project"

**Logos:**
- "Trusted by" section with customer logos (when we have them)
- For now: "Built with" logos (Expo, Supabase, OpenAI, Google)

#### 7. Objection Handling (FAQ)

**"Is the code actually production-ready?"**
```
Yes. We generate TypeScript + React Native with Expo, not prototypes.
Every project includes:
- Complete test scaffolding (Jest + Detox)
- Type-safe code throughout
- Platform-aware design tokens
- Deployment configuration
- Post-handoff checklist

You own the code. Zero lock-in.
```

**"What if I don't like the generated design?"**
```
Express Tier: Automatic design with brand guidelines locked in
Concierge Tier: YOU design in Stitch, we just ensure code matches

Both tiers: Unlimited iterations on code to match your approved design.
```

**"How does the AI validation actually work?"**
```
1. We render your generated code with Playwright
2. AI compares the rendered screenshot to your approved design
3. Multimodal AI scores match across layout, colors, typography, spacing
4. If score < 0.85, AI iterates with specific feedback
5. Repeat until pixel-perfect

You can see every iteration and score in your dashboard.
```

**"What if I need changes after handoff?"**
```
You own the code. It's TypeScript + Expo, fully editable.
Plus:
- Clear documentation
- Architecture compliance built-in
- Easy to modify (follows Core Architecture Blueprint)
- No proprietary frameworks or vendor lock-in
```

#### 8. Pricing

```
┌─────────────────────────────────────────────────────┐
│                    EXPRESS TIER                      │
│                 Fully Automated                      │
│                                                      │
│         $100-200 per project                         │
│                                                      │
│  ✓ AI designs with locked brand guidelines          │
│  ✓ 4-5 minutes from concept to code                 │
│  ✓ Agent validates code matches design              │
│  ✓ 6-12 screens                                     │
│  ✓ Production-ready Expo app                        │
│  ✓ Testing scaffolding                              │
│                                                      │
│  Best for: MVPs, internal tools, rapid prototyping  │
│                                                      │
│           [Start Free Project →]                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                  CONCIERGE TIER                      │
│              Human Design Approval                   │
│                                                      │
│        $500-2,000 per project                        │
│                                                      │
│  ✓ YOU iterate designs in Stitch                    │
│  ✓ Full creative control                            │
│  ✓ Agent validates code matches YOUR design         │
│  ✓ Unlimited design iterations                      │
│  ✓ Priority support                                 │
│  ✓ Everything from Express                          │
│                                                      │
│  Best for: Client work, brand-critical apps         │
│                                                      │
│          [Schedule Consultation →]                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   WEBSITE REFRESH                    │
│               M&A / Rebranding Special               │
│                                                      │
│        $5,000-50,000 per site                        │
│                                                      │
│  ✓ Preserve OR refresh branding                     │
│  ✓ Extract existing screens/flows                   │
│  ✓ Modernize UX to 2025 standards                   │
│  ✓ Maintain technical capabilities                  │
│  ✓ Deploy to production                             │
│                                                      │
│  Best for: PE firms, acquired companies, rebrand    │
│                                                      │
│         [Request Custom Quote →]                     │
└─────────────────────────────────────────────────────┘
```

#### 9. Final CTA

**Headline:** "Stop Guessing if Code Will Match Design. Know for Sure."

**Copy:**
```
Join developers and agencies who trust AI validation for pixel-perfect apps.

Free tier: 3 projects/month
No credit card required
Export code anytime
```

**CTA:**
- Primary: "Start Your First Project Free"
- Secondary: "Watch 4-Minute Demo"

**Visual:**
- Dashboard screenshot showing validation scores
- Before/after code quality comparison

#### 10. Trust Signals (Footer Area)

- Security: "SOC 2 Type II Compliant" (when ready)
- Uptime: "99.9% SLA"
- Support: "Response within 4 hours"
- Open Source: "Built on open source (Expo, Supabase)"
- No Lock-in: "You own the code. Zero vendor lock-in."

---

## Part 2: Generated App Landing Pages

Every app we generate should include a conversion-optimized landing page.

### Integration into Workflow

#### Phase 1: Enhanced Intake (Add to PRD Generation)

**New Questions in Intake:**
```typescript
interface LandingPageIntake {
  // Avatar
  targetAudience: {
    role: string; // "Small business owner", "Fitness enthusiast", etc.
    painPoints: string[]; // Top 3 pains
    aspirations: string[]; // What success looks like
    objections: string[]; // Why they might not sign up
    language: string[]; // How they describe the problem
  };

  // Marketing
  valueProposition: string; // One sentence: "We help X do Y without Z"
  keyBenefits: string[]; // 3-4 benefits (not features!)
  socialProof: {
    testimonials?: Array<{ quote: string; author: string; role: string }>;
    metrics?: Array<{ value: string; label: string }>; // "10K users", "4.8★ rating"
    logos?: string[]; // URLs to customer/partner logos
  };

  // Conversion
  primaryCTA: string; // "Start Free Trial", "Book Demo", "Download Now"
  secondaryCTA?: string; // "Watch Demo", "Learn More"
  conversionGoal: 'signup' | 'waitlist' | 'download' | 'contact' | 'purchase';
}
```

**Prompt Enhancement:**
```typescript
// Add to prd-generation.service.ts
async generateLandingPageCopy(
  intake: LandingPageIntake,
  prd: PRD
): Promise<LandingPageSections> {
  const prompt = `You are a conversion copywriter. Based on this product and target audience,
  generate high-converting landing page copy.

  Product: ${prd.project_name}
  Description: ${prd.executive_summary}

  Target Audience:
  ${JSON.stringify(intake.targetAudience, null, 2)}

  Generate copy for each section following these principles:
  1. Focus - One clear primary action
  2. Benefits first - Features tell, benefits sell
  3. Address pain points directly using their language
  4. Handle objections proactively
  5. Build trust with social proof
  6. Low friction - clear what happens next

  For each section, generate 3 variations emphasizing different pain/benefit angles.

  Sections:
  - Hero (headline + subhead)
  - Problem statement
  - Solution introduction
  - 3-4 core value propositions
  - Feature highlights (tied to benefits)
  - Social proof (testimonials, metrics)
  - Objection handling (FAQ)
  - Final CTA

  Return as structured JSON with multiple options per section.`;

  // Call Gemini to generate
  const result = await this.gemini.generateContent(prompt);

  return parseLandingPageSections(result);
}
```

#### Phase 2: Component Selection (Add to Design System)

**Landing Page Component Library:**

For Expo (Mobile + Web):
```typescript
interface LandingPageComponents {
  heroes: {
    split_with_image: ComponentSpec;
    centered_with_video: ComponentSpec;
    gradient_animated: ComponentSpec;
    minimal_text: ComponentSpec;
  };

  value_props: {
    bento_grid: ComponentSpec; // 2x2 or 3x2 grid
    icon_cards: ComponentSpec; // 3-4 cards with icons
    feature_list: ComponentSpec; // Vertical list with checks
    comparison_table: ComponentSpec; // Us vs Them
  };

  social_proof: {
    testimonial_carousel: ComponentSpec;
    logo_grid: ComponentSpec;
    metrics_bar: ComponentSpec; // "10K users  •  4.8★  •  99.9% uptime"
    case_study_cards: ComponentSpec;
  };

  ctas: {
    primary_button: ComponentSpec; // High contrast, 48px min height
    secondary_button: ComponentSpec;
    form_capture: ComponentSpec; // Email or waitlist
    two_step_cta: ComponentSpec; // "Start Free" → "Enter Email"
  };

  navigation: {
    sticky_header: ComponentSpec; // Logo + CTA always visible
    footer: ComponentSpec; // Links + trust signals
  };
}
```

**Mapping Logic:**
```typescript
// Add to master-workflow.service.ts
async generateLandingPage(
  landingPageCopy: LandingPageSections,
  designSystem: DesignSystem,
  selectedComponents: ComponentSelection
): Promise<LandingPageCode> {
  // For each section, map copy to component
  const sections = [
    {
      type: 'hero',
      component: selectedComponents.hero,
      copy: landingPageCopy.hero,
      props: {
        headline: landingPageCopy.hero.headline,
        subhead: landingPageCopy.hero.subhead,
        primaryCTA: landingPageCopy.cta.primary,
        secondaryCTA: landingPageCopy.cta.secondary,
        image: '...',
      },
    },
    // ... more sections
  ];

  // Generate code for complete landing page
  const code = await this.codex.generateLandingPageFromSections(
    sections,
    designSystem
  );

  return code;
}
```

#### Phase 3: Conversion QA (Add to Code Validation)

**Automated Checks:**
```typescript
// Add to code-validation.service.ts
interface ConversionQA {
  accessibility: {
    colorContrast: { passed: boolean; issues: string[] };
    altText: { passed: boolean; missing: string[] };
    formLabels: { passed: boolean; issues: string[] };
  };

  structure: {
    clearValueProp: boolean; // Above fold?
    primaryCTAVisible: boolean; // Without scroll?
    secondaryOption: boolean; // Low-pressure option?
  };

  performance: {
    loadTime: number; // < 3s?
    imageOptimized: boolean;
    lazyLoading: boolean;
  };

  mobile: {
    responsive: boolean; // Test 375px, 768px, 1440px
    touchTargets: { passed: boolean; tooSmall: string[] }; // 44x44px min
    horizontalScroll: boolean; // Should be false
  };

  copyQuality: {
    valuePropositionClear: boolean;
    benefitsNotFeatures: boolean; // AI check
    ctaActionOriented: boolean; // "Start", "Get", not "Learn More"
    objectionHandling: boolean; // FAQ present?
  };
}

async validateLandingPageConversion(
  code: string,
  projectPath: string
): Promise<ConversionQA> {
  // Run automated checks
  const accessibility = await this.checkAccessibility(projectPath);
  const performance = await this.checkPerformance(projectPath);
  const mobile = await this.checkMobileResponsive(projectPath);

  // AI-powered copy analysis
  const copyQuality = await this.analyzeCopyQuality(code);

  return {
    accessibility,
    structure: await this.checkStructure(code),
    performance,
    mobile,
    copyQuality,
  };
}

private async analyzeCopyQuality(code: string): Promise<CopyQuality> {
  // Extract copy from code
  const copy = extractTextContent(code);

  // AI prompt to evaluate
  const prompt = `Analyze this landing page copy for conversion best practices:

  ${copy}

  Evaluate:
  1. Is the value proposition clear and above the fold?
  2. Are benefits emphasized over features?
  3. Is the CTA action-oriented and clear?
  4. Are objections addressed (FAQ or guarantee)?
  5. Is social proof present and credible?

  Return JSON with boolean scores and specific feedback.`;

  const result = await this.gemini.generateContent(prompt);
  return parseGeminiResponse(result);
}
```

#### Phase 4: Component Library (Magic UI Alternative for Expo)

**Problem:** Magic UI is web-only. We need Expo-compatible components.

**Solution:** Create our own high-quality component library.

**Recommendations:**

For **Web** (Next.js generated apps):
- Use Magic UI directly
- Or Shadcn components (what we already use)
- Or Aceternity UI (similar to Magic UI)

For **Expo** (mobile + web):
- Create custom landing page components
- Based on best practices from Magic UI
- Fully responsive (mobile-first)
- Platform-aware

**Expo Landing Page Components to Build:**

```typescript
// src/components/landing/Hero.tsx
import { View, Text, Platform } from 'react-native';
import { useWindowDimensions } from 'react-native';

export function HeroSplit({ headline, subhead, primaryCTA, image }) {
  const { width } = useWindowDimensions();
  const isMobile = width < 768;

  return (
    <View style={{
      flexDirection: isMobile ? 'column' : 'row',
      padding: isMobile ? 24 : 48,
      alignItems: 'center',
    }}>
      <View style={{ flex: 1 }}>
        <Text style={{
          fontSize: isMobile ? 32 : 48,
          fontWeight: 'bold',
          lineHeight: 1.2,
        }}>
          {headline}
        </Text>
        <Text style={{
          fontSize: isMobile ? 18 : 24,
          marginTop: 16,
          color: '#666',
        }}>
          {subhead}
        </Text>
        <CTAButton
          title={primaryCTA}
          onPress={handleCTA}
          style={{ marginTop: 32 }}
        />
      </View>

      {!isMobile && (
        <View style={{ flex: 1 }}>
          <Image source={image} style={{ width: '100%', height: 400 }} />
        </View>
      )}
    </View>
  );
}
```

**Component Library Structure:**
```
src/components/landing/
├── Hero/
│   ├── HeroSplit.tsx
│   ├── HeroCentered.tsx
│   ├── HeroMinimal.tsx
│   └── HeroWithVideo.tsx
├── ValueProps/
│   ├── BentoGrid.tsx
│   ├── FeatureCards.tsx
│   ├── FeatureList.tsx
│   └── ComparisonTable.tsx
├── SocialProof/
│   ├── TestimonialCarousel.tsx
│   ├── LogoGrid.tsx
│   ├── MetricsBar.tsx
│   └── CaseStudyCard.tsx
├── CTA/
│   ├── PrimaryButton.tsx
│   ├── SecondaryButton.tsx
│   ├── EmailCapture.tsx
│   └── TwoStepCTA.tsx
└── Layout/
    ├── StickyHeader.tsx
    ├── Footer.tsx
    └── Section.tsx
```

**Each component follows:**
- Mobile-first responsive
- Platform-aware (iOS/Android/Web)
- Accessibility built-in (color contrast, touch targets)
- Conversion-optimized (CTA prominence, low friction)
- Design tokens from theme

---

## Part 3: Implementation Plan

### Phase 1: Factory Landing Page (Week 1-2)

**Goal:** Convert prospects to factory customers

**Tasks:**
1. **Day 1-2:** Define avatar and pain points (use Sean's questions)
2. **Day 3-4:** Generate landing page copy (3 options per section)
3. **Day 5-7:** Build page with Shadcn components (web-first)
4. **Day 8-9:** Design QA checklist (color contrast, mobile, performance)
5. **Day 10:** Deploy to factory.example.com
6. **Day 11-14:** A/B test different hero variations

**Components Needed:**
- Hero with animated workflow diagram
- Bento grid for value props
- Demo videos (record 3 flows)
- Testimonials (collect from beta users)
- Pricing table (3 tiers)
- FAQ accordion (address objections)

**Metrics to Track:**
- Bounce rate (target: < 40%)
- Time on page (target: > 2 minutes)
- CTA click rate (target: > 10%)
- Conversion to signup (target: > 5%)

### Phase 2: Landing Page in Intake (Week 3)

**Goal:** Capture landing page requirements during project intake

**Tasks:**
1. **Add landing page questions to intake flow:**
   ```typescript
   // In intake UI, after core project questions:
   "Will this app need a landing page?" [Yes/No]

   If Yes:
   "Who is your ideal user?"
   "What's their biggest pain point?"
   "What does success look like for them?"
   "What might stop them from trying your app?"
   "How do they describe this problem?"
   ```

2. **Update prd-generation.service.ts:**
   - Parse landing page responses
   - Generate landing page copy sections
   - Include in PRD output

3. **Store in database:**
   ```sql
   ALTER TABLE projects ADD COLUMN landing_page_intake JSONB;
   ```

### Phase 3: Component Library (Week 4-5)

**Goal:** Build reusable landing page components for Expo

**Tasks:**
1. **Design system extension:**
   - Add landing page specific tokens (hero sizes, CTA colors)
   - Document conversion principles

2. **Build 15 core components:**
   - 4 hero variants
   - 4 value prop layouts
   - 4 social proof components
   - 3 CTA variants

3. **Test on all platforms:**
   - iOS simulator
   - Android emulator
   - Web browser (responsive)

4. **Document in Storybook:**
   - Each component with examples
   - Props documentation
   - Conversion tips

### Phase 4: Generation Integration (Week 6-7)

**Goal:** Auto-generate landing pages for every project

**Tasks:**
1. **Update master-workflow.service.ts:**
   - After code generation phase
   - Generate landing page if requested
   - Use landing page copy from intake
   - Map to component library

2. **Conversion QA automation:**
   - Run accessibility checks
   - Validate mobile responsive
   - Check color contrast
   - Performance audit

3. **Include in project ZIP:**
   - `src/screens/LandingScreen.tsx`
   - Link from app navigation
   - Or standalone Next.js site for web-only

### Phase 5: Iteration & Optimization (Week 8+)

**Goal:** Improve conversion rates over time

**Tasks:**
1. **A/B testing framework:**
   - Easy to swap hero variations
   - Track which copy converts better
   - Test different CTA wording

2. **Analytics integration:**
   - PostHog or Google Analytics
   - Track scroll depth
   - Heatmaps (Hotjar)
   - Form abandonment

3. **Feedback loop:**
   - Collect user feedback on landing pages
   - Improve prompts based on what works
   - Update component library

---

## Part 4: Copy Generation Prompts

### Hero Section Prompt

```typescript
const heroPrompt = `Generate 3 high-converting hero section variations for a landing page.

Product: ${productName}
Target Audience: ${targetAudience}
Main Pain Point: ${mainPain}
Key Benefit: ${keyBenefit}

For each variation:
- Headline: 5-10 words, promise transformation
- Subhead: 10-20 words, expand on benefit
- Primary CTA: 2-3 words, action-oriented

Principles:
- Lead with benefit, not feature
- Use customer's language
- Create urgency (but not false scarcity)
- Promise specific outcome

Format as JSON:
{
  "variations": [
    {
      "headline": "...",
      "subhead": "...",
      "cta": "...",
      "angle": "problem-focused" | "aspiration-focused" | "proof-focused"
    }
  ]
}`;
```

### Value Prop Prompt

```typescript
const valuePropsPrompt = `Generate 4 core value propositions for this product.

Product: ${productName}
Target Audience: ${targetAudience}
Pain Points: ${painPoints}
Features: ${features}

For each value prop:
- Headline: Benefit statement (not feature)
- Description: 2-3 sentences explaining benefit
- Icon suggestion: Metaphor for the benefit
- Proof point: Metric or testimonial supporting claim

Principles:
- Features tell, benefits sell (always lead with benefit)
- Connect to specific pain points
- Use concrete outcomes ("Save 10 hours/week" not "More efficient")
- Tie to customer aspirations

Format as JSON array of 4 value props.`;
```

### Objection Handling Prompt

```typescript
const objectionPrompt = `Generate FAQ content that proactively addresses objections.

Product: ${productName}
Target Audience: ${targetAudience}
Objections: ${commonObjections}

For each objection:
- Question: How customer phrases their concern
- Answer: 2-3 sentences addressing concern
- Proof: Social proof or guarantee that reinforces answer

Common objection types:
- Price/value ("Too expensive")
- Trust ("Seems too good to be true")
- Fit ("Will this work for my specific situation?")
- Effort ("Sounds complicated to set up")
- Risk ("What if I'm not satisfied?")

Principles:
- Acknowledge concern (don't dismiss)
- Address directly and honestly
- End with reassurance
- Include risk reversal (guarantee, trial, etc.)

Format as JSON array of FAQ items.`;
```

---

## Part 5: Conversion QA Automation

### Automated Checklist

```typescript
// src/services/conversion-qa.service.ts
interface ConversionQAResult {
  score: number; // 0-100
  passed: boolean;
  issues: Array<{
    severity: 'critical' | 'warning' | 'info';
    category: 'accessibility' | 'structure' | 'copy' | 'performance' | 'mobile';
    message: string;
    suggestion: string;
  }>;
}

export class ConversionQAService {
  async audit(landingPageCode: string, projectPath: string): Promise<ConversionQAResult> {
    const checks = [
      // Critical checks (must pass)
      await this.checkColorContrast(projectPath),
      await this.checkMobileResponsive(projectPath),
      await this.checkCTAVisibility(landingPageCode),
      await this.checkLoadTime(projectPath),

      // Important checks (warnings)
      await this.checkValuePropAboveFold(landingPageCode),
      await this.checkSocialProofPresent(landingPageCode),
      await this.checkFormFriction(landingPageCode),

      // Nice-to-have (info)
      await this.analyzeCopyTone(landingPageCode),
      await this.checkImageOptimization(projectPath),
    ];

    const issues = checks.filter(c => !c.passed);
    const criticalIssues = issues.filter(i => i.severity === 'critical');

    return {
      score: calculateScore(checks),
      passed: criticalIssues.length === 0,
      issues,
    };
  }

  private async checkColorContrast(projectPath: string) {
    // Use axe-core or similar
    const violations = await runAccessibilityAudit(projectPath);

    const contrastIssues = violations.filter(v =>
      v.id === 'color-contrast'
    );

    return {
      passed: contrastIssues.length === 0,
      severity: 'critical' as const,
      category: 'accessibility' as const,
      message: `${contrastIssues.length} color contrast violations`,
      suggestion: 'Ensure text has 4.5:1 contrast ratio (WCAG AA)',
    };
  }

  private async checkCTAVisibility(code: string) {
    // AI-powered check
    const prompt = `Analyze this landing page code. Is the primary CTA:
    1. Above the fold (visible without scrolling)?
    2. High contrast from background?
    3. Clear what action user takes?

    Code:
    ${code.substring(0, 2000)}

    Return JSON: { visible: boolean, contrast: boolean, clear: boolean, feedback: string }`;

    const result = await this.gemini.generateContent(prompt);
    const analysis = parseGeminiResponse(result);

    return {
      passed: analysis.visible && analysis.contrast && analysis.clear,
      severity: 'critical' as const,
      category: 'structure' as const,
      message: analysis.feedback,
      suggestion: 'Ensure CTA is prominent and action-oriented',
    };
  }

  private async checkValuePropAboveFold(code: string) {
    // Check if clear value prop in first 800px
    const hasValueProp = code.includes('value-proposition') ||
                        /What (we do|you get|makes us different)/i.test(code);

    return {
      passed: hasValueProp,
      severity: 'warning' as const,
      category: 'copy' as const,
      message: hasValueProp ? 'Value prop found' : 'No clear value proposition detected',
      suggestion: 'Include "We help [audience] do [outcome] without [pain]" above fold',
    };
  }
}
```

### Integration with Master Workflow

```typescript
// In master-workflow.service.ts, after landing page generation:
if (projectIncludesLandingPage) {
  console.log('\n🎯 Running Conversion QA...');

  const conversionQA = new ConversionQAService(this.geminiApiKey);
  const qaResult = await conversionQA.audit(landingPageCode, projectPath);

  console.log(`Conversion Score: ${qaResult.score}/100`);

  if (!qaResult.passed) {
    console.warn('⚠️  Critical conversion issues found:');
    qaResult.issues
      .filter(i => i.severity === 'critical')
      .forEach(issue => {
        console.warn(`  - ${issue.message}`);
        console.warn(`    Suggestion: ${issue.suggestion}`);
      });

    // Optionally: iterate to fix issues
    if (autoFixEnabled) {
      landingPageCode = await this.fixConversionIssues(
        landingPageCode,
        qaResult.issues
      );
    }
  }

  // Save QA report
  await supabase.from('landing_page_audits').insert({
    project_id: projectId,
    score: qaResult.score,
    issues: qaResult.issues,
  });
}
```

---

## Part 6: Success Metrics

### Factory Landing Page Metrics

Track these to optimize factory conversion:

**Awareness:**
- Unique visitors/month
- Traffic sources (organic, paid, referral)
- Bounce rate (target: < 40%)

**Engagement:**
- Time on page (target: > 2 minutes)
- Scroll depth (target: 70% reach final CTA)
- Video play rate (if applicable)

**Conversion:**
- CTA click rate (target: > 10%)
- Signup rate (target: > 5%)
- Trial start rate
- Free → Paid conversion (target: > 20%)

**Optimization:**
- A/B test results (hero variations)
- Heatmap analysis
- Session recordings (drop-off points)

### Generated Landing Page Metrics

For apps we generate, recommend tracking:

- Bounce rate
- Signup conversion rate
- CTA click-through rate
- Mobile vs desktop conversion
- Time to first action

Provide PostHog integration by default in generated apps.

---

## Part 7: Example Output

### What a Generated Landing Page Looks Like

When user completes intake with landing page requirements:

**Input:**
```json
{
  "projectName": "FitTrack Pro",
  "targetAudience": {
    "role": "Busy professionals who want to stay fit",
    "painPoints": [
      "No time for gym",
      "Can't stay motivated",
      "Don't know if making progress"
    ],
    "aspirations": ["Get fit without gym membership", "Work out from home efficiently"],
    "objections": ["Too busy", "Tried apps before, didn't stick"]
  },
  "valueProposition": "We help busy professionals get fit with 15-minute home workouts that actually work",
  "conversionGoal": "signup"
}
```

**Output: Complete Landing Page**

```typescript
// src/screens/LandingScreen.tsx
import React from 'react';
import { ScrollView } from 'react-native';
import {
  HeroSplit,
  BentoGrid,
  TestimonialCarousel,
  PricingTable,
  FAQ,
  CTABlock,
} from '../components/landing';

export default function LandingScreen() {
  return (
    <ScrollView>
      {/* Hero */}
      <HeroSplit
        headline="Get Fit in 15 Minutes a Day. No Gym Required."
        subhead="Proven workouts for busy professionals who don't have time for the gym but refuse to give up on fitness."
        primaryCTA="Start Free Trial"
        secondaryCTA="See How It Works"
        image={require('../assets/hero-workout.jpg')}
      />

      {/* Problem Agitation */}
      <ProblemSection
        problems={[
          "You know you need to exercise, but who has time for the gym?",
          "You've tried workout apps before, but they were too complicated or boring.",
          "You're not even sure if you're making progress without a trainer.",
        ]}
      />

      {/* Value Props */}
      <BentoGrid
        items={[
          {
            title: "15-Minute Workouts",
            description: "Science-backed routines that fit into your lunch break. No equipment needed.",
            icon: "clock",
          },
          {
            title: "AI Personal Trainer",
            description: "Form correction and motivation in real-time. Like having a trainer in your pocket.",
            icon: "sparkles",
          },
          {
            title: "Progress You Can See",
            description: "Track strength, endurance, and body composition. See results in 2 weeks.",
            icon: "chart",
          },
          {
            title: "Works Anywhere",
            description: "Home, hotel, park, or office. Your workout goes wherever you do.",
            icon: "location",
          },
        ]}
      />

      {/* Social Proof */}
      <TestimonialCarousel
        testimonials={[
          {
            quote: "I've tried every workout app. This is the only one that stuck. Down 15 pounds in 2 months.",
            author: "Sarah M.",
            role: "Product Manager, 36",
            image: "...",
          },
          // More testimonials
        ]}
      />

      {/* Pricing */}
      <PricingTable
        tiers={[
          {
            name: "Free",
            price: "$0/month",
            features: ["3 workouts/week", "Basic tracking"],
            cta: "Start Free",
          },
          {
            name: "Pro",
            price: "$9.99/month",
            features: ["Unlimited workouts", "AI form correction", "Progress analytics", "Meal planning"],
            cta: "Try 14 Days Free",
            highlighted: true,
          },
        ]}
      />

      {/* FAQ - Objection Handling */}
      <FAQ
        items={[
          {
            q: "I'm too busy. How can I fit this in?",
            a: "That's exactly why we built 15-minute workouts. Shorter than your coffee break, but you'll see results in 2 weeks. 94% of users complete at least 3 workouts/week.",
          },
          {
            q: "I've tried workout apps before and quit. Why is this different?",
            a: "We focus on building a habit first. Start with just 2 workouts/week. Our AI trainer adapts to your schedule and energy levels. It's not about perfection, it's about consistency.",
          },
          // More FAQs
        ]}
      />

      {/* Final CTA */}
      <CTABlock
        headline="Join 50,000+ busy professionals getting fit in 15 minutes a day"
        cta="Start Free Trial"
        subtext="No credit card required. Cancel anytime."
      />
    </ScrollView>
  );
}
```

---

## Conclusion

This framework ensures:

1. **Factory Landing Page** converts prospects into customers
2. **Every Generated App** includes conversion-optimized landing page
3. **Sean's Best Practices** integrated into workflow
4. **Automated QA** catches conversion issues before launch
5. **Component Library** makes it fast and consistent

**Next Steps:**

1. **This Week:** Build factory landing page
2. **Next Week:** Add landing page questions to intake
3. **Week 3-4:** Build Expo component library
4. **Week 5:** Integrate into code generation
5. **Week 6:** Add conversion QA automation

**Success Metrics:**
- Factory: 5% visitor → signup conversion
- Generated apps: Landing page included in 80%+ of projects
- Average conversion QA score: 85+/100

The landing page is often the difference between success and failure. With this framework, every project starts with a conversion-optimized foundation.

---

**Prepared by:** Claude
**Date:** 2025-11-07
**Status:** Ready for implementation
**Based on:** Sean's AI Landing Page Workflow + Conversion Best Practices
