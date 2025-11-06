# Architecture Documentation

## System Overview

The Design-First Software Factory is a multi-tier application that orchestrates the journey from initial user requirements to production-ready code.

```
┌─────────────────────────────────────────────────────────────┐
│                    Expo Application (Frontend)              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Intake    │→ │   Prompt     │→ │     Design       │  │
│  │     UI      │  │   Review     │  │     Review       │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓ (API Calls)
┌─────────────────────────────────────────────────────────────┐
│                  Supabase Backend                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Database   │  │ Edge         │  │  Auth &          │  │
│  │  (Postgres) │  │ Functions    │  │  Storage         │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓ (Orchestration)
┌─────────────────────────────────────────────────────────────┐
│              External AI Services                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   LLM       │  │   Stitch     │  │     Figma        │  │
│  │  (Gemini)   │  │   (Design)   │  │     (Output)     │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend (Expo/React Native)
- **Framework:** Expo SDK 50+
- **Language:** TypeScript
- **State Management:** React Context + Hooks
- **Navigation:** Expo Router (file-based routing)
- **UI Components:** React Native Paper / Custom components
- **Testing:** Jest + Detox (E2E)

### Backend (Supabase)
- **Database:** PostgreSQL
- **API:** Auto-generated REST + GraphQL
- **Auth:** Supabase Auth (email, OAuth)
- **Storage:** Supabase Storage (for generated artifacts)
- **Realtime:** Supabase Realtime (for status updates)
- **Edge Functions:** Deno-based serverless functions

### AI Integration
- **LLM Provider:** Google Gemini (via API)
- **Design Generation:** Stitch API
- **Design Output:** Figma (via API)
- **Code Generation:** Custom templates + AI assistance

## Data Model

### Core Entities

#### Project
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  name TEXT NOT NULL,
  description TEXT,
  service_tier TEXT CHECK (service_tier IN ('express', 'concierge')),
  status TEXT CHECK (status IN ('intake', 'prompt_engineering', 'design_generation', 'design_review', 'code_generation', 'complete', 'failed')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Requirements
```sql
CREATE TABLE requirements (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  raw_input TEXT NOT NULL,
  structured_data JSONB,
  approved BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Prompts
```sql
CREATE TABLE prompts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,
  content TEXT NOT NULL,
  approved BOOLEAN DEFAULT FALSE,
  approved_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Designs
```sql
CREATE TABLE designs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  figma_url TEXT,
  figma_file_id TEXT,
  approved BOOLEAN DEFAULT FALSE,
  approved_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Generated_Code
```sql
CREATE TABLE generated_code (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  design_id UUID REFERENCES designs(id),
  storage_path TEXT NOT NULL,
  bundled BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Service Architecture

### Frontend Services

#### ProjectService
- **Responsibility:** Project CRUD operations
- **Methods:** `createProject()`, `updateProject()`, `getProject()`, `listProjects()`

#### RequirementsService
- **Responsibility:** Requirements capture and validation
- **Methods:** `captureRequirements()`, `validateRequirements()`, `approveRequirements()`

#### DesignService
- **Responsibility:** Design generation and review
- **Methods:** `generateDesign()`, `getDesignStatus()`, `approveDesign()`

#### CodeGenerationService
- **Responsibility:** Code generation orchestration
- **Methods:** `generateCode()`, `getGenerationStatus()`, `downloadProject()`

### Backend Edge Functions

#### `/intake-processor`
- **Input:** Raw user requirements
- **Process:** LLM processing to structure requirements
- **Output:** Structured JSON + generated prompts

#### `/design-generator`
- **Input:** Approved prompts
- **Process:** Stitch API → Figma conversion
- **Output:** Figma file URL + file ID

#### `/design-validator`
- **Input:** Figma file ID
- **Process:** Validation checks (completeness, accessibility)
- **Output:** Validation report

#### `/code-generator`
- **Input:** Approved Figma design
- **Process:** Expo project scaffolding + component generation
- **Output:** Bundled project in storage

## Workflow States

### Express Tier Flow
```
intake → prompt_engineering → design_generation → design_review → code_generation → complete
  (auto)      (auto)              (auto)              (auto)           (auto)
```

### Concierge Tier Flow
```
intake → prompt_engineering → design_generation → design_review → code_generation → complete
  (user)    (approval gate)        (auto)        (approval gate)        (auto)
```

## Security Considerations

### Authentication
- Supabase Auth with JWT tokens
- Row-Level Security (RLS) policies on all tables
- API keys stored in secure environment variables

### Data Privacy
- User projects isolated by user_id
- Generated code stored in user-specific buckets
- Temporary artifacts cleaned up after 30 days

### API Rate Limiting
- Supabase Edge Functions have built-in rate limiting
- External API calls (Stitch, Figma) wrapped with retry logic
- User quotas enforced per service tier

## Scalability

### Database
- PostgreSQL with connection pooling
- Indexes on frequently queried fields (project_id, user_id, status)
- Archive old projects after 90 days

### Storage
- Supabase Storage with CDN
- Generated projects compressed before storage
- Lifecycle policies for automatic cleanup

### Compute
- Edge Functions auto-scale with demand
- Async job processing for long-running tasks
- Status polling with exponential backoff

## Monitoring & Observability

### Metrics
- Project creation rate
- Approval gate conversion rates
- Average time per phase
- Error rates per service

### Logging
- Structured logs in Edge Functions
- User action audit trail
- Error tracking with stack traces

### Alerts
- Failed code generation
- API quota exhaustion
- Unusual user activity

---

**Maintained by:** Claude (Foundation Architect)
**Last Updated:** 2025-11-06
