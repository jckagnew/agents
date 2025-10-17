# Future Upgrades Tracking Guide

## Overview

The `scripts/add_future_upgrade.py` script maintains a structured backlog of emerging tools and capabilities without derailing current development momentum.

## Quick Usage

### Add a new upgrade candidate:
```bash
python3 scripts/add_future_upgrade.py \
  --name "Tool Name" \
  --status "Keep Watching" \
  --summary "One-line description" \
  --triggers "What would make us reconsider this" \
  --owner "Your Name" \
  --notes "Additional context or links"
```

### Update an existing entry:
```bash
python3 scripts/add_future_upgrade.py \
  --name "Existing Tool" \
  --status "Prototype" \
  --summary "Updated description" \
  --triggers "New trigger conditions" \
  --owner "New Owner" \
  --notes "Updated notes"
```

## Status Levels

- **Keep Watching**: Interesting but not ready for investment
- **Prototype**: Worth a small pilot or proof-of-concept
- **Adopt**: Ready for production integration
- **Parked**: No longer relevant or superseded

## Review Process

1. **Monthly Review**: During sprint retrospectives, scan the list for status changes
2. **Trigger Events**: When customer needs change or new capabilities emerge
3. **Decision Points**: Move items between statuses based on evidence and business needs

## Best Practices

- Keep summaries concise but descriptive
- Define clear trigger conditions for status changes
- Assign ownership to ensure accountability
- Update notes with research findings or customer feedback
- Archive or remove items that are no longer relevant

## Integration with Factory Workflow

- Link to this tracker in project READMEs
- Reference during architecture decisions
- Include in monthly factory planning sessions
- Use as input for tool evaluation criteria
