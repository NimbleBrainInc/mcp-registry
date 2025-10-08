import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("ClickUp")

API_TOKEN = os.getenv("CLICKUP_API_TOKEN")
BASE_URL = "https://api.clickup.com/api/v2"


def get_headers() -> dict:
    """Get headers with API token authentication."""
    return {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }


@mcp.tool()
async def list_workspaces() -> dict:
    """List all accessible workspaces (teams)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/team",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_spaces(
    workspace_id: str,
    archived: bool = False
) -> dict:
    """List spaces in a workspace.

    Args:
        workspace_id: Workspace (team) ID
        archived: Include archived spaces (default: false)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/team/{workspace_id}/space",
            headers=get_headers(),
            params={"archived": str(archived).lower()}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_space(space_id: str) -> dict:
    """Get space details.

    Args:
        space_id: Space ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/space/{space_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_folders(
    space_id: str,
    archived: bool = False
) -> dict:
    """List folders in a space.

    Args:
        space_id: Space ID
        archived: Include archived folders (default: false)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/space/{space_id}/folder",
            headers=get_headers(),
            params={"archived": str(archived).lower()}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_lists(
    folder_id: Optional[str] = None,
    space_id: Optional[str] = None,
    archived: bool = False
) -> dict:
    """List lists in a folder or space.

    Args:
        folder_id: Folder ID (provide either folder_id or space_id)
        space_id: Space ID (for folderless lists)
        archived: Include archived lists (default: false)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        if folder_id:
            url = f"{BASE_URL}/folder/{folder_id}/list"
        elif space_id:
            url = f"{BASE_URL}/space/{space_id}/list"
        else:
            raise ValueError("Either folder_id or space_id must be provided")

        response = await client.get(
            url,
            headers=get_headers(),
            params={"archived": str(archived).lower()}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_tasks(
    list_id: str,
    archived: bool = False,
    page: int = 0,
    order_by: str = "created",
    reverse: bool = True,
    subtasks: bool = True,
    statuses: Optional[List[str]] = None,
    include_closed: bool = False,
    assignees: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    due_date_gt: Optional[int] = None,
    due_date_lt: Optional[int] = None
) -> dict:
    """List tasks with filters.

    Args:
        list_id: List ID
        archived: Include archived tasks (default: false)
        page: Page number (default: 0)
        order_by: Order by field (created, updated, due_date)
        reverse: Reverse order (default: true)
        subtasks: Include subtasks (default: true)
        statuses: Filter by status names
        include_closed: Include closed tasks (default: false)
        assignees: Filter by assignee user IDs
        tags: Filter by tag names
        due_date_gt: Due date greater than (Unix timestamp ms)
        due_date_lt: Due date less than (Unix timestamp ms)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {
            "archived": str(archived).lower(),
            "page": page,
            "order_by": order_by,
            "reverse": str(reverse).lower(),
            "subtasks": str(subtasks).lower(),
            "include_closed": str(include_closed).lower()
        }

        if statuses:
            params["statuses[]"] = statuses
        if assignees:
            params["assignees[]"] = assignees
        if tags:
            params["tags[]"] = tags
        if due_date_gt:
            params["due_date_gt"] = due_date_gt
        if due_date_lt:
            params["due_date_lt"] = due_date_lt

        response = await client.get(
            f"{BASE_URL}/list/{list_id}/task",
            headers=get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_task(task_id: str) -> dict:
    """Get task details with custom fields.

    Args:
        task_id: Task ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/task/{task_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_task(
    list_id: str,
    name: str,
    description: Optional[str] = None,
    assignees: Optional[List[int]] = None,
    tags: Optional[List[str]] = None,
    status: Optional[str] = None,
    priority: Optional[int] = None,
    due_date: Optional[int] = None,
    due_date_time: bool = False,
    time_estimate: Optional[int] = None,
    start_date: Optional[int] = None,
    start_date_time: bool = False,
    notify_all: bool = True,
    parent: Optional[str] = None,
    custom_fields: Optional[List[Dict[str, Any]]] = None
) -> dict:
    """Create a new task.

    Args:
        list_id: List ID
        name: Task name (required)
        description: Task description
        assignees: List of assignee user IDs
        tags: List of tag names
        status: Status name
        priority: Priority (1=urgent, 2=high, 3=normal, 4=low)
        due_date: Due date (Unix timestamp ms)
        due_date_time: Include time in due date (default: false)
        time_estimate: Time estimate in milliseconds
        start_date: Start date (Unix timestamp ms)
        start_date_time: Include time in start date (default: false)
        notify_all: Notify all assignees (default: true)
        parent: Parent task ID (for subtasks)
        custom_fields: List of custom field objects
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "name": name,
            "notify_all": notify_all
        }

        if description:
            payload["description"] = description
        if assignees:
            payload["assignees"] = assignees
        if tags:
            payload["tags"] = tags
        if status:
            payload["status"] = status
        if priority:
            payload["priority"] = priority
        if due_date:
            payload["due_date"] = due_date
            payload["due_date_time"] = due_date_time
        if time_estimate:
            payload["time_estimate"] = time_estimate
        if start_date:
            payload["start_date"] = start_date
            payload["start_date_time"] = start_date_time
        if parent:
            payload["parent"] = parent
        if custom_fields:
            payload["custom_fields"] = custom_fields

        response = await client.post(
            f"{BASE_URL}/list/{list_id}/task",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_task(
    task_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[int] = None,
    due_date: Optional[int] = None,
    time_estimate: Optional[int] = None,
    assignees: Optional[Dict[str, List[int]]] = None
) -> dict:
    """Update task details.

    Args:
        task_id: Task ID
        name: Updated task name
        description: Updated description
        status: Updated status
        priority: Updated priority (1-4)
        due_date: Updated due date (Unix timestamp ms)
        time_estimate: Updated time estimate (ms)
        assignees: Assignees object {"add": [user_ids], "rem": [user_ids]}
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {}

        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if status:
            payload["status"] = status
        if priority:
            payload["priority"] = priority
        if due_date:
            payload["due_date"] = due_date
        if time_estimate:
            payload["time_estimate"] = time_estimate
        if assignees:
            payload["assignees"] = assignees

        response = await client.put(
            f"{BASE_URL}/task/{task_id}",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def delete_task(task_id: str) -> dict:
    """Delete a task.

    Args:
        task_id: Task ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.delete(
            f"{BASE_URL}/task/{task_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return {"success": True, "task_id": task_id}


@mcp.tool()
async def add_task_comment(
    task_id: str,
    comment_text: str,
    assignee: Optional[int] = None,
    notify_all: bool = True
) -> dict:
    """Add comment to a task.

    Args:
        task_id: Task ID
        comment_text: Comment text
        assignee: Assign comment to user ID
        notify_all: Notify all task assignees (default: true)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "comment_text": comment_text,
            "notify_all": notify_all
        }

        if assignee:
            payload["assignee"] = assignee

        response = await client.post(
            f"{BASE_URL}/task/{task_id}/comment",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_task_comments(task_id: str) -> dict:
    """Get task comments.

    Args:
        task_id: Task ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/task/{task_id}/comment",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_time_entry(
    task_id: str,
    duration: int,
    start: Optional[int] = None,
    description: Optional[str] = None
) -> dict:
    """Track time on a task.

    Args:
        task_id: Task ID
        duration: Duration in milliseconds
        start: Start time (Unix timestamp ms, defaults to now)
        description: Time entry description
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {"duration": duration}

        if start:
            payload["start"] = start
        if description:
            payload["description"] = description

        response = await client.post(
            f"{BASE_URL}/task/{task_id}/time",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_time_entries(
    workspace_id: str,
    start_date: Optional[int] = None,
    end_date: Optional[int] = None,
    assignee: Optional[int] = None
) -> dict:
    """Get time tracking entries.

    Args:
        workspace_id: Workspace (team) ID
        start_date: Filter by start date (Unix timestamp ms)
        end_date: Filter by end date (Unix timestamp ms)
        assignee: Filter by assignee user ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if assignee:
            params["assignee"] = assignee

        response = await client.get(
            f"{BASE_URL}/team/{workspace_id}/time_entries",
            headers=get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_goals(workspace_id: str) -> dict:
    """List goals in a workspace.

    Args:
        workspace_id: Workspace (team) ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/team/{workspace_id}/goal",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_goal(goal_id: str) -> dict:
    """Get goal details and progress.

    Args:
        goal_id: Goal ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/goal/{goal_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_custom_fields(list_id: str) -> dict:
    """Get custom fields for a list.

    Args:
        list_id: List ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/list/{list_id}/field",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_tasks(
    workspace_id: str,
    query: str,
    start_date: Optional[int] = None,
    end_date: Optional[int] = None,
    assignees: Optional[List[int]] = None,
    statuses: Optional[List[str]] = None,
    tags: Optional[List[str]] = None
) -> dict:
    """Search tasks across workspace.

    Args:
        workspace_id: Workspace (team) ID
        query: Search query text
        start_date: Filter by start date (Unix timestamp ms)
        end_date: Filter by end date (Unix timestamp ms)
        assignees: Filter by assignee user IDs
        statuses: Filter by status names
        tags: Filter by tag names
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"query": query}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if assignees:
            params["assignees[]"] = assignees
        if statuses:
            params["statuses[]"] = statuses
        if tags:
            params["tags[]"] = tags

        response = await client.get(
            f"{BASE_URL}/team/{workspace_id}/task",
            headers=get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
