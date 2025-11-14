# Sentry MCP Server

MCP server for Sentry API. Track errors, monitor performance, manage releases, and debug issues with comprehensive error tracking and observability features.

## Features

- **Error Tracking**: Monitor and manage application errors
- **Issue Management**: Group, assign, and resolve issues
- **Release Tracking**: Track deployments and versions
- **Event Details**: Access stack traces and breadcrumbs
- **Performance Monitoring**: Track application performance metrics
- **Search & Filters**: Advanced query syntax for finding issues
- **Team Management**: Organize teams and assignments
- **Project Statistics**: Monitor error rates and trends

## Setup

### Prerequisites

- Sentry account (free or paid)
- Auth token with appropriate scopes

### Environment Variables

- `SENTRY_AUTH_TOKEN` (required): Your Sentry authentication token

**How to get credentials:**
1. Go to [sentry.io](https://sentry.io/)
2. Log in to your account
3. Go to Settings → Account → API → Auth Tokens
4. Click "Create New Token"
5. Select scopes: `project:read`, `project:write`, `event:read`, `org:read`, `member:read`
6. Copy the token and store as `SENTRY_AUTH_TOKEN`

Direct link: https://sentry.io/settings/account/api/auth-tokens/

## Rate Limits

- **Free/Developer**: 100 requests per second
- **Team/Business**: Higher limits based on plan
- **Enterprise**: Custom limits
- HTTP 429 response when limit exceeded
- Rate limit headers included in responses

## Available Tools

### Organization & Project Management

#### `list_organizations`
List all organizations the user has access to.

**Example:**
```python
orgs = await list_organizations()

# Returns:
# [
#   {
#     "id": "123456",
#     "slug": "my-org",
#     "name": "My Organization",
#     "dateCreated": "2024-01-01T00:00:00Z",
#     "features": ["performance-view", "release-health"]
#   }
# ]
```

#### `list_projects`
List projects in an organization.

**Parameters:**
- `organization_slug` (string, required): Organization slug

**Example:**
```python
projects = await list_projects(organization_slug="my-org")

# Returns projects with:
# - id, slug, name
# - platform (python, javascript, etc.)
# - status (active, disabled)
# - firstEvent, dateCreated
# - team associations
```

#### `get_project`
Get project details and statistics.

**Parameters:**
- `organization_slug` (string, required): Organization slug
- `project_slug` (string, required): Project slug

**Example:**
```python
project = await get_project(
    organization_slug="my-org",
    project_slug="my-app"
)

# Returns:
# - Configuration settings
# - Error rate statistics
# - Team assignments
# - Platform information
# - Issue grouping settings
```

### Issue Management

#### `list_issues`
List issues with filters.

**Parameters:**
- `organization_slug` (string, required): Organization slug
- `project_slug` (string, optional): Filter to specific project
- `query` (string, optional): Search query
- `status` (string, optional): Filter by status (unresolved, resolved, ignored)
- `limit` (int, optional): Number of issues (default: 25, max: 100)

**Issue Statuses:**
- **unresolved**: Active issues requiring attention
- **resolved**: Fixed issues
- **ignored**: Issues marked to ignore
- **reprocessing**: Issues being reprocessed

**Example:**
```python
# Unresolved errors
issues = await list_issues(
    organization_slug="my-org",
    status="unresolved",
    limit=50
)

# Errors in specific project
issues = await list_issues(
    organization_slug="my-org",
    project_slug="my-app",
    query="level:error"
)

# Complex query
issues = await list_issues(
    organization_slug="my-org",
    query="is:unresolved level:error assigned:me"
)
```

#### `get_issue`
Get issue details with events.

**Parameters:**
- `issue_id` (string, required): Issue ID

**Example:**
```python
issue = await get_issue(issue_id="1234567890")

# Returns:
# {
#   "id": "1234567890",
#   "title": "TypeError: Cannot read property 'foo' of undefined",
#   "culprit": "app/views/index.js in handleClick",
#   "level": "error",
#   "status": "unresolved",
#   "count": 42,
#   "userCount": 15,
#   "firstSeen": "2025-10-01T10:00:00Z",
#   "lastSeen": "2025-10-08T15:30:00Z",
#   "metadata": {
#     "type": "TypeError",
#     "value": "Cannot read property 'foo' of undefined"
#   },
#   "assignedTo": {
#     "email": "dev@example.com",
#     "name": "Developer Name"
#   }
# }
```

#### `update_issue`
Update issue status or assignment.

**Parameters:**
- `issue_id` (string, required): Issue ID
- `status` (string, optional): New status (resolved, unresolved, ignored, resolvedInNextRelease)
- `assigned_to` (string, optional): Username or email to assign
- `has_seen` (bool, optional): Mark as seen
- `is_bookmarked` (bool, optional): Bookmark status

**Example:**
```python
# Assign to developer
issue = await update_issue(
    issue_id="1234567890",
    assigned_to="dev@example.com",
    has_seen=True
)

# Resolve in next release
issue = await update_issue(
    issue_id="1234567890",
    status="resolvedInNextRelease"
)

# Bookmark for review
issue = await update_issue(
    issue_id="1234567890",
    is_bookmarked=True
)
```

#### `resolve_issue`
Mark issue as resolved.

**Parameters:**
- `issue_id` (string, required): Issue ID

**Example:**
```python
issue = await resolve_issue(issue_id="1234567890")
```

#### `ignore_issue`
Ignore an issue.

**Parameters:**
- `issue_id` (string, required): Issue ID

**Example:**
```python
# Useful for known issues or false positives
issue = await ignore_issue(issue_id="1234567890")
```

### Event Management

#### `list_events`
List error events for an issue.

**Parameters:**
- `issue_id` (string, required): Issue ID
- `limit` (int, optional): Number of events (default: 25, max: 100)

**Example:**
```python
events = await list_events(
    issue_id="1234567890",
    limit=50
)

# Returns individual occurrences of the issue
# Each event has unique context and stack trace
```

#### `get_event`
Get detailed event information with stack trace.

**Parameters:**
- `organization_slug` (string, required): Organization slug
- `project_slug` (string, required): Project slug
- `event_id` (string, required): Event ID

**Example:**
```python
event = await get_event(
    organization_slug="my-org",
    project_slug="my-app",
    event_id="abc123def456"
)

# Returns:
# {
#   "eventID": "abc123def456",
#   "message": "TypeError: Cannot read property 'foo' of undefined",
#   "datetime": "2025-10-08T15:30:00Z",
#   "platform": "javascript",
#   "user": {
#     "id": "user123",
#     "email": "user@example.com",
#     "ip_address": "192.168.1.1"
#   },
#   "contexts": {
#     "browser": {"name": "Chrome", "version": "118.0"},
#     "os": {"name": "Windows", "version": "10"}
#   },
#   "entries": [
#     {
#       "type": "exception",
#       "data": {
#         "values": [{
#           "type": "TypeError",
#           "value": "Cannot read property 'foo' of undefined",
#           "stacktrace": {
#             "frames": [...]
#           }
#         }]
#       }
#     },
#     {
#       "type": "breadcrumbs",
#       "data": {
#         "values": [...]
#       }
#     }
#   ],
#   "tags": [
#     {"key": "environment", "value": "production"},
#     {"key": "release", "value": "1.0.0"}
#   ]
# }
```

### Release Management

#### `list_releases`
List releases in a project.

**Parameters:**
- `organization_slug` (string, required): Organization slug
- `project_slug` (string, required): Project slug
- `limit` (int, optional): Number of releases (default: 25, max: 100)

**Example:**
```python
releases = await list_releases(
    organization_slug="my-org",
    project_slug="my-app",
    limit=20
)

# Returns releases with:
# - version, dateCreated, dateReleased
# - newGroups (new issues introduced)
# - commitCount, deployCount
# - authors
```

#### `get_release`
Get release details with commits.

**Parameters:**
- `organization_slug` (string, required): Organization slug
- `version` (string, required): Release version

**Example:**
```python
release = await get_release(
    organization_slug="my-org",
    version="1.0.0"
)

# Returns:
# - Full release information
# - Commit list with authors
# - Deploy information
# - Issue counts (new, resolved)
# - Health data
```

#### `create_release`
Create a new release.

**Parameters:**
- `organization_slug` (string, required): Organization slug
- `version` (string, required): Release version (e.g., "1.0.0")
- `projects` (list, required): List of project slugs
- `refs` (list, optional): Repository references
- `commits` (list, optional): Commit information
- `date_released` (string, optional): ISO 8601 datetime

**Example:**
```python
# Simple release
release = await create_release(
    organization_slug="my-org",
    version="1.2.0",
    projects=["my-app", "my-api"]
)

# Release with commits
release = await create_release(
    organization_slug="my-org",
    version="1.2.0",
    projects=["my-app"],
    refs=[{
        "repository": "my-org/my-app",
        "commit": "abc123def456"
    }],
    commits=[
        {
            "id": "abc123def456",
            "message": "Fix critical bug in auth",
            "author_email": "dev@example.com"
        },
        {
            "id": "def456ghi789",
            "message": "Add new feature"
        }
    ],
    date_released="2025-10-08T12:00:00Z"
)

# Releases help track:
# - Which errors were introduced in which version
# - Regression detection
# - Deploy health
# - Commit associations
```

### Team Management

#### `list_teams`
List teams in organization.

**Parameters:**
- `organization_slug` (string, required): Organization slug

**Example:**
```python
teams = await list_teams(organization_slug="my-org")

# Returns:
# [
#   {
#     "id": "123",
#     "slug": "frontend",
#     "name": "Frontend Team",
#     "memberCount": 5
#   }
# ]
```

### Statistics & Analytics

#### `get_project_stats`
Get project error statistics.

**Parameters:**
- `organization_slug` (string, required): Organization slug
- `project_slug` (string, required): Project slug
- `stat` (string, optional): Stat type (received, rejected, blacklisted)
- `resolution` (string, optional): Time resolution (1h, 1d, 1w)

**Example:**
```python
# Hourly error rates
stats = await get_project_stats(
    organization_slug="my-org",
    project_slug="my-app",
    stat="received",
    resolution="1h"
)

# Returns time series data:
# [[timestamp1, count1], [timestamp2, count2], ...]
```

### Search & Filtering

#### `search_issues`
Search issues with query filters.

**Parameters:**
- `organization_slug` (string, required): Organization slug
- `query` (string, required): Search query
- `limit` (int, optional): Number of results (default: 25, max: 100)
- `sort` (string, optional): Sort by (date, new, freq, priority, user)

**Query Syntax:**

**Status Filters:**
- `is:unresolved` - Active issues
- `is:resolved` - Fixed issues
- `is:ignored` - Ignored issues

**Level Filters:**
- `level:error` - Error level
- `level:warning` - Warning level
- `level:info` - Info level
- `level:debug` - Debug level
- `level:fatal` - Fatal errors

**Assignment:**
- `assigned:me` - Assigned to you
- `assigned:user@example.com` - Assigned to specific user
- `assigned:none` - Unassigned

**Release & Environment:**
- `release:1.0.0` - Specific release
- `environment:production` - Specific environment

**User Filters:**
- `user.email:user@example.com` - Errors from specific user
- `user.id:12345` - Errors from user ID

**Time Filters:**
- `age:-24h` - Last 24 hours
- `age:+1d` - Older than 1 day
- `firstSeen:-7d` - First seen in last week

**Other:**
- `has:stacktrace` - Has stack trace
- `has:user` - Has user context
- `is:for_review` - Marked for review
- `is:bookmarked` - Bookmarked

**Example:**
```python
# Complex search
issues = await search_issues(
    organization_slug="my-org",
    query="is:unresolved level:error assigned:me environment:production",
    limit=50,
    sort="freq"
)

# Find recent critical errors
issues = await search_issues(
    organization_slug="my-org",
    query="level:fatal age:-1d",
    sort="date"
)

# Unassigned production errors
issues = await search_issues(
    organization_slug="my-org",
    query="is:unresolved assigned:none environment:production release:1.2.0"
)
```

## Common Workflows

### Error Triage Workflow
```python
# 1. Get unresolved errors
issues = await list_issues(
    organization_slug="my-org",
    status="unresolved",
    query="level:error",
    limit=50
)

# 2. Review high-frequency issues
for issue in sorted(issues, key=lambda x: x['count'], reverse=True)[:10]:
    print(f"Issue: {issue['title']}")
    print(f"Occurrences: {issue['count']}")
    print(f"Users affected: {issue['userCount']}")

    # Get latest event details
    events = await list_events(issue_id=issue['id'], limit=1)

    # Assign to team member
    await update_issue(
        issue_id=issue['id'],
        assigned_to="dev@example.com",
        has_seen=True
    )
```

### Release Tracking
```python
# 1. Create release on deploy
release = await create_release(
    organization_slug="my-org",
    version="2.0.0",
    projects=["my-app"],
    commits=[
        {"id": "abc123", "message": "Fix auth bug"},
        {"id": "def456", "message": "Add new dashboard"}
    ]
)

# 2. Monitor release health
release_data = await get_release(
    organization_slug="my-org",
    version="2.0.0"
)

print(f"New issues: {release_data.get('newGroups', 0)}")

# 3. Check for regressions
new_issues = await search_issues(
    organization_slug="my-org",
    query="release:2.0.0 firstSeen:-1d",
    sort="new"
)
```

### Performance Investigation
```python
# 1. Get event details with full context
event = await get_event(
    organization_slug="my-org",
    project_slug="my-app",
    event_id="abc123"
)

# 2. Analyze stack trace
for entry in event['entries']:
    if entry['type'] == 'exception':
        frames = entry['data']['values'][0]['stacktrace']['frames']
        print("Stack trace:")
        for frame in frames:
            print(f"  {frame['filename']}:{frame['lineno']} in {frame['function']}")

# 3. Check breadcrumbs for user actions
for entry in event['entries']:
    if entry['type'] == 'breadcrumbs':
        print("User actions before error:")
        for crumb in entry['data']['values']:
            print(f"  {crumb['timestamp']}: {crumb['message']}")
```

### Team Dashboard
```python
# Get org overview
orgs = await list_organizations()

for org in orgs:
    projects = await list_projects(organization_slug=org['slug'])

    for project in projects:
        # Get error stats
        stats = await get_project_stats(
            organization_slug=org['slug'],
            project_slug=project['slug'],
            resolution="1d"
        )

        # Count unresolved issues
        issues = await list_issues(
            organization_slug=org['slug'],
            project_slug=project['slug'],
            status="unresolved"
        )

        print(f"Project: {project['name']}")
        print(f"  Unresolved issues: {len(issues)}")
        print(f"  24h error rate: {stats[-1][1] if stats else 0}")
```

## Best Practices

1. **Set up releases**: Track deployments for regression detection
2. **Use source maps**: Get readable JavaScript stack traces
3. **Configure error grouping**: Reduce noise from similar errors
4. **Set up alerts**: Get notified of critical issues
5. **Use breadcrumbs**: Add context for debugging
6. **Tag errors**: Add custom tags for filtering
7. **Monitor trends**: Watch error rates over time
8. **Assign ownership**: Route errors to responsible teams
9. **Review ignored issues**: Periodically check ignored errors
10. **Clean up resolved issues**: Archive old resolved issues

## Error Levels

Sentry classifies errors by severity:

- **fatal**: Critical errors causing complete failure
- **error**: Standard errors requiring attention
- **warning**: Warnings that may indicate problems
- **info**: Informational messages
- **debug**: Debug-level information

## Integration Tips

### CI/CD Integration
```python
# On deploy, create release
release = await create_release(
    organization_slug="my-org",
    version=os.getenv("BUILD_VERSION"),
    projects=["my-app"],
    refs=[{
        "repository": "my-org/my-app",
        "commit": os.getenv("GIT_COMMIT")
    }]
)

# Upload source maps (separate API call)
# Associate commits automatically from git
```

### Automated Triage
```python
# Auto-resolve issues fixed in latest release
resolved_issues = await search_issues(
    organization_slug="my-org",
    query="status:resolvedInNextRelease"
)

for issue in resolved_issues:
    # Check if fix was deployed
    await resolve_issue(issue_id=issue['id'])
```

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid auth token
- **403 Forbidden**: Insufficient permissions (check token scopes)
- **404 Not Found**: Organization, project, or issue not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Sentry service issue

## API Documentation

- [Sentry API Documentation](https://docs.sentry.io/api/)
- [Authentication](https://docs.sentry.io/api/auth/)
- [Issues API](https://docs.sentry.io/api/events/list-a-projects-issues/)
- [Releases API](https://docs.sentry.io/api/releases/)
- [Query Syntax](https://docs.sentry.io/product/sentry-basics/search/)

## Support

- [Documentation](https://docs.sentry.io/)
- [Community Forum](https://forum.sentry.io/)
- [Discord](https://discord.gg/sentry)
- [Status Page](https://status.sentry.io/)
- [Support](https://sentry.io/support/)
