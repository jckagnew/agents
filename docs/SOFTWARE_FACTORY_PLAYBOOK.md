# 🏭 Software Factory Playbook

## Overview
This playbook documents the complete Software Factory workflow from idea to production code, including all automation tools and integration points.

**Last Updated**: January 2025  
**Status**: Production Ready

---

## 🎯 Workflow Overview

The Software Factory follows a structured 14-phase approach:

1. **Discovery** - Interactive requirements gathering
2. **AI Studio Research** - AI-powered market and opportunity analysis
3. **PRD Generation** - Comprehensive documentation creation
4. **Architecture Generation** - System design documentation
5. **UX Generation** - User flows and interaction patterns
6. **Backlog Sync** - Extract and track future features
7. **Future-Feature Parking** - Capture and evaluate speculative ideas
8. **Security Scanning** - Static security analysis
9. **Test Automation** - Unit, integration, and E2E testing
10. **DevOps Scaffold** - Containerization and infrastructure
11. **Design Generation** - Visual mockups and prototypes
12. **Visual QA** - Automated quality assurance
13. **Feedback & Refinement** - Client validation and iteration
14. **Code Generation** - Production-ready application

---

## 📋 Phase 1: Discovery

**Purpose**: Transform vague client ideas into structured requirements

**Tool**: `scripts/idea-to-design.sh` (Interactive mode)

**Inputs**:
- Client's initial app idea
- Interactive Q&A session

**Outputs**:
- `session-X/requirements/iteration-0.json`
- Structured requirements with app name, type, features, design preferences

**Key Questions**:
- App name and type
- Core features (must-have vs nice-to-have)
- Design style preferences
- Brand colors and inspiration
- Success criteria

---

## 🤖 Phase 2: AI Studio Research

**Purpose**: Leverage Google AI Studio for comprehensive market research, opportunity analysis, and strategic insights

**Tool**: Google AI Studio (Web-based) + `workspaces/c-level-business-discovery/`

**Inputs**:
- Initial app idea from Discovery phase
- Market research requirements
- Strategic analysis needs
- Competitive landscape questions

**Outputs** (`.claude/idea-to-design/session-X/ai-studio-research/`):
- `market-analysis.json` - Market size, trends, opportunities
- `opportunity-evaluation.json` - Financial viability and risk assessment
- `competitive-analysis.json` - Competitor landscape and positioning
- `user-research.json` - User personas and behavior insights
- `strategic-recommendations.json` - Strategic direction and next steps

**Key Features**:
- **Market Gap Discovery**: Identify underserved markets and opportunities
- **Financial Viability Analysis**: Comprehensive business case development
- **Media Asset Generation**: Create visual content and presentations
- **Strategic Planning**: Develop strategic frameworks and roadmaps
- **Competitive Intelligence**: Analyze competitive landscape and positioning
- **User Research**: Generate detailed user personas and insights

**AI Studio Workspaces**:
- **Chat Workspace**: Interactive analysis and research
- **Build Workspace**: Automated workflows and API integrations
- **Generate Media**: Visual content and presentation materials

**Prompt Templates**:
- Market Opportunity Scanner
- Business Case Builder
- Visual Content Creator
- Strategic Framework Builder
- Competitor Intelligence
- User Persona Development

**Status**: ✅ Production Ready - Complete AI Studio integration
**Documentation**: See [docs/AI_STUDIO_SETUP.md](./AI_STUDIO_SETUP.md) for setup guide
**Prompts**: See [docs/AI_STUDIO_PROMPTS.md](./AI_STUDIO_PROMPTS.md) for template library

### AI Studio Research Process

#### 1. Market Analysis
```bash
# Export from AI Studio Chat workspace
# Save as: .claude/idea-to-design/session-X/ai-studio-research/market-analysis.json

# Process with Software Factory
node scripts/process-ai-studio-research.js --session SESSION_DIR --type market-analysis
```

#### 2. Opportunity Evaluation
```bash
# Export from AI Studio Chat workspace
# Save as: .claude/idea-to-design/session-X/ai-studio-research/opportunity-evaluation.json

# Process with Software Factory
node scripts/process-ai-studio-research.js --session SESSION_DIR --type opportunity-evaluation
```

#### 3. Competitive Analysis
```bash
# Export from AI Studio Chat workspace
# Save as: .claude/idea-to-design/session-X/ai-studio-research/competitive-analysis.json

# Process with Software Factory
node scripts/process-ai-studio-research.js --session SESSION_DIR --type competitive-analysis
```

#### 4. User Research
```bash
# Export from AI Studio Chat workspace
# Save as: .claude/idea-to-design/session-X/ai-studio-research/user-research.json

# Process with Software Factory
node scripts/process-ai-studio-research.js --session SESSION_DIR --type user-research
```

#### 5. Feature Ideas to Parking Lot

**NEW**: AI Studio exports can now be automatically ingested into the Future Feature Parking system

```bash
# Ingest AI Studio feature ideas into parking lot
node scripts/ai-studio-ingest.js \
  --session-dir SESSION_DIR \
  --source ai-studio-features.json

# With auto-tagging
npm run ai-studio:ingest:auto-tag -- ai-studio-features.json

# With stricter confidence threshold (0.7 instead of 0.6)
npm run ai-studio:ingest:strict -- ai-studio-features.json

# Dry run to preview
npm run ai-studio:dry-run -- ai-studio-features.json
```

**Automatic Conversion**:
- AI Studio `feasibility` → Parking Lot `estimatedValue` (1-10)
- AI Studio `cost/effort` → Parking Lot `estimatedEffort` (1-10)
- AI Studio `confidence` → Parking Lot `confidence` (0.0-1.0)
- AI Studio `opportunity_driver` → Parking Lot `drivers`
- AI Studio `timeframe` → Parking Lot `targetPhase`

**Auto-Tagging**: Content analysis automatically detects theme (user-experience, performance, security, analytics, etc.)

**Promotion-Ready Detection**: Ideas with Confidence ≥ 0.6 AND Value ≥ 7 are automatically flagged for promotion to active backlog
```

#### 5. Strategic Planning
```bash
# Export from AI Studio Chat workspace
# Save as: .claude/idea-to-design/session-X/ai-studio-research/strategic-recommendations.json

# Process with Software Factory
node scripts/process-ai-studio-research.js --session SESSION_DIR --type strategic-planning
```

### Integration with Software Factory

#### PRD Generation Integration
- **Market insights** feed into market analysis section
- **User research** informs user personas and requirements
- **Competitive analysis** shapes positioning and differentiation
- **Strategic recommendations** guide product strategy

#### Architecture Generation Integration
- **Technical requirements** from AI Studio analysis
- **Performance requirements** based on market needs
- **Integration requirements** from competitive analysis
- **Security requirements** from strategic planning

#### UX Generation Integration
- **User personas** from AI Studio user research
- **User flows** based on behavior insights
- **Interaction patterns** from competitive analysis
- **Accessibility requirements** from strategic planning

#### Parking Lot Integration
- **Market opportunities** automatically routed to parking lot
- **Strategic recommendations** captured as future features
- **Competitive gaps** identified as potential opportunities
- **User insights** inform feature prioritization

### Export Processing

#### JSON Export Processing
```bash
# Process AI Studio JSON exports
node scripts/process-ai-studio-json.js --input-file export.json --output-dir .claude/idea-to-design/session-X/ai-studio-research/

# Validate and transform data
node scripts/validate-ai-studio-data.js --source ai-studio --format json
```

#### Markdown Export Processing
```bash
# Process AI Studio Markdown exports
node scripts/process-ai-studio-markdown.js --input-file export.md --output-dir .claude/idea-to-design/session-X/ai-studio-research/

# Extract structured data
node scripts/extract-structured-data.js --input-file export.md --format json
```

### Quality Assurance

#### Data Validation
- **Content completeness**: Ensure all required sections are present
- **Format validation**: Verify JSON structure and required fields
- **Data consistency**: Check for logical consistency across analyses
- **Integration readiness**: Validate data for downstream processing

#### Quality Metrics
- **Analysis depth**: Comprehensive coverage of required topics
- **Data accuracy**: Factual accuracy and source validation
- **Strategic value**: Actionable insights and recommendations
- **Integration success**: Successful processing by downstream tools

### Best Practices

#### AI Studio Usage
- **Use specific prompts**: Leverage template library for consistent results
- **Provide context**: Include relevant background information
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

---

## 🏷️ Phase 2.5: Business Name Vetting

**Purpose**: Automated validation of business names, DBA names, and product names through comprehensive domain, trademark, and social media screening

**Tool**: `scripts/name-vetting.js`

**Inputs**:
- List of candidate business names (from AI Studio or Discovery)
- Industry category (for trademark classification)
- Optional: Preferred domain extensions

**Outputs** (`.claude/idea-to-design/session-X/name-vetting/`):
- `vetting-report-TIMESTAMP.json` - Comprehensive scoring and risk assessment
- `name-ranking.md` - Ranked list of candidates with recommendations
- Individual name reports with detailed findings

**Scoring System** (0-100 points):
- **Domain Availability** (40 points):
  - .com available = 40 points
  - .io or .co available = 30 points
  - Other TLDs available = 20 points
  - No domains available = 0 points
- **Trademark Risk** (30 points):
  - No conflicts = 30 points
  - Similar marks in different industry = 15 points
  - Direct conflict = 0 points (⚠️ AVOID)
- **Social Handle Availability** (20 points):
  - All 3 platforms available (Twitter/X, Instagram, LinkedIn) = 20 points
  - 2 of 3 available = 13 points
  - 1 of 3 available = 7 points
  - None available = 0 points
- **Uniqueness** (10 points):
  - < 1,000 Google results = 10 points (very unique)
  - 1,000-10,000 results = 5 points (moderately unique)
  - > 10,000 results = 0 points (generic/common)

**Risk Assessment**:
- **70-100**: EXCELLENT - Strong candidate, proceed with confidence
- **50-69**: GOOD - Viable option, minor concerns to address
- **30-49**: RISKY - Significant concerns, additional research needed
- **0-29**: AVOID - High risk, select alternative name

**Usage**:

```bash
# Vet a single business name
node scripts/name-vetting.js --name "Acme Corp" --industry "Software"

# Vet multiple candidates (returns ranked list)
node scripts/name-vetting.js --names "Acme Corp,Widget Labs,Tech Solutions"

# Batch processing from JSON file
node scripts/name-vetting.js --input names.json --output vetting-report.json

# Deep check mode (slower, more thorough)
node scripts/name-vetting.js --name "Acme Corp" --deep-check
```

**API Integration Requirements**:

The name vetting script requires API keys for comprehensive checks:

```bash
# Environment variables
export DOMAINR_API_KEY="your_domainr_key"          # Domain availability
export GODADDY_API_KEY="your_godaddy_key"          # Fallback domain check
export GODADDY_API_SECRET="your_godaddy_secret"
export USPTO_API_KEY="your_uspto_key"              # Trademark screening
export GOOGLE_SEARCH_API_KEY="your_google_key"     # Uniqueness check
```

**Key Checks**:

#### 1. Domain Availability
- Primary: Domainr API for multi-TLD availability check
- Fallback: GoDaddy API for domain search
- Extensions checked: .com, .io, .co, .app, .tech, .ai
- Alternative suggestions when preferred domain unavailable

#### 2. Trademark Screening
- Primary: USPTO TSDR (Trademark Status & Document Retrieval)
- Fallback: PatentsView API
- Search strategies:
  - Exact match search
  - Phonetic similarity (Soundex)
  - Levenshtein distance < 3
  - Industry class filtering (Nice Classification)
- Risk levels: HIGH (direct conflict), MEDIUM (similar marks), LOW (no conflicts)

#### 3. Social Handle Availability
- **Twitter/X**: API v2 or direct HTTP check
- **Instagram**: Web scraping (API requires Facebook OAuth)
- **LinkedIn**: LinkedIn Pages API or web scraping
- Handle normalization per platform rules
- Alternative suggestions when unavailable

#### 4. Uniqueness Scoring
- Google Custom Search API or Bing Web Search API
- Quoted search for exact name matches
- Result count analysis for generic name detection
- Top 10 results reviewed for conflicts

**Workflow Integration**:

```bash
# 1. Generate name candidates in AI Studio
# Export to: .claude/idea-to-design/session-X/ai-studio-research/name-candidates.json

# 2. Run name vetting
node scripts/name-vetting.js \
  --input .claude/idea-to-design/session-X/ai-studio-research/name-candidates.json \
  --output .claude/idea-to-design/session-X/name-vetting/vetting-report.json \
  --industry "Software"

# 3. Review results and select top candidate
cat .claude/idea-to-design/session-X/name-vetting/name-ranking.md

# 4. Proceed with PRD generation using validated name
```

**Best Practices**:

- **Run early**: Vet names before investing in branding or development
- **Batch processing**: Always vet multiple candidates to have backups
- **Legal review**: For HIGH trademark risk, always consult attorney
- **Domain registration**: Secure top candidate domains immediately after vetting
- **Social handles**: Claim available handles even if not immediately using
- **Documentation**: Save vetting reports for future reference and compliance

**Quality Checks**:
- [ ] All candidate names vetted with scores
- [ ] Trademark conflicts identified and documented
- [ ] Domain availability confirmed for top candidates
- [ ] Social handles checked across all platforms
- [ ] Risk assessment documented with recommendations
- [ ] Alternative names identified if primary has issues
- [ ] Legal review flagged for high-risk situations

**Status**: 🚧 Scaffold Complete - API integration pending
**Script**: [scripts/name-vetting.js](../scripts/name-vetting.js)
**Backlog**: P1 task in [global/backlog/manual-queue.json](../.claude/idea-to-design/global/backlog/manual-queue.json)

**Future Enhancement**: Name Audit Service for clients (tracked in global parking lot)

---

## 📄 Phase 3: PRD Bundle Generation

**Purpose**: Transform basic requirements into comprehensive product documentation

**Tool**: `scripts/generate-prd.js`

**Inputs**:
- `requirements/iteration-X.json`

**Outputs** (`.claude/idea-to-design/session-X/prd/`):
- `01-personas.md` - User personas with demographics, goals, frustrations, jobs-to-be-done
- `02-problem-solution.md` - Escape-arrival framing, value proposition, success metrics  
- `03-acceptance-criteria.md` - Must-have features, non-functional requirements, definition of done

**Usage**:
```bash
node scripts/generate-prd.js \
  --requirements .claude/idea-to-design/session-X/requirements/iteration-0.json \
  --output-dir .claude/idea-to-design/session-X/prd
```

**Quality Checks**:
- [ ] All 3 PRD documents generated
- [ ] Personas include demographics, goals, frustrations, jobs-to-be-done
- [ ] Problem/solution includes escape-arrival journey
- [ ] Acceptance criteria include must-have features and non-functional requirements
- [ ] Grammar and terminology consistency

---

## 🏗️ Phase 3: Architecture Generation (Claude Integration)

**Purpose**: Generate system architecture and technical specifications

**Tool**: Claude Code (✅ Active - generating comprehensive architecture docs)

**Inputs**:
- PRD Bundle from Phase 2
- Requirements from Phase 1

**Outputs** (`.claude/idea-to-design/session-X/architecture/`):
- `architecture-data-model.md` - Complete data schema with TypeScript interfaces
- `architecture-services.md` - Service architecture and module breakdown
- `architecture-tech-stack.md` - Technology choices and rationale
- `architecture-api.md` - API specifications (when backend needed)
- `architecture-deployment.md` - Deployment and infrastructure specs

**Key Deliverables**:
- **Data Model**: Entry/Goal entities with validation rules and relationships
- **Tech Stack**: Next.js 14, React Context, localStorage, Vercel deployment
- **Services**: UI Layer, State Management, Data Persistence modules
- **Security**: Privacy-first local storage, GDPR compliance
- **Performance**: <2s load time, <100ms entry creation targets

**Validation**: Respect-Spec Framework validates compliance with PRD requirements
**Status**: ✅ Production Ready - Architecture generation working

---

## 🎨 Phase 4: UX Generation (Claude Integration)

**Purpose**: Create user flows, wireframes, and interaction specifications

**Tool**: Claude Code (🚧 In Progress - placeholders ready for integration)

**Inputs**:
- PRD Bundle from Phase 2
- Architecture from Phase 3

**Outputs** (`.claude/idea-to-design/session-X/ux/`):
- `user-flows.md` - User journey diagrams with Mermaid flows
- `wireframes.md` - Low-fidelity screen layouts and component specs
- `interaction-specs.md` - Detailed interaction behaviors and animations
- `accessibility-guidelines.md` - WCAG 2.1 AA compliance specifications

**Key Deliverables**:
- **User Flows**: Primary flows (onboarding, tracking, goals, progress) + persona-specific journeys
- **Wireframes**: 6 core screens (splash, dashboard, log entry, history, settings, goals)
- **Interactions**: Core interactions, animations, gestures, performance specs
- **Accessibility**: WCAG 2.1 AA compliance, screen reader support, visual accessibility

**Validation**: Respect-Spec Framework validates UX compliance with PRD and architecture
**Status**: 🚧 In Progress - Placeholders created, waiting for Claude Code integration
**Acceptance Criteria**: See `docs/UX_ACCEPTANCE_CRITERIA.md` for detailed requirements

---

## 📋 Phase 5: Backlog Sync

**Purpose**: Extract and sync backlog items from documentation to issue tracker

**Tool**: `scripts/backlog-sync.js`

**Inputs**:
- PRD, Architecture, and UX documentation from previous phases
- Respect-spec audit reports
- Optional: Manual backlog input JSON file

**Outputs** (`.claude/idea-to-design/session-X/backlog/`):
- `backlog-TIMESTAMP.json` - Extracted backlog items with metadata
- `audit-TIMESTAMP.json` - Sync audit trail (success/failure logs)

**Key Features**:
- **Automated Extraction**: Scans documentation for future features, nice-to-haves, and audit findings
- **GitHub Integration**: Pushes backlog items to GitHub Issues using `gh` CLI
- **Deduplication**: Prevents duplicate items across multiple source documents
- **Audit Logging**: Complete trail of synced items with timestamps and sources
- **Dry-Run Mode**: Preview changes before creating actual issues

**Item Sources**:
- **PRD**: Nice-to-have features, future considerations from acceptance criteria
- **Architecture**: Future enhancements, API additions, migration paths from architecture docs
- **UX**: Future features from UX flows (e.g., command palette, advanced interactions)
- **Audit**: Issues and missing features flagged by respect-spec validation

**Status**: ✅ Production Ready - Fully implemented with GitHub integration

### Backlog Sync Process

#### 1. Basic Usage (Extract from Documentation)
```bash
# Extract backlog items and sync to GitHub (live mode)
node scripts/backlog-sync.js \
  --session-dir .claude/idea-to-design/session-X

# Dry run (preview without creating issues)
node scripts/backlog-sync.js \
  --session-dir .claude/idea-to-design/session-X \
  --dry-run
```

#### 2. Using Manual Input File
```bash
# Sync from pre-defined backlog JSON
node scripts/backlog-sync.js \
  --input .claude/idea-to-design/session-X/backlog-input.json \
  --dry-run
```

#### 3. View Sync Results
```bash
# View backlog items
cat .claude/idea-to-design/session-X/backlog/backlog-TIMESTAMP.json

# View audit log
cat .claude/idea-to-design/session-X/backlog/audit-TIMESTAMP.json

# List all synced items
ls -lh .claude/idea-to-design/session-X/backlog/
```

#### 4. Prerequisites
```bash
# Install GitHub CLI (if not already installed)
brew install gh

# Authenticate with GitHub
gh auth login

# Verify repository access
gh repo view
```

### Supported Issue Trackers

| Provider | Status | CLI Tool | Authentication |
|----------|--------|----------|----------------|
| **GitHub** | ✅ Implemented | `gh` CLI | GitHub authentication via `gh auth login` |
| **GitLab** | 🚧 Future | `glab` CLI | Personal Access Token |
| **Jira** | 🚧 Future | `jira` CLI | API Token + Email |
| **Linear** | 🚧 Future | Linear API | API Key |

**Current Implementation**: GitHub Issues via GitHub CLI (`gh`)

### Backlog Item Structure

```json
{
  "title": "[Category] Feature title",
  "description": "Detailed description with context",
  "priority": "P1|P2|P3",
  "source": "PRD (Nice-to-Have)|Architecture (filename)|UX (filename)|Spec Compliance Audit",
  "labels": ["enhancement", "post-mvp", "backend", "api", "future", "ux", "bug", "audit"],
  "status": "backlog|todo"
}
```

**Priority Levels**:
- **P1**: Critical issues from spec audit that block MVP
- **P2**: Important enhancements (API, command palette, etc.)
- **P3**: Nice-to-have improvements (scaling, migrations)

**Automatically Generated Labels**:
- **Source**: `enhancement`, `bug`, `audit`
- **Category**: `backend`, `api`, `ux`, `architecture`, `infrastructure`
- **Phase**: `post-mvp`, `future`, `scaling`

### Extraction Patterns

**From PRD** (`03-acceptance-criteria.md`):
- Nice-to-have features section
- "Future" mentions in feature descriptions

**From Architecture** (all `architecture-*.md` files):
- "Future Consideration" sections
- "If API Added Later" sections
- "Migration Path" sections

**From UX** (all `ux-*.md` files):
- "Future" mentions in interaction specs
- Command palette references
- Advanced feature mentions

**From Audit** (`respect-spec-report.json`):
- Architecture validation issues
- UX validation issues
- Missing required features

---

## 🅿️ Phase 6: Future-Feature Parking

**Purpose**: Capture and evaluate speculative feature ideas that aren't ready for immediate development but have potential future value

**Tool**: `scripts/parking-sync.js` + JSON templates

**Inputs**:
- Generated application code from previous phases
- User feedback and feature requests
- Market research and competitive analysis
- Strategic planning documents

**Outputs** (`.claude/idea-to-design/session-X/parking/`):
- `parking-template.json` - Template for feature ideas
- `feature-{timestamp}-{name}.json` - Individual feature entries
- `parking-summary.md` - Summary of all parked features
- `evaluation-report.json` - Value and confidence analysis
- `promotion-candidates.json` - Items ready for backlog promotion

**Key Features**:
- **Structured Capture**: JSON schema for consistent feature documentation
- **Value Assessment**: 1-10 value scoring with confidence levels
- **Dependency Tracking**: Links between features and requirements
- **Evaluation Framework**: Systematic approach to feature prioritization
- **Promotion Pipeline**: Clear path from parking to backlog
- **Analytics**: Insights into feature trends and patterns

**Template Fields**:
- **Core**: title, description, opportunity_driver, estimated_value, confidence
- **Planning**: dependencies, timeframe, notes
- **Metadata**: created_date, created_by, status, priority, category, tags, source

**Status**: ✅ Production Ready - Templates and documentation complete
**Documentation**: See [docs/FUTURE_FEATURE_TEMPLATES.md](./FUTURE_FEATURE_TEMPLATES.md) for complete guide

### Future-Feature Parking Process

#### 1. Capture Feature Ideas
```bash
# Generate parking template
npm run parking:template

# Add new feature idea
cp .claude/idea-to-design/test-gen/parking/parking-template.json \
   .claude/idea-to-design/session-X/parking/feature-20250124-ai-chat.json

# Edit the feature entry
nano .claude/idea-to-design/session-X/parking/feature-20250124-ai-chat.json
```

#### 2. Evaluate and Score
```bash
# Validate parking entries
npm run parking:validate

# Generate evaluation report
npm run parking:evaluate

# Find high-value items
npm run parking:search -- --min-value 7
```

#### 3. Promote to Backlog
```bash
# Find promotion candidates
npm run parking:ready-for-promotion

# Promote specific feature
npm run parking:promote -- feature-20250124-ai-chat.json

# Sync with backlog
npm run parking:sync
```

#### 4. Analytics and Reporting
```bash
# Generate parking summary
npm run parking:report

# Value distribution analysis
npm run parking:analytics -- --value-distribution

# Category breakdown
npm run parking:analytics -- --category-breakdown
```

### Feature Evaluation Framework

#### Value Assessment (1-10)
- **Revenue Impact**: Direct revenue generation or cost savings
- **User Satisfaction**: Improvement in user experience metrics
- **Competitive Advantage**: Differentiation from competitors
- **Strategic Alignment**: Fit with company strategy
- **Market Opportunity**: Size and growth potential

#### Confidence Levels (0-1)
- **0-0.3**: Low confidence, rough estimates
- **0.4-0.6**: Medium confidence, some data available
- **0.7-0.8**: High confidence, good analysis
- **0.9-1.0**: Very high confidence, extensive validation

#### Promotion Criteria
Items are ready for promotion when they meet:
- **High Value**: Estimated value ≥ 7
- **High Confidence**: Confidence ≥ 0.7
- **Clear Requirements**: Detailed understanding of what to build
- **Dependencies Resolved**: Blocking items are completed
- **Resource Available**: Team capacity and timeline alignment

### Integration Points

- **Backlog Sync**: High-value parked items can be promoted to backlog
- **Architecture Generation**: Parking helps inform system design decisions
- **UX Generation**: Feature ideas influence user experience planning
- **Code Generation**: Parking provides input for future development

---

## 🔒 Phase 7: Security Scanning

**Purpose**: Static security analysis to identify vulnerabilities before deployment

**Tool**: `scripts/security-scan.js`

**Inputs**:
- Source code directories (src/, scripts/, apps/, etc.)
- Configuration files (.semgrep.yml, .bandit)

**Outputs** (`.claude/idea-to-design/session-X/security/`):
- `semgrep-report-TIMESTAMP.json` - Semgrep findings (JavaScript/TypeScript)
- `bandit-report-TIMESTAMP.json` - Bandit findings (Python)
- `security-summary-TIMESTAMP.md` - Aggregated summary with remediation notes

**Key Features**:
- **Semgrep**: JavaScript/TypeScript security analysis with OWASP Top 10 coverage
- **Bandit**: Python security analysis with CWE mappings
- **Fail on High**: CI/CD integration fails builds on critical/high severity findings
- **Backlog Integration**: High-severity findings automatically captured for tracking

**Status**: ✅ Production Ready - Fully integrated with CI/CD

### Security Scanning Process

#### 1. Basic Scan
```bash
# Run full security scan
npm run security:scan

# Semgrep only (JavaScript/TypeScript)
npm run security:scan:semgrep

# Bandit only (Python)
npm run security:scan:bandit
```

#### 2. CI/CD Mode (Strict)
```bash
# Fail build on high severity findings
npm run security:scan:strict
```

#### 3. View Results
```bash
# View security summary
cat .claude/idea-to-design/security-scan/security/security-summary-*.md

# View detailed reports
cat .claude/idea-to-design/security-scan/security/semgrep-report-*.json
cat .claude/idea-to-design/security-scan/security/bandit-report-*.json
```

### Severity Classification

| Severity | Action | Timeline | Examples |
|----------|--------|----------|----------|
| 🔴 Critical | Must fix before deployment | Immediate | SQL injection, RCE, hardcoded secrets |
| 🟠 High | Should fix before production | Within sprint | XSS, CSRF, auth bypass |
| 🟡 Medium | Review and address | Next sprint | Weak crypto, info disclosure |
| 🔵 Low | Optional improvements | Backlog | Code quality, best practices |
| ⚪ Info | Informational | None | Notes, suggestions |

### CI/CD Integration

Security scans run automatically in GitHub Actions after lint and tests:

```yaml
- name: Install security scanning tools
  run: |
    pip install semgrep bandit

- name: Run Software Factory security scan
  run: |
    npm run security:scan:strict
  continue-on-error: false
```

**Behavior**:
- Fails build if critical/high findings exist
- Reports uploaded as CI artifacts
- Findings tracked in backlog sync

### Backlog Integration

High-severity findings are automatically extracted by backlog sync:

```bash
node scripts/backlog-sync.js --session-dir .claude/idea-to-design/session-X
```

Creates issues like:
```json
{
  "title": "[Security] SQL Injection vulnerability",
  "priority": "P1",
  "labels": ["security", "critical", "sql-injection"],
  "source": "Security Scan (Semgrep)"
}
```

**Documentation**: See [docs/SECURITY_SCANNING.md](./SECURITY_SCANNING.md) for complete guide

---

## 🧪 Phase 7: Test Automation

**Purpose**: Automated testing across unit, integration, and E2E test suites

**Tool**: `scripts/run-tests.js` + Vitest + Supertest + Playwright

**Inputs**:
- Generated application code from previous phases
- Test specifications and requirements
- Test data and fixtures

**Outputs** (`.claude/idea-to-design/test-reports/`):
- `unit-report.json` - Vitest unit test results
- `integration-report.json` - Vitest integration results
- `e2e-report.json` - Playwright test results
- `test-summary.md` - Unified test summary
- `coverage/` - HTML coverage reports
- `playwright-report/` - Playwright HTML report

**Key Features**:
- **Multi-Layer Testing**: Unit, integration, and E2E test coverage
- **Multi-Browser Support**: Chrome, Firefox, Safari, Edge, Mobile browsers
- **Automated Coverage**: 80% threshold for branches, functions, lines, statements
- **CI/CD Integration**: Automated test execution in deployment pipeline
- **Test Data Management**: Automated test data creation and cleanup

**Test Categories**:
- **Unit Tests**: Individual functions, components, and utilities
- **Integration Tests**: API endpoints, database interactions, service integration
- **E2E Tests**: Complete user workflows, cross-browser compatibility
- **Performance Tests**: Load testing, response time validation
- **Accessibility Tests**: WCAG compliance, screen reader support

**Status**: ✅ Production Ready - Tools installed and configured
**Documentation**: See [docs/TEST_AUTOMATION.md](./TEST_AUTOMATION.md) for complete guide

### Test Automation Process

#### 1. Run All Tests
```bash
# Run complete test suite
npm run test:all

# Strict mode (fail on any error)
npm run test:all:strict
```

#### 2. Run Specific Test Types
```bash
# Unit tests only (Vitest)
npm run test:unit

# Integration tests only (Vitest + Supertest)
npm run test:integration

# E2E tests only (Playwright)
npm run test:e2e

# Watch mode for development
npm run test:watch

# Coverage report
npm run test:coverage
```

#### 3. View Test Reports
```bash
# View unified summary
cat .claude/idea-to-design/test-reports/test-summary.md

# Open coverage report
open .claude/idea-to-design/test-reports/coverage/index.html

# View Playwright report
npx playwright show-report .claude/idea-to-design/test-reports/playwright-report
```

### Test Configuration

#### Vitest Configuration (`vitest.config.ts`)
- **Environment**: Node.js with browser-like globals
- **Coverage**: V8 provider with 80% thresholds
- **Setup**: Global mocks and test utilities
- **Aliases**: Path mapping for clean imports

#### Playwright Configuration (`playwright.config.ts`)
- **Browsers**: Chrome, Firefox, Safari, Edge, Mobile Chrome, Mobile Safari
- **Parallel Execution**: Full parallelization for faster execution
- **Retry Logic**: 2 retries on CI, 0 locally
- **Artifacts**: Screenshots, videos, traces on failure

#### Integration Test Setup (`tests/integration/setup.ts`)
- **Test Server**: Automated Express server for API testing
- **Database**: SQLite test database with automatic cleanup
- **Data Management**: Test data factories and cleanup utilities

### Test Data Management

#### Mock Data Factories
```typescript
// Create test users
const testUser = createMockUser({ email: 'test@example.com' })

// Create test weight entries
const testEntry = createMockWeightEntry({ weight: 70.5 })

// Create test goals
const testGoal = createMockGoal({ targetWeight: 65.0 })
```

#### Database Seeding
```typescript
// Seed test database
await seedTestData({
  users: 5,
  weightEntries: 20,
  goals: 3
})
```

### Test Coverage Requirements

#### Coverage Thresholds
- **Branches**: 80% (conditional logic coverage)
- **Functions**: 80% (function call coverage)
- **Lines**: 80% (line execution coverage)
- **Statements**: 80% (statement execution coverage)

#### Coverage Reports
- **HTML Report**: Interactive coverage visualization
- **JSON Report**: Machine-readable coverage data
- **Text Report**: Console-friendly coverage summary

### Integration Points

- **PRD Generator**: Test requirements from acceptance criteria
- **Architecture Generator**: Test coverage for system components
- **UX Generator**: E2E tests for user workflows
- **Security Scanning**: Test security vulnerabilities
- **Visual QA Factory**: Visual regression testing

---

## 🐳 Phase 8: DevOps Scaffold

**Purpose**: Generate deployment-ready DevOps artifacts for containerization and infrastructure setup

**Tool**: `scripts/devops-scaffold.js` + Docker + Docker Compose

**Inputs**:
- Generated application code from previous phases
- package.json for dependency detection
- Infrastructure requirements from architecture

**Outputs** (`.claude/idea-to-design/devops-scaffold/`):
- `Dockerfile` - Multi-stage production build
- `docker-compose.yml` - Service orchestration with optional services
- `.env.template` - Environment variable documentation
- `deployment-guide.md` - Complete deployment instructions
- `scaffold-metadata.json` - Generation metadata

**Key Features**:
- **Auto-Detection**: Identifies framework (Next.js, Express, React, Python) and dependencies
- **Multi-Stage Builds**: Optimized production containers with security hardening
- **Service Options**: PostgreSQL, Redis, Nginx with health checks
- **Environment Validation**: Validates required environment variables
- **CI/CD Integration**: Automated artifact generation and validation
- **Security Best Practices**: Non-root execution, minimal images, health checks

**Supported Frameworks**:
- **Next.js**: Standalone build with static optimization
- **Express**: Node.js runtime with middleware support
- **React**: Create React App with static serving
- **Python**: Python 3.11+ with requirements.txt

**Container Services** (Optional):
- **PostgreSQL**: Version 15-alpine with persistent volumes and health checks
- **Redis**: Version 7-alpine for caching and session storage
- **Nginx**: Alpine for reverse proxy and SSL termination

**Status**: ✅ Production Ready - Fully automated generation
**Documentation**: See [docs/DEVOPS_SCAFFOLD.md](./DEVOPS_SCAFFOLD.md) for complete guide

### DevOps Scaffold Process

#### 1. Generate DevOps Artifacts
```bash
# Basic scaffold (no services)
npm run devops:scaffold

# With PostgreSQL
npm run devops:scaffold:postgres

# With PostgreSQL + Redis (full stack)
npm run devops:scaffold:full

# Strict mode (fail on missing env vars)
npm run devops:scaffold:strict
```

#### 2. Manual Generation with Options
```bash
# Custom session directory
node scripts/devops-scaffold.js --session-dir .claude/idea-to-design/my-app

# Specify services
node scripts/devops-scaffold.js --services postgres,redis,nginx

# Fail on missing environment variables
node scripts/devops-scaffold.js --fail-on-missing-env
```

#### 3. Environment Setup
```bash
# Navigate to output directory
cd .claude/idea-to-design/devops-scaffold

# Copy environment template
cp .env.template .env

# Edit environment variables
nano .env

# Start development environment
docker-compose up -d
```

#### 4. Verify Deployment
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f app

# Access application
curl http://localhost:3000/health
```

### Auto-Detection Features

The scaffold automatically detects your application configuration:

**Framework Detection**:
- Scans `package.json` for framework dependencies (Next.js, Express, React)
- Detects Python applications via `requirements.txt`
- Determines appropriate build commands and port settings

**Dependency Detection**:
- PostgreSQL: Checks for `pg` or `postgres` packages
- Redis: Checks for `redis` or `ioredis` packages
- Automatically adds required environment variables

**Example Output**:
```
🔍 Detecting application type...

   Framework: next
   Language: javascript
   Port: 3000
   Database: Yes
   Redis: No
```

### Generated Artifacts

**Dockerfile**:
- Multi-stage build (deps → builder → runner)
- Non-root user (nextjs/appuser with UID 1001)
- Framework-specific optimizations
- Labels for metadata and tracking

**docker-compose.yml**:
- Application service with health checks
- Optional PostgreSQL with persistent volumes
- Optional Redis for caching
- Optional Nginx for reverse proxy
- Network isolation with `app-network`
- Volume management for data persistence

**Environment Files**:
- `.env.template`: Comprehensive variable documentation
- Categories: Application, Database, Redis, API Keys, Monitoring
- Secure defaults with placeholder values

**deployment-guide.md**:
- Complete operational procedures
- Service management commands
- Backup and restore strategies
- Troubleshooting common issues

### CI/CD Integration

The DevOps verification job runs automatically in GitHub Actions:

```yaml
devops-verification:
  - Generate scaffold
  - Verify artifacts exist
  - Validate Dockerfile syntax
  - Validate docker-compose.yml syntax
  - Upload artifacts
```

This ensures deployment artifacts are always up-to-date and syntactically valid.

#### Security Features
- **Non-root containers**: Security best practices
- **Network isolation**: Private container networks
- **Secrets management**: Environment-based secrets
- **Security headers**: Nginx security configuration

### Environment Management

#### Development Environment
```bash
# Start development stack
docker-compose up -d

# View logs
docker-compose logs -f

# Execute commands
docker-compose exec app npm run migrate
```

#### Production Environment
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up --scale app=3 -d

# Health checks
docker-compose ps
```

### Integration Points

- **Test Automation**: Container testing and validation
- **Security Scanning**: Container vulnerability scanning
- **Visual QA**: Container-based visual testing
- **Code Generation**: Production-ready containerized applications

---

## 🅿️ Phase 9: Future Feature Parking

**Purpose**: Capture and prioritize long-horizon or exploratory ideas without cluttering the active backlog

**Tool**: `scripts/parking-lot.js`

**Inputs**:
- Manual idea submissions (JSON, Markdown)
- AI Studio outputs
- Backlog sync exploratory items
- Meeting notes and brainstorms

**Outputs** (`.claude/idea-to-design/session-X/parking/`):
- `parking-lot-TIMESTAMP.json` - Structured parking lot entries
- `parking-summary-TIMESTAMP.md` - Prioritization report with ROI analysis

**Key Features**:
- **Structured Capture**: Consistent schema for all ideas
- **ROI Prioritization**: Value, Effort, Confidence scoring
- **Promotion Criteria**: Automatic flagging of ready items (Confidence ≥ 0.6 AND Value ≥ 7)
- **Duplicate Detection**: Similarity-based deduplication
- **Theme Grouping**: Organize ideas by category
- **Impact vs Effort Matrix**: Visual quadrant analysis
- **Backlog Integration**: Automatic routing from backlog sync

**Status**: ✅ Production Ready - Complete parking lot system
**Documentation**: See [docs/FUTURE_FEATURE_PARKING.md](./FUTURE_FEATURE_PARKING.md) for complete guide

### Parking Lot Process

#### 1. Capture Ideas

```bash
# Manual submission from template
cp parking-template.json my-idea.json
# Edit with idea details...
npm run parking:add -- --source my-idea.json

# From Markdown
node scripts/parking-lot.js --session-dir SESSION_DIR --source ideas.md --merge

# From AI Studio output
node scripts/parking-lot.js --session-dir SESSION_DIR --source ai-output.txt --merge
```

#### 2. Review and Prioritize

```bash
# Generate prioritization report
npm run parking:report

# View report
cat .claude/idea-to-design/session-X/parking/parking-summary-*.md
```

#### 3. Promote Ready Ideas

**Automatic Flagging**:
- Ideas with Confidence ≥ 0.6 AND Value ≥ 7 are marked as promotion-ready

**Manual Promotion**:
1. Review prioritization report
2. Validate with stakeholders
3. Move to active backlog using backlog sync
4. Update status to `"promoted"`

### Parking Lot Schema

```json
{
  "title": "Multi-language Support",
  "description": "Add i18n support for multiple languages",
  "drivers": ["Expanding to EU markets", "Customer requests"],
  "estimatedValue": 8,
  "estimatedEffort": 7,
  "confidence": 0.7,
  "dependencies": ["Translation service", "UI updates"],
  "targetPhase": "v2",
  "theme": "user-experience",
  "source": "customer-feedback",
  "status": "parked"
}
```

### Prioritization Model

**ROI Formula**: `ROI = (Value / Effort) * Confidence`

**Promotion Criteria**:
- Confidence ≥ 0.6 (60% certainty)
- Value ≥ 7 (High business value)

**Impact vs Effort Quadrants**:
- **Quick Wins**: High Value, Low Effort → Prioritize first
- **Strategic**: High Value, High Effort → Long-term bets
- **Fill-Ins**: Low Value, Low Effort → Spare capacity
- **Major Projects**: Low Value, High Effort → Reconsider

### Integration with Backlog Sync

Backlog sync automatically routes items to parking lot based on:

**Routing Criteria**:
- Labels: `future`, `exploratory`, `research`, `post-mvp`, `nice-to-have`
- Priority: P3 or lower
- Keywords: "explore", "consider", "investigate", "research"

**Example Flow**:
```
PRD "Nice-to-Have Features"
  → Backlog Sync extracts
  → Labeled as "post-mvp"
  → Automatically routed to Parking Lot
  → Confidence = 0.4 (low, needs validation)
```

### Reporting

**Generated Reports Include**:
- Executive Summary (Top 10 by ROI)
- Ideas by Theme (grouped and sorted)
- Promotion-Ready List (auto-flagged)
- Impact vs Effort Matrix (quadrant analysis)
- Next Steps (actionable recommendations)

**Example Output**:
```
Total Ideas: 15
Promotion Ready: 3

Top Priority (by ROI):
1. Advanced Search (ROI: 1.80) ✅ Ready
2. Dark Mode (ROI: 1.98) ✅ Ready
3. Keyboard Shortcuts (ROI: 2.10) ✅ Ready
```

### Best Practices

**Capturing**:
- Be honest about confidence (low confidence is OK!)
- Include business drivers and user needs
- Add dependencies early
- Use consistent themes

**Estimating**:
- Value (1-10): Business impact
- Effort (1-10): Implementation complexity
- Confidence (0.0-1.0): Certainty in estimates

**Reviewing**:
- Weekly: Quick scan of new ideas
- Monthly: Full prioritization report
- Quarterly: Deep dive with stakeholders, promote ready items

### Integration Points

- **Backlog Sync**: Automatic routing of exploratory items
- **Respect-Spec**: Validates parking lot structure and reports
- **PRD/Architecture/UX**: Sources for future features
- **AI Studio**: Ingest AI-generated ideas

---

## 🎨 Phase 10: Design Generation

**Purpose**: Create visual mockups and prototypes

**Tool**: `scripts/generate-mockups.js`

**Inputs**:
- Requirements from Phase 1
- PRD Bundle from Phase 2
- UX specifications from Phase 4 (when available)

**Outputs** (`.claude/idea-to-design/session-X/mockups/iteration-X/`):
- `option-a/` - Design variation A with HTML screenshots
- `option-b/` - Design variation B with HTML screenshots  
- `option-c/` - Design variation C with HTML screenshots

**Usage**:
```bash
node scripts/generate-mockups.js \
  --requirements session-X/requirements/iteration-X.json \
  --output-dir session-X/mockups/iteration-X
```

**Quality Checks**:
- [ ] 3 design variations generated
- [ ] All required screens present (splash, dashboard, settings, etc.)
- [ ] Responsive design for desktop, tablet, mobile
- [ ] Screenshots generated for all viewports

---

## 📊 Phase 8: Visual QA

**Purpose**: Automated quality assurance of generated designs

**Tool**: `scripts/visual-qa-runner.js` + Playwright MCP

**Inputs**:
- Mockup variations from Phase 5

**Outputs** (`.claude/idea-to-design/session-X/scores/`):
- `iteration-X-option-a.json` - Detailed QA scores for option A
- `iteration-X-option-b.json` - Detailed QA scores for option B
- `iteration-X-option-c.json` - Detailed QA scores for option C
- `iteration-X-comparison.md` - Comparative analysis report

**Usage**:
```bash
node scripts/visual-qa-runner.js \
  --mockup-dir session-X/mockups/iteration-X/option-a \
  --output-file session-X/scores/iteration-X-option-a.json
```

**Quality Metrics**:
- Overall Score (target: ≥90/100)
- Brand Compliance (25 points)
- Responsive Design (20 points)
- Accessibility (25 points)
- Performance (15 points)
- Visual Polish (15 points)

---

## 🔄 Phase 9: Feedback & Refinement

**Purpose**: Client validation and iterative improvement

**Tool**: Interactive feedback collection + refinement agents

**Process**:
1. Present top 2 mockups to client
2. Collect structured feedback
3. If approved → proceed to code generation
4. If refinement needed → update requirements and iterate

**Feedback Questions**:
- Which design feels more "you"?
- What do you love about your choice?
- What would you change?
- Energy level: too low / just right / too high?
- Ready to proceed or want another iteration?

**Refinement Process**:
- Update requirements based on feedback
- Generate new iteration
- Repeat until client approval

---

## 💻 Phase 10: Code Generation

**Purpose**: Convert approved design to production-ready code

**Tool**: Code generation agents (Placeholder)

**Inputs**:
- Approved mockup from Phase 7
- PRD Bundle from Phase 2
- Architecture from Phase 3
- UX specifications from Phase 4

**Outputs**:
- `software-factory/generated-apps/app-name/` - Complete Next.js application
- Production-ready code with all features implemented
- Documentation and deployment instructions

**Status**: 🚧 In Development

---

## 🔍 Respect-Spec Framework

**Purpose**: Validate that generated artifacts respect original PRD specifications

**Tool**: `scripts/respect_spec.js`

**Usage**:
```bash
node scripts/respect_spec.js \
  --prd-dir session-X/prd \
  --architecture-dir session-X/architecture \
  --ux-dir session-X/ux \
  --output-file session-X/respect-spec-report.json
```

**Validation Checks**:
- Architecture compliance with PRD requirements
- UX flows match persona scenarios
- Acceptance criteria coverage
- Non-functional requirements adherence

**Status**: ✅ Skeleton ready, waiting for Claude artifacts

---

## 🚀 Quick Start Guide

### Prerequisites
```bash
# Install Node.js 18+
node --version

# Install Docker Desktop (for DevOps phase)
docker --version
docker-compose --version

# Verify Git is available
git --version
```

### 1. Start a New Session
```bash
./scripts/idea-to-design.sh "I want an app to track my daily water intake"
```

### 2. Generate PRD Bundle
```bash
node scripts/generate-prd.js \
  --requirements .claude/idea-to-design/session-YYYYMMDD-HHMMSS/requirements/iteration-0.json \
  --output-dir .claude/idea-to-design/session-YYYYMMDD-HHMMSS/prd
```

### 3. Generate Architecture (via Claude Code)
Architecture docs are generated by Claude Code analyzing PRD requirements.

### 4. Generate UX Flows (via Claude Code)
UX flows are generated by Claude Code based on PRD and architecture.

### 5. Validate Compliance
```bash
node scripts/respect_spec.js \
  --prd-dir .claude/idea-to-design/session-YYYYMMDD-HHMMSS/prd \
  --architecture-dir .claude/idea-to-design/session-YYYYMMDD-HHMMSS/architecture \
  --ux-dir .claude/idea-to-design/session-YYYYMMDD-HHMMSS/ux \
  --output-file .claude/idea-to-design/session-YYYYMMDD-HHMMSS/respect-spec-report.json
```

### 6. Sync Backlog
```bash
# Preview backlog items
node scripts/backlog-sync.js \
  --session-dir .claude/idea-to-design/session-YYYYMMDD-HHMMSS \
  --dry-run

# Sync to GitHub Issues
node scripts/backlog-sync.js \
  --session-dir .claude/idea-to-design/session-YYYYMMDD-HHMMSS
```

### 7. Run Security Scan
```bash
# Scan for security vulnerabilities
npm run security:scan

# View results
cat .claude/idea-to-design/security-scan/security/security-summary-*.md
```

### 8. Run Tests
```bash
# Run all tests
npm run test:all

# View results
cat .claude/idea-to-design/test-reports/test-summary.md
```

### 9. Generate DevOps Scaffold
```bash
# Generate Docker configuration
npm run devops:scaffold

# Start containerized environment
npm run devops:up

# Check service status
npm run devops:ps
```

### 10. Run Visual QA (if mockups generated)
```bash
node scripts/visual-qa-runner.js \
  --mockup-dir .claude/idea-to-design/session-YYYYMMDD-HHMMSS/mockups/iteration-0/option-a \
  --output-file .claude/idea-to-design/session-YYYYMMDD-HHMMSS/scores/iteration-0-option-a.json
```

---

## 📁 Directory Structure

```
.claude/idea-to-design/
├── session-YYYYMMDD-HHMMSS/
│   ├── requirements/
│   │   └── iteration-0.json
│   ├── prd/                    # Generated by scripts/generate-prd.js
│   │   ├── 01-personas.md
│   │   ├── 02-problem-solution.md
│   │   └── 03-acceptance-criteria.md
│   ├── architecture/           # Generated by scripts/generate-architecture.js
│   │   ├── architecture-tech-stack.md
│   │   ├── architecture-services.md
│   │   ├── architecture-data-model.md
│   │   ├── architecture-api.md
│   │   └── architecture-deployment.md
│   ├── ux/                     # Generated by scripts/generate-ux-flows.js
│   │   ├── ux-screen-map.md
│   │   ├── ux-states.md
│   │   ├── ux-interactions.md
│   │   ├── user-flows.md
│   │   ├── wireframes.md
│   │   ├── interaction-specs.md
│   │   └── accessibility-guidelines.md
│   ├── backlog/                # Generated by scripts/backlog-sync.js
│   │   ├── backlog-TIMESTAMP.json
│   │   └── audit-TIMESTAMP.json
│   ├── security/               # Generated by scripts/security-scan.js
│   │   ├── semgrep-report-TIMESTAMP.json
│   │   ├── bandit-report-TIMESTAMP.json
│   │   └── security-summary-TIMESTAMP.md
│   ├── test-reports/           # Generated by scripts/run-tests.js
│   │   ├── unit-report.json
│   │   ├── integration-report.json
│   │   ├── e2e-report.json
│   │   ├── test-summary.md
│   │   ├── coverage/
│   │   └── playwright-report/
│   ├── mockups/
│   │   └── iteration-0/
│   │       ├── option-a/
│   │       ├── option-b/
│   │       └── option-c/
│   ├── scores/
│   │   ├── iteration-0-option-a.json
│   │   ├── iteration-0-option-b.json
│   │   ├── iteration-0-option-c.json
│   │   └── iteration-0-comparison.md
│   ├── feedback/
│   │   └── iteration-0.json
│   └── respect-spec-report.json
```

---

## 🔧 Troubleshooting

### PRD Generation Issues
- **Missing requirements file**: Ensure discovery phase completed successfully
- **Invalid JSON**: Check requirements file format and syntax
- **Empty outputs**: Verify all required fields present in requirements

### Architecture/UX Generation Issues
- **Missing documents**: Ensure all generator scripts ran successfully
- **Empty files**: Check script output for errors
- **Invalid Mermaid diagrams**: Verify syntax in generated markdown

### Backlog Sync Issues
- **GitHub CLI not found**: Install with `brew install gh`
- **Authentication failed**: Run `gh auth login`
- **Not a GitHub repo**: Ensure working directory is a git repository with GitHub remote
- **No items extracted**: Check that documentation has "Future" sections or nice-to-have features
- **Duplicate issues created**: Use `--dry-run` first to preview, deduplication only works within single run

### Visual QA Issues
- **Playwright errors**: Ensure Chrome browser installed and accessible
- **Low scores**: Review design against acceptance criteria
- **Missing screenshots**: Check HTML file generation in mockup phase

### Respect-Spec Validation Issues
- **Low compliance**: Review missing files or validation errors in report
- **Overall compliance 0%**: Bug in score calculation (should be fixed in v1.1)
- **Missing artifacts**: Ensure all phases completed before validation

### Security Scanning Issues
- **Semgrep not found**: Install with `brew install semgrep` or `pip install semgrep`
- **Bandit not found**: Install with `pip install bandit`
- **No findings**: Ensure source directories contain code files
- **Too many false positives**: Configure exclusions in `.semgrep.yml` or `.bandit`
- **Scan timeout**: Increase timeout or limit source directories
- **CI build fails**: Review security summary and fix critical/high findings

### Test Automation Issues
- **Vitest not running**: Ensure dependencies installed with `npm install`
- **Playwright browsers missing**: Run `npx playwright install`
- **Tests timing out**: Increase timeout in test config
- **Coverage too low**: Write more unit tests for critical paths
- **E2E tests flaky**: Add explicit waits and use data-testid attributes
- **CI tests failing**: Check environment variables and dependencies

---

## 📈 Success Metrics

### Quality Targets
- **PRD Completeness**: 100% of required sections generated
- **Visual QA Score**: ≥90/100 for approved designs
- **Client Satisfaction**: ≥9/10 for final approval
- **Spec Compliance**: ≥80% for all generated artifacts

### Performance Targets
- **PRD Generation**: <30 seconds
- **Mockup Generation**: <2 minutes
- **Visual QA**: <5 minutes per variation
- **Total Session Time**: <2 hours for complete workflow

---

## 🔄 Continuous Improvement

### Regular Reviews
- Weekly analysis of QA scores and client feedback
- Monthly review of workflow efficiency
- Quarterly updates to templates and generators

### Feedback Integration
- Client feedback incorporated into template improvements
- QA score patterns used to enhance design generation
- Respect-spec validation results inform process refinements

---

## 🌐 Global Infrastructure Setup

### Domain & Analytics Configuration

**Purpose**: Set up foundational infrastructure for multiple DBA (Doing Business As) applications

**Prerequisites**: DBA names must be finalized through AI Studio research

**Global Backlog**: `.claude/idea-to-design/global/backlog/manual-queue.json`

#### Domain Routing Setup

**Task**: Configure domain routing for partner DBAs
- **URL Pattern**: `clevelsalesguy.com/{dba-category}/*`
- **DBA Categories**: Consumer-facing, Bespoke/White-label, Enterprise
- **Implementation**: Vercel path-based routing or separate projects
- **Status**: Pending DBA name finalization

**Dependencies**:
- AI Studio DBA naming research completion
- Domain availability confirmation
- Trademark clearance verification

#### Analytics Properties Setup

**Task**: Provision analytics properties per DBA
- **Platform**: GA4 or Segment
- **Properties**: Separate property per DBA category
- **Configuration**: Environment variables for per-app tracking
- **Documentation**: Tracking setup guide per DBA

**Dependencies**:
- DBA names and categories finalized
- Domain routing configuration complete
- Analytics strategy defined per DBA

#### AI Studio DBA Research

**Prompt Library**: `docs/AI_STUDIO_PROMPTS_DBA.md`

**Research Categories**:
1. **Consumer-Facing Brand**: Playful, accessible naming
2. **Bespoke/White-Label Brand**: Professional, flexible naming  
3. **Enterprise Sales Suite**: Sophisticated, authoritative naming

**Export Location**: `.claude/idea-to-design/dba-research/ai-studio/`

**Integration Points**:
- Global backlog updates with selected DBA names
- Domain mapping generation
- Analytics property configuration
- Deployment pipeline updates

#### Workflow Integration

**Before DBA Development**:
1. Run AI Studio DBA naming research
2. Validate domain availability and trademarks
3. Update global backlog with selected names
4. Configure domain routing and analytics
5. Proceed with DBA-specific application development

**Documentation References**:
- [AI Studio DBA Prompts](./AI_STUDIO_PROMPTS_DBA.md) - Naming research templates
- [Global Backlog](../.claude/idea-to-design/global/backlog/README.md) - Infrastructure tasks
- [Deployment Notes](./DEPLOYMENT_NOTES.md) - Domain and analytics configuration

---

**Last Updated**: January 2025
**Next Review**: February 2025

---

## 🔐 Design Integration Gate

**Purpose**: Ensure design-to-code traceability and prevent QA/deployment mismatches

**Problem**: QA runs against wrong UI version when design spec exists but code is not yet implemented

### Overview

The Design Integration Gate enforces end-to-end traceability from Figma design → specification → code → baselines → QA. It prevents QA from running until design artifacts are valid and implementation is complete.

### Design Version Manifest

**Location**: `<app-directory>/design_version.json`

**Example** (Weight Tracker):
```json
{
  "design_version": "v2",
  "figma_file": "https://www.figma.com/design/<file-id>/...",
  "figma_file_id": "<file-id>",
  "spec_path": "docs/design/generated/weight-tracker-spec-v1.json",
  "spec_hash": "<SHA256 of spec file>",
  "baseline_path": "screenshots/baseline/v2",
  "baseline_hash": "<SHA256 of concatenated PNG MD5s>",
  "status": "implemented | pending_implementation",
  "last_updated": "2025-10-28"
}
```

### Required Steps Before QA/Deployment

#### Step 1: Design Specification

1. **Figma Design Finalized**
   - Design file URL documented in manifest
   - Dev Mode accessible for measurements/tokens
   - All screens approved by stakeholders

2. **Specification Generated**
   - JSON spec exists at `spec_path`
   - Contains: design system, components, screens, accessibility requirements
   - SHA256 hash computed and recorded in manifest

**Compute Spec Hash**:
```bash
node -e "const crypto=require('crypto');const fs=require('fs');console.log(crypto.createHash('sha256').update(fs.readFileSync('docs/design/generated/<spec>.json')).digest('hex'))"
```

#### Step 2: Code Implementation

1. **Implement UI Based on Spec**
   - React components implement design system
   - Colors, typography, spacing match spec
   - Component variants implement spec requirements
   - Accessibility requirements met (ARIA, contrast, keyboard nav)

2. **Code Review with Design Validation**
   - Tech lead reviews implementation against spec
   - Design tokens verified (colors, spacing, typography)
   - Component mapping documented
   - No placeholder TODOs or stub implementations

3. **Update Manifest Status**
   ```json
   "status": "implemented"
   ```

#### Step 3: Baseline Screenshot Capture

1. **Prerequisites**
   - UI implementation complete and reviewed
   - Development server running (`npm run dev`)
   - Application loads without errors

2. **Capture Baselines**
   ```bash
   cd <app-directory>
   npm run test:visual
   ```

3. **Verify Screenshots**
   - Manually inspect `screenshots/test-results/`
   - Check all screens loaded correctly
   - Verify no loading spinners, error states
   - Confirm UI matches Figma design

4. **Promote to Baseline**
   ```bash
   mv screenshots/test-results/*.png screenshots/baseline/v2/
   ```

5. **Compute Baseline Hash**
   ```bash
   node scripts/check-design-version.js --compute-baseline
   ```

   Copy output hash to manifest `baseline_hash` field.

#### Step 4: Validation Gate

**Before every QA run or deployment**, validate design version:

```bash
node scripts/check-design-version.js
```

**Checks**:
- ✅ Manifest exists and is valid JSON
- ✅ All required fields present (no `<TBD>` placeholders)
- ✅ Spec file exists at `spec_path`
- ✅ Spec hash matches manifest (detects spec changes)
- ✅ Baseline directory exists at `baseline_path`
- ✅ Baseline contains PNG files
- ✅ Baseline hash matches manifest (detects baseline changes)
- ✅ Status is `implemented` (not `pending_implementation`)

**If validation fails**: QA/deployment BLOCKED until issues resolved.

### Integration Points

#### Playwright Visual Tests

**Location**: `tests/visual/<app>-qa.spec.js`

**Hook**: Design version check runs automatically before tests

```javascript
function checkDesignVersion() {
    console.log('🔍 Checking design version...');
    try {
        execSync(`node scripts/check-design-version.js`, { stdio: 'inherit' });
        console.log('✅ Design version validation passed\n');
    } catch (error) {
        console.error('\n❌ Design version validation FAILED');
        console.error('⛔ QA cannot proceed until design artifacts are valid');
        process.exit(1);
    }
}
```

**Result**: Tests abort with clear error message if validation fails.

#### CI/CD Pipeline

**GitHub Actions Workflow**: `.github/workflows/design-integration.yml`

```yaml
name: Design Integration Check
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Validate Design Version
        run: node scripts/check-design-version.js
```

**Status**: Created but not yet required for merge (TODO).

### Common Scenarios

#### Scenario 1: Design Spec Changes

**Trigger**: Designer updates Figma, new spec generated

**Process**:
1. New spec file committed to repo
2. Compute new spec hash
3. Update manifest with new hash
4. Review if code changes needed
5. If code changes: implement, review, re-capture baselines
6. If no code changes: just update hash
7. Run validation script (should pass)

#### Scenario 2: UI Implementation in Progress

**Status**: Manifest has `"status": "pending_implementation"`

**Result**: `check-design-version.js` will FAIL, blocking QA

**Action**: Complete implementation before running QA

#### Scenario 3: Intentional UI Change (Bug Fix)

**Trigger**: Visual bug fixed, UI appearance changes

**Process**:
1. Implement fix in code
2. Code review and merge
3. Run `npm run test:visual` to generate new screenshots
4. Manually verify fix is correct
5. Promote to baseline (`mv screenshots/test-results/*.png screenshots/baseline/v2/`)
6. Recompute baseline hash (`node scripts/check-design-version.js --compute-baseline`)
7. Update manifest with new hash
8. Commit updated manifest and baseline screenshots
9. Run validation (should pass)

#### Scenario 4: Unintended Visual Regression

**Trigger**: Code change causes unexpected UI differences

**Detection**: Future visual diff tool will detect differences

**Process**:
1. Visual diff tool highlights differences in screenshots
2. Review diff images to understand changes
3. If unintended: fix code, re-test
4. If acceptable: update baselines (follow Scenario 3)
5. Never update baselines without understanding why they changed

### Troubleshooting

#### Error: "Spec hash mismatch"

**Cause**: Design spec file changed since manifest was last updated

**Fix**:
1. Review spec changes (git diff)
2. Determine if code needs updating
3. Recompute hash: `node -e "...compute SHA256..."`
4. Update manifest `spec_hash` field
5. If code changed: re-capture baselines

#### Error: "No baseline screenshots found"

**Cause**: Baseline directory empty or missing

**Fix**:
1. Ensure implementation is complete
2. Run `npm run test:visual`
3. Verify screenshots manually
4. Move to baseline: `mv screenshots/test-results/*.png screenshots/baseline/v2/`
5. Compute hash and update manifest

#### Error: "Implementation status: pending_implementation"

**Cause**: UI not yet implemented based on spec

**Fix**:
1. Complete UI implementation
2. Code review with design validation
3. Update manifest: `"status": "implemented"`
4. Capture baselines (see Step 3 above)

#### Error: "Baseline hash mismatch"

**Cause**: Baseline screenshots changed since manifest was last updated

**Fix**:
1. Review what changed (`git diff screenshots/baseline/v2/`)
2. If intentional: recompute hash and update manifest
3. If unintentional: restore baselines from git history
4. Never update manifest hash without understanding why

### Future Enhancements

**Planned**:
- [ ] Visual diff comparison (pixelmatch or similar)
- [ ] Automated diff image generation
- [ ] Figma API integration for auto-spec updates
- [ ] Design token export from Figma
- [ ] Component-level mapping documentation
- [ ] Baseline approval workflow (UI for reviewing diffs)

**Status**: Core validation implemented, visual diff pending.

---

## LLM Provider Strategy

- Claude remains the default provider for architecture, UX, and documentation.
- When Claude sessions are limited, fall back to:
  - OpenAI GPT-4.1 for architecture/UX text generation.
  - Google Gemini 1.5 Pro for research or summarization tasks.
  - Other providers (Groq, Together) can be added through the unified LLM client (`scripts/llm-clients.js`).
- Configure API keys via `config/llm/.env.llm.example` and set `LLM_DEFAULT_PROVIDER` as needed.
- Scripts accept `--provider` to override (e.g., `node scripts/generate-architecture.js --provider openai ...`).
- The unified client automatically falls back when a provider hits rate or session limits.
