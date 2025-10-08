import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("Todoist")

API_TOKEN = os.getenv("TODOIST_API_TOKEN")
BASE_URL = "https://api.todoist.com/rest/v2"


def get_headers() -> dict:
    """Get headers with Bearer token authentication."""
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }


@mcp.tool()
async def list_tasks(
    project_id: Optional[str] = None,
    label: Optional[str] = None,
    filter: Optional[str] = None,
    lang: str = "en"
) -> list:
    """List all active tasks with optional filters.

    Args:
        project_id: Filter by project ID
        label: Filter by label name
        filter: Filter string (e.g., "today", "p1", "overdue")
        lang: Language for filter parsing (default: en)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"lang": lang}
        if project_id:
            params["project_id"] = project_id
        if label:
            params["label"] = label
        if filter:
            params["filter"] = filter

        response = await client.get(
            f"{BASE_URL}/tasks",
            headers=get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_task(task_id: str) -> dict:
    """Get specific task details.

    Args:
        task_id: Task ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_task(
    content: str,
    description: Optional[str] = None,
    project_id: Optional[str] = None,
    section_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    order: Optional[int] = None,
    labels: Optional[List[str]] = None,
    priority: int = 1,
    due_string: Optional[str] = None,
    due_date: Optional[str] = None,
    due_datetime: Optional[str] = None,
    due_lang: str = "en",
    assignee_id: Optional[str] = None
) -> dict:
    """Create a new task.

    Args:
        content: Task content (required)
        description: Task description
        project_id: Project ID
        section_id: Section ID
        parent_id: Parent task ID (for subtasks)
        order: Task position order
        labels: List of label names
        priority: Priority from 1 (normal) to 4 (urgent)
        due_string: Natural language due date (e.g., "tomorrow at 3pm")
        due_date: Due date in YYYY-MM-DD format
        due_datetime: Due datetime in RFC 3339 format
        due_lang: Language for due_string parsing (default: en)
        assignee_id: User ID to assign task to
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "content": content,
            "priority": priority,
            "due_lang": due_lang
        }

        if description:
            payload["description"] = description
        if project_id:
            payload["project_id"] = project_id
        if section_id:
            payload["section_id"] = section_id
        if parent_id:
            payload["parent_id"] = parent_id
        if order is not None:
            payload["order"] = order
        if labels:
            payload["labels"] = labels
        if due_string:
            payload["due_string"] = due_string
        if due_date:
            payload["due_date"] = due_date
        if due_datetime:
            payload["due_datetime"] = due_datetime
        if assignee_id:
            payload["assignee_id"] = assignee_id

        response = await client.post(
            f"{BASE_URL}/tasks",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_task(
    task_id: str,
    content: Optional[str] = None,
    description: Optional[str] = None,
    labels: Optional[List[str]] = None,
    priority: Optional[int] = None,
    due_string: Optional[str] = None,
    due_date: Optional[str] = None,
    due_datetime: Optional[str] = None,
    due_lang: str = "en",
    assignee_id: Optional[str] = None
) -> dict:
    """Update task details.

    Args:
        task_id: Task ID
        content: Updated task content
        description: Updated description
        labels: Updated list of label names
        priority: Updated priority (1-4)
        due_string: Natural language due date
        due_date: Due date in YYYY-MM-DD format
        due_datetime: Due datetime in RFC 3339 format
        due_lang: Language for due_string parsing (default: en)
        assignee_id: User ID to assign task to
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {"due_lang": due_lang}

        if content:
            payload["content"] = content
        if description:
            payload["description"] = description
        if labels:
            payload["labels"] = labels
        if priority:
            payload["priority"] = priority
        if due_string:
            payload["due_string"] = due_string
        if due_date:
            payload["due_date"] = due_date
        if due_datetime:
            payload["due_datetime"] = due_datetime
        if assignee_id:
            payload["assignee_id"] = assignee_id

        response = await client.post(
            f"{BASE_URL}/tasks/{task_id}",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def complete_task(task_id: str) -> dict:
    """Mark task as completed.

    Args:
        task_id: Task ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/tasks/{task_id}/close",
            headers=get_headers()
        )
        response.raise_for_status()
        return {"success": True, "task_id": task_id}


@mcp.tool()
async def reopen_task(task_id: str) -> dict:
    """Reopen a completed task.

    Args:
        task_id: Task ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/tasks/{task_id}/reopen",
            headers=get_headers()
        )
        response.raise_for_status()
        return {"success": True, "task_id": task_id}


@mcp.tool()
async def delete_task(task_id: str) -> dict:
    """Delete a task.

    Args:
        task_id: Task ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.delete(
            f"{BASE_URL}/tasks/{task_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return {"success": True, "task_id": task_id}


@mcp.tool()
async def list_projects() -> list:
    """List all projects."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/projects",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_project(project_id: str) -> dict:
    """Get project details.

    Args:
        project_id: Project ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/projects/{project_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_project(
    name: str,
    parent_id: Optional[str] = None,
    color: Optional[str] = None,
    is_favorite: bool = False,
    view_style: str = "list"
) -> dict:
    """Create a new project.

    Args:
        name: Project name (required)
        parent_id: Parent project ID (for nested projects)
        color: Color name (e.g., "red", "blue", "green")
        is_favorite: Mark as favorite
        view_style: View style ("list" or "board")
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "name": name,
            "is_favorite": is_favorite,
            "view_style": view_style
        }

        if parent_id:
            payload["parent_id"] = parent_id
        if color:
            payload["color"] = color

        response = await client.post(
            f"{BASE_URL}/projects",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_project(
    project_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    view_style: Optional[str] = None
) -> dict:
    """Update project details.

    Args:
        project_id: Project ID
        name: Updated project name
        color: Updated color name
        is_favorite: Updated favorite status
        view_style: Updated view style ("list" or "board")
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {}

        if name:
            payload["name"] = name
        if color:
            payload["color"] = color
        if is_favorite is not None:
            payload["is_favorite"] = is_favorite
        if view_style:
            payload["view_style"] = view_style

        response = await client.post(
            f"{BASE_URL}/projects/{project_id}",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def delete_project(project_id: str) -> dict:
    """Delete a project.

    Args:
        project_id: Project ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.delete(
            f"{BASE_URL}/projects/{project_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return {"success": True, "project_id": project_id}


@mcp.tool()
async def list_sections(project_id: Optional[str] = None) -> list:
    """List sections in a project.

    Args:
        project_id: Project ID (optional, returns all sections if not provided)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {}
        if project_id:
            params["project_id"] = project_id

        response = await client.get(
            f"{BASE_URL}/sections",
            headers=get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_section(
    name: str,
    project_id: str,
    order: Optional[int] = None
) -> dict:
    """Create a new section.

    Args:
        name: Section name (required)
        project_id: Project ID (required)
        order: Section position order
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "name": name,
            "project_id": project_id
        }

        if order is not None:
            payload["order"] = order

        response = await client.post(
            f"{BASE_URL}/sections",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_labels() -> list:
    """List all labels."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/labels",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_label(
    name: str,
    color: Optional[str] = None,
    order: Optional[int] = None,
    is_favorite: bool = False
) -> dict:
    """Create a new label.

    Args:
        name: Label name (required)
        color: Color name (e.g., "red", "blue", "green")
        order: Label position order
        is_favorite: Mark as favorite
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "name": name,
            "is_favorite": is_favorite
        }

        if color:
            payload["color"] = color
        if order is not None:
            payload["order"] = order

        response = await client.post(
            f"{BASE_URL}/labels",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_comments(
    task_id: Optional[str] = None,
    project_id: Optional[str] = None
) -> list:
    """Get comments for a task or project.

    Args:
        task_id: Task ID (provide either task_id or project_id)
        project_id: Project ID (provide either task_id or project_id)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {}
        if task_id:
            params["task_id"] = task_id
        elif project_id:
            params["project_id"] = project_id

        response = await client.get(
            f"{BASE_URL}/comments",
            headers=get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_comment(
    content: str,
    task_id: Optional[str] = None,
    project_id: Optional[str] = None,
    attachment: Optional[Dict[str, Any]] = None
) -> dict:
    """Add a comment to a task or project.

    Args:
        content: Comment content (required)
        task_id: Task ID (provide either task_id or project_id)
        project_id: Project ID (provide either task_id or project_id)
        attachment: File attachment object with "file_name", "file_type", "file_url"
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {"content": content}

        if task_id:
            payload["task_id"] = task_id
        elif project_id:
            payload["project_id"] = project_id

        if attachment:
            payload["attachment"] = attachment

        response = await client.post(
            f"{BASE_URL}/comments",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
