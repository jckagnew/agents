# Tech Stack Architecture

## Executive Summary

HydroTrack is a health tracking application prioritizing **simplicity, privacy, and performance**. Based on the PRD requirements, we recommend a **frontend-focused** architecture with local-first data storage and optional cloud sync.

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
- **Performance**: Sufficient for 3 core features
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
- **Brand Control**: Full control over design system (#2196F3)
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
```typescript
interface StorageSchema {
  entries: Entry[];           // Core tracking data
  goals: Goal[];              // User-defined targets
  preferences: UserPrefs;     // Settings
  lastSync?: Date;            // Optional cloud sync timestamp
}
```

**Migration Path**:
- **Phase 1**: localStorage (MVP, ~5MB limit)
- **Phase 2**: IndexedDB (unlimited, structured queries)
- **Phase 3**: Optional cloud sync (Firebase/Supabase)

---

## Backend Stack (Optional - Not Required for MVP)


**Decision**: **No backend required for MVP**

**Rationale**:
- All 3 must-have features work locally
- Privacy-first approach (no accounts needed)
- Faster development (ship in weeks, not months)
- Lower hosting costs ($0 vs $20-50/month)

**When to Add Backend**:
- User requests cloud sync
- Team collaboration features
- Analytics/insights beyond local
- Monetization (subscriptions)


---

## Infrastructure & Deployment

### Hosting
**Choice**: **Vercel** (frontend) 

**Rationale**:
- **Zero Config**: `git push` to deploy
- **Global CDN**: <100ms response times worldwide
- **Free Tier**: Sufficient for 1000+ users
- **DX**: Preview deploys, instant rollbacks

**Deployment Flow**:
```
main branch → Vercel Production (hydrotrack.vercel.app)
feature/* → Preview Deploys (pr-123.vercel.app)
```

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
```yaml
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
```

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
- API response times 
- User sessions (anonymous)

**Alerting**:
- Slack webhook for critical errors
- Email for deployment failures
- Weekly health reports

---

## Security & Compliance

### Authentication (Optional)

**Decision**: No authentication required for MVP (local-only app)


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
- **Rate Limiting**: API endpoints throttled (N/A)
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

- **AI Insights**: Claude API for personalized recommendations
- **Wearables**: Apple Health / Google Fit sync
- **Export**: CSV/PDF report generation


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

### Internationalization (Future)

**Decision**: English-only for MVP
- Add i18n when requested by users
- next-intl is drop-in compatible


---

## Technology Decision Matrix

| Concern | Choice | Rationale | Alternative |
|---------|--------|-----------|-------------|
| **Frontend Framework** | Next.js 14 | SSR, performance, DX | Remix, Vite |
| **State Management** | Context + localStorage | Simple, privacy-first | Zustand, Redux |
| **UI Library** | Custom CSS | Brand control, performance | Tailwind, shadcn |
| **Database** | localStorage only | No server needed | IndexedDB |
| **Hosting** | Vercel | Zero-config, global CDN | Netlify, Cloudflare |
| **CI/CD** | GitHub Actions | Free, integrated | GitLab CI, CircleCI |
| **Monitoring** | Vercel + Sentry | Built-in, error tracking | DataDog, New Relic |
| **Auth** | None (local-only) | Privacy-first | N/A |

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
- **Updates**: Weekly `npm audit` + `npm outdated`
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

- [Web.dev Performance](https://web.dev/performance/)

**PRD Cross-References**:
- See `prd/01-personas.md` for user needs driving tech choices
- See `prd/03-acceptance-criteria.md` for performance requirements
