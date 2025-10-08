# Asana MCP Server

MCP server for Asana API. Complete work management platform for task tracking, project planning, team collaboration, and workflow automation. Organize work across workspaces, projects, sections, and tasks.

## Features

- **Workspace Management**: Access multiple workspaces and organizations
- **Project Planning**: Create and manage projects with timelines
- **Task Management**: Full task lifecycle from creation to completion
- **Sections**: Organize tasks within projects using sections
- **Tags**: Flexible categorization across projects
- **Portfolios**: Group and track multiple projects
- **Collaboration**: Assignees, followers, and comments
- **Custom Fields**: Add metadata to tasks and projects
- **Search**: Find tasks, projects, and users quickly
- **Team Coordination**: Share work and track progress

## Setup

### Prerequisites

- Asana account (free or paid plan)
- Personal Access Token

### Environment Variables

- `ASANA_PERSONAL_ACCESS_TOKEN` (required): Your Asana Personal Access Token

**How to get credentials:**

1. Go to [app.asana.com/0/my-apps](https://app.asana.com/0/my-apps)
2. Sign in to your Asana account
3. Click on "My Profile Settings" in the top right
4. Select the "Apps" tab
5. Scroll to "Personal access tokens"
6. Click "Create new token"
7. Enter a token name (e.g., "MCP Server")
8. Click "Create token"
9. Copy the token immediately (it won't be shown again)
10. Store as `ASANA_PERSONAL_ACCESS_TOKEN`

**Token Format:**
- Format: `0/1234567890abcdef...`
- Full access to your account
- Keep secure - treat like a password

## Rate Limits

**Standard Rate Limits:**
- 1,500 requests per minute per token
- 150 concurrent requests
- Burst capacity for short spikes

**Premium Plans:**
- Higher rate limits available
- Contact Asana for enterprise limits

**Best Practices:**
- Use pagination for large result sets
- Cache data when appropriate
- Implement exponential backoff
- Monitor rate limit headers

## Asana Hierarchy

Asana organizes work in this hierarchy:

```
Workspace/Organization
  └── Project
      └── Section
          └── Task
              └── Subtask
```

- **Workspace**: Top-level container for teams
- **Project**: Collection of tasks for a goal
- **Section**: Organize tasks within projects
- **Task**: Individual work item
- **Subtask**: Break down tasks into smaller steps

## Available Tools

### Workspace Management

#### `list_workspaces`
List all workspaces you have access to.

**Parameters:**
- `limit` (int, optional): Results per page (default: 20, max: 100)
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
workspaces = await list_workspaces(limit=20)

# With specific fields
workspaces = await list_workspaces(
    limit=10,
    opt_fields="name,is_organization"
)

# Returns:
# {
#   "data": [
#     {
#       "gid": "1234567890",
#       "name": "My Company",
#       "resource_type": "workspace",
#       "is_organization": true
#     }
#   ]
# }
```

### Project Management

#### `list_projects`
List projects in a workspace.

**Parameters:**
- `workspace` (string, required): Workspace GID
- `archived` (bool, optional): Include archived projects (default: false)
- `limit` (int, optional): Results per page (default: 20, max: 100)
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
# Active projects
projects = await list_projects(workspace="1234567890")

# Include archived
projects = await list_projects(
    workspace="1234567890",
    archived=True
)

# With specific fields
projects = await list_projects(
    workspace="1234567890",
    opt_fields="name,due_date,owner,color"
)

# Returns:
# {
#   "data": [
#     {
#       "gid": "9876543210",
#       "name": "Website Redesign",
#       "resource_type": "project"
#     }
#   ]
# }
```

#### `get_project`
Get detailed information about a project.

**Parameters:**
- `project_gid` (string, required): Project GID
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
project = await get_project(project_gid="9876543210")

# With all fields
project = await get_project(
    project_gid="9876543210",
    opt_fields="name,notes,due_date,start_date,color,owner,team,members,archived,public,created_at,modified_at"
)

# Returns:
# {
#   "data": {
#     "gid": "9876543210",
#     "name": "Website Redesign",
#     "notes": "Complete redesign of company website",
#     "due_date": "2025-12-31",
#     "start_date": "2025-10-01",
#     "color": "light-blue",
#     "owner": {
#       "gid": "1111111111",
#       "name": "John Doe"
#     },
#     "team": {
#       "gid": "2222222222",
#       "name": "Marketing"
#     },
#     "archived": false,
#     "public": true,
#     "created_at": "2025-10-01T00:00:00.000Z",
#     "modified_at": "2025-10-08T15:00:00.000Z"
#   }
# }
```

#### `create_project`
Create a new project.

**Parameters:**
- `workspace` (string, required): Workspace GID
- `name` (string, required): Project name
- `notes` (string, optional): Project description
- `color` (string, optional): Project color (see color list below)
- `due_date` (string, optional): Due date (YYYY-MM-DD)
- `start_date` (string, optional): Start date (YYYY-MM-DD)
- `public` (bool, optional): Public to organization (default: true)

**Project Colors:**
- Light: light-pink, light-green, light-orange, light-yellow, light-teal, light-blue, light-purple, light-warm-gray
- Dark: dark-pink, dark-green, dark-orange, dark-yellow, dark-teal, dark-blue, dark-purple, dark-warm-gray

**Example:**
```python
# Simple project
project = await create_project(
    workspace="1234567890",
    name="Q4 Marketing Campaign"
)

# Full project
project = await create_project(
    workspace="1234567890",
    name="Product Launch",
    notes="Launch new product line in Q1 2026",
    color="light-blue",
    due_date="2026-03-31",
    start_date="2025-11-01",
    public=True
)

# Returns:
# {
#   "data": {
#     "gid": "9876543211",
#     "name": "Product Launch",
#     "notes": "Launch new product line in Q1 2026",
#     "color": "light-blue",
#     "due_date": "2026-03-31",
#     "start_date": "2025-11-01",
#     "public": true
#   }
# }
```

### Task Management

#### `list_tasks`
List tasks with filters.

**Parameters:**
- `project` (string, optional): Filter by project GID
- `section` (string, optional): Filter by section GID
- `assignee` (string, optional): Filter by assignee GID (or "me")
- `workspace` (string, optional): Workspace GID (required if not using project/section)
- `completed_since` (string, optional): Tasks completed after this time (ISO 8601)
- `modified_since` (string, optional): Tasks modified after this time (ISO 8601)
- `limit` (int, optional): Results per page (default: 20, max: 100)
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
# All tasks in project
tasks = await list_tasks(project="9876543210")

# My tasks
tasks = await list_tasks(
    workspace="1234567890",
    assignee="me"
)

# Tasks in section
tasks = await list_tasks(section="5555555555")

# Recently completed
tasks = await list_tasks(
    project="9876543210",
    completed_since="2025-10-01T00:00:00Z"
)

# With specific fields
tasks = await list_tasks(
    project="9876543210",
    opt_fields="name,completed,due_on,assignee,tags"
)

# Returns:
# {
#   "data": [
#     {
#       "gid": "1111111111",
#       "name": "Design homepage mockup",
#       "resource_type": "task"
#     }
#   ]
# }
```

#### `get_task`
Get detailed information about a task.

**Parameters:**
- `task_gid` (string, required): Task GID
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
task = await get_task(task_gid="1111111111")

# With all fields
task = await get_task(
    task_gid="1111111111",
    opt_fields="name,notes,completed,assignee,due_on,start_on,tags,projects,memberships,num_subtasks,parent,followers,created_at,modified_at"
)

# Returns:
# {
#   "data": {
#     "gid": "1111111111",
#     "name": "Design homepage mockup",
#     "notes": "Create high-fidelity mockup for new homepage design",
#     "completed": false,
#     "assignee": {
#       "gid": "2222222222",
#       "name": "Jane Smith"
#     },
#     "due_on": "2025-10-15",
#     "start_on": "2025-10-08",
#     "tags": [
#       {"gid": "3333333333", "name": "design"}
#     ],
#     "projects": [
#       {"gid": "9876543210", "name": "Website Redesign"}
#     ],
#     "num_subtasks": 3,
#     "parent": null,
#     "created_at": "2025-10-01T10:00:00.000Z",
#     "modified_at": "2025-10-08T14:30:00.000Z"
#   }
# }
```

#### `create_task`
Create a new task.

**Parameters:**
- `workspace` (string, optional): Workspace GID (required if projects not provided)
- `projects` (list of strings, optional): Project GIDs to add task to
- `name` (string, optional): Task name (default: empty)
- `notes` (string, optional): Task description
- `assignee` (string, optional): Assignee GID (or "me")
- `due_on` (string, optional): Due date (YYYY-MM-DD)
- `start_on` (string, optional): Start date (YYYY-MM-DD)
- `tags` (list of strings, optional): Tag GIDs

**Example:**
```python
# Simple task
task = await create_task(
    workspace="1234567890",
    name="Review quarterly reports"
)

# Task in project
task = await create_task(
    projects=["9876543210"],
    name="Design homepage mockup"
)

# Full task
task = await create_task(
    projects=["9876543210"],
    name="Implement user authentication",
    notes="Add OAuth2 support for Google and GitHub",
    assignee="me",
    due_on="2025-10-31",
    start_on="2025-10-15",
    tags=["3333333333", "4444444444"]
)

# Returns:
# {
#   "data": {
#     "gid": "1111111112",
#     "name": "Implement user authentication",
#     "notes": "Add OAuth2 support for Google and GitHub",
#     "assignee": {"gid": "2222222222", "name": "John Doe"},
#     "due_on": "2025-10-31",
#     "start_on": "2025-10-15"
#   }
# }
```

#### `update_task`
Update task details.

**Parameters:**
- `task_gid` (string, required): Task GID
- `name` (string, optional): Updated name
- `notes` (string, optional): Updated description
- `assignee` (string, optional): Updated assignee GID (or "me", or null to unassign)
- `due_on` (string, optional): Updated due date (YYYY-MM-DD, or null to clear)
- `start_on` (string, optional): Updated start date (YYYY-MM-DD, or null to clear)
- `completed` (bool, optional): Completion status

**Example:**
```python
# Update name
task = await update_task(
    task_gid="1111111111",
    name="Updated task name"
)

# Assign task
task = await update_task(
    task_gid="1111111111",
    assignee="2222222222"
)

# Set due date
task = await update_task(
    task_gid="1111111111",
    due_on="2025-10-20"
)

# Multiple updates
task = await update_task(
    task_gid="1111111111",
    name="Design homepage mockup (final)",
    notes="Final version incorporating feedback",
    due_on="2025-10-18",
    completed=False
)

# Unassign task
task = await update_task(
    task_gid="1111111111",
    assignee=None
)

# Returns:
# {
#   "data": {
#     "gid": "1111111111",
#     "name": "Design homepage mockup (final)",
#     ...
#   }
# }
```

#### `complete_task`
Mark task as complete.

**Parameters:**
- `task_gid` (string, required): Task GID

**Example:**
```python
task = await complete_task(task_gid="1111111111")

# Returns:
# {
#   "data": {
#     "gid": "1111111111",
#     "completed": true,
#     "completed_at": "2025-10-08T16:00:00.000Z"
#   }
# }
```

#### `delete_task`
Delete a task permanently.

**Parameters:**
- `task_gid` (string, required): Task GID

**Example:**
```python
result = await delete_task(task_gid="1111111111")

# Returns:
# {
#   "data": {}
# }
```

#### `add_task_comment`
Add a comment (story) to a task.

**Parameters:**
- `task_gid` (string, required): Task GID
- `text` (string, required): Comment text

**Example:**
```python
comment = await add_task_comment(
    task_gid="1111111111",
    text="Updated the mockup with client feedback"
)

# Multi-line comment
comment = await add_task_comment(
    task_gid="1111111111",
    text="Status update:\n\n- Completed initial design\n- Sent to client for review\n- Awaiting feedback"
)

# Returns:
# {
#   "data": {
#     "gid": "5555555556",
#     "text": "Updated the mockup with client feedback",
#     "created_at": "2025-10-08T16:15:00.000Z",
#     "created_by": {
#       "gid": "2222222222",
#       "name": "John Doe"
#     }
#   }
# }
```

### Section Management

#### `list_sections`
List sections in a project.

**Parameters:**
- `project_gid` (string, required): Project GID
- `limit` (int, optional): Results per page (default: 20, max: 100)
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
sections = await list_sections(project_gid="9876543210")

# With specific fields
sections = await list_sections(
    project_gid="9876543210",
    opt_fields="name,created_at"
)

# Returns:
# {
#   "data": [
#     {
#       "gid": "5555555555",
#       "name": "To Do",
#       "resource_type": "section"
#     },
#     {
#       "gid": "5555555556",
#       "name": "In Progress",
#       "resource_type": "section"
#     },
#     {
#       "gid": "5555555557",
#       "name": "Done",
#       "resource_type": "section"
#     }
#   ]
# }
```

#### `create_section`
Create a section in a project.

**Parameters:**
- `project_gid` (string, required): Project GID
- `name` (string, required): Section name

**Example:**
```python
section = await create_section(
    project_gid="9876543210",
    name="Ready for Review"
)

# Returns:
# {
#   "data": {
#     "gid": "5555555558",
#     "name": "Ready for Review",
#     "project": {
#       "gid": "9876543210",
#       "name": "Website Redesign"
#     }
#   }
# }
```

### Tag Management

#### `list_tags`
List tags in a workspace.

**Parameters:**
- `workspace` (string, required): Workspace GID
- `limit` (int, optional): Results per page (default: 20, max: 100)
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
tags = await list_tags(workspace="1234567890")

# With specific fields
tags = await list_tags(
    workspace="1234567890",
    opt_fields="name,color,created_at"
)

# Returns:
# {
#   "data": [
#     {
#       "gid": "3333333333",
#       "name": "design",
#       "resource_type": "tag"
#     },
#     {
#       "gid": "3333333334",
#       "name": "urgent",
#       "resource_type": "tag"
#     }
#   ]
# }
```

#### `create_tag`
Create a new tag.

**Parameters:**
- `workspace` (string, required): Workspace GID
- `name` (string, required): Tag name
- `color` (string, optional): Tag color (see color list below)

**Tag Colors:**
- Dark: dark-pink, dark-green, dark-blue, dark-red, dark-teal, dark-brown, dark-orange, dark-purple, dark-warm-gray
- Light: light-pink, light-green, light-blue, light-red, light-teal, light-brown, light-orange, light-purple, light-warm-gray
- None: none (no color)

**Example:**
```python
# Simple tag
tag = await create_tag(
    workspace="1234567890",
    name="frontend"
)

# Tag with color
tag = await create_tag(
    workspace="1234567890",
    name="critical",
    color="dark-red"
)

# Returns:
# {
#   "data": {
#     "gid": "3333333335",
#     "name": "critical",
#     "color": "dark-red"
#   }
# }
```

### Search

#### `search_workspace`
Search for tasks, projects, users, portfolios, or tags.

**Parameters:**
- `workspace` (string, required): Workspace GID
- `resource_type` (string, required): Type to search (task, project, user, portfolio, tag)
- `query` (string, required): Search query
- `limit` (int, optional): Results per page (default: 20, max: 100)
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
# Search tasks
tasks = await search_workspace(
    workspace="1234567890",
    resource_type="task",
    query="design"
)

# Search projects
projects = await search_workspace(
    workspace="1234567890",
    resource_type="project",
    query="website"
)

# Search users
users = await search_workspace(
    workspace="1234567890",
    resource_type="user",
    query="john"
)

# Returns:
# {
#   "data": [
#     {
#       "gid": "1111111111",
#       "name": "Design homepage mockup",
#       "resource_type": "task"
#     }
#   ]
# }
```

### Portfolio Management

#### `list_portfolios`
List portfolios in a workspace.

**Parameters:**
- `workspace` (string, required): Workspace GID
- `owner` (string, optional): Filter by owner GID (or "me")
- `limit` (int, optional): Results per page (default: 20, max: 100)
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
# All portfolios
portfolios = await list_portfolios(workspace="1234567890")

# My portfolios
portfolios = await list_portfolios(
    workspace="1234567890",
    owner="me"
)

# With specific fields
portfolios = await list_portfolios(
    workspace="1234567890",
    opt_fields="name,color,created_at,owner"
)

# Returns:
# {
#   "data": [
#     {
#       "gid": "7777777777",
#       "name": "Product Development",
#       "resource_type": "portfolio"
#     }
#   ]
# }
```

### User Management

#### `get_user`
Get user details.

**Parameters:**
- `user_gid` (string, required): User GID (or "me" for current user)
- `opt_fields` (string, optional): Comma-separated fields to include

**Example:**
```python
# Current user
user = await get_user(user_gid="me")

# Specific user
user = await get_user(user_gid="2222222222")

# With all fields
user = await get_user(
    user_gid="me",
    opt_fields="name,email,photo,workspaces"
)

# Returns:
# {
#   "data": {
#     "gid": "2222222222",
#     "name": "John Doe",
#     "email": "john@example.com",
#     "photo": {
#       "image_128x128": "https://...",
#       "image_60x60": "https://..."
#     },
#     "workspaces": [
#       {
#         "gid": "1234567890",
#         "name": "My Company"
#       }
#     ]
#   }
# }
```

## Common Workflows

### Daily Task Management
```python
# Get my tasks
my_tasks = await list_tasks(
    workspace="1234567890",
    assignee="me",
    opt_fields="name,due_on,completed"
)

# Complete a task
await complete_task(task_gid="1111111111")

# Add progress update
await add_task_comment(
    task_gid="1111111111",
    text="Completed the first draft"
)
```

### Project Setup
```python
# Create project
project = await create_project(
    workspace="1234567890",
    name="Website Redesign",
    due_date="2025-12-31",
    color="light-blue"
)

# Create sections
await create_section(
    project_gid=project["data"]["gid"],
    name="To Do"
)
await create_section(
    project_gid=project["data"]["gid"],
    name="In Progress"
)
await create_section(
    project_gid=project["data"]["gid"],
    name="Done"
)

# Create initial tasks
await create_task(
    projects=[project["data"]["gid"]],
    name="Create wireframes",
    assignee="me",
    due_on="2025-10-20"
)
```

### Team Collaboration
```python
# Search for team member
users = await search_workspace(
    workspace="1234567890",
    resource_type="user",
    query="jane"
)

# Assign task to team member
await update_task(
    task_gid="1111111111",
    assignee=users["data"][0]["gid"]
)

# Add comment with @mention
await add_task_comment(
    task_gid="1111111111",
    text="@Jane Smith - Can you review this design?"
)
```

### Progress Tracking
```python
# Get project details
project = await get_project(
    project_gid="9876543210",
    opt_fields="name,completed_count,num_tasks"
)

# Get tasks by section
sections = await list_sections(project_gid="9876543210")
for section in sections["data"]:
    tasks = await list_tasks(
        section=section["gid"],
        opt_fields="name,completed"
    )
    # Calculate section progress
```

### Task Organization
```python
# Create tags for categorization
design_tag = await create_tag(
    workspace="1234567890",
    name="design",
    color="light-purple"
)

dev_tag = await create_tag(
    workspace="1234567890",
    name="development",
    color="light-blue"
)

# Create task with tags
await create_task(
    projects=["9876543210"],
    name="Implement responsive layout",
    tags=[design_tag["data"]["gid"], dev_tag["data"]["gid"]]
)
```

## Custom Fields

Asana supports custom fields for adding metadata to tasks:

- **Text**: Free-form text input
- **Number**: Numeric values
- **Dropdown**: Select from predefined options
- **Date**: Date picker
- **Checkbox**: Yes/no values
- **People**: User selection
- **Currency**: Monetary values

Custom fields require Premium or higher plans.

## Task Dependencies

Tasks can have dependencies (requires Premium or higher):

- **Predecessor**: Task that must complete before this one
- **Successor**: Task that depends on this one completing

## Best Practices

1. **Use workspaces wisely**: Organize by company or major divisions
2. **Structure projects**: Use sections for workflow stages
3. **Tag consistently**: Create tag taxonomy for categorization
4. **Set due dates**: Track deadlines and milestones
5. **Assign work**: Clear ownership and accountability
6. **Add context**: Use task descriptions and comments
7. **Use opt_fields**: Fetch only needed data for performance
8. **Pagination**: Use limit parameter for large datasets
9. **Search effectively**: Use specific queries for better results
10. **Cache data**: Avoid repeated fetching of unchanged data

## GID Format

Asana uses GIDs (Global IDs) for resources:

- Format: String of digits (e.g., "1234567890")
- Always use as strings, not integers
- Unique across all Asana
- Required for all resource-specific operations

## Response Format

All Asana API responses wrap data in a `data` field:

```json
{
  "data": {
    "gid": "1234567890",
    "name": "Example",
    ...
  }
}
```

Or for lists:

```json
{
  "data": [
    {"gid": "1234567890", "name": "Item 1"},
    {"gid": "1234567891", "name": "Item 2"}
  ]
}
```

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid or expired token
- **402 Payment Required**: Premium feature on free plan
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist or no access
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error (retry)

## API Documentation

- [Asana API Documentation](https://developers.asana.com/docs)
- [Personal Access Tokens](https://developers.asana.com/docs/personal-access-token)
- [API Reference](https://developers.asana.com/reference)
- [Task Guide](https://developers.asana.com/docs/tasks)
- [Project Guide](https://developers.asana.com/docs/projects)
- [Custom Fields](https://developers.asana.com/docs/custom-fields)
- [Rate Limits](https://developers.asana.com/docs/rate-limits)

## Support

- [Help Center](https://asana.com/support)
- [Developer Forum](https://forum.asana.com/)
- [API Status](https://status.asana.com/)
- [Contact Support](https://asana.com/support/contact)
