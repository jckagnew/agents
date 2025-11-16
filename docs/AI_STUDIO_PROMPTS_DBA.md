# AI Studio Prompts - DBA Naming Research

## Overview

This document contains reusable prompt templates for Google AI Studio to brainstorm and research DBA (Doing Business As) names for C-Level Sales Guy LLC's planned business categories. These prompts help generate brand-appropriate names that align with target audiences and business objectives.

## Table of Contents

- [Consumer-Facing Brand](#consumer-facing-brand)
- [Bespoke/White-Label Brand](#bespokewhite-label-brand)
- [Enterprise Sales Suite](#enterprise-sales-suite)
- [Export Processing](#export-processing)
- [Integration Guidelines](#integration-guidelines)

---

## Consumer-Facing Brand

### Template: Playful Consumer Brand Naming

**Use Case**: Generate consumer-facing DBA names that are playful, accessible, and memorable  
**Mode**: Chat (for creative brainstorming)  
**Context Required**: Target audience, brand personality, market positioning

```markdown
# Consumer-Facing DBA Name Brainstorming

## Company Context
- **Parent Company**: C-Level Sales Guy LLC
- **Industry**: AI-powered software development and sales consulting
- **Location**: Dallas, TX
- **Target Audience**: Individual consumers, small businesses, tech enthusiasts

## Brand Personality
- **Tone**: Playful, approachable, innovative
- **Values**: Simplicity, accessibility, empowerment
- **Emotion**: Friendly, trustworthy, exciting
- **Style**: Modern, clean, memorable

## Naming Requirements
1. **Memorable**: Easy to remember and pronounce
2. **Available**: Check domain and trademark availability
3. **Brandable**: Works well for logos, marketing, and word-of-mouth
4. **Scalable**: Can grow with the business
5. **Differentiated**: Stands out from competitors

## Target Applications
- Personal productivity tools
- Consumer AI applications
- Mobile apps for individuals
- Freemium software products
- Community-driven platforms

## Output Format
Provide structured analysis in JSON format:
```json
{
  "dba_candidates": [
    {
      "name": "DBA Name",
      "description": "What this name represents",
      "target_audience": "Primary audience",
      "brand_personality": "Key personality traits",
      "domain_availability": "Domain availability status",
      "trademark_risk": "Low/Medium/High",
      "memorability_score": "1-10",
      "brandability_score": "1-10",
      "differentiation_score": "1-10",
      "overall_score": "1-10",
      "reasoning": "Why this name works",
      "potential_concerns": "Any potential issues"
    }
  ],
  "naming_themes": [
    "Theme 1: Description",
    "Theme 2: Description"
  ],
  "recommendations": {
    "top_choice": "Best overall option",
    "backup_options": ["Option 2", "Option 3"],
    "avoid": ["Names to avoid and why"],
    "next_steps": ["Domain check", "Trademark search", "Logo concepts"]
  }
}
```

---

## Bespoke/White-Label Brand

### Template: Professional White-Label Naming

**Use Case**: Generate professional DBA names for bespoke and white-label solutions  
**Mode**: Chat (for strategic analysis)  
**Context Required**: Partner requirements, customization needs, professional positioning

```markdown
# Bespoke/White-Label DBA Name Brainstorming

## Company Context
- **Parent Company**: C-Level Sales Guy LLC
- **Industry**: AI-powered software development and sales consulting
- **Location**: Dallas, TX
- **Target Audience**: Partners, agencies, white-label clients

## Brand Personality
- **Tone**: Professional, reliable, flexible
- **Values**: Customization, partnership, quality
- **Emotion**: Trust, confidence, capability
- **Style**: Sophisticated, adaptable, professional

## Naming Requirements
1. **Professional**: Suitable for B2B partnerships
2. **Flexible**: Works across different industries
3. **Customizable**: Allows for white-label adaptation
4. **Trustworthy**: Conveys reliability and expertise
5. **Partnership-Ready**: Appeals to potential partners

## Target Applications
- White-label software solutions
- Custom development services
- Partner integration platforms
- Bespoke AI implementations
- Co-branded applications

## Output Format
Provide structured analysis in JSON format:
```json
{
  "dba_candidates": [
    {
      "name": "DBA Name",
      "description": "What this name represents",
      "target_audience": "Primary audience",
      "brand_personality": "Key personality traits",
      "white_label_potential": "How well it works for white-labeling",
      "partnership_appeal": "1-10",
      "professional_score": "1-10",
      "flexibility_score": "1-10",
      "trustworthiness_score": "1-10",
      "overall_score": "1-10",
      "reasoning": "Why this name works",
      "potential_concerns": "Any potential issues"
    }
  ],
  "naming_themes": [
    "Theme 1: Description",
    "Theme 2: Description"
  ],
  "recommendations": {
    "top_choice": "Best overall option",
    "backup_options": ["Option 2", "Option 3"],
    "avoid": ["Names to avoid and why"],
    "next_steps": ["Domain check", "Trademark search", "Partner feedback"]
  }
}
```

---

## Enterprise Sales Suite

### Template: Enterprise-Grade Brand Naming

**Use Case**: Generate sophisticated DBA names for enterprise sales and business solutions  
**Mode**: Chat (for comprehensive analysis)  
**Context Required**: Enterprise requirements, C-level positioning, market sophistication

```markdown
# Enterprise Sales Suite DBA Name Brainstorming

## Company Context
- **Parent Company**: C-Level Sales Guy LLC
- **Industry**: AI-powered software development and sales consulting
- **Location**: Dallas, TX
- **Target Audience**: C-Level executives, enterprise decision makers, Fortune 500 companies

## Brand Personality
- **Tone**: Sophisticated, authoritative, data-driven
- **Values**: Excellence, innovation, results
- **Emotion**: Confidence, prestige, reliability
- **Style**: Premium, professional, cutting-edge

## Naming Requirements
1. **Sophisticated**: Appeals to C-Level executives
2. **Authoritative**: Conveys expertise and leadership
3. **Scalable**: Works for large enterprise implementations
4. **Premium**: Justifies enterprise pricing
5. **Memorable**: Easy to remember in boardroom discussions

## Target Applications
- Enterprise sales automation
- C-Level business intelligence
- Fortune 500 consulting
- Executive dashboards
- Strategic planning tools

## Output Format
Provide structured analysis in JSON format:
```json
{
  "dba_candidates": [
    {
      "name": "DBA Name",
      "description": "What this name represents",
      "target_audience": "Primary audience",
      "brand_personality": "Key personality traits",
      "enterprise_appeal": "1-10",
      "sophistication_score": "1-10",
      "authority_score": "1-10",
      "premium_score": "1-10",
      "memorability_score": "1-10",
      "overall_score": "1-10",
      "reasoning": "Why this name works",
      "potential_concerns": "Any potential issues"
    }
  ],
  "naming_themes": [
    "Theme 1: Description",
    "Theme 2: Description"
  ],
  "recommendations": {
    "top_choice": "Best overall option",
    "backup_options": ["Option 2", "Option 3"],
    "avoid": ["Names to avoid and why"],
    "next_steps": ["Domain check", "Trademark search", "C-Level feedback"]
  }
}
```

---

## Export Processing

### Export Locations

#### For DBA Research
```
.claude/idea-to-design/dba-research/ai-studio/
├── consumer-brand/
│   ├── naming-research.json
│   ├── domain-availability.json
│   └── trademark-analysis.json
├── bespoke-brand/
│   ├── naming-research.json
│   ├── partnership-analysis.json
│   └── white-label-potential.json
└── enterprise-brand/
    ├── naming-research.json
    ├── c-level-analysis.json
    └── enterprise-appeal.json
```

#### For Global Backlog Integration
```
.claude/idea-to-design/global/backlog/
├── manual-queue.json
├── dba-naming-results.json
└── domain-mapping.json
```

### Processing Commands

#### JSON Export Processing
```bash
# Process AI Studio DBA research exports
node scripts/process-ai-studio-dba.js --input-dir .claude/idea-to-design/dba-research/ai-studio/ --output-dir .claude/idea-to-design/global/backlog/

# Validate DBA naming results
node scripts/validate-dba-names.js --input .claude/idea-to-design/global/backlog/dba-naming-results.json

# Generate domain mapping
node scripts/generate-domain-mapping.js --dba-results .claude/idea-to-design/global/backlog/dba-naming-results.json --output .claude/idea-to-design/global/backlog/domain-mapping.json
```

#### Markdown Export Processing
```bash
# Process AI Studio Markdown exports
node scripts/process-ai-studio-markdown.js --input-file dba-research.md --output-dir .claude/idea-to-design/dba-research/ai-studio/

# Extract structured data
node scripts/extract-dba-insights.js --input-file dba-research.md --format json
```

---

## Integration Guidelines

### DBA Naming Workflow

1. **Research Phase**: Use AI Studio prompts to generate name candidates
2. **Validation Phase**: Check domain availability and trademark conflicts
3. **Selection Phase**: Evaluate against business requirements
4. **Integration Phase**: Update global backlog with selected names
5. **Implementation Phase**: Configure domain routing and analytics

### Quality Assurance

#### Name Validation Checklist
- [ ] **Domain Availability**: .com domain available
- [ ] **Trademark Clearance**: No conflicting trademarks
- [ ] **Brand Alignment**: Matches target audience and personality
- [ ] **Memorability**: Easy to remember and pronounce
- [ ] **Scalability**: Works across planned applications
- [ ] **Differentiation**: Stands out from competitors

#### Business Requirements
- [ ] **Target Audience Fit**: Appeals to intended users
- [ ] **Brand Personality Match**: Aligns with desired tone
- [ ] **Market Positioning**: Supports business strategy
- [ ] **Partnership Readiness**: Works for B2B relationships
- [ ] **Enterprise Appeal**: Suitable for C-Level executives

### Best Practices

#### AI Studio Usage
- **Use specific prompts**: Leverage templates for consistent results
- **Provide context**: Include target audience and business requirements
- **Iterate on results**: Refine prompts based on initial outputs
- **Export regularly**: Save work frequently to avoid data loss

#### Data Management
- **Consistent naming**: Use descriptive, consistent file names
- **Metadata inclusion**: Always include relevant metadata
- **Version control**: Track changes and versions
- **Backup strategy**: Maintain backups of important exports

#### Integration
- **Validate before processing**: Check data quality before integration
- **Monitor processing**: Track success rates and error patterns
- **Update templates**: Refine prompts based on results
- **Document changes**: Track template and process improvements

#### Local Ollama Workflow (optional)
- **Install & Warm Models**: `brew install ollama` then `ollama pull llama3` (or another preferred model) so the uniqueness workflow has an on-device option ready.
- **Environment Setup**: Run `ollama serve` (default `http://127.0.0.1:11434`) and set `UNIQUE_CHECK_PROVIDER=ollama`, `OLLAMA_MODEL=llama3`, and optional `OLLAMA_ENDPOINT` in `.env.local`.
- **Script Behaviour**: `scripts/name-vetting.js` now calls `searchWithOllama` before the Gemini/Google/Bing stack, using the same `{resultCount, topResults, notes}` contract and automatically falling back if the local request fails.
- **Usage Pattern**: Flip the env flag only when you want the on-device run (e.g. sensitive DBA candidates); otherwise leave it unset to stay on cloud-powered search.

---

## Round 2 Follow-up

### Conflict-Avoidant Naming (October 2025)

After initial DBA naming research revealed significant conflicts with existing brands (Apex Systems, Google Pixel, Adobe Spark), a second round was conducted with enhanced constraints to generate safer alternatives.

**Generated Files**:
- **JSON Data**: `.claude/idea-to-design/dba-research/filtered/dba-candidates-round2.json`
- **Summary Report**: `.claude/idea-to-design/dba-research/DBA_NAMING_ROUND2_SUMMARY.md`
- **Individual Reports**: `.claude/idea-to-design/dba-research/ai-studio-v2/`

**Key Improvements**:
- **Conflict Avoidance**: 100% elimination of "Apex", "Pixel", "Spark" conflicts
- **Uniqueness Focus**: Emphasis on invented words and distinctive combinations
- **Domain Availability**: 90% of candidates have available .com domains
- **Trademark Safety**: Very low risk across all top candidates

**Top Recommendations**:
- **Consumer**: Fathomly, Quillan, Locusive
- **Bespoke**: Spokeform, Verinex, Modus Built
- **Enterprise**: Veriquant, Praetori, Correlai

**Usage for Future Runs**:
Reference the JSON file for structured candidate data and the summary for conflict analysis patterns. Use the enhanced constraints from Round 2 prompts as templates for future naming research.

---

**Last Updated**: October 25, 2025  
**Version**: 2.0  
**Status**: Production Ready
