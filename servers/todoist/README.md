# Todoist MCP Server

MCP server for Todoist API. Manage tasks, projects, labels, and productivity workflows with natural language date parsing and advanced organization features.

## Features

- **Task Management**: Create, update, complete, and delete tasks
- **Projects**: Organize tasks into projects with nested hierarchies
- **Labels**: Tag and categorize tasks with labels
- **Sections**: Group tasks within projects
- **Natural Language**: Parse due dates with natural language ("tomorrow at 3pm")
- **Priorities**: Set task priority from normal to urgent
- **Subtasks**: Create task hierarchies with parent tasks
- **Comments**: Collaborate with task and project comments
- **Filters**: Advanced task filtering and search

## Setup

### Prerequisites

- Todoist account (free or premium)
- API token

### Environment Variables

- `TODOIST_API_TOKEN` (required): Your Todoist API token

**How to get credentials:**
1. Go to [todoist.com](https://todoist.com/)
2. Log in to your account
3. Go to Settings → Integrations → Developer
4. Find your API token under "API token"
5. Copy the token and store as `TODOIST_API_TOKEN`

Direct link: https://todoist.com/app/settings/integrations/developer

## Rate Limits

- **Free & Premium**: 450 requests per 15 minutes
- Rate limit resets every 15 minutes
- HTTP 429 response when limit exceeded

## Available Tools

### Task Management

#### `list_tasks`
List all active tasks with optional filters.

**Parameters:**
- `project_id` (string, optional): Filter by project ID
- `label` (string, optional): Filter by label name
- `filter` (string, optional): Filter string (today, p1, overdue, etc.)
- `lang` (string, optional): Language for filter parsing (default: en)

**Example:**
```python
# All tasks
tasks = await list_tasks()

# Tasks for today
today_tasks = await list_tasks(filter="today")

# High priority tasks
urgent = await list_tasks(filter="p1")

# Tasks in a specific project
project_tasks = await list_tasks(project_id="2203306141")

# Tasks with a specific label
work_tasks = await list_tasks(label="work")
```

**Common Filters:**
- `today`: Tasks due today
- `tomorrow`: Tasks due tomorrow
- `overdue`: Overdue tasks
- `p1`: Priority 1 (urgent) tasks
- `p2`: Priority 2 (high) tasks
- `no date`: Tasks with no due date
- `assigned to: me`: Tasks assigned to you
- `@label_name`: Tasks with specific label

#### `get_task`
Get specific task details.

**Parameters:**
- `task_id` (string, required): Task ID

**Example:**
```python
task = await get_task(task_id="7498765432")

# Returns:
# - id, content, description
# - project_id, section_id, parent_id
# - order, priority, labels
# - due (date, datetime, string, timezone)
# - url, comment_count
# - created_at, creator_id
# - assignee_id, assigner_id
# - is_completed
```

#### `create_task`
Create a new task.

**Parameters:**
- `content` (string, required): Task content
- `description` (string, optional): Task description
- `project_id` (string, optional): Project ID
- `section_id` (string, optional): Section ID
- `parent_id` (string, optional): Parent task ID (for subtasks)
- `order` (int, optional): Task position order
- `labels` (list, optional): List of label names
- `priority` (int, optional): Priority 1-4 (default: 1)
- `due_string` (string, optional): Natural language due date
- `due_date` (string, optional): Due date (YYYY-MM-DD)
- `due_datetime` (string, optional): Due datetime (RFC 3339)
- `due_lang` (string, optional): Language for parsing (default: en)
- `assignee_id` (string, optional): User ID to assign to

**Priority Levels:**
- **1**: Normal (default)
- **2**: High
- **3**: Very High
- **4**: Urgent

**Example:**
```python
# Simple task
task = await create_task(
    content="Buy groceries"
)

# Task with natural language due date
task = await create_task(
    content="Team meeting",
    due_string="tomorrow at 3pm",
    priority=3,
    labels=["work", "meetings"]
)

# Task with specific due date
task = await create_task(
    content="Submit report",
    due_date="2025-10-15",
    project_id="2203306141",
    priority=4
)

# Subtask
subtask = await create_task(
    content="Review draft",
    parent_id="7498765432",
    priority=2
)

# Task with description and labels
task = await create_task(
    content="Project planning",
    description="Outline Q4 goals and milestones",
    labels=["planning", "important"],
    project_id="2203306141",
    section_id="123456"
)
```

**Natural Language Date Examples:**
- "today"
- "tomorrow"
- "next Monday"
- "tomorrow at 3pm"
- "every day"
- "every Monday"
- "every other week"
- "every 3 days"
- "1st of every month"

#### `update_task`
Update task details.

**Parameters:**
- `task_id` (string, required): Task ID
- `content` (string, optional): Updated content
- `description` (string, optional): Updated description
- `labels` (list, optional): Updated labels
- `priority` (int, optional): Updated priority (1-4)
- `due_string` (string, optional): Natural language due date
- `due_date` (string, optional): Due date (YYYY-MM-DD)
- `due_datetime` (string, optional): Due datetime (RFC 3339)
- `due_lang` (string, optional): Language for parsing
- `assignee_id` (string, optional): User ID to assign to

**Example:**
```python
# Update content and priority
task = await update_task(
    task_id="7498765432",
    content="Buy groceries (urgent!)",
    priority=4
)

# Update due date
task = await update_task(
    task_id="7498765432",
    due_string="next Monday at 2pm"
)

# Update labels
task = await update_task(
    task_id="7498765432",
    labels=["shopping", "urgent"]
)
```

#### `complete_task`
Mark task as completed.

**Parameters:**
- `task_id` (string, required): Task ID

**Example:**
```python
result = await complete_task(task_id="7498765432")
```

#### `reopen_task`
Reopen a completed task.

**Parameters:**
- `task_id` (string, required): Task ID

**Example:**
```python
result = await reopen_task(task_id="7498765432")
```

#### `delete_task`
Delete a task.

**Parameters:**
- `task_id` (string, required): Task ID

**Example:**
```python
result = await delete_task(task_id="7498765432")
```

### Project Management

#### `list_projects`
List all projects.

**Example:**
```python
projects = await list_projects()

# Returns array of projects with:
# - id, name, color
# - parent_id (for nested projects)
# - order, comment_count
# - is_shared, is_favorite, is_inbox_project
# - view_style (list or board)
# - url
```

#### `get_project`
Get project details.

**Parameters:**
- `project_id` (string, required): Project ID

**Example:**
```python
project = await get_project(project_id="2203306141")
```

#### `create_project`
Create a new project.

**Parameters:**
- `name` (string, required): Project name
- `parent_id` (string, optional): Parent project ID (for nested projects)
- `color` (string, optional): Color name
- `is_favorite` (bool, optional): Mark as favorite (default: false)
- `view_style` (string, optional): "list" or "board" (default: list)

**Colors:**
- berry_red, red, orange, yellow, olive_green
- lime_green, green, mint_green, teal, sky_blue
- light_blue, blue, grape, violet, lavender
- magenta, salmon, charcoal, grey, taupe

**Example:**
```python
# Simple project
project = await create_project(name="Work Projects")

# Project with color and favorite
project = await create_project(
    name="Personal Goals",
    color="blue",
    is_favorite=True,
    view_style="list"
)

# Nested project (subproject)
subproject = await create_project(
    name="Q4 Goals",
    parent_id="2203306141",
    color="green"
)

# Board-style project
board = await create_project(
    name="Sprint Planning",
    view_style="board"
)
```

#### `update_project`
Update project details.

**Parameters:**
- `project_id` (string, required): Project ID
- `name` (string, optional): Updated name
- `color` (string, optional): Updated color
- `is_favorite` (bool, optional): Updated favorite status
- `view_style` (string, optional): Updated view style

**Example:**
```python
project = await update_project(
    project_id="2203306141",
    name="Work - 2025",
    color="red",
    is_favorite=True
)
```

#### `delete_project`
Delete a project.

**Parameters:**
- `project_id` (string, required): Project ID

**Example:**
```python
result = await delete_project(project_id="2203306141")
```

### Section Management

#### `list_sections`
List sections in a project.

**Parameters:**
- `project_id` (string, optional): Project ID (returns all sections if not provided)

**Example:**
```python
# All sections
sections = await list_sections()

# Sections in specific project
sections = await list_sections(project_id="2203306141")

# Returns:
# - id, project_id, order
# - name
```

#### `create_section`
Create a new section.

**Parameters:**
- `name` (string, required): Section name
- `project_id` (string, required): Project ID
- `order` (int, optional): Section position order

**Example:**
```python
section = await create_section(
    name="In Progress",
    project_id="2203306141",
    order=1
)

# Common section names:
# - "To Do", "In Progress", "Done"
# - "Backlog", "This Week", "Completed"
# - "High Priority", "Medium Priority", "Low Priority"
```

### Label Management

#### `list_labels`
List all labels.

**Example:**
```python
labels = await list_labels()

# Returns array of labels with:
# - id, name, color
# - order, is_favorite
```

#### `create_label`
Create a new label.

**Parameters:**
- `name` (string, required): Label name
- `color` (string, optional): Color name
- `order` (int, optional): Label position order
- `is_favorite` (bool, optional): Mark as favorite (default: false)

**Example:**
```python
# Simple label
label = await create_label(name="urgent")

# Label with color
label = await create_label(
    name="work",
    color="blue",
    is_favorite=True
)

# Common labels:
# - urgent, important, low-priority
# - work, personal, home
# - waiting, next, someday
# - errand, call, email, meeting
```

### Comments

#### `list_comments`
Get comments for a task or project.

**Parameters:**
- `task_id` (string, optional): Task ID
- `project_id` (string, optional): Project ID

**Example:**
```python
# Task comments
comments = await list_comments(task_id="7498765432")

# Project comments
comments = await list_comments(project_id="2203306141")

# Returns:
# - id, task_id, project_id
# - content
# - posted_at
# - attachment (file info if present)
```

#### `create_comment`
Add a comment to a task or project.

**Parameters:**
- `content` (string, required): Comment content
- `task_id` (string, optional): Task ID
- `project_id` (string, optional): Project ID
- `attachment` (dict, optional): File attachment object

**Example:**
```python
# Task comment
comment = await create_comment(
    content="Started working on this",
    task_id="7498765432"
)

# Project comment
comment = await create_comment(
    content="Project kickoff meeting notes",
    project_id="2203306141"
)

# Comment with attachment
comment = await create_comment(
    content="See attached file",
    task_id="7498765432",
    attachment={
        "file_name": "report.pdf",
        "file_type": "application/pdf",
        "file_url": "https://example.com/report.pdf"
    }
)
```

## Common Workflows

### Daily Task Management
```python
# Get today's tasks
today = await list_tasks(filter="today")

# Create a task for today
task = await create_task(
    content="Review PRs",
    due_string="today at 2pm",
    labels=["work"],
    priority=3
)

# Complete a task
await complete_task(task_id=task["id"])
```

### Project Setup
```python
# Create a project
project = await create_project(
    name="Website Redesign",
    color="blue",
    view_style="board"
)

# Create sections
await create_section(name="To Do", project_id=project["id"], order=1)
await create_section(name="In Progress", project_id=project["id"], order=2)
await create_section(name="Done", project_id=project["id"], order=3)

# Create labels
await create_label(name="frontend", color="red")
await create_label(name="backend", color="green")
await create_label(name="design", color="blue")

# Add tasks
await create_task(
    content="Design homepage mockup",
    project_id=project["id"],
    labels=["design"],
    priority=4,
    due_string="next Monday"
)
```

### Weekly Planning
```python
# Get overdue tasks
overdue = await list_tasks(filter="overdue")

# Get this week's tasks
week_tasks = await list_tasks(filter="7 days")

# Create recurring weekly task
weekly = await create_task(
    content="Weekly team meeting",
    due_string="every Monday at 10am",
    labels=["meetings"],
    priority=3
)
```

### Subtask Management
```python
# Create parent task
parent = await create_task(
    content="Launch marketing campaign",
    project_id="2203306141",
    priority=4
)

# Create subtasks
await create_task(
    content="Design email template",
    parent_id=parent["id"],
    priority=3
)

await create_task(
    content="Write copy",
    parent_id=parent["id"],
    priority=3
)

await create_task(
    content="Set up automation",
    parent_id=parent["id"],
    priority=2
)
```

## Due Date Formats

### Natural Language (due_string)
- "today"
- "tomorrow"
- "next Monday"
- "in 3 days"
- "next week"
- "tomorrow at 3pm"
- "Monday at 9am"
- "every day"
- "every Monday"
- "every other week"
- "every 3 months"
- "1st of every month"

### Specific Date (due_date)
- Format: YYYY-MM-DD
- Example: "2025-10-15"
- Time not included

### Specific DateTime (due_datetime)
- Format: RFC 3339 (ISO 8601)
- Example: "2025-10-15T15:00:00Z"
- Includes timezone

## Priority Levels

Todoist uses priority levels 1-4:

- **Priority 1**: Normal (default, grey flag)
- **Priority 2**: High (blue flag)
- **Priority 3**: Very High (orange flag)
- **Priority 4**: Urgent (red flag)

## Best Practices

1. **Use natural language dates**: More intuitive than specific dates
2. **Organize with projects**: Group related tasks
3. **Use sections**: Further organize tasks within projects
4. **Label consistently**: Create a labeling system and stick to it
5. **Set priorities**: Focus on what matters most
6. **Create subtasks**: Break down complex tasks
7. **Add descriptions**: Provide context and details
8. **Use comments**: Collaborate and track progress
9. **Review regularly**: Use filters to see overdue and upcoming tasks
10. **Recurring tasks**: Automate repetitive tasks

## Productivity Tips

### GTD (Getting Things Done)
```python
# Inbox (capture everything)
await create_task(content="Random idea", project_id="inbox_id")

# Process inbox (organize)
await update_task(
    task_id="...",
    project_id="work_id",
    labels=["next-action"],
    due_string="tomorrow"
)

# Next actions filter
next_actions = await list_tasks(label="next-action")
```

### Time Blocking
```python
# Morning tasks
await create_task(
    content="Deep work: Write report",
    due_string="today at 9am",
    priority=4
)

# Afternoon tasks
await create_task(
    content="Meetings and collaboration",
    due_string="today at 2pm",
    priority=3
)
```

### Weekly Review
```python
# What was completed this week?
completed = await list_tasks(filter="completed & 7 days")

# What's overdue?
overdue = await list_tasks(filter="overdue")

# What's coming up?
upcoming = await list_tasks(filter="7 days")
```

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid API token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Task, project, or resource not found
- **429 Too Many Requests**: Rate limit exceeded (450 per 15 min)
- **500 Internal Server Error**: Todoist service issue

## API Documentation

- [Todoist REST API v2](https://developer.todoist.com/rest/v2/)
- [Quick Start Guide](https://developer.todoist.com/rest/v2/#quick-start)
- [Filters Documentation](https://todoist.com/help/articles/introduction-to-filters-V98wIH)
- [Integration Best Practices](https://developer.todoist.com/rest/v2/#best-practices)

## Support

- [Help Center](https://todoist.com/help)
- [API Support](https://todoist.com/contact)
- [Community](https://www.reddit.com/r/todoist/)
- [Twitter](https://twitter.com/todoist)
