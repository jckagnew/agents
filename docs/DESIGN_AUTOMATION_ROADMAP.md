# Design Automation Roadmap

Goal: fully automate idea → mockup → code → deployment using our agentic patterns, with humans (you or the client) only approving or tweaking curated options.

## Phase 0 – Foundations (In Progress)
- Inventory existing agent templates (routing, planning, reflection, tool use) and adapt for the design workflow.
- Define orchestrator state machine and Supabase tables (`projects`, `design_versions`, `feedback`).
- Prepare Figma workspace: design system file, best-practices preset, install Dev Mode MCP + ShadCN MCP configs.
- Draft planning + Figma Make prompt templates.

### Orchestrator State Machine

**States**:
1. `INTAKE` - Receive project requirements from client intake form
2. `PLANNING` - Generate design specifications and component breakdown
3. `DESIGN_GENERATION` - Create Figma mockups using Figma Make API
4. `DESIGN_CRITIQUE` - Evaluate design quality against rubrics
5. `DESIGN_REFINEMENT` - Apply critic feedback and iterate (max 3 iterations)
6. `CLIENT_REVIEW` - Present curated options to client for approval
7. `FEEDBACK_PROCESSING` - Parse client feedback and determine next action
8. `APPROVED` - Design approved, ready for implementation
9. `IMPLEMENTATION` - Generate code from Figma using Dev Mode MCP
10. `QA` - Run automated tests (lint, Playwright, analytics checks)
11. `DEPLOYMENT` - Deploy to Vercel staging environment
12. `ERROR` - Handle exceptions and determine recovery strategy
13. `COMPLETE` - Project delivered successfully

**State Transitions**:
```
INTAKE → PLANNING
  Trigger: Intake form submitted
  Data: project requirements, branding preferences, target audience

PLANNING → DESIGN_GENERATION
  Trigger: Planning agent completes design specification
  Data: component list, layout structure, color palette, typography

DESIGN_GENERATION → DESIGN_CRITIQUE
  Trigger: Figma mockup created
  Data: Figma file URL, design system compliance status

DESIGN_CRITIQUE → DESIGN_REFINEMENT (if quality < threshold)
  Trigger: Critic score < 8/10
  Data: specific improvement suggestions, quality rubric scores
  Condition: iteration_count < 3

DESIGN_CRITIQUE → CLIENT_REVIEW (if quality >= threshold OR max iterations reached)
  Trigger: Critic score >= 8/10 OR iteration_count >= 3
  Data: final Figma URLs, design rationale, quality scores

DESIGN_REFINEMENT → DESIGN_GENERATION
  Trigger: Refinement agent updates design specification
  Data: updated component specs, modified layout

CLIENT_REVIEW → FEEDBACK_PROCESSING
  Trigger: Client submits approval/rejection/changes
  Data: approval status, change requests, feedback text

FEEDBACK_PROCESSING → APPROVED (if approved)
  Trigger: Client approves design
  Data: final approved Figma URL

FEEDBACK_PROCESSING → PLANNING (if major changes)
  Trigger: Client requests significant redesign
  Data: new requirements, updated preferences

FEEDBACK_PROCESSING → DESIGN_REFINEMENT (if minor changes)
  Trigger: Client requests tweaks
  Data: specific change requests

APPROVED → IMPLEMENTATION
  Trigger: Design approval confirmed
  Data: Figma file URL, component inventory

IMPLEMENTATION → QA
  Trigger: Code generation complete
  Data: Next.js project files, component implementations

QA → DEPLOYMENT (if tests pass)
  Trigger: All QA checks passing
  Data: build artifacts, test results

QA → IMPLEMENTATION (if tests fail)
  Trigger: Lint errors, failing tests, or analytics issues
  Data: error logs, specific failures
  Condition: retry_count < 2

DEPLOYMENT → COMPLETE
  Trigger: Vercel deployment successful
  Data: production URL, deployment logs

ANY_STATE → ERROR (on exception)
  Trigger: Unhandled error, timeout, API failure
  Data: error type, stack trace, recovery options

ERROR → PLANNING | DESIGN_GENERATION | IMPLEMENTATION (recovery)
  Trigger: Error classified as recoverable
  Data: recovery strategy (retry, fallback, simplified version)

ERROR → CLIENT_REVIEW (if unrecoverable)
  Trigger: Error classified as requiring human intervention
  Data: error summary, manual override options
```

**State Machine Properties**:
- **Max iterations per design cycle**: 3 (prevents infinite refinement loops)
- **Quality threshold for auto-approval**: 8/10 on critic rubric
- **Timeout per state**: 5 minutes (prevents stuck states)
- **Error recovery attempts**: 2 retries with exponential backoff
- **Persistence**: State saved to Supabase after each transition
- **Rollback capability**: Can revert to any previous approved state

### Supabase Schema

**Table: `projects`**
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  client_id UUID REFERENCES clients(id),
  project_name TEXT NOT NULL,
  current_state TEXT NOT NULL, -- ENUM: matches state machine states
  intake_data JSONB, -- Client requirements, preferences
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);
```

**Table: `design_versions`**
```sql
CREATE TABLE design_versions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id),
  version_number INTEGER NOT NULL,
  figma_file_url TEXT,
  design_spec JSONB, -- Planning agent output
  critic_scores JSONB, -- Quality rubric scores
  iteration_count INTEGER DEFAULT 0,
  status TEXT, -- draft, under_review, approved, rejected
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Table: `feedback`**
```sql
CREATE TABLE feedback (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  design_version_id UUID REFERENCES design_versions(id),
  feedback_type TEXT, -- client_approval, critic_suggestion, qa_error
  feedback_data JSONB, -- Structured feedback content
  processed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Table: `state_transitions`** (audit log)
```sql
CREATE TABLE state_transitions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id),
  from_state TEXT,
  to_state TEXT,
  trigger_event TEXT,
  transition_data JSONB,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Prompt Templates Required

#### 1. **Planning Agent Prompt** (`prompts/design-planning.txt`)
**Purpose**: Transform client requirements into detailed design specification
**Input**: Intake form data (project name, description, target audience, branding preferences)
**Output**: Structured design specification (JSON)

```
You are a design planning specialist. Given client requirements, create a comprehensive design specification for a web application.

Input:
- Project Name: {project_name}
- Description: {description}
- Target Audience: {target_audience}
- Brand Colors: {brand_colors}
- Design Style: {design_style} (modern, minimal, playful, corporate)

Output a JSON design specification with:
1. Component Inventory: List all UI components needed (header, nav, hero, forms, etc.)
2. Layout Structure: Page hierarchy and information architecture
3. Color Palette: Primary, secondary, accent colors with hex codes
4. Typography: Font families, sizes, weights for headings/body/UI
5. Spacing System: Grid system, padding/margin scale
6. Component Specifications: For each component, define:
   - Purpose and user interaction
   - Visual hierarchy requirements
   - Accessibility considerations
   - Responsive behavior (mobile, tablet, desktop)

Design Principles:
- Follow modern UX best practices
- Ensure WCAG 2.1 AA accessibility compliance
- Optimize for mobile-first responsive design
- Maintain visual consistency with brand guidelines
```

#### 2. **Figma Make Prompt** (`prompts/figma-generation.txt`)
**Purpose**: Generate Figma mockup from design specification
**Input**: Design specification JSON from planning agent
**Output**: Figma file URL with implemented design

```
You are a Figma design automation specialist using the Figma Make API. Create a complete mockup based on this design specification.

Design Specification:
{design_spec_json}

Instructions:
1. Create a new Figma file named "{project_name} - Design v{version}"
2. Set up artboards for: Desktop (1440px), Tablet (768px), Mobile (375px)
3. Implement the design system:
   - Create color styles for all palette colors
   - Set up text styles for typography hierarchy
   - Define component variants for buttons, inputs, cards
4. Build out each page/screen according to component inventory
5. Apply auto-layout for responsive behavior
6. Ensure proper layer naming and organization
7. Add design notes and annotations for developers

Figma Best Practices:
- Use Auto Layout for all containers
- Create reusable components in separate page
- Apply consistent spacing using 8px grid
- Use proper layer hierarchy and naming conventions
- Include interaction prototypes for key user flows

Return:
- Figma file URL
- Component inventory (list of all created components)
- Design system compliance checklist
```

#### 3. **Design Critic Rubric** (`prompts/design-critic.txt`)
**Purpose**: Evaluate design quality and provide specific improvement suggestions
**Input**: Figma file URL, design specification
**Output**: Quality scores (0-10) and actionable feedback

```
You are a design quality critic. Evaluate this Figma mockup against professional design standards.

Figma File: {figma_url}
Design Specification: {design_spec_json}

Evaluation Rubric (score each 0-10):

1. **Visual Hierarchy** (0-10)
   - Clear focal points and content prioritization
   - Effective use of size, color, spacing for importance
   - Easy scanning and information discovery

2. **Consistency** (0-10)
   - Uniform spacing, typography, color usage
   - Reusable component patterns
   - Design system adherence

3. **Accessibility** (0-10)
   - Color contrast ratios (WCAG 2.1 AA minimum)
   - Text readability (font sizes, line heights)
   - Clear interactive elements and states

4. **Responsive Design** (0-10)
   - Mobile-first approach
   - Proper breakpoint handling
   - Content adaptation across screen sizes

5. **User Experience** (0-10)
   - Intuitive navigation and user flows
   - Clear calls-to-action
   - Error prevention and helpful feedback

6. **Brand Alignment** (0-10)
   - Matches specified brand colors and style
   - Appropriate tone and personality
   - Target audience resonance

7. **Technical Feasibility** (0-10)
   - Implementable with standard web technologies
   - Performance considerations (image sizes, animations)
   - Developer-friendly structure

8. **Polish & Professionalism** (0-10)
   - Attention to detail (alignment, spacing)
   - High-quality assets and imagery
   - Production-ready quality

Output Format:
{
  "overall_score": <average of all scores>,
  "rubric_scores": {
    "visual_hierarchy": <score>,
    "consistency": <score>,
    "accessibility": <score>,
    "responsive_design": <score>,
    "user_experience": <score>,
    "brand_alignment": <score>,
    "technical_feasibility": <score>,
    "polish": <score>
  },
  "strengths": ["<specific positive aspects>"],
  "improvement_suggestions": [
    {
      "category": "<rubric category>",
      "issue": "<specific problem>",
      "suggestion": "<actionable fix>",
      "priority": "high|medium|low"
    }
  ],
  "approve_for_client": <true if overall_score >= 8, false otherwise>
}
```

#### 4. **Design Refinement Prompt** (`prompts/design-refinement.txt`)
**Purpose**: Apply critic feedback to improve design
**Input**: Original design spec, critic feedback, Figma file URL
**Output**: Updated design specification

```
You are a design refinement specialist. Update the design specification based on critic feedback.

Original Design Spec: {original_design_spec}
Critic Feedback: {critic_feedback}
Current Figma URL: {figma_url}

Instructions:
1. Review each improvement suggestion from the critic
2. For HIGH priority suggestions: Apply immediately
3. For MEDIUM priority suggestions: Apply if feasible without major restructuring
4. For LOW priority suggestions: Apply only if they align with project goals

Update the design specification to address:
- Layout adjustments for improved hierarchy
- Color/typography refinements for accessibility
- Component modifications for better UX
- Responsive behavior improvements

Output:
- Updated design specification JSON (same structure as planning agent)
- Change summary: What was modified and why
- Expected impact on quality scores

Constraints:
- Maintain brand alignment and core design direction
- Don't introduce breaking changes to approved elements
- Keep changes focused on critic-identified issues
```

#### 5. **Feedback Processing Prompt** (`prompts/feedback-processing.txt`)
**Purpose**: Parse client feedback and determine appropriate state transition
**Input**: Client feedback text, current design version
**Output**: Classification and structured action plan

```
You are a client feedback interpreter. Analyze this feedback and determine the appropriate next action.

Client Feedback: {client_feedback_text}
Current Design Version: {design_version_url}

Classification Options:
1. **APPROVED** - Client is satisfied, proceed to implementation
2. **MINOR_CHANGES** - Small tweaks (color adjustments, copy changes, spacing) → DESIGN_REFINEMENT state
3. **MAJOR_CHANGES** - Significant redesign (layout restructure, different direction) → PLANNING state
4. **CLARIFICATION_NEEDED** - Ambiguous feedback, need more information → CLIENT_REVIEW with questions

Extract from feedback:
- Approval status (approved / needs changes / unclear)
- Specific change requests (as structured list)
- Emotional tone (satisfied / neutral / frustrated)
- Priority indicators (must-have / nice-to-have)

Output Format:
{
  "classification": "APPROVED|MINOR_CHANGES|MAJOR_CHANGES|CLARIFICATION_NEEDED",
  "next_state": "APPROVED|DESIGN_REFINEMENT|PLANNING|CLIENT_REVIEW",
  "change_requests": [
    {
      "category": "color|layout|typography|content|interaction",
      "description": "<specific change>",
      "priority": "high|medium|low"
    }
  ],
  "clarification_questions": ["<question to ask client>"],
  "estimated_effort": "low|medium|high",
  "reasoning": "<explanation of classification>"
}
```

### Missing Assets Checklist

Based on the prompt templates above, we need:

**Figma Workspace Setup**:
- [ ] Create Figma organization/team for automated designs
- [ ] Install Figma Make API access (requires Figma Enterprise or compatible plugin)
- [ ] Set up base design system file with ShadCN-compatible components
- [ ] Configure Figma Dev Mode MCP for code generation
- [ ] Create template file with artboard presets (desktop/tablet/mobile)

**MCP Integrations**:
- [ ] ShadCN MCP: For React component code generation from Figma
- [ ] Figma Dev Mode MCP: For design-to-code conversions
- [ ] Supabase MCP: For state persistence and project tracking
- [ ] Vercel MCP: For automated deployments (Phase 3)

**Environment Variables**:
```bash
# Figma API
FIGMA_ACCESS_TOKEN=<personal_access_token>
FIGMA_TEAM_ID=<team_id>

# Supabase
SUPABASE_URL=<project_url>
SUPABASE_SERVICE_KEY=<service_role_key>

# AI Models
OPENAI_API_KEY=<key>  # For planning, critic, refinement agents
ANTHROPIC_API_KEY=<key>  # Alternative/parallel processing

# Vercel (Phase 3)
VERCEL_TOKEN=<deployment_token>
VERCEL_TEAM_ID=<team_id>
```

**Prompt Template Files** (to be created):
- [ ] `prompts/design-planning.txt` - Planning agent system prompt
- [ ] `prompts/figma-generation.txt` - Figma Make instructions
- [ ] `prompts/design-critic.txt` - Quality evaluation rubric
- [ ] `prompts/design-refinement.txt` - Improvement application
- [ ] `prompts/feedback-processing.txt` - Client feedback parsing

**Agentic Patterns to Leverage** (from AGENTIC_PATTERNS_ANALYSIS.md):
- ✅ **Pattern 4: Reflection** - Critic agent for design quality assessment
- ✅ **Pattern 6: Planning** - Design specification generation
- ✅ **Pattern 5: Tool Use** - Figma API, Supabase, Vercel integrations
- ✅ **Pattern 11: Exception Handling** - State machine error recovery
- ✅ **Pattern 17: Evaluation & Monitoring** - Quality rubrics and scoring
- ⚠️ **Pattern 8: Memory Management** - Consider for multi-project context (Phase 2)
- ⚠️ **Pattern 12: Human-in-the-Loop** - Client review and approval workflow

## Phase 1 – Automated Design Loop Prototype
- Build orchestrator to move from intake data → planning agent → design agent → critic loop → store Figma link.
- Run end-to-end on sample data with zero manual prompt copy/paste.

## Phase 2 – Client Portal Integration
- Hook intake form to orchestrator.
- Surface live Figma previews and “approve / request changes” buttons.
- Feedback agent translates client input into design refinements automatically.

## Phase 3 – Implementation & QA Agents
- Use Figma Dev Mode + ShadCN MCPs so Cursor/Claude generate Next.js code automatically.
- QA agent runs lint, Playwright, analytics checks; deployment agent handles Vercel.

## Phase 4 – Safety, Monitoring, Documentation
- Add logging, cost tracking, rollback playbooks, human override switches.
- Document onboarding and maintenance workflows.

### Analytics / GA4 Creation
Creating GA4 properties and environment variables can be deferred until DBAs are finalized. The current codebase already expects the env vars `NEXT_PUBLIC_GA4_CONSUMER_ID`, `NEXT_PUBLIC_GA4_BESPOKE_ID`, and `NEXT_PUBLIC_GA4_ENTERPRISE_ID`; placeholders are acceptable for now. When final names are approved, we will:
1. Create the real GA4 measurement IDs.
2. Update Vercel env vars (`vercel env add … --overwrite`) and `.env.local`.
3. Adjust the hostname mapping if the final DBA domains differ from the current placeholders.

This deferral lets us progress through Phases 0–3 without blocking on branding decisions.

---

## Active Project: Weight Tracker Redesign

**Status**: Scaffolding Complete | Design Phase Pending  
**Branch**: `weight-tracker-redesign`  
**Legacy UI Snapshot**: `weight-tracker-v1-ui` (tag)  

### Redesign Planning

The current Weight Tracker UI has been frozen at tag `weight-tracker-v1-ui`. A complete redesign will be implemented from scratch with:

#### Scaffolding Files Created:
- **Prompts**: `prompts/design-planning.txt`, `prompts/figma-generation.txt`, `prompts/design-critic.txt`, `prompts/design-refinement.txt`, `prompts/feedback-processing.txt`
- **Supabase Schema**: `supabase/schema/projects.sql`, `supabase/schema/design_versions.sql`, `supabase/schema/feedback.sql`, `supabase/schema/state_transitions.sql`

#### Next Steps:
1. Claude to populate prompt templates with specific design requirements
2. Claude to define database schemas for design orchestration
3. Implement design generation workflow using Figma Make API
4. Build critique and refinement agents
5. Generate fresh UI components based on new designs

The redesign will leverage the existing authentication flow and data models while completely rebuilding the UI layer for improved usability and visual consistency.
