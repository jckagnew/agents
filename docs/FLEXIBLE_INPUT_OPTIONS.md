# Flexible Input Options Guide

## Overview

The Design-First Software Factory supports multiple input methods and website refresh modes to accommodate different use cases and customer needs. This document explains all available options.

## PRD Input Flexibility

### Three Ways to Provide Requirements

#### 1. Generate PRD from Conversation (Most Common)

**Use Case**: Client has an idea but no formal documentation

```typescript
const prdService = getPRDService(geminiApiKey);

const result = await prdService.processPRDInput(
  PRDInputType.GENERATE,
  {
    conversation: [
      { role: 'user', content: 'I need a fitness tracking app' },
      { role: 'user', content: 'Should track workouts and nutrition' },
      { role: 'user', content: 'Target audience is runners aged 25-40' }
    ]
  }
);

// AI generates complete PRD from conversation
// Extracts user stories, features, success metrics
```

**Advantages**:
- Low barrier to entry
- No documentation needed
- Natural conversation flow
- AI fills in implied requirements

**Best For**:
- New projects without documentation
- Early-stage ideas
- Non-technical stakeholders

#### 2. Import Existing PRD Document

**Use Case**: Client has a formal PRD already written

```typescript
// Option A: Import markdown/text PRD
const prdDocument = `
# Fitness Tracker App

## Executive Summary
A mobile app for runners to track workouts...

## User Stories
1. As a runner, I want to track my daily runs...
`;

const result = await prdService.processPRDInput(
  PRDInputType.IMPORT,
  {
    prdDocument: prdDocument
  }
);

// Option B: Import structured PRD object
const existingPRD = {
  project_name: 'Fitness Tracker',
  executive_summary: '...',
  user_stories: [...],
  features: [...]
};

const result = await prdService.processPRDInput(
  PRDInputType.IMPORT,
  {
    existingPRD: existingPRD
  }
);

// AI parses and validates the PRD
// Identifies missing information
// Generates clarifying questions
```

**Advantages**:
- Preserves existing documentation work
- Faster than conversation
- Can import from various formats (markdown, JSON, etc.)
- Validates completeness

**Best For**:
- Projects with existing documentation
- Enterprise clients with formal processes
- Handoffs from product managers

#### 3. Augment Partial PRD (Hybrid Approach)

**Use Case**: Client has some requirements but needs help completing them

```typescript
// Start with partial PRD
const partialPRD = {
  project_name: 'Fitness Tracker',
  target_audience: { primary: 'Runners aged 25-40' },
  features: [
    { id: 'f1', name: 'Workout Tracking', description: '...' }
  ]
  // Missing: user stories, success metrics, etc.
};

// Fill in gaps via conversation
const result = await prdService.processPRDInput(
  PRDInputType.AUGMENT,
  {
    existingPRD: partialPRD,
    conversation: [
      { role: 'user', content: 'Also need nutrition tracking' },
      { role: 'user', content: 'Social features for sharing runs' }
    ]
  }
);

// AI:
// 1. Preserves ALL existing PRD content
// 2. Uses conversation to fill missing sections
// 3. Expands on incomplete areas
// 4. Maintains consistency
```

**Advantages**:
- Best of both worlds
- Preserves existing work
- Interactive refinement
- Progressive disclosure

**Best For**:
- Projects with partial documentation
- Iterative requirements gathering
- When PRD needs expansion/clarification

### Confidence Scoring & Missing Information

All three methods return confidence scores:

```typescript
{
  prd: { ... },
  confidence: 0.85,  // 0.0 to 1.0
  missing_information: ['success_metrics', 'out_of_scope'],
  clarifying_questions: [
    'How will you measure success?',
    'What features are explicitly out of scope?'
  ]
}
```

**If confidence < 0.80**: System automatically generates clarifying questions

**Interactive Refinement**:
```typescript
// Present questions to user
const questions = result.clarifying_questions;

// User responds
const refinedResult = await prdService.refinePRD(
  result.prd,
  "Success metrics: 10k active users in 6 months",
  [...conversationHistory, newMessage]
);

// Repeat until confidence >= 0.80
```

## Website Refresh Modes

### Three Refresh Strategies

#### 1. Preserve Brand (Default)

**Use Case**: Company wants modern UX but must keep brand identity

```typescript
const result = await masterWorkflow.executeWorkflow(
  [{ role: 'user', content: 'Modernize our website' }],
  'express',  // or 'concierge'
  'https://company.com',
  WebsiteRefreshMode.PRESERVE_BRAND  // <-- Preserve brand
);

// Workflow:
// 1. Captures screenshot of existing site
// 2. Extracts brand (colors, typography, logo)
// 3. LOCKS brand as "Must Follow" guideline
// 4. Generates modern UX using existing brand
// 5. Validates new code matches brand requirements

// Result:
// ✅ Updated UX patterns (2025 standards)
// ✅ Preserved brand colors
// ✅ Preserved typography
// ✅ Preserved logo usage
// ✅ Modern responsiveness
// ❌ Does NOT change branding
```

**What Gets Preserved**:
- Color palette (exact hex codes)
- Typography (font families, weights, sizes)
- Logo and usage guidelines
- Brand voice/tone (from content analysis)

**What Gets Updated**:
- Layout patterns → modern standards
- Navigation structure → improved UX
- Responsive design → mobile-first
- Performance → optimized
- Accessibility → WCAG compliant

**Best For**:
- Established brands (don't want to confuse customers)
- Recent rebrand (invested in current brand)
- Regulated industries (brand consistency required)
- Franchises (brand guidelines from corporate)

#### 2. Refresh Brand (New Coat of Paint)

**Use Case**: Company wants to keep functionality but apply new branding

```typescript
const result = await masterWorkflow.executeWorkflow(
  [
    { role: 'user', content: 'Rebrand our website' },
    { role: 'user', content: 'Keep all current features and flows' },
    { role: 'user', content: 'Apply fresh, modern branding' }
  ],
  'concierge',  // Human creative control for brand
  'https://company.com',
  WebsiteRefreshMode.REFRESH_BRAND  // <-- New branding
);

// Workflow:
// 1. Analyzes existing site for screens/flows
// 2. Extracts information architecture
// 3. Maps user flows (e.g., Home → Products → Cart → Checkout)
// 4. Identifies navigation patterns
// 5. Preserves screen structure and functionality
// 6. Generates NEW brand identity (or applies provided brand)
// 7. Applies new brand to existing screens/flows

// Result:
// ✅ Same screens and user flows
// ✅ Same features and functionality
// ✅ Same information architecture
// ✅ ENTIRELY new branding (colors, fonts, style)
// ❌ Does NOT change UX flows
```

**What Gets Preserved**:
- All screens/pages (structure)
- User flows (navigation paths)
- Information architecture (content organization)
- Features and functionality
- Technical capabilities

**What Gets Replaced**:
- Color palette → new brand colors
- Typography → new fonts
- Logo → new logo design
- Visual style → new aesthetic
- Component styling → new look

**Best For**:
- Company rebranding (merger, new direction)
- Technical debt (features work, design doesn't)
- Acquired companies (apply parent brand to acquired site)
- Outdated brand (brand doesn't match market position)

**Example Scenario**:
```
Existing Site:
- E-commerce with 50 product pages
- 5-step checkout flow
- User account dashboard
- Blog with 200 articles

Refresh Brand Result:
- Same 50 product pages (NEW branding)
- Same 5-step checkout (NEW branding)
- Same dashboard (NEW branding)
- Same blog (NEW branding)
- Everything LOOKS different but WORKS the same
```

#### 3. Full Modernization

**Use Case**: Company wants to update BOTH UX and brand

```typescript
const result = await masterWorkflow.executeWorkflow(
  [{ role: 'user', content: 'Complete website overhaul' }],
  'concierge',
  'https://company.com',
  WebsiteRefreshMode.FULL_MODERNIZATION  // <-- Update everything
);

// Workflow:
// 1. Analyzes existing site (for reference only)
// 2. Extracts current brand and UX (as baseline)
// 3. Generates modern UX patterns
// 4. Generates fresh brand identity
// 5. Builds entirely new site

// Result:
// ✅ Modern UX (2025 standards)
// ✅ Fresh branding
// ✅ Improved user flows
// ✅ Updated information architecture
// ⚠️ Existing site used only as inspiration
```

**Best For**:
- Complete overhaul needed
- Startup pivoting
- Legacy site (5+ years old)
- Both brand and UX outdated

### Comparison Matrix

| Aspect | Preserve Brand | Refresh Brand | Full Modernization |
|--------|---------------|---------------|-------------------|
| **Brand Colors** | ✅ Preserved exactly | ❌ Replaced | ❌ New |
| **Typography** | ✅ Preserved | ❌ Replaced | ❌ New |
| **Logo** | ✅ Preserved | ❌ New logo | ❌ New logo |
| **Screen Structure** | ⚠️ Updated | ✅ Preserved | ⚠️ Redesigned |
| **User Flows** | ⚠️ Improved | ✅ Preserved | ⚠️ Redesigned |
| **Features** | ✅ Preserved | ✅ Preserved | ⚠️ Re-evaluated |
| **UX Patterns** | ❌ Modernized | ✅ Preserved | ❌ Modernized |
| **Use Case** | Brand consistency | Rebranding | Complete overhaul |
| **Risk Level** | Low | Medium | High |
| **Stakeholder Buy-in** | Easy | Requires approval | Extensive approval |

## Combined Example: All Options Together

### Scenario: E-commerce Company Rebrand

**Situation**:
- Company was acquired
- Need to apply parent company's brand
- Current site's features work well
- Have partial PRD from acquisition docs

**Implementation**:

```typescript
// Step 1: Import partial PRD from acquisition docs
const acquisitionPRD = {
  project_name: 'E-commerce Platform Rebrand',
  features: [
    { id: 'f1', name: 'Product Catalog', description: 'Working well, keep as-is' },
    { id: 'f2', name: 'Checkout Flow', description: '5-step process, preserve' },
    { id: 'f3', name: 'User Accounts', description: 'Dashboard and order history' }
  ],
  constraints: ['Must preserve all existing functionality'],
  // Missing: user stories, success metrics, etc.
};

// Step 2: Augment with conversation to fill gaps
const prdResult = await prdService.processPRDInput(
  PRDInputType.AUGMENT,  // <-- Start with partial, fill gaps
  {
    existingPRD: acquisitionPRD,
    conversation: [
      { role: 'user', content: 'Need to apply parent company brand' },
      { role: 'user', content: 'Parent brand: https://parentcompany.com' },
      { role: 'user', content: 'Success metric: Complete rebrand in 3 months' },
      { role: 'user', content: 'Must not disrupt existing customers' }
    ]
  }
);

// Step 3: Execute workflow with REFRESH_BRAND mode
const result = await masterWorkflow.executeWorkflow(
  prdResult.conversation_history,
  'concierge',  // Human approval for brand application
  'https://acquired-company.com',  // Existing site
  WebsiteRefreshMode.REFRESH_BRAND  // <-- Keep screens/flows, new brand
);

// Result:
// ✅ All existing features preserved
// ✅ User flows unchanged (no customer disruption)
// ✅ Parent company brand applied throughout
// ✅ Same screens, entirely new look
// ✅ Stakeholders approved new brand via Stitch
// ✅ 3-month timeline achievable
```

## Best Practices

### PRD Input Selection

**Choose GENERATE when**:
- Starting from scratch
- Client has no documentation
- Early exploration/discovery
- Stakeholders prefer conversation

**Choose IMPORT when**:
- Formal PRD exists
- Documentation already invested in
- Need to validate existing PRD
- Enterprise client with processes

**Choose AUGMENT when**:
- Have partial requirements
- PRD needs expansion
- Iterative refinement preferred
- Mix of documented + new requirements

### Website Refresh Mode Selection

**Choose PRESERVE_BRAND when**:
- Brand is recent (<2 years old)
- Strong brand recognition
- Just completed rebrand
- Regulated industry (consistency required)

**Choose REFRESH_BRAND when**:
- Company rebranding/merger
- Features work, design doesn't
- Acquiring company wants to apply their brand
- Outdated brand, working functionality

**Choose FULL_MODERNIZATION when**:
- Everything is outdated (5+ years)
- Complete overhaul needed
- Startup pivot
- Both UX and brand problems

## Advanced: Hybrid Combinations

### Example: Partial Rebrand

**Scenario**: Keep main brand, but modernize specific sections

```typescript
// Use PRESERVE_BRAND as base
const result = await masterWorkflow.executeWorkflow(
  conversation,
  'concierge',
  'https://company.com',
  WebsiteRefreshMode.PRESERVE_BRAND
);

// Then in Stitch (human approval):
// 1. Most screens: Apply existing brand (preserved)
// 2. New features: Modern brand evolution
// 3. Old features: Existing brand maintained

// Agent validates:
// - Old sections match existing brand
// - New sections have evolved brand
// - Consistent overall
```

### Example: Feature-Specific Refresh

**Scenario**: Add new features with new branding, preserve existing features

```typescript
// Augment existing PRD with new features
const augmented = await prdService.processPRDInput(
  PRDInputType.AUGMENT,
  {
    existingPRD: currentPRD,
    conversation: [
      { role: 'user', content: 'Add social features with fresh branding' },
      { role: 'user', content: 'Keep existing e-commerce sections as-is' }
    ]
  }
);

// Execute with custom instructions
// Agent will:
// - Preserve brand for existing features
// - Apply new brand to new features
// - Validate consistency
```

## Troubleshooting

### PRD Confidence Low

**Problem**: Generated PRD has confidence < 0.60

**Solution**:
```typescript
// Get clarifying questions
const questions = await prdService.generateClarifyingQuestions(
  conversationHistory,
  partialPRD
);

// Present to user:
// 1. "Who is the primary target audience?"
// 2. "What are the key success metrics?"
// 3. "Are there any technical constraints?"

// Refine PRD with answers
const refined = await prdService.refinePRD(
  currentPRD,
  answersToQuestions,
  updatedConversation
);
```

### Website Analysis Fails

**Problem**: Can't extract screens/brand from existing site

**Solutions**:
1. **Provide multiple screenshots**: Different pages/states
2. **Supply brand guidelines manually**: If available
3. **Use IMPORT + custom brand**: Skip analysis, provide brand directly
4. **Fallback to GENERATE**: Skip existing site entirely

### Conflicting Requirements

**Problem**: REFRESH_BRAND but also "preserve current design"

**Solution**: Clarify with user:
```typescript
const questions = [
  'You mentioned "refresh brand" but also "preserve design".',
  'Do you want to:',
  'A) Keep screens/flows but apply new branding (Refresh Brand)',
  'B) Keep brand but modernize UX (Preserve Brand)',
  'C) Something else?'
];
```

## Summary

The system offers maximum flexibility:

**PRD Input**:
- Generate (conversation)
- Import (existing docs)
- Augment (hybrid)

**Website Refresh**:
- Preserve Brand (modern UX, same brand)
- Refresh Brand (same screens, new brand)
- Full Modernization (update everything)

**All combinations work with both Express and Concierge tiers**.

This flexibility accommodates:
- Startups to enterprises
- No docs to formal PRDs
- Simple refreshes to complete overhauls
- Technical and non-technical stakeholders

**Key Principle**: Meet users where they are, adapt to their needs, provide guardrails and guidance.
