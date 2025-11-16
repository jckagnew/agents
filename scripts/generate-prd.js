#!/usr/bin/env node
/**
 * PRD (Product Requirements Document) Generator
 * Extends basic requirements into comprehensive spec bundle
 *
 * Generates:
 * - User personas with jobs-to-be-done
 * - Problem/Escape-Arrival framing
 * - Acceptance criteria
 * - System architecture outline
 * - UX flow documentation
 *
 * Usage:
 *   node scripts/generate-prd.js \
 *     --requirements session-X/requirements/iteration-0.json \
 *     --output-dir session-X/prd
 */

const fs = require('fs');
const path = require('path');

// Parse arguments
const args = process.argv.slice(2);
const getArg = (flag) => {
    const index = args.indexOf(flag);
    return index !== -1 ? args[index + 1] : null;
};

const requirementsFile = getArg('--requirements');
const outputDir = getArg('--output-dir');

if (!requirementsFile || !outputDir) {
    console.error('Usage: node generate-prd.js --requirements <path> --output-dir <path>');
    process.exit(1);
}

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// Read requirements
const requirements = JSON.parse(fs.readFileSync(requirementsFile, 'utf8'));

console.log('📋 Generating PRD Bundle...');
console.log(`   App: ${requirements.app_name}`);
console.log(`   Type: ${requirements.app_type}\n`);

// ============================================================================
// 1. USER PERSONAS
// ============================================================================

function generatePersonas(requirements) {
    const appType = requirements.app_type;
    const features = requirements.features?.must_have || [];

    // Template personas based on app type
    const personaTemplates = {
        health_tracking: {
            primary: {
                name: 'Health-Conscious Hannah',
                age: 32,
                occupation: 'Marketing Manager',
                goals: [
                    'Maintain healthy habits consistently',
                    'Track progress toward wellness goals',
                    'Feel accomplished and motivated'
                ],
                frustrations: [
                    'Forgets to track habits throughout busy days',
                    'Loses motivation when progress is not visible',
                    'Too many complex health apps to manage'
                ],
                jobs_to_be_done: [
                    'When I want to build healthy habits, I need an easy way to track them, so I can stay consistent',
                    'When I feel unmotivated, I need to see my progress, so I remember why I started',
                    'When I\'m busy, I need quick logging, so tracking doesn\'t feel like a chore'
                ]
            },
            secondary: {
                name: 'Fitness Frank',
                age: 28,
                occupation: 'Personal Trainer',
                goals: [
                    'Optimize performance metrics',
                    'Share progress with clients',
                    'Data-driven decision making'
                ],
                frustrations: [
                    'Scattered data across multiple apps',
                    'Limited export/sharing capabilities',
                    'No coaching insights from data'
                ],
                jobs_to_be_done: [
                    'When I train clients, I need to show my own results, so I can lead by example',
                    'When analyzing progress, I need detailed metrics, so I can adjust my approach',
                    'When planning workouts, I need historical data, so I can track what works'
                ]
            }
        },
        productivity: {
            primary: {
                name: 'Productive Paula',
                age: 29,
                occupation: 'Software Developer',
                goals: [
                    'Complete tasks efficiently',
                    'Reduce context switching',
                    'Maintain work-life balance'
                ],
                frustrations: [
                    'Too many tools fragmenting workflow',
                    'Losing track of priorities',
                    'Burnout from overwork'
                ],
                jobs_to_be_done: [
                    'When I start my day, I need clear priorities, so I know what to focus on',
                    'When I\'m interrupted, I need to quickly capture tasks, so nothing falls through the cracks',
                    'When I finish work, I need to close loops, so I can disconnect'
                ]
            }
        },
        // Add more templates as needed
    };

    const personas = personaTemplates[appType] || personaTemplates.productivity;

    return `# User Personas

## Primary Persona: ${personas.primary.name}

**Demographics**:
- Age: ${personas.primary.age}
- Occupation: ${personas.primary.occupation}

**Goals**:
${personas.primary.goals.map(g => `- ${g}`).join('\n')}

**Frustrations**:
${personas.primary.frustrations.map(f => `- ${f}`).join('\n')}

**Jobs to be Done**:
${personas.primary.jobs_to_be_done.map(j => `> ${j}`).join('\n\n')}

---

${personas.secondary ? `## Secondary Persona: ${personas.secondary.name}

**Demographics**:
- Age: ${personas.secondary.age}
- Occupation: ${personas.secondary.occupation}

**Goals**:
${personas.secondary.goals.map(g => `- ${g}`).join('\n')}

**Frustrations**:
${personas.secondary.frustrations.map(f => `- ${f}`).join('\n')}

**Jobs to be Done**:
${personas.secondary.jobs_to_be_done.map(j => `> ${j}`).join('\n\n')}
` : ''}

## Usage Scenarios

### Scenario 1: First-Time User Onboarding
**Context**: New user downloads ${requirements.app_name} for the first time
**Steps**:
1. User opens app and sees splash screen with value proposition
2. User taps "Get Started" and sets up profile
3. User sets their first goal/target
4. User completes first action (e.g., ${features[0] || 'log entry'})
5. User sees immediate feedback and progress

**Success Criteria**: User completes first action within 2 minutes

### Scenario 2: Daily Habit Tracking
**Context**: Returning user wants to ${features[0] || 'log activity'}
**Steps**:
1. User opens app to dashboard
2. User sees current progress/stats
3. User taps primary action button
4. User logs entry with minimal friction
5. User sees updated progress immediately

**Success Criteria**: Entry logged in under 10 seconds

### Scenario 3: Progress Review
**Context**: User wants to see how they're doing
**Steps**:
1. User navigates to history/analytics
2. User views trend charts and historical data
3. User identifies patterns or areas for improvement
4. User adjusts goals if needed

**Success Criteria**: User gains actionable insights within 1 minute
`;
}

// ============================================================================
// 2. PROBLEM/ESCAPE-ARRIVAL FRAMING
// ============================================================================

function generateProblemSolution(requirements) {
    const appName = requirements.app_name;
    const description = requirements.description;
    const features = requirements.features?.must_have || [];

    return `# Problem/Solution Framing

## The Problem (Escape)

### What users are escaping FROM:
- **Fragmented tracking**: Using multiple apps or paper logs that don't sync
- **Lost motivation**: Progress invisible, no sense of achievement
- **Complexity fatigue**: Overcomplicated apps with features they don't need
- **Inconsistency**: Forgetting to track, losing streaks, feeling guilty
- **Data silos**: Information locked in apps, no ownership or export

### Pain points we're solving:
1. **Friction in tracking**: Current solutions require too many steps
2. **Lack of visibility**: Can't see progress at a glance
3. **No encouragement**: Apps don't celebrate wins or help recover from misses
4. **Feature bloat**: Paying for features that distract from core goal

## The Solution (Arrival)

### What users are arriving TO:
- **Simplicity**: ${appName} focuses on ${features[0] || 'core tracking'} without bloat
- **Visual progress**: See trends, streaks, and achievements immediately
- **Frictionless logging**: ${features[0] || 'Log entries'} in under 10 seconds
- **Ownership**: All data stored locally, full privacy and control
- **Motivation**: Positive reinforcement for consistency, gentle nudges for recovery

### Value proposition:
> ${description}

### Core promise:
**${appName} helps you ${features[0]?.toLowerCase() || 'track what matters'} consistently with zero friction, so you can ${requirements.success_criteria || 'achieve your goals'} without the overwhelm.**

## Escape-Arrival Journey

\`\`\`
BEFORE (Escape)                          AFTER (Arrival)
├─ Scattered data                    →   ├─ Centralized tracking
├─ Invisible progress                →   ├─ Visual trends & insights
├─ Complex workflows                 →   ├─ One-tap actions
├─ Lost motivation                   →   ├─ Celebration & recovery
└─ No control over data              →   └─ Full ownership & privacy
\`\`\`

## Success Metrics

**User achieves escape when**:
- Stops using competing apps
- No longer forgets to track
- Feels confident in their progress

**User arrives at destination when**:
- Tracks ${features[0] || 'activity'} daily for 30+ days
- Makes data-driven decisions about their ${requirements.app_type.replace('_', ' ')}
- Recommends ${appName} to others
`;
}

// ============================================================================
// 3. ACCEPTANCE CRITERIA
// ============================================================================

function generateAcceptanceCriteria(requirements) {
    const features = requirements.features?.must_have || [];
    const niceToHave = requirements.features?.nice_to_have || [];

    return `# Acceptance Criteria

## Must-Have Features (MVP)

${features.map((feature, i) => `### ${i + 1}. ${feature}

**User Story**: As a user, I want to ${feature.toLowerCase()}, so I can track my progress

**Acceptance Criteria**:
- [ ] User can access ${feature} from main dashboard
- [ ] Action completes in < 10 seconds
- [ ] Data persists across app sessions
- [ ] User sees immediate visual feedback
- [ ] Works offline (local storage)

**Edge Cases**:
- Invalid input handling (validation errors shown)
- Empty state (helpful prompt to get started)
- Data conflicts (offline edits sync correctly)

**Done When**:
- [ ] Manual testing passes all acceptance criteria
- [ ] Visual QA scores ≥ 90/100
- [ ] No console errors
- [ ] Works on all 3 viewports (desktop, tablet, mobile)

---
`).join('\n')}

## Nice-to-Have Features (Post-MVP)

${niceToHave.length > 0 ? niceToHave.map((feature, i) => `### ${features.length + i + 1}. ${feature}

**User Story**: As a user, I want to ${feature.toLowerCase()}, so I can enhance my experience

**Priority**: Low (ship after MVP)

**Acceptance Criteria**:
- [ ] Feature can be toggled on/off
- [ ] Doesn't impact core performance
- [ ] Optional during onboarding

---
`).join('\n') : '*No nice-to-have features specified*'}

## Non-Functional Requirements

### Performance
- [ ] App loads in < 2 seconds
- [ ] Actions complete in < 500ms
- [ ] Smooth 60fps animations

### Accessibility
- [ ] WCAG AA compliance
- [ ] Screen reader support
- [ ] Keyboard navigation
- [ ] High contrast mode

### Security & Privacy
- [ ] All data stored locally (no cloud sync without consent)
- [ ] No tracking pixels or analytics without opt-in
- [ ] Data export available in JSON format
- [ ] Clear privacy policy

### Browser Support
- [ ] Chrome/Edge (latest 2 versions)
- [ ] Safari (latest 2 versions)
- [ ] Firefox (latest 2 versions)
- [ ] Mobile browsers (iOS Safari, Chrome)

## Definition of Done (Checklist)

**Design Phase**:
- [ ] Mockups generated for all screens
- [ ] Visual QA scores ≥ 90/100
- [ ] Design rationale documented
- [ ] Client approved mockup variation

**Development Phase**:
- [ ] Code generated from approved mockup
- [ ] All acceptance criteria met
- [ ] Manual testing completed
- [ ] No critical bugs

**Deployment Phase**:
- [ ] Production build passes
- [ ] Environment variables configured
- [ ] Deployment runbook followed
- [ ] Health checks passing
`;
}

// ============================================================================
// GENERATE ALL DOCUMENTS
// ============================================================================

console.log('📄 Generating personas...');
const personasDoc = generatePersonas(requirements);
fs.writeFileSync(path.join(outputDir, '01-personas.md'), personasDoc);
console.log('   ✅ 01-personas.md');

console.log('📄 Generating problem/solution...');
const problemSolutionDoc = generateProblemSolution(requirements);
fs.writeFileSync(path.join(outputDir, '02-problem-solution.md'), problemSolutionDoc);
console.log('   ✅ 02-problem-solution.md');

console.log('📄 Generating acceptance criteria...');
const acceptanceCriteriaDoc = generateAcceptanceCriteria(requirements);
fs.writeFileSync(path.join(outputDir, '03-acceptance-criteria.md'), acceptanceCriteriaDoc);
console.log('   ✅ 03-acceptance-criteria.md');

console.log('\n✅ PRD Bundle generated!');
console.log(`📂 Output: ${outputDir}/`);
console.log('\nNext: Generate system architecture and UX flows');
console.log('  node scripts/generate-architecture.js --requirements <path> --output-dir <path>');
console.log('  node scripts/generate-ux-flows.js --requirements <path> --output-dir <path>');

process.exit(0);
