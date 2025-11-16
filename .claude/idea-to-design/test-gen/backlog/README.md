# Backlog Management

This directory contains backlog items for the Software Factory pipeline, including templates and manual queue management.

## Files

- `backlog-template.json` - Template for backlog items with standard fields
- `backlog-sync.json` - Synced backlog from issue tracker (auto-generated)
- `manual-queue.json` - Manually queued items for processing

## Backlog Item Structure

Each backlog item contains the following fields:

### Required Fields
- **`id`**: Unique identifier (e.g., "BL-001")
- **`title`**: Short, descriptive title
- **`description`**: Detailed description of the work
- **`priority`**: Priority level (`high`, `medium`, `low`)
- **`source`**: Source of the requirement (`prd-requirements`, `ux-wireframes`, `architecture-requirements`, etc.)
- **`status`**: Current status (`pending`, `in_progress`, `completed`, `cancelled`)

### Optional Fields
- **`category`**: Work category (`feature`, `ui`, `infrastructure`, `backend`, `accessibility`, `bug`)
- **`effort_estimate`**: Estimated effort in story points or hours
- **`acceptance_criteria`**: Array of acceptance criteria
- **`dependencies`**: Array of dependent backlog item IDs
- **`tags`**: Array of tags for categorization
- **`created_date`**: ISO date when item was created
- **`due_date`**: ISO date when item should be completed
- **`assignee`**: Person assigned to the item
- **`labels`**: Array of labels for filtering and organization

## Manual Queue Management

### Adding Items to Manual Queue

1. **Create New Item**:
   ```json
   {
     "id": "BL-006",
     "title": "Your backlog item title",
     "description": "Detailed description of what needs to be done",
     "priority": "medium",
     "source": "manual-queue",
     "status": "pending",
     "category": "feature",
     "effort_estimate": "3",
     "acceptance_criteria": [
       "Criterion 1",
       "Criterion 2"
     ],
     "dependencies": [],
     "tags": ["tag1", "tag2"],
     "created_date": "2025-01-23",
     "due_date": "2025-02-01",
     "assignee": null,
     "labels": ["software-factory", "priority-medium", "feature"]
   }
   ```

2. **Add to `manual-queue.json`**:
   ```bash
   # Append to manual queue
   echo '{"id": "BL-006", "title": "New item", ...}' >> manual-queue.json
   ```

3. **Validate JSON**:
   ```bash
   # Check JSON validity
   jq . manual-queue.json
   ```

### Processing Manual Queue

The Software Factory pipeline will automatically process items in the manual queue:

1. **Read Manual Queue**: Load items from `manual-queue.json`
2. **Validate Items**: Check required fields and data types
3. **Merge with Sync**: Combine with synced items from issue tracker
4. **Generate Tasks**: Create actionable tasks from backlog items
5. **Update Status**: Mark items as processed

### Queue Status Tracking

Monitor queue processing through:

- **Status Updates**: Items move from `pending` → `in_progress` → `completed`
- **Progress Reports**: Generated in `reports/backlog-sync-report.json`
- **Log Files**: Detailed processing logs in `logs/backlog-sync.log`

## Integration with Issue Trackers

### Supported Providers
- **GitHub**: Issues and Projects
- **GitLab**: Issues and Milestones  
- **Jira**: Issues and Epics
- **Linear**: Issues and Projects
- **Asana**: Tasks and Projects

### Sync Process
1. **Authentication**: Use credentials from `.mcp/config`
2. **Fetch Issues**: Retrieve issues with `software-factory` label
3. **Transform Data**: Convert to backlog format
4. **Merge Updates**: Update existing items, add new ones
5. **Generate Report**: Create sync report with statistics

### Sync Commands
```bash
# Manual sync
npm run backlog:sync

# Sync with specific provider
npm run backlog:sync -- --provider github

# Dry run (preview changes)
npm run backlog:sync -- --dry-run

# Force sync (ignore rate limits)
npm run backlog:sync -- --force
```

## Backlog Categories

### Feature Development
- **`feature`**: New functionality and capabilities
- **`ui`**: User interface and user experience improvements
- **`backend`**: Server-side logic and API development

### Infrastructure
- **`infrastructure`**: DevOps, CI/CD, and deployment
- **`testing`**: Test automation and quality assurance
- **`documentation`**: Documentation and knowledge management

### Quality & Compliance
- **`accessibility`**: WCAG compliance and accessibility features
- **`security`**: Security improvements and vulnerability fixes
- **`performance`**: Performance optimization and monitoring

### Maintenance
- **`bug`**: Bug fixes and defect resolution
- **`refactor`**: Code refactoring and technical debt
- **`upgrade`**: Dependency updates and version upgrades

## Priority Levels

### High Priority
- **Critical bugs** affecting core functionality
- **Security vulnerabilities** requiring immediate attention
- **Blocking issues** preventing development progress
- **User-facing features** with tight deadlines

### Medium Priority
- **Feature enhancements** for better user experience
- **Performance improvements** for better scalability
- **Code quality** improvements and refactoring
- **Documentation** updates and improvements

### Low Priority
- **Nice-to-have features** with no immediate deadline
- **Technical debt** that can be addressed over time
- **Experimental features** for future consideration
- **Cosmetic improvements** with minimal impact

## Best Practices

### Writing Good Backlog Items
1. **Clear Titles**: Use action verbs and be specific
2. **Detailed Descriptions**: Include context, requirements, and constraints
3. **Acceptance Criteria**: Define clear, testable criteria
4. **Realistic Estimates**: Base effort estimates on historical data
5. **Proper Dependencies**: Identify and document dependencies

### Managing Dependencies
1. **Identify Blockers**: Mark items that block others
2. **Plan Sequencing**: Order items to minimize delays
3. **Track Progress**: Monitor dependent items regularly
4. **Adjust Priorities**: Reorder when dependencies change

### Status Management
1. **Regular Updates**: Keep status current and accurate
2. **Progress Tracking**: Update progress regularly
3. **Completion Criteria**: Ensure all criteria are met before marking complete
4. **Documentation**: Document decisions and changes

## Troubleshooting

### Common Issues

#### JSON Validation Errors
```bash
# Validate JSON syntax
jq . manual-queue.json

# Fix common issues
# - Missing commas between objects
# - Unclosed quotes or brackets
# - Invalid date formats
```

#### Sync Failures
```bash
# Check MCP configuration
cat .mcp/config

# Test API access
curl -H "Authorization: token $MCP_ISSUE_TRACKER_TOKEN" \
     https://api.github.com/user

# Check rate limits
curl -H "Authorization: token $MCP_ISSUE_TRACKER_TOKEN" \
     https://api.github.com/rate_limit
```

#### Duplicate Items
```bash
# Check for duplicate IDs
jq '.backlog_items | group_by(.id) | map(select(length > 1))' backlog-sync.json

# Remove duplicates
jq '.backlog_items | unique_by(.id)' backlog-sync.json > temp.json && mv temp.json backlog-sync.json
```

---

**Last Updated**: January 2025  
**Next Review**: February 2025  
**Status**: Ready for Use
