# Web Deployment Guide
**Admin Console - Design-First Software Factory**

**Date**: 2025-11-12
**Status**: ✅ Web Support Configured
**Expo SDK**: 54.0.22

---

## Overview

The Admin Console is built with **Expo** and **React Native**, which provides full web support through **Expo Web** (powered by React Native for Web). This means the same React Native codebase runs on iOS, Android, **and Web browsers** without code duplication.

This guide covers:
1. Local web development
2. Production web builds
3. Deployment to hosting platforms (Vercel, Netlify, AWS)
4. Environment configuration
5. CORS setup for production domains

---

## Prerequisites

Before deploying to the web, ensure you have:

- ✅ Node.js 18+ and npm/yarn installed
- ✅ Expo CLI installed (`npm install -g expo-cli`)
- ✅ Supabase project configured with correct CORS origins
- ✅ Production domain or hosting platform account

---

## Local Web Development

### 1. Install Dependencies

```bash
cd admin-console
npm install
```

### 2. Start Web Development Server

```bash
npm run web
# or
expo start --web
```

This will:
- Start Metro bundler
- Build web bundle with Webpack/Metro
- Open browser at `http://localhost:19006` (default Expo web port)

**Alternative ports:**
```bash
expo start --web --port 3000
# Opens at http://localhost:3000
```

### 3. Development Features

- **Hot Reload**: Changes automatically refresh in browser
- **Fast Refresh**: React state persists across updates
- **DevTools**: Use browser DevTools (F12) for debugging
- **Network Tab**: Inspect API calls to Supabase
- **Console**: View logs and errors

### 4. Testing Locally

Open browser and navigate to:
- **Primary**: `http://localhost:19006`
- **Alternate**: `http://localhost:3000`
- **Mobile Simulation**: Use Chrome DevTools responsive mode

**Test Authentication:**
```javascript
// Open browser console
console.log('Testing Supabase auth...');
// Should see Supabase client initialized
```

---

## Production Web Build

### 1. Configure Environment Variables

Create `.env.production` (or configure in hosting platform):

```bash
# Supabase Configuration
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Web-specific Configuration
EXPO_PUBLIC_WEB_URL=https://yourdomain.com
EXPO_PUBLIC_API_URL=https://your-project.supabase.co/functions/v1
```

**Security Note**: Never commit `.env.production` to Git. Add it to `.gitignore`.

### 2. Build for Production

Expo provides two build methods:

#### Option A: Expo Export (Static Site)

```bash
# Export static web bundle
npx expo export:web

# Output location
ls -la web-build/
# Creates: index.html, static assets, bundles
```

**Build Output:**
```
web-build/
├── index.html          # Entry point
├── static/
│   ├── js/             # JavaScript bundles
│   ├── css/            # Stylesheets
│   └── media/          # Images, fonts
├── manifest.json       # PWA manifest
└── favicon.png         # Favicon
```

#### Option B: EAS Build (Advanced)

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure EAS for web
eas build:configure

# Build for web
eas build --platform web --profile production
```

### 3. Optimize Build

**Enable Production Mode:**
- React optimizations (minification, tree-shaking)
- Source maps for debugging (optional)
- Asset optimization (images, fonts)

**Reduce Bundle Size:**
```bash
# Analyze bundle size
npx expo export:web --dump-assetmap

# Check bundle size
du -sh web-build/
```

**Expected Bundle Size:**
- Initial load: ~500KB-1MB (gzipped)
- Vendor bundle: ~300-400KB (React, React Native Web)
- App bundle: ~200-300KB (your code)

---

## Deployment Options

### Option 1: Vercel (Recommended)

**Why Vercel?**
- ✅ Automatic deployments from Git
- ✅ Global CDN
- ✅ Zero-config for Expo
- ✅ Free tier available
- ✅ Custom domains and SSL

**Step-by-Step:**

#### 1. Install Vercel CLI

```bash
npm install -g vercel
```

#### 2. Configure Vercel

Create `vercel.json` in `admin-console/`:

```json
{
  "version": 2,
  "name": "admin-console",
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "web-build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "EXPO_PUBLIC_SUPABASE_URL": "@supabase_url",
    "EXPO_PUBLIC_SUPABASE_ANON_KEY": "@supabase_anon_key"
  }
}
```

#### 3. Add Build Script

Update `package.json`:

```json
{
  "scripts": {
    "build": "expo export:web"
  }
}
```

#### 4. Deploy

```bash
# First deployment
vercel

# Production deployment
vercel --prod
```

**Set Environment Variables:**
```bash
vercel env add EXPO_PUBLIC_SUPABASE_URL production
vercel env add EXPO_PUBLIC_SUPABASE_ANON_KEY production
```

#### 5. Configure Custom Domain

```bash
vercel domains add yourdomain.com
```

**Update CORS:**
Add to `supabase/functions/_shared/cors.ts`:
```typescript
const ALLOWED_ORIGINS = [
  // ... existing origins
  'https://yourdomain.com',
  'https://admin-console.vercel.app',
];
```

---

### Option 2: Netlify

**Why Netlify?**
- ✅ Continuous deployment from Git
- ✅ Global CDN
- ✅ Form handling and serverless functions
- ✅ Free tier with SSL

**Step-by-Step:**

#### 1. Install Netlify CLI

```bash
npm install -g netlify-cli
```

#### 2. Configure Netlify

Create `netlify.toml` in `admin-console/`:

```toml
[build]
  command = "expo export:web"
  publish = "web-build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

#### 3. Deploy

```bash
# Login
netlify login

# Initialize site
netlify init

# Deploy
netlify deploy --prod
```

#### 4. Configure Environment Variables

In Netlify Dashboard:
1. Go to Site Settings → Build & Deploy → Environment
2. Add:
   - `EXPO_PUBLIC_SUPABASE_URL`
   - `EXPO_PUBLIC_SUPABASE_ANON_KEY`

#### 5. Update CORS

Add to `supabase/functions/_shared/cors.ts`:
```typescript
const ALLOWED_ORIGINS = [
  // ... existing origins
  'https://your-site.netlify.app',
  'https://yourdomain.com',
];
```

---

### Option 3: AWS S3 + CloudFront

**Why AWS?**
- ✅ Maximum control and customization
- ✅ Enterprise-grade scalability
- ✅ Integration with AWS services
- ✅ Cost-effective for high traffic

**Step-by-Step:**

#### 1. Build Static Site

```bash
npx expo export:web
```

#### 2. Create S3 Bucket

```bash
# Using AWS CLI
aws s3 mb s3://admin-console-web

# Enable static website hosting
aws s3 website s3://admin-console-web \
  --index-document index.html \
  --error-document index.html
```

#### 3. Upload Files

```bash
# Sync web-build to S3
aws s3 sync web-build/ s3://admin-console-web \
  --acl public-read \
  --cache-control "max-age=31536000,public" \
  --exclude "index.html"

# Upload index.html with short cache
aws s3 cp web-build/index.html s3://admin-console-web/index.html \
  --acl public-read \
  --cache-control "max-age=0,no-cache,no-store,must-revalidate"
```

#### 4. Create CloudFront Distribution

```bash
# Create distribution (use AWS Console or CLI)
aws cloudfront create-distribution \
  --origin-domain-name admin-console-web.s3.amazonaws.com \
  --default-root-object index.html
```

**CloudFront Configuration:**
- **Origin**: S3 bucket
- **Viewer Protocol Policy**: Redirect HTTP to HTTPS
- **Allowed HTTP Methods**: GET, HEAD, OPTIONS
- **Cache Policy**: CachingOptimized
- **Custom Error Response**: 404 → /index.html (for client-side routing)

#### 5. Configure Custom Domain

1. Add CNAME in Route 53 or your DNS provider
2. Add SSL certificate (AWS Certificate Manager)
3. Update CloudFront distribution with domain

#### 6. Update CORS

Add to `supabase/functions/_shared/cors.ts`:
```typescript
const ALLOWED_ORIGINS = [
  // ... existing origins
  'https://d111111abcdef8.cloudfront.net', // CloudFront domain
  'https://yourdomain.com',
];
```

---

## CORS Configuration for Production

### 1. Update Supabase CORS Whitelist

Edit `supabase/functions/_shared/cors.ts`:

```typescript
const ALLOWED_ORIGINS = [
  // Mobile development
  'http://localhost:8081',
  'exp://localhost:8081',

  // Web development
  'http://localhost:19006',
  'http://localhost:3000',
  'http://127.0.0.1:19006',
  'http://127.0.0.1:3000',

  // Production - Vercel
  'https://admin-console.vercel.app',
  'https://yourdomain.com',

  // Production - Netlify
  'https://your-site.netlify.app',

  // Production - AWS CloudFront
  'https://d111111abcdef8.cloudfront.net',

  // Production - Custom Domain
  'https://admin.yourdomain.com',
];
```

### 2. Deploy Updated CORS Configuration

```bash
cd supabase/functions
supabase functions deploy admin-customers
supabase functions deploy admin-projects
# Deploy all other Edge Functions
```

### 3. Test CORS

```bash
# Test from production domain
curl -X OPTIONS https://your-project.supabase.co/functions/v1/admin-customers \
  -H "Origin: https://yourdomain.com" \
  -v

# Should return:
# Access-Control-Allow-Origin: https://yourdomain.com
# Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
```

---

## Environment Variables

### Development Environment

Create `.env` in `admin-console/`:

```bash
# Supabase
EXPO_PUBLIC_SUPABASE_URL=http://localhost:54321
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-local-anon-key

# API
EXPO_PUBLIC_API_URL=http://localhost:54321/functions/v1
```

### Production Environment

**Option A: Vercel**
```bash
vercel env add EXPO_PUBLIC_SUPABASE_URL production
vercel env add EXPO_PUBLIC_SUPABASE_ANON_KEY production
```

**Option B: Netlify**
```bash
netlify env:set EXPO_PUBLIC_SUPABASE_URL "https://your-project.supabase.co"
netlify env:set EXPO_PUBLIC_SUPABASE_ANON_KEY "your-anon-key"
```

**Option C: AWS (use Systems Manager Parameter Store)**
```bash
aws ssm put-parameter \
  --name "/admin-console/supabase-url" \
  --value "https://your-project.supabase.co" \
  --type String

aws ssm put-parameter \
  --name "/admin-console/supabase-anon-key" \
  --value "your-anon-key" \
  --type SecureString
```

### Accessing Environment Variables in Code

```typescript
// app/config/supabase.ts
import Constants from 'expo-constants';

const supabaseUrl = Constants.expoConfig?.extra?.supabaseUrl ||
                    process.env.EXPO_PUBLIC_SUPABASE_URL;

const supabaseAnonKey = Constants.expoConfig?.extra?.supabaseAnonKey ||
                        process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

---

## Progressive Web App (PWA) Support

Expo Web automatically generates PWA configuration. Customize it:

### 1. Update app.json

```json
{
  "expo": {
    "web": {
      "favicon": "./assets/favicon.png",
      "bundler": "metro",
      "config": {
        "firebase": {
          "apiKey": "...",
          "authDomain": "..."
        }
      }
    },
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    }
  }
}
```

### 2. PWA Features

**Automatically Generated:**
- ✅ `manifest.json` (app name, icons, theme)
- ✅ Service worker registration
- ✅ Offline support (basic)
- ✅ Install prompt (Add to Home Screen)

**Test PWA:**
1. Open in Chrome
2. F12 → Application tab
3. Check "Manifest" and "Service Workers"
4. Lighthouse → Generate PWA report

---

## Performance Optimization

### 1. Code Splitting

Expo automatically code-splits routes when using Expo Router:

```typescript
// app/(tabs)/customers.tsx
// This route is automatically code-split
export default function CustomersScreen() {
  return <CustomerList />;
}
```

### 2. Lazy Loading Images

```typescript
import { Image } from 'expo-image';

<Image
  source={{ uri: customer.avatar }}
  placeholder={{ blurhash: customer.blurhash }}
  contentFit="cover"
  transition={200}
/>
```

### 3. Caching Strategy

```typescript
import { useQuery } from '@tanstack/react-query';

const { data: customers } = useQuery({
  queryKey: ['customers'],
  queryFn: fetchCustomers,
  staleTime: 5 * 60 * 1000, // 5 minutes
  cacheTime: 10 * 60 * 1000, // 10 minutes
});
```

### 4. Bundle Size Optimization

```bash
# Analyze bundle
npx expo export:web --dump-assetmap

# Check for large dependencies
npm install -g source-map-explorer
source-map-explorer web-build/static/js/*.js
```

**Common Large Dependencies:**
- `@supabase/supabase-js` (~50KB)
- `react-native-web` (~300KB)
- Remove unused dependencies

---

## Monitoring and Analytics

### 1. Web Vitals

Track Core Web Vitals in production:

```typescript
// app/_layout.tsx
import { useEffect } from 'react';
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

export default function RootLayout() {
  useEffect(() => {
    if (typeof window !== 'undefined') {
      getCLS(console.log);
      getFID(console.log);
      getFCP(console.log);
      getLCP(console.log);
      getTTFB(console.log);
    }
  }, []);

  return <Slot />;
}
```

### 2. Error Tracking

Integrate Sentry or similar:

```bash
npm install @sentry/react-native
```

```typescript
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'your-sentry-dsn',
  environment: process.env.NODE_ENV,
  enabled: process.env.NODE_ENV === 'production',
});
```

### 3. Analytics

Use Supabase Analytics or Google Analytics:

```typescript
import { supabase } from './config/supabase';

// Track page views
supabase.from('analytics_events').insert({
  event_name: 'page_view',
  page: window.location.pathname,
  user_id: user?.id,
});
```

---

## Troubleshooting

### Issue 1: CORS Errors in Production

**Symptom:**
```
Access to fetch at 'https://your-project.supabase.co/functions/v1/admin-customers'
from origin 'https://yourdomain.com' has been blocked by CORS policy
```

**Solution:**
1. Verify domain is in CORS whitelist (`cors.ts`)
2. Redeploy Edge Functions: `supabase functions deploy admin-customers`
3. Clear browser cache and test

### Issue 2: Environment Variables Not Loading

**Symptom:**
```
Error: supabaseUrl is required
```

**Solution:**
1. Verify environment variables in hosting platform dashboard
2. Check variable names start with `EXPO_PUBLIC_`
3. Rebuild and redeploy: `expo export:web && vercel --prod`

### Issue 3: Routes Not Working (404)

**Symptom:**
Navigation works initially, but refresh returns 404

**Solution:**
Configure SPA fallback:

**Vercel:**
```json
{
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ]
}
```

**Netlify:**
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Issue 4: Slow Initial Load

**Symptom:**
First page load takes >5 seconds

**Solution:**
1. Enable Gzip/Brotli compression (automatic on Vercel/Netlify)
2. Optimize images with `expo-image`
3. Code-split large components
4. Use CDN (CloudFront, Vercel Edge Network)

---

## Security Checklist

Before going to production:

- [ ] **HTTPS Enabled**: All traffic uses SSL/TLS
- [ ] **CORS Configured**: Only whitelisted domains allowed
- [ ] **Environment Variables Secured**: No secrets in client code
- [ ] **Input Validation**: All API calls validated (Zod schemas)
- [ ] **Rate Limiting**: API calls rate-limited (60/min default)
- [ ] **Authentication**: JWT tokens secured with httpOnly cookies (if applicable)
- [ ] **CSP Headers**: Content Security Policy configured
- [ ] **XSS Protection**: Input sanitization enabled
- [ ] **Audit Logging**: All actions logged to `audit_log` table

---

## Deployment Checklist

- [ ] Run `npm run build` locally and verify no errors
- [ ] Test authentication flow on web
- [ ] Test CRUD operations (customers, projects, invoices)
- [ ] Verify responsive design on mobile/tablet/desktop
- [ ] Check browser console for errors
- [ ] Test in Chrome, Firefox, Safari, Edge
- [ ] Verify CORS with production domain
- [ ] Set environment variables in hosting platform
- [ ] Deploy Edge Functions with updated CORS
- [ ] Configure custom domain and SSL
- [ ] Test PWA installation (Add to Home Screen)
- [ ] Run Lighthouse audit (aim for >90 score)
- [ ] Set up monitoring and error tracking
- [ ] Document deployment process for team

---

## Continuous Deployment (CD)

### GitHub Actions Workflow

Create `.github/workflows/deploy-web.yml`:

```yaml
name: Deploy Admin Console to Vercel

on:
  push:
    branches:
      - main

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
        run: cd admin-console && npm ci

      - name: Build for production
        run: cd admin-console && npm run build
        env:
          EXPO_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          EXPO_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./admin-console
```

---

## Next Steps

1. **Choose Hosting Platform**: Vercel (recommended), Netlify, or AWS
2. **Configure Environment**: Set up environment variables
3. **Update CORS**: Add production domain to whitelist
4. **Deploy**: Follow platform-specific steps above
5. **Test**: Verify all functionality works on production domain
6. **Monitor**: Set up analytics and error tracking
7. **Optimize**: Run Lighthouse and improve performance

---

## Support and Resources

- **Expo Web Docs**: https://docs.expo.dev/workflow/web/
- **React Native for Web**: https://necolas.github.io/react-native-web/
- **Vercel Docs**: https://vercel.com/docs
- **Netlify Docs**: https://docs.netlify.com/
- **Supabase Docs**: https://supabase.com/docs

---

## Conclusion

The Admin Console is fully configured for web deployment with:
- ✅ Expo Web support enabled
- ✅ CORS configured for web origins
- ✅ Production build process documented
- ✅ Multiple hosting options (Vercel, Netlify, AWS)
- ✅ PWA support included
- ✅ Security measures in place

**Ready to deploy!** Choose your hosting platform and follow the steps above.

---

**Last Updated**: 2025-11-12
**Branch**: `claude/comprehensive-technical-review-guide-011CV4GmG4H3M7Seg9KC2ZcP`
**Status**: ✅ Web Deployment Ready
