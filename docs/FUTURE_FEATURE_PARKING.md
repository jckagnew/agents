# 🅿️ Future Feature Parking System

## Overview

The Future Feature Parking System provides a structured way to capture, evaluate, and prioritize long-horizon or exploratory ideas without cluttering the active backlog. It serves as a holding area for features that are too uncertain, too far out, or not yet validated enough for immediate development.

**Status**: ✅ Production Ready
**Last Updated**: October 2024

---

## Purpose

### Why Parking Lot?

The active backlog should contain only validated, actionable items that are ready (or nearly ready) for development. However, many valuable ideas don't meet this bar initially:

- **Exploratory Concepts**: Ideas that need research or prototyping
- **Long-Horizon Features**: Strategic initiatives for future phases
- **Low-Confidence Items**: Features with uncertain value or feasibility
- **Speculative Innovations**: AI-generated or brainstormed concepts

Without a parking system, these ideas either:
1. Clutter the active backlog with noise
2. Get lost in meeting notes or Slack threads
3. Are prematurely rejected before proper evaluation

The parking lot solves this by providing:
- **Structured capture** with consistent schema
- **Prioritization framework** based on ROI and confidence
- **Promotion pathway** for items that become actionable
- **Visibility** into the future roadmap

---

## Schema

### Parking Lot Idea Structure

```json
{
  "id": "idea-1234567890-abc123",
  "title": "Multi-language Support",
  "description": "Add internationalization (i18n) to support multiple languages",
  "drivers": [
    "Expanding to European markets",
    "15% of users have non-English browser settings"
  ],
  "estimatedValue": 8,
  "estimatedEffort": 7,
  "confidence": 0.7,
  "dependencies": [
    "Content translation service",
    "Updated UI components for RTL languages"
  ],
  "targetPhase": "v2",
  "theme": "user-experience",
  "source": "customer-feedback",
  "status": "parked",
  "createdAt": "2025-10-24T12:00:00Z",
  "updatedAt": "2025-10-24T12:00:00Z"
}
```

### Field Definitions

| Field | Type | Range/Values | Description |
|-------|------|--------------|-------------|
| `id` | string | auto-generated | Unique identifier |
| `title` | string | required | Clear, concise feature name |
| `description` | string | required | What it does and why it matters |
| `drivers` | array<string> | optional | Business drivers, user needs, market trends |
| `estimatedValue` | number | 1-10 (required) | Business value or impact (10 = highest) |
| `estimatedEffort` | number | 1-10 (required) | Implementation complexity (10 = most complex) |
| `confidence` | number | 0.0-1.0 (required) | Certainty in estimates (1.0 = very confident) |
| `dependencies` | array<string> | optional | Other features, tech, or external factors required |
| `targetPhase` | string | optional | When to consider: 'mvp', 'post-mvp', 'v2', 'future', 'exploratory' |
| `theme` | string | optional | Category: 'user-experience', 'performance', 'security', etc. |
| `source` | string | optional | Where idea came from: 'manual', 'customer-feedback', 'ai-studio', 'backlog-sync' |
| `status` | string | enum | 'parked', 'ready', 'promoted', 'archived' |
| `createdAt` | ISO timestamp | auto-generated | When idea was first parked |
| `updatedAt` | ISO timestamp | auto-updated | Last modification timestamp |

---

## Usage

### Installation

```bash
# Already included in Software Factory setup
npm install

# Verify parking lot script
node scripts/parking-lot.js --help
```

### Quick Start

```bash
# 1. Create idea from template
cp parking-template.json my-idea.json

# 2. Edit with your idea details
nano my-idea.json

# 3. Add to parking lot
npm run parking:add -- --source my-idea.json

# 4. Generate prioritization report
npm run parking:report
```

### CLI Commands

#### Add Ideas

```bash
# Add from JSON file (merge with existing)
node scripts/parking-lot.js \
  --session-dir .claude/idea-to-design/session-123 \
  --source ideas.json \
  --merge

# Add from Markdown file
node scripts/parking-lot.js \
  --session-dir SESSION_DIR \
  --source ideas.md \
  --merge

# Add with strict duplicate checking
node scripts/parking-lot.js \
  --session-dir SESSION_DIR \
  --source ideas.json \
  --merge \
  --fail-on-duplicate

# Dry run (preview without saving)
node scripts/parking-lot.js \
  --session-dir SESSION_DIR \
  --source ideas.json \
  --dry-run
```

#### Generate Reports

```bash
# Generate prioritization report
node scripts/parking-lot.js \
  --session-dir SESSION_DIR \
  --generate-report

# View promotion-ready ideas
# These are automatically flagged in the report
```

### npm Scripts

```bash
# Add idea with merge
npm run parking:add -- --source my-idea.json

# Generate prioritization report
npm run parking:report

# Dry run mode
npm run parking:dry-run
```

---

## Input Formats

### JSON Format

**Single Idea**:
```json
{
  "title": "Real-time Collaboration",
  "description": "Allow multiple users to edit simultaneously",
  "drivers": ["Team workflow improvement", "Competitor parity"],
  "estimatedValue": 9,
  "estimatedEffort": 9,
  "confidence": 0.4,
  "targetPhase": "exploratory",
  "theme": "user-experience"
}
```

**Multiple Ideas**:
```json
[
  {
    "title": "Idea 1",
    "description": "...",
    "estimatedValue": 8,
    "estimatedEffort": 6,
    "confidence": 0.7
  },
  {
    "title": "Idea 2",
    "description": "...",
    "estimatedValue": 7,
    "estimatedEffort": 5,
    "confidence": 0.8
  }
]
```

### Markdown Format

```markdown
## Multi-language Support
Add internationalization (i18n) to support multiple languages and locales, starting with Spanish and French.

- Drivers: Expanding to European markets, 15% of users have non-English browsers
- Value: 8
- Effort: 7
- Confidence: 0.7
- Theme: user-experience

## Real-time Collaboration
Allow multiple users to edit the same document simultaneously.

- Drivers: Team collaboration workflow, Competitor feature parity
- Value: 9
- Effort: 9
- Confidence: 0.4
- Theme: user-experience
```

### AI Studio Format

AI Studio outputs can be ingested directly if they follow either JSON or Markdown format above.

```bash
# Ingest AI Studio output
node scripts/parking-lot.js \
  --session-dir SESSION_DIR \
  --source ai-studio-output.txt \
  --merge
```

---

## Prioritization Model

### ROI Calculation

**Formula**: `ROI = (Value / Effort) * Confidence`

**Examples**:
- High value (9), low effort (3), high confidence (0.9) → ROI = 2.7 (Quick Win!)
- High value (9), high effort (9), low confidence (0.3) → ROI = 0.3 (Risky)
- Medium value (5), medium effort (5), high confidence (0.8) → ROI = 0.8 (Steady)

### Promotion Criteria

Ideas are automatically flagged as **promotion-ready** when they meet BOTH criteria:

1. **Confidence ≥ 0.6** (60% certainty)
2. **Value ≥ 7** (High business value)

**Rationale**:
- High-value, high-confidence ideas deserve immediate attention
- Low-confidence ideas need more research/validation first
- Low-value ideas may not be worth the effort

### Impact vs Effort Matrix

```
High Value │
     10    │
           │
      7    │  QUICK WINS   │  STRATEGIC
           │               │
      5    ├───────────────┼────────────
           │               │
      3    │  FILL-INS     │  MAJOR
           │               │  PROJECTS
 Low Value │
      0    └────────────────────────────
              0      5      10
            Low    Medium   High
                 Effort
```

**Quadrants**:

- **Quick Wins** (High Value, Low Effort): Prioritize these first
- **Strategic** (High Value, High Effort): Important long-term bets
- **Fill-Ins** (Low Value, Low Effort): Nice-to-haves when capacity allows
- **Major Projects** (Low Value, High Effort): Reconsider or archive

---

## Workflow Integration

### Idea Flow

```
┌─────────────────┐
│  Idea Sources   │
│  - Manual       │
│  - AI Studio    │
│  - Backlog Sync │
│  - Meetings     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parking Lot    │
│  - Capture      │
│  - Evaluate     │
│  - Prioritize   │
└────────┬────────┘
         │
         ▼
   ┌─────────────┐
   │ Confidence  │◄─── Research, Validation
   │   Check     │
   └──┬──────┬───┘
      │      │
 Low  │      │ High (≥0.6)
      │      │
      ▼      ▼
   Park   ┌──────────┐
   More   │  Value   │
          │  Check   │
          └──┬───┬───┘
             │   │
        Low  │   │ High (≥7)
             │   │
             ▼   ▼
           Stay  Promote to
           Parked Active Backlog
```

### Integration with Backlog Sync

The backlog-sync automatically routes items to the parking lot based on:

**Automatic Routing Criteria**:
1. **Labels**: `future`, `exploratory`, `research`, `post-mvp`, `nice-to-have`
2. **Priority**: P3 or lower
3. **Keywords** in description: "explore", "consider", "investigate", "research"

**Example**:
```javascript
// From PRD "Nice-to-Have Features" section
// → Automatically routed to parking lot with:
{
  priority: 'P3',
  labels: ['post-mvp', 'nice-to-have'],
  confidence: 0.4  // Low confidence = needs validation
}
```

**Manual Override**:
Backlog sync saves all items locally first. You can review and manually move items between parking lot and active backlog.

---

## Reports

### Prioritization Report Structure

Generated reports include:

1. **Executive Summary**
   - Total ideas
   - Promotion-ready count
   - Top 10 by ROI

2. **Ideas by Theme**
   - Grouped by theme/category
   - Average value, effort, confidence per theme
   - Sorted by ROI within each theme

3. **Promotion-Ready List**
   - Ideas meeting promotion criteria
   - Detailed metrics for each

4. **Impact vs Effort Matrix**
   - Visual quadrant distribution
   - Quick Wins, Strategic, Fill-Ins, Major Projects

5. **Next Steps**
   - Actionable recommendations
   - Review and promotion process

### Example Report Output

```markdown
# Future Feature Parking Lot - Prioritization Report

**Generated**: 2025-10-24T12:00:00Z
**Total Ideas**: 15
**Ready for Promotion**: 3

## Executive Summary

### Top Priority Ideas (by ROI)

| Rank | Title | Value | Effort | Confidence | ROI | Ready? |
|------|-------|-------|--------|------------|-----|--------|
| 1 | Advanced Search | 8 | 4 | 90% | 1.80 | ✅ |
| 2 | Multi-language | 8 | 7 | 70% | 0.80 | ✅ |
| 3 | Dark Mode | 7 | 3 | 85% | 1.98 | ✅ |

## Promotion-Ready Ideas

The following 3 ideas are ready to be promoted to the active backlog:

1. **Advanced Search**
   - Value: 8/10
   - Effort: 4/10
   - Confidence: 90%
   - ROI: 1.80

2. **Multi-language Support**
   - Value: 8/10
   - Effort: 7/10
   - Confidence: 70%
   - ROI: 0.80

3. **Dark Mode Theme**
   - Value: 7/10
   - Effort: 3/10
   - Confidence: 85%
   - ROI: 1.98
```

---

## Promotion Process

### When to Promote

Promote an idea when:
1. ✅ Confidence ≥ 0.6 AND Value ≥ 7 (auto-flagged)
2. ✅ Dependencies are available or planned
3. ✅ Team capacity exists
4. ✅ Stakeholder buy-in secured

### How to Promote

**Manual Promotion**:
1. Review prioritization report
2. Validate promotion-ready ideas with stakeholders
3. Update idea status to `"promoted"`
4. Create backlog item using backlog-sync
5. Link parking lot idea ID in backlog item for traceability

**Automated Promotion** (future enhancement):
```bash
# Promote specific idea by ID
node scripts/parking-lot.js \
  --session-dir SESSION_DIR \
  --promote idea-123

# Auto-promote all ready ideas
node scripts/parking-lot.js \
  --session-dir SESSION_DIR \
  --auto-promote
```

### After Promotion

- Update status: `parked` → `promoted`
- Keep in parking lot for historical tracking
- Link to active backlog issue/ticket
- Update confidence and value as you learn more

---

## Best Practices

### Capturing Ideas

✅ **DO**:
- Capture ideas immediately when they arise
- Write clear, actionable descriptions
- Include business drivers and user needs
- Be honest about confidence levels
- Add dependencies early

❌ **DON'T**:
- Overcomplicate idea descriptions
- Inflate value scores
- Ignore uncertainty (low confidence is OK!)
- Skip the parking lot and dump everything in backlog

### Estimating

**Value (1-10)**:
- 9-10: Game-changing, strategic priority
- 7-8: High impact, clear user value
- 5-6: Moderate value, nice improvement
- 3-4: Minor value, limited impact
- 1-2: Negligible value, questionable fit

**Effort (1-10)**:
- 9-10: Major project, months of work, high complexity
- 7-8: Significant feature, weeks of work
- 5-6: Medium feature, 1-2 weeks
- 3-4: Small feature, days of work
- 1-2: Trivial, hours of work

**Confidence (0.0-1.0)**:
- 0.9-1.0: Very confident, clear understanding
- 0.7-0.8: Confident, some unknowns
- 0.5-0.6: Uncertain, needs validation
- 0.3-0.4: Low confidence, exploratory
- 0.0-0.2: Wild guess, very speculative

### Reviewing Parking Lot

**Cadence**:
- **Weekly**: Quick scan of new ideas
- **Monthly**: Full prioritization report review
- **Quarterly**: Deep dive with stakeholders, promote ready items

**Review Checklist**:
- [ ] Generate latest prioritization report
- [ ] Review promotion-ready ideas
- [ ] Update confidence scores based on learnings
- [ ] Archive obsolete or rejected ideas
- [ ] Add new ideas from recent meetings
- [ ] Validate dependencies for high-priority items

---

## Examples

### Example 1: Customer Feedback Idea

**Scenario**: Customer requests multi-language support

**Parking Lot Entry**:
```json
{
  "title": "Multi-language Support (i18n)",
  "description": "Add internationalization to support Spanish, French, and German",
  "drivers": [
    "3 enterprise customers requested this",
    "Expanding to European markets",
    "15% of users have non-English browser settings"
  ],
  "estimatedValue": 8,
  "estimatedEffort": 7,
  "confidence": 0.7,
  "dependencies": [
    "Translation service selection",
    "Content translation process",
    "RTL UI component updates"
  ],
  "targetPhase": "v2",
  "theme": "user-experience",
  "source": "customer-feedback"
}
```

**Analysis**:
- **ROI**: (8/7) * 0.7 = 0.80 (medium)
- **Promotion Ready**: ✅ Yes (confidence 0.7 ≥ 0.6, value 8 ≥ 7)
- **Action**: Promote to active backlog for v2 planning

### Example 2: Speculative AI Feature

**Scenario**: Team brainstorms AI-powered recommendation engine

**Parking Lot Entry**:
```json
{
  "title": "AI Recommendation Engine",
  "description": "Use ML to suggest relevant content based on user behavior",
  "drivers": [
    "Increase engagement metrics",
    "Personalization is a trend",
    "Competitor has similar feature"
  ],
  "estimatedValue": 7,
  "estimatedEffort": 9,
  "confidence": 0.3,
  "dependencies": [
    "ML infrastructure and expertise",
    "User behavior data collection",
    "A/B testing framework"
  ],
  "targetPhase": "exploratory",
  "theme": "user-experience",
  "source": "team-brainstorm"
}
```

**Analysis**:
- **ROI**: (7/9) * 0.3 = 0.23 (low)
- **Promotion Ready**: ❌ No (confidence 0.3 < 0.6)
- **Action**: Keep parked, spike/prototype to increase confidence

### Example 3: Quick Win

**Scenario**: Simple feature with clear value

**Parking Lot Entry**:
```json
{
  "title": "Keyboard Shortcuts",
  "description": "Add common keyboard shortcuts for power users",
  "drivers": [
    "Power users request this frequently",
    "Improve productivity",
    "Low implementation cost"
  ],
  "estimatedValue": 7,
  "estimatedEffort": 3,
  "confidence": 0.9,
  "dependencies": [],
  "targetPhase": "post-mvp",
  "theme": "user-experience",
  "source": "customer-feedback"
}
```

**Analysis**:
- **ROI**: (7/3) * 0.9 = 2.10 (very high!)
- **Quadrant**: Quick Win
- **Promotion Ready**: ✅ Yes
- **Action**: Promote immediately, schedule for next sprint

---

## Troubleshooting

### Common Issues

**Issue**: Duplicate ideas in parking lot
- **Solution**: Use `--fail-on-duplicate` flag or manually deduplicate
- **Prevention**: Check existing ideas before adding new ones

**Issue**: All ideas have low confidence
- **Solution**: This is OK! Parking lot is for uncertain ideas
- **Action**: Run validation spikes to increase confidence over time

**Issue**: No ideas are promotion-ready
- **Solution**: Review confidence scores - you may be too conservative
- **Action**: Look for ideas close to threshold (confidence 0.5-0.6, value 6-7)

**Issue**: Too many ideas in parking lot
- **Solution**: Archive obsolete ideas, promote ready ones
- **Action**: Set up quarterly review process

### Validation Process

To increase confidence and move ideas toward promotion:

1. **User Research**
   - Interview customers
   - Run surveys
   - Analyze usage data

2. **Technical Spikes**
   - Prototype key functionality
   - Evaluate technical feasibility
   - Estimate effort more accurately

3. **Competitive Analysis**
   - Research how competitors solve this
   - Identify best practices
   - Understand market demand

4. **Stakeholder Validation**
   - Present to leadership
   - Get buy-in from affected teams
   - Align with strategic priorities

---

## Integration with respect-spec

The respect-spec audit checks for:

- [ ] Parking directory exists: `.claude/idea-to-design/session-X/parking/`
- [ ] At least one parking lot file: `parking-lot-*.json`
- [ ] Valid JSON schema in parking lot files
- [ ] Prioritization report exists: `parking-summary-*.md`
- [ ] High-confidence items are flagged for promotion

**Audit Output**:
```
Phase 9: Future Feature Parking
  ✅ Parking directory exists
  ✅ Parking lot files found: 3
  ✅ Total parked ideas: 15
  ⚠️  Promotion-ready ideas: 3 (review and promote)
  ✅ Prioritization report is up-to-date
```

---

## Roadmap

### Current Features ✅
- JSON and Markdown ingestion
- Similarity-based duplicate detection
- ROI calculation and prioritization
- Promotion-ready flagging
- Comprehensive reporting
- Backlog sync integration

### Planned Enhancements 🚧
- Automated promotion workflow
- Integration with AI Studio for idea generation
- Trend analysis over time
- Stakeholder voting/scoring
- Slack/email notifications for promotion-ready ideas
- Visual dashboard (web UI)

---

## FAQ

**Q: Should I put all new ideas in the parking lot first?**
A: No. Only park ideas that are uncertain, exploratory, or far-horizon. If an idea is validated, high-confidence, and ready for development, add it directly to the active backlog.

**Q: How do I choose between theme categories?**
A: Use the most specific theme that applies. Common themes: `user-experience`, `performance`, `security`, `analytics`, `infrastructure`, `business`, `developer-experience`.

**Q: Can I manually edit parking lot JSON files?**
A: Yes, but be careful to maintain the schema. It's safer to use the CLI or create new ideas from the template.

**Q: What if confidence increases but value stays low?**
A: That's fine! High-confidence, low-value ideas can be archived or kept as "fill-ins" for when you have spare capacity.

**Q: How often should ideas be promoted?**
A: There's no fixed cadence. Promote when ideas become ready (meet criteria) and you have capacity to work on them.

---

**Last Updated**: October 2024
**Maintained By**: Software Factory Team
**Related Documentation**:
- [Backlog Sync Guide](./BACKLOG_SYNC.md)
- [Software Factory Playbook](./SOFTWARE_FACTORY_PLAYBOOK.md)
- [Respect-Spec Documentation](./RESPECT_SPEC.md)
