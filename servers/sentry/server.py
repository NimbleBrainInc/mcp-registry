import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("Sentry")

AUTH_TOKEN = os.getenv("SENTRY_AUTH_TOKEN")
BASE_URL = "https://sentry.io/api/0"


def get_headers() -> dict:
    """Get headers with Bearer token authentication."""
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }


@mcp.tool()
async def list_organizations() -> list:
    """List all organizations the user has access to."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/organizations/",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_projects(organization_slug: str) -> list:
    """List projects in an organization.

    Args:
        organization_slug: Organization slug (e.g., "my-org")
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/organizations/{organization_slug}/projects/",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_project(
    organization_slug: str,
    project_slug: str
) -> dict:
    """Get project details and statistics.

    Args:
        organization_slug: Organization slug
        project_slug: Project slug (e.g., "my-project")
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/projects/{organization_slug}/{project_slug}/",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_issues(
    organization_slug: str,
    project_slug: Optional[str] = None,
    query: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 25
) -> list:
    """List issues with filters.

    Args:
        organization_slug: Organization slug
        project_slug: Project slug (optional, filters to specific project)
        query: Search query (e.g., "is:unresolved level:error")
        status: Filter by status (unresolved, resolved, ignored)
        limit: Number of issues to return (default: 25, max: 100)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"limit": limit}

        # Build query string
        query_parts = []
        if status:
            query_parts.append(f"is:{status}")
        if project_slug:
            query_parts.append(f"project:{project_slug}")
        if query:
            query_parts.append(query)

        if query_parts:
            params["query"] = " ".join(query_parts)

        response = await client.get(
            f"{BASE_URL}/organizations/{organization_slug}/issues/",
            headers=get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_issue(issue_id: str) -> dict:
    """Get issue details with events.

    Args:
        issue_id: Issue ID (string)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/issues/{issue_id}/",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_issue(
    issue_id: str,
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    has_seen: Optional[bool] = None,
    is_bookmarked: Optional[bool] = None
) -> dict:
    """Update issue status or assignment.

    Args:
        issue_id: Issue ID
        status: New status (resolved, unresolved, ignored, resolvedInNextRelease)
        assigned_to: Username or email to assign to
        has_seen: Mark as seen
        is_bookmarked: Bookmark status
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {}

        if status:
            payload["status"] = status
        if assigned_to:
            payload["assignedTo"] = assigned_to
        if has_seen is not None:
            payload["hasSeen"] = has_seen
        if is_bookmarked is not None:
            payload["isBookmarked"] = is_bookmarked

        response = await client.put(
            f"{BASE_URL}/issues/{issue_id}/",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def resolve_issue(issue_id: str) -> dict:
    """Mark issue as resolved.

    Args:
        issue_id: Issue ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.put(
            f"{BASE_URL}/issues/{issue_id}/",
            headers=get_headers(),
            json={"status": "resolved"}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def ignore_issue(issue_id: str) -> dict:
    """Ignore an issue.

    Args:
        issue_id: Issue ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.put(
            f"{BASE_URL}/issues/{issue_id}/",
            headers=get_headers(),
            json={"status": "ignored"}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_events(
    issue_id: str,
    limit: int = 25
) -> list:
    """List error events for an issue.

    Args:
        issue_id: Issue ID
        limit: Number of events to return (default: 25, max: 100)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/issues/{issue_id}/events/",
            headers=get_headers(),
            params={"limit": limit}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_event(
    organization_slug: str,
    project_slug: str,
    event_id: str
) -> dict:
    """Get detailed event information with stack trace.

    Args:
        organization_slug: Organization slug
        project_slug: Project slug
        event_id: Event ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/projects/{organization_slug}/{project_slug}/events/{event_id}/",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_releases(
    organization_slug: str,
    project_slug: str,
    limit: int = 25
) -> list:
    """List releases in a project.

    Args:
        organization_slug: Organization slug
        project_slug: Project slug
        limit: Number of releases to return (default: 25, max: 100)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/projects/{organization_slug}/{project_slug}/releases/",
            headers=get_headers(),
            params={"limit": limit}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_release(
    organization_slug: str,
    version: str
) -> dict:
    """Get release details with commits.

    Args:
        organization_slug: Organization slug
        version: Release version (e.g., "1.0.0")
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/organizations/{organization_slug}/releases/{version}/",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_release(
    organization_slug: str,
    version: str,
    projects: List[str],
    refs: Optional[List[Dict[str, str]]] = None,
    commits: Optional[List[Dict[str, str]]] = None,
    date_released: Optional[str] = None
) -> dict:
    """Create a new release.

    Args:
        organization_slug: Organization slug
        version: Release version (e.g., "1.0.0")
        projects: List of project slugs
        refs: List of repository references [{"repository": "repo", "commit": "sha"}]
        commits: List of commits [{"id": "sha", "message": "msg"}]
        date_released: ISO 8601 datetime (optional)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "version": version,
            "projects": projects
        }

        if refs:
            payload["refs"] = refs
        if commits:
            payload["commits"] = commits
        if date_released:
            payload["dateReleased"] = date_released

        response = await client.post(
            f"{BASE_URL}/organizations/{organization_slug}/releases/",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_teams(organization_slug: str) -> list:
    """List teams in organization.

    Args:
        organization_slug: Organization slug
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/organizations/{organization_slug}/teams/",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_project_stats(
    organization_slug: str,
    project_slug: str,
    stat: str = "received",
    resolution: str = "1h"
) -> list:
    """Get project error statistics.

    Args:
        organization_slug: Organization slug
        project_slug: Project slug
        stat: Stat type (received, rejected, blacklisted)
        resolution: Time resolution (1h, 1d, 1w)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/projects/{organization_slug}/{project_slug}/stats/",
            headers=get_headers(),
            params={"stat": stat, "resolution": resolution}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_issues(
    organization_slug: str,
    query: str,
    limit: int = 25,
    sort: str = "date"
) -> list:
    """Search issues with query filters.

    Args:
        organization_slug: Organization slug
        query: Search query (e.g., "is:unresolved assigned:me level:error")
        limit: Number of results (default: 25, max: 100)
        sort: Sort by (date, new, freq, priority, user)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/organizations/{organization_slug}/issues/",
            headers=get_headers(),
            params={
                "query": query,
                "limit": limit,
                "sort": sort
            }
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
