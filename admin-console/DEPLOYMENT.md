# Production Deployment Guide

**Admin Console - Design-First Software Factory**
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Build Configuration](#build-configuration)
4. [iOS Deployment](#ios-deployment)
5. [Android Deployment](#android-deployment)
6. [Web Deployment](#web-deployment)
7. [Push Notifications](#push-notifications)
8. [Monitoring & Analytics](#monitoring--analytics)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts

- **Expo Account**: https://expo.dev (EAS Build)
- **Apple Developer Account**: https://developer.apple.com ($99/year)
- **Google Play Console Account**: https://play.google.com/console ($25 one-time)
- **Supabase Project**: Production instance configured

### Required Tools

```bash
# Install EAS CLI globally
npm install -g eas-cli

# Login to Expo
eas login

# Verify installation
eas --version
```

---

## Environment Setup

### 1. Production Environment Variables

Create `.env.production`:

```bash
EXPO_PUBLIC_SUPABASE_URL=https://your-production-ref.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-production-anon-key
EXPO_PUBLIC_REDIRECT_URL=adminconsole://
```

### 2. Update `app.json`

```json
{
  "expo": {
    "extra": {
      "eas": {
        "projectId": "your-actual-eas-project-id"
      }
    }
  }
}
```

Get your EAS project ID:
```bash
eas project:init
```

### 3. Configure Supabase Production

**Backend Checklist**:
- ✅ Run all migrations on production database
- ✅ Load seed data (admin user only)
- ✅ Deploy all Edge Functions
- ✅ Configure RLS policies
- ✅ Set up storage buckets
- ✅ Configure authentication providers
- ✅ Set environment secrets

```bash
# Link to production project
supabase link --project-ref your-production-ref

# Push database migrations
supabase db push

# Deploy Edge Functions
supabase functions deploy admin-customers
supabase functions deploy admin-projects
supabase functions deploy upload-design
supabase functions deploy stripe-webhook

# Set secrets
supabase secrets set STRIPE_SECRET_KEY=sk_live_...
supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## Build Configuration

### iOS Configuration

1. **Update `eas.json`** with your Apple Developer info:

```json
{
  "build": {
    "production": {
      "ios": {
        "bundleIdentifier": "com.designfactory.adminconsole",
        "appleTeamId": "YOUR_TEAM_ID"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-apple-id@example.com",
        "ascAppId": "YOUR_ASC_APP_ID",
        "appleTeamId": "YOUR_TEAM_ID"
      }
    }
  }
}
```

2. **Generate App Icon & Splash Screen**:

```bash
# Use Expo's icon generator
npx expo-splash-screen --resize --platform all

# Or create manually:
# - Icon: 1024x1024px PNG (./assets/icon.png)
# - Splash: 1242x2688px PNG (./assets/splash.png)
# - Adaptive Icon (Android): 1024x1024px PNG (./assets/adaptive-icon.png)
```

### Android Configuration

1. **Create Service Account Key**:

- Go to Google Cloud Console
- Create Service Account with Google Play Developer permissions
- Download JSON key file
- Save as `service-account-key.json` (DO NOT commit to git)

2. **Update `eas.json`**:

```json
{
  "submit": {
    "production": {
      "android": {
        "serviceAccountKeyPath": "./service-account-key.json",
        "track": "internal"
      }
    }
  }
}
```

---

## iOS Deployment

### Step 1: Build for iOS

```bash
# Build for production
eas build --platform ios --profile production

# This will:
# 1. Upload your code to EAS
# 2. Build the app on Expo's servers
# 3. Generate an IPA file
# 4. Provide a download link (10-20 minutes)
```

### Step 2: Submit to App Store

```bash
# Automatic submission
eas submit --platform ios --latest

# Or manual submission:
# 1. Download IPA from EAS build page
# 2. Use Xcode Transporter to upload to App Store Connect
# 3. Fill out App Store listing
# 4. Submit for review
```

### Step 3: App Store Listing

**Required Information**:

- **App Name**: Admin Console - Design Factory
- **Subtitle**: Manage customers and projects
- **Description**: Professional admin console for managing Design Factory customers, projects, and operations. Track project progress, manage subscriptions, and communicate with customers.
- **Keywords**: admin, management, design, factory, console
- **Support URL**: https://your-website.com/support
- **Marketing URL**: https://your-website.com
- **Privacy Policy URL**: https://your-website.com/privacy
- **Screenshots**: 6.5" (iPhone 14 Pro Max) and 12.9" (iPad Pro)
- **Category**: Business / Productivity
- **Age Rating**: 4+

**App Review Information**:
- **Demo Account**: admin@designfactory.dev / SupabaseShouldReset!
- **Notes**: This is an internal admin console for managing our design factory operations.

---

## Android Deployment

### Step 1: Build for Android

```bash
# Build app bundle for production
eas build --platform android --profile production

# This creates an AAB (Android App Bundle)
```

### Step 2: Submit to Google Play

```bash
# Automatic submission to internal track
eas submit --platform android --latest

# Or manual submission:
# 1. Go to Google Play Console
# 2. Create new app
# 3. Upload AAB file
# 4. Fill out store listing
# 5. Submit for review
```

### Step 3: Google Play Listing

**Required Information**:

- **App Name**: Admin Console
- **Short Description**: Manage Design Factory operations
- **Full Description**: Professional admin console for Design Factory. Manage customers, track projects, handle invoices, and communicate with customers. Features include real-time project tracking, customer management, invoice viewing, and project notes.
- **App Category**: Business
- **Content Rating**: Everyone
- **Screenshots**: Phone (1080x1920), Tablet (1200x1920)
- **Feature Graphic**: 1024x500px
- **App Icon**: 512x512px

**Store Listing Assets**:
- Phone screenshots (minimum 2, maximum 8)
- 7-inch tablet screenshots (minimum 1, recommended)
- 10-inch tablet screenshots (minimum 1, recommended)
- Feature graphic (required)
- Promo video (optional but recommended)

---

## Web Deployment

The Admin Console supports web deployment through **Expo Web** (React Native for Web). The same codebase runs on browsers without any code modifications.

### Overview

**Web Support**: ✅ Fully configured
**Recommended Platform**: Vercel (zero-config deployment)
**Alternative Platforms**: Netlify, AWS S3 + CloudFront
**Build Time**: ~2-5 minutes
**Bundle Size**: ~500KB-1MB (gzipped)

For comprehensive web deployment documentation, see **[WEB_DEPLOYMENT.md](./WEB_DEPLOYMENT.md)** which covers:
- Local web development setup
- Production build process
- Hosting options (Vercel, Netlify, AWS)
- CORS configuration for web domains
- Progressive Web App (PWA) features
- Performance optimization
- Environment variables for web

### Quick Start: Deploy to Vercel

**1. Install Vercel CLI**:
```bash
npm install -g vercel
```

**2. Build for Web**:
```bash
cd admin-console
npx expo export:web
```

**3. Deploy**:
```bash
vercel --prod
```

**4. Configure Environment Variables**:
```bash
vercel env add EXPO_PUBLIC_SUPABASE_URL production
vercel env add EXPO_PUBLIC_SUPABASE_ANON_KEY production
```

**5. Update CORS Configuration**:

Add your Vercel domain to `supabase/functions/_shared/cors.ts`:
```typescript
const ALLOWED_ORIGINS = [
  // ... existing origins
  'https://admin-console.vercel.app',
  'https://yourdomain.com',
];
```

**6. Deploy Updated CORS**:
```bash
cd supabase/functions
supabase functions deploy admin-customers
supabase functions deploy admin-projects
supabase functions deploy upload-design
supabase functions deploy stripe-webhook
```

### Testing Web Deployment

After deployment, verify:
- ✅ App loads at production URL
- ✅ Authentication works (sign in/out)
- ✅ API calls succeed (check browser Network tab)
- ✅ CORS errors resolved
- ✅ Responsive design on mobile/tablet/desktop
- ✅ PWA installable (Add to Home Screen)

### Web vs Mobile Considerations

**Web-Specific Features**:
- Accessible via browser (no app store approval needed)
- Instant updates (no app store review process)
- SEO-friendly URLs with Expo Router
- Progressive Web App (PWA) support

**Limitations on Web**:
- No native push notifications (use web push API)
- No access to native device features (camera requires browser APIs)
- File system access limited to browser storage

### Continuous Deployment

Set up automatic deployments from Git:

**Vercel**:
1. Connect GitHub repository in Vercel dashboard
2. Configure environment variables
3. Every push to `main` auto-deploys

**Netlify**:
1. Connect repository in Netlify dashboard
2. Build command: `expo export:web`
3. Publish directory: `web-build`

### Web Deployment Checklist

- ✅ Run `expo export:web` locally to verify build
- ✅ Test locally at `http://localhost:19006`
- ✅ Configure environment variables on hosting platform
- ✅ Add production domain to CORS whitelist
- ✅ Deploy Edge Functions with updated CORS
- ✅ Test authentication flow on web
- ✅ Verify API calls work (no CORS errors)
- ✅ Test responsive design on multiple screen sizes
- ✅ Run Lighthouse audit (aim for score >90)
- ✅ Set up custom domain and SSL
- ✅ Configure error tracking (Sentry)
- ✅ Monitor Web Vitals in production

**See [WEB_DEPLOYMENT.md](./WEB_DEPLOYMENT.md) for complete step-by-step instructions.**

---

## Push Notifications

### Setup

1. **iOS - APNs Configuration**:

```bash
# Generate push notification credentials
eas credentials

# Follow prompts to:
# 1. Create Apple Push Notification Key
# 2. Upload to EAS
# 3. EAS will handle the rest
```

2. **Android - FCM Configuration**:

```bash
# EAS handles FCM automatically for managed workflow
# No additional configuration needed
```

### Testing Push Notifications

```bash
# Install expo-notifications-test CLI
npm install -g expo-notifications-test

# Send test notification
expo push:send --token YOUR_EXPO_PUSH_TOKEN --title "Test" --body "Testing notifications"
```

### Backend Integration

Add push notification column to `admin_users` table:

```sql
ALTER TABLE admin_users ADD COLUMN push_token TEXT;
```

Update Edge Function to send notifications:

```typescript
// supabase/functions/send-notification/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

serve(async (req) => {
  const { token, title, body } = await req.json();

  const message = {
    to: token,
    sound: 'default',
    title,
    body,
    data: { additionalData: 'goes here' },
  };

  await fetch('https://exp.host/--/api/v2/push/send', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(message),
  });

  return new Response('Notification sent', { status: 200 });
});
```

---

## Monitoring & Analytics

### Error Tracking (Recommended: Sentry)

```bash
npm install @sentry/react-native

# Initialize in app/_layout.tsx
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'your-sentry-dsn',
  environment: 'production',
});
```

### Analytics (Recommended: Expo Analytics or Firebase)

```bash
npm install expo-firebase-analytics

# Or use Segment, Amplitude, etc.
```

### Performance Monitoring

Use Expo's built-in performance monitoring:

```bash
# View metrics in Expo dashboard
https://expo.dev/accounts/[account]/projects/[project]/insights
```

---

## Troubleshooting

### Common Build Errors

**Error: Bundle identifier mismatch**
```bash
# Solution: Ensure bundle ID in app.json matches eas.json
# iOS: com.designfactory.adminconsole
# Android: com.designfactory.adminconsole
```

**Error: Push notification certificate expired**
```bash
# Solution: Regenerate certificates
eas credentials --platform ios
# Select "Push Notifications: Manage your Apple Push Notification Key"
```

**Error: Service account permissions**
```bash
# Solution: Ensure service account has these roles:
# - Service Account User
# - Google Play Developer
```

### Build Taking Too Long

- Typical build time: 10-20 minutes
- If >30 minutes, check EAS build status: https://expo.dev/accounts/[account]/builds
- Look for queued builds or errors

### App Rejected by App Store

Common rejection reasons:
1. **Missing demo account** - Provide test credentials
2. **Incomplete metadata** - Fill all required fields
3. **Privacy policy missing** - Add link in app.json and listing
4. **Screenshots don't match app** - Update with actual app screenshots

---

## Post-Deployment Checklist

### After iOS Approval
- ✅ Update app listing with actual screenshots
- ✅ Enable in all countries/regions
- ✅ Set up App Store optimization (ASO)
- ✅ Monitor crash reports
- ✅ Respond to user reviews

### After Android Release
- ✅ Promote from internal → closed beta → open beta → production
- ✅ Enable staged rollout (10% → 50% → 100%)
- ✅ Monitor Play Console vitals
- ✅ Respond to user feedback

### Monitoring (First Week)
- ✅ Check crash reports daily
- ✅ Monitor error tracking (Sentry)
- ✅ Review performance metrics
- ✅ Monitor API error rates (Supabase dashboard)
- ✅ Check push notification delivery rates

---

## Update Process

### Over-The-Air (OTA) Updates

For minor updates (JS, assets):

```bash
# Publish OTA update
eas update --branch production --message "Bug fix"

# All users will get the update on next app restart
```

### Full Rebuild (For Native Changes)

For native module updates:

```bash
# Build new version
eas build --platform all --profile production

# Submit to stores
eas submit --platform all --latest
```

### Version Bumping

```bash
# Update version in app.json
{
  "expo": {
    "version": "1.0.1",  // Bump this
    "ios": {
      "buildNumber": "2"  // Auto-incremented by EAS
    },
    "android": {
      "versionCode": 2     // Auto-incremented by EAS
    }
  }
}
```

---

## Support & Resources

- **EAS Documentation**: https://docs.expo.dev/eas/
- **Expo Forums**: https://forums.expo.dev/
- **Apple Developer Forums**: https://developer.apple.com/forums/
- **Android Developer Help**: https://support.google.com/googleplay/android-developer/

---

## Production Rollout Strategy

### Phase 1: Internal Testing (Week 1)
- Deploy to internal track
- Test with 2-3 admin users
- Verify all features work in production
- Monitor for crashes

### Phase 2: Beta Release (Week 2-3)
- iOS: TestFlight with 10-20 beta testers
- Android: Closed beta track
- Collect feedback
- Fix critical bugs

### Phase 3: Soft Launch (Week 4)
- iOS: Release to App Store
- Android: Open beta → Production (10% rollout)
- Monitor metrics closely
- Iterate based on feedback

### Phase 4: Full Release (Week 5+)
- Android: 100% rollout
- Marketing push
- Onboard all admin users
- Continuous monitoring and updates

---

**Status**: Ready for production deployment ✅
