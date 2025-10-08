import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("Asana")

ACCESS_TOKEN = os.getenv("ASANA_PERSONAL_ACCESS_TOKEN")
BASE_URL = "https://app.asana.com/api/1.0"


def get_headers() -> dict:
    """Get headers with Bearer token authorization."""
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }


async def api_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None
) -> dict:
    """Make API request to Asana."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method,
            f"{BASE_URL}{endpoint}",
            headers=get_headers(),
            params=params,
            json=json
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_workspaces(
    limit: int = 20,
    opt_fields: Optional[str] = None
) -> dict:
    """List all accessible workspaces.

    Args:
        limit: Number of results per page (default: 20, max: 100)
        opt_fields: Comma-separated field names to include in response
    """
    params = {"limit": limit}
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", "/workspaces", params=params)


@mcp.tool()
async def list_projects(
    workspace: str,
    archived: bool = False,
    limit: int = 20,
    opt_fields: Optional[str] = None
) -> dict:
    """List projects in a workspace.

    Args:
        workspace: Workspace GID
        archived: Only return archived projects (default: false)
        limit: Number of results per page (default: 20, max: 100)
        opt_fields: Comma-separated field names to include
    """
    params = {
        "workspace": workspace,
        "archived": archived,
        "limit": limit
    }
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", "/projects", params=params)


@mcp.tool()
async def get_project(
    project_gid: str,
    opt_fields: Optional[str] = None
) -> dict:
    """Get project details.

    Args:
        project_gid: Project GID
        opt_fields: Comma-separated field names to include
    """
    params = {}
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", f"/projects/{project_gid}", params=params)


@mcp.tool()
async def create_project(
    workspace: str,
    name: str,
    notes: Optional[str] = None,
    color: Optional[str] = None,
    due_date: Optional[str] = None,
    start_date: Optional[str] = None,
    public: bool = True
) -> dict:
    """Create a new project.

    Args:
        workspace: Workspace GID
        name: Project name
        notes: Project description
        color: Project color (light-pink, light-green, light-orange, light-yellow, light-teal, light-blue, light-purple, light-warm-gray, dark-pink, dark-green, dark-orange, dark-yellow, dark-teal, dark-blue, dark-purple, dark-warm-gray)
        due_date: Due date (YYYY-MM-DD)
        start_date: Start date (YYYY-MM-DD)
        public: Whether project is public to organization
    """
    data = {
        "data": {
            "workspace": workspace,
            "name": name,
            "public": public
        }
    }
    if notes:
        data["data"]["notes"] = notes
    if color:
        data["data"]["color"] = color
    if due_date:
        data["data"]["due_date"] = due_date
    if start_date:
        data["data"]["start_date"] = start_date

    return await api_request("POST", "/projects", json=data)


@mcp.tool()
async def list_tasks(
    project: Optional[str] = None,
    section: Optional[str] = None,
    assignee: Optional[str] = None,
    workspace: Optional[str] = None,
    completed_since: Optional[str] = None,
    modified_since: Optional[str] = None,
    limit: int = 20,
    opt_fields: Optional[str] = None
) -> dict:
    """List tasks with filters.

    Args:
        project: Filter to tasks in project GID
        section: Filter to tasks in section GID
        assignee: Filter to tasks assigned to user GID (or "me")
        workspace: Workspace GID (required if not using project/section)
        completed_since: Only return tasks completed after this time (ISO 8601)
        modified_since: Only return tasks modified after this time (ISO 8601)
        limit: Number of results per page (default: 20, max: 100)
        opt_fields: Comma-separated field names to include
    """
    params = {"limit": limit}
    if project:
        params["project"] = project
    if section:
        params["section"] = section
    if assignee:
        params["assignee"] = assignee
    if workspace:
        params["workspace"] = workspace
    if completed_since:
        params["completed_since"] = completed_since
    if modified_since:
        params["modified_since"] = modified_since
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", "/tasks", params=params)


@mcp.tool()
async def get_task(
    task_gid: str,
    opt_fields: Optional[str] = None
) -> dict:
    """Get task details.

    Args:
        task_gid: Task GID
        opt_fields: Comma-separated field names to include
    """
    params = {}
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", f"/tasks/{task_gid}", params=params)


@mcp.tool()
async def create_task(
    workspace: Optional[str] = None,
    projects: Optional[List[str]] = None,
    name: str = "",
    notes: Optional[str] = None,
    assignee: Optional[str] = None,
    due_on: Optional[str] = None,
    start_on: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> dict:
    """Create a new task.

    Args:
        workspace: Workspace GID (required if projects not provided)
        projects: List of project GIDs to add task to
        name: Task name
        notes: Task description
        assignee: Assignee user GID (or "me")
        due_on: Due date (YYYY-MM-DD)
        start_on: Start date (YYYY-MM-DD)
        tags: List of tag GIDs
    """
    data = {"data": {"name": name}}

    if workspace:
        data["data"]["workspace"] = workspace
    if projects:
        data["data"]["projects"] = projects
    if notes:
        data["data"]["notes"] = notes
    if assignee:
        data["data"]["assignee"] = assignee
    if due_on:
        data["data"]["due_on"] = due_on
    if start_on:
        data["data"]["start_on"] = start_on
    if tags:
        data["data"]["tags"] = tags

    return await api_request("POST", "/tasks", json=data)


@mcp.tool()
async def update_task(
    task_gid: str,
    name: Optional[str] = None,
    notes: Optional[str] = None,
    assignee: Optional[str] = None,
    due_on: Optional[str] = None,
    start_on: Optional[str] = None,
    completed: Optional[bool] = None
) -> dict:
    """Update task details.

    Args:
        task_gid: Task GID
        name: Updated task name
        notes: Updated task description
        assignee: Updated assignee GID (or "me", or null to unassign)
        due_on: Updated due date (YYYY-MM-DD, or null to clear)
        start_on: Updated start date (YYYY-MM-DD, or null to clear)
        completed: Whether task is completed
    """
    data = {"data": {}}

    if name is not None:
        data["data"]["name"] = name
    if notes is not None:
        data["data"]["notes"] = notes
    if assignee is not None:
        data["data"]["assignee"] = assignee
    if due_on is not None:
        data["data"]["due_on"] = due_on
    if start_on is not None:
        data["data"]["start_on"] = start_on
    if completed is not None:
        data["data"]["completed"] = completed

    return await api_request("PUT", f"/tasks/{task_gid}", json=data)


@mcp.tool()
async def complete_task(task_gid: str) -> dict:
    """Mark task as complete.

    Args:
        task_gid: Task GID
    """
    data = {"data": {"completed": True}}
    return await api_request("PUT", f"/tasks/{task_gid}", json=data)


@mcp.tool()
async def delete_task(task_gid: str) -> dict:
    """Delete a task.

    Args:
        task_gid: Task GID
    """
    return await api_request("DELETE", f"/tasks/{task_gid}")


@mcp.tool()
async def add_task_comment(
    task_gid: str,
    text: str
) -> dict:
    """Add a comment to a task.

    Args:
        task_gid: Task GID
        text: Comment text
    """
    data = {"data": {"text": text}}
    return await api_request("POST", f"/tasks/{task_gid}/stories", json=data)


@mcp.tool()
async def list_sections(
    project_gid: str,
    limit: int = 20,
    opt_fields: Optional[str] = None
) -> dict:
    """List sections in a project.

    Args:
        project_gid: Project GID
        limit: Number of results per page (default: 20, max: 100)
        opt_fields: Comma-separated field names to include
    """
    params = {"limit": limit}
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", f"/projects/{project_gid}/sections", params=params)


@mcp.tool()
async def create_section(
    project_gid: str,
    name: str
) -> dict:
    """Create a section in a project.

    Args:
        project_gid: Project GID
        name: Section name
    """
    data = {"data": {"name": name}}
    return await api_request("POST", f"/projects/{project_gid}/sections", json=data)


@mcp.tool()
async def list_tags(
    workspace: str,
    limit: int = 20,
    opt_fields: Optional[str] = None
) -> dict:
    """List tags in a workspace.

    Args:
        workspace: Workspace GID
        limit: Number of results per page (default: 20, max: 100)
        opt_fields: Comma-separated field names to include
    """
    params = {
        "workspace": workspace,
        "limit": limit
    }
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", "/tags", params=params)


@mcp.tool()
async def create_tag(
    workspace: str,
    name: str,
    color: Optional[str] = None
) -> dict:
    """Create a new tag.

    Args:
        workspace: Workspace GID
        name: Tag name
        color: Tag color (dark-pink, dark-green, dark-blue, dark-red, dark-teal, dark-brown, dark-orange, dark-purple, dark-warm-gray, light-pink, light-green, light-blue, light-red, light-teal, light-brown, light-orange, light-purple, light-warm-gray, none)
    """
    data = {
        "data": {
            "workspace": workspace,
            "name": name
        }
    }
    if color:
        data["data"]["color"] = color

    return await api_request("POST", "/tags", json=data)


@mcp.tool()
async def search_workspace(
    workspace: str,
    resource_type: str,
    query: str,
    limit: int = 20,
    opt_fields: Optional[str] = None
) -> dict:
    """Search for tasks, projects, or users in a workspace.

    Args:
        workspace: Workspace GID
        resource_type: Type to search (task, project, user, portfolio, tag)
        query: Search query string
        limit: Number of results per page (default: 20, max: 100)
        opt_fields: Comma-separated field names to include
    """
    params = {
        "workspace": workspace,
        "resource_type": resource_type,
        "query": query,
        "limit": limit
    }
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", "/typeahead", params=params)


@mcp.tool()
async def list_portfolios(
    workspace: str,
    owner: Optional[str] = None,
    limit: int = 20,
    opt_fields: Optional[str] = None
) -> dict:
    """List portfolios in a workspace.

    Args:
        workspace: Workspace GID
        owner: Filter to portfolios owned by user GID (or "me")
        limit: Number of results per page (default: 20, max: 100)
        opt_fields: Comma-separated field names to include
    """
    params = {
        "workspace": workspace,
        "limit": limit
    }
    if owner:
        params["owner"] = owner
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", "/portfolios", params=params)


@mcp.tool()
async def get_user(
    user_gid: str,
    opt_fields: Optional[str] = None
) -> dict:
    """Get user details.

    Args:
        user_gid: User GID (or "me" for current user)
        opt_fields: Comma-separated field names to include
    """
    params = {}
    if opt_fields:
        params["opt_fields"] = opt_fields

    return await api_request("GET", f"/users/{user_gid}", params=params)


if __name__ == "__main__":
    mcp.run()
