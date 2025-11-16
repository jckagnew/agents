#!/usr/bin/env node
/**
 * System Architecture Generator
 * Generates comprehensive technical architecture documentation
 *
 * Outputs:
 * - Tech stack recommendations with rationales
 * - Service/module map with Mermaid diagrams
 * - Data models with Prisma schemas
 * - API endpoint specifications
 * - Deployment and environment documentation
 *
 * Usage:
 *   node scripts/generate-architecture.js \
 *     --requirements session-X/requirements/iteration-0.json \
 *     --prd-dir session-X/prd \
 *     --output-dir session-X/architecture
 */

const fs = require('fs');
const path = require('path');

// Parse arguments
const args = process.argv.slice(2);
const getArg = (flag) => {
    const index = args.indexOf(flag);
    return index !== -1 ? args[index + 1] : null;
};

const requirementsFile = getArg('--requirements');
const prdDir = getArg('--prd-dir');
const outputDir = getArg('--output-dir');

if (!requirementsFile || !outputDir) {
    console.error('Usage: node generate-architecture.js --requirements <path> --prd-dir <path> --output-dir <path>');
    process.exit(1);
}

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// Read requirements
const requirements = JSON.parse(fs.readFileSync(requirementsFile, 'utf8'));

console.log('🏗️  Generating System Architecture...');
console.log(`   App: ${requirements.app_name}`);
console.log(`   Type: ${requirements.app_type}\n`);

// ============================================================================
// 1. TECH STACK
// ============================================================================

function generateTechStack(requirements) {
    const appName = requirements.app_name;
    const appType = requirements.app_type;
    const features = requirements.features?.must_have || [];

    // Determine stack based on app type and requirements
    const needsBackend = features.some(f =>
        f.toLowerCase().includes('sync') ||
        f.toLowerCase().includes('share') ||
        f.toLowerCase().includes('api')
    );

    const needsAuth = features.some(f =>
        f.toLowerCase().includes('account') ||
        f.toLowerCase().includes('user') ||
        f.toLowerCase().includes('profile')
    );

    const needsRealtime = features.some(f =>
        f.toLowerCase().includes('chat') ||
        f.toLowerCase().includes('live') ||
        f.toLowerCase().includes('notification')
    );

    return `# Tech Stack Architecture

## Executive Summary

${appName} is a ${appType.replace('_', ' ')} application prioritizing **simplicity, privacy, and performance**. Based on the PRD requirements, we recommend a **${needsBackend ? 'full-stack' : 'frontend-focused'}** architecture with local-first data storage and optional cloud sync.

## Frontend Stack

### Core Framework
**Choice**: **Next.js 14** (App Router with React Server Components)

**Rationale**:
- **Developer Experience**: Fast refresh, TypeScript support, built-in optimization
- **Performance**: Automatic code splitting, image optimization, font optimization
- **SEO**: Server-side rendering for marketing pages (splash screen)
- **Deployment**: Vercel zero-config deployment (or self-hosted)
- **Community**: Large ecosystem, extensive documentation, active maintenance

**Alternatives Considered**:
- **Vite + React**: Lighter weight but requires more configuration
- **Remix**: Excellent for forms but less mature ecosystem
- **SvelteKit**: Smaller bundle but smaller community

**Trade-offs**: Next.js is opinionated about routing/structure but this accelerates development for standard apps.

---

### State Management
**Choice**: **React Context API** + **localStorage**

**Rationale**:
- **Simplicity**: No external dependencies for basic state
- **Privacy**: All data stored locally, no cloud by default
- **Performance**: Sufficient for ${features.length} core features
- **Migration Path**: Easy upgrade to Zustand/Redux if needed

**When to Upgrade**:
- App grows beyond 10 features
- Need for complex async state
- Time-travel debugging required

**Alternatives**:
- **Zustand**: Drop-in replacement if Context becomes unwieldy
- **Redux Toolkit**: If team prefers Redux patterns
- **Jotai/Recoil**: For atomic state management

---

### UI Component Library
**Choice**: **Custom CSS** with **CSS Variables** (design tokens)

**Rationale**:
- **Brand Control**: Full control over design system (${requirements.design_preferences?.primary_color || '#4285F4'})
- **Performance**: No framework overhead (~50KB saved vs Material-UI)
- **Flexibility**: Easy to match mockups exactly
- **Learning**: Transparent implementation (no "magic")

**Component Patterns**:
- PillButton (rounded, primary/secondary/outline variants)
- MetricCard (dashboard statistics)
- ProgressBar (goal tracking)
- Navigation (tab-based for single-page app)

**Alternatives**:
- **Tailwind CSS**: Utility-first (add later if team prefers)
- **shadcn/ui**: Copy-paste components (good for rapid prototyping)
- **Material-UI**: Heavy but comprehensive (avoid for performance)

---

### Data Persistence
**Choice**: **localStorage** (primary) + **IndexedDB** (future)

**Rationale**:
- **Privacy First**: No server required, user owns data
- **Offline Support**: Works without internet
- **Simplicity**: Native browser API, no dependencies
- **GDPR Compliant**: No data leaves user's device

**Storage Strategy**:
\`\`\`typescript
interface StorageSchema {
  entries: Entry[];           // Core tracking data
  goals: Goal[];              // User-defined targets
  preferences: UserPrefs;     // Settings
  lastSync?: Date;            // Optional cloud sync timestamp
}
\`\`\`

**Migration Path**:
- **Phase 1**: localStorage (MVP, ~5MB limit)
- **Phase 2**: IndexedDB (unlimited, structured queries)
- **Phase 3**: Optional cloud sync (Firebase/Supabase)

---

## Backend Stack ${needsBackend ? '' : '(Optional - Not Required for MVP)'}

${needsBackend ? `
### API Framework
**Choice**: **Next.js API Routes** (serverless functions)

**Rationale**:
- **Monorepo**: Frontend + API in same codebase
- **TypeScript**: End-to-end type safety
- **Deployment**: Same platform as frontend (Vercel/self-hosted)
- **Cost**: Free tier sufficient for early users

**API Endpoints**:
\`\`\`
POST   /api/sync        - Sync local data to cloud (authenticated)
GET    /api/export      - Export data as JSON (authenticated)
POST   /api/auth/login  - Email/password authentication
POST   /api/auth/signup - Create account
\`\`\`

**Alternatives**:
- **tRPC**: Type-safe RPC (if heavy client-server communication)
- **GraphQL**: If complex data fetching patterns emerge
- **Separate Express API**: If need to deploy independently

---

### Database
**Choice**: **PostgreSQL** (via Supabase or Neon)

**Rationale**:
- **Reliability**: ACID transactions, proven at scale
- **TypeScript Integration**: Prisma ORM for type safety
- **Features**: JSON columns for flexible schemas
- **Managed**: Supabase/Neon handle backups, scaling

**Schema Design**: See \`architecture-data-model.md\`

**Alternatives**:
- **SQLite** (Turso/Cloudflare D1): Lower cost, simpler
- **MongoDB**: If document model fits better
- **Firebase**: All-in-one but vendor lock-in
` : `
**Decision**: **No backend required for MVP**

**Rationale**:
- All ${features.length} must-have features work locally
- Privacy-first approach (no accounts needed)
- Faster development (ship in weeks, not months)
- Lower hosting costs ($0 vs $20-50/month)

**When to Add Backend**:
- User requests cloud sync
- Team collaboration features
- Analytics/insights beyond local
- Monetization (subscriptions)
`}

---

## Infrastructure & Deployment

### Hosting
**Choice**: **Vercel** (frontend) ${needsBackend ? '+ **Supabase** (database)' : ''}

**Rationale**:
- **Zero Config**: \`git push\` to deploy
- **Global CDN**: <100ms response times worldwide
- **Free Tier**: Sufficient for 1000+ users
- **DX**: Preview deploys, instant rollbacks

**Deployment Flow**:
\`\`\`
main branch → Vercel Production (${appName.toLowerCase()}.vercel.app)
feature/* → Preview Deploys (pr-123.vercel.app)
\`\`\`

**Alternatives**:
- **Netlify**: Similar to Vercel, slightly different pricing
- **Cloudflare Pages**: Cheaper at scale, more config needed
- **Self-hosted**: VPS (DigitalOcean/Hetzner) if cost-sensitive

---

### CI/CD Pipeline
**Choice**: **GitHub Actions**

**Rationale**:
- **Integration**: Native GitHub integration
- **Free**: 2000 minutes/month for private repos
- **Flexible**: Can run tests, linting, security scans
- **Standard**: Industry-standard YAML config

**Pipeline Stages**:
\`\`\`yaml
build:
  - Install dependencies (npm ci)
  - Type check (tsc --noEmit)
  - Lint (eslint)
  - Build (next build)
  - Visual QA (Playwright tests)

deploy:
  - Preview (feature branches)
  - Production (main branch)
  - Rollback (manual trigger)
\`\`\`

---

### Monitoring & Observability
**Choice**: **Vercel Analytics** + **Sentry** (errors)

**Rationale**:
- **Built-in**: Vercel Analytics included (Web Vitals)
- **Errors**: Sentry free tier (5000 events/month)
- **Privacy**: No user tracking without consent

**Metrics to Track**:
- Core Web Vitals (LCP, FID, CLS)
- Error rates by page
- API response times ${needsBackend ? '(backend)' : ''}
- User sessions (anonymous)

**Alerting**:
- Slack webhook for critical errors
- Email for deployment failures
- Weekly health reports

---

## Security & Compliance

### Authentication ${needsAuth ? '(Required)' : '(Optional)'}
${needsAuth ? `
**Choice**: **NextAuth.js**

**Rationale**:
- **Providers**: Email, Google, GitHub out-of-box
- **Security**: Built-in CSRF, session management
- **Integration**: Works with Next.js API routes
- **Standards**: OAuth 2.0 / OpenID Connect

**Supported Methods**:
- Email + Password (with email verification)
- Google OAuth (social login)
- Magic Links (passwordless)
` : `
**Decision**: No authentication required for MVP (local-only app)
`}

### Data Privacy
**Approach**: **Privacy by Design**

**Principles**:
- **Local First**: All data stored on device by default
- **No Tracking**: No analytics without explicit opt-in
- **GDPR Ready**: Data export, deletion built-in
- **Transparency**: Clear privacy policy, open source

**GDPR Compliance Checklist**:
- [ ] Data minimization (only collect what's needed)
- [ ] User consent (opt-in for any cloud features)
- [ ] Right to access (export data as JSON)
- [ ] Right to deletion (clear all data button)
- [ ] Data portability (standard JSON format)

---

### Security Measures
**Implemented**:
- **CSP Headers**: Content Security Policy prevents XSS
- **Rate Limiting**: API endpoints throttled ${needsBackend ? '(Vercel built-in)' : '(N/A)'}
- **Input Validation**: All user input sanitized
- **Dependencies**: Automated security updates (Dependabot)

**Security Scanning**:
- **npm audit**: Weekly automated scans
- **Snyk**: Dependency vulnerability alerts
- **Semgrep**: Static analysis for code patterns

---

## Third-Party Integrations

### Current (MVP)
**None** - Intentionally avoiding dependencies for simplicity and privacy

### Future Consideration
${appType === 'health_tracking' ? `
- **AI Insights**: Claude API for personalized recommendations
- **Wearables**: Apple Health / Google Fit sync
- **Export**: CSV/PDF report generation
` : `
- **AI**: Claude API for intelligent features
- **Analytics**: PostHog (privacy-focused)
- **Payments**: Stripe (if monetization)
`}

**Integration Principles**:
- **Optional**: All integrations must be opt-in
- **Privacy**: No data sharing without explicit consent
- **Fallback**: App works fully without integrations
- **Vendor**: Prefer vendors with strong privacy policies

---

## Cross-Cutting Concerns

### Performance Targets
- **Load Time**: < 2 seconds (3G network)
- **Time to Interactive**: < 3 seconds
- **Bundle Size**: < 200KB initial (Next.js optimized)
- **Lighthouse Score**: ≥ 90 (all categories)

### Accessibility
- **Standard**: WCAG AA compliance
- **Testing**: axe DevTools, screen reader testing
- **Keyboard**: Full keyboard navigation
- **Contrast**: 4.5:1 minimum ratio

### Browser Support
- **Modern Browsers**: Last 2 versions
- **Mobile**: iOS Safari 14+, Chrome Android 90+
- **Desktop**: Chrome, Firefox, Safari, Edge
- **No IE11**: Modern features only

### Internationalization ${features.some(f => f.toLowerCase().includes('language')) ? '(Required)' : '(Future)'}
${features.some(f => f.toLowerCase().includes('language')) ? `
**Choice**: **next-intl**
- Locale detection, message formatting
- Right-to-left (RTL) support
- Pluralization, number/date formatting
` : `
**Decision**: English-only for MVP
- Add i18n when requested by users
- next-intl is drop-in compatible
`}

---

## Technology Decision Matrix

| Concern | Choice | Rationale | Alternative |
|---------|--------|-----------|-------------|
| **Frontend Framework** | Next.js 14 | SSR, performance, DX | Remix, Vite |
| **State Management** | Context + localStorage | Simple, privacy-first | Zustand, Redux |
| **UI Library** | Custom CSS | Brand control, performance | Tailwind, shadcn |
| **Database** | ${needsBackend ? 'PostgreSQL (Supabase)' : 'localStorage only'} | ${needsBackend ? 'Reliable, type-safe' : 'No server needed'} | ${needsBackend ? 'MongoDB, Firebase' : 'IndexedDB'} |
| **Hosting** | Vercel | Zero-config, global CDN | Netlify, Cloudflare |
| **CI/CD** | GitHub Actions | Free, integrated | GitLab CI, CircleCI |
| **Monitoring** | Vercel + Sentry | Built-in, error tracking | DataDog, New Relic |
| **Auth** | ${needsAuth ? 'NextAuth.js' : 'None (local-only)'} | ${needsAuth ? 'Standard, secure' : 'Privacy-first'} | ${needsAuth ? 'Auth0, Clerk' : 'N/A'} |

---

## Cost Estimate (Monthly)

**MVP (Local-Only)**:
- Hosting: $0 (Vercel free tier)
- Database: $0 (localStorage)
- Monitoring: $0 (free tiers)
- **Total: $0/month** for up to 10,000 users

**With Backend (Optional)**:
- Hosting: $0 (Vercel Hobby)
- Database: $0 (Supabase free tier, 500MB)
- Monitoring: $0 (Sentry free tier)
- **Total: $0/month** until ~100,000 page views

**At Scale (1M+ users)**:
- Hosting: ~$200/month (Vercel Pro)
- Database: ~$50/month (Supabase Pro)
- Monitoring: ~$30/month (Sentry Team)
- **Total: ~$280/month**

---

## Tech Debt & Maintenance

### Upgrade Path
- **Phase 1 (MVP)**: Local-only, custom CSS, Context API
- **Phase 2 (Growth)**: Add backend, cloud sync, Zustand
- **Phase 3 (Scale)**: Migrate to monorepo, microservices if needed

### Dependency Management
- **Updates**: Weekly \`npm audit\` + \`npm outdated\`
- **Major Versions**: Test in preview deploys before merging
- **Security**: Auto-merge Dependabot patches

### Code Quality
- **Linting**: ESLint (Airbnb rules + custom)
- **Formatting**: Prettier (auto-format on save)
- **Type Safety**: TypeScript strict mode
- **Testing**: Visual QA (Playwright) + unit tests (Vitest)

---

## References

**Documentation**:
- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev)
- [Vercel Platform](https://vercel.com/docs)
${needsBackend ? '- [Supabase Docs](https://supabase.com/docs)' : ''}
- [Web.dev Performance](https://web.dev/performance/)

**PRD Cross-References**:
- See \`prd/01-personas.md\` for user needs driving tech choices
- See \`prd/03-acceptance-criteria.md\` for performance requirements
`;
}

// ============================================================================
// 2. SERVICE/MODULE MAP
// ============================================================================

function generateServices(requirements) {
    const appName = requirements.app_name;
    const features = requirements.features?.must_have || [];

    const needsBackend = features.some(f =>
        f.toLowerCase().includes('sync') ||
        f.toLowerCase().includes('share')
    );

    return `# Service & Module Architecture

## System Overview

${appName} follows a **${needsBackend ? 'client-server' : 'client-only'}** architecture with emphasis on **local-first data** and **progressive enhancement**.

## Architecture Diagram

\`\`\`mermaid
graph TB
    subgraph "Client (Browser)"
        UI[React UI Components]
        State[State Management<br/>Context + localStorage]
        Storage[IndexedDB / localStorage]

        UI --> State
        State --> Storage
    end

    ${needsBackend ? `
    subgraph "Backend (Optional)"
        API[Next.js API Routes]
        DB[(PostgreSQL<br/>Supabase)]
        Auth[NextAuth.js]

        API --> DB
        API --> Auth
    end

    State -.Sync.-> API
    ` : ''}

    subgraph "External Services"
        CDN[Vercel CDN]
        Monitor[Sentry Error Tracking]
        Analytics[Vercel Analytics]
    end

    UI --> CDN
    UI -.Errors.-> Monitor
    UI -.Metrics.-> Analytics

    style UI fill:#4285F4,stroke:#333,color:#fff
    style State fill:#34A853,stroke:#333,color:#fff
    style Storage fill:#FBBC04,stroke:#333,color:#000
    ${needsBackend ? 'style API fill:#EA4335,stroke:#333,color:#fff' : ''}
\`\`\`

---

## Module Breakdown

### Frontend Modules

#### 1. UI Layer
**Path**: \`src/components/\`

**Responsibilities**:
- Render user interface
- Handle user interactions
- Display data from state

**Sub-modules**:
\`\`\`
src/components/
├── screens/           # Full-screen views
│   ├── DashboardScreen.tsx
│   ├── LogEntryScreen.tsx
│   ├── HistoryScreen.tsx
│   ├── AnalyticsScreen.tsx
│   └── SettingsScreen.tsx
├── ui/                # Reusable components
│   ├── PillButton.tsx
│   ├── MetricCard.tsx
│   ├── ProgressBar.tsx
│   ├── Input.tsx
│   └── Navigation.tsx
└── layout/            # Layout components
    ├── AppHeader.tsx
    ├── AppFooter.tsx
    └── AppLayout.tsx
\`\`\`

**Key Patterns**:
- **Screen Components**: Full pages, receive data from Context
- **UI Components**: Reusable, accept props, no state
- **Layout Components**: Wrapper/structure, provide navigation

**Dependencies**:
- React 18+ (hooks, suspense)
- CSS Modules (scoped styles)

---

#### 2. State Management Layer
**Path**: \`src/context/\`

**Responsibilities**:
- Manage application state
- Sync with localStorage
- Provide data to UI components

**Modules**:
\`\`\`typescript
// src/context/DataContext.tsx
interface DataContextType {
  entries: Entry[];
  goals: Goal[];
  addEntry: (entry: Omit<Entry, 'id'>) => void;
  updateGoal: (goal: Goal) => void;
  deleteEntry: (id: string) => void;
  exportData: () => string;
  importData: (json: string) => void;
}

// State lifecycle:
// 1. Load from localStorage on mount
// 2. Update state via Context methods
// 3. Auto-save to localStorage on change
// 4. Optional: sync to backend
\`\`\`

**Storage Strategy**:
- **Primary**: localStorage (5MB limit, sync API)
- **Fallback**: sessionStorage (temporary)
- **Future**: IndexedDB (unlimited, async API)

**Dependencies**:
- React Context API
- localStorage API (native)

---

#### 3. Data Persistence Layer
**Path**: \`src/lib/storage.ts\`

**Responsibilities**:
- Abstract storage implementation
- Handle serialization/deserialization
- Manage migrations

**Interface**:
\`\`\`typescript
interface StorageAdapter {
  get<T>(key: string): T | null;
  set<T>(key: string, value: T): void;
  remove(key: string): void;
  clear(): void;
  keys(): string[];
}

class LocalStorageAdapter implements StorageAdapter {
  // Implementation using localStorage
}

class IndexedDBAdapter implements StorageAdapter {
  // Future: Implementation using IndexedDB
}
\`\`\`

**Migration System**:
\`\`\`typescript
// Versioned schema for upgrades
const SCHEMA_VERSION = 1;

interface StorageSchema_V1 {
  version: 1;
  entries: Entry[];
  goals: Goal[];
}

// Migration functions
const migrations = {
  0: (data: any) => ({ version: 1, ...data }),
  // Future: 1: (data) => migrate_v1_to_v2(data)
};
\`\`\`

---

${needsBackend ? `
### Backend Modules

#### 4. API Layer
**Path**: \`src/app/api/\`

**Responsibilities**:
- Handle HTTP requests
- Validate input
- Orchestrate business logic
- Return responses

**Endpoints**:
\`\`\`
src/app/api/
├── sync/
│   └── route.ts          # POST /api/sync - Sync local → cloud
├── export/
│   └── route.ts          # GET /api/export - Export data
├── auth/
│   ├── [...nextauth]/
│   │   └── route.ts      # NextAuth.js handlers
│   └── signup/
│       └── route.ts      # POST /api/auth/signup
└── healthz/
    └── route.ts          # GET /api/healthz - Health check
\`\`\`

**Request Flow**:
\`\`\`
Client Request
  ↓
Middleware (auth, rate limit)
  ↓
Route Handler (validation)
  ↓
Business Logic (data processing)
  ↓
Database Query (Prisma)
  ↓
Response (JSON)
\`\`\`

---

#### 5. Database Layer
**Path**: \`prisma/schema.prisma\`

**Responsibilities**:
- Define data models
- Manage migrations
- Provide type-safe queries

**ORM**: Prisma (TypeScript)

**Schema**: See \`architecture-data-model.md\` for full schema

---

#### 6. Authentication Module
**Path**: \`src/lib/auth.ts\`

**Responsibilities**:
- User authentication
- Session management
- Authorization checks

**Implementation**: NextAuth.js

**Flow**:
\`\`\`
User submits credentials
  ↓
NextAuth.js validates
  ↓
Create session (JWT)
  ↓
Store in cookie (httpOnly, secure)
  ↓
Middleware checks on API requests
\`\`\`
` : ''}

---

## Data Flow Diagrams

### Core Feature: ${features[0] || 'Log Entry'}

\`\`\`mermaid
sequenceDiagram
    participant User
    participant UI as UI Component
    participant State as Context State
    participant Storage as localStorage
    ${needsBackend ? 'participant API as Backend API\n    participant DB as Database' : ''}

    User->>UI: Click "Log Entry"
    UI->>UI: Show input form
    User->>UI: Enter data + submit
    UI->>State: addEntry(data)
    State->>State: Validate data
    State->>Storage: Save to localStorage
    Storage-->>State: Success
    State-->>UI: Update UI (optimistic)
    UI->>User: Show success + updated stats

    ${needsBackend ? `
    Note over State,API: Optional cloud sync
    State->>API: POST /api/sync (background)
    API->>DB: INSERT entry
    DB-->>API: Confirm
    API-->>State: Sync complete
    ` : ''}
\`\`\`

---

### Error Handling Flow

\`\`\`mermaid
graph TD
    A[User Action] --> B{Input Valid?}
    B -->|No| C[Show Validation Error]
    B -->|Yes| D{Storage Available?}
    D -->|No| E[Show Offline Warning]
    D -->|Yes| F[Save Data]
    F --> G{Save Successful?}
    G -->|No| H[Log Error to Sentry]
    G -->|Yes| I[Update UI]
    H --> J[Show Generic Error]
    ${needsBackend ? `
    I --> K{Backend Sync?}
    K -->|Yes| L{Sync Success?}
    L -->|No| M[Queue for Retry]
    L -->|Yes| N[Mark Synced]
    ` : ''}

    style C fill:#EA4335,color:#fff
    style E fill:#FBBC04,color:#000
    style H fill:#EA4335,color:#fff
    style J fill:#EA4335,color:#fff
\`\`\`

---

## Module Dependencies

\`\`\`mermaid
graph LR
    UI[UI Components] --> State[State Management]
    State --> Storage[Storage Layer]
    ${needsBackend ? 'State -.Optional.-> API[API Client]' : ''}
    ${needsBackend ? 'API --> Backend[Backend Services]' : ''}

    UI --> Theme[Theme/Styles]
    UI --> Utils[Utility Functions]

    ${needsBackend ? 'Backend --> Database[(Database)]' : ''}
    ${needsBackend ? 'Backend --> Auth[Auth Service]' : ''}

    External[External Services] -.Monitor.-> UI
    External -.Monitor.-> ${needsBackend ? 'Backend' : 'UI'}

    style UI fill:#4285F4,color:#fff
    style State fill:#34A853,color:#fff
    style Storage fill:#FBBC04,color:#000
    ${needsBackend ? 'style Backend fill:#EA4335,color:#fff' : ''}
\`\`\`

---

## Cross-Cutting Concerns

### Error Handling
**Strategy**: Defensive programming + graceful degradation

**Layers**:
1. **UI**: Try-catch around user interactions
2. **State**: Validate all data before storage
3. **Storage**: Fallback to sessionStorage if localStorage full
4. **${needsBackend ? 'API' : 'N/A'}**: ${needsBackend ? 'Rate limiting, input validation, error responses' : 'Not applicable'}

**Error Reporting**:
- **Development**: Console errors + React Error Boundaries
- **Production**: Sentry (batched, sampled)

---

### Logging
**Strategy**: Structured logging with levels

**Levels**:
- \`ERROR\`: Exceptions, failed operations
- \`WARN\`: Degraded functionality, missing features
- \`INFO\`: User actions, lifecycle events
- \`DEBUG\`: Development only

**Implementation**:
\`\`\`typescript
const logger = {
  error: (msg: string, meta?: object) => {
    console.error(msg, meta);
    if (isProd) sentry.captureException(new Error(msg));
  },
  warn: (msg: string) => console.warn(msg),
  info: (msg: string) => console.log(msg),
  debug: (msg: string) => !isProd && console.debug(msg),
};
\`\`\`

---

### Testing Strategy
**Approach**: Visual QA + Unit Tests

**Test Pyramid**:
\`\`\`
           /\\
          /  \\  Manual Testing (smoke tests)
         /____\\
        / E2E  \\  Visual QA (Playwright) - 9 scenarios
       /________\\
      / Integ.  \\  Component Testing - Key flows
     /__________\\
    /   Unit     \\  Pure Functions - Utils, validators
   /______________\\
\`\`\`

**Tools**:
- **Visual QA**: Playwright (already integrated)
- **Unit**: Vitest (fast, ESM-native)
- **E2E**: Playwright (full user flows)

---

## Scalability Considerations

### Performance Targets
- **Initial Load**: < 2s (3G network)
- **Entry Creation**: < 100ms (localStorage write)
- **Data Export**: < 500ms (serialize to JSON)
- **${needsBackend ? 'API Response' : 'N/A'}**: ${needsBackend ? '< 200ms (p95)' : 'Not applicable'}

### Capacity Planning
**Local Storage**:
- Average entry size: ~100 bytes
- 5MB limit = ~50,000 entries
- Sufficient for 10+ years of daily tracking

${needsBackend ? `
**Backend (Future)**:
- Database: PostgreSQL handles 10M+ rows easily
- API: Serverless scales automatically (Vercel)
- Rate Limit: 100 requests/min per user
` : ''}

### Bottlenecks & Mitigations
| Bottleneck | Impact | Mitigation |
|------------|--------|------------|
| localStorage full | Cannot save new entries | Migrate to IndexedDB (unlimited) |
| Slow render | Laggy UI | Virtualize long lists, memo components |
| ${needsBackend ? 'API rate limits' : 'N/A'} | ${needsBackend ? 'Sync failures' : 'N/A'} | ${needsBackend ? 'Queue + exponential backoff' : 'N/A'} |
| Bundle size | Slow initial load | Code splitting, lazy loading |

---

## Security Architecture

### Threat Model
**Attack Vectors**:
1. **XSS**: Malicious scripts in user input
2. **CSRF**: Forged requests ${needsBackend ? '(API)' : '(N/A - local-only)'}
3. **Data Loss**: localStorage cleared/corrupted
4. **${needsBackend ? 'SQL Injection' : 'N/A'}**: ${needsBackend ? 'Malicious queries' : 'Not applicable'}

**Mitigations**:
1. **XSS**: React auto-escapes, CSP headers
2. **CSRF**: ${needsBackend ? 'SameSite cookies, CSRF tokens' : 'Not applicable'}
3. **Data Loss**: Export feature, backups encouraged
4. **${needsBackend ? 'SQL Injection' : 'N/A'}**: ${needsBackend ? 'Prisma (parameterized queries)' : 'Not applicable'}

### Defense in Depth
\`\`\`
User Input
  ↓
[Client Validation] ← TypeScript types
  ↓
[React XSS Protection] ← Auto-escaping
  ↓
${needsBackend ? '[API Validation] ← Zod schemas' : '[localStorage] ← Sanitized'}
  ↓
${needsBackend ? '[ORM Protection] ← Prisma' : '[Render] ← React'}
  ↓
${needsBackend ? '[Database]' : '[Display]'}
\`\`\`

---

## Module Ownership (Future)

As team grows, suggest ownership model:

| Module | Owner | Backup |
|--------|-------|--------|
| UI Components | Frontend Lead | Designer |
| State Management | Frontend Lead | Backend Lead |
| API Layer | Backend Lead | DevOps |
| Database | Backend Lead | DBA (if hired) |
| DevOps/Deploy | DevOps Lead | Backend Lead |
| Security | Security Lead | All |

**For MVP**: Single developer owns all modules

---

## References

**Architecture Patterns**:
- [Local-First Software](https://www.inkandswitch.com/local-first/)
- [React Architecture](https://react.dev/learn/thinking-in-react)
- [Next.js App Router](https://nextjs.org/docs/app)

**PRD Cross-References**:
- See \`prd/03-acceptance-criteria.md\` for feature requirements
- See \`architecture-data-model.md\` for schema details
- See \`architecture-api.md\` for endpoint specs
`;
}

// ============================================================================
// 3. DATA MODEL
// ============================================================================

function generateDataModel(requirements) {
    const appName = requirements.app_name;
    const features = requirements.features?.must_have || [];

    // Infer entities from features
    const entities = [];

    // Always have Entry and Goal for tracking apps
    if (requirements.app_type === 'health_tracking' ||
        features.some(f => f.toLowerCase().includes('track') || f.toLowerCase().includes('log'))) {
        entities.push('Entry', 'Goal');
    }

    if (features.some(f => f.toLowerCase().includes('user') || f.toLowerCase().includes('account'))) {
        entities.push('User');
    }

    return `# Data Model Architecture

## Entity Overview

${appName} uses a **simple, normalized schema** optimized for local storage with optional cloud sync capability.

**Core Entities**:
${entities.map(e => `- **${e}**: ${getEntityDescription(e)}`).join('\n')}

---

## Entity Definitions

### Entry

**Purpose**: Represents a single tracking event (e.g., water logged, workout completed)

**Schema**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| \`id\` | UUID | Yes | Unique identifier (client-generated) |
| \`timestamp\` | DateTime | Yes | When entry was created (ISO 8601) |
| \`value\` | Number | Yes | Tracked value (e.g., 250ml water, 30min exercise) |
| \`unit\` | String | Yes | Unit of measurement ('ml', 'min', 'reps') |
| \`notes\` | String | No | Optional user notes (max 500 chars) |
| \`goalId\` | UUID | No | Associated goal (foreign key) |
| \`createdAt\` | DateTime | Yes | Record creation timestamp |
| \`updatedAt\` | DateTime | Yes | Last modification timestamp |
| \`syncedAt\` | DateTime | No | Last cloud sync timestamp (if backend exists) |

**TypeScript Interface**:
\`\`\`typescript
interface Entry {
  id: string;                    // UUID v4
  timestamp: Date;               // ISO 8601 string
  value: number;                 // Positive number
  unit: 'ml' | 'min' | 'reps';  // Enum
  notes?: string;                // Optional, max 500 chars
  goalId?: string;               // UUID v4 (nullable)
  createdAt: Date;
  updatedAt: Date;
  syncedAt?: Date;               // Nullable
}
\`\`\`

**Validation Rules**:
- \`id\`: Must be valid UUID v4
- \`value\`: Must be positive number, max 100,000
- \`notes\`: Max 500 characters, sanitized for XSS
- \`timestamp\`: Cannot be in future

**Prisma Schema** (if backend added):
\`\`\`prisma
model Entry {
  id        String   @id @default(uuid())
  timestamp DateTime
  value     Float
  unit      String
  notes     String?  @db.VarChar(500)
  goalId    String?
  goal      Goal?    @relation(fields: [goalId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  syncedAt  DateTime?

  @@index([timestamp])
  @@index([goalId])
}
\`\`\`

**Indexes**:
- \`timestamp\`: For chronological queries (history view)
- \`goalId\`: For goal-specific filtering

---

### Goal

**Purpose**: User-defined targets for tracking

**Schema**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| \`id\` | UUID | Yes | Unique identifier |
| \`name\` | String | Yes | Goal name (e.g., "Daily Water Intake") |
| \`target\` | Number | Yes | Target value (e.g., 2000ml) |
| \`unit\` | String | Yes | Same units as entries |
| \`frequency\` | String | Yes | 'daily', 'weekly', 'monthly' |
| \`startDate\` | Date | Yes | When goal begins |
| \`endDate\` | Date | No | Optional end date (null = ongoing) |
| \`active\` | Boolean | Yes | Whether goal is currently active |
| \`createdAt\` | DateTime | Yes | Record creation |
| \`updatedAt\` | DateTime | Yes | Last modification |

**TypeScript Interface**:
\`\`\`typescript
interface Goal {
  id: string;
  name: string;                           // Max 100 chars
  target: number;                         // Positive number
  unit: 'ml' | 'min' | 'reps';
  frequency: 'daily' | 'weekly' | 'monthly';
  startDate: Date;
  endDate?: Date;                         // Nullable
  active: boolean;
  createdAt: Date;
  updatedAt: Date;
}
\`\`\`

**Validation Rules**:
- \`name\`: 1-100 characters, non-empty
- \`target\`: Positive number, max 1,000,000
- \`endDate\`: Must be after \`startDate\` if set

**Prisma Schema** (if backend added):
\`\`\`prisma
model Goal {
  id        String   @id @default(uuid())
  name      String   @db.VarChar(100)
  target    Float
  unit      String
  frequency String
  startDate DateTime
  endDate   DateTime?
  active    Boolean  @default(true)
  entries   Entry[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([active])
}
\`\`\`

---

${entities.includes('User') ? `
### User

**Purpose**: User account for cloud sync (optional)

**Schema**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| \`id\` | UUID | Yes | Unique identifier |
| \`email\` | String | Yes | Email address (unique) |
| \`passwordHash\` | String | Yes | Bcrypt hash (never stored in plain text) |
| \`name\` | String | No | Display name |
| \`emailVerified\` | DateTime | No | Email verification timestamp |
| \`createdAt\` | DateTime | Yes | Account creation |
| \`updatedAt\` | DateTime | Yes | Last profile update |

**TypeScript Interface**:
\`\`\`typescript
interface User {
  id: string;
  email: string;                // Unique, validated
  passwordHash: string;         // Never exposed to client
  name?: string;
  emailVerified?: Date;
  createdAt: Date;
  updatedAt: Date;
}
\`\`\`

**Security**:
- Passwords hashed with bcrypt (cost factor 12)
- Email validation before account creation
- Email verification required for sync

**Prisma Schema**:
\`\`\`prisma
model User {
  id            String    @id @default(uuid())
  email         String    @unique
  passwordHash  String
  name          String?
  emailVerified DateTime?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  @@index([email])
}
\`\`\`
` : ''}

---

## Entity Relationships

${entities.includes('Entry') && entities.includes('Goal') ? `
\`\`\`mermaid
erDiagram
    GOAL ||--o{ ENTRY : "tracks"
    ${entities.includes('User') ? 'USER ||--o{ GOAL : "creates"\n    USER ||--o{ ENTRY : "owns"' : ''}

    GOAL {
        uuid id PK
        string name
        number target
        string unit
        string frequency
        date startDate
        date endDate
        boolean active
    }

    ENTRY {
        uuid id PK
        datetime timestamp
        number value
        string unit
        string notes
        uuid goalId FK
        datetime syncedAt
    }

    ${entities.includes('User') ? `
    USER {
        uuid id PK
        string email UK
        string passwordHash
        string name
        datetime emailVerified
    }
    ` : ''}
\`\`\`

**Relationship Rules**:
- One Goal can have many Entries (one-to-many)
- One Entry belongs to zero or one Goal (optional)
${entities.includes('User') ? '- One User can have many Goals and Entries (one-to-many)' : ''}
- Deleting a Goal does NOT delete its Entries (orphan handling)
` : ''}

---

## Storage Strategy

### Local Storage Schema
**Key**: \`${appName.toLowerCase()}-data\`

**Value**: JSON-serialized object
\`\`\`typescript
interface LocalStorageSchema {
  version: number;              // Schema version for migrations
  entries: Entry[];             // Array of all entries
  goals: Goal[];                // Array of all goals
  preferences: {                // User preferences
    theme: 'light' | 'dark';
    notifications: boolean;
    exportReminder: boolean;
  };
  lastExport?: Date;            // Last data export timestamp
  lastSync?: Date;              // Last cloud sync (if applicable)
}
\`\`\`

**Size Estimate**:
- Average entry: ~150 bytes
- Average goal: ~100 bytes
- 365 entries/year × 10 years = ~540 KB
- Well within 5MB localStorage limit

---

### IndexedDB Schema (Future Migration)
**Database**: \`${appName}DB\`

**Object Stores**:
\`\`\`typescript
// Entries store
{
  name: 'entries',
  keyPath: 'id',
  indexes: [
    { name: 'timestamp', keyPath: 'timestamp' },
    { name: 'goalId', keyPath: 'goalId' }
  ]
}

// Goals store
{
  name: 'goals',
  keyPath: 'id',
  indexes: [
    { name: 'active', keyPath: 'active' }
  ]
}
\`\`\`

**Migration Trigger**: When localStorage approaches 4MB (80% capacity)

---

## Data Integrity

### Validation
**Client-Side** (TypeScript + Zod):
\`\`\`typescript
import { z } from 'zod';

const EntrySchema = z.object({
  id: z.string().uuid(),
  timestamp: z.date().max(new Date()),
  value: z.number().positive().max(100000),
  unit: z.enum(['ml', 'min', 'reps']),
  notes: z.string().max(500).optional(),
  goalId: z.string().uuid().optional(),
});

// Validate before saving
const entry = EntrySchema.parse(userInput);
\`\`\`

**Server-Side** (if backend exists):
- Same Zod schemas
- Database constraints (Prisma)
- Rate limiting on mutations

---

### Backup & Recovery
**Export Format**: JSON
\`\`\`json
{
  "version": 1,
  "exportedAt": "2025-10-24T12:00:00Z",
  "entries": [...],
  "goals": [...],
  "checksum": "sha256-hash-of-data"
}
\`\`\`

**Import Process**:
1. Validate JSON structure
2. Check schema version
3. Verify checksum
4. Merge or replace existing data (user choice)
5. Confirm success

---

## Performance Optimization

### Query Patterns
**Common Queries**:
1. Get recent entries (last 7 days)
2. Get entries for specific goal
3. Calculate progress toward goal
4. Export all data

**Optimization**:
- Keep entries sorted by timestamp in memory
- Cache goal progress calculations
- Lazy-load old entries (only show recent by default)

### Caching Strategy
\`\`\`typescript
// Cache calculated values
const cache = {
  todayProgress: null as number | null,
  weekStats: null as Stats | null,
  lastCalculated: null as Date | null,
};

// Invalidate on new entry
function addEntry(entry: Entry) {
  entries.push(entry);
  cache.todayProgress = null;  // Recalculate
  cache.weekStats = null;
  saveToStorage(entries);
}
\`\`\`

---

## Migration Strategy

### Schema Versioning
\`\`\`typescript
const migrations = {
  0: (data: any) => {
    // Initial schema (no migration needed)
    return { version: 1, ...data };
  },
  1: (data: SchemaV1) => {
    // Example: Add 'unit' field to old entries
    return {
      version: 2,
      entries: data.entries.map(e => ({ ...e, unit: 'ml' })),
      goals: data.goals,
    };
  },
};

function loadData(): LocalStorageSchema {
  const raw = localStorage.getItem('${appName.toLowerCase()}-data');
  if (!raw) return initialSchema;

  let data = JSON.parse(raw);
  const currentVersion = data.version || 0;
  const targetVersion = Object.keys(migrations).length;

  // Run migrations sequentially
  for (let v = currentVersion; v < targetVersion; v++) {
    data = migrations[v](data);
  }

  return data;
}
\`\`\`

---

## Data Privacy & Compliance

### GDPR Compliance
- **Right to Access**: Export data as JSON (one-click)
- **Right to Erasure**: "Delete All Data" button (irreversible)
- **Data Portability**: Standard JSON format
- **Data Minimization**: Only collect what's needed

### Data Retention
**Local Storage**:
- Data persists until user clears browser or deletes app
- No automatic deletion

**Cloud Sync** (if backend):
- Inactive accounts deleted after 2 years
- User can request deletion anytime
- 30-day soft delete (recovery window)

---

## References

**Data Modeling**:
- [Database Normalization](https://en.wikipedia.org/wiki/Database_normalization)
- [Prisma Best Practices](https://www.prisma.io/docs/guides/performance-and-optimization)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)

**PRD Cross-References**:
- See \`prd/03-acceptance-criteria.md\` for data requirements
- See \`architecture-api.md\` for API data contracts
`;
}

function getEntityDescription(entity) {
    const descriptions = {
        'Entry': 'Individual tracking record (e.g., 250ml water logged at 2pm)',
        'Goal': 'User-defined target (e.g., drink 2L water daily)',
        'User': 'Account for cloud sync and multi-device access',
        'Setting': 'User preferences and configuration',
    };
    return descriptions[entity] || 'Application entity';
}

// ============================================================================
// GENERATE ALL DOCUMENTS
// ============================================================================

console.log('📄 Generating tech stack...');
const techStackDoc = generateTechStack(requirements);
fs.writeFileSync(path.join(outputDir, 'architecture-tech-stack.md'), techStackDoc);
console.log('   ✅ architecture-tech-stack.md');

console.log('📄 Generating service map...');
const servicesDoc = generateServices(requirements);
fs.writeFileSync(path.join(outputDir, 'architecture-services.md'), servicesDoc);
console.log('   ✅ architecture-services.md');

console.log('📄 Generating data model...');
const dataModelDoc = generateDataModel(requirements);
fs.writeFileSync(path.join(outputDir, 'architecture-data-model.md'), dataModelDoc);
console.log('   ✅ architecture-data-model.md');

console.log('\n✅ Architecture documentation generated!');
console.log(`📂 Output: ${outputDir}/`);
console.log('\nNext steps:');
console.log('  1. Review architecture decisions with team');
console.log('  2. Generate API specs: node scripts/generate-api-spec.js');
console.log('  3. Generate deployment docs: node scripts/generate-deployment.js');

process.exit(0);
