# Deployment Notes

## Overview

This document tracks deployment configurations and notes for various applications and services in the C-Level Sales Guy LLC ecosystem.

**Last Updated**: January 24, 2025  
**Status**: Active

---

## Partner Showcase UI

### Deployment Target
- **Primary Domain**: `clevelsalesguy.com/partners`
- **Staging Domain**: `partner-showcase-ui.vercel.app`
- **Vercel Project**: `partner-showcase-ui` (placeholder)

### Configuration
- **Framework**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Node Version**: 18.x
- **Region**: `iad1` (US East)

### DNS Configuration
- **A Record**: `partners.clevelsalesguy.com` → Vercel IP
- **CNAME Record**: `www.partners.clevelsalesguy.com` → `partners.clevelsalesguy.com`
- **SSL**: Automatic via Vercel

### Environment Variables
```bash
# Production
NEXT_PUBLIC_APP_URL=https://partners.clevelsalesguy.com
NEXT_PUBLIC_API_URL=https://api.clevelsalesguy.com
NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX

# Staging
NEXT_PUBLIC_APP_URL=https://partner-showcase-ui.vercel.app
NEXT_PUBLIC_API_URL=https://staging-api.clevelsalesguy.com
NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX
```

### Performance Requirements
- **Load Time**: < 2 seconds
- **LCP**: < 2.5 seconds
- **FID**: < 100ms
- **CLS**: < 0.1

### Security Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy: default-src 'self'`

### Monitoring
- **Uptime**: Vercel Analytics
- **Performance**: Vercel Speed Insights
- **Errors**: Vercel Functions Logs
- **Custom**: Google Analytics 4

### Deployment Process
1. **Development**: `npm run dev` (local development)
2. **Preview**: `vercel` (staging deployment)
3. **Production**: `vercel --prod` (production deployment)

### Rollback Strategy
- **Vercel**: Automatic rollback to previous deployment
- **DNS**: Point to previous deployment if needed
- **Database**: No database dependencies

### Backup Strategy
- **Code**: Git repository (GitHub)
- **Assets**: Vercel CDN
- **Configuration**: Vercel dashboard

---

## C-Level Sales Guy Website

### Deployment Target
- **Primary Domain**: `clevelsalesguy.com`
- **Staging Domain**: `clevel-sales-guy.vercel.app`
- **Vercel Project**: `clevel-sales-guy`

### Configuration
- **Framework**: Next.js
- **Database**: Supabase
- **Authentication**: Supabase Auth
- **File Storage**: Supabase Storage

### Environment Variables
```bash
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

---

## Software Factory

### Deployment Target
- **Primary Domain**: `factory.clevelsalesguy.com`
- **Staging Domain**: `software-factory.vercel.app`
- **Vercel Project**: `software-factory`

### Configuration
- **Framework**: Next.js
- **Database**: Supabase
- **AI Integration**: Claude API, OpenAI API, Google AI Studio

---

## Weight Tracker Apps

### Deployment Target
- **Primary Domain**: `apps.clevelsalesguy.com/weight-tracker`
- **Staging Domain**: `weight-tracker-nextjs.vercel.app`
- **Vercel Project**: `weight-tracker-nextjs`

### Configuration
- **Framework**: Next.js
- **Database**: Supabase
- **Authentication**: Supabase Auth

---

## Monitoring & Analytics

### Uptime Monitoring
- **Primary**: Vercel Analytics
- **Secondary**: UptimeRobot
- **Alerts**: Email, Slack

### Performance Monitoring
- **Core Web Vitals**: Vercel Speed Insights
- **Custom Metrics**: Google Analytics 4
- **Error Tracking**: Vercel Functions Logs

### Security Monitoring
- **SSL**: Vercel automatic renewal
- **DDoS**: Vercel protection
- **Security Headers**: Automated via Vercel

---

## Backup & Recovery

### Code Backup
- **Primary**: GitHub repository
- **Secondary**: Local development machines
- **Retention**: Indefinite

### Database Backup
- **Supabase**: Automatic daily backups
- **Retention**: 30 days
- **Recovery**: Point-in-time recovery

### Asset Backup
- **Images**: Vercel CDN + Supabase Storage
- **Documents**: Supabase Storage
- **Retention**: Indefinite

---

## Disaster Recovery

### Recovery Time Objective (RTO)
- **Critical Services**: < 1 hour
- **Non-Critical Services**: < 4 hours

### Recovery Point Objective (RPO)
- **Database**: < 1 hour
- **Static Assets**: < 15 minutes

### Recovery Procedures
1. **Assess Impact**: Determine scope of outage
2. **Activate Backup**: Switch to backup systems
3. **Restore Data**: Restore from latest backup
4. **Validate Service**: Ensure functionality
5. **Communicate**: Notify stakeholders

---

**Last Updated**: January 24, 2025  
**Next Review**: February 24, 2025  
**Status**: Active
