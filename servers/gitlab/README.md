# GitLab MCP Server

MCP server for GitLab API. Complete DevOps platform for version control, issue tracking, merge requests, CI/CD pipelines, and team collaboration. Works with both GitLab.com and self-hosted GitLab instances.

## Features

- **Project Management**: Access and manage GitLab projects
- **Issue Tracking**: Create, update, search, and track issues
- **Merge Requests**: Full MR workflow with approvals
- **CI/CD Pipelines**: Monitor and control pipelines
- **Code Search**: Search code across projects
- **Repository Operations**: Commits, branches, and repository management
- **Team Collaboration**: Assignees, reviewers, and labels
- **Self-Hosted Support**: Works with custom GitLab instances
- **DevOps Integration**: Complete platform for software delivery
- **Approval Workflows**: Merge request approval process

## Setup

### Prerequisites

- GitLab account (GitLab.com or self-hosted instance)
- Personal Access Token with appropriate scopes

### Environment Variables

- `GITLAB_PERSONAL_ACCESS_TOKEN` (required): Your GitLab Personal Access Token
- `GITLAB_URL` (optional): GitLab instance URL (defaults to https://gitlab.com)

**How to get credentials:**

1. Go to [gitlab.com/-/profile/personal_access_tokens](https://gitlab.com/-/profile/personal_access_tokens)
2. Sign in to your GitLab account
3. Click "Add new token"
4. Enter a token name (e.g., "MCP Server")
5. Set expiration date (optional but recommended)
6. Select required scopes:
   - `api`: Full API access (recommended)
   - `read_api`: Read-only API access
   - `read_repository`: Read repository content
   - `write_repository`: Write to repository
7. Click "Create personal access token"
8. Copy the token immediately (it won't be shown again)
9. Store as `GITLAB_PERSONAL_ACCESS_TOKEN`

**For self-hosted GitLab:**
- Set `GITLAB_URL` to your instance URL (e.g., `https://gitlab.mycompany.com`)
- Create token from your instance's profile settings

**Token Format:**
- Format: `glpat-xxxxxxxxxxxxxxxxxxxx`
- Keep your token secure - it has full access to your account

## Rate Limits

**GitLab.com:**
- 2,000 requests per minute per user
- Higher limits for GitLab Premium/Ultimate

**Self-hosted GitLab:**
- Rate limits configured by administrator
- Default: 10 requests per second per IP
- Can be customized per instance

**Best Practices:**
- Use pagination for large result sets
- Cache data when appropriate
- Implement exponential backoff for retries
- Monitor rate limit headers in responses

## Project Identification

GitLab accepts two formats for project IDs:

- **Numeric ID**: `"278964"`
- **Path format**: `"namespace/project"` (e.g., `"gitlab-org/gitlab"`)

The path format is URL-encoded automatically by the server.

## Available Tools

### Project Management

#### `list_projects`
List projects you have access to.

**Parameters:**
- `visibility` (string, optional): Filter by visibility (public, internal, private)
- `owned` (bool, optional): Limit to owned projects (default: false)
- `starred` (bool, optional): Limit to starred projects (default: false)
- `archived` (bool, optional): Include archived projects (default: false)
- `per_page` (int, optional): Results per page (default: 20, max: 100)

**Example:**
```python
# List all accessible projects
projects = await list_projects(per_page=20)

# List only owned projects
projects = await list_projects(owned=True)

# List starred projects
projects = await list_projects(starred=True)

# List public projects
projects = await list_projects(visibility="public")

# Returns:
# [
#   {
#     "id": 278964,
#     "name": "My Project",
#     "path": "my-project",
#     "path_with_namespace": "username/my-project",
#     "description": "Project description",
#     "visibility": "private",
#     "default_branch": "main",
#     "ssh_url_to_repo": "git@gitlab.com:username/my-project.git",
#     "http_url_to_repo": "https://gitlab.com/username/my-project.git",
#     "web_url": "https://gitlab.com/username/my-project",
#     "star_count": 5,
#     "forks_count": 2,
#     "created_at": "2025-01-01T00:00:00.000Z",
#     "last_activity_at": "2025-10-08T12:00:00.000Z"
#   }
# ]
```

#### `get_project`
Get detailed information about a specific project.

**Parameters:**
- `project_id` (string, required): Project ID or path

**Example:**
```python
# Using numeric ID
project = await get_project(project_id="278964")

# Using path format
project = await get_project(project_id="gitlab-org/gitlab")

# Returns:
# {
#   "id": 278964,
#   "name": "GitLab",
#   "path": "gitlab",
#   "path_with_namespace": "gitlab-org/gitlab",
#   "description": "The open source DevOps platform",
#   "visibility": "public",
#   "default_branch": "master",
#   "tag_list": ["devops", "git", "ci-cd"],
#   "archived": false,
#   "created_at": "2011-10-09T00:00:00.000Z",
#   "last_activity_at": "2025-10-08T14:30:00.000Z",
#   "creator_id": 123,
#   "namespace": {
#     "id": 456,
#     "name": "GitLab.org",
#     "path": "gitlab-org",
#     "kind": "group"
#   },
#   "open_issues_count": 1234,
#   "star_count": 23000,
#   "forks_count": 8000,
#   "web_url": "https://gitlab.com/gitlab-org/gitlab"
# }
```

### Issue Management

#### `list_issues`
List issues with filters.

**Parameters:**
- `project_id` (string, optional): Project ID or path (if omitted, returns all accessible issues)
- `state` (string, optional): Filter by state (opened, closed, all)
- `labels` (string, optional): Comma-separated label names
- `milestone` (string, optional): Milestone title
- `assignee_id` (int, optional): Assignee user ID
- `author_id` (int, optional): Author user ID
- `scope` (string, optional): Filter by scope (created_by_me, assigned_to_me, all)
- `per_page` (int, optional): Results per page (default: 20, max: 100)

**Example:**
```python
# All accessible issues
issues = await list_issues(per_page=20)

# Project issues
issues = await list_issues(project_id="gitlab-org/gitlab")

# Open issues assigned to me
issues = await list_issues(
    state="opened",
    scope="assigned_to_me"
)

# Filter by labels
issues = await list_issues(
    project_id="278964",
    labels="bug,critical"
)

# Filter by assignee
issues = await list_issues(
    project_id="278964",
    assignee_id=123,
    state="opened"
)

# Returns:
# [
#   {
#     "id": 12345,
#     "iid": 42,
#     "project_id": 278964,
#     "title": "Fix authentication bug",
#     "description": "Users unable to login with OAuth",
#     "state": "opened",
#     "created_at": "2025-10-01T10:00:00.000Z",
#     "updated_at": "2025-10-08T14:00:00.000Z",
#     "closed_at": null,
#     "labels": ["bug", "security"],
#     "milestone": {
#       "id": 789,
#       "title": "v2.0"
#     },
#     "assignees": [
#       {
#         "id": 123,
#         "username": "johndoe",
#         "name": "John Doe"
#       }
#     ],
#     "author": {
#       "id": 456,
#       "username": "janedoe",
#       "name": "Jane Doe"
#     },
#     "web_url": "https://gitlab.com/username/project/-/issues/42"
#   }
# ]
```

#### `get_issue`
Get detailed information about a specific issue.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `issue_iid` (int, required): Issue IID (internal ID within project)

**Note:** Use `iid` (internal ID) not `id` (global ID).

**Example:**
```python
issue = await get_issue(
    project_id="gitlab-org/gitlab",
    issue_iid=42
)

# Returns:
# {
#   "id": 12345,
#   "iid": 42,
#   "project_id": 278964,
#   "title": "Implement dark mode",
#   "description": "Add dark mode theme support",
#   "state": "opened",
#   "created_at": "2025-10-01T10:00:00.000Z",
#   "updated_at": "2025-10-08T14:00:00.000Z",
#   "closed_at": null,
#   "closed_by": null,
#   "labels": ["enhancement", "ui"],
#   "milestone": {"id": 789, "title": "v2.0"},
#   "assignees": [{"id": 123, "username": "johndoe", "name": "John Doe"}],
#   "author": {"id": 456, "username": "janedoe", "name": "Jane Doe"},
#   "confidential": false,
#   "discussion_locked": false,
#   "due_date": "2025-10-31",
#   "time_stats": {
#     "time_estimate": 7200,
#     "total_time_spent": 3600,
#     "human_time_estimate": "2h",
#     "human_total_time_spent": "1h"
#   },
#   "web_url": "https://gitlab.com/username/project/-/issues/42",
#   "user_notes_count": 5,
#   "upvotes": 10,
#   "downvotes": 0
# }
```

#### `create_issue`
Create a new issue in a project.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `title` (string, required): Issue title
- `description` (string, optional): Issue description (markdown supported)
- `assignee_ids` (list of ints, optional): Assignee user IDs
- `labels` (string, optional): Comma-separated label names
- `milestone_id` (int, optional): Milestone ID
- `confidential` (bool, optional): Mark as confidential (default: false)

**Example:**
```python
# Simple issue
issue = await create_issue(
    project_id="278964",
    title="Add user authentication"
)

# Full issue with all fields
issue = await create_issue(
    project_id="gitlab-org/gitlab",
    title="Implement OAuth2 login",
    description="## Requirements\n\n- Support Google OAuth\n- Support GitHub OAuth\n- Add token refresh\n\n## Acceptance Criteria\n\n- [ ] OAuth flow works\n- [ ] Tokens are secure\n- [ ] Tests pass",
    assignee_ids=[123, 456],
    labels="enhancement,security",
    milestone_id=789,
    confidential=False
)

# Returns:
# {
#   "id": 12346,
#   "iid": 43,
#   "project_id": 278964,
#   "title": "Implement OAuth2 login",
#   "description": "## Requirements...",
#   "state": "opened",
#   "created_at": "2025-10-08T15:00:00.000Z",
#   "labels": ["enhancement", "security"],
#   "assignees": [
#     {"id": 123, "username": "johndoe", "name": "John Doe"},
#     {"id": 456, "username": "janedoe", "name": "Jane Doe"}
#   ],
#   "web_url": "https://gitlab.com/username/project/-/issues/43"
# }
```

#### `update_issue`
Update an existing issue.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `issue_iid` (int, required): Issue IID
- `title` (string, optional): Updated title
- `description` (string, optional): Updated description
- `state_event` (string, optional): State event (close, reopen)
- `assignee_ids` (list of ints, optional): Updated assignee IDs
- `labels` (string, optional): Updated labels

**Example:**
```python
# Update title
result = await update_issue(
    project_id="278964",
    issue_iid=42,
    title="Fix critical authentication bug"
)

# Close issue
result = await update_issue(
    project_id="278964",
    issue_iid=42,
    state_event="close"
)

# Update multiple fields
result = await update_issue(
    project_id="gitlab-org/gitlab",
    issue_iid=42,
    title="Updated title",
    description="Updated description",
    assignee_ids=[789],
    labels="bug,fixed"
)

# Reopen issue
result = await update_issue(
    project_id="278964",
    issue_iid=42,
    state_event="reopen"
)

# Returns:
# {
#   "id": 12345,
#   "iid": 42,
#   "title": "Fix critical authentication bug",
#   "state": "closed",
#   "updated_at": "2025-10-08T15:30:00.000Z",
#   ...
# }
```

### Merge Requests

#### `list_merge_requests`
List merge requests with filters.

**Parameters:**
- `project_id` (string, optional): Project ID or path (if omitted, returns all accessible MRs)
- `state` (string, optional): Filter by state (opened, closed, locked, merged, all)
- `scope` (string, optional): Filter by scope (created_by_me, assigned_to_me, all)
- `author_id` (int, optional): Author user ID
- `assignee_id` (int, optional): Assignee user ID
- `reviewer_id` (int, optional): Reviewer user ID
- `labels` (string, optional): Comma-separated label names
- `per_page` (int, optional): Results per page (default: 20, max: 100)

**Example:**
```python
# All accessible MRs
mrs = await list_merge_requests(per_page=20)

# Project MRs
mrs = await list_merge_requests(project_id="gitlab-org/gitlab")

# Open MRs assigned to me
mrs = await list_merge_requests(
    state="opened",
    scope="assigned_to_me"
)

# Filter by author
mrs = await list_merge_requests(
    project_id="278964",
    author_id=123
)

# Returns:
# [
#   {
#     "id": 67890,
#     "iid": 15,
#     "project_id": 278964,
#     "title": "Add dark mode feature",
#     "description": "Implements dark mode theme",
#     "state": "opened",
#     "created_at": "2025-10-05T09:00:00.000Z",
#     "updated_at": "2025-10-08T14:00:00.000Z",
#     "merged_at": null,
#     "source_branch": "feature/dark-mode",
#     "target_branch": "main",
#     "work_in_progress": false,
#     "draft": false,
#     "merge_status": "can_be_merged",
#     "labels": ["enhancement", "ui"],
#     "author": {"id": 123, "username": "johndoe", "name": "John Doe"},
#     "assignee": {"id": 456, "username": "janedoe", "name": "Jane Doe"},
#     "reviewers": [{"id": 789, "username": "reviewer1", "name": "Reviewer One"}],
#     "web_url": "https://gitlab.com/username/project/-/merge_requests/15",
#     "has_conflicts": false,
#     "blocking_discussions_resolved": true
#   }
# ]
```

#### `get_merge_request`
Get detailed information about a specific merge request.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `mr_iid` (int, required): Merge request IID

**Example:**
```python
mr = await get_merge_request(
    project_id="gitlab-org/gitlab",
    mr_iid=15
)

# Returns:
# {
#   "id": 67890,
#   "iid": 15,
#   "title": "Add dark mode feature",
#   "description": "Implements dark mode theme",
#   "state": "opened",
#   "merge_status": "can_be_merged",
#   "source_branch": "feature/dark-mode",
#   "target_branch": "main",
#   "author": {"id": 123, "username": "johndoe"},
#   "assignee": {"id": 456, "username": "janedoe"},
#   "reviewers": [{"id": 789, "username": "reviewer1"}],
#   "approvals_before_merge": 2,
#   "upvotes": 3,
#   "downvotes": 0,
#   "changes_count": "15",
#   "user_notes_count": 8,
#   "pipeline": {
#     "id": 12345,
#     "status": "success",
#     "ref": "feature/dark-mode"
#   },
#   "web_url": "https://gitlab.com/username/project/-/merge_requests/15"
# }
```

#### `create_merge_request`
Create a new merge request.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `source_branch` (string, required): Source branch name
- `target_branch` (string, required): Target branch name
- `title` (string, required): MR title
- `description` (string, optional): MR description (markdown supported)
- `assignee_id` (int, optional): Assignee user ID
- `reviewer_ids` (list of ints, optional): Reviewer user IDs
- `labels` (string, optional): Comma-separated label names
- `remove_source_branch` (bool, optional): Delete source branch after merge (default: false)

**Example:**
```python
# Simple MR
mr = await create_merge_request(
    project_id="278964",
    source_branch="feature/new-feature",
    target_branch="main",
    title="Add new feature"
)

# Full MR with reviewers and auto-delete
mr = await create_merge_request(
    project_id="gitlab-org/gitlab",
    source_branch="feature/authentication",
    target_branch="develop",
    title="Implement OAuth2 authentication",
    description="## Changes\n\n- Add OAuth2 provider\n- Update login flow\n- Add tests\n\n## Testing\n\n- [ ] Manual testing\n- [ ] Unit tests pass\n- [ ] Integration tests pass",
    assignee_id=123,
    reviewer_ids=[456, 789],
    labels="enhancement,security",
    remove_source_branch=True
)

# Returns:
# {
#   "id": 67891,
#   "iid": 16,
#   "title": "Implement OAuth2 authentication",
#   "state": "opened",
#   "source_branch": "feature/authentication",
#   "target_branch": "develop",
#   "author": {"id": 123, "username": "johndoe"},
#   "web_url": "https://gitlab.com/username/project/-/merge_requests/16"
# }
```

#### `approve_merge_request`
Approve a merge request.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `mr_iid` (int, required): Merge request IID

**Example:**
```python
result = await approve_merge_request(
    project_id="gitlab-org/gitlab",
    mr_iid=15
)

# Returns:
# {
#   "id": 67890,
#   "iid": 15,
#   "title": "Add dark mode feature",
#   "approved": true,
#   "approvals_left": 1,
#   "approved_by": [
#     {"user": {"id": 123, "username": "johndoe", "name": "John Doe"}}
#   ]
# }
```

#### `merge_merge_request`
Merge a merge request.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `mr_iid` (int, required): Merge request IID
- `merge_commit_message` (string, optional): Custom merge commit message
- `should_remove_source_branch` (bool, optional): Delete source branch after merge (default: false)
- `merge_when_pipeline_succeeds` (bool, optional): Merge when pipeline succeeds (default: false)

**Example:**
```python
# Simple merge
result = await merge_merge_request(
    project_id="278964",
    mr_iid=15
)

# Merge with auto-delete and wait for pipeline
result = await merge_merge_request(
    project_id="gitlab-org/gitlab",
    mr_iid=15,
    merge_commit_message="Merge branch 'feature/dark-mode' into 'main'\n\nImplements dark mode theme",
    should_remove_source_branch=True,
    merge_when_pipeline_succeeds=True
)

# Returns:
# {
#   "id": 67890,
#   "iid": 15,
#   "title": "Add dark mode feature",
#   "state": "merged",
#   "merged_at": "2025-10-08T16:00:00.000Z",
#   "merged_by": {"id": 123, "username": "johndoe"}
# }
```

### CI/CD Pipelines

#### `list_pipelines`
List CI/CD pipelines for a project.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `scope` (string, optional): Filter by scope (running, pending, finished, branches, tags)
- `status` (string, optional): Filter by status (created, waiting_for_resource, preparing, pending, running, success, failed, canceled, skipped, manual)
- `ref` (string, optional): Filter by ref (branch or tag name)
- `per_page` (int, optional): Results per page (default: 20, max: 100)

**Example:**
```python
# All pipelines
pipelines = await list_pipelines(project_id="gitlab-org/gitlab")

# Running pipelines
pipelines = await list_pipelines(
    project_id="278964",
    scope="running"
)

# Failed pipelines
pipelines = await list_pipelines(
    project_id="278964",
    status="failed"
)

# Pipelines for specific branch
pipelines = await list_pipelines(
    project_id="gitlab-org/gitlab",
    ref="main"
)

# Returns:
# [
#   {
#     "id": 12345,
#     "iid": 567,
#     "project_id": 278964,
#     "status": "success",
#     "source": "push",
#     "ref": "main",
#     "sha": "a1b2c3d4e5f6",
#     "web_url": "https://gitlab.com/username/project/-/pipelines/12345",
#     "created_at": "2025-10-08T10:00:00.000Z",
#     "updated_at": "2025-10-08T10:15:00.000Z",
#     "finished_at": "2025-10-08T10:15:00.000Z",
#     "duration": 900,
#     "coverage": "95.5"
#   }
# ]
```

#### `get_pipeline`
Get detailed information about a specific pipeline.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `pipeline_id` (int, required): Pipeline ID

**Example:**
```python
pipeline = await get_pipeline(
    project_id="gitlab-org/gitlab",
    pipeline_id=12345
)

# Returns:
# {
#   "id": 12345,
#   "iid": 567,
#   "project_id": 278964,
#   "status": "success",
#   "source": "push",
#   "ref": "main",
#   "sha": "a1b2c3d4e5f6",
#   "before_sha": "f6e5d4c3b2a1",
#   "tag": false,
#   "yaml_errors": null,
#   "user": {"id": 123, "username": "johndoe", "name": "John Doe"},
#   "created_at": "2025-10-08T10:00:00.000Z",
#   "updated_at": "2025-10-08T10:15:00.000Z",
#   "started_at": "2025-10-08T10:01:00.000Z",
#   "finished_at": "2025-10-08T10:15:00.000Z",
#   "duration": 840,
#   "queued_duration": 60,
#   "coverage": "95.5",
#   "web_url": "https://gitlab.com/username/project/-/pipelines/12345"
# }
```

#### `retry_pipeline`
Retry a failed pipeline.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `pipeline_id` (int, required): Pipeline ID

**Example:**
```python
result = await retry_pipeline(
    project_id="gitlab-org/gitlab",
    pipeline_id=12345
)

# Returns:
# {
#   "id": 12346,
#   "iid": 568,
#   "status": "pending",
#   "ref": "main",
#   "sha": "a1b2c3d4e5f6",
#   "created_at": "2025-10-08T16:30:00.000Z",
#   "web_url": "https://gitlab.com/username/project/-/pipelines/12346"
# }
```

### Repository Operations

#### `list_commits`
List repository commits.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `ref_name` (string, optional): Branch or tag name (default: default branch)
- `since` (string, optional): Only commits after or on this date (ISO 8601 format)
- `until` (string, optional): Only commits before or on this date (ISO 8601 format)
- `per_page` (int, optional): Results per page (default: 20, max: 100)

**Example:**
```python
# Recent commits on default branch
commits = await list_commits(project_id="gitlab-org/gitlab")

# Commits on specific branch
commits = await list_commits(
    project_id="278964",
    ref_name="develop"
)

# Commits in date range
commits = await list_commits(
    project_id="gitlab-org/gitlab",
    since="2025-10-01T00:00:00Z",
    until="2025-10-08T23:59:59Z"
)

# Returns:
# [
#   {
#     "id": "a1b2c3d4e5f6",
#     "short_id": "a1b2c3d",
#     "title": "Fix authentication bug",
#     "message": "Fix authentication bug\n\nUsers were unable to login with OAuth",
#     "author_name": "John Doe",
#     "author_email": "john@example.com",
#     "authored_date": "2025-10-08T14:30:00.000Z",
#     "committer_name": "John Doe",
#     "committer_email": "john@example.com",
#     "committed_date": "2025-10-08T14:30:00.000Z",
#     "created_at": "2025-10-08T14:30:00.000Z",
#     "parent_ids": ["f6e5d4c3b2a1"],
#     "web_url": "https://gitlab.com/username/project/-/commit/a1b2c3d4e5f6"
#   }
# ]
```

#### `get_commit`
Get detailed information about a specific commit.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `sha` (string, required): Commit SHA or branch/tag name

**Example:**
```python
commit = await get_commit(
    project_id="gitlab-org/gitlab",
    sha="a1b2c3d4e5f6"
)

# Returns:
# {
#   "id": "a1b2c3d4e5f6",
#   "short_id": "a1b2c3d",
#   "title": "Fix authentication bug",
#   "message": "Fix authentication bug\n\nUsers were unable to login with OAuth",
#   "author_name": "John Doe",
#   "author_email": "john@example.com",
#   "authored_date": "2025-10-08T14:30:00.000Z",
#   "committer_name": "John Doe",
#   "committer_email": "john@example.com",
#   "committed_date": "2025-10-08T14:30:00.000Z",
#   "created_at": "2025-10-08T14:30:00.000Z",
#   "parent_ids": ["f6e5d4c3b2a1"],
#   "stats": {
#     "additions": 15,
#     "deletions": 8,
#     "total": 23
#   },
#   "status": "success",
#   "last_pipeline": {
#     "id": 12345,
#     "status": "success",
#     "ref": "main"
#   },
#   "web_url": "https://gitlab.com/username/project/-/commit/a1b2c3d4e5f6"
# }
```

#### `list_branches`
List repository branches.

**Parameters:**
- `project_id` (string, required): Project ID or path
- `search` (string, optional): Search query to filter branches
- `per_page` (int, optional): Results per page (default: 20, max: 100)

**Example:**
```python
# All branches
branches = await list_branches(project_id="gitlab-org/gitlab")

# Search branches
branches = await list_branches(
    project_id="278964",
    search="feature"
)

# Returns:
# [
#   {
#     "name": "main",
#     "merged": false,
#     "protected": true,
#     "default": true,
#     "developers_can_push": false,
#     "developers_can_merge": false,
#     "can_push": true,
#     "commit": {
#       "id": "a1b2c3d4e5f6",
#       "short_id": "a1b2c3d",
#       "title": "Latest commit",
#       "author_name": "John Doe",
#       "author_email": "john@example.com",
#       "created_at": "2025-10-08T14:30:00.000Z",
#       "message": "Latest commit message"
#     },
#     "web_url": "https://gitlab.com/username/project/-/tree/main"
#   }
# ]
```

### Code Search

#### `search_code`
Search code, issues, merge requests, and more across projects.

**Parameters:**
- `scope` (string, required): Search scope (projects, issues, merge_requests, milestones, users, blobs, commits, wiki_blobs)
- `search` (string, required): Search query
- `project_id` (string, optional): Limit search to specific project
- `per_page` (int, optional): Results per page (default: 20, max: 100)

**Search Scopes:**
- `projects`: Search project names and descriptions
- `issues`: Search issue titles and descriptions
- `merge_requests`: Search MR titles and descriptions
- `milestones`: Search milestone titles and descriptions
- `users`: Search usernames and names
- `blobs`: Search file contents (code search)
- `commits`: Search commit messages
- `wiki_blobs`: Search wiki pages

**Example:**
```python
# Search code across all projects
results = await search_code(
    scope="blobs",
    search="def authenticate"
)

# Search code in specific project
results = await search_code(
    scope="blobs",
    search="OAuth2",
    project_id="gitlab-org/gitlab"
)

# Search issues
results = await search_code(
    scope="issues",
    search="authentication bug"
)

# Search commits
results = await search_code(
    scope="commits",
    search="fix bug"
)

# Returns (for blobs scope):
# [
#   {
#     "basename": "auth.py",
#     "data": "def authenticate(user, password):\n    # authentication logic",
#     "path": "src/auth.py",
#     "filename": "src/auth.py",
#     "id": null,
#     "ref": "main",
#     "startline": 42,
#     "project_id": 278964
#   }
# ]
```

## Common Workflows

### Daily Development

```python
# Check my assigned issues
issues = await list_issues(scope="assigned_to_me", state="opened")

# Check my merge requests
mrs = await list_merge_requests(scope="created_by_me", state="opened")

# Check pipeline status for my branch
pipelines = await list_pipelines(
    project_id="278964",
    ref="feature/my-feature"
)
```

### Code Review Process

```python
# Get MR details
mr = await get_merge_request(
    project_id="gitlab-org/gitlab",
    mr_iid=15
)

# Approve the MR
await approve_merge_request(
    project_id="gitlab-org/gitlab",
    mr_iid=15
)

# Merge when pipeline succeeds
await merge_merge_request(
    project_id="gitlab-org/gitlab",
    mr_iid=15,
    should_remove_source_branch=True,
    merge_when_pipeline_succeeds=True
)
```

### Issue Triage

```python
# Get all open issues
issues = await list_issues(
    project_id="278964",
    state="opened"
)

# Assign and label critical issues
for issue in critical_issues:
    await update_issue(
        project_id="278964",
        issue_iid=issue["iid"],
        assignee_ids=[123],
        labels="critical,bug"
    )
```

### CI/CD Management

```python
# Check failed pipelines
failed = await list_pipelines(
    project_id="gitlab-org/gitlab",
    status="failed"
)

# Retry failed pipeline
for pipeline in failed:
    result = await retry_pipeline(
        project_id="gitlab-org/gitlab",
        pipeline_id=pipeline["id"]
    )

# Monitor running pipelines
running = await list_pipelines(
    project_id="278964",
    scope="running"
)
```

### Project Setup

```python
# Create initial issue for project
issue = await create_issue(
    project_id="new-project",
    title="Setup CI/CD pipeline",
    description="Configure GitLab CI with:\n- Build stage\n- Test stage\n- Deploy stage",
    labels="infrastructure,setup"
)

# Create feature branch MR
mr = await create_merge_request(
    project_id="new-project",
    source_branch="setup/ci-cd",
    target_branch="main",
    title="Add GitLab CI configuration",
    description="Adds .gitlab-ci.yml with build, test, and deploy stages"
)
```

### Code Search and Analysis

```python
# Find all uses of deprecated function
results = await search_code(
    scope="blobs",
    search="old_function_name",
    project_id="gitlab-org/gitlab"
)

# Find security-related commits
commits = await search_code(
    scope="commits",
    search="security fix"
)

# Search for specific error message
issues = await search_code(
    scope="issues",
    search="500 Internal Server Error"
)
```

## Issue States

GitLab issues have these states:

- **opened**: New or active issues
- **closed**: Resolved or completed issues
- **reopened**: Previously closed issues that were reopened
- **all**: All issues regardless of state

## Merge Request States

GitLab merge requests have these states:

- **opened**: Active MRs waiting for review/merge
- **closed**: MRs that were closed without merging
- **locked**: MRs that are locked from further changes
- **merged**: MRs that have been merged
- **all**: All MRs regardless of state

## Pipeline States

GitLab pipelines have these statuses:

- **created**: Pipeline created but not started
- **waiting_for_resource**: Waiting for runner
- **preparing**: Runner is preparing
- **pending**: Waiting to run
- **running**: Currently executing
- **success**: Completed successfully
- **failed**: One or more jobs failed
- **canceled**: Manually canceled
- **skipped**: Pipeline was skipped
- **manual**: Waiting for manual action

## Required Token Scopes

For full functionality, your Personal Access Token needs these scopes:

- **api**: Full API access (recommended for all operations)
- **read_api**: Read-only API access
- **read_repository**: Read repository content and metadata
- **write_repository**: Create branches, commits, and tags

## Best Practices

1. **Use project paths**: More readable than numeric IDs (`gitlab-org/gitlab` vs `278964`)
2. **Pagination**: Use `per_page` to limit results for large datasets
3. **Filter early**: Use scope and state filters to reduce API calls
4. **Cache data**: Don't repeatedly fetch unchanged data
5. **Error handling**: Implement retry logic with exponential backoff
6. **Token security**: Never commit tokens to version control
7. **Self-hosted**: Set `GITLAB_URL` for custom instances
8. **Rate limits**: Monitor usage and respect rate limits
9. **Batch operations**: Group related changes together
10. **Use IID**: For issues and MRs, use `iid` (internal ID) not `id`

## Self-Hosted GitLab

This server supports self-hosted GitLab instances:

```bash
# Set your GitLab instance URL
export GITLAB_URL="https://gitlab.mycompany.com"
export GITLAB_PERSONAL_ACCESS_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
```

The server will automatically use your custom instance for all API calls.

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist or no access
- **409 Conflict**: Resource conflict (e.g., branch already exists)
- **422 Unprocessable Entity**: Validation error
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error (retry)

## API Documentation

- [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
- [Personal Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
- [Projects API](https://docs.gitlab.com/ee/api/projects.html)
- [Issues API](https://docs.gitlab.com/ee/api/issues.html)
- [Merge Requests API](https://docs.gitlab.com/ee/api/merge_requests.html)
- [Pipelines API](https://docs.gitlab.com/ee/api/pipelines.html)
- [Search API](https://docs.gitlab.com/ee/api/search.html)
- [Rate Limits](https://docs.gitlab.com/ee/user/gitlab_com/index.html#gitlabcom-specific-rate-limits)

## Support

- [GitLab Support](https://about.gitlab.com/support/)
- [Community Forum](https://forum.gitlab.com/)
- [GitLab Docs](https://docs.gitlab.com/)
- [Status Page](https://status.gitlab.com/)
