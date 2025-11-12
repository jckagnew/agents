# Web Deployment Guide - Factory Admin

**Factory Admin Dashboard**
**Framework**: Next.js 14
**Date**: 2025-11-12

---

## Overview

The Factory Admin is a Next.js 14 web application for managing software factory projects, health alerts, and capability launches. It's designed to be deployed as a static site or with SSR depending on your needs.

**Key Features**:
- Dashboard with project metrics
- Project registry with CRUD operations
- Health alert monitoring
- Splash creator integration
- Design token editing

---

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Hosting platform account (Vercel recommended for Next.js)

---

## Local Development

### 1. Install Dependencies

```bash
cd software-factory/admin
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 3. Development Features

- **Hot Reload**: Changes automatically refresh
- **Fast Refresh**: React state preserved across edits
- **TypeScript**: Full type checking
- **ESLint**: Code quality enforcement

---

## Production Build

### Option 1: Static Export (Recommended for Simple Hosting)

```bash
# Build static site
npm run build
npm run export

# Output in /out directory
ls -la out/
```

**Use case**: Host on CDN, S3, Netlify, or any static hosting

### Option 2: Server-Side Rendering (SSR)

```bash
# Build with SSR support
npm run build

# Start production server
npm run start
```

**Use case**: Dynamic routes, API routes, server-side data fetching

---

## Deployment Options

### Option 1: Vercel (Recommended for Next.js)

**Why Vercel?**
- Built by Next.js creators
- Zero-config deployments
- Automatic HTTPS and CDN
- Free tier available

**Step-by-Step**:

#### 1. Install Vercel CLI

```bash
npm install -g vercel
```

#### 2. Deploy

```bash
cd software-factory/admin
vercel
```

Follow prompts:
- Login to Vercel
- Link to project (or create new)
- Confirm settings

#### 3. Production Deployment

```bash
vercel --prod
```

#### 4. Configure Environment Variables (if needed)

```bash
# Add environment variables
vercel env add API_URL production
vercel env add NEXT_PUBLIC_FACTORY_API production
```

#### 5. Custom Domain

In Vercel Dashboard:
1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS (Vercel provides instructions)

**Result**: `https://factory-admin.yourdomain.com`

---

### Option 2: Netlify

**Step-by-Step**:

#### 1. Install Netlify CLI

```bash
npm install -g netlify-cli
```

#### 2. Build Configuration

Create `netlify.toml`:

```toml
[build]
  command = "npm run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

#### 3. Deploy

```bash
cd software-factory/admin
netlify init
netlify deploy --prod
```

#### 4. Environment Variables

In Netlify Dashboard:
- Site Settings → Build & Deploy → Environment
- Add variables

---

### Option 3: AWS Amplify

**Step-by-Step**:

#### 1. Install Amplify CLI

```bash
npm install -g @aws-amplify/cli
amplify configure
```

#### 2. Initialize Amplify

```bash
cd software-factory/admin
amplify init
```

#### 3. Add Hosting

```bash
amplify add hosting
# Select: Hosting with Amplify Console
# Select: Manual deployment
```

#### 4. Deploy

```bash
amplify publish
```

---

### Option 4: Self-Hosted (Docker)

#### 1. Create Dockerfile

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]
```

#### 2. Build and Run

```bash
# Build image
docker build -t factory-admin .

# Run container
docker run -p 3000:3000 factory-admin
```

#### 3. Deploy with Docker Compose

```yaml
version: '3.8'
services:
  factory-admin:
    build: ./software-factory/admin
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - API_URL=https://api.yourdomain.com
    restart: unless-stopped
```

---

## Environment Configuration

### Development Environment

Create `.env.local`:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FACTORY_DATA=/data

# Development flags
NEXT_PUBLIC_DEBUG=true
```

### Production Environment

**Vercel**:
```bash
vercel env add NEXT_PUBLIC_API_URL production
```

**Netlify**:
```bash
netlify env:set NEXT_PUBLIC_API_URL "https://api.yourdomain.com"
```

**Docker**:
```bash
docker run -e NEXT_PUBLIC_API_URL=https://api.yourdomain.com factory-admin
```

---

## Data Configuration

The Factory Admin reads from JSON data files:

### 1. Projects Data

Location: `software-factory/data/projects.json`

```json
{
  "projects": [
    {
      "id": "proj-001",
      "name": "Project Name",
      "status": "active",
      "created_at": "2025-01-15"
    }
  ]
}
```

### 2. Health Alerts

Location: `software-factory/data/health-alerts.json`

```json
{
  "alerts": [
    {
      "id": "alert-001",
      "severity": "warning",
      "message": "API latency increased",
      "timestamp": "2025-01-15T10:30:00Z"
    }
  ]
}
```

**Deployment Considerations**:
- Include data files in build (`next.config.js` → `publicRuntimeConfig`)
- Or fetch from API endpoint
- Or use CMS (Contentful, Sanity, etc.)

---

## Performance Optimization

### 1. Image Optimization

Next.js automatically optimizes images:

```tsx
import Image from 'next/image';

<Image
  src="/factory-logo.png"
  width={200}
  height={100}
  alt="Factory Logo"
  priority // Load immediately for above-the-fold images
/>
```

### 2. Code Splitting

Automatic with Next.js:
- Each page is a separate bundle
- Shared code extracted to common chunks

### 3. Static Generation

For mostly static content:

```tsx
// pages/projects.tsx
export async function getStaticProps() {
  const projects = await fetchProjects();
  return {
    props: { projects },
    revalidate: 60, // Revalidate every 60 seconds
  };
}
```

### 4. Caching Strategy

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};
```

---

## Security Considerations

### 1. Content Security Policy

```javascript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: "default-src 'self'; script-src 'self' 'unsafe-eval'; style-src 'self' 'unsafe-inline';",
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

### 2. Environment Variables

- Never commit `.env.local` to git
- Use `NEXT_PUBLIC_` prefix only for client-side variables
- Store secrets in hosting platform's environment settings

---

## Monitoring

### 1. Vercel Analytics

Automatically included on Vercel:
- View in Dashboard → Analytics
- Core Web Vitals tracking
- Real user monitoring

### 2. Error Tracking with Sentry

```bash
npm install @sentry/nextjs
```

```javascript
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

module.exports = withSentryConfig(
  {
    // Your Next.js config
  },
  {
    silent: true,
    org: 'your-org',
    project: 'factory-admin',
  }
);
```

### 3. Custom Monitoring

```typescript
// lib/monitoring.ts
export function trackEvent(event: string, data: any) {
  if (process.env.NODE_ENV === 'production') {
    fetch('/api/analytics', {
      method: 'POST',
      body: JSON.stringify({ event, data, timestamp: new Date() }),
    });
  }
}
```

---

## Continuous Deployment

### GitHub Actions (Vercel)

Create `.github/workflows/deploy-admin.yml`:

```yaml
name: Deploy Factory Admin

on:
  push:
    branches:
      - main
    paths:
      - 'software-factory/admin/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd software-factory/admin
          npm ci

      - name: Build
        run: |
          cd software-factory/admin
          npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./software-factory/admin
```

---

## Troubleshooting

### Issue 1: Build Fails with Type Errors

**Solution**:
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Fix type errors or temporarily disable strict mode
# In tsconfig.json: "strict": false
```

### Issue 2: Data Files Not Found in Production

**Solution**:
```javascript
// next.config.js
module.exports = {
  publicRuntimeConfig: {
    dataPath: process.env.DATA_PATH || './data',
  },
};
```

### Issue 3: Styles Not Loading

**Solution**:
```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  // Ensure CSS is properly configured
  experimental: {
    optimizeCss: true,
  },
};
```

---

## Testing Before Deployment

### 1. Build Locally

```bash
npm run build
npm run start

# Test at http://localhost:3000
```

### 2. Check Bundle Size

```bash
npm run build

# Review output:
# Page                              Size     First Load JS
# ┌ ○ /                            2.5 kB          85 kB
# └ ○ /projects                    3.1 kB          86 kB
```

### 3. Lighthouse Audit

```bash
# Install Lighthouse
npm install -g lighthouse

# Run audit
lighthouse http://localhost:3000 --view
```

**Target Scores**:
- Performance: >90
- Accessibility: >95
- Best Practices: >90
- SEO: >90

---

## Deployment Checklist

- [ ] Run `npm run build` locally and verify no errors
- [ ] Test all routes work correctly
- [ ] Verify data files are accessible
- [ ] Check responsive design on mobile/tablet/desktop
- [ ] Test in Chrome, Firefox, Safari, Edge
- [ ] Configure environment variables on hosting platform
- [ ] Set up custom domain and SSL
- [ ] Configure error tracking (Sentry)
- [ ] Set up monitoring and analytics
- [ ] Run Lighthouse audit (aim for >90 scores)
- [ ] Test authentication/authorization if applicable
- [ ] Verify API endpoints work in production
- [ ] Set up CI/CD pipeline (GitHub Actions)

---

## Cost Estimates

### Vercel
- **Hobby** (Free): Perfect for personal projects
- **Pro** ($20/month): Team collaboration, analytics
- **Enterprise**: Custom pricing

### Netlify
- **Starter** (Free): 100GB bandwidth
- **Pro** ($19/month): 1TB bandwidth
- **Business** ($99/month): SSO, advanced features

### AWS Amplify
- **Build minutes**: $0.01/minute
- **Hosting**: $0.15/GB served
- Typically $5-20/month for small apps

---

## Next Steps

1. Choose hosting platform (Vercel recommended)
2. Configure environment variables
3. Deploy using steps above
4. Set up custom domain
5. Configure monitoring and analytics
6. Set up CI/CD for automatic deployments
7. Monitor performance and errors

---

## Support

- **Next.js Docs**: https://nextjs.org/docs
- **Vercel Docs**: https://vercel.com/docs
- **Netlify Docs**: https://docs.netlify.com/

---

**Last Updated**: 2025-11-12
**Status**: ✅ Ready for Web Deployment
