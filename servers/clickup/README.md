# ClickUp MCP Server

MCP server for ClickUp API. Manage projects, tasks, time tracking, goals, and team collaboration with a flexible hierarchical project management system.

## Features

- **Hierarchical Organization**: Workspace → Space → Folder → List → Task
- **Task Management**: Create, update, and track tasks with custom fields
- **Time Tracking**: Log time entries and estimates
- **Goals**: Set and track goals with progress metrics
- **Custom Fields**: Flexible metadata for tasks
- **Collaboration**: Comments, assignments, and notifications
- **Search**: Find tasks across your workspace
- **Statuses**: Customizable per-list status workflows

## Setup

### Prerequisites

- ClickUp account (free or paid)
- API token

### Environment Variables

- `CLICKUP_API_TOKEN` (required): Your ClickUp API token

**How to get credentials:**
1. Go to [app.clickup.com](https://app.clickup.com/)
2. Log in to your account
3. Click your avatar → Settings
4. Go to "Apps" in the sidebar
5. Click "Generate" under "API Token"
6. Copy the token (starts with `pk_`)
7. Store as `CLICKUP_API_TOKEN`

Direct link: https://app.clickup.com/settings/apps

**Important**: Keep your API token secure. It has full access to your ClickUp account.

## Rate Limits

- **Standard**: 100 requests per minute per token
- Rate limit headers included in responses
- HTTP 429 response when limit exceeded
- Consider caching for frequently accessed data

## Hierarchy Overview

ClickUp uses a hierarchical structure:

```
Workspace (Team)
  └─ Space
      ├─ Folder (optional)
      │   └─ List
      │       └─ Task
      │           └─ Subtask
      └─ List (folderless)
          └─ Task
```

## Available Tools

### Workspace & Space Management

#### `list_workspaces`
List all accessible workspaces (teams).

**Example:**
```python
workspaces = await list_workspaces()

# Returns:
# {
#   "teams": [
#     {
#       "id": "123",
#       "name": "My Workspace",
#       "color": "#FF0000",
#       "avatar": "https://...",
#       "members": [...]
#     }
#   ]
# }
```

#### `list_spaces`
List spaces in a workspace.

**Parameters:**
- `workspace_id` (string, required): Workspace ID
- `archived` (bool, optional): Include archived (default: false)

**Example:**
```python
spaces = await list_spaces(workspace_id="123")

# Returns:
# {
#   "spaces": [
#     {
#       "id": "456",
#       "name": "Marketing",
#       "private": false,
#       "statuses": [...],
#       "multiple_assignees": true,
#       "features": {
#         "due_dates": {"enabled": true},
#         "time_tracking": {"enabled": true}
#       }
#     }
#   ]
# }
```

#### `get_space`
Get space details.

**Parameters:**
- `space_id` (string, required): Space ID

**Example:**
```python
space = await get_space(space_id="456")
```

### Folder & List Management

#### `list_folders`
List folders in a space.

**Parameters:**
- `space_id` (string, required): Space ID
- `archived` (bool, optional): Include archived (default: false)

**Example:**
```python
folders = await list_folders(space_id="456")

# Returns:
# {
#   "folders": [
#     {
#       "id": "789",
#       "name": "Q4 Campaigns",
#       "orderindex": 0,
#       "task_count": 15,
#       "lists": [...]
#     }
#   ]
# }
```

#### `list_lists`
List lists in a folder or space.

**Parameters:**
- `folder_id` (string, optional): Folder ID
- `space_id` (string, optional): Space ID (for folderless lists)
- `archived` (bool, optional): Include archived (default: false)

**Example:**
```python
# Lists in a folder
lists = await list_lists(folder_id="789")

# Folderless lists in a space
lists = await list_lists(space_id="456")

# Returns:
# {
#   "lists": [
#     {
#       "id": "abc123",
#       "name": "Sprint Backlog",
#       "orderindex": 0,
#       "status": {
#         "status": "active",
#         "color": "#87909e"
#       },
#       "task_count": 42
#     }
#   ]
# }
```

### Task Management

#### `list_tasks`
List tasks with filters.

**Parameters:**
- `list_id` (string, required): List ID
- `archived` (bool, optional): Include archived (default: false)
- `page` (int, optional): Page number (default: 0)
- `order_by` (string, optional): Order by (created, updated, due_date)
- `reverse` (bool, optional): Reverse order (default: true)
- `subtasks` (bool, optional): Include subtasks (default: true)
- `statuses` (list, optional): Filter by status names
- `include_closed` (bool, optional): Include closed tasks (default: false)
- `assignees` (list, optional): Filter by assignee user IDs
- `tags` (list, optional): Filter by tag names
- `due_date_gt` (int, optional): Due date greater than (Unix ms)
- `due_date_lt` (int, optional): Due date less than (Unix ms)

**Example:**
```python
# All tasks in a list
tasks = await list_tasks(list_id="abc123")

# Open tasks assigned to specific user
tasks = await list_tasks(
    list_id="abc123",
    assignees=["12345"],
    include_closed=False
)

# Tasks due this week
import time
now = int(time.time() * 1000)
week_later = now + (7 * 24 * 60 * 60 * 1000)

tasks = await list_tasks(
    list_id="abc123",
    due_date_gt=now,
    due_date_lt=week_later
)

# Tasks with specific status
tasks = await list_tasks(
    list_id="abc123",
    statuses=["in progress", "review"]
)
```

#### `get_task`
Get task details with custom fields.

**Parameters:**
- `task_id` (string, required): Task ID

**Example:**
```python
task = await get_task(task_id="xyz789")

# Returns:
# {
#   "id": "xyz789",
#   "name": "Implement user authentication",
#   "description": "Add OAuth 2.0 support",
#   "status": {
#     "status": "in progress",
#     "color": "#d3d3d3"
#   },
#   "orderindex": "1.00",
#   "date_created": "1633024800000",
#   "date_updated": "1633111200000",
#   "date_closed": null,
#   "creator": {"id": 123, "username": "user"},
#   "assignees": [{"id": 456, "username": "dev"}],
#   "tags": [{"name": "backend", "tag_fg": "#000", "tag_bg": "#FFF"}],
#   "parent": null,
#   "priority": 2,
#   "due_date": "1633197600000",
#   "start_date": "1633024800000",
#   "time_estimate": 7200000,
#   "time_spent": 3600000,
#   "custom_fields": [...],
#   "list": {"id": "abc123", "name": "Sprint"},
#   "folder": {"id": "789", "name": "Engineering"},
#   "space": {"id": "456"},
#   "url": "https://app.clickup.com/t/xyz789"
# }
```

#### `create_task`
Create a new task.

**Parameters:**
- `list_id` (string, required): List ID
- `name` (string, required): Task name
- `description` (string, optional): Task description
- `assignees` (list, optional): Assignee user IDs
- `tags` (list, optional): Tag names
- `status` (string, optional): Status name
- `priority` (int, optional): Priority (1=urgent, 2=high, 3=normal, 4=low)
- `due_date` (int, optional): Due date (Unix timestamp ms)
- `due_date_time` (bool, optional): Include time (default: false)
- `time_estimate` (int, optional): Time estimate in milliseconds
- `start_date` (int, optional): Start date (Unix timestamp ms)
- `start_date_time` (bool, optional): Include time (default: false)
- `notify_all` (bool, optional): Notify assignees (default: true)
- `parent` (string, optional): Parent task ID (for subtasks)
- `custom_fields` (list, optional): Custom field objects

**Priority Levels:**
- **1**: Urgent (red flag)
- **2**: High (yellow flag)
- **3**: Normal (blue flag, default)
- **4**: Low (gray flag)

**Example:**
```python
# Simple task
task = await create_task(
    list_id="abc123",
    name="Write API documentation"
)

# Full task with all options
import time
tomorrow = int((time.time() + 86400) * 1000)

task = await create_task(
    list_id="abc123",
    name="Deploy to production",
    description="Deploy version 2.0.0 with new features",
    assignees=[12345, 67890],
    tags=["deployment", "urgent"],
    status="todo",
    priority=1,
    due_date=tomorrow,
    due_date_time=True,
    time_estimate=3600000,  # 1 hour in ms
    notify_all=True
)

# Subtask
subtask = await create_task(
    list_id="abc123",
    name="Run database migrations",
    parent="xyz789",  # Parent task ID
    assignees=[12345],
    priority=2
)

# Task with custom fields
task = await create_task(
    list_id="abc123",
    name="Bug fix: Login issue",
    custom_fields=[
        {"id": "field_123", "value": "Bug"},
        {"id": "field_456", "value": "High"}
    ]
)
```

#### `update_task`
Update task details.

**Parameters:**
- `task_id` (string, required): Task ID
- `name` (string, optional): Updated name
- `description` (string, optional): Updated description
- `status` (string, optional): Updated status
- `priority` (int, optional): Updated priority (1-4)
- `due_date` (int, optional): Updated due date (Unix ms)
- `time_estimate` (int, optional): Updated time estimate (ms)
- `assignees` (dict, optional): Assignees {"add": [ids], "rem": [ids]}

**Example:**
```python
# Update task status
task = await update_task(
    task_id="xyz789",
    status="in progress"
)

# Add assignees
task = await update_task(
    task_id="xyz789",
    assignees={"add": [12345, 67890]}
)

# Remove assignees
task = await update_task(
    task_id="xyz789",
    assignees={"rem": [12345]}
)

# Update priority and due date
import time
next_week = int((time.time() + 7 * 86400) * 1000)

task = await update_task(
    task_id="xyz789",
    priority=1,
    due_date=next_week
)
```

#### `delete_task`
Delete a task.

**Parameters:**
- `task_id` (string, required): Task ID

**Example:**
```python
result = await delete_task(task_id="xyz789")
```

### Comments

#### `add_task_comment`
Add comment to a task.

**Parameters:**
- `task_id` (string, required): Task ID
- `comment_text` (string, required): Comment text
- `assignee` (int, optional): Assign comment to user ID
- `notify_all` (bool, optional): Notify all assignees (default: true)

**Example:**
```python
# Simple comment
comment = await add_task_comment(
    task_id="xyz789",
    comment_text="Great progress on this task!"
)

# Comment with assignment
comment = await add_task_comment(
    task_id="xyz789",
    comment_text="Can you review this?",
    assignee=12345,
    notify_all=True
)
```

#### `list_task_comments`
Get task comments.

**Parameters:**
- `task_id` (string, required): Task ID

**Example:**
```python
comments = await list_task_comments(task_id="xyz789")

# Returns:
# {
#   "comments": [
#     {
#       "id": "123",
#       "comment_text": "Great work!",
#       "user": {"id": 456, "username": "user"},
#       "date": "1633024800000"
#     }
#   ]
# }
```

### Time Tracking

#### `create_time_entry`
Track time on a task.

**Parameters:**
- `task_id` (string, required): Task ID
- `duration` (int, required): Duration in milliseconds
- `start` (int, optional): Start time (Unix ms, defaults to now)
- `description` (string, optional): Time entry description

**Example:**
```python
# Log 2 hours of work
two_hours_ms = 2 * 60 * 60 * 1000

time_entry = await create_time_entry(
    task_id="xyz789",
    duration=two_hours_ms,
    description="Implemented OAuth integration"
)

# Log time with specific start time
import time
start_time = int((time.time() - 7200) * 1000)  # 2 hours ago

time_entry = await create_time_entry(
    task_id="xyz789",
    duration=two_hours_ms,
    start=start_time
)
```

#### `list_time_entries`
Get time tracking entries.

**Parameters:**
- `workspace_id` (string, required): Workspace ID
- `start_date` (int, optional): Filter by start date (Unix ms)
- `end_date` (int, optional): Filter by end date (Unix ms)
- `assignee` (int, optional): Filter by assignee user ID

**Example:**
```python
# All time entries
entries = await list_time_entries(workspace_id="123")

# Time entries for this week
import time
week_ago = int((time.time() - 7 * 86400) * 1000)
now = int(time.time() * 1000)

entries = await list_time_entries(
    workspace_id="123",
    start_date=week_ago,
    end_date=now
)

# Time entries for specific user
entries = await list_time_entries(
    workspace_id="123",
    assignee=12345
)
```

### Goals

#### `list_goals`
List goals in a workspace.

**Parameters:**
- `workspace_id` (string, required): Workspace ID

**Example:**
```python
goals = await list_goals(workspace_id="123")

# Returns:
# {
#   "goals": [
#     {
#       "id": "goal_123",
#       "name": "Q4 Revenue Target",
#       "due_date": "1640995200000",
#       "description": "Reach $1M ARR",
#       "percent_completed": 75,
#       "color": "#32a852"
#     }
#   ]
# }
```

#### `get_goal`
Get goal details and progress.

**Parameters:**
- `goal_id` (string, required): Goal ID

**Example:**
```python
goal = await get_goal(goal_id="goal_123")

# Returns:
# {
#   "goal": {
#     "id": "goal_123",
#     "name": "Q4 Revenue Target",
#     "description": "Reach $1M ARR",
#     "due_date": "1640995200000",
#     "color": "#32a852",
#     "percent_completed": 75,
#     "key_results": [
#       {
#         "id": "kr_456",
#         "name": "Close 10 enterprise deals",
#         "type": "number",
#         "current": 7,
#         "target": 10,
#         "percent_completed": 70
#       }
#     ]
#   }
# }
```

### Custom Fields

#### `list_custom_fields`
Get custom fields for a list.

**Parameters:**
- `list_id` (string, required): List ID

**Example:**
```python
fields = await list_custom_fields(list_id="abc123")

# Returns:
# {
#   "fields": [
#     {
#       "id": "field_123",
#       "name": "Priority",
#       "type": "drop_down",
#       "type_config": {
#         "options": [
#           {"id": "opt_1", "name": "High", "color": "#FF0000"},
#           {"id": "opt_2", "name": "Low", "color": "#00FF00"}
#         ]
#       }
#     },
#     {
#       "id": "field_456",
#       "name": "Story Points",
#       "type": "number"
#     }
#   ]
# }
```

**Custom Field Types:**
- `text`: Text input
- `number`: Numeric input
- `drop_down`: Dropdown selection
- `date`: Date picker
- `checkbox`: Boolean checkbox
- `url`: URL input
- `email`: Email input
- `phone`: Phone number
- `currency`: Currency value

### Search

#### `search_tasks`
Search tasks across workspace.

**Parameters:**
- `workspace_id` (string, required): Workspace ID
- `query` (string, required): Search query text
- `start_date` (int, optional): Filter by start date (Unix ms)
- `end_date` (int, optional): Filter by end date (Unix ms)
- `assignees` (list, optional): Filter by assignee user IDs
- `statuses` (list, optional): Filter by status names
- `tags` (list, optional): Filter by tag names

**Example:**
```python
# Search by keyword
tasks = await search_tasks(
    workspace_id="123",
    query="authentication"
)

# Advanced search with filters
tasks = await search_tasks(
    workspace_id="123",
    query="bug",
    assignees=[12345],
    statuses=["in progress"],
    tags=["urgent"]
)
```

## Common Workflows

### Project Setup
```python
# 1. Get workspace
workspaces = await list_workspaces()
workspace_id = workspaces["teams"][0]["id"]

# 2. Create or get space
spaces = await list_spaces(workspace_id=workspace_id)
space_id = spaces["spaces"][0]["id"]

# 3. Get lists
lists = await list_lists(space_id=space_id)
list_id = lists["lists"][0]["id"]

# 4. Create tasks
await create_task(
    list_id=list_id,
    name="Set up development environment",
    priority=2
)

await create_task(
    list_id=list_id,
    name="Write technical documentation",
    priority=3
)
```

### Sprint Planning
```python
# Get all tasks
tasks = await list_tasks(list_id="abc123")

# Sort by priority
sorted_tasks = sorted(
    tasks["tasks"],
    key=lambda t: t.get("priority", 3)
)

# Assign to team members
team_members = [12345, 67890, 11111]

for i, task in enumerate(sorted_tasks[:10]):
    assignee = team_members[i % len(team_members)]
    await update_task(
        task_id=task["id"],
        assignees={"add": [assignee]},
        status="todo"
    )
```

### Time Tracking Report
```python
import time

# Get this week's time entries
week_ago = int((time.time() - 7 * 86400) * 1000)
now = int(time.time() * 1000)

entries = await list_time_entries(
    workspace_id="123",
    start_date=week_ago,
    end_date=now
)

# Calculate total hours
total_ms = sum(entry["duration"] for entry in entries["data"])
total_hours = total_ms / (1000 * 60 * 60)

print(f"Total hours this week: {total_hours:.2f}")
```

### Goal Tracking
```python
# List all goals
goals = await list_goals(workspace_id="123")

# Check progress on each goal
for goal in goals["goals"]:
    goal_detail = await get_goal(goal_id=goal["id"])

    print(f"Goal: {goal_detail['goal']['name']}")
    print(f"Progress: {goal_detail['goal']['percent_completed']}%")

    for kr in goal_detail['goal']['key_results']:
        print(f"  - {kr['name']}: {kr['current']}/{kr['target']}")
```

## Best Practices

1. **Use hierarchy effectively**: Organize with Spaces → Folders → Lists
2. **Custom statuses**: Set up workflows per list
3. **Custom fields**: Add metadata for filtering and reporting
4. **Time tracking**: Log time regularly for accurate estimates
5. **Tags**: Use tags for cross-list categorization
6. **Goals**: Set measurable goals with key results
7. **Priorities**: Use priority levels consistently
8. **Assignees**: Assign tasks for accountability
9. **Comments**: Communicate within tasks
10. **Search**: Use search for cross-workspace queries

## Rate Limit Handling

```python
import asyncio

async def make_request_with_retry():
    try:
        return await list_tasks(list_id="abc123")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            # Wait and retry
            await asyncio.sleep(60)
            return await list_tasks(list_id="abc123")
        raise
```

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid API token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded (100 req/min)
- **500 Internal Server Error**: ClickUp service issue

## API Documentation

- [ClickUp API Documentation](https://clickup.com/api/)
- [Authentication](https://clickup.com/api/developer-portal/authentication/)
- [Tasks API](https://clickup.com/api/clickupreference/operation/GetTasks/)
- [Time Tracking](https://clickup.com/api/clickupreference/operation/Gettimeentrieswithinadaterange/)

## Support

- [Help Center](https://help.clickup.com/)
- [API Support](https://clickup.com/contact)
- [Community](https://clickup.com/community)
- [Status Page](https://status.clickup.com/)
