# MCP (Model Context Protocol) Setup Guide

## Overview

This guide explains how to configure MCP integrations for the Software Factory, specifically for Issue Tracker access and backlog synchronization.

## Prerequisites

- GitHub account with repository access
- Personal Access Token (PAT) with appropriate permissions
- MCP client installed and configured

## Issue Tracker Configuration

### 1. GitHub Setup

#### Create Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` - Full control of private repositories
   - `issues` - Read and write access to issues
   - `project` - Read and write access to project boards
4. Copy the generated token

#### Configure Repository
1. Ensure your repository has Issues enabled
2. Create labels for backlog items:
   - `software-factory`
   - `backlog-sync`
   - `priority-high`
   - `priority-medium`
   - `priority-low`

### 2. MCP Configuration

#### Update `.mcp/config`
```bash
# Edit the configuration file
nano .mcp/config

# Update with your credentials
ISSUE_TRACKER_PROVIDER=github
ISSUE_TRACKER_API_URL=https://api.github.com
ISSUE_TRACKER_TOKEN=ghp_your_token_here
ISSUE_TRACKER_OWNER=your_username
ISSUE_TRACKER_REPO=your_repository_name
```

#### Environment Variables (Alternative)
```bash
# Add to your .env file
export MCP_ISSUE_TRACKER_TOKEN=ghp_your_token_here
export MCP_ISSUE_TRACKER_OWNER=your_username
export MCP_ISSUE_TRACKER_REPO=your_repository_name
```

### 3. Test Configuration

#### Verify API Access
```bash
# Test GitHub API access
curl -H "Authorization: token $MCP_ISSUE_TRACKER_TOKEN" \
     https://api.github.com/repos/$MCP_ISSUE_TRACKER_OWNER/$MCP_ISSUE_TRACKER_REPO/issues
```

#### Test MCP Connection
```bash
# Run MCP test command
mcp test-connection --provider github
```

## Supported Providers

### GitHub
- **API URL**: `https://api.github.com`
- **Authentication**: Personal Access Token
- **Required Scopes**: `repo`, `issues`, `project`
- **Rate Limit**: 5000 requests/hour (authenticated)

### GitLab
- **API URL**: `https://gitlab.com/api/v4`
- **Authentication**: Personal Access Token
- **Required Scopes**: `api`, `read_api`, `write_repository`
- **Rate Limit**: 2000 requests/hour

### Jira
- **API URL**: `https://your-domain.atlassian.net/rest/api/3`
- **Authentication**: API Token + Email
- **Required Permissions**: Browse projects, Create issues, Edit issues
- **Rate Limit**: 300 requests/minute

### Linear
- **API URL**: `https://api.linear.app/graphql`
- **Authentication**: API Key
- **Required Permissions**: Read issues, Create issues, Update issues
- **Rate Limit**: 1000 requests/hour

## Configuration Options

### Rate Limiting
```bash
# Adjust rate limiting based on provider
ISSUE_TRACKER_RATE_LIMIT=60  # requests per minute
```

### Custom Field Mappings
```bash
# Map custom fields to standard backlog fields
ISSUE_TRACKER_PRIORITY_FIELD=priority
ISSUE_TRACKER_STATUS_FIELD=status
ISSUE_TRACKER_LABELS_FIELD=labels
```

### Default Settings
```bash
# Set default labels and assignee
ISSUE_TRACKER_DEFAULT_LABELS=software-factory,backlog-sync
ISSUE_TRACKER_DEFAULT_ASSIGNEE=your_username
```

## Security Best Practices

### Token Management
- Store tokens in `.mcp/config` (not committed to git)
- Use environment variables for production
- Rotate tokens regularly
- Use minimal required permissions

### Access Control
- Limit repository access to necessary repositories
- Use organization-level tokens when possible
- Monitor token usage in provider dashboards

### Configuration Validation
- Validate configuration before first use
- Test API access with minimal permissions
- Verify rate limiting settings

## Troubleshooting

### Common Issues

#### Authentication Errors
```bash
# Check token validity
curl -H "Authorization: token $MCP_ISSUE_TRACKER_TOKEN" \
     https://api.github.com/user

# Verify repository access
curl -H "Authorization: token $MCP_ISSUE_TRACKER_TOKEN" \
     https://api.github.com/repos/$MCP_ISSUE_TRACKER_OWNER/$MCP_ISSUE_TRACKER_REPO
```

#### Rate Limiting
```bash
# Check rate limit status
curl -H "Authorization: token $MCP_ISSUE_TRACKER_TOKEN" \
     https://api.github.com/rate_limit
```

#### Permission Errors
- Verify token has required scopes
- Check repository permissions
- Ensure repository has Issues enabled

### Debug Mode
```bash
# Enable debug logging
ISSUE_TRACKER_DEBUG=true

# Check MCP logs
mcp logs --provider github
```

## Integration with Software Factory

### Backlog Sync Process
1. **Read Configuration**: Load settings from `.mcp/config`
2. **Authenticate**: Use stored credentials to access API
3. **Fetch Issues**: Retrieve issues with `software-factory` label
4. **Transform Data**: Convert to backlog format
5. **Update Local**: Sync with local backlog files

### Automation Triggers
- **Manual**: Run backlog sync command
- **Scheduled**: Set up cron job for regular sync
- **Webhook**: Trigger on issue updates (if webhook configured)

## Next Steps

1. **Configure Provider**: Set up your chosen issue tracker
2. **Test Connection**: Verify API access works
3. **Create Labels**: Set up required labels in your repository
4. **Run First Sync**: Test the backlog synchronization process

---

**Last Updated**: January 2025  
**Next Review**: February 2025  
**Status**: Ready for Configuration
