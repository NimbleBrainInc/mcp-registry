import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("Linear")

API_KEY = os.getenv("LINEAR_API_KEY")
BASE_URL = "https://api.linear.app/graphql"


def get_headers() -> dict:
    """Get headers with API key authorization."""
    return {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }


async def graphql_query(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    """Execute GraphQL query."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            BASE_URL,
            headers=get_headers(),
            json={"query": query, "variables": variables or {}}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_issues(
    team_id: Optional[str] = None,
    project_id: Optional[str] = None,
    assignee_id: Optional[str] = None,
    label_id: Optional[str] = None,
    state: Optional[str] = None,
    first: int = 50
) -> dict:
    """List issues with filters.

    Args:
        team_id: Filter by team ID
        project_id: Filter by project ID
        assignee_id: Filter by assignee ID
        label_id: Filter by label ID
        state: Filter by state (backlog, unstarted, started, completed, canceled)
        first: Number of issues to return (default: 50)
    """
    filters = []
    if team_id:
        filters.append(f'team: {{ id: {{ eq: "{team_id}" }} }}')
    if project_id:
        filters.append(f'project: {{ id: {{ eq: "{project_id}" }} }}')
    if assignee_id:
        filters.append(f'assignee: {{ id: {{ eq: "{assignee_id}" }} }}')
    if label_id:
        filters.append(f'labels: {{ id: {{ eq: "{label_id}" }} }}')
    if state:
        filters.append(f'state: {{ name: {{ eq: "{state}" }} }}')

    filter_str = ", ".join(filters) if filters else ""

    query = f"""
    query {{
      issues(first: {first}, filter: {{ {filter_str} }}) {{
        nodes {{
          id
          title
          description
          priority
          state {{
            name
            type
          }}
          assignee {{
            id
            name
          }}
          labels {{
            nodes {{
              id
              name
            }}
          }}
          createdAt
          updatedAt
        }}
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def get_issue(issue_id: str) -> dict:
    """Get issue details.

    Args:
        issue_id: Issue ID
    """
    query = f"""
    query {{
      issue(id: "{issue_id}") {{
        id
        title
        description
        priority
        estimate
        state {{
          name
          type
        }}
        assignee {{
          id
          name
          email
        }}
        labels {{
          nodes {{
            id
            name
            color
          }}
        }}
        project {{
          id
          name
        }}
        team {{
          id
          name
        }}
        createdAt
        updatedAt
        url
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def create_issue(
    team_id: str,
    title: str,
    description: Optional[str] = None,
    priority: int = 0,
    assignee_id: Optional[str] = None,
    project_id: Optional[str] = None,
    label_ids: Optional[List[str]] = None
) -> dict:
    """Create a new issue.

    Args:
        team_id: Team ID (required)
        title: Issue title (required)
        description: Issue description in markdown
        priority: Priority (0=none, 1=urgent, 2=high, 3=medium, 4=low)
        assignee_id: Assignee user ID
        project_id: Project ID
        label_ids: List of label IDs
    """
    input_fields = [
        f'teamId: "{team_id}"',
        f'title: "{title}"',
        f'priority: {priority}'
    ]

    if description:
        input_fields.append(f'description: "{description}"')
    if assignee_id:
        input_fields.append(f'assigneeId: "{assignee_id}"')
    if project_id:
        input_fields.append(f'projectId: "{project_id}"')
    if label_ids:
        label_ids_str = ", ".join([f'"{lid}"' for lid in label_ids])
        input_fields.append(f'labelIds: [{label_ids_str}]')

    input_str = ", ".join(input_fields)

    mutation = f"""
    mutation {{
      issueCreate(input: {{ {input_str} }}) {{
        success
        issue {{
          id
          title
          url
        }}
      }}
    }}
    """

    return await graphql_query(mutation)


@mcp.tool()
async def update_issue(
    issue_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[int] = None,
    state_id: Optional[str] = None,
    assignee_id: Optional[str] = None
) -> dict:
    """Update issue details.

    Args:
        issue_id: Issue ID
        title: Updated title
        description: Updated description
        priority: Updated priority (0-4)
        state_id: Updated state ID
        assignee_id: Updated assignee ID
    """
    updates = []
    if title:
        updates.append(f'title: "{title}"')
    if description:
        updates.append(f'description: "{description}"')
    if priority is not None:
        updates.append(f'priority: {priority}')
    if state_id:
        updates.append(f'stateId: "{state_id}"')
    if assignee_id:
        updates.append(f'assigneeId: "{assignee_id}"')

    update_str = ", ".join(updates) if updates else ""

    mutation = f"""
    mutation {{
      issueUpdate(id: "{issue_id}", input: {{ {update_str} }}) {{
        success
        issue {{
          id
          title
          state {{
            name
          }}
        }}
      }}
    }}
    """

    return await graphql_query(mutation)


@mcp.tool()
async def delete_issue(issue_id: str) -> dict:
    """Delete an issue.

    Args:
        issue_id: Issue ID
    """
    mutation = f"""
    mutation {{
      issueDelete(id: "{issue_id}") {{
        success
      }}
    }}
    """

    return await graphql_query(mutation)


@mcp.tool()
async def add_comment(
    issue_id: str,
    body: str
) -> dict:
    """Add comment to an issue.

    Args:
        issue_id: Issue ID
        body: Comment body in markdown
    """
    mutation = f"""
    mutation {{
      commentCreate(input: {{ issueId: "{issue_id}", body: "{body}" }}) {{
        success
        comment {{
          id
          body
          createdAt
        }}
      }}
    }}
    """

    return await graphql_query(mutation)


@mcp.tool()
async def list_projects(
    team_id: Optional[str] = None,
    first: int = 50
) -> dict:
    """List all projects.

    Args:
        team_id: Filter by team ID
        first: Number of projects to return (default: 50)
    """
    filter_str = f'filter: {{ team: {{ id: {{ eq: "{team_id}" }} }} }}' if team_id else ""

    query = f"""
    query {{
      projects(first: {first}, {filter_str}) {{
        nodes {{
          id
          name
          description
          state
          progress
          targetDate
          lead {{
            id
            name
          }}
          createdAt
        }}
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def get_project(project_id: str) -> dict:
    """Get project details.

    Args:
        project_id: Project ID
    """
    query = f"""
    query {{
      project(id: "{project_id}") {{
        id
        name
        description
        state
        progress
        targetDate
        startDate
        lead {{
          id
          name
        }}
        teams {{
          nodes {{
            id
            name
          }}
        }}
        url
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def create_project(
    name: str,
    team_ids: List[str],
    description: Optional[str] = None,
    target_date: Optional[str] = None,
    lead_id: Optional[str] = None
) -> dict:
    """Create a new project.

    Args:
        name: Project name (required)
        team_ids: List of team IDs (required)
        description: Project description
        target_date: Target completion date (YYYY-MM-DD)
        lead_id: Project lead user ID
    """
    team_ids_str = ", ".join([f'"{tid}"' for tid in team_ids])
    input_fields = [
        f'name: "{name}"',
        f'teamIds: [{team_ids_str}]'
    ]

    if description:
        input_fields.append(f'description: "{description}"')
    if target_date:
        input_fields.append(f'targetDate: "{target_date}"')
    if lead_id:
        input_fields.append(f'leadId: "{lead_id}"')

    input_str = ", ".join(input_fields)

    mutation = f"""
    mutation {{
      projectCreate(input: {{ {input_str} }}) {{
        success
        project {{
          id
          name
          url
        }}
      }}
    }}
    """

    return await graphql_query(mutation)


@mcp.tool()
async def list_teams() -> dict:
    """List all teams."""
    query = """
    query {
      teams {
        nodes {
          id
          name
          key
          description
          private
          createdAt
        }
      }
    }
    """

    return await graphql_query(query)


@mcp.tool()
async def get_team(team_id: str) -> dict:
    """Get team details.

    Args:
        team_id: Team ID
    """
    query = f"""
    query {{
      team(id: "{team_id}") {{
        id
        name
        key
        description
        private
        members {{
          nodes {{
            id
            name
            email
          }}
        }}
        projects {{
          nodes {{
            id
            name
          }}
        }}
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def list_cycles(
    team_id: Optional[str] = None,
    first: int = 20
) -> dict:
    """List sprint cycles.

    Args:
        team_id: Filter by team ID
        first: Number of cycles to return (default: 20)
    """
    filter_str = f'filter: {{ team: {{ id: {{ eq: "{team_id}" }} }} }}' if team_id else ""

    query = f"""
    query {{
      cycles(first: {first}, {filter_str}) {{
        nodes {{
          id
          number
          name
          startsAt
          endsAt
          progress
          completedIssueCount
          issueCount
          team {{
            id
            name
          }}
        }}
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def get_cycle(cycle_id: str) -> dict:
    """Get cycle details.

    Args:
        cycle_id: Cycle ID
    """
    query = f"""
    query {{
      cycle(id: "{cycle_id}") {{
        id
        number
        name
        description
        startsAt
        endsAt
        progress
        completedIssueCount
        issueCount
        team {{
          id
          name
        }}
        url
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def list_labels(team_id: Optional[str] = None) -> dict:
    """List all labels.

    Args:
        team_id: Filter by team ID
    """
    filter_str = f'filter: {{ team: {{ id: {{ eq: "{team_id}" }} }} }}' if team_id else ""

    query = f"""
    query {{
      issueLabels({filter_str}) {{
        nodes {{
          id
          name
          description
          color
          team {{
            id
            name
          }}
        }}
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def create_label(
    name: str,
    team_id: str,
    color: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """Create a new label.

    Args:
        name: Label name (required)
        team_id: Team ID (required)
        color: Hex color (e.g., "#FF0000")
        description: Label description
    """
    input_fields = [
        f'name: "{name}"',
        f'teamId: "{team_id}"'
    ]

    if color:
        input_fields.append(f'color: "{color}"')
    if description:
        input_fields.append(f'description: "{description}"')

    input_str = ", ".join(input_fields)

    mutation = f"""
    mutation {{
      issueLabelCreate(input: {{ {input_str} }}) {{
        success
        issueLabel {{
          id
          name
          color
        }}
      }}
    }}
    """

    return await graphql_query(mutation)


@mcp.tool()
async def search_issues(
    query_text: str,
    first: int = 20
) -> dict:
    """Search issues with query.

    Args:
        query_text: Search query
        first: Number of results (default: 20)
    """
    query = f"""
    query {{
      issueSearch(query: "{query_text}", first: {first}) {{
        nodes {{
          id
          title
          description
          state {{
            name
          }}
          assignee {{
            name
          }}
          url
        }}
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def get_roadmap(first: int = 50) -> dict:
    """Get roadmap items.

    Args:
        first: Number of items to return (default: 50)
    """
    query = f"""
    query {{
      projects(first: {first}) {{
        nodes {{
          id
          name
          description
          state
          progress
          targetDate
          startDate
          lead {{
            name
          }}
        }}
      }}
    }}
    """

    return await graphql_query(query)


@mcp.tool()
async def list_milestones(
    project_id: Optional[str] = None,
    first: int = 50
) -> dict:
    """List project milestones.

    Args:
        project_id: Filter by project ID
        first: Number of milestones to return (default: 50)
    """
    filter_str = f'filter: {{ project: {{ id: {{ eq: "{project_id}" }} }} }}' if project_id else ""

    query = f"""
    query {{
      projectMilestones(first: {first}, {filter_str}) {{
        nodes {{
          id
          name
          description
          targetDate
          project {{
            id
            name
          }}
        }}
      }}
    }}
    """

    return await graphql_query(query)


if __name__ == "__main__":
    mcp.run()
