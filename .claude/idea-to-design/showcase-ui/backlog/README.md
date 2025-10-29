# Partner Showcase UI - Active Backlog

## Overview

This directory contains the active backlog for the Partner Showcase UI launch. These are immediate, actionable tasks that need to be completed before the Partner Showcase goes live.

## Files

### `manual-queue.json`
Contains 7 launch-critical tasks organized by priority:

**P1 Tasks (Critical for Launch)**:
- Finalize Partner Showcase content & metrics
- Confirm Partner Showcase CTA destinations  
- Complete Visual QA rerun with system Chrome
- Configure GA4 tracking and conversion goals
- Deploy Partner Showcase to staging
- Launch Partner Showcase to production

**P2 Tasks (Important but not blocking)**:
- Conduct stakeholder review

## Task Categories

- **launch**: Critical for launch readiness
- **content**: Content and copy tasks
- **cta**: Call-to-action and conversion tasks
- **qa**: Quality assurance and testing
- **analytics**: Tracking and measurement setup
- **deployment**: Staging and production deployment
- **stakeholder**: Review and approval processes

## Usage

### Manual Queue Processing
```bash
# Validate JSON structure
npm run parking:validate -- .claude/idea-to-design/showcase-ui/backlog/manual-queue.json

# Process with backlog sync
node scripts/backlog-sync.js --input .claude/idea-to-design/showcase-ui/backlog/manual-queue.json --dry-run

# Full processing
node scripts/backlog-sync.js --input .claude/idea-to-design/showcase-ui/backlog/manual-queue.json
```

### Task Management
- **Status**: pending → in-progress → completed
- **Priority**: P1 (critical), P2 (important)
- **Labels**: Use for filtering and categorization
- **Source**: Tracks where the task originated

## Integration with Software Factory

These backlog items integrate with:
- **Visual QA Factory**: QA rerun tasks
- **Deployment Pipeline**: Staging and production deployment
- **Analytics Setup**: GA4 configuration
- **Content Management**: Final content and metrics

## Success Criteria

All P1 tasks must be completed before production launch:
- [ ] Content finalized and reviewed
- [ ] CTAs tested and verified
- [ ] Visual QA passing
- [ ] Analytics configured
- [ ] Staging deployment successful
- [ ] Production launch completed

---

**Last Updated**: January 24, 2025  
**Status**: Active Launch Backlog  
**Next Review**: After P1 tasks completion
