# Claude Code Web ↔ Cursor Workflow Integration

## Overview

This workflow orchestrates background Claude Code Web jobs with local Cursor development, enabling async repository tasks while keeping Cursor free for focused editing.

## Key Benefits

- **Async Throughput**: Run long-running refactors/research in Claude Web while Cursor stays free
- **Shared Context**: Teleport workflow carries full cloud conversation into Cursor
- **Clean Branch Lifecycle**: Auto-push branches/PRs keep GitHub as source of truth
- **Cross-Device Workflow**: Start tasks from browser, continue in Cursor
- **Background Research**: Split discovery (Claude Web) from implementation (local Cursor)

## Prerequisites

### Required Tools
```bash
# Install dependencies
brew install jq gh  # macOS
# or
sudo apt-get install jq gh  # Ubuntu

# Install Claude CLI
npm install -g @anthropic-ai/claude
```

### Authentication
```bash
# GitHub CLI authentication
gh auth login

# Claude CLI authentication
claude auth login
```

## Quick Start

### 1. Queue a Background Job
```bash
# Basic job
./scripts/claude_cursor_workflow.sh queue "Refactor authentication system to use JWT tokens"

# High priority job
./scripts/claude_cursor_workflow.sh queue "Add comprehensive error handling" high

# Research job with custom suffix
./scripts/claude_cursor_workflow.sh queue "Research AI integration patterns" normal research
```

### 2. Monitor Progress
```bash
# List all jobs
./scripts/claude_cursor_workflow.sh list

# Check specific job
./scripts/claude_cursor_workflow.sh show job-1

# Sync job status and pull results
./scripts/claude_cursor_workflow.sh sync job-1
```

### 3. Import Conversation to Cursor
```bash
# Generate teleport command
./scripts/claude_cursor_workflow.sh teleport job-1

# Run the generated command in Cursor CLI
claude teleport claude-session-1234567890
```

## Workflow Patterns

### Background Research + Local Implementation
```bash
# 1. Queue research job
./scripts/claude_cursor_workflow.sh queue "Research best practices for AI agent orchestration" normal research

# 2. Continue local work in Cursor
# ... work on other features ...

# 3. Check research results
./scripts/claude_cursor_workflow.sh sync job-1

# 4. Import research conversation
./scripts/claude_cursor_workflow.sh teleport job-1

# 5. Implement findings locally
```

### Async Refactoring
```bash
# 1. Queue refactoring job
./scripts/claude_cursor_workflow.sh queue "Refactor user authentication to use OAuth2 with proper error handling" high

# 2. Work on other features locally
# ... continue development ...

# 3. Sync refactoring results
./scripts/claude_cursor_workflow.sh sync job-2

# 4. Review and integrate changes
git checkout claude-20241022-143022
# Review changes, test, merge
```

### Feature Research + Implementation
```bash
# 1. Research phase
./scripts/claude_cursor_workflow.sh queue "Research real-time collaboration patterns for web applications" normal research

# 2. Implementation phase (after research)
./scripts/claude_cursor_workflow.sh queue "Implement WebSocket-based real-time collaboration" high

# 3. Sync both jobs
./scripts/claude_cursor_workflow.sh sync job-1
./scripts/claude_cursor_workflow.sh sync job-2
```

## Command Reference

### Queue Commands
```bash
# Basic queue
./scripts/claude_cursor_workflow.sh queue "<prompt>"

# With priority (low, normal, high)
./scripts/claude_cursor_workflow.sh queue "<prompt>" high

# With custom branch suffix
./scripts/claude_cursor_workflow.sh queue "<prompt>" normal research
```

### Sync Commands
```bash
# Sync specific job
./scripts/claude_cursor_workflow.sh sync <job_id>

# List all jobs
./scripts/claude_cursor_workflow.sh list

# Show job details
./scripts/claude_cursor_workflow.sh show <job_id>
```

### Teleport Commands
```bash
# Generate teleport command
./scripts/claude_cursor_workflow.sh teleport <job_id>

# Run in Cursor CLI
claude teleport <session_id>
```

### Maintenance Commands
```bash
# Clean up old jobs (default: 7 days)
./scripts/claude_cursor_workflow.sh cleanup

# Clean up jobs older than 14 days
./scripts/claude_cursor_workflow.sh cleanup 14
```

## Configuration

### Environment Variables
```bash
# Max concurrent jobs (default: 3)
export CLAUDE_MAX_JOBS=5

# Branch prefix (default: claude-)
export CLAUDE_BRANCH_PREFIX="ai-"

# Jobs directory (default: .claude-jobs)
export CLAUDE_JOBS_DIR=".ai-jobs"
```

### Job Metadata
Jobs are stored in `.claude-jobs/metadata.json`:
```json
{
  "jobs": {
    "job-1": {
      "id": "job-1",
      "branch_name": "claude-20241022-143022",
      "prompt": "Refactor authentication system",
      "priority": "high",
      "status": "completed",
      "created_at": "2024-10-22T14:30:22Z",
      "updated_at": "2024-10-22T14:45:30Z",
      "claude_session_id": "claude-session-1234567890",
      "teleport_command": "claude teleport claude-session-1234567890",
      "notes": "Branch pushed to remote"
    }
  },
  "next_id": 2
}
```

## Best Practices

### Job Naming
- Use descriptive prompts that clearly state the objective
- Include context about the codebase when relevant
- Specify priority levels appropriately

### Branch Management
- Review branches before merging
- Test changes thoroughly
- Use descriptive commit messages
- Clean up merged branches

### Concurrent Work
- Limit concurrent jobs to avoid conflicts
- Use different branch suffixes for different types of work
- Monitor job status regularly
- Clean up completed jobs periodically

### Error Handling
- Check job status before syncing
- Handle failed jobs gracefully
- Use teleport commands to debug issues
- Clear context if teleport sessions fail

## Troubleshooting

### Common Issues

#### Teleport Sessions Fail
```bash
# Clear context and retry
claude clear-context
claude teleport <session_id>
```

#### Branch Conflicts
```bash
# Check for conflicts
git status
git diff

# Resolve conflicts manually
git add .
git commit -m "Resolve conflicts"
```

#### Job Stuck in Running
```bash
# Check job status
./scripts/claude_cursor_workflow.sh show <job_id>

# Force sync
./scripts/claude_cursor_workflow.sh sync <job_id>
```

### Debug Commands
```bash
# Show all job details
./scripts/claude_cursor_workflow.sh list

# Check specific job
./scripts/claude_cursor_workflow.sh show <job_id>

# View metadata file
cat .claude-jobs/metadata.json | jq .
```

## Integration with Cursor

### Recommended Workflow
1. **Start Background Job**: Queue research/refactoring in Claude Web
2. **Continue Local Work**: Use Cursor for focused development
3. **Sync Results**: Pull completed work from Claude Web
4. **Import Context**: Use teleport to bring conversation into Cursor
5. **Review & Integrate**: Test and merge changes locally

### Cursor Integration Points
- Use teleport commands in Cursor's CLI
- Import conversation context for follow-up work
- Review and test changes before merging
- Use Cursor's built-in tools for final implementation

## Future Enhancements

### Planned Features
- **Webhook Integration**: Auto-sync when jobs complete
- **Slack Notifications**: Notify when jobs finish
- **Job Templates**: Pre-defined job types
- **Metrics Dashboard**: Track job performance
- **Auto-merge**: Automatic PR creation and merging

### Customization Options
- **Custom Branch Naming**: Configurable branch patterns
- **Job Scheduling**: Queue jobs for specific times
- **Resource Limits**: Control job resource usage
- **Integration Hooks**: Custom post-job actions

---

**Last Updated**: October 22, 2025  
**Version**: 1.0  
**Status**: Ready for Pilot Testing