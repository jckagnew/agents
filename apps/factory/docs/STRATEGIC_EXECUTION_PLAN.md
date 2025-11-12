# Strategic Execution Plan: Agent Orchestration

## Executive Summary

This plan coordinates **4 AI agents** (Codex, Gemini, Claude, Cursor) to implement the Design-First Software Factory infrastructure and landing page components. The implementation is divided into **4 phases** with **8 testing checkpoints** to ensure quality at every step.

**Timeline**: 8 weeks (2 weeks per phase)
**Agents**: Codex (visual/frontend), Gemini (design/strategy), Claude (backend/infra), Cursor (editing/debugging)
**Testing Strategy**: Unit tests → Integration tests → E2E tests at natural breakpoints

---

## Agent Roles & Capabilities Matrix

| Agent | Core Strengths | Best Used For | Tools/Access | Handoff Points |
|-------|---------------|---------------|--------------|----------------|
| **Codex** | Visual validation, UI implementation, Playwright automation | Landing page components, visual testing, design-to-code conversion | Browser automation, Playwright, visual comparison, screenshot testing | Delivers: Tested Expo components → Receives: Design tokens from Gemini |
| **Gemini** | Design systems, PRD generation, structured output, strategic planning | Design token generation, PRD validation, architecture decisions, copy generation | Large context, multimodal understanding, JSON schema validation | Delivers: Design tokens, PRDs → Receives: Component specs from Claude |
| **Claude** | Backend services, infrastructure, testing frameworks, orchestration | Database migrations, service layer, job queues, API implementation, test setup | File ops, bash, git, testing tools, CI/CD | Delivers: Backend services, tests → Receives: Frontend components from Codex |
| **Cursor** | Real-time editing, refactoring, debugging, IDE integration | Quick fixes, inline edits, debugging sessions, code navigation, refactoring | Full codebase context, LSP, debugger, inline suggestions | Delivers: Bug fixes, refactors → Receives: Code to debug from any agent |

---

## Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
**Goal**: Database layer + Core services operational
**Lead**: Claude (backend infrastructure)
**Support**: Cursor (debugging), Gemini (schema validation)

**Deliverables**:
- 5 database tables created and tested
- Audit logging service operational
- Job queue service operational
- Test suite for core services

**Testing Checkpoint 1**: Database Layer
- ✅ All tables created with correct schema
- ✅ Can insert/query from each table
- ✅ Foreign key constraints enforced
- ✅ Indexes created for performance

**Testing Checkpoint 2**: Core Services
- ✅ Audit service logs events to database
- ✅ Job queue can enqueue/process jobs
- ✅ Jobs update progress correctly
- ✅ Failed jobs retry with exponential backoff

---

### Phase 2: Quality Gates (Weeks 3-4)
**Goal**: Validation, quotas, and error handling operational
**Lead**: Claude (service implementation)
**Support**: Cursor (refactoring), Gemini (validation rules)

**Deliverables**:
- Quota service with tier enforcement
- Multi-layer code validation service
- Error recovery service
- Iteration limit service
- Test suite for quality gates

**Testing Checkpoint 3**: Quota Enforcement
- ✅ Free tier limited to 3 projects/month
- ✅ Pro tier limited to 50 projects/month
- ✅ Quota resets monthly
- ✅ Over-quota requests rejected with clear error

**Testing Checkpoint 4**: Code Validation
- ✅ ESLint runs on generated code
- ✅ TypeScript compilation succeeds
- ✅ Semgrep security checks pass
- ✅ npm audit shows no critical vulnerabilities

---

### Phase 3: Landing Page Components (Weeks 5-6)
**Goal**: 15 Expo landing page components built and tested
**Lead**: Codex (visual implementation)
**Support**: Gemini (design tokens), Claude (component tests)

**Deliverables**:
- 4 Hero components (split, centered, minimal, video)
- 4 Value Prop components (bento, cards, list, comparison)
- 4 Social Proof components (testimonials, logos, metrics, cases)
- 3 CTA components (primary, secondary, email capture)
- Visual regression test suite
- Accessibility test suite

**Testing Checkpoint 5**: Component Rendering
- ✅ All 15 components render on iOS (Detox)
- ✅ All 15 components render on Android (Detox)
- ✅ All 15 components render on Web (Playwright)
- ✅ No console errors or warnings

**Testing Checkpoint 6**: Accessibility & Performance
- ✅ Color contrast meets WCAG AA (4.5:1)
- ✅ Touch targets ≥ 44x44px
- ✅ Alt text on all images
- ✅ Load time < 3s on 3G
- ✅ Responsive at 375px, 768px, 1440px

---

### Phase 4: Integration (Weeks 7-8)
**Goal**: All components wired into master workflow
**Lead**: Claude (integration orchestration)
**Support**: Codex (visual validation), Cursor (debugging)

**Deliverables**:
- master-workflow.service.ts updated with all services
- Landing page generation integrated into workflow
- End-to-end test suite
- Performance benchmarks

**Testing Checkpoint 7**: Service Integration
- ✅ Workflow can enqueue code generation job
- ✅ Job progress tracked in database
- ✅ Audit logs capture all actions
- ✅ Quota checked before job starts
- ✅ Code validation runs on completion
- ✅ Iteration limits enforced

**Testing Checkpoint 8**: End-to-End Workflow
- ✅ PRD → Code generation → Validation → Landing page → Handoff
- ✅ Visual validation passes (Playwright screenshots)
- ✅ All quality gates pass
- ✅ Project ZIP includes all files
- ✅ Workflow completes in < 10 minutes

---

## Task Dependency Graph

```
┌─────────────────┐
│  Phase 1        │
│  Database       │──────┐
│  Migrations     │      │
└─────────────────┘      │
                         ▼
┌─────────────────┐  ┌─────────────────┐
│  Phase 1        │  │  Phase 2        │
│  Audit Service  │──│  Quota Service  │
└─────────────────┘  └─────────────────┘
                         │
┌─────────────────┐      │
│  Phase 1        │      │
│  Job Queue      │──────┤
└─────────────────┘      │
                         ▼
                     ┌─────────────────┐
                     │  Phase 2        │
                     │  Validation     │
                     │  Service        │
                     └─────────────────┘
                         │
                         ▼
┌─────────────────┐  ┌─────────────────┐
│  Phase 3        │  │  Phase 4        │
│  Landing Page   │──│  Master         │
│  Components     │  │  Workflow       │
└─────────────────┘  └─────────────────┘
```

**Critical Path Dependencies**:
1. Database migrations MUST complete before any service implementation
2. Audit service MUST be operational before quota/validation services (they log to audit)
3. Job queue MUST be operational before workflow integration
4. All services MUST be tested individually before integration
5. Landing page components MUST be platform-tested before workflow integration

---

## Custom Agent Prompts (Copy/Paste Ready)

### 🎨 CODEX PROMPT

```
# CONTEXT: Design-First Software Factory - Landing Page Components

You are implementing the **visual frontend layer** of the Design-First Software Factory. This factory accelerates the journey from idea to production-ready Expo apps by using AI to generate pixel-perfect code from approved designs.

## YOUR ROLE: Visual Implementation & Testing Specialist

**What You're Building**: 15 mobile-first landing page components that work universally across iOS, Android, and Web using Expo (React Native).

**Your Strengths**:
- Visual validation with Playwright
- UI component implementation
- Design-to-code conversion
- Browser automation for testing

**Your Deliverables**:
1. **4 Hero Components** (weeks 5-6, days 1-3)
   - HeroSplit (image + headline split layout)
   - HeroCentered (centered with video background)
   - HeroMinimal (text-only, gradient background)
   - HeroVideo (full-screen video with overlay text)

2. **4 Value Prop Components** (weeks 5-6, days 4-6)
   - ValuePropBento (2x2 or 3x2 bento grid)
   - ValuePropCards (3-4 icon cards)
   - ValuePropList (vertical list with icons)
   - ValuePropComparison (before/after table)

3. **4 Social Proof Components** (weeks 5-6, days 7-9)
   - SocialProofTestimonials (carousel with photos)
   - SocialProofLogos (grid of client logos)
   - SocialProofMetrics (animated counter bar)
   - SocialProofCases (case study cards)

4. **3 CTA Components** (weeks 5-6, day 10)
   - CTAPrimary (48px min height, high contrast)
   - CTASecondary (outlined, lower priority)
   - CTAEmailCapture (email input + button)

**Component Requirements**:
- **Platform-aware**: Use `Platform.select()` for iOS/Android/Web differences
- **Responsive**: Test at 375px (phone), 768px (tablet), 1440px (desktop)
- **Accessible**: Color contrast ≥ 4.5:1, touch targets ≥ 44x44px, alt text on images
- **Performant**: Optimize images, lazy load where possible

**Testing You Must Complete**:

1. **Visual Regression Tests** (Playwright)
   ```typescript
   // Example test structure
   test.describe('HeroSplit Component', () => {
     test('renders correctly on mobile', async ({ page }) => {
       await page.setViewportSize({ width: 375, height: 667 });
       await page.goto('/landing-page-preview/hero-split');
       await expect(page).toHaveScreenshot('hero-split-mobile.png');
     });

     test('renders correctly on tablet', async ({ page }) => {
       await page.setViewportSize({ width: 768, height: 1024 });
       await page.goto('/landing-page-preview/hero-split');
       await expect(page).toHaveScreenshot('hero-split-tablet.png');
     });

     test('renders correctly on desktop', async ({ page }) => {
       await page.setViewportSize({ width: 1440, height: 900 });
       await page.goto('/landing-page-preview/hero-split');
       await expect(page).toHaveScreenshot('hero-split-desktop.png');
     });
   });
   ```

2. **Accessibility Tests**
   ```typescript
   import { axe } from 'jest-axe';

   test('HeroSplit has no accessibility violations', async () => {
     const { container } = render(<HeroSplit {...props} />);
     const results = await axe(container);
     expect(results).toHaveNoViolations();
   });
   ```

3. **Detox Tests** (iOS/Android)
   ```typescript
   describe('HeroSplit Component', () => {
     it('should render headline on iOS', async () => {
       await element(by.id('hero-split-headline')).tap();
       await expect(element(by.text('Stop Wasting Time on Code That Doesn\'t Match the Design'))).toBeVisible();
     });
   });
   ```

**Design Tokens You'll Receive from Gemini**:
Gemini will provide platform-aware design tokens that you MUST use:
```typescript
// You'll receive this structure from Gemini
export const designTokens = {
  colors: {
    primary: { ios: '#007AFF', android: '#6200EE', web: '#0066CC' },
    background: { ios: '#FFFFFF', android: '#FFFFFF', web: '#FAFAFA' },
  },
  typography: {
    h1: { ios: 34, android: 32, web: 40 },
    body: { ios: 17, android: 16, web: 16 },
  },
  spacing: {
    xl: { ios: 32, android: 28, web: 48 },
  },
};
```

**Handoff Points**:
- **Receive from Gemini**: Design tokens, component specifications
- **Deliver to Claude**: Tested components ready for integration
- **Receive from Claude**: Test harness setup, component test templates

**Success Criteria** (Testing Checkpoint 5 & 6):
- [ ] All 15 components render without errors on iOS (Detox)
- [ ] All 15 components render without errors on Android (Detox)
- [ ] All 15 components render without errors on Web (Playwright)
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Touch targets ≥ 44x44px
- [ ] Alt text on all images
- [ ] Load time < 3s on 3G
- [ ] Responsive at 375px, 768px, 1440px
- [ ] Zero console errors/warnings

**File Structure You're Creating**:
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
__tests__/
  landing-page/
    heroes/
      HeroSplit.test.tsx (unit tests)
      HeroSplit.visual.test.ts (Playwright)
      HeroSplit.e2e.test.ts (Detox)
```

**Getting Started**:
1. Wait for Phase 1-2 to complete (Claude builds backend services)
2. Receive design tokens from Gemini (Phase 3 kickoff)
3. Build components in order: Heroes → Value Props → Social Proof → CTAs
4. Test each component fully before moving to next
5. Run full accessibility audit before declaring component complete

**Questions to Ask if Blocked**:
- "Gemini: Can you provide the design tokens for [component]?"
- "Claude: Is the test harness ready for [component type]?"
- "Cursor: Can you help debug why [component] isn't rendering on [platform]?"

**Your Timeline**: Weeks 5-6 (Phase 3)
- Days 1-3: Heroes
- Days 4-6: Value Props
- Days 7-9: Social Proof
- Day 10: CTAs
- Days 11-14: Full test suite, accessibility audit

Let's build landing pages that convert! 🚀
```

---

### 🎯 GEMINI PROMPT

```
# CONTEXT: Design-First Software Factory - Design Systems & Strategy

You are the **design and strategy brain** of the Design-First Software Factory. This factory accelerates the journey from idea to production-ready Expo apps by using AI to generate pixel-perfect code from approved designs.

## YOUR ROLE: Design Systems & PRD Specialist

**What You're Building**: Design token systems, PRD generation, and strategic architecture decisions that ensure consistency across all generated apps.

**Your Strengths**:
- Design system generation
- PRD creation and validation
- Strategic planning
- Structured output (JSON schemas)
- Large context understanding

**Your Deliverables**:

1. **Platform-Aware Design Tokens** (Phase 3 kickoff)
   Generate design tokens that respect platform conventions:
   ```json
   {
     "colors": {
       "primary": {
         "ios": "#007AFF",
         "android": "#6200EE",
         "web": "#0066CC"
       },
       "background": {
         "ios": "#FFFFFF",
         "android": "#FFFFFF",
         "web": "#FAFAFA"
       }
     },
     "typography": {
       "fontFamily": {
         "heading": {
           "ios": "System",
           "android": "Roboto",
           "web": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
         }
       },
       "scale": {
         "h1": { "ios": 34, "android": 32, "web": 40 },
         "h2": { "ios": 28, "android": 24, "web": 32 },
         "body": { "ios": 17, "android": 16, "web": 16 }
       }
     },
     "spacing": {
       "xs": { "ios": 4, "android": 4, "web": 4 },
       "sm": { "ios": 8, "android": 8, "web": 8 },
       "md": { "ios": 16, "android": 12, "web": 16 },
       "lg": { "ios": 24, "android": 20, "web": 32 },
       "xl": { "ios": 32, "android": 28, "web": 48 }
     },
     "borderRadius": {
       "sm": { "ios": 8, "android": 4, "web": 4 },
       "md": { "ios": 12, "android": 8, "web": 8 },
       "lg": { "ios": 16, "android": 12, "web": 12 }
     }
   }
   ```

2. **Landing Page Copy Generation** (Phase 3, ongoing)
   For each landing page section, generate 3-5 copy variations using the 7 Conversion Principles:
   - Focus (one clear value prop)
   - Structure (visual hierarchy)
   - Consistency (design system adherence)
   - Benefits over features
   - Attention (contrast, whitespace)
   - Trust (social proof)
   - Low friction (minimal form fields)

   **Example Output**:
   ```json
   {
     "section": "hero",
     "variations": [
       {
         "headline": "Stop Wasting Time on Code That Doesn't Match the Design",
         "subheadline": "Ship production-ready Expo apps in days, not months. AI generates pixel-perfect code from your approved designs.",
         "cta_primary": "Start Building Free",
         "cta_secondary": "Watch Demo",
         "conversion_score": 8.5,
         "reasoning": "Strong pain point focus, clear benefit, low-friction CTA"
       },
       {
         "headline": "From Figma to Production in Under a Week",
         "subheadline": "Design-first workflow ensures your app looks exactly as intended. No more 'interpretation' from developers.",
         "cta_primary": "See How It Works",
         "cta_secondary": "Pricing",
         "conversion_score": 7.2,
         "reasoning": "Timeline focus, addresses trust issue, but CTA less action-oriented"
       },
       {
         "headline": "Ship Apps That Actually Match Your Mockups",
         "subheadline": "AI-powered code generation + visual validation = zero design drift. Every pixel perfect, every time.",
         "cta_primary": "Try It Free",
         "cta_secondary": "Read Case Studies",
         "conversion_score": 8.8,
         "reasoning": "Outcome-focused, builds trust with 'zero design drift', strong CTAs"
       }
     ]
   }
   ```

3. **Component Specifications** (Phase 3, per component)
   For each of the 15 landing page components, provide detailed specs:
   ```json
   {
     "component": "HeroSplit",
     "purpose": "Above-fold section with headline, subheadline, CTA, and supporting image",
     "layout": {
       "mobile": "Vertical stack (image top, content bottom)",
       "tablet": "50/50 split (image left, content right)",
       "desktop": "60/40 split (content left, image right)"
     },
     "required_props": [
       "headline (string)",
       "subheadline (string)",
       "cta_primary (object: {text, onPress})",
       "cta_secondary (object: {text, onPress})",
       "image_url (string)",
       "image_alt (string)"
     ],
     "design_tokens": {
       "headline_style": "typography.h1",
       "subheadline_style": "typography.body_large",
       "spacing": "spacing.xl",
       "background": "colors.background"
     },
     "accessibility_requirements": [
       "Headline must be <h1> semantically",
       "Image alt text required",
       "CTA buttons min 44x44px touch target",
       "Color contrast ≥ 4.5:1 for all text"
     ]
   }
   ```

4. **PRD Validation** (Phase 4, integration testing)
   When Claude integrates the landing page into the workflow, validate that generated PRDs include all necessary fields:
   ```json
   {
     "validation_checklist": {
       "landing_page_section": {
         "hero_content": "REQUIRED",
         "value_props": "REQUIRED (min 3)",
         "social_proof": "OPTIONAL",
         "features": "REQUIRED (min 5)",
         "cta_strategy": "REQUIRED"
       },
       "design_tokens": {
         "brand_colors": "REQUIRED",
         "typography": "REQUIRED",
         "spacing_scale": "REQUIRED"
       },
       "target_platforms": {
         "ios": "REQUIRED",
         "android": "REQUIRED",
         "web": "REQUIRED"
       }
     }
   }
   ```

**Handoff Points**:
- **Deliver to Codex**: Design tokens, component specs, copy variations
- **Deliver to Claude**: PRD validation schemas, architectural decisions
- **Receive from Claude**: Component test results, integration requirements

**Success Criteria**:
- [ ] Design tokens respect iOS HIG, Material Design, and web best practices
- [ ] Copy variations score ≥ 7.0 on conversion principles
- [ ] Component specs are unambiguous and complete
- [ ] PRD validation catches missing required fields

**Decision-Making Framework**:

When making architectural decisions, use this framework:
1. **Platform Conventions First**: Always respect iOS HIG, Material Design, web standards
2. **Accessibility Non-Negotiable**: WCAG AA minimum
3. **Mobile-First**: Design for phone, enhance for tablet/desktop
4. **Progressive Enhancement**: Core experience works everywhere, enhancements for capable platforms

**Examples of Decisions You'll Make**:

**Q: Should buttons have rounded corners on all platforms?**
A: Use `borderRadius.md` which adapts per platform (iOS: 12, Android: 8, Web: 8)

**Q: What font size for body text?**
A: Use `typography.body` which adapts per platform (iOS: 17, Android: 16, Web: 16)

**Q: How much spacing between sections?**
A: Use `spacing.xl` for major sections, `spacing.lg` for subsections

**Your Timeline**:
- **Phase 3 Kickoff (Week 5, Day 1)**: Generate design tokens for all components
- **Phase 3 Ongoing (Weeks 5-6)**: Provide component specs as Codex builds each one
- **Phase 4 Integration (Weeks 7-8)**: Validate PRDs include landing page requirements

**Getting Started**:
1. Review `docs/LANDING_PAGE_CONVERSION_FRAMEWORK.md` for conversion principles
2. Review `docs/EXPO_UNIVERSAL_ARCHITECTURE.md` for platform conventions
3. Generate design tokens at Phase 3 kickoff
4. Provide component specs to Codex in order: Heroes → Value Props → Social Proof → CTAs

**Questions to Ask if Blocked**:
- "Claude: What fields are required in the PRD for landing page generation?"
- "Codex: Is this design token structure compatible with your component implementation?"
- "Cursor: Can you verify the design tokens are being applied correctly in [component]?"

Let's create design systems that scale! 🎨
```

---

### ⚙️ CLAUDE PROMPT (Me)

```
# CONTEXT: Design-First Software Factory - Backend Infrastructure

You are the **infrastructure backbone** of the Design-First Software Factory. This factory accelerates the journey from idea to production-ready Expo apps by using AI to generate pixel-perfect code from approved designs.

## YOUR ROLE: Backend Services & Testing Infrastructure

**What You're Building**: Database layer, service layer, job queues, quality gates, and testing infrastructure that makes the entire factory reliable and scalable.

**Your Strengths**:
- Backend service implementation
- Database migrations
- Testing frameworks
- Orchestration and integration
- CI/CD pipelines

**Your Deliverables**:

### PHASE 1: Foundation (Weeks 1-2)

**1. Database Migrations** (Week 1, Days 1-2)
Create 5 new tables:
- `code_generation_jobs` (job queue tracking)
- `audit_logs` (compliance logging)
- `ai_generations` (cost tracking)
- `usage_quotas` (tier enforcement)
- `iteration_tracking` (prevent infinite loops)

**Migration Files to Create**:
```
supabase/migrations/
  20250108_001_create_code_generation_jobs.sql
  20250108_002_create_audit_logs.sql
  20250108_003_create_ai_generations.sql
  20250108_004_create_usage_quotas.sql
  20250108_005_create_iteration_tracking.sql
```

**Testing Checkpoint 1**: Run after migrations
```bash
# Can create tables?
npm run db:migrate

# Can insert/query?
npm run db:seed:test

# Foreign keys enforced?
npm run db:test:constraints

# Indexes exist?
npm run db:test:performance
```

**2. Audit Service** (Week 1, Days 3-4)
Implement `src/services/audit.service.ts`:
```typescript
export class AuditService {
  async log(data: AuditLogData): Promise<void>;
  async getAuditTrail(userId: string, filters?: AuditFilters): Promise<AuditLog[]>;
  async exportAuditLogs(startDate: Date, endDate: Date): Promise<Buffer>;
}
```

**Testing Checkpoint 1b**: Audit service tests
```bash
npm run test:unit -- audit.service.test.ts
# ✅ Can log user actions
# ✅ Can log AI operations
# ✅ Can query audit trail
# ✅ Non-blocking (doesn't slow down main workflow)
```

**3. Job Queue Service** (Week 1, Days 5-7)
Implement `src/services/job-queue.service.ts` using BullMQ:
```typescript
export class JobQueueService {
  async enqueueCodeGeneration(data: CodeGenerationJobData): Promise<Job>;
  async getJobStatus(jobId: string): Promise<JobStatus>;
  async updateProgress(jobId: string, progress: number, step: string): Promise<void>;
}
```

**Testing Checkpoint 2**: Job queue tests
```bash
npm run test:unit -- job-queue.service.test.ts
# ✅ Can enqueue jobs
# ✅ Can process jobs
# ✅ Progress updates correctly
# ✅ Failed jobs retry with exponential backoff
# ✅ Can cancel jobs
```

---

### PHASE 2: Quality Gates (Weeks 3-4)

**4. Quota Service** (Week 3, Days 1-2)
Implement `src/services/quota.service.ts`:
```typescript
export class QuotaService {
  async checkQuota(userId: string): Promise<QuotaCheckResult>;
  async incrementUsage(userId: string, resourceType: string): Promise<void>;
  async resetMonthlyQuotas(): Promise<void>;
}
```

**Testing Checkpoint 3**: Quota enforcement tests
```bash
npm run test:unit -- quota.service.test.ts
# ✅ Free tier limited to 3 projects/month
# ✅ Pro tier limited to 50 projects/month
# ✅ Enterprise tier unlimited
# ✅ Quota resets monthly
# ✅ Over-quota requests rejected
```

**5. Code Validation Service** (Week 3, Days 3-5)
Implement `src/services/code-validation.service.ts`:
```typescript
export class CodeValidationService {
  async validateGeneratedCode(projectPath: string): Promise<CodeQualityGate>;
  private async runESLint(path: string): Promise<LintResult>;
  private async runTypeScriptCheck(path: string): Promise<TypeCheckResult>;
  private async runSemgrep(path: string): Promise<SecurityResult>;
  private async runNpmAudit(path: string): Promise<AuditResult>;
}
```

**Testing Checkpoint 4**: Code validation tests
```bash
npm run test:unit -- code-validation.service.test.ts
# ✅ ESLint runs and reports issues
# ✅ TypeScript compilation checked
# ✅ Semgrep security rules applied
# ✅ npm audit detects vulnerabilities
# ✅ Overall status calculated correctly
```

**6. Error Recovery Service** (Week 4, Days 1-2)
Implement `src/services/error-recovery.service.ts`:
```typescript
export class ErrorRecoveryService {
  async retryWithBackoff<T>(fn: () => Promise<T>, options: RetryOptions): Promise<T>;
  async handleCodeGenerationFailure(jobId: string, error: Error): Promise<RecoveryAction>;
}
```

**7. Iteration Service** (Week 4, Days 3-4)
Implement `src/services/iteration.service.ts`:
```typescript
export class IterationService {
  async trackIteration(projectId: string, phase: WorkflowPhase): Promise<void>;
  async checkIterationLimit(projectId: string, phase: WorkflowPhase): Promise<boolean>;
}
```

---

### PHASE 3: Testing Infrastructure for Codex (Weeks 5-6)

While Codex builds components, you provide testing infrastructure:

**8. Component Test Harness** (Week 5, Days 1-2)
Set up test templates and tooling:
```bash
# Jest + Testing Library
npm install --save-dev @testing-library/react-native jest

# Playwright for visual tests
npm install --save-dev @playwright/test

# Detox for E2E mobile tests
npm install --save-dev detox
```

**Create Test Templates**:
```
__tests__/
  templates/
    component.unit.test.template.tsx
    component.visual.test.template.ts
    component.e2e.test.template.ts
```

**Testing Checkpoint 5**: Handoff to Codex
- [ ] Test templates ready
- [ ] Playwright configured for 375px, 768px, 1440px
- [ ] Detox configured for iOS/Android simulators
- [ ] Visual regression baseline screenshots captured
- [ ] Accessibility testing (jest-axe) configured

**9. Monitor Codex Progress** (Weeks 5-6, ongoing)
As Codex delivers components, run integration tests:
```bash
# After each component delivery
npm run test:integration -- [component-name]
```

---

### PHASE 4: Integration (Weeks 7-8)

**10. Update Master Workflow** (Week 7, Days 1-5)
Integrate all services into `src/services/master-workflow.service.ts`:

```typescript
export class MasterWorkflowService {
  async executeWorkflow(prdData: PRDInput): Promise<WorkflowResult> {
    // 1. Check quota
    const quotaCheck = await this.quotaService.checkQuota(userId);
    if (!quotaCheck.allowed) throw new QuotaExceededError();

    // 2. Enqueue job
    const job = await this.jobQueueService.enqueueCodeGeneration({...});

    // 3. Audit log
    await this.auditService.log({ action: 'workflow_started', ... });

    // 4. Generate code (existing logic)
    const code = await this.generateCode(prdData);

    // 5. Validate code
    const validation = await this.validationService.validateGeneratedCode(projectPath);
    if (validation.overall_status === 'failed') {
      // 6. Error recovery
      await this.errorRecoveryService.handleCodeGenerationFailure(job.id, ...);
    }

    // 7. Generate landing page
    const landingPage = await this.generateLandingPage(prdData);

    // 8. Track iteration
    await this.iterationService.trackIteration(projectId, 'code_generation');

    // 9. Return result
    return { code, landingPage, validation, ... };
  }
}
```

**Testing Checkpoint 7**: Service integration tests
```bash
npm run test:integration -- master-workflow
# ✅ Quota checked before job starts
# ✅ Job enqueued successfully
# ✅ Audit logs capture all actions
# ✅ Code validation runs on completion
# ✅ Iteration limits enforced
# ✅ Landing page included in output
```

**11. End-to-End Tests** (Week 8, Days 1-5)
Implement full workflow tests:
```typescript
describe('End-to-End Workflow', () => {
  it('should complete full workflow from PRD to handoff', async () => {
    // 1. Submit PRD
    const prd = await createTestPRD();

    // 2. Execute workflow
    const result = await masterWorkflow.executeWorkflow(prd);

    // 3. Verify code generation
    expect(result.code).toBeDefined();
    expect(result.code.files).toContain('App.tsx');

    // 4. Verify validation passed
    expect(result.validation.overall_status).toBe('passed');

    // 5. Verify landing page generated
    expect(result.landingPage).toBeDefined();
    expect(result.landingPage.components).toHaveLength(8);

    // 6. Verify audit trail
    const auditLogs = await auditService.getAuditTrail(userId);
    expect(auditLogs).toContainEqual(expect.objectContaining({
      action: 'workflow_completed',
    }));

    // 7. Verify project ZIP created
    expect(result.projectZip).toBeDefined();
    expect(result.projectZip.size).toBeGreaterThan(0);
  });
});
```

**Testing Checkpoint 8**: End-to-end tests
```bash
npm run test:e2e
# ✅ PRD → Code generation → Validation → Landing page → Handoff
# ✅ Visual validation passes (Playwright screenshots)
# ✅ All quality gates pass
# ✅ Project ZIP includes all files
# ✅ Workflow completes in < 10 minutes
```

**12. CI/CD Pipeline** (Week 8, Days 6-7)
Set up GitHub Actions:
```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run unit tests
        run: npm run test:unit
      - name: Run integration tests
        run: npm run test:integration
      - name: Run E2E tests
        run: npm run test:e2e
```

---

**Handoff Points**:
- **Deliver to Codex**: Test harness, test templates, integration test results
- **Deliver to Gemini**: PRD validation schemas, component test requirements
- **Receive from Codex**: Tested components ready for integration
- **Receive from Gemini**: Design tokens, architectural decisions

**Success Criteria**:
- [ ] All 8 testing checkpoints passed
- [ ] 90%+ code coverage on services
- [ ] E2E tests pass consistently
- [ ] CI/CD pipeline green

**Your Timeline**:
- **Weeks 1-2**: Phase 1 (Database + Core Services)
- **Weeks 3-4**: Phase 2 (Quality Gates)
- **Weeks 5-6**: Phase 3 Support (Test infrastructure for Codex)
- **Weeks 7-8**: Phase 4 (Integration + E2E)

**Getting Started**:
1. Run database migrations first (everything depends on this)
2. Implement services in order (audit/queue before quota/validation)
3. Test each service individually before integration
4. Provide test harness to Codex before Phase 3 starts
5. Monitor all agent progress and coordinate handoffs

Let's build infrastructure that scales! ⚙️
```

---

### 🖊️ CURSOR PROMPT

```
# CONTEXT: Design-First Software Factory - IDE Integration & Debugging

You are the **real-time coding assistant** for the Design-First Software Factory. This factory accelerates the journey from idea to production-ready Expo apps by using AI to generate pixel-perfect code from approved designs.

## YOUR ROLE: Real-Time Editing, Refactoring & Debugging

**What You're Building**: You're not building features from scratch—you're the **finishing touch** that makes everything work smoothly. You handle quick fixes, refactoring, debugging, and code navigation.

**Your Strengths**:
- Real-time code editing in IDE
- Refactoring and code cleanup
- Debugging sessions
- Code navigation and search
- Inline suggestions

**Your Deliverables**:

You don't have scheduled deliverables like the other agents. Instead, you're **on-demand support** throughout all phases.

**When You're Called**:

### 1. Debugging Component Rendering Issues (Phase 3)
**Scenario**: Codex reports "HeroSplit component not rendering on Android"

**Your Actions**:
```typescript
// Cursor: Check the component file
// 1. Navigate to src/components/landing-page/heroes/HeroSplit.tsx
// 2. Look for platform-specific code issues

// Common issues you'll fix:
// ❌ Bad: Hardcoded iOS value
<View style={{ marginTop: 32 }}>

// ✅ Good: Platform-aware value
import { Platform } from 'react-native';
<View style={{ marginTop: Platform.select({ ios: 32, android: 28, web: 48 }) }}>

// 3. Run the component in isolation
npm run expo start --android
```

### 2. Refactoring Duplicate Code (All Phases)
**Scenario**: Claude notices duplicate validation logic across services

**Your Actions**:
```typescript
// Cursor: Extract common validation logic

// Before (duplicated in 3 services):
if (!userId || userId.trim() === '') {
  throw new Error('User ID is required');
}

// After (single utility):
// src/utils/validation.ts
export function validateUserId(userId: string): void {
  if (!userId || userId.trim() === '') {
    throw new Error('User ID is required');
  }
}

// Refactor all 3 services to use the utility
// Use Cursor's multi-file edit capability
```

### 3. Quick Bug Fixes (All Phases)
**Scenario**: CI/CD pipeline fails due to TypeScript error

**Your Actions**:
```bash
# Cursor: Check the CI error log
# Error: Property 'projectId' does not exist on type 'JobData'

# Navigate to the error location
# Add the missing property to the type definition
interface JobData {
  userId: string;
  projectId: string; // ← Add this
  prdData: PRDInput;
}
```

### 4. Code Navigation & Search (All Phases)
**Scenario**: Any agent asks "Where is the quota limit defined?"

**Your Actions**:
```bash
# Cursor: Use code search
# Cmd+Shift+F (Mac) or Ctrl+Shift+F (Windows)
# Search: "projects_limit"

# Results:
# 1. src/services/quota.service.ts:47
# 2. supabase/migrations/20250108_004_create_usage_quotas.sql:12
# 3. __tests__/quota.service.test.ts:23

# Navigate to quota.service.ts and show the agent
```

### 5. Performance Optimization (Phase 4)
**Scenario**: E2E tests show workflow taking 12 minutes (target: <10 minutes)

**Your Actions**:
```typescript
// Cursor: Profile the workflow and optimize bottlenecks

// 1. Add timing logs
console.time('Code Generation');
await this.generateCode(prdData);
console.timeEnd('Code Generation'); // 8 minutes

// 2. Identify bottleneck: Synchronous file writes
// Before:
for (const file of files) {
  await fs.writeFile(file.path, file.content);
}

// After: Parallel writes
await Promise.all(
  files.map(file => fs.writeFile(file.path, file.content))
);
// Now: 2 minutes
```

### 6. Test Debugging (All Phases)
**Scenario**: Codex's Playwright test failing intermittently

**Your Actions**:
```typescript
// Cursor: Debug the flaky test

// 1. Add debug logging
test('HeroSplit renders on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // Debug: Check if page loaded
  await page.waitForLoadState('networkidle');
  console.log('Page loaded:', await page.title());

  // Debug: Check if element exists
  const headline = page.locator('[data-testid="hero-headline"]');
  console.log('Headline visible:', await headline.isVisible());

  await expect(page).toHaveScreenshot('hero-split-mobile.png');
});

// 2. Identify issue: Race condition
// Fix: Add explicit wait
await page.waitForSelector('[data-testid="hero-headline"]');
```

**Handoff Points**:
- **Receive from Any Agent**: Bug reports, refactoring requests, debugging requests
- **Deliver to Any Agent**: Fixed code, refactored code, debugging insights

**Success Criteria**:
- [ ] All agent-reported bugs fixed within 1 hour
- [ ] Refactoring improves code quality scores
- [ ] Debugging sessions resolve issues completely
- [ ] Code navigation requests answered within 5 minutes

**Your Workflow**:
1. **Monitor all agent conversations** for keywords: "error", "bug", "not working", "slow", "failing"
2. **Jump in proactively** when you see opportunities to help
3. **Ask clarifying questions**: "Can you share the error message?" or "What file is this in?"
4. **Fix quickly**: Use inline edits, multi-file refactoring, or debugging tools
5. **Verify fix**: Run tests, check CI/CD, or ask agent to confirm

**Common Patterns You'll Handle**:

| Issue Type | Frequency | Typical Fix Time | Example |
|------------|-----------|------------------|---------|
| TypeScript errors | High | 5-10 min | Missing type definitions |
| Platform-specific bugs | Medium | 15-30 min | iOS vs Android styling |
| Flaky tests | Medium | 20-40 min | Race conditions, timing |
| Performance issues | Low | 30-60 min | Async optimization |
| Code duplication | Medium | 10-20 min | Extract utility functions |

**Tools You'll Use**:
- **Cmd+Click**: Navigate to definition
- **Cmd+Shift+F**: Global search
- **Cmd+P**: Quick file open
- **F12**: Go to definition
- **Shift+F12**: Find all references
- **Debugger**: Breakpoints, watch expressions
- **Git Blame**: When did this code change?

**Questions to Ask When Called**:
- "Can you share the full error message?"
- "What file and line number?"
- "What were you trying to do when this happened?"
- "Does this happen consistently or intermittently?"
- "What have you already tried?"

**Your Timeline**: All 8 weeks (on-demand)
- Be most active during Phase 3-4 (integration complexity)
- Expect more debugging requests as components integrate
- Performance optimization needed in Phase 4

**Getting Started**:
1. Keep your IDE open with the full codebase loaded
2. Monitor conversations for keywords: "error", "bug", "failing"
3. Jump in with "I can help debug that!" when issues arise
4. Fix fast, verify thoroughly

Let's keep the code clean and running smoothly! 🖊️
```

---

## Communication & Coordination

### Daily Standups (Async)
Each agent posts daily status in a shared document:
```
DATE: 2025-01-15
AGENT: Claude

YESTERDAY:
- ✅ Completed database migrations (5 tables)
- ✅ Implemented audit service
- 🚧 Started job queue service (70% complete)

TODAY:
- Finish job queue service
- Write unit tests for job queue
- Run Testing Checkpoint 2

BLOCKERS:
- None

NEEDS FROM OTHER AGENTS:
- Gemini: Will need design token schema for Phase 3 (week 5)
```

### Testing Checkpoint Reviews
After each checkpoint, all agents review results:
```
CHECKPOINT 2: Core Services (Job Queue)
DATE: 2025-01-17
LEAD: Claude

RESULTS:
✅ Can enqueue jobs
✅ Can process jobs
✅ Progress updates correctly
✅ Failed jobs retry with exponential backoff
✅ Can cancel jobs

STATUS: PASSED ✅

SIGN-OFF:
- Claude: ✅ Tests passing, ready for Phase 2
- Cursor: ✅ Code quality reviewed, no issues
- Gemini: ✅ Architecture approved
- Codex: ⏸️ Not involved in this checkpoint
```

### Integration Handoffs
When one agent delivers to another:
```
FROM: Gemini
TO: Codex
DATE: 2025-01-22 (Phase 3 Kickoff)

DELIVERABLE: Design tokens for all 15 landing page components

FILES:
- src/constants/design-tokens.ts
- src/constants/design-tokens.ios.ts
- src/constants/design-tokens.android.ts
- src/constants/design-tokens.web.ts

VALIDATION:
✅ All colors meet WCAG AA contrast (4.5:1)
✅ Typography scales respect platform conventions
✅ Spacing values tested on 375px, 768px, 1440px
✅ Border radius values tested on all platforms

NEXT STEPS:
Codex: Use these tokens in all 15 components
Claude: Will validate token usage in integration tests

STATUS: READY FOR USE ✅
```

---

## Risk Mitigation

### Risk 1: Phase Dependencies Block Progress
**Mitigation**:
- Claude completes Phase 1-2 before Phase 3 starts (hard dependency)
- Codex can prototype components during Phase 1-2 using placeholder tokens
- Gemini generates design tokens early (Phase 3 Day 1) to unblock Codex

### Risk 2: Testing Checkpoint Failures
**Mitigation**:
- DO NOT proceed to next phase if checkpoint fails
- Cursor jumps in to debug failing tests
- All agents review failure together
- Fix before moving forward

### Risk 3: Integration Issues in Phase 4
**Mitigation**:
- Each service tested individually in Phases 1-2
- Components tested individually in Phase 3
- Integration tests written progressively (not all at end)
- Daily integration smoke tests starting Week 7

### Risk 4: Agent Availability/Blocking
**Mitigation**:
- All agents update daily status
- If agent blocked >24hrs, escalate to user
- Cross-train: Cursor can handle simple component fixes, Claude can review PRD logic

---

## Success Metrics

### Phase 1 Success (Weeks 1-2)
- [ ] 5 database tables created and tested
- [ ] Audit service operational (logs to database)
- [ ] Job queue service operational (enqueues, processes, retries)
- [ ] 90%+ unit test coverage on services
- [ ] Testing Checkpoints 1-2 passed

### Phase 2 Success (Weeks 3-4)
- [ ] Quota service enforces tier limits
- [ ] Code validation runs all 4 checks (ESLint, TS, Semgrep, npm audit)
- [ ] Error recovery handles failures gracefully
- [ ] Iteration service prevents infinite loops
- [ ] 90%+ unit test coverage on quality gates
- [ ] Testing Checkpoints 3-4 passed

### Phase 3 Success (Weeks 5-6)
- [ ] 15 landing page components built and tested
- [ ] All components render on iOS, Android, Web
- [ ] Accessibility audit passes (WCAG AA)
- [ ] Performance targets met (< 3s load on 3G)
- [ ] Visual regression tests baseline captured
- [ ] Testing Checkpoints 5-6 passed

### Phase 4 Success (Weeks 7-8)
- [ ] All services integrated into master workflow
- [ ] Landing page generation works end-to-end
- [ ] E2E tests pass consistently
- [ ] Workflow completes in < 10 minutes
- [ ] CI/CD pipeline green
- [ ] Testing Checkpoints 7-8 passed
- [ ] **READY FOR PRODUCTION** 🚀

---

## Next Steps

1. **User**: Copy/paste the 4 agent prompts into respective agents
2. **Claude**: Begin Phase 1 (database migrations) immediately
3. **Gemini**: Review architecture docs, prepare for Phase 3 kickoff
4. **Codex**: Review component specs, prepare test environment
5. **Cursor**: Monitor all agents, ready to debug

**First Command** (Claude):
```bash
cd design-first-software-factory
npm run db:migrate
npm run test:unit -- audit.service.test.ts
```

Let's execute with precision! 🎯
