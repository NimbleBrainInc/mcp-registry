import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("GitLab")

ACCESS_TOKEN = os.getenv("GITLAB_PERSONAL_ACCESS_TOKEN")
GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
BASE_URL = f"{GITLAB_URL}/api/v4"


def get_headers() -> dict:
    """Get headers with access token authorization."""
    return {
        "PRIVATE-TOKEN": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }


async def api_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None
) -> dict:
    """Make API request to GitLab."""
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
async def list_projects(
    visibility: Optional[str] = None,
    owned: bool = False,
    starred: bool = False,
    archived: bool = False,
    per_page: int = 20
) -> dict:
    """List accessible projects.

    Args:
        visibility: Filter by visibility (public, internal, private)
        owned: Limit to owned projects
        starred: Limit to starred projects
        archived: Include archived projects (default: false)
        per_page: Results per page (default: 20, max: 100)
    """
    params = {"per_page": per_page, "archived": archived}
    if visibility:
        params["visibility"] = visibility
    if owned:
        params["owned"] = True
    if starred:
        params["starred"] = True

    return await api_request("GET", "/projects", params=params)


@mcp.tool()
async def get_project(project_id: str) -> dict:
    """Get project details.

    Args:
        project_id: Project ID or path (e.g., "123" or "namespace/project")
    """
    # URL encode the project ID/path
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")
    return await api_request("GET", f"/projects/{encoded_id}")


@mcp.tool()
async def list_issues(
    project_id: Optional[str] = None,
    state: Optional[str] = None,
    labels: Optional[str] = None,
    milestone: Optional[str] = None,
    assignee_id: Optional[int] = None,
    author_id: Optional[int] = None,
    scope: Optional[str] = None,
    per_page: int = 20
) -> dict:
    """List issues with filters.

    Args:
        project_id: Project ID or path (if not provided, returns all accessible issues)
        state: Filter by state (opened, closed, all)
        labels: Comma-separated label names
        milestone: Milestone title
        assignee_id: Assignee user ID
        author_id: Author user ID
        scope: Filter by scope (created_by_me, assigned_to_me, all)
        per_page: Results per page (default: 20, max: 100)
    """
    params = {"per_page": per_page}
    if state:
        params["state"] = state
    if labels:
        params["labels"] = labels
    if milestone:
        params["milestone"] = milestone
    if assignee_id:
        params["assignee_id"] = assignee_id
    if author_id:
        params["author_id"] = author_id
    if scope:
        params["scope"] = scope

    if project_id:
        import urllib.parse
        encoded_id = urllib.parse.quote(project_id, safe="")
        return await api_request("GET", f"/projects/{encoded_id}/issues", params=params)
    else:
        return await api_request("GET", "/issues", params=params)


@mcp.tool()
async def get_issue(project_id: str, issue_iid: int) -> dict:
    """Get issue details.

    Args:
        project_id: Project ID or path
        issue_iid: Issue IID (internal ID within project)
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")
    return await api_request("GET", f"/projects/{encoded_id}/issues/{issue_iid}")


@mcp.tool()
async def create_issue(
    project_id: str,
    title: str,
    description: Optional[str] = None,
    assignee_ids: Optional[List[int]] = None,
    labels: Optional[str] = None,
    milestone_id: Optional[int] = None,
    confidential: bool = False
) -> dict:
    """Create a new issue.

    Args:
        project_id: Project ID or path
        title: Issue title
        description: Issue description (markdown supported)
        assignee_ids: List of assignee user IDs
        labels: Comma-separated label names
        milestone_id: Milestone ID
        confidential: Whether issue is confidential
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")

    data = {
        "title": title,
        "confidential": confidential
    }
    if description:
        data["description"] = description
    if assignee_ids:
        data["assignee_ids"] = assignee_ids
    if labels:
        data["labels"] = labels
    if milestone_id:
        data["milestone_id"] = milestone_id

    return await api_request("POST", f"/projects/{encoded_id}/issues", json=data)


@mcp.tool()
async def update_issue(
    project_id: str,
    issue_iid: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    state_event: Optional[str] = None,
    assignee_ids: Optional[List[int]] = None,
    labels: Optional[str] = None
) -> dict:
    """Update an issue.

    Args:
        project_id: Project ID or path
        issue_iid: Issue IID
        title: Updated title
        description: Updated description
        state_event: State event (close, reopen)
        assignee_ids: Updated assignee IDs
        labels: Updated labels
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")

    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if state_event:
        data["state_event"] = state_event
    if assignee_ids is not None:
        data["assignee_ids"] = assignee_ids
    if labels is not None:
        data["labels"] = labels

    return await api_request("PUT", f"/projects/{encoded_id}/issues/{issue_iid}", json=data)


@mcp.tool()
async def list_merge_requests(
    project_id: Optional[str] = None,
    state: Optional[str] = None,
    scope: Optional[str] = None,
    author_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    reviewer_id: Optional[int] = None,
    labels: Optional[str] = None,
    per_page: int = 20
) -> dict:
    """List merge requests.

    Args:
        project_id: Project ID or path (if not provided, returns all accessible MRs)
        state: Filter by state (opened, closed, locked, merged, all)
        scope: Filter by scope (created_by_me, assigned_to_me, all)
        author_id: Author user ID
        assignee_id: Assignee user ID
        reviewer_id: Reviewer user ID
        labels: Comma-separated label names
        per_page: Results per page (default: 20, max: 100)
    """
    params = {"per_page": per_page}
    if state:
        params["state"] = state
    if scope:
        params["scope"] = scope
    if author_id:
        params["author_id"] = author_id
    if assignee_id:
        params["assignee_id"] = assignee_id
    if reviewer_id:
        params["reviewer_id"] = reviewer_id
    if labels:
        params["labels"] = labels

    if project_id:
        import urllib.parse
        encoded_id = urllib.parse.quote(project_id, safe="")
        return await api_request("GET", f"/projects/{encoded_id}/merge_requests", params=params)
    else:
        return await api_request("GET", "/merge_requests", params=params)


@mcp.tool()
async def get_merge_request(project_id: str, mr_iid: int) -> dict:
    """Get merge request details.

    Args:
        project_id: Project ID or path
        mr_iid: Merge request IID
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")
    return await api_request("GET", f"/projects/{encoded_id}/merge_requests/{mr_iid}")


@mcp.tool()
async def create_merge_request(
    project_id: str,
    source_branch: str,
    target_branch: str,
    title: str,
    description: Optional[str] = None,
    assignee_id: Optional[int] = None,
    reviewer_ids: Optional[List[int]] = None,
    labels: Optional[str] = None,
    remove_source_branch: bool = False
) -> dict:
    """Create a new merge request.

    Args:
        project_id: Project ID or path
        source_branch: Source branch name
        target_branch: Target branch name
        title: MR title
        description: MR description (markdown supported)
        assignee_id: Assignee user ID
        reviewer_ids: List of reviewer user IDs
        labels: Comma-separated label names
        remove_source_branch: Delete source branch after merge
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")

    data = {
        "source_branch": source_branch,
        "target_branch": target_branch,
        "title": title,
        "remove_source_branch": remove_source_branch
    }
    if description:
        data["description"] = description
    if assignee_id:
        data["assignee_id"] = assignee_id
    if reviewer_ids:
        data["reviewer_ids"] = reviewer_ids
    if labels:
        data["labels"] = labels

    return await api_request("POST", f"/projects/{encoded_id}/merge_requests", json=data)


@mcp.tool()
async def approve_merge_request(project_id: str, mr_iid: int) -> dict:
    """Approve a merge request.

    Args:
        project_id: Project ID or path
        mr_iid: Merge request IID
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")
    return await api_request("POST", f"/projects/{encoded_id}/merge_requests/{mr_iid}/approve")


@mcp.tool()
async def merge_merge_request(
    project_id: str,
    mr_iid: int,
    merge_commit_message: Optional[str] = None,
    should_remove_source_branch: bool = False,
    merge_when_pipeline_succeeds: bool = False
) -> dict:
    """Merge a merge request.

    Args:
        project_id: Project ID or path
        mr_iid: Merge request IID
        merge_commit_message: Custom merge commit message
        should_remove_source_branch: Delete source branch after merge
        merge_when_pipeline_succeeds: Merge when pipeline succeeds
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")

    data = {
        "should_remove_source_branch": should_remove_source_branch,
        "merge_when_pipeline_succeeds": merge_when_pipeline_succeeds
    }
    if merge_commit_message:
        data["merge_commit_message"] = merge_commit_message

    return await api_request("PUT", f"/projects/{encoded_id}/merge_requests/{mr_iid}/merge", json=data)


@mcp.tool()
async def list_pipelines(
    project_id: str,
    scope: Optional[str] = None,
    status: Optional[str] = None,
    ref: Optional[str] = None,
    per_page: int = 20
) -> dict:
    """List CI/CD pipelines.

    Args:
        project_id: Project ID or path
        scope: Filter by scope (running, pending, finished, branches, tags)
        status: Filter by status (created, waiting_for_resource, preparing, pending, running, success, failed, canceled, skipped, manual)
        ref: Filter by ref (branch or tag name)
        per_page: Results per page (default: 20, max: 100)
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")

    params = {"per_page": per_page}
    if scope:
        params["scope"] = scope
    if status:
        params["status"] = status
    if ref:
        params["ref"] = ref

    return await api_request("GET", f"/projects/{encoded_id}/pipelines", params=params)


@mcp.tool()
async def get_pipeline(project_id: str, pipeline_id: int) -> dict:
    """Get pipeline details.

    Args:
        project_id: Project ID or path
        pipeline_id: Pipeline ID
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")
    return await api_request("GET", f"/projects/{encoded_id}/pipelines/{pipeline_id}")


@mcp.tool()
async def retry_pipeline(project_id: str, pipeline_id: int) -> dict:
    """Retry a failed pipeline.

    Args:
        project_id: Project ID or path
        pipeline_id: Pipeline ID
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")
    return await api_request("POST", f"/projects/{encoded_id}/pipelines/{pipeline_id}/retry")


@mcp.tool()
async def list_commits(
    project_id: str,
    ref_name: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    per_page: int = 20
) -> dict:
    """List repository commits.

    Args:
        project_id: Project ID or path
        ref_name: Branch or tag name (default: default branch)
        since: Only commits after or on this date (ISO 8601 format)
        until: Only commits before or on this date (ISO 8601 format)
        per_page: Results per page (default: 20, max: 100)
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")

    params = {"per_page": per_page}
    if ref_name:
        params["ref_name"] = ref_name
    if since:
        params["since"] = since
    if until:
        params["until"] = until

    return await api_request("GET", f"/projects/{encoded_id}/repository/commits", params=params)


@mcp.tool()
async def get_commit(project_id: str, sha: str) -> dict:
    """Get commit details.

    Args:
        project_id: Project ID or path
        sha: Commit SHA or branch/tag name
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")
    encoded_sha = urllib.parse.quote(sha, safe="")
    return await api_request("GET", f"/projects/{encoded_id}/repository/commits/{encoded_sha}")


@mcp.tool()
async def search_code(
    scope: str,
    search: str,
    project_id: Optional[str] = None,
    per_page: int = 20
) -> dict:
    """Search code across projects.

    Args:
        scope: Search scope (projects, issues, merge_requests, milestones, users, blobs, commits, wiki_blobs)
        search: Search query
        project_id: Limit search to specific project ID or path
        per_page: Results per page (default: 20, max: 100)
    """
    params = {
        "scope": scope,
        "search": search,
        "per_page": per_page
    }
    if project_id:
        import urllib.parse
        encoded_id = urllib.parse.quote(project_id, safe="")
        params["project_id"] = encoded_id

    return await api_request("GET", "/search", params=params)


@mcp.tool()
async def list_branches(
    project_id: str,
    search: Optional[str] = None,
    per_page: int = 20
) -> dict:
    """List repository branches.

    Args:
        project_id: Project ID or path
        search: Search query to filter branches
        per_page: Results per page (default: 20, max: 100)
    """
    import urllib.parse
    encoded_id = urllib.parse.quote(project_id, safe="")

    params = {"per_page": per_page}
    if search:
        params["search"] = search

    return await api_request("GET", f"/projects/{encoded_id}/repository/branches", params=params)


if __name__ == "__main__":
    mcp.run()
