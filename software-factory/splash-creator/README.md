# Splash Creator Web App

This Next.js application will power the interactive splash screen creator. It will:
- let users select a factory project and inherit its design tokens
- collect creative brief information and guidance assets
- orchestrate the existing Python-based agent workflow
- provide human-in-the-loop review and export of variants

## High-Level Structure

```
splash-creator/
├── app/
│   ├── (dashboard)/          # authenticated dashboard layout
│   ├── api/                  # Next API routes for orchestration
│   └── page.tsx              # landing / project picker
├── lib/                      # shared utilities (API clients, schema helpers)
├── components/               # UI components
├── public/                   # static assets
├── package.json
├── tsconfig.json
└── next.config.js
```

The initial scaffolding intentionally excludes third-party UI kits so we can integrate the existing design system once the API contracts are stable.

## Getting Started (future)

Once dependencies can be installed:
```
npm install
npm run dev
```

The development server will expose the interactive creator at `http://localhost:3000`.

### Interaction Flow

- The landing page now guides users through a four-step wizard: project selection → creative brief → guidance assets (placeholder) → review & launch.
- Validation gates (e.g., project required, headline/CTA required) prevent skipping ahead prematurely.
- Detailed sequence and state machine documented in [`docs/flow-overview.md`](docs/flow-overview.md).

## Health Alert Watchlist

The factory will surface dependency and integration risks through `/api/health-alerts`. Alerts are stored in `software-factory/data/health-alerts.json` and validated via `lib/schemas/health.ts`. The initial entry tracks the critical npm audit vulnerability discovered during splash creator verification. Later the admin UI can display this list and allow updates (status changes, remediation notes, next review dates).
