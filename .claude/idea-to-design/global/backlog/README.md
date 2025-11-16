# Global Backlog - Infrastructure & DBA Setup

## Overview

This directory contains global infrastructure tasks that support multiple DBAs (Doing Business As) and applications across the C-Level Sales Guy LLC ecosystem. These tasks are foundational and must be completed before launching specific DBA applications.

## Files

### `manual-queue.json`
Contains 7 infrastructure, admin, and naming tasks:

**P1 Tasks (Critical for DBA Launch)**:
- Configure domain routing for partner DBAs
- Provision analytics properties per DBA
- Validate domain availability for selected DBA names
- Implement name vetting automation (domain + trademark API) - [scripts/name-vetting.js](../../../scripts/name-vetting.js)

**P2 Tasks (Admin Dashboard - linked to [DBA Dashboard Spec](../software-factory-admin/dba-dashboard-spec.md))**:
- Design DBA metrics view for Software Factory admin
- Implement API endpoints to serve per-DBA analytics
- Build social handle availability monitor

## Task Categories

- **domain**: Domain routing and URL structure
- **infrastructure**: Vercel configuration and deployment setup
- **analytics**: GA4/Segment properties and tracking configuration
- **naming**: Business name vetting, domain checks, trademark screening
- **automation**: Automated workflows and API integrations
- **admin**: Software Factory admin dashboard and metrics
- **legal**: Trademark and legal compliance validation
- **social**: Social media handle availability and monitoring

## DBA Categories

These tasks support the following planned DBA categories:

### Consumer-Facing Brand
- **Target**: Direct-to-consumer applications
- **URL Pattern**: `clevelsalesguy.com/d2c/*`
- **Analytics**: Consumer behavior tracking
- **Tone**: Playful, accessible

### Bespoke/White-Label Brand
- **Target**: Custom solutions for partners
- **URL Pattern**: `clevelsalesguy.com/bespoke/*`
- **Analytics**: Partner engagement tracking
- **Tone**: Professional, customizable

### Enterprise Sales Suite
- **Target**: Enterprise clients and large organizations
- **URL Pattern**: `clevelsalesguy.com/enterprise/*`
- **Analytics**: Enterprise metrics and ROI tracking
- **Tone**: Sophisticated, data-driven

## Usage

### Manual Queue Processing
```bash
# Validate JSON structure
node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('.claude/idea-to-design/global/backlog/manual-queue.json', 'utf8'));
console.log('✅ JSON valid, items:', data.items.length);
"

# Process with backlog sync
node scripts/backlog-sync.js --input .claude/idea-to-design/global/backlog/manual-queue.json --dry-run

# Full processing
node scripts/backlog-sync.js --input .claude/idea-to-design/global/backlog/manual-queue.json
```

### Task Management
- **Status**: pending → in-progress → completed
- **Priority**: P1 (critical for DBA launch)
- **Labels**: Use for filtering and categorization
- **Dependencies**: These tasks block DBA-specific development

## Integration Points

### Domain Routing
- **Vercel Configuration**: Path-based routing setup
- **DNS Management**: Subdomain and path configuration
- **SSL Certificates**: Automatic HTTPS for all paths
- **CDN**: Global content delivery optimization

### Analytics Setup
- **GA4 Properties**: Separate properties per DBA category
- **Environment Variables**: Per-app tracking configuration
- **Conversion Goals**: DBA-specific conversion tracking
- **Reporting**: Consolidated and segmented analytics

## Dependencies

These global tasks must be completed before:
- DBA-specific application development
- Analytics implementation in individual apps
- Domain-specific deployment configurations
- Cross-DBA feature development

## Success Criteria

- [ ] All DBA categories have defined URL patterns
- [ ] Vercel routing configured for all planned paths
- [ ] Analytics properties created and documented
- [ ] Environment variables documented for each DBA
- [ ] DNS configuration ready for DBA launches

## Next Steps

1. **DBA Naming Automation**: Complete [scripts/name-vetting.js](../../../scripts/name-vetting.js) implementation
   - Integrate Domainr/GoDaddy API for domain availability
   - Connect to USPTO TSDR for trademark screening
   - Build social handle availability checks
   - Enable automated scoring and risk assessment
2. **DBA Name Validation**: Run name vetting on selected DBA candidates
   - Pixelspark (Consumer)
   - Apex Partner Solutions (Bespoke)
   - Apex Strategy Group (Enterprise)
3. **Domain Planning**: Map validated DBA names to URL patterns
4. **Analytics Design**: Create tracking strategy per DBA category
5. **Implementation**: Execute domain and analytics setup
6. **Documentation**: Update deployment guides with DBA-specific configs

---

**Last Updated**: January 24, 2025  
**Status**: Pending DBA Naming  
**Next Review**: After DBA names are finalized  
**Dependencies**: AI Studio DBA naming research
