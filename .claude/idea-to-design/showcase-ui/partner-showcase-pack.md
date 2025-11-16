# Partner Showcase UI – Briefing Pack

## 1. Opportunity Overview
- **Goal**: Provide prospective partners with a clear view of our agentic Software Factory + AI Studio capabilities.
- **Audience Personas**:
  - *Strategic Partner Lead*: needs rapid understanding of differentiation, proof points, and partnership value.
  - *Technical Due-Diligence Lead*: requires architecture transparency, security stance, and integration touch-points.
- **Success Criteria**:
  - Value proposition understood in < 60 seconds.
  - Workflow storytelling (Discovery → Production) reinforced with automation highlights.
  - Increase partnership conversations by 25% within 30 days of launch.

## 2. Product Requirements Snapshot
- Must-haves: workflow timeline, AI Studio outcomes, case studies/metrics, strong CTA.
- Nice-to-haves: interactive filtering, downloadable PDF, embedded media.
- Constraints: responsive (desktop/tablet/mobile), < 2s load time, WCAG AA compliance.

## 3. Architecture & UX Highlights
- **Tech Stack Recommendation**: Next.js 14 on Vercel, local-first content with optional Supabase/Headless CMS for case studies.
- **Service Layout**: Client-side SPA with optional API for contact form submissions.
- **Data Model**: Partner stories, workflow stages, metrics collections to power timeline + ROI sections.
- **UX Flow**: Hub-and-spoke navigation (Hero → Workflow → Proof → CTA). Accessibility guidelines emphasize semantic structure and keyboard navigation.
- **Compliance**: Respect-Spec audit score 110% (Architecture 115%, UX 105%).

## 4. Visual Direction
- **Mockup Variations Generated**: Safe (Option A), Bold (Option B), Balanced (Option C).
- **Recommended Variant**: **Option B – Bold & Innovative**
  - Hero: split layout with animated workflow timeline + headline copy.
  - Mid-section: AI Studio research cards with confidence/value badges.
  - Proof: carousel of case studies with metrics.
  - CTA: sticky footer contact button + scheduling link.
- **Visual QA**: Automated Playwright run blocked by local Chrome sandbox (Mach port error). Manual review required; rerun visual QA with Chrome path configured for final approval.

## 5. Deployment Readiness
- DevOps scaffold (Docker, docker-compose, env template, nginx, prometheus) generated under `devops/`.
- Deployment notes + summary prepared:
  - Staging: `partner-showcase-ui.vercel.app`
  - Production: `clevelsalesguy.com/partners`
  - Env vars documented (`NEXT_PUBLIC_APP_URL`, `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_ANALYTICS_ID`).

## 6. Open Items
| Item | Owner | Due |
|------|-------|-----|
| Finalize copy + partner metrics | Marketing | TBA |
| Visual QA rerun with Chrome path | Engineering | Before go-live |
| Contact/CTA destination confirmation | Partnerships | Before go-live |
| GA4 & conversion goals setup | Ops | At deployment |

## 7. Next Steps
1. Incorporate final content (copy, metrics, CTA links).
2. Run `npm run devops:up` for local verification and gather stakeholder feedback.
3. Execute visual QA with configured Chrome path or run headed mode.
4. Deploy preview via Vercel; collect partner feedback.
5. Launch on `clevelsalesguy.com/partners` once approvals complete.
