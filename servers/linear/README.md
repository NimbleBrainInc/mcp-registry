# Linear MCP Server

MCP server for Linear API. Streamlined issue tracking, project management, sprint planning, and team collaboration for modern development teams.

## Features

- **Issue Management**: Create, update, search, and track issues
- **Project Planning**: Manage projects with milestones and roadmaps
- **Sprint Cycles**: Track sprint progress and metrics
- **Team Collaboration**: Organize teams and assign work
- **Labels & Organization**: Custom labels and filtering
- **GraphQL API**: Powerful, flexible queries
- **Real-time Updates**: Live issue status tracking
- **Custom Fields**: Priority levels, states, and metadata
- **Search & Filter**: Advanced issue search capabilities
- **Roadmap Planning**: Long-term project visibility

## Setup

### Prerequisites

- Linear account (Free or paid plan)
- API key with appropriate permissions

### Environment Variables

- `LINEAR_API_KEY` (required): Your Linear API key

**How to get credentials:**
1. Go to [linear.app/settings/api](https://linear.app/settings/api)
2. Sign in to your Linear workspace
3. Click "Create new key" or "Personal API keys"
4. Give your key a descriptive name
5. Copy the generated key (starts with `lin_api_`)
6. Store as `LINEAR_API_KEY`

**API Key Format:**
- Format: `lin_api_xxxxxxxxxxxxxxxxxxxxxxxx`
- Keep your key secure - it has full access to your workspace

## Rate Limits

**Standard Rate Limits:**
- 1500 requests per minute per IP address
- 50 requests per second per IP address
- Queries are counted by complexity (points system)
- Simple queries: 1-5 points
- Complex queries with relations: 10-50 points

**Best Practices:**
- Batch operations when possible
- Use pagination for large datasets
- Cache frequently accessed data
- Implement exponential backoff for retries

## GraphQL API

Linear uses GraphQL, which means:
- All requests POST to single endpoint: `https://api.linear.app/graphql`
- Specify exactly what data you need
- Combine multiple operations efficiently
- Strong typing and introspection
- Nested data fetching in single request

## Available Tools

### Issue Management

#### `list_issues`
List and filter issues across your workspace.

**Parameters:**
- `team_id` (string, optional): Filter by team ID
- `project_id` (string, optional): Filter by project ID
- `assignee_id` (string, optional): Filter by assignee user ID
- `label_id` (string, optional): Filter by label ID
- `state` (string, optional): Filter by state name (backlog, unstarted, started, completed, canceled)
- `first` (int, optional): Number of issues to return (default: 50)

**Example:**
```python
# List all issues
issues = await list_issues(first=20)

# Filter by team
issues = await list_issues(team_id="team-123", first=10)

# Filter by state
issues = await list_issues(state="started", first=25)

# Multiple filters
issues = await list_issues(
    team_id="team-123",
    assignee_id="user-456",
    state="unstarted"
)

# Returns:
# {
#   "data": {
#     "issues": {
#       "nodes": [
#         {
#           "id": "issue-123",
#           "title": "Implement user authentication",
#           "description": "Add OAuth2 support...",
#           "priority": 2,
#           "state": {
#             "name": "In Progress",
#             "type": "started"
#           },
#           "assignee": {
#             "id": "user-456",
#             "name": "Jane Smith"
#           },
#           "labels": {
#             "nodes": [
#               {"id": "label-789", "name": "backend"}
#             ]
#           },
#           "createdAt": "2025-10-01T10:00:00Z",
#           "updatedAt": "2025-10-08T14:30:00Z"
#         }
#       ]
#     }
#   }
# }
```

#### `get_issue`
Get detailed information about a specific issue.

**Parameters:**
- `issue_id` (string, required): Issue ID

**Example:**
```python
issue = await get_issue(issue_id="issue-123")

# Returns:
# {
#   "data": {
#     "issue": {
#       "id": "issue-123",
#       "title": "Fix login bug",
#       "description": "Users unable to login with email...",
#       "priority": 1,
#       "estimate": 3,
#       "state": {
#         "name": "In Progress",
#         "type": "started"
#       },
#       "assignee": {
#         "id": "user-456",
#         "name": "Jane Smith",
#         "email": "jane@company.com"
#       },
#       "labels": {
#         "nodes": [
#           {"id": "label-123", "name": "bug", "color": "#ff0000"}
#         ]
#       },
#       "project": {
#         "id": "proj-789",
#         "name": "Q4 Release"
#       },
#       "team": {
#         "id": "team-123",
#         "name": "Engineering"
#       },
#       "createdAt": "2025-10-05T09:00:00Z",
#       "updatedAt": "2025-10-08T15:00:00Z",
#       "url": "https://linear.app/company/issue/ENG-123"
#     }
#   }
# }
```

#### `create_issue`
Create a new issue in Linear.

**Parameters:**
- `team_id` (string, required): Team ID
- `title` (string, required): Issue title
- `description` (string, optional): Issue description (markdown supported)
- `priority` (int, optional): Priority level (0=none, 1=urgent, 2=high, 3=medium, 4=low, default: 0)
- `assignee_id` (string, optional): Assignee user ID
- `project_id` (string, optional): Project ID
- `label_ids` (list of strings, optional): List of label IDs

**Priority Levels:**
- `0`: No priority
- `1`: Urgent (red)
- `2`: High (orange)
- `3`: Medium (yellow)
- `4`: Low (blue)

**Example:**
```python
# Simple issue
issue = await create_issue(
    team_id="team-123",
    title="Add dark mode support"
)

# Full issue with all fields
issue = await create_issue(
    team_id="team-123",
    title="Implement user dashboard",
    description="Create a personalized dashboard with:\n- Activity feed\n- Quick actions\n- Stats overview",
    priority=2,
    assignee_id="user-456",
    project_id="proj-789",
    label_ids=["label-123", "label-456"]
)

# Returns:
# {
#   "data": {
#     "issueCreate": {
#       "success": true,
#       "issue": {
#         "id": "issue-new-123",
#         "title": "Implement user dashboard",
#         "url": "https://linear.app/company/issue/ENG-124"
#       }
#     }
#   }
# }
```

#### `update_issue`
Update an existing issue.

**Parameters:**
- `issue_id` (string, required): Issue ID
- `title` (string, optional): Updated title
- `description` (string, optional): Updated description
- `priority` (int, optional): Updated priority (0-4)
- `state_id` (string, optional): Updated state ID
- `assignee_id` (string, optional): Updated assignee ID

**Example:**
```python
# Update title
result = await update_issue(
    issue_id="issue-123",
    title="Fix critical login bug"
)

# Update multiple fields
result = await update_issue(
    issue_id="issue-123",
    priority=1,
    assignee_id="user-789",
    description="Updated: Users getting 500 error on login"
)

# Change state
result = await update_issue(
    issue_id="issue-123",
    state_id="state-completed"
)

# Returns:
# {
#   "data": {
#     "issueUpdate": {
#       "success": true,
#       "issue": {
#         "id": "issue-123",
#         "title": "Fix critical login bug",
#         "state": {
#           "name": "Done"
#         }
#       }
#     }
#   }
# }
```

#### `delete_issue`
Delete an issue.

**Parameters:**
- `issue_id` (string, required): Issue ID

**Example:**
```python
result = await delete_issue(issue_id="issue-123")

# Returns:
# {
#   "data": {
#     "issueDelete": {
#       "success": true
#     }
#   }
# }
```

#### `add_comment`
Add a comment to an issue.

**Parameters:**
- `issue_id` (string, required): Issue ID
- `body` (string, required): Comment body (markdown supported)

**Example:**
```python
# Simple comment
comment = await add_comment(
    issue_id="issue-123",
    body="Working on this now"
)

# Markdown comment
comment = await add_comment(
    issue_id="issue-123",
    body="""## Update

- Completed API integration
- Testing authentication flow
- Need to review error handling

**ETA:** End of day"""
)

# Returns:
# {
#   "data": {
#     "commentCreate": {
#       "success": true,
#       "comment": {
#         "id": "comment-123",
#         "body": "Working on this now",
#         "createdAt": "2025-10-08T16:00:00Z"
#       }
#     }
#   }
# }
```

#### `search_issues`
Search issues with full-text query.

**Parameters:**
- `query_text` (string, required): Search query
- `first` (int, optional): Number of results (default: 20)

**Search Tips:**
- Search by title, description, or comments
- Use quotes for exact phrases: `"login bug"`
- Case-insensitive matching
- Returns most relevant results first

**Example:**
```python
# Simple search
results = await search_issues(query_text="authentication")

# Specific phrase
results = await search_issues(query_text="\"user login\"", first=10)

# Returns:
# {
#   "data": {
#     "issueSearch": {
#       "nodes": [
#         {
#           "id": "issue-123",
#           "title": "Fix authentication flow",
#           "description": "User login not working...",
#           "state": {"name": "In Progress"},
#           "assignee": {"name": "Jane Smith"},
#           "url": "https://linear.app/company/issue/ENG-123"
#         }
#       ]
#     }
#   }
# }
```

### Project Management

#### `list_projects`
List all projects in your workspace.

**Parameters:**
- `team_id` (string, optional): Filter by team ID
- `first` (int, optional): Number of projects to return (default: 50)

**Example:**
```python
# All projects
projects = await list_projects(first=20)

# Team projects
projects = await list_projects(team_id="team-123")

# Returns:
# {
#   "data": {
#     "projects": {
#       "nodes": [
#         {
#           "id": "proj-123",
#           "name": "Q4 2025 Release",
#           "description": "Major feature release...",
#           "state": "started",
#           "progress": 0.65,
#           "targetDate": "2025-12-31",
#           "lead": {
#             "id": "user-456",
#             "name": "John Doe"
#           },
#           "createdAt": "2025-09-01T00:00:00Z"
#         }
#       ]
#     }
#   }
# }
```

#### `get_project`
Get detailed project information.

**Parameters:**
- `project_id` (string, required): Project ID

**Example:**
```python
project = await get_project(project_id="proj-123")

# Returns:
# {
#   "data": {
#     "project": {
#       "id": "proj-123",
#       "name": "Mobile App Redesign",
#       "description": "Complete UI/UX overhaul...",
#       "state": "started",
#       "progress": 0.42,
#       "targetDate": "2026-01-31",
#       "startDate": "2025-10-01",
#       "lead": {
#         "id": "user-456",
#         "name": "Jane Smith"
#       },
#       "teams": {
#         "nodes": [
#           {"id": "team-123", "name": "Design"},
#           {"id": "team-456", "name": "Engineering"}
#         ]
#       },
#       "url": "https://linear.app/company/project/redesign"
#     }
#   }
# }
```

#### `create_project`
Create a new project.

**Parameters:**
- `name` (string, required): Project name
- `team_ids` (list of strings, required): List of team IDs
- `description` (string, optional): Project description
- `target_date` (string, optional): Target completion date (YYYY-MM-DD)
- `lead_id` (string, optional): Project lead user ID

**Example:**
```python
# Simple project
project = await create_project(
    name="API v2 Migration",
    team_ids=["team-123"]
)

# Full project
project = await create_project(
    name="Customer Portal",
    team_ids=["team-123", "team-456"],
    description="Self-service customer dashboard with billing and support",
    target_date="2026-03-31",
    lead_id="user-789"
)

# Returns:
# {
#   "data": {
#     "projectCreate": {
#       "success": true,
#       "project": {
#         "id": "proj-new-123",
#         "name": "Customer Portal",
#         "url": "https://linear.app/company/project/customer-portal"
#       }
#     }
#   }
# }
```

#### `list_milestones`
List project milestones.

**Parameters:**
- `project_id` (string, optional): Filter by project ID
- `first` (int, optional): Number of milestones (default: 50)

**Example:**
```python
# All milestones
milestones = await list_milestones(first=20)

# Project milestones
milestones = await list_milestones(project_id="proj-123")

# Returns:
# {
#   "data": {
#     "projectMilestones": {
#       "nodes": [
#         {
#           "id": "milestone-123",
#           "name": "Beta Release",
#           "description": "Feature-complete beta version",
#           "targetDate": "2025-11-30",
#           "project": {
#             "id": "proj-123",
#             "name": "Q4 Release"
#           }
#         }
#       ]
#     }
#   }
# }
```

#### `get_roadmap`
Get roadmap view of all projects.

**Parameters:**
- `first` (int, optional): Number of items (default: 50)

**Example:**
```python
roadmap = await get_roadmap(first=30)

# Returns:
# {
#   "data": {
#     "projects": {
#       "nodes": [
#         {
#           "id": "proj-123",
#           "name": "Mobile App v2",
#           "description": "Next generation mobile experience",
#           "state": "started",
#           "progress": 0.35,
#           "targetDate": "2026-02-28",
#           "startDate": "2025-10-01",
#           "lead": {"name": "Jane Smith"}
#         }
#       ]
#     }
#   }
# }
```

### Team Management

#### `list_teams`
List all teams in your workspace.

**Example:**
```python
teams = await list_teams()

# Returns:
# {
#   "data": {
#     "teams": {
#       "nodes": [
#         {
#           "id": "team-123",
#           "name": "Engineering",
#           "key": "ENG",
#           "description": "Product development team",
#           "private": false,
#           "createdAt": "2025-01-01T00:00:00Z"
#         }
#       ]
#     }
#   }
# }
```

#### `get_team`
Get detailed team information.

**Parameters:**
- `team_id` (string, required): Team ID

**Example:**
```python
team = await get_team(team_id="team-123")

# Returns:
# {
#   "data": {
#     "team": {
#       "id": "team-123",
#       "name": "Engineering",
#       "key": "ENG",
#       "description": "Product development team",
#       "private": false,
#       "members": {
#         "nodes": [
#           {
#             "id": "user-123",
#             "name": "Jane Smith",
#             "email": "jane@company.com"
#           }
#         ]
#       },
#       "projects": {
#         "nodes": [
#           {"id": "proj-123", "name": "Q4 Release"}
#         ]
#       }
#     }
#   }
# }
```

### Sprint Management

#### `list_cycles`
List sprint cycles.

**Parameters:**
- `team_id` (string, optional): Filter by team ID
- `first` (int, optional): Number of cycles (default: 20)

**Example:**
```python
# All cycles
cycles = await list_cycles(first=10)

# Team cycles
cycles = await list_cycles(team_id="team-123")

# Returns:
# {
#   "data": {
#     "cycles": {
#       "nodes": [
#         {
#           "id": "cycle-123",
#           "number": 42,
#           "name": "Sprint 42",
#           "startsAt": "2025-10-07T00:00:00Z",
#           "endsAt": "2025-10-20T23:59:59Z",
#           "progress": 0.58,
#           "completedIssueCount": 12,
#           "issueCount": 18,
#           "team": {
#             "id": "team-123",
#             "name": "Engineering"
#           }
#         }
#       ]
#     }
#   }
# }
```

#### `get_cycle`
Get detailed cycle information.

**Parameters:**
- `cycle_id` (string, required): Cycle ID

**Example:**
```python
cycle = await get_cycle(cycle_id="cycle-123")

# Returns:
# {
#   "data": {
#     "cycle": {
#       "id": "cycle-123",
#       "number": 42,
#       "name": "Sprint 42",
#       "description": "Focus on authentication improvements",
#       "startsAt": "2025-10-07T00:00:00Z",
#       "endsAt": "2025-10-20T23:59:59Z",
#       "progress": 0.58,
#       "completedIssueCount": 12,
#       "issueCount": 18,
#       "team": {
#         "id": "team-123",
#         "name": "Engineering"
#       },
#       "url": "https://linear.app/company/cycle/42"
#     }
#   }
# }
```

### Labels & Organization

#### `list_labels`
List all labels.

**Parameters:**
- `team_id` (string, optional): Filter by team ID

**Example:**
```python
# All labels
labels = await list_labels()

# Team labels
labels = await list_labels(team_id="team-123")

# Returns:
# {
#   "data": {
#     "issueLabels": {
#       "nodes": [
#         {
#           "id": "label-123",
#           "name": "bug",
#           "description": "Something isn't working",
#           "color": "#ff0000",
#           "team": {
#             "id": "team-123",
#             "name": "Engineering"
#           }
#         }
#       ]
#     }
#   }
# }
```

#### `create_label`
Create a new label.

**Parameters:**
- `name` (string, required): Label name
- `team_id` (string, required): Team ID
- `color` (string, optional): Hex color code (e.g., "#FF0000")
- `description` (string, optional): Label description

**Example:**
```python
# Simple label
label = await create_label(
    name="security",
    team_id="team-123"
)

# Full label
label = await create_label(
    name="performance",
    team_id="team-123",
    color="#FFA500",
    description="Performance optimization tasks"
)

# Returns:
# {
#   "data": {
#     "issueLabelCreate": {
#       "success": true,
#       "issueLabel": {
#         "id": "label-new-123",
#         "name": "performance",
#         "color": "#FFA500"
#       }
#     }
#   }
# }
```

## Common Workflows

### Daily Standup Preparation
```python
# Get team's current sprint
cycles = await list_cycles(team_id="team-123", first=1)
current_cycle = cycles["data"]["cycles"]["nodes"][0]

# Get my active issues
my_issues = await list_issues(
    assignee_id="user-456",
    state="started",
    first=10
)

# Check recently completed issues
completed = await list_issues(
    assignee_id="user-456",
    state="completed",
    first=5
)
```

### Sprint Planning
```python
# Get upcoming cycle
cycle = await get_cycle(cycle_id="cycle-123")

# Review backlog issues
backlog = await list_issues(
    team_id="team-123",
    state="backlog",
    first=50
)

# Create sprint issues
for item in sprint_plan:
    issue = await create_issue(
        team_id="team-123",
        title=item["title"],
        description=item["description"],
        priority=item["priority"],
        assignee_id=item["assignee"]
    )
```

### Bug Triage
```python
# Get all bugs
bugs = await search_issues(query_text="bug", first=30)

# Or use label filter
bugs = await list_issues(label_id="label-bug-123")

# Prioritize urgent bugs
for bug in urgent_bugs:
    await update_issue(
        issue_id=bug["id"],
        priority=1,
        state_id="state-started"
    )

    await add_comment(
        issue_id=bug["id"],
        body="Escalated to urgent - investigating now"
    )
```

### Project Status Update
```python
# Get project details
project = await get_project(project_id="proj-123")

# Get project milestones
milestones = await list_milestones(project_id="proj-123")

# Get issues for project
issues = await list_issues(project_id="proj-123", first=100)

# Calculate metrics
total = len(issues["data"]["issues"]["nodes"])
completed = len([i for i in issues["data"]["issues"]["nodes"]
                 if i["state"]["type"] == "completed"])
progress = completed / total if total > 0 else 0
```

### Roadmap Planning
```python
# Get all active projects
roadmap = await get_roadmap(first=50)

# Create new quarterly project
project = await create_project(
    name="Q1 2026 Infrastructure",
    team_ids=["team-123"],
    description="Scale infrastructure for 10x growth",
    target_date="2026-03-31",
    lead_id="user-789"
)

# Add milestones (would need milestone creation tool)
# Add initial issues
for initiative in initiatives:
    await create_issue(
        team_id="team-123",
        project_id=project["data"]["projectCreate"]["project"]["id"],
        title=initiative["title"],
        description=initiative["description"]
    )
```

### Team Performance Metrics
```python
# Get team info
team = await get_team(team_id="team-123")

# Get current cycle
cycles = await list_cycles(team_id="team-123", first=1)
cycle = cycles["data"]["cycles"]["nodes"][0]

# Calculate velocity
completed = cycle["completedIssueCount"]
total = cycle["issueCount"]
velocity = completed / total if total > 0 else 0

# Get member contributions
for member in team["data"]["team"]["members"]["nodes"]:
    member_issues = await list_issues(
        assignee_id=member["id"],
        first=100
    )
```

## Issue States

Linear uses a workflow with these standard state types:

- **backlog**: Not yet scheduled
- **unstarted**: Planned but not started
- **started**: Currently in progress
- **completed**: Done and verified
- **canceled**: Won't be completed

Teams can customize state names (e.g., "In Review", "Testing") while keeping these types.

## Priority Levels

| Level | Name | Color | Use Case |
|-------|------|-------|----------|
| 0 | None | Gray | Default, no urgency |
| 1 | Urgent | Red | Critical issues, production down |
| 2 | High | Orange | Important features, significant bugs |
| 3 | Medium | Yellow | Standard work, normal priority |
| 4 | Low | Blue | Nice-to-have, low impact |

## Best Practices

1. **Use team_id filters**: Narrow down results for better performance
2. **Pagination**: Use `first` parameter to limit results
3. **Specific queries**: Request only the fields you need
4. **Batch operations**: Group related changes together
5. **State management**: Follow your team's workflow states
6. **Labels**: Use consistent labeling for better filtering
7. **Search wisely**: Use specific terms for better search results
8. **Cache data**: Don't repeatedly fetch unchanged data
9. **Error handling**: Implement retries with backoff
10. **Monitor rate limits**: Track API usage

## GraphQL Tips

### Request Only Needed Fields
```python
# Good - minimal fields
query = """
  query {
    issues(first: 10) {
      nodes { id title }
    }
  }
"""

# Avoid - too many unnecessary fields
query = """
  query {
    issues(first: 10) {
      nodes {
        id title description priority
        state { ... }
        assignee { ... }
        # many more fields
      }
    }
  }
"""
```

### Use Filters Effectively
```python
# Good - specific filters
issues = await list_issues(
    team_id="team-123",
    state="started",
    first=10
)

# Less efficient - fetch everything then filter
all_issues = await list_issues(first=1000)
# then filter in Python
```

### Pagination
```python
# For large datasets, use pagination
first_page = await list_issues(first=50)
# Get cursor from last item for next page
# Linear supports cursor-based pagination
```

## Error Handling

Common GraphQL errors:

- **Authentication failed**: Invalid or expired API key
- **Not found**: Resource ID doesn't exist
- **Rate limited**: Too many requests
- **Validation error**: Invalid input parameters
- **Insufficient permissions**: User lacks access

All tools return GraphQL response format:
```json
{
  "data": { ... },
  "errors": [
    {
      "message": "Error description",
      "extensions": { "code": "ERROR_CODE" }
    }
  ]
}
```

## API Documentation

- [Linear API Documentation](https://developers.linear.app/)
- [GraphQL API Reference](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Schema Explorer](https://studio.apollographql.com/public/Linear-API/home)
- [Webhooks](https://developers.linear.app/docs/graphql/webhooks)
- [OAuth](https://developers.linear.app/docs/oauth/authentication)

## Support

- [Help Center](https://linear.app/help)
- [Community Slack](https://linear.app/join-slack)
- [GitHub Discussions](https://github.com/linearapp/linear/discussions)
- [Twitter](https://twitter.com/linear)
