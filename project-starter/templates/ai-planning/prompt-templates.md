# 🎯 AI Planning Prompt Templates

## Gap Analysis Prompts

### 1. Technical Stack Clarification
```
Analyze this project description and identify missing technical details:

[PROJECT_DESCRIPTION]

Please ask specific questions about:
- Preferred programming languages and frameworks
- Database and storage requirements
- API and integration needs
- Performance and scalability requirements
- Security and compliance considerations
- Deployment and hosting preferences

Format your response as:
**Missing Details**: [List specific gaps]
**Questions**: [Numbered list of clarifying questions]
**Recommendations**: [Suggested tech stack based on requirements]
```

### 2. Architecture Planning
```
Based on these requirements, help me plan the system architecture:

[REQUIREMENTS]

Please provide:
- High-level system architecture diagram (text-based)
- Component breakdown and responsibilities
- Data flow and integration points
- Technology choices with justifications
- Potential scalability bottlenecks
- Security considerations

Format as:
**Architecture**: [System overview]
**Components**: [Detailed breakdown]
**Data Flow**: [How data moves through system]
**Tech Stack**: [Specific technologies and versions]
**Scalability**: [Growth considerations]
**Security**: [Security measures needed]
```

### 3. Implementation Phases
```
Create a detailed implementation plan for this project:

[PROJECT_DETAILS]

Break down into phases with:
- Phase objectives and deliverables
- Dependencies between phases
- Estimated time and complexity
- Risk assessment and mitigation
- Testing strategy for each phase
- Success criteria

Format as:
**Phase 1**: [Name and objectives]
  - Tasks: [Specific implementation tasks]
  - Dependencies: [What must be completed first]
  - Timeline: [Estimated duration]
  - Risks: [Potential issues and solutions]
  - Testing: [How to verify success]

[Repeat for each phase]
```

## Verification Prompts

### 1. Code Review Template
```
Review this code implementation for issues:

[CODE_TO_REVIEW]

Check for:
- Critical errors that would break functionality
- Major issues affecting performance or security
- Minor improvements for code quality
- Adherence to best practices
- Missing error handling
- Security vulnerabilities

Format as:
**Critical Issues**: [Issues that must be fixed immediately]
**Major Issues**: [Issues that should be addressed soon]
**Minor Issues**: [Code quality improvements]
**Security**: [Security concerns and fixes]
**Performance**: [Performance optimization opportunities]
**Best Practices**: [Code quality recommendations]
```

### 2. Requirements Verification
```
Verify this implementation against the original requirements:

[ORIGINAL_REQUIREMENTS]
[IMPLEMENTED_CODE]

Check:
- All requirements have been implemented
- Implementation matches the intended design
- No scope creep or missing features
- Performance meets specified criteria
- Security requirements are satisfied

Format as:
**Requirements Coverage**: [What's implemented vs. what was requested]
**Gaps**: [Missing functionality]
**Extras**: [Features added beyond requirements]
**Compliance**: [How well it meets the original spec]
**Recommendations**: [Suggestions for improvement]
```

## Project-Specific Templates

### AI Agent Projects
```
Plan an AI agent project with these requirements:

[AGENT_REQUIREMENTS]

Consider:
- Agent framework choice (CrewAI, LangGraph, AutoGen, custom)
- Agent roles and responsibilities
- Tool integration and capabilities
- Communication patterns and handoffs
- Data sources and processing
- Testing and validation strategies

Format as:
**Agent Architecture**: [Overall design]
**Agent Roles**: [Specific agent definitions]
**Tools & Capabilities**: [What each agent can do]
**Workflow**: [How agents interact]
**Data Flow**: [Information processing]
**Testing**: [Validation approach]
```

### Web Application Projects
```
Plan a web application with these specifications:

[WEB_APP_REQUIREMENTS]

Cover:
- Frontend framework and UI components
- Backend API design and endpoints
- Database schema and relationships
- Authentication and authorization
- State management and caching
- Deployment and CI/CD pipeline

Format as:
**Frontend**: [UI framework and components]
**Backend**: [API design and architecture]
**Database**: [Schema and data modeling]
**Auth**: [User management and security]
**State**: [Data flow and caching]
**Deployment**: [Release and hosting strategy]
```

### Mobile Application Projects
```
Plan a mobile application with these needs:

[MOBILE_APP_REQUIREMENTS]

Address:
- Platform choice (React Native, Flutter, native)
- UI/UX design considerations
- Device-specific features and APIs
- Offline functionality and sync
- Performance optimization
- App store deployment

Format as:
**Platform**: [Technology choice and reasoning]
**UI/UX**: [Design considerations]
**Features**: [Device-specific capabilities]
**Offline**: [Data sync and storage]
**Performance**: [Optimization strategies]
**Deployment**: [App store and distribution]
```

## Usage Instructions

1. **Copy the relevant prompt template**
2. **Replace placeholders with your project details**
3. **Paste into Cursor chat**
4. **Follow the structured response format**
5. **Use responses to guide implementation**

## Integration with Project Starter

These templates work seamlessly with:
- AI agent frameworks (CrewAI, LangGraph, AutoGen)
- Web frameworks (Next.js, FastAPI, Flask)
- Mobile development (React Native, Expo)
- Database integration (Supabase, PostgreSQL)
- Authentication systems (NextAuth, JWT)
