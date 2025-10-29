# Future-Feature Parking System

## Overview

The Future-Feature Parking system is designed to capture and evaluate speculative feature ideas that aren't ready for immediate development but have potential future value. This system complements the backlog sync by providing a structured way to store, evaluate, and prioritize ideas that may become features later.

## How to Add Items Manually

### 1. Create a New Parking Entry

Copy the template file and create a new entry:

```bash
# Copy the template
cp .claude/idea-to-design/test-gen/parking/parking-template.json \
   .claude/idea-to-design/test-gen/parking/feature-{timestamp}-{name}.json

# Edit the new file
nano .claude/idea-to-design/test-gen/parking/feature-20250124-ai-chat.json
```

### 2. Fill in the Required Fields

```json
{
  "title": "AI-Powered Chat Assistant",
  "description": "Integrate Claude API to provide intelligent chat assistance within the application, helping users navigate features and get contextual help.",
  "opportunity_driver": "User feedback indicates confusion with complex workflows; AI assistance could reduce support tickets by 40%",
  "estimated_value": 8,
  "confidence": 0.6,
  "dependencies": [
    "Claude API integration",
    "User authentication system",
    "Chat UI components"
  ],
  "timeframe": "Q3 2025",
  "notes": "Research shows 60% of users would use AI assistance. Need to evaluate Claude vs OpenAI costs.",
  "metadata": {
    "created_date": "2025-01-24",
    "created_by": "product-manager",
    "status": "parked",
    "priority": "high",
    "category": "ai-integration",
    "tags": ["ai", "chat", "user-experience"],
    "source": "user-feedback"
  }
}
```

### 3. Validate the Entry

```bash
# Validate JSON syntax
cat .claude/idea-to-design/test-gen/parking/feature-*.json | jq .

# Check required fields
node scripts/validate-parking.js .claude/idea-to-design/test-gen/parking/feature-*.json
```

## Field Definitions

### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Short, descriptive title for the feature |
| `description` | string | Yes | Detailed description of what the feature does and how it works |
| `opportunity_driver` | string | Yes | Business case or market opportunity that justifies this feature |
| `estimated_value` | number | Yes | Business value score from 1-10 (10 = highest value) |
| `confidence` | number | Yes | Confidence in the estimate from 0-1 (1 = highest confidence) |
| `dependencies` | array | No | List of other features or infrastructure that must be completed first |
| `timeframe` | string | No | Estimated delivery timeframe (e.g., "Q2 2025", "H2 2025") |
| `notes` | string | No | Additional context, research findings, or implementation considerations |

### Metadata Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `created_date` | string | Yes | ISO date when the entry was created |
| `created_by` | string | Yes | Who created the entry (user, product-manager, developer, etc.) |
| `status` | string | Yes | Current status (parked, evaluating, prioritized, rejected) |
| `priority` | string | No | Priority level (low, medium, high, critical) |
| `category` | string | No | Feature category (enhancement, integration, ai, ui, backend, etc.) |
| `tags` | array | No | Searchable tags for filtering and organization |
| `source` | string | No | Where the idea came from (user-feedback, research, competitor-analysis, etc.) |

## Best Practices

### Writing Effective Descriptions

1. **Problem Statement**: Start with the problem the feature solves
2. **Solution Overview**: Describe how the feature addresses the problem
3. **User Impact**: Explain how users will benefit
4. **Technical Considerations**: Note any technical challenges or requirements

### Estimating Value and Confidence

**Value Scale (1-10)**:
- 1-3: Nice to have, minimal business impact
- 4-6: Moderate value, some business impact
- 7-8: High value, significant business impact
- 9-10: Critical value, major business impact

**Confidence Scale (0-1)**:
- 0-0.3: Low confidence, estimates are rough guesses
- 0.4-0.6: Medium confidence, some research or data available
- 0.7-0.8: High confidence, good data and analysis
- 0.9-1.0: Very high confidence, extensive research and validation

### Dependencies

List dependencies in order of importance:
1. **Blocking dependencies**: Must be completed before this feature
2. **Enabling dependencies**: Make this feature easier or better
3. **Optional dependencies**: Nice to have but not required

### Timeframes

Use consistent timeframe formats:
- Quarters: "Q1 2025", "Q2 2025", etc.
- Half-years: "H1 2025", "H2 2025"
- Years: "2025", "2026"
- Relative: "Next 6 months", "Within 1 year"

## Difference from Backlog Entries

### Parking vs Backlog

| Aspect | Parking | Backlog |
|--------|---------|---------|
| **Purpose** | Capture speculative ideas | Track committed work |
| **Status** | Not yet prioritized | Ready for development |
| **Detail Level** | High-level concept | Detailed requirements |
| **Timeline** | Future consideration | Near-term delivery |
| **Validation** | Initial evaluation | Fully validated |
| **Dependencies** | May be unclear | Well-defined |
| **Effort** | Rough estimates | Detailed estimates |

### When to Use Parking

- **Early-stage ideas**: Concepts that need more research
- **Speculative features**: Ideas based on market trends or user feedback
- **Long-term vision**: Features that are years away
- **Dependency blockers**: Ideas waiting for other work to complete
- **Resource constraints**: Good ideas without immediate capacity

### When to Move to Backlog

- **Validated need**: Clear business case and user demand
- **Defined requirements**: Detailed understanding of what to build
- **Resource availability**: Team capacity and timeline alignment
- **Dependencies resolved**: Blocking items are completed
- **Priority confirmed**: Feature ranks high enough for immediate work

## File Naming Convention

Use descriptive, consistent naming:

```
feature-{YYYYMMDD}-{short-name}.json
```

Examples:
- `feature-20250124-ai-chat.json`
- `feature-20250124-mobile-app.json`
- `feature-20250124-api-integration.json`

## Integration with Backlog Sync

The parking system integrates with the backlog sync in several ways:

1. **Promotion**: High-value parked items can be promoted to the backlog
2. **Dependency Tracking**: Backlog items can reference parked dependencies
3. **Priority Alignment**: Parking helps inform backlog prioritization
4. **Resource Planning**: Parking provides visibility into future work

## AI Studio Integration

### AI Studio Exports as Valid Source

The parking system accepts exports from Google AI Studio as a valid source for future feature ideas. AI Studio research can generate market opportunities, strategic recommendations, and competitive insights that are automatically routed to the parking lot.

#### Supported AI Studio Export Types

- **Market Research**: Market opportunities and trends from AI Studio analysis
- **Strategic Planning**: Strategic recommendations and future initiatives
- **Competitive Analysis**: Competitive gaps and positioning opportunities
- **User Research**: User insights and feature suggestions
- **Financial Analysis**: Investment opportunities and ROI projections

#### Processing AI Studio Exports

```bash
# Process AI Studio exports for parking lot
node scripts/process-ai-studio-exports.js --input-dir .claude/idea-to-design/session-X/ai-studio-research/ --output-dir .claude/idea-to-design/test-gen/parking/

# Validate AI Studio parking entries
node scripts/validate-parking.js --source ai-studio

# Generate parking report including AI Studio insights
npm run parking:report -- --include-ai-studio
```

#### AI Studio Export Format

AI Studio exports should follow this structure for parking lot integration:

```json
{
  "source": "ai-studio",
  "export_type": "market-research|strategic-planning|competitive-analysis|user-research|financial-analysis",
  "session_id": "session-123",
  "export_date": "2025-01-24T18:30:00Z",
  "opportunities": [
    {
      "title": "AI-Powered Market Analysis Tool",
      "description": "Automated market research and competitive analysis using AI",
      "opportunity_driver": "Market research shows 40% of C-Level executives struggle with data-driven decision making",
      "estimated_value": 8,
      "confidence": 0.7,
      "dependencies": ["AI integration", "Data sources", "Analytics platform"],
      "timeframe": "Q2 2025",
      "notes": "Based on AI Studio market analysis - high demand, low competition",
      "metadata": {
        "created_date": "2025-01-24",
        "created_by": "ai-studio",
        "status": "parked",
        "priority": "high",
        "category": "ai-integration",
        "tags": ["ai", "market-research", "analytics"],
        "source": "ai-studio-market-research"
      }
    }
  ]
}
```

#### AI Studio Integration Workflow

1. **Export from AI Studio**: Save research results in JSON format
2. **Process with Software Factory**: Use processing scripts to extract opportunities
3. **Validate and Transform**: Ensure data meets parking lot requirements
4. **Route to Parking Lot**: Automatically categorize and prioritize opportunities
5. **Review and Refine**: Human review of AI-generated opportunities
6. **Promote to Backlog**: Move validated opportunities to active development

#### Quality Assurance for AI Studio Exports

- **Content Validation**: Ensure AI-generated content is relevant and accurate
- **Format Compliance**: Verify JSON structure matches parking lot schema
- **Business Value Assessment**: Validate estimated value and confidence scores
- **Dependency Analysis**: Check for realistic and achievable dependencies
- **Timeline Validation**: Ensure timeframes are reasonable and achievable

## Maintenance

### Regular Reviews

- **Monthly**: Review parked items for promotion opportunities
- **Quarterly**: Evaluate items for continued relevance
- **Annually**: Archive or remove outdated ideas

### Cleanup

- Remove items that are no longer relevant
- Archive items that have been implemented
- Update status and priority based on new information

## Tools and Scripts

### Validation Script

```bash
# Validate all parking entries
npm run parking:validate

# Validate specific entry
npm run parking:validate -- feature-20250124-ai-chat.json
```

### Sync Script

```bash
# Sync parking with backlog
npm run parking:sync

# Generate parking report
npm run parking:report
```

### Search and Filter

```bash
# Search by category
npm run parking:search -- --category ai

# Filter by priority
npm run parking:search -- --priority high

# Find items ready for promotion
npm run parking:search -- --ready-for-promotion
```

---

**Last Updated**: January 2025  
**Next Review**: February 2025  
**Status**: Ready for Use
