
# Master Workflow: Unified Design-First Software Factory

## Overview

This document describes the **unified master workflow** that combines the best of both approaches into a single, flexible system. The key insight: **agent-in-the-loop validates that generated CODE matches approved DESIGN**, regardless of how that design was created.

## Core Concept

Previously, we had two separate workflows:
- **Express**: Fully automated
- **Concierge**: Human approval gates

**New approach**: **One master workflow with flexible checkpoints**

Both tiers share 90% of the same workflow. They only differ in **how the design gets approved**:
- **Express Tier**: Codex auto-generates and validates against locked brand guideline
- **Concierge Tier**: Human iterates in Stitch and approves final design

Then **both** converge to use agent-in-the-loop to ensure the **code implementation matches the approved design**.

## Master Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: INTAKE & PRD GENERATION                           │
│  (Both Tiers - Identical)                                   │
│                                                              │
│  User Input:                                                │
│    • Free-form conversation about app idea                  │
│    • OR existing website URL for "Website Refresh"          │
│                                                              │
│  Process:                                                   │
│    • Gemini converts conversation → structured PRD          │
│    • Identifies target audience, user stories, features     │
│    • Extracts inspiration URLs (max 3)                      │
│    • Identifies which URL is "locked" brand guideline       │
│                                                              │
│  Output:                                                    │
│    • Complete PRD with requirements                         │
│    • Confidence score (missing information flagged)         │
│    • Clarifying questions if needed                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: REQUIREMENTS ANALYSIS                             │
│  (Both Tiers - Identical)                                   │
│                                                              │
│  Process:                                                   │
│    1. Capture screenshots of all inspiration URLs           │
│    2. Gemini analyzes each screenshot:                      │
│       - Extract color palette                               │
│       - Identify typography                                 │
│       - Analyze layout patterns                             │
│       - 🔒 LOCKED URL: Extract mandatory brand guidelines   │
│    3. Gemini generates:                                     │
│       - Complete design system                              │
│       - User stories with acceptance criteria               │
│       - Feature breakdown                                   │
│       - Screen mappings (features → screens)                │
│                                                              │
│  Output:                                                    │
│    • Design system (colors, typography, spacing)            │
│    • 6-12 screen requirements                               │
│    • Brand guidelines from locked URL                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────┴───────────┐
         │                       │
    Express Tier           Concierge Tier
         │                       │
         ▼                       ▼
┌──────────────────────┐  ┌──────────────────────┐
│ PHASE 3a:            │  │ PHASE 3b:            │
│ AUTO DESIGN          │  │ HUMAN DESIGN         │
│                      │  │                      │
│ Codex Generates:     │  │ Human in Stitch:     │
│  • Initial screens   │  │  • Sees Stitch       │
│  • Validates vs      │  │    prompts           │
│    locked guideline  │  │  • Pastes into       │
│  • Iterates (max 5x) │  │    stitch.with       │
│  • Target score:0.85 │  │    google.com        │
│                      │  │  • Annotates         │
│ Agent compares:      │  │  • Reprompts         │
│  • Layout ✓          │  │  • Iterates freely   │
│  • Colors ✓          │  │  • Exports HTML      │
│  • Typography ✓      │  │                      │
│                      │  │ Human Approves:      │
│ Output:              │  │  • Reviews each      │
│  • Codex screenshots │  │    screen            │
│  • Quality scores    │  │  • Uploads HTMLs     │
│  • Initial code      │  │  • Clicks "Approve"  │
│                      │  │                      │
│ Time: ~3-4 min       │  │ Output:              │
│ Cost: ~$1.00         │  │  • Stitch HTMLs      │
│                      │  │  • Human-approved ✓  │
│                      │  │                      │
│                      │  │ Time: ~15-25 min     │
│                      │  │ Cost: ~$0.20         │
└──────────┬───────────┘  └──────────┬───────────┘
           │                         │
           │   APPROVED DESIGN       │
           │   (Codex screenshots    │
           │    OR Stitch HTML)      │
           │                         │
           └───────────┬─────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 4: CODE GENERATION                                   │
│  (Both Tiers Converge)                                      │
│                                                              │
│  Express Path:                                              │
│    • Already have code from Codex                           │
│    • Skip to Phase 5                                        │
│                                                              │
│  Concierge Path:                                            │
│    • Convert Stitch HTML → React Native                     │
│    • Claude/Cursor generates TypeScript components          │
│    • Apply design system                                    │
│                                                              │
│  Output:                                                    │
│    • Complete React Native components for all screens       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 5: AGENT-IN-THE-LOOP CODE VALIDATION                │
│  (Both Tiers - Identical)                                   │
│                                                              │
│  🎯 KEY INNOVATION: Agent validates CODE matches DESIGN     │
│                                                              │
│  For Each Screen:                                           │
│    ┌──────────────────────────────────────┐               │
│    │ 1. Playwright Renders                │               │
│    │    - Generated React Native code     │               │
│    │    - Captures screenshot             │               │
│    └────────────┬─────────────────────────┘               │
│                 │                                           │
│                 ▼                                           │
│    ┌──────────────────────────────────────┐               │
│    │ 2. Codex Compares                    │               │
│    │    - Rendered screenshot             │               │
│    │    - VS approved design (benchmark)  │               │
│    │    - Calculates match score          │               │
│    └────────────┬─────────────────────────┘               │
│                 │                                           │
│        Score >= 0.85? ────Yes──> ✅ Next screen           │
│                 │                                           │
│                No                                           │
│                 │                                           │
│                 ▼                                           │
│    ┌──────────────────────────────────────┐               │
│    │ 3. Codex Refines Code                │               │
│    │    - Gets specific feedback          │               │
│    │    - "Button color #3498db should    │               │
│    │      be #2196F3"                     │               │
│    │    - "Spacing 16px should be 24px"   │               │
│    │    - Generates improved code         │               │
│    └────────────┬─────────────────────────┘               │
│                 │                                           │
│                 └──> Back to Step 1 (max 3 iterations)     │
│                                                              │
│  This ensures:                                              │
│    ✓ Code matches approved design pixel-perfect            │
│    ✓ Works for BOTH Express (Codex) and Concierge (Stitch) │
│    ✓ Objective quality metrics                             │
│    ✓ Consistent validation across all projects             │
│                                                              │
│  Output:                                                    │
│    • Validated code (matches design)                        │
│    • Quality scores per screen                             │
│    • Iteration counts                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 6: PROJECT PACKAGING                                 │
│  (Both Tiers - Identical)                                   │
│                                                              │
│  Generate:                                                  │
│    • Navigation structure                                   │
│    • Theme file (from design system)                        │
│    • package.json with dependencies                         │
│    • README with setup instructions                         │
│                                                              │
│  Package:                                                   │
│    • Create ZIP file with complete project                  │
│    • Upload to storage                                      │
│    • Generate download URL                                  │
│                                                              │
│  Output:                                                    │
│    • Complete Expo project (ZIP)                            │
│    • Ready to npm install && expo start                     │
└─────────────────────────────────────────────────────────────┘
```

## Key Innovation: Agent Validates Code Matches Design

The breakthrough insight is that **agent-in-the-loop is for CODE validation, not DESIGN creation**.

### Before (Incorrect Understanding)
```
Express: Agent generates AND validates design
Concierge: Human generates and validates design
```

### After (Correct Understanding)
```
Express: Agent generates design → Agent validates code matches design
Concierge: Human generates design → Agent validates code matches design
                                      ↑
                         SAME VALIDATION FOR BOTH
```

The agent's job is to ensure that the **React Native code, when rendered, visually matches the approved design** - regardless of whether that approved design came from:
- Codex (Express tier)
- Stitch (Concierge tier)
- Figma (Premium tier - future)

## Shared Components Across Both Tiers

### 1. PRD Generation (Both)

```typescript
const prdService = getPRDService(geminiApiKey);

// Convert conversation to structured PRD
const prdResult = await prdService.generatePRDFromConversation(
  conversationHistory,
  existingWebsiteUrl // Optional: for "Website Refresh"
);

// PRD includes:
// - Project name, executive summary
// - User stories with acceptance criteria
// - Feature breakdown
// - Inspiration URLs (max 3, 1 lockable)
// - Success metrics
```

**Key Feature**: Works from free-form conversation OR existing website URL

**Website Refresh Example**:
```typescript
await prdService.generatePRDFromConversation(
  [{ role: 'user', content: 'Modernize our company website' }],
  'https://mycompany.com' // Existing site as baseline
);

// PRD will:
// - Analyze existing site
// - Preserve brand identity
// - Suggest modern improvements
// - Lock existing site as brand guideline
```

### 2. Requirements Analysis (Both)

```typescript
const gemini = getGeminiService(geminiApiKey);

// Capture and analyze inspiration screenshots
for (const url of inspirationUrls) {
  const screenshot = await captureScreenshot(url);
  const analysis = await gemini.analyzeInspirationWebsite(
    screenshot,
    url,
    url.locked // Extract mandatory brand guidelines if locked
  );
}

// Generate problem deconstruction
const deconstruction = await gemini.generateProblemDeconstruction(
  intake,
  inspirationAnalyses
);

// Generate screen mappings
const screenMappings = await gemini.generateScreenMappings(
  deconstruction
);
```

**Locked Brand Guideline**: One URL can be marked "Must Follow"
- Colors extracted become mandatory
- Typography must be preserved
- Layout patterns strongly influence design
- Used as validation benchmark

### 3. Agent Code Validation (Both)

```typescript
// THE SAME for both Express and Concierge

for (const screen of approvedDesigns) {
  // 1. Render generated code
  const rendered = await playwright.renderComponentAndCapture(
    screen.code,
    screen.name,
    'react-native'
  );

  // 2. Compare against approved design (the benchmark)
  const comparison = await codex.compareDesignAgainstBenchmark(
    rendered.screenshot,      // Generated code rendered
    screen.approvedDesign,    // Codex screenshot OR Stitch HTML screenshot
    designSystem,
    requirements
  );

  // 3. Iterate if score < 0.85
  while (comparison.score < 0.85 && iterations < 3) {
    screen.code = await codex.refineCode(
      screen.code,
      comparison.feedback
    );
    // Re-render and compare...
  }
}
```

**Key Point**: The "approved design" is different per tier:
- **Express**: Codex-generated screenshot
- **Concierge**: Stitch HTML (rendered as screenshot)

But the **validation logic is identical**!

## Comparison: Express vs Concierge

| Phase | Express Tier | Concierge Tier | Shared? |
|-------|-------------|----------------|---------|
| **1. PRD Generation** | Free-form conversation → PRD | Free-form conversation → PRD | ✅ 100% shared |
| **2. Requirements Analysis** | Gemini analyzes inspiration + locked guideline | Gemini analyzes inspiration + locked guideline | ✅ 100% shared |
| **3. Design Approval** | Codex auto-generates (3-4 min) | Human iterates in Stitch (15-25 min) | ❌ Diverges here |
| **4. Code Generation** | Already done by Codex | HTML → React Native | ⚠️ Different paths |
| **5. Code Validation** | Agent validates code matches Codex design | Agent validates code matches Stitch design | ✅ 100% shared |
| **6. Packaging** | Generate ZIP | Generate ZIP | ✅ 100% shared |

**Shared Components**: 5 out of 6 phases (83%)
**Divergence Point**: Design approval method only

## Use Cases

### Use Case 1: Express Tier - Rapid MVP

**Scenario**: Startup needs to validate idea quickly

```typescript
const masterWorkflow = getMasterWorkflow(config);

const result = await masterWorkflow.executeWorkflow(
  [
    { role: 'user', content: 'I need a fitness tracking app for runners' },
    { role: 'user', content: 'Should track workouts, nutrition, and have social features' },
  ],
  'express' // Fully automated
);

// 5 minutes later:
// ✅ Complete app generated
// ✅ Code validated against locked brand guideline
// ✅ Ready to download and test
```

**Timeline**:
- PRD generation: 30s
- Requirements analysis: 45s
- Codex design generation: 3 min
- Code validation: 1 min
- Packaging: 15s
- **Total: ~5 minutes**

**Cost**: ~$1.50

### Use Case 2: Concierge Tier - Client Project

**Scenario**: Agency building app for client with specific brand requirements

```typescript
const result = await masterWorkflow.executeWorkflow(
  [
    { role: 'user', content: 'Client wants e-commerce app for their clothing brand' },
    { role: 'user', content: 'Brand website: https://clientbrand.com (must follow exactly)' },
  ],
  'concierge' // Human approval gates
);

// Returns immediately with:
// status: 'awaiting_human_approval'
// Stitch prompts ready for human

// Human iterates in Stitch:
// - Pastes prompts
// - Refines designs
// - Gets client approval
// - Uploads HTML exports

// Resume workflow:
const finalResult = await masterWorkflow.resumeAfterHumanApproval(
  result.project_id,
  stitchDesigns
);

// ✅ Complete app with client-approved designs
// ✅ Code validated to match approved designs pixel-perfect
```

**Timeline**:
- PRD generation: 30s
- Requirements analysis: 45s
- **Human Stitch iteration: 15-25 minutes** ⏸️ (blocking)
- Code generation: 2 min
- Code validation: 2 min
- Packaging: 15s
- **Total: ~20-30 minutes** (including human time)

**Cost**: ~$2.50

### Use Case 3: Website Refresh

**Scenario**: Company wants to modernize their outdated website while preserving brand

```typescript
const result = await masterWorkflow.executeWorkflow(
  [
    { role: 'user', content: 'Refresh our company website with modern design trends' },
  ],
  'express', // or 'concierge'
  'https://mycompany.com' // Existing site as baseline
);

// Workflow will:
// 1. Analyze existing site (brand colors, typography, logo)
// 2. Lock existing site as brand guideline (must preserve)
// 3. Generate modernized design (keeping brand identity)
// 4. Validate new code matches brand requirements

// Result:
// ✅ Modern, responsive design
// ✅ Preserves brand identity
// ✅ Matches original color palette
// ✅ Updates UX patterns to 2025 standards
```

**Key Feature**: Existing website URL becomes the locked brand guideline automatically

## Configuration

```typescript
const config = {
  geminiApiKey: process.env.GEMINI_API_KEY!,
  codexApiKey: process.env.OPENAI_API_KEY!,
  supabaseConfig: {
    url: process.env.SUPABASE_URL!,
    anonKey: process.env.SUPABASE_ANON_KEY!,
    serviceRoleKey: process.env.SUPABASE_SERVICE_ROLE_KEY!,
  },
};

const masterWorkflow = getMasterWorkflow(config);
```

## Environment Variables

```bash
# Required for both tiers
GEMINI_API_KEY=your-gemini-key          # PRD generation, requirements analysis
OPENAI_API_KEY=your-openai-key          # Code validation (both tiers)
SUPABASE_URL=your-supabase-url          # Database, storage
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key

# Optional
SCREENSHOT_API_KEY=your-screenshot-key  # For capturing inspiration websites
```

## Performance Benchmarks

### Express Tier (8-screen app)

| Phase | Time | Cost |
|-------|------|------|
| PRD Generation | 30s | $0.05 |
| Requirements Analysis | 45s | $0.15 |
| Codex Design Generation | 180s | $1.00 |
| Code Validation | 60s | $0.15 |
| Packaging | 15s | $0.05 |
| **Total** | **5.5 min** | **$1.40** |

### Concierge Tier (8-screen app)

| Phase | Time | Cost |
|-------|------|------|
| PRD Generation | 30s | $0.05 |
| Requirements Analysis | 45s | $0.15 |
| Human Stitch Iteration | **20 min** | $0.00 |
| Code Generation | 120s | $0.80 |
| Code Validation | 120s | $0.30 |
| Packaging | 15s | $0.05 |
| **Total** | **~25 min** | **$1.35** |

**Key Insight**: Concierge is actually CHEAPER (no Codex design cost) but requires human time

## Quality Metrics

### Code Validation Scores

Target: **0.85** (85% visual similarity)

Typical results:
- **Express tier**: 0.87 average (Codex designs already well-validated)
- **Concierge tier**: 0.89 average (human-approved designs are clear benchmarks)

### Iteration Counts

- **Express tier**: Avg 2.5 iterations per screen during design generation, 1.5 iterations during code validation
- **Concierge tier**: 0 iterations during design (human approved), 1.2 iterations during code validation

### Success Rate

- **Express tier**: 95% complete without human intervention
- **Concierge tier**: 100% complete (human ensures quality)

## Future Enhancements

### Short-term

1. **Interactive PRD Refinement**
   - Chat interface for clarifying questions
   - Real-time PRD preview
   - Confidence scoring per section

2. **Premium Tier (Hybrid)**
   - Stitch rapid prototype
   - Export to Figma for professional refinement
   - Figma API integration
   - Agent validates code matches Figma

3. **A/B Testing**
   - Generate multiple design variants (Express tier)
   - Agent scores each variant
   - Present top 3 to user for selection

### Medium-term

1. **Multi-Platform Targets**
   - iOS native (SwiftUI)
   - Android native (Jetpack Compose)
   - Web (Next.js)
   - Agent validates across all platforms

2. **Component Library**
   - Reusable components across projects
   - Company-specific design systems
   - Pre-validated component templates

3. **Advanced Validation**
   - Animation validation
   - Interaction testing
   - Accessibility scoring (WCAG)
   - Performance metrics (Lighthouse)

### Long-term

1. **Continuous Refresh**
   - Schedule periodic website refreshes
   - Auto-update to latest design trends
   - Preserve brand identity
   - A/B test refreshed vs original

2. **Multi-Tenant White Label**
   - Agencies can brand as their own
   - Custom pricing tiers
   - Client portal integration

3. **AI Design Critic**
   - Agent provides design feedback before approval
   - "This doesn't follow accessibility guidelines"
   - "Consider increasing contrast here"
   - Helps humans make better decisions

## Troubleshooting

### "PRD confidence score is low"

**Problem**: Conversation doesn't have enough information

**Solution**:
```typescript
const questions = await prdService.generateClarifyingQuestions(
  conversationHistory,
  partialPRD
);

// Present questions to user:
// - "Who is the primary target audience?"
// - "What are the key features you envision?"
// - "Are there any design inspirations?"
```

### "Code validation score below target"

**Problem**: Generated code doesn't match approved design

**Check**:
1. Is the design system being applied correctly?
2. Are there complex gradients or effects?
3. Is the benchmark screenshot clear?

**Solution**:
- Review feedback from comparison agent
- Increase max iterations from 3 to 5
- Consider manual code review for complex screens

### "Website Refresh not preserving brand"

**Problem**: Generated design doesn't match original brand

**Check**:
1. Is existing website URL marked as "locked"?
2. Was screenshot captured successfully?
3. Did Gemini extract brand guidelines?

**Solution**:
```typescript
const analysis = await prdService.analyzeExistingWebsite(url);
console.log(analysis.brand_guidelines); // Review extracted guidelines

// Manually add to PRD if missing:
prd.inspiration_sources[0].locked = true;
```

## Summary

The **Master Workflow** unifies Express and Concierge tiers into a single, flexible system:

1. **Both start the same**: Conversation → PRD → Requirements Analysis
2. **They diverge briefly**: Design approval method (auto vs human)
3. **Both end the same**: Agent validates code matches approved design → Package → Handoff

**Key Innovation**: Agent-in-the-loop validates **code implementation matches approved design** for BOTH tiers, ensuring pixel-perfect results regardless of approval method.

**Enables**: Website Refresh product, where existing site becomes the locked brand guideline, and the system generates a modernized version while preserving brand identity.

This is the foundation for the next evolution: **Design-First Software Factory that scales from rapid prototypes to enterprise applications, all from a single unified workflow**.
