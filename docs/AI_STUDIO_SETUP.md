# Google AI Studio Setup Guide

## Overview

Google AI Studio is a web-based platform for building and testing AI applications using Google's Gemini models. This guide covers workspace setup, authentication, rate limits, and integration with the Software Factory.

## Table of Contents

- [Getting Started](#getting-started)
- [Workspace Creation](#workspace-creation)
- [Authentication Options](#authentication-options)
- [Rate Limits & Quotas](#rate-limits--quotas)
- [Export Formats](#export-formats)
- [Software Factory Integration](#software-factory-integration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Google account (jckagnew@gmail.com)
- Access to Google AI Studio
- API key for programmatic access

### Accessing AI Studio

1. **Navigate to**: [https://aistudio.google.com](https://aistudio.google.com)
2. **Sign in** with your Google account
3. **Accept** terms of service and privacy policy
4. **Complete** the onboarding tutorial

## Workspace Creation

### Creating a New Workspace

1. **Click** "Create" in the left sidebar
2. **Choose** workspace type:
   - **Chat**: Interactive conversations with AI
   - **Build**: Create custom applications
   - **Generate Media**: Create images, audio, video

### Workspace Configuration

#### Chat Workspace
- **Purpose**: Interactive AI conversations and analysis
- **Best for**: Market research, opportunity evaluation, strategic planning
- **Context**: Large context window for comprehensive analysis

#### Build Workspace
- **Purpose**: Create custom AI applications
- **Best for**: Automated workflows, API integrations
- **Context**: Structured prompts and responses

#### Generate Media Workspace
- **Purpose**: Create visual and audio content
- **Best for**: Marketing materials, presentations, demos
- **Context**: Visual asset generation

### Workspace Naming Convention

Use descriptive names for easy identification:
- `C-Level-Market-Research`
- `Business-Opportunity-Analysis`
- `Strategic-Planning-Sessions`
- `Media-Asset-Generation`

## Authentication Options

### API Key Authentication (Recommended)

1. **Navigate** to "Get API Key" in left sidebar
2. **Click** "Create API Key"
3. **Choose** key type:
   - **Restricted**: Limited to specific projects
   - **Unrestricted**: Full access (use with caution)
4. **Copy** the API key
5. **Store** securely in environment variables

### Service Account Authentication

For production applications:
1. **Go to** Google Cloud Console
2. **Create** a service account
3. **Download** JSON credentials
4. **Configure** authentication in your application

### Current Configuration

```json
{
  "apiKey": "AIzaSyCzvHSDaZJAkV-iXBm20rlCgncjJTFQwm8",
  "account": "jckagnew@gmail.com",
  "authentication": "API Key",
  "status": "Active"
}
```

## Rate Limits & Quotas

### Free Tier Limits

- **Requests per minute**: 60
- **Requests per day**: 1,500
- **Tokens per minute**: 32,000
- **Tokens per day**: 50,000

### Paid Tier Limits

- **Requests per minute**: 1,000
- **Requests per day**: 50,000
- **Tokens per minute**: 1,000,000
- **Tokens per day**: 10,000,000

### Model-Specific Limits

| Model | Max Tokens | Context Window | Rate Limit |
|-------|------------|----------------|------------|
| Gemini 2.5 Pro | 8,192 | 1M tokens | 60/min |
| Gemini 2.5 Flash | 8,192 | 1M tokens | 1,000/min |
| Gemini 2.0 Flash | 8,192 | 1M tokens | 1,000/min |

### Monitoring Usage

1. **Check** usage in AI Studio dashboard
2. **Monitor** API quotas in Google Cloud Console
3. **Set up** alerts for quota approaching limits
4. **Implement** rate limiting in your applications

## Export Formats

### Supported Export Formats

#### JSON Export
```json
{
  "conversation": {
    "id": "conversation_123",
    "title": "Market Analysis",
    "messages": [
      {
        "role": "user",
        "content": "Analyze the AI sales automation market"
      },
      {
        "role": "assistant",
        "content": "The AI sales automation market..."
      }
    ],
    "metadata": {
      "model": "gemini-2.5-pro",
      "timestamp": "2025-01-24T18:30:00Z",
      "tokens_used": 1500
    }
  }
}
```

#### Markdown Export
```markdown
# Market Analysis: AI Sales Automation

## Executive Summary
The AI sales automation market represents a significant opportunity...

## Market Size
- Current market: $5-7 billion
- Projected growth: 18-22% CAGR
- Target market: $15-20 billion by 2028

## Key Insights
1. Market consolidation is accelerating
2. AI-native solutions are gaining traction
3. C-Level executives are driving adoption
```

#### CSV Export
```csv
Metric,Value,Source,Confidence
Market Size,$5-7B,Industry Report,High
Growth Rate,18-22%,Analyst Projections,Medium
Competitors,15+,Market Research,High
```

### Export Best Practices

1. **Include metadata**: Timestamp, model used, token count
2. **Structure data**: Use consistent formatting
3. **Validate exports**: Check for completeness
4. **Version control**: Track changes over time

## Software Factory Integration

### Export Locations

#### For Parking Lot Ingestion
```
.claude/idea-to-design/test-gen/parking/
├── ai-studio-exports/
│   ├── market-research/
│   ├── opportunity-analysis/
│   └── strategic-planning/
└── README.md
```

#### For PRD Generation
```
.claude/idea-to-design/test-gen/prd/
├── ai-studio-inputs/
│   ├── market-insights/
│   ├── user-research/
│   └── competitive-analysis/
```

#### For Architecture Generation
```
.claude/idea-to-design/test-gen/architecture/
├── ai-studio-inputs/
│   ├── technical-requirements/
│   ├── system-constraints/
│   └── performance-requirements/
```

### Integration Workflow

1. **Export** from AI Studio in JSON format
2. **Save** to appropriate directory
3. **Process** through Software Factory pipeline
4. **Validate** against existing data
5. **Integrate** with downstream processes

### Automated Processing

```bash
# Process AI Studio exports
node scripts/process-ai-studio-exports.js --input-dir .claude/idea-to-design/test-gen/parking/ai-studio-exports/

# Validate parking lot entries
node scripts/validate-parking.js --source ai-studio

# Generate reports
node scripts/generate-reports.js --include-ai-studio
```

## Best Practices

### Workspace Organization

1. **Use descriptive names** for workspaces
2. **Group related projects** together
3. **Archive completed** workspaces
4. **Document** workspace purposes

### Prompt Engineering

1. **Be specific** about requirements
2. **Provide context** for better responses
3. **Use examples** to guide output format
4. **Iterate** on prompts for better results

### Data Management

1. **Export regularly** to avoid data loss
2. **Backup** important conversations
3. **Version control** exported data
4. **Clean up** old workspaces

### Security

1. **Protect API keys** from exposure
2. **Use environment variables** for secrets
3. **Implement access controls** for workspaces
4. **Monitor** usage for anomalies

## Troubleshooting

### Common Issues

#### API Key Not Working
- **Check** key format (starts with `AIzaSy`)
- **Verify** key permissions
- **Test** with simple request
- **Regenerate** if necessary

#### Rate Limit Exceeded
- **Wait** for quota reset
- **Implement** exponential backoff
- **Upgrade** to paid tier if needed
- **Optimize** request frequency

#### Export Failures
- **Check** file permissions
- **Verify** export format
- **Retry** with smaller chunks
- **Contact** support if persistent

#### Model Not Available
- **Check** model name spelling
- **Verify** model availability
- **Use** alternative model
- **Update** to latest version

### Getting Help

1. **Check** AI Studio documentation
2. **Search** community forums
3. **Contact** Google support
4. **Review** error messages

### Support Resources

- **Documentation**: [https://ai.google.dev/docs](https://ai.google.dev/docs)
- **Community**: [https://discuss.ai.google.dev](https://discuss.ai.google.dev)
- **Support**: [https://support.google.com/aistudio](https://support.google.com/aistudio)

## Next Steps

1. **Set up** your first workspace
2. **Create** API key for integration
3. **Test** export functionality
4. **Integrate** with Software Factory
5. **Monitor** usage and performance

---

**Last Updated**: January 24, 2025  
**Version**: 1.0  
**Status**: Production Ready
