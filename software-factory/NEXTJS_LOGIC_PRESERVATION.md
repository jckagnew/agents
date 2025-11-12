# Next.js Logic Preservation Document

> **Purpose**: This document preserves the business logic, architecture patterns, and workflows from the Next.js implementations of the Admin Dashboard and Splash Creator. Use this as a reference when migrating to the Expo (React Native) implementation.

**Last Updated**: November 12, 2025
**Next.js Version**: 14.1.0
**Status**: Reference Document for Expo Migration

---

## Table of Contents

1. [Admin Dashboard Logic](#1-admin-dashboard-logic)
2. [Splash Creator Logic](#2-splash-creator-logic)
3. [Shared Patterns](#3-shared-patterns)
4. [Business Logic to Preserve](#4-business-logic-to-preserve)
5. [Migration Considerations](#5-migration-considerations)

---

## 1. Admin Dashboard Logic

### 1.1 Component Architecture

#### Layout Pattern
- **Two-column grid layout**: Sidebar navigation (260px) + main content area
- **Responsive design**: Collapses to single column on mobile (<960px)
- **Sidebar content**: Brand header + navigation links
- **Navigation items**: Dashboard, Projects, Health Alerts, Splash Creator

```typescript
// Layout structure:
<div className="app-shell">
  <aside className="sidebar">
    <div className="brand">Factory Admin</div>
    <nav>
      <a href="/">Dashboard</a>
      <a href="/projects">Projects</a>
      <a href="/health">Health Alerts</a>
      <a href="/splash">Splash Creator</a>
    </nav>
  </aside>
  <main className="content">{children}</main>
</div>
```

#### Dashboard Overview
- **Card-based metrics display**
- **Auto-fit grid layout**: `repeat(auto-fit, minmax(240px, 1fr))`
- **Three primary cards**:
  1. Projects count with "View projects" CTA
  2. Health alerts count with "View alerts" CTA
  3. Splash Creator launcher with "Open splash creator" CTA

### 1.2 Data Models

#### Project Data Structure
```typescript
interface FactoryProject {
  id: string;                    // Unique identifier (e.g., "weight-tracker-nextjs")
  name: string;                  // Display name (e.g., "Weight Tracker Pro")
  description?: string;          // One-line project overview
  designTokens?: {
    palette: Array<{
      name: string;              // Role name (e.g., "Primary")
      value: string;             // Hex color (e.g., "#22c55e")
      role: string;              // Semantic role (e.g., "primary", "secondary", "accent")
    }>;
    typography: Array<{
      name: string;              // Role name (e.g., "Heading")
      fontFamily: string;        // Font name (e.g., "Nunito")
      weight: number;            // Font weight (e.g., 700)
    }>;
    imageryStyle?: string;       // Description of imagery style
    animationStyle?: string;     // Description of animation style
  };
  createdAt: string;             // ISO 8601 timestamp
  updatedAt: string;             // ISO 8601 timestamp
}
```

**Storage Location**: `/software-factory/data/projects.json`

#### Health Alert Data Structure
```typescript
interface HealthAlert {
  id: string;                    // Unique identifier
  title: string;                 // Alert title
  description?: string;          // Detailed description
  source: string;                // Source of alert (e.g., "npm audit")
  severity: "critical" | "high" | "medium" | "low";
  status: string;                // Current status (e.g., "watching", "resolved")
  detectedAt: string;            // ISO 8601 timestamp
  updatedAt: string;             // ISO 8601 timestamp
  affectedProjects: string[];    // Array of project IDs
  references?: string[];         // External reference URLs
  remediation?: string;          // Suggested fix
  nextReview?: string;           // ISO 8601 timestamp for next review
}
```

**Storage Location**: `/software-factory/data/health-alerts.json`

### 1.3 UI/UX Patterns and Workflows

#### Projects Management Workflow

**1. List View (`/projects`)**
- Table layout with columns: Name, Description, Actions
- "New project" button in header
- Each row links to project detail page
- "Edit" link opens detail view

**2. Create New Project (`/projects/new`)**
- Server action form (`"use server"`)
- Required fields: Project ID, Name
- Optional field: Description
- Validation:
  - ID and Name are required
  - ID must be unique (checks existing projects)
  - Timestamps automatically added (createdAt, updatedAt)
- On success: Redirects to project detail page
- Uses `revalidatePath("/projects")` for cache invalidation

**3. Edit Project (`/projects/[projectId]`)**
- Server action form for updates
- Editable fields:
  - Name (required)
  - Description
  - Primary color (design token)
  - Heading font (design token)
- Partial update strategy: Only updates provided fields
- Design token merging: Preserves existing tokens, updates specific ones
- Updates `updatedAt` timestamp
- Uses `revalidatePath("/projects")` for cache invalidation

#### Health Alerts Workflow

**1. List View (`/health`)**
- Card-based list layout
- Each alert shows:
  - Severity badge (color-coded: critical=red, high=orange, medium=blue, low=green)
  - Title
  - Status
  - Updated timestamp (localized format)
  - Reference links (if available)
- No editing in this version (read-only)
- Direct file read from `health-alerts.json`

#### Splash Creator Integration

**Purpose**: Bridge between Admin and Splash Creator
- Displays instructions for launching splash creator
- Provides project context for selection
- Links to `http://localhost:3001` (splash creator dev server)
- Three-step instructions:
  1. Ensure splash creator dev server is running
  2. Open the wizard URL
  3. Use project list for context when launching runs

### 1.4 API Integration Patterns

#### Projects API (`/api/projects`)

**GET** `/api/projects`
- Returns: `{ projects: FactoryProject[] }`
- Loads from `projects.json` file
- No pagination (assumes manageable project count)

**POST** `/api/projects`
- Body: `{ id, name, description?, designTokens? }`
- Validation:
  - Requires `id` and `name`
  - Checks for duplicate IDs (409 Conflict)
- Auto-adds timestamps
- Returns: Created project (201 Created)

**GET** `/api/projects/[projectId]`
- Returns: Single project or 404
- Direct lookup by ID

**PATCH** `/api/projects/[projectId]`
- Body: Partial project updates
- Merges with existing data
- Updates `updatedAt` timestamp
- Returns: Updated project

**DELETE** `/api/projects/[projectId]`
- Removes project from registry
- Returns: Removed project
- Note: No cascade delete handling

#### Health API (`/api/health`)

**GET** `/api/health`
- Returns: `{ alerts: HealthAlert[] }`
- Loads from `health-alerts.json` file
- Error handling: Returns empty array on failure
- No caching strategy specified

#### Data Loading Pattern

```typescript
// Server-side data loading pattern
import { readFile, writeFile } from "fs/promises";
import { join } from "path";

async function loadProjects(): Promise<FactoryProject[]> {
  const projectsPath = join(process.cwd(), "..", "data", "projects.json");
  const raw = await readFile(projectsPath, "utf-8");
  return JSON.parse(raw);
}

async function saveProjects(projects: FactoryProject[]): Promise<void> {
  const projectsPath = join(process.cwd(), "..", "data", "projects.json");
  await writeFile(projectsPath, JSON.stringify(projects, null, 2));
}
```

### 1.5 Key Features and Functionality

1. **Project Registry CRUD**
   - Create: Form-based with server actions
   - Read: List view + detail view
   - Update: Server actions with partial updates
   - Delete: API endpoint (not exposed in UI)

2. **Design Token Management**
   - Inline editing in project detail view
   - Partial token updates (palette, typography)
   - Preservation of existing tokens when updating

3. **Health Monitoring Dashboard**
   - Read-only alert feed
   - Severity-based visual coding
   - Reference link tracking
   - Timestamp display

4. **Capability Launcher**
   - Integration point for Splash Creator
   - Context passing via project selection
   - Multi-app coordination pattern

---

## 2. Splash Creator Logic

### 2.1 Workflow Steps and State Management

#### Step-Based Wizard Pattern

**Four-Step Flow**:
1. **Project Selection**: Choose factory project to inherit design tokens
2. **Creative Brief**: Define tone, headlines, CTAs, and targeting
3. **Guidance Assets**: Upload inspiration (placeholder - not yet implemented)
4. **Review & Launch**: Confirm inputs and submit workflow

#### Step State Machine

```typescript
type StepKey = "project" | "brief" | "guidance" | "review";

interface StepDefinition {
  key: StepKey;
  label: string;
  description: string;
}

// State transitions:
// project -> brief -> guidance -> review
// Back button available except on first step
// Next button enabled only when validation passes
```

#### Step Validation Logic

```typescript
function canAdvance(): boolean {
  switch (currentStepKey) {
    case "project":
      return Boolean(selectedProjectId);
    case "brief":
      return Boolean(primaryHeadline && callToActionPrimary);
    case "guidance":
      return true; // No validation (placeholder)
    case "review":
      return true; // Validated on launch
  }
}
```

#### Navigation Controls
- **Back button**: Disabled on step 0, enabled otherwise
- **Next button**: Shows on steps 0-2, disabled when validation fails
- **Launch button**: Shows on step 3 (review), requires project + headline + CTA

### 2.2 Form State Structure (NOT Zustand - Local State)

**Note**: Despite the package.json including Zustand, the current implementation uses React's `useState` for form state management.

```typescript
interface FormState {
  // Tone selection
  tone: "confident" | "premium" | "approachable" | "playful" | "other";
  toneOther: string;                    // Custom tone description

  // Copy fields
  primaryHeadline: string;              // Required
  secondaryHeadline: string;
  callToActionPrimary: string;          // Required
  callToActionSecondary: string;

  // Targeting fields
  targetAudience: string;
  keywords: string;                     // Comma-separated
  goals: string;                        // Comma-separated

  // Design inheritance
  inheritsDesignTokens: boolean;        // Default: true
}
```

**State Management Pattern**:
```typescript
const [formState, setFormState] = useState<FormState>(initialFormState);
const [selectedProjectId, setSelectedProjectId] = useState<string>("");
const [designTokens, setDesignTokens] = useState<DesignTokens | null>(null);
const [currentStep, setCurrentStep] = useState<number>(0);
const [runStatus, setRunStatus] = useState<SplashGenerationResult | null>(null);
```

### 2.3 Zod Validation Schemas

**Note**: Schema files are imported but not present in the codebase. Based on usage, here's the inferred structure:

```typescript
// @/lib/schemas (to be implemented)

import { z } from "zod";

// Creative Brief Schema
const creativeBriefSchema = z.object({
  projectId: z.string().min(1),
  projectName: z.string().min(1),
  tone: z.enum(["confident", "premium", "approachable", "playful", "other"]),
  toneOther: z.string().optional(),
  primaryHeadline: z.string().min(1),
  secondaryHeadline: z.string().optional(),
  callToActionPrimary: z.string().min(1),
  callToActionSecondary: z.string().optional(),
  targetAudience: z.string().optional(),
  goals: z.array(z.string()).optional(),
  keywords: z.array(z.string()).optional(),
  inheritsDesignTokens: z.boolean(),
  designTokensOverride: z.object({
    palette: z.array(z.object({
      name: z.string(),
      value: z.string(),
      role: z.string()
    })),
    typography: z.array(z.object({
      name: z.string(),
      fontFamily: z.string(),
      weight: z.number()
    })),
    imageryStyle: z.string().optional(),
    animationStyle: z.string().optional()
  }).optional(),
  guidanceAssets: z.array(z.any()).default([]),
  references: z.any().optional()
});

// Health Alert Schema
const healthAlertSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string().optional(),
  source: z.string(),
  severity: z.enum(["critical", "high", "medium", "low"]),
  status: z.string(),
  detectedAt: z.string(),
  updatedAt: z.string(),
  affectedProjects: z.array(z.string()),
  references: z.array(z.string()).optional(),
  remediation: z.string().optional(),
  nextReview: z.string().optional()
});
```

### 2.4 Component Architecture

#### Main Page Component (`app/page.tsx`)
- Client component (`"use client"`)
- Single-file implementation (no separate components folder for logic)
- Co-located sub-components (StepIndicator)
- Scoped CSS using styled-jsx

#### DesignTokenPreview Component

**Purpose**: Display inherited design tokens from selected project

```typescript
interface Props {
  tokens: DesignTokens | null;
  projectName?: string;
  isLoading?: boolean;
}
```

**Display Sections**:
1. **Palette**: Color swatches with name and hex value
2. **Typography**: Font family, size, weight details
3. **Imagery & Animation**: Style descriptions

**Loading States**:
- `isLoading`: Shows "Loading design tokens…"
- `!tokens`: Shows "Select a project to inherit its design language."
- `tokens`: Renders full token preview

#### GuidancePlaceholder Component

**Purpose**: Roadmap placeholder for future guidance uploader

**Planned Features** (documented in component):
- Upload multiple assets with inline previews
- Tag assets with priority and usage notes
- Bias sourcing prompts with structured annotations
- Reuse saved guidance sets across projects

**Current State**: Static informational component

### 2.5 Image Processing Logic (Backend Integration)

**Note**: The actual image processing happens in Python scripts, but the Next.js app orchestrates the workflow.

#### Workflow Orchestration Pattern

```typescript
// POST /api/runs
// 1. Validate creative brief with Zod
const parsed = creativeBriefSchema.safeParse(payload);

// 2. Create temporary directory for run
const tempDir = join(process.cwd(), "..", "generated-apps", projectId, "temp");
await mkdir(tempDir, { recursive: true });

// 3. Write brief to JSON file
const briefPath = join(tempDir, `brief-${runId}.json`);
await writeFile(briefPath, JSON.stringify(brief, null, 2));

// 4. Create results tracking file
const resultsPath = join(tempDir, `results-${runId}.json`);
const initialResults = {
  runId,
  status: "pending",
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  brief: brief,
  phases: {},
  artifacts: []
};

// 5. Spawn Python orchestration script
const pythonProcess = spawn("python3", [scriptPath], {
  cwd: scriptsDir,
  stdio: ["pipe", "pipe", "pipe"]
});

// 6. Monitor process output
pythonProcess.stdout.on("data", (data) => console.log(`Python stdout: ${data}`));
pythonProcess.stderr.on("data", (data) => console.error(`Python stderr: ${data}`));

// 7. On completion, transform results
pythonProcess.on("close", async (code) => {
  // Read workflow_results.json from Python script
  // Transform to our format
  // Update results file
});

// 8. Return immediately with run ID (202 Accepted)
return { runId, status: "pending" };
```

#### Results Transformation

```typescript
// Transform Python workflow results to frontend format
{
  runId: string,
  status: "pending" | "running" | "complete" | "failed",
  createdAt: string,
  updatedAt: string,
  brief: CreativeBrief,
  phases: Record<string, any>,  // From Python workflow phases
  artifacts: Array<{
    variantId: string,           // Generated ID (variant-1, variant-2, etc.)
    previewUrl: string,          // Image URL from Python script
    score: number,               // Overall score from evaluation
    metadata: {
      rank: number,
      beforeDescription: string,
      afterDescription: string,
      scores: object,            // Detailed scores (commercial_appeal, etc.)
      implementationSuggestions: array
    },
    approved?: boolean,          // Set when user approves
    approvedAt?: string
  }>
}
```

### 2.6 Generation Workflow

#### Phase 1: Project Selection
1. Load projects from `/api/projects`
2. User selects project
3. Load design tokens from `/api/projects/[projectId]/design`
4. Display tokens in preview panel
5. Enable "Next" button

#### Phase 2: Creative Brief
1. User fills form fields (tone, headlines, CTAs, etc.)
2. Comma-separated fields parsed into arrays (keywords, goals)
3. Design token inheritance toggle affects payload
4. Validation: Primary headline + primary CTA required
5. Enable "Next" button when valid

#### Phase 3: Guidance Assets
1. Display placeholder (not yet implemented)
2. No validation required
3. "Next" always enabled

#### Phase 4: Review & Launch
1. Display summary of all inputs
2. "Launch workflow" button enabled when:
   - Project selected
   - Primary headline provided
   - Primary CTA provided
3. On launch:
   - Build `CreativeBrief` payload
   - POST to `/api/runs`
   - Receive run ID and status
   - Display run status card
   - Keep user on review step (for future polling)

#### Approval Workflow (Planned)
- POST `/api/runs/[runId]` with `{ variantId }`
- Marks variant as approved
- Updates results file with approval timestamp
- Returns success confirmation

---

## 3. Shared Patterns

### 3.1 Design Tokens and Theming

#### Color System

**Admin Dashboard**:
- Background: `#f8fafc` (light slate)
- Text: `#0f172a` (dark slate)
- Cards: `#ffffff` (white)
- Accent: `linear-gradient(135deg, #6366f1, #a855f7)` (indigo to purple)
- Sidebar: `linear-gradient(180deg, #1f2937 0%, #111827 100%)` (dark gray gradient)

**Splash Creator**:
- Background: `radial-gradient(circle at top left, #fdf2f8, #eef2ff)` (pink to blue)
- Text: `#0f172a` (dark slate)
- Cards: `#ffffff` (white)
- Accent: `linear-gradient(135deg, #6366f1, #a855f7)` (indigo to purple)
- Muted text: `#475569` (slate)

**Severity Color Coding** (Health Alerts):
```css
critical: background: rgba(220, 38, 38, 0.15), color: #b91c1c (red)
high:     background: rgba(245, 158, 11, 0.15), color: #b45309 (orange)
medium:   background: rgba(59, 130, 246, 0.15), color: #1d4ed8 (blue)
low:      background: rgba(34, 197, 94, 0.15),  color: #15803d (green)
```

#### Typography System
- Primary font: `"Inter"` (fallback to system fonts)
- Font weights: 400 (body), 500 (medium), 600 (semi-bold), 700 (bold)
- Heading sizes: Project-specific (Nunito, Poppins)

#### Spacing System
- Card padding: `1.5rem` to `2rem`
- Grid gaps: `1rem` to `2rem`
- Border radius: `12px` (small), `16px` (medium), `18px` (large), `20px` (xl), `999px` (pill)
- Box shadows: `0 12px 24px rgba(15, 23, 42, 0.08)` (light), `0 18px 30px rgba(15, 23, 42, 0.08)` (medium)

### 3.2 Configuration Patterns

#### Path Resolution
- Both apps use `@/*` alias mapping to project root
- Relative imports for sibling components
- Data files accessed via `process.cwd()` + relative path

#### Environment Assumptions
- Development: Multiple Next.js apps on different ports
- Admin: Default port (3000)
- Splash Creator: Port 3001
- File system access: Direct read/write to shared data directory

#### API Conventions
- REST-like endpoints
- JSON request/response
- Error responses: `{ error: string, ...additionalInfo }`
- Success responses: Direct data or `{ [key]: data }`
- Status codes: 200 (success), 201 (created), 202 (accepted), 400 (validation), 404 (not found), 409 (conflict), 500 (server error)

### 3.3 Data Fetching Strategies

#### Server Components (Admin)
- Direct file system access in server components
- Async functions for data loading
- No client-side caching (relies on Next.js caching)

```typescript
// Server component pattern
export default async function Page() {
  const data = await loadDataFromFile();
  return <div>{/* render data */}</div>;
}
```

#### Client Components (Splash Creator)
- `useEffect` for data loading
- Multiple loading states
- Fetch API for HTTP requests
- Local state management (useState)

```typescript
// Client component pattern
const [data, setData] = useState<T[]>([]);
const [isLoading, setIsLoading] = useState(false);

useEffect(() => {
  const loadData = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/endpoint");
      const json = await res.json();
      setData(json.data);
    } catch (error) {
      console.error("Failed to load", error);
    } finally {
      setIsLoading(false);
    }
  };
  loadData();
}, [dependency]);
```

#### Revalidation Strategy
- `revalidatePath()` after mutations in server actions
- No explicit cache keys
- Relies on Next.js automatic caching

### 3.4 Error Handling Approaches

#### API Route Error Handling
```typescript
try {
  // Operation
  return NextResponse.json({ data });
} catch (error) {
  console.error("Operation failed", error);
  return NextResponse.json(
    { error: "User-friendly message" },
    { status: 500 }
  );
}
```

#### Client-Side Error Handling
```typescript
try {
  const res = await fetch("/api/endpoint");
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error ?? "Failed to perform operation");
  }
  // Success handling
} catch (error: any) {
  console.error(error);
  setErrorState(error.message ?? "Unexpected error");
}
```

#### Form Error Handling
- Validation errors: Display inline with form
- Server errors: Display error message above form
- Redirect on success, show error on failure

---

## 4. Business Logic to Preserve

### 4.1 Project Registry CRUD Operations

#### Core Business Rules

**Create Project**:
1. ID must be unique across all projects
2. ID and Name are required fields
3. Description is optional
4. Timestamps (createdAt, updatedAt) are auto-generated
5. Design tokens are optional at creation
6. On success: Redirect to project detail page

**Update Project**:
1. Only update provided fields (partial updates)
2. Cannot change project ID
3. Design token updates merge with existing tokens
4. Update `updatedAt` timestamp
5. Preserve fields not included in update

**Read Projects**:
1. Return all projects (no pagination in current version)
2. Support single project lookup by ID
3. Include all design tokens in response

**Delete Project**:
1. Remove from registry
2. No cascade deletion of related records
3. No soft delete (permanent removal)

#### Design Token Management Logic

**Token Structure Preservation**:
- Palette: Multiple colors with roles (primary, secondary, accent)
- Typography: Multiple font definitions with roles (heading, body)
- Imagery style: Free-text description
- Animation style: Free-text description

**Update Strategy**:
```typescript
// Merge strategy for partial updates
const updated: FactoryProject = {
  ...existingProject,
  name: newName || existingProject.name,
  description: newDescription,
  designTokens: {
    ...existingProject.designTokens,
    palette: newPrimaryColor
      ? [{ name: "Primary", value: newPrimaryColor, role: "primary" }]
      : existingProject.designTokens?.palette,
    typography: newHeadingFont
      ? [{ name: "Heading", fontFamily: newHeadingFont, weight: 600 }]
      : existingProject.designTokens?.typography
  },
  updatedAt: new Date().toISOString()
};
```

### 4.2 Health Monitoring System

#### Alert Tracking Logic

**Alert Properties**:
- Unique ID for tracking
- Title and description
- Source system (e.g., "npm audit")
- Severity level (critical, high, medium, low)
- Status (e.g., "watching", "resolved")
- Detection and update timestamps
- Affected project IDs (many-to-many relationship)
- External references (URLs)
- Remediation suggestions
- Next review date

**Display Logic**:
1. Sort alerts by severity (critical first)
2. Color-code severity badges
3. Show most recent update timestamp
4. Link to external references
5. Show affected projects

**No Editing in Current Version**: Health alerts are managed externally and synced to JSON file

### 4.3 Splash Generation Workflow

#### Workflow Orchestration

**Step 1: Project Context Loading**
1. Fetch available projects
2. User selects project
3. Fetch design tokens for project
4. Display tokens in preview panel
5. Prepare token inheritance for brief

**Step 2: Creative Brief Assembly**
1. Collect required fields:
   - Primary headline (required)
   - Primary CTA (required)
2. Collect optional fields:
   - Tone (with custom option)
   - Secondary headline
   - Secondary CTA
   - Target audience
   - Goals (comma-separated → array)
   - Keywords (comma-separated → array)
3. Design token inheritance decision
4. Validate before proceeding

**Step 3: Guidance Asset Collection**
- Placeholder for future feature
- Will collect:
  - Reference images
  - Motion clips
  - Priority tags
  - Usage notes

**Step 4: Workflow Submission**
1. Build CreativeBrief payload from form state
2. Include design tokens (inherited or override)
3. Submit to `/api/runs` (POST)
4. Receive run ID
5. Poll for status updates (planned)
6. Display artifacts when ready (planned)

#### Python Script Integration

**Orchestration Pattern**:
1. Write brief to temporary JSON file
2. Spawn Python process with script path
3. Monitor stdout/stderr
4. On completion, read results file
5. Transform Python results to frontend format
6. Update run status

**Results File Structure**:
```json
{
  "runId": "uuid",
  "status": "pending|running|complete|failed",
  "createdAt": "ISO timestamp",
  "updatedAt": "ISO timestamp",
  "brief": { /* CreativeBrief object */ },
  "phases": { /* Workflow phase results */ },
  "artifacts": [
    {
      "variantId": "variant-1",
      "previewUrl": "path/to/image.png",
      "score": 0.85,
      "metadata": {
        "rank": 1,
        "beforeDescription": "...",
        "afterDescription": "...",
        "scores": {
          "commercial_appeal": 0.9,
          "animation_potential": 0.8,
          "design_quality": 0.85
        },
        "implementationSuggestions": [...]
      }
    }
  ]
}
```

### 4.4 Design Token Editing

#### Inline Editing Pattern

**Admin Dashboard Approach**:
- Edit design tokens within project detail view
- Form fields for primary color and heading font
- Partial updates preserve other tokens
- No separate design token management UI

**Splash Creator Approach**:
- Read-only token preview
- Inheritance from selected project
- Option to override with custom tokens (not fully implemented)
- No token editing in splash creator

#### Token Inheritance Logic

```typescript
// Splash Creator brief assembly
const brief: CreativeBrief = {
  projectId: selectedProject.id,
  projectName: selectedProject.name,
  // ... other brief fields
  inheritsDesignTokens: formState.inheritsDesignTokens,
  designTokensOverride: formState.inheritsDesignTokens
    ? undefined
    : designTokens ?? undefined,
};
```

**Inheritance Rules**:
1. By default, inherit all tokens from project
2. If inheritance disabled, include full token set in brief
3. Python workflow uses tokens to guide image selection and styling

### 4.5 Capability Launcher Patterns

#### Multi-App Coordination

**Admin Dashboard as Hub**:
- Central dashboard for all factory capabilities
- Links to specialized tools (Splash Creator, etc.)
- Context passing via project selection
- Shared data directory for coordination

**Launch Pattern**:
1. User selects "Splash Creator" from admin
2. Opens splash creator in separate tab/window
3. User selects same project in splash creator
4. Splash creator inherits project context
5. Workflow runs independently
6. Results stored in shared directory

**Data Handoff**:
- No direct data passing between apps
- Projects stored in shared JSON file
- Each app reads projects independently
- Workflow results stored per-project

---

## 5. Migration Considerations

### 5.1 From Next.js to Expo/React Native

#### Platform Differences

**Layout & Navigation**:
- Next.js: File-based routing, links, browser navigation
- Expo: Stack/Tab navigators, programmatic navigation
- **Preserve**: Navigation hierarchy and step-based flow logic

**Styling**:
- Next.js: styled-jsx, CSS modules, Tailwind
- Expo: StyleSheet, styled-components, or Tailwind (NativeWind)
- **Preserve**: Design tokens, color system, spacing values

**Data Fetching**:
- Next.js: Server components, server actions, API routes
- Expo: Client-only fetching (fetch API, React Query, etc.)
- **Preserve**: API contract, validation logic, error handling patterns

**File System**:
- Next.js: Direct file system access (Node.js)
- Expo: No file system access, requires backend API
- **Preserve**: Data models, CRUD logic (move to backend API)

#### Component Equivalents

| Next.js Pattern | Expo/React Native Equivalent |
|-----------------|------------------------------|
| `<div>` | `<View>` |
| `<span>`, `<p>` | `<Text>` |
| `<input>` | `<TextInput>` |
| `<button>` | `<Button>` or `<Pressable>` |
| `<select>` | `<Picker>` or custom dropdown |
| `<a>` (link) | `<Link>` from Expo Router |
| styled-jsx | StyleSheet or styled-components |
| CSS grid | Flexbox (React Native doesn't support grid) |

#### State Management Migration

**Current** (Next.js Splash Creator):
- Local state with useState
- Multiple useState calls
- useEffect for data loading
- No global state management

**Recommended** (Expo):
- Zustand (already in package.json, not used yet)
- Create store for wizard state
- Persist state across navigation
- Share state between screens

```typescript
// Example Zustand store for splash creator
import create from 'zustand';

interface SplashCreatorState {
  currentStep: number;
  selectedProjectId: string;
  formState: FormState;
  designTokens: DesignTokens | null;
  runStatus: SplashGenerationResult | null;

  setCurrentStep: (step: number) => void;
  setSelectedProjectId: (id: string) => void;
  updateFormState: (updates: Partial<FormState>) => void;
  setDesignTokens: (tokens: DesignTokens | null) => void;
  setRunStatus: (status: SplashGenerationResult | null) => void;
  resetState: () => void;
}

const useSplashCreatorStore = create<SplashCreatorState>((set) => ({
  currentStep: 0,
  selectedProjectId: "",
  formState: initialFormState,
  designTokens: null,
  runStatus: null,

  setCurrentStep: (step) => set({ currentStep: step }),
  setSelectedProjectId: (id) => set({ selectedProjectId: id }),
  updateFormState: (updates) => set((state) => ({
    formState: { ...state.formState, ...updates }
  })),
  setDesignTokens: (tokens) => set({ designTokens: tokens }),
  setRunStatus: (status) => set({ runStatus: status }),
  resetState: () => set({
    currentStep: 0,
    selectedProjectId: "",
    formState: initialFormState,
    designTokens: null,
    runStatus: null
  })
}));
```

#### Backend Requirements for Expo

**File System Operations Must Move to API**:
1. Project CRUD → RESTful API or tRPC
2. Health alerts loading → API endpoint
3. Workflow submission → API with job queue
4. Results polling → WebSocket or polling API

**Recommended Architecture**:
```
Expo App (Frontend)
    ↓ HTTP/WebSocket
Express/Fastify API (Node.js)
    ↓ File System / Database
Data Storage (JSON files or DB)
    ↓ Process Spawning
Python Workflow Scripts
```

### 5.2 Feature Parity Checklist

#### Admin Dashboard

- [ ] Dashboard overview with project/alert counts
- [ ] Projects list view with search/filter
- [ ] Create new project form
- [ ] Edit project with design tokens
- [ ] Health alerts list view
- [ ] Severity-based color coding
- [ ] Navigation to splash creator
- [ ] Responsive layout (mobile + tablet)

#### Splash Creator

- [ ] Four-step wizard flow
- [ ] Project selection with token preview
- [ ] Creative brief form with validation
- [ ] Guidance asset upload (future)
- [ ] Review & launch workflow
- [ ] Run status tracking
- [ ] Artifact preview gallery (future)
- [ ] Variant approval (future)
- [ ] Step indicator with visual states
- [ ] Back/Next navigation
- [ ] Form state persistence

#### Shared Features

- [ ] Design token preview component
- [ ] Color palette display
- [ ] Typography display
- [ ] Consistent styling and theming
- [ ] Error handling and display
- [ ] Loading states
- [ ] Responsive design
- [ ] Accessibility features

### 5.3 Testing Strategy

#### Unit Tests
- Form validation logic
- Token inheritance logic
- Data transformation functions
- API client functions

#### Integration Tests
- Workflow submission end-to-end
- Project CRUD operations
- Design token loading and preview
- Error handling scenarios

#### E2E Tests
- Complete splash creation workflow
- Project management workflow
- Navigation between steps
- Form persistence across navigation

### 5.4 Data Migration Plan

**Phase 1: Keep JSON Files**
- Expo app calls Node.js backend
- Backend reads/writes JSON files (same as Next.js)
- No data migration needed
- Validates data with Zod on backend

**Phase 2: Database Migration (Optional)**
- Migrate projects.json → Database (SQLite, PostgreSQL, etc.)
- Migrate health-alerts.json → Database
- Add proper relationships and indexing
- Keep workflow results in file system (or S3)

**Schema Preservation**:
- Keep same TypeScript interfaces
- Use same validation schemas (Zod)
- Maintain API contracts
- Version API for breaking changes

### 5.5 Performance Considerations

**Next.js Advantages**:
- Server-side rendering
- Automatic code splitting
- File-based routing
- Server components (no JavaScript to client)

**Expo Advantages**:
- Native mobile performance
- Offline capabilities
- Native UI components
- Better mobile UX patterns

**Optimization for Expo**:
1. Implement data caching (React Query)
2. Optimize images for mobile
3. Use native components where possible
4. Implement pagination for large lists
5. Add pull-to-refresh patterns
6. Cache design tokens locally
7. Implement optimistic updates

### 5.6 Security Considerations

**Next.js Security**:
- Server-side validation
- No direct client access to file system
- API routes with middleware
- CSRF protection (built-in with server actions)

**Expo Security**:
- All validation must happen on backend
- Secure API communication (HTTPS)
- Token-based authentication recommended
- Sensitive data should not be stored in AsyncStorage
- API keys must not be in client code

**Migration Checklist**:
- [ ] Move all validation to backend API
- [ ] Implement authentication (if not already)
- [ ] Add rate limiting to API routes
- [ ] Validate all file paths (prevent traversal)
- [ ] Sanitize user inputs
- [ ] Add CORS configuration
- [ ] Use environment variables for secrets
- [ ] Implement request logging

---

## Appendix A: File Structure Reference

### Admin Dashboard (`/admin`)
```
admin/
├── app/
│   ├── api/
│   │   ├── health/
│   │   │   └── route.ts              # Health alerts API
│   │   └── projects/
│   │       ├── route.ts              # Projects list/create API
│   │       └── [projectId]/
│   │           └── route.ts          # Single project API
│   ├── health/
│   │   └── page.tsx                  # Health alerts page
│   ├── projects/
│   │   ├── page.tsx                  # Projects list page
│   │   ├── new/
│   │   │   └── page.tsx              # Create project page
│   │   └── [projectId]/
│   │       └── page.tsx              # Project detail page
│   ├── splash/
│   │   └── page.tsx                  # Splash creator launcher
│   ├── globals.css                   # Global styles
│   ├── layout.tsx                    # Root layout with sidebar
│   └── page.tsx                      # Dashboard overview
├── package.json
└── tsconfig.json
```

### Splash Creator (`/splash-creator`)
```
splash-creator/
├── app/
│   ├── api/
│   │   ├── health-alerts/
│   │   │   └── route.ts              # Health alerts API
│   │   ├── projects/
│   │   │   ├── route.ts              # Projects list API
│   │   │   └── [projectId]/
│   │   │       └── design/
│   │   │           └── route.ts      # Design tokens API
│   │   └── runs/
│   │       ├── route.ts              # Submit workflow API
│   │       └── [runId]/
│   │           └── route.ts          # Run status/approval API
│   ├── globals.css                   # Global styles
│   ├── layout.tsx                    # Root layout
│   └── page.tsx                      # Main wizard page
├── components/
│   ├── design-token-preview.tsx      # Token preview component
│   └── guidance-placeholder.tsx      # Guidance placeholder
├── docs/
│   └── flow-overview.md              # Workflow documentation
├── lib/                               # (Not yet implemented)
│   ├── schemas.ts                    # Zod schemas (to be created)
│   └── services.ts                   # Service layer (to be created)
├── package.json
└── tsconfig.json
```

### Shared Data (`/data`)
```
data/
├── projects.json                      # Project registry
└── health-alerts.json                 # Health monitoring data
```

---

## Appendix B: Key Dependencies

### Admin Dashboard
```json
{
  "next": "14.1.0",
  "react": "18.2.0",
  "react-dom": "18.2.0",
  "swr": "2.2.4",           // Not actively used in current implementation
  "typescript": "5.3.3"
}
```

### Splash Creator
```json
{
  "next": "14.1.0",
  "react": "18.2.0",
  "react-dom": "18.2.0",
  "zustand": "^4.5.0",      // In package.json but not yet used
  "zod": "^3.22.4",         // For validation
  "glob": "^10.3.10",       // For file searching
  "typescript": "5.3.3"
}
```

### Expo Equivalent Dependencies (Suggested)
```json
{
  "expo": "~50.0.0",
  "react": "18.2.0",
  "react-native": "0.73.0",
  "expo-router": "^3.0.0",    // File-based routing
  "zustand": "^4.5.0",        // State management (already planned)
  "zod": "^3.22.4",           // Validation (already used)
  "@tanstack/react-query": "^5.0.0",  // Data fetching
  "react-hook-form": "^7.49.0",       // Form management
  "nativewind": "^4.0.0"      // Tailwind for React Native (optional)
}
```

---

## Appendix C: API Contract Reference

### Projects API

**GET** `/api/projects`
```typescript
Response: {
  projects: Array<{
    id: string;
    name: string;
    description?: string;
    designTokens?: DesignTokens;
    createdAt: string;
    updatedAt: string;
  }>
}
```

**POST** `/api/projects`
```typescript
Request: {
  id: string;              // Required, unique
  name: string;            // Required
  description?: string;
  designTokens?: DesignTokens;
}

Response: FactoryProject (201 Created)
Error: { error: string } (400 | 409 | 500)
```

**GET** `/api/projects/[projectId]`
```typescript
Response: FactoryProject (200)
Error: { error: "Not found" } (404)
```

**PATCH** `/api/projects/[projectId]`
```typescript
Request: Partial<FactoryProject>

Response: FactoryProject (200)
Error: { error: string } (404 | 500)
```

**DELETE** `/api/projects/[projectId]`
```typescript
Response: FactoryProject (200)
Error: { error: "Not found" } (404)
```

### Design Tokens API

**GET** `/api/projects/[projectId]/design`
```typescript
Response: {
  designTokens: {
    palette: Array<{ name: string; value: string; role: string }>;
    typography: Array<{ name: string; fontFamily: string; weight: number }>;
    components: Array<any>;
    imageryStyle?: string;
    animationStyle?: string;
  }
}

Error: { error: string } (500)
```

### Runs API

**POST** `/api/runs`
```typescript
Request: CreativeBrief (validated with Zod)

Response: {
  runId: string;
  status: "pending";
  createdAt: string;
  updatedAt: string;
} (202 Accepted)

Error: {
  error: string;
  issues?: ZodIssue[];
} (400 | 500)
```

**GET** `/api/runs/[runId]`
```typescript
Response: SplashGenerationResult (200)
Error: { error: string } (404 | 500)
```

**POST** `/api/runs/[runId]` (Approve variant)
```typescript
Request: {
  variantId: string;
}

Response: { ok: true } (200)
Error: { error: string } (400 | 404 | 500)
```

### Health Alerts API

**GET** `/api/health` or `/api/health-alerts`
```typescript
Response: {
  alerts: Array<HealthAlert>
}

Error: { error: string } (500)
```

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-12 | Initial documentation of Next.js implementations |

---

**End of Document**
