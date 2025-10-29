# AI Studio Prompt & Template Library

## Overview

This library contains reusable prompt templates for Google AI Studio, optimized for different use cases in the Software Factory workflow. Each template includes context requirements, expected outputs, and integration notes.

## Table of Contents

- [Market Gap Discovery](#market-gap-discovery)
- [Financial Viability Analysis](#financial-viability-analysis)
- [Media Asset Generation](#media-asset-generation)
- [Strategic Planning](#strategic-planning)
- [Competitive Analysis](#competitive-analysis)
- [User Research](#user-research)
- [Technical Requirements](#technical-requirements)
- [Integration Guidelines](#integration-guidelines)

## Market Gap Discovery

### Template: Market Opportunity Scanner

**Use Case**: Identify underserved markets and opportunities  
**Mode**: Build (for automation) or Chat (for exploration)  
**Context Required**: Industry focus, target audience, geographic scope

```markdown
# Market Opportunity Scanner

## Context
- Industry: {INDUSTRY}
- Target Audience: {TARGET_AUDIENCE}
- Geographic Scope: {GEOGRAPHY}
- Company: C-Level Sales Guy LLC (AI-powered software development and sales consulting)

## Task
Analyze the {INDUSTRY} market to identify:
1. Underserved market segments
2. Emerging opportunities
3. Competitive gaps
4. Revenue potential
5. Implementation feasibility

## Output Format
Provide structured analysis in JSON format:
```json
{
  "opportunities": [
    {
      "title": "Opportunity Name",
      "description": "Brief description",
      "market_size": "Estimated market size",
      "growth_rate": "Projected growth rate",
      "competition_level": "Low/Medium/High",
      "barriers_to_entry": "Key barriers",
      "revenue_potential": "1-10 scale",
      "implementation_effort": "1-10 scale",
      "time_to_market": "Estimated months",
      "confidence": "0.0-1.0"
    }
  ],
  "insights": {
    "market_trends": ["Trend 1", "Trend 2"],
    "key_drivers": ["Driver 1", "Driver 2"],
    "risks": ["Risk 1", "Risk 2"],
    "recommendations": ["Recommendation 1", "Recommendation 2"]
  }
}
```

## Financial Viability Analysis

### Template: Business Case Builder

**Use Case**: Evaluate financial feasibility of opportunities  
**Mode**: Chat (with large context for detailed analysis)  
**Context Required**: Opportunity details, market data, cost estimates

```markdown
# Financial Viability Analysis

## Context
- Opportunity: {OPPORTUNITY_TITLE}
- Description: {OPPORTUNITY_DESCRIPTION}
- Market Size: {MARKET_SIZE}
- Target Customers: {TARGET_CUSTOMERS}
- Company: C-Level Sales Guy LLC

## Financial Analysis Required
1. Revenue projections (3-year)
2. Cost structure analysis
3. Break-even analysis
4. ROI calculations
5. Risk assessment
6. Sensitivity analysis

## Output Format
```json
{
  "financial_summary": {
    "total_investment": 0,
    "break_even_months": 0,
    "roi_3_year": 0,
    "npv_3_year": 0,
    "irr": 0
  },
  "revenue_projections": {
    "year_1": {
      "revenue": 0,
      "customers": 0,
      "avg_revenue_per_customer": 0
    },
    "year_2": {
      "revenue": 0,
      "customers": 0,
      "avg_revenue_per_customer": 0
    },
    "year_3": {
      "revenue": 0,
      "customers": 0,
      "avg_revenue_per_customer": 0
    }
  },
  "cost_structure": {
    "development": 0,
    "marketing": 0,
    "operations": 0,
    "personnel": 0,
    "infrastructure": 0
  },
  "risk_analysis": {
    "high_risk_factors": ["Factor 1", "Factor 2"],
    "mitigation_strategies": ["Strategy 1", "Strategy 2"],
    "sensitivity_scenarios": {
      "optimistic": {"revenue_multiplier": 1.5, "roi": 0},
      "realistic": {"revenue_multiplier": 1.0, "roi": 0},
      "pessimistic": {"revenue_multiplier": 0.6, "roi": 0}
    }
  },
  "recommendations": {
    "go_no_go": "Go/No-Go/Maybe",
    "key_metrics": ["Metric 1", "Metric 2"],
    "next_steps": ["Step 1", "Step 2"]
  }
}
```

## Media Asset Generation

### Template: Visual Content Creator

**Use Case**: Generate marketing materials and presentations  
**Mode**: Generate Media  
**Context Required**: Brand guidelines, content requirements, target audience

```markdown
# Visual Content Creator

## Brand Context
- Company: C-Level Sales Guy LLC
- Industry: AI-powered software development and sales consulting
- Target Audience: C-Level executives
- Tone: Professional, innovative, trustworthy

## Content Requirements
- Type: {CONTENT_TYPE} (presentation slide, social media post, infographic, etc.)
- Topic: {TOPIC}
- Key Message: {KEY_MESSAGE}
- Call to Action: {CALL_TO_ACTION}

## Visual Specifications
- Style: Modern, clean, professional
- Colors: Blue (#1E40AF), Gray (#6B7280), White (#FFFFFF)
- Typography: Sans-serif, readable
- Layout: Balanced, not cluttered

## Output Requirements
- Format: High-resolution image
- Dimensions: {WIDTH}x{HEIGHT}
- File size: Optimized for web
- Accessibility: Alt text included

## Brand Guidelines
- Logo placement: Top-left or bottom-right
- Color consistency: Use brand colors
- Typography: Clear, professional fonts
- Imagery: High-quality, relevant visuals
```

### Template: Presentation Slide Generator

**Use Case**: Create presentation slides for business proposals  
**Mode**: Generate Media  
**Context Required**: Slide content, presentation theme, audience

```markdown
# Presentation Slide Generator

## Slide Information
- Slide Number: {SLIDE_NUMBER}
- Title: {SLIDE_TITLE}
- Content: {SLIDE_CONTENT}
- Presentation Theme: {THEME}
- Audience: C-Level executives

## Design Requirements
- Layout: Clean, professional
- Visual Hierarchy: Clear title, bullet points, supporting visuals
- Branding: C-Level Sales Guy LLC
- Readability: Large fonts, high contrast

## Content Structure
1. Compelling headline
2. 3-5 key points
3. Supporting data/visuals
4. Call to action (if applicable)

## Output Specifications
- Format: PNG or JPG
- Resolution: 1920x1080 (16:9)
- Quality: Print-ready
- File naming: slide-{SLIDE_NUMBER}-{SLIDE_TITLE}.png
```

## Strategic Planning

### Template: Strategic Framework Builder

**Use Case**: Develop comprehensive strategic plans  
**Mode**: Chat (with large context)  
**Context Required**: Company information, market data, goals

```markdown
# Strategic Framework Builder

## Company Context
- Name: C-Level Sales Guy LLC
- Industry: AI-powered software development and sales consulting
- Location: Dallas, TX
- Current Stage: {STAGE} (startup, growth, mature)
- Key Strengths: {STRENGTHS}
- Key Challenges: {CHALLENGES}

## Strategic Planning Requirements
1. Vision and mission refinement
2. Market positioning strategy
3. Competitive advantage analysis
4. Growth strategy development
5. Resource allocation plan
6. Risk mitigation strategies
7. Success metrics definition

## Output Format
```json
{
  "strategic_framework": {
    "vision": "Company vision statement",
    "mission": "Company mission statement",
    "values": ["Value 1", "Value 2", "Value 3"],
    "strategic_objectives": [
      {
        "objective": "Objective 1",
        "description": "Description",
        "timeline": "Timeline",
        "success_metrics": ["Metric 1", "Metric 2"],
        "priority": "High/Medium/Low"
      }
    ]
  },
  "market_positioning": {
    "target_market": "Primary target market",
    "value_proposition": "Unique value proposition",
    "competitive_advantages": ["Advantage 1", "Advantage 2"],
    "differentiation": "How we differentiate"
  },
  "growth_strategy": {
    "short_term": {
      "goals": ["Goal 1", "Goal 2"],
      "initiatives": ["Initiative 1", "Initiative 2"],
      "timeline": "6-12 months"
    },
    "medium_term": {
      "goals": ["Goal 1", "Goal 2"],
      "initiatives": ["Initiative 1", "Initiative 2"],
      "timeline": "1-3 years"
    },
    "long_term": {
      "goals": ["Goal 1", "Goal 2"],
      "initiatives": ["Initiative 1", "Initiative 2"],
      "timeline": "3-5 years"
    }
  },
  "resource_requirements": {
    "human_resources": {
      "hiring_needs": ["Role 1", "Role 2"],
      "skill_development": ["Skill 1", "Skill 2"],
      "organizational_structure": "Recommended structure"
    },
    "financial_resources": {
      "investment_required": 0,
      "funding_sources": ["Source 1", "Source 2"],
      "revenue_projections": "Revenue forecast"
    },
    "technology_resources": {
      "infrastructure_needs": ["Need 1", "Need 2"],
      "software_requirements": ["Software 1", "Software 2"],
      "security_requirements": ["Requirement 1", "Requirement 2"]
    }
  },
  "risk_mitigation": {
    "high_priority_risks": [
      {
        "risk": "Risk description",
        "impact": "High/Medium/Low",
        "probability": "High/Medium/Low",
        "mitigation_strategy": "Mitigation approach"
      }
    ],
    "contingency_plans": ["Plan 1", "Plan 2"]
  },
  "success_metrics": {
    "financial_metrics": ["Revenue growth", "Profit margin", "ROI"],
    "operational_metrics": ["Customer satisfaction", "Employee retention", "Process efficiency"],
    "strategic_metrics": ["Market share", "Brand recognition", "Innovation index"]
  }
}
```

## Competitive Analysis

### Template: Competitor Intelligence

**Use Case**: Analyze competitive landscape  
**Mode**: Chat (with large context)  
**Context Required**: Industry focus, competitor list, analysis depth

```markdown
# Competitor Intelligence Analysis

## Analysis Context
- Industry: {INDUSTRY}
- Company: C-Level Sales Guy LLC
- Competitors: {COMPETITOR_LIST}
- Analysis Depth: {DEPTH} (surface, detailed, comprehensive)

## Competitive Analysis Framework
1. Competitor identification and categorization
2. Product/service comparison
3. Market positioning analysis
4. Strengths and weaknesses assessment
5. Pricing strategy analysis
6. Marketing and sales approach
7. Technology and innovation assessment
8. Financial performance analysis
9. Strategic direction analysis
10. Threat and opportunity assessment

## Output Format
```json
{
  "competitive_landscape": {
    "direct_competitors": [
      {
        "name": "Competitor Name",
        "market_share": "Estimated percentage",
        "strengths": ["Strength 1", "Strength 2"],
        "weaknesses": ["Weakness 1", "Weakness 2"],
        "pricing_strategy": "Pricing approach",
        "target_market": "Primary target market",
        "key_differentiators": ["Differentiator 1", "Differentiator 2"]
      }
    ],
    "indirect_competitors": [
      {
        "name": "Competitor Name",
        "threat_level": "High/Medium/Low",
        "competitive_advantage": "Their advantage",
        "market_position": "Market position"
      }
    ]
  },
  "market_analysis": {
    "market_leader": "Market leader name",
    "market_follower": "Market follower name",
    "market_nicher": "Market nicher name",
    "market_challenger": "Market challenger name"
  },
  "competitive_gaps": [
    {
      "gap": "Identified gap",
      "opportunity_size": "Small/Medium/Large",
      "difficulty_to_exploit": "Easy/Medium/Hard",
      "strategic_importance": "High/Medium/Low"
    }
  ],
  "strategic_recommendations": {
    "positioning_strategy": "Recommended positioning",
    "differentiation_strategy": "How to differentiate",
    "competitive_advantages": ["Advantage 1", "Advantage 2"],
    "threat_mitigation": ["Mitigation 1", "Mitigation 2"]
  }
}
```

## User Research

### Template: User Persona Development

**Use Case**: Create detailed user personas  
**Mode**: Chat (with large context)  
**Context Required**: Target audience, market research data

```markdown
# User Persona Development

## Research Context
- Target Audience: {TARGET_AUDIENCE}
- Industry: {INDUSTRY}
- Product/Service: {PRODUCT_SERVICE}
- Research Scope: {SCOPE}

## Persona Development Requirements
1. Demographics and psychographics
2. Goals and motivations
3. Pain points and challenges
4. Technology adoption patterns
5. Decision-making process
6. Communication preferences
7. Buying behavior
8. Success metrics

## Output Format
```json
{
  "personas": [
    {
      "name": "Persona Name",
      "title": "Job Title",
      "demographics": {
        "age_range": "Age range",
        "education": "Education level",
        "income": "Income range",
        "location": "Geographic location",
        "company_size": "Company size"
      },
      "psychographics": {
        "values": ["Value 1", "Value 2"],
        "interests": ["Interest 1", "Interest 2"],
        "lifestyle": "Lifestyle description",
        "personality_traits": ["Trait 1", "Trait 2"]
      },
      "goals": {
        "primary_goals": ["Goal 1", "Goal 2"],
        "secondary_goals": ["Goal 1", "Goal 2"],
        "success_metrics": ["Metric 1", "Metric 2"]
      },
      "pain_points": {
        "current_challenges": ["Challenge 1", "Challenge 2"],
        "frustrations": ["Frustration 1", "Frustration 2"],
        "unmet_needs": ["Need 1", "Need 2"]
      },
      "technology_profile": {
        "tech_savviness": "High/Medium/Low",
        "preferred_tools": ["Tool 1", "Tool 2"],
        "adoption_patterns": "Early adopter/early majority/late majority/laggard",
        "device_usage": ["Device 1", "Device 2"]
      },
      "decision_making": {
        "decision_process": "Decision process description",
        "influencers": ["Influencer 1", "Influencer 2"],
        "decision_criteria": ["Criteria 1", "Criteria 2"],
        "timeline": "Decision timeline"
      },
      "communication": {
        "preferred_channels": ["Channel 1", "Channel 2"],
        "communication_style": "Communication style",
        "content_preferences": ["Preference 1", "Preference 2"]
      },
      "buying_behavior": {
        "purchase_triggers": ["Trigger 1", "Trigger 2"],
        "budget_range": "Budget range",
        "evaluation_process": "Evaluation process",
        "objections": ["Objection 1", "Objection 2"]
      }
    }
  ],
  "insights": {
    "common_patterns": ["Pattern 1", "Pattern 2"],
    "key_insights": ["Insight 1", "Insight 2"],
    "opportunities": ["Opportunity 1", "Opportunity 2"],
    "recommendations": ["Recommendation 1", "Recommendation 2"]
  }
}
```

## Technical Requirements

### Template: Technical Specification Generator

**Use Case**: Generate technical requirements and specifications  
**Mode**: Chat (with large context)  
**Context Required**: Product requirements, technical constraints

```markdown
# Technical Specification Generator

## Product Context
- Product Name: {PRODUCT_NAME}
- Product Type: {PRODUCT_TYPE}
- Target Users: {TARGET_USERS}
- Business Requirements: {BUSINESS_REQUIREMENTS}

## Technical Analysis Requirements
1. Functional requirements
2. Non-functional requirements
3. Technical constraints
4. Integration requirements
5. Security requirements
6. Performance requirements
7. Scalability requirements
8. Technology stack recommendations

## Output Format
```json
{
  "functional_requirements": [
    {
      "id": "FR-001",
      "title": "Requirement Title",
      "description": "Detailed description",
      "priority": "High/Medium/Low",
      "acceptance_criteria": ["Criterion 1", "Criterion 2"],
      "dependencies": ["Dependency 1", "Dependency 2"]
    }
  ],
  "non_functional_requirements": {
    "performance": {
      "response_time": "Response time requirement",
      "throughput": "Throughput requirement",
      "concurrent_users": "Concurrent user requirement"
    },
    "security": {
      "authentication": "Authentication requirements",
      "authorization": "Authorization requirements",
      "data_protection": "Data protection requirements",
      "compliance": "Compliance requirements"
    },
    "reliability": {
      "uptime": "Uptime requirement",
      "availability": "Availability requirement",
      "fault_tolerance": "Fault tolerance requirements"
    },
    "scalability": {
      "horizontal_scaling": "Horizontal scaling requirements",
      "vertical_scaling": "Vertical scaling requirements",
      "load_balancing": "Load balancing requirements"
    }
  },
  "technical_constraints": {
    "platform": "Platform constraints",
    "browser_support": "Browser support requirements",
    "device_support": "Device support requirements",
    "integration_requirements": ["Integration 1", "Integration 2"]
  },
  "technology_stack": {
    "frontend": {
      "framework": "Frontend framework",
      "libraries": ["Library 1", "Library 2"],
      "tools": ["Tool 1", "Tool 2"]
    },
    "backend": {
      "language": "Programming language",
      "framework": "Backend framework",
      "database": "Database technology",
      "server": "Server technology"
    },
    "infrastructure": {
      "hosting": "Hosting solution",
      "cdn": "CDN requirements",
      "monitoring": "Monitoring tools",
      "deployment": "Deployment strategy"
    }
  },
  "integration_requirements": [
    {
      "system": "System name",
      "type": "Integration type",
      "requirements": "Integration requirements",
      "priority": "High/Medium/Low"
    }
  ],
  "security_requirements": {
    "authentication": "Authentication requirements",
    "authorization": "Authorization requirements",
    "data_encryption": "Data encryption requirements",
    "api_security": "API security requirements",
    "compliance": "Compliance requirements"
  },
  "performance_requirements": {
    "response_time": "Response time requirements",
    "throughput": "Throughput requirements",
    "concurrent_users": "Concurrent user requirements",
    "resource_usage": "Resource usage requirements"
  }
}
```

## Integration Guidelines

### Export Processing

#### JSON Export Processing
```bash
# Process AI Studio JSON exports
node scripts/process-ai-studio-json.js --input-file export.json --output-dir .claude/idea-to-design/test-gen/parking/

# Validate and transform data
node scripts/validate-ai-studio-data.js --source ai-studio --format json
```

#### Markdown Export Processing
```bash
# Process AI Studio Markdown exports
node scripts/process-ai-studio-markdown.js --input-file export.md --output-dir .claude/idea-to-design/test-gen/prd/

# Extract structured data
node scripts/extract-structured-data.js --input-file export.md --format json
```

### Data Validation

#### Required Fields
- `timestamp`: Export timestamp
- `model`: AI model used
- `tokens_used`: Token consumption
- `content`: Main content
- `metadata`: Additional metadata

#### Quality Checks
- Content completeness
- Format validation
- Data consistency
- Integration readiness

### Storage Organization

#### Directory Structure
```
.claude/idea-to-design/test-gen/
├── ai-studio-exports/
│   ├── market-research/
│   ├── opportunity-analysis/
│   ├── strategic-planning/
│   ├── competitive-analysis/
│   ├── user-research/
│   └── technical-requirements/
├── parking/
│   └── ai-studio-imports/
├── prd/
│   └── ai-studio-inputs/
└── architecture/
    └── ai-studio-inputs/
```

### Best Practices

1. **Consistent Naming**: Use descriptive, consistent file names
2. **Metadata Inclusion**: Always include relevant metadata
3. **Version Control**: Track changes and versions
4. **Quality Validation**: Validate data before integration
5. **Backup Strategy**: Maintain backups of important exports
6. **Documentation**: Document export sources and processing

---

**Last Updated**: January 24, 2025  
**Version**: 1.0  
**Status**: Production Ready
