# Weight Tracker Web Design System Upgrade Plan

## Overview
- Align the React Native and Next.js experiences around the shared Google-inspired token source without blocking on full component parity.
- Deliver upgrades across three waves so QA can validate incrementally and catch regressions early.
- Keep documentation and visual artefacts updated to socialize the new design system across teams.

## Wave 1 – Shared Tokens & Theme (in progress)
Goal: Wire shared tokens into both platforms and ensure baseline typography and color alignment.

Action Items:
- [x] Shared token module lives in `design-system/googleTheme.ts` and remains the single source of truth for colors, typography, spacing, and components.
- [x] React Native theme re-exports shared tokens via `weight-tracker/src/theme/index.ts` (verified during this plan review).
- [x] Configure Next.js root styles to map shared tokens to CSS variables in `software-factory/generated-apps/weight-tracker-nextjs/src/app/globals.css`, set background color, and define default text colors.
- [x] Load Poppins and Nunito with `next/font/google` inside `software-factory/generated-apps/weight-tracker-nextjs/src/app/layout.tsx`, apply the generated classes to `<body>`, and expose fallbacks in CSS.
- [x] Publish usage notes describing how web components import `design-system/googleTheme` tokens and how React Native keeps parity through `weight-tracker/src/theme/index.ts`.

Definition of Done:
- Shared tokens drive both React Native and web typography, color, spacing, and radius defaults.
- The Next.js shell renders with the new fonts and background colors without cumulative layout shift or hydration warnings.
- Documented guidance exists so contributors know which files to touch for future token edits.
- Local linting and build commands succeed for both projects after the token wiring.

Dependencies:
- Confirm `@next/font` support in the current Next.js version.
- Ensure Tailwind or existing utility classes do not override the new CSS variables at runtime.
- Coordinate with QA on when to snapshot baseline screens for comparison.
- Verify Poppins and Nunito licences cover web embedding for the project.

## Wave 2 – Component Refresh
Goal: Modernize the web components using the shared design language while preserving functionality.

Action Items:
- [x] Restyle dashboard metric cards in `software-factory/generated-apps/weight-tracker-nextjs/src/components/DashboardScreen.tsx` using the pastel tints and `components.metricCard` token defaults.
- [x] Create reusable `MetricCard` and `PillButton` web components under `software-factory/generated-apps/weight-tracker-nextjs/src/components/design-system/` that pull from `design-system/googleTheme`.
- [x] Update navigation, log-entry, and analytics screens to use `components.button.primary` and `components.button.secondary` tokens plus shared spacing in their respective files.
- [x] Apply the chart palette (`chartPrimary`, `chartSecondary`, `chartArea`, `chartGoal`) to any charting elements in `software-factory/generated-apps/weight-tracker-nextjs/src/components/AnalyticsScreen.tsx` and align gradients with the React Native styling.
- [x] Review responsiveness and typography scaling across desktop and tablet breakpoints once the new fonts land.

Definition of Done:
- All primary web surfaces adopt shared token colors, typography, spacing, and radius values.
- Buttons and cards render consistently across dashboard, analytics, history, and log-entry screens.
- New reusable components reduce duplicate style objects and include inline usage examples or Storybook snippets.
- Design review signs off on the updated component spec and visual polish.

Dependencies:
- Completion of Wave 1 so fonts and CSS variables are available globally.
- Confirmation that the charting hooks can accept token values without additional transforms.
- Coordination with the React Native team to share screenshots ensuring parity.
- Fallback plan identified if gradients are not supported in the current chart placeholder implementation.

## Wave 3 – Validation & Docs
Goal: Validate visual updates, document the cross-platform system, and prepare review assets.

Action Items:
- [x] Run smoke or Playwright coverage focusing on navigation flows and critical dashboards after styling changes merge.
- [x] Update internal documentation to highlight that both platforms consume `design-system/googleTheme` as the shared source.
- [x] Capture annotated screenshots or a Loom walkthrough comparing before and after states for design review.
- [ ] Coordinate sign-off with design and product once validation artefacts are prepared.

Definition of Done:
- Automated and manual validation confirms no regressions in navigation, logging, or analytics flows.
- Documentation clearly references shared token ownership and update workflows.
- Review artefacts are distributed and approved ahead of release readiness.
- Release checklist reflects the new validation steps required for shared design changes.

Dependencies:
- Access to the latest staging environment data set for meaningful screenshots.
- Stable token API so documentation does not immediately churn.
- QA availability to execute regression checks within the wave timeline.
- Time reserved with stakeholders for review meetings and feedback.

## Open Questions
- Should Tailwind utility classes remain or be refactored to consume CSS variables for consistency?
- Do we need a theming toggle (light and dark) in scope or can it be deferred until after Wave 3?
- How should versioning of `design-system/googleTheme.ts` be handled if multiple apps consume it?
- Is a shared package (npm or workspace) required long term, or is relative importing sustainable?
