"""
Airtable MCP Server
Provides tools for managing Airtable bases, tables, and records.
"""

import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Airtable MCP Server")

# Get API credentials from environment
AIRTABLE_ACCESS_TOKEN = os.getenv("AIRTABLE_ACCESS_TOKEN")
BASE_URL = "https://api.airtable.com/v0"


def get_headers() -> dict:
    """Get headers for Airtable API requests."""
    if not AIRTABLE_ACCESS_TOKEN:
        raise ValueError("AIRTABLE_ACCESS_TOKEN environment variable is required")
    return {
        "Authorization": f"Bearer {AIRTABLE_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }


@mcp.tool()
async def list_bases() -> dict:
    """
    List all accessible Airtable bases.

    Returns:
        Dictionary containing list of bases with IDs, names, and permission levels
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.airtable.com/v0/meta/bases",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_base_schema(base_id: str) -> dict:
    """
    Get schema for a base including all tables and field definitions.

    Args:
        base_id: Base ID (starts with 'app', e.g., 'appXXXXXXXXXXXXXX')

    Returns:
        Dictionary containing base schema with tables, fields, and views
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_records(
    base_id: str,
    table_id_or_name: str,
    fields: Optional[List[str]] = None,
    filter_by_formula: Optional[str] = None,
    max_records: Optional[int] = None,
    page_size: Optional[int] = None,
    sort: Optional[List[Dict[str, str]]] = None,
    view: Optional[str] = None,
    offset: Optional[str] = None
) -> dict:
    """
    List records from a table with optional filters and sorting.

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name
        fields: List of field names to return (optional, returns all if not specified)
        filter_by_formula: Airtable formula to filter records (e.g., "{Status} = 'Active'")
        max_records: Maximum number of records to return (optional)
        page_size: Number of records per page (max: 100, default: 100)
        sort: List of sort objects with 'field' and 'direction' (e.g., [{"field": "Name", "direction": "asc"}])
        view: Name or ID of a view to use (optional)
        offset: Pagination offset from previous response (optional)

    Returns:
        Dictionary containing records and optional offset for pagination
    """
    async with httpx.AsyncClient() as client:
        params = {}

        if fields:
            for field in fields:
                params[f"fields[]"] = field
        if filter_by_formula:
            params["filterByFormula"] = filter_by_formula
        if max_records:
            params["maxRecords"] = max_records
        if page_size:
            params["pageSize"] = page_size
        if view:
            params["view"] = view
        if offset:
            params["offset"] = offset
        if sort:
            for i, sort_item in enumerate(sort):
                params[f"sort[{i}][field]"] = sort_item["field"]
                params[f"sort[{i}][direction]"] = sort_item.get("direction", "asc")

        response = await client.get(
            f"{BASE_URL}/{base_id}/{table_id_or_name}",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_record(
    base_id: str,
    table_id_or_name: str,
    record_id: str
) -> dict:
    """
    Get a specific record by ID.

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name
        record_id: Record ID (starts with 'rec', e.g., 'recXXXXXXXXXXXXXX')

    Returns:
        Dictionary containing the record with all fields
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/{base_id}/{table_id_or_name}/{record_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_record(
    base_id: str,
    table_id_or_name: str,
    fields: Dict[str, Any]
) -> dict:
    """
    Create a new record in a table.

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name
        fields: Dictionary of field names and values (e.g., {"Name": "John", "Age": 30})

    Returns:
        Dictionary containing the created record with ID and fields
    """
    async with httpx.AsyncClient() as client:
        data = {"fields": fields}

        response = await client.post(
            f"{BASE_URL}/{base_id}/{table_id_or_name}",
            headers=get_headers(),
            json=data,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_record(
    base_id: str,
    table_id_or_name: str,
    record_id: str,
    fields: Dict[str, Any],
    replace_all: bool = False
) -> dict:
    """
    Update an existing record.

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name
        record_id: Record ID (starts with 'rec')
        fields: Dictionary of field names and values to update
        replace_all: If True, replace all fields (PUT). If False, merge fields (PATCH). Default: False

    Returns:
        Dictionary containing the updated record
    """
    async with httpx.AsyncClient() as client:
        data = {"fields": fields}

        if replace_all:
            response = await client.put(
                f"{BASE_URL}/{base_id}/{table_id_or_name}/{record_id}",
                headers=get_headers(),
                json=data,
            )
        else:
            response = await client.patch(
                f"{BASE_URL}/{base_id}/{table_id_or_name}/{record_id}",
                headers=get_headers(),
                json=data,
            )

        response.raise_for_status()
        return response.json()


@mcp.tool()
async def delete_record(
    base_id: str,
    table_id_or_name: str,
    record_id: str
) -> dict:
    """
    Delete a record from a table.

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name
        record_id: Record ID (starts with 'rec')

    Returns:
        Dictionary containing deleted record ID and deletion status
    """
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{BASE_URL}/{base_id}/{table_id_or_name}/{record_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_records(
    base_id: str,
    table_id_or_name: str,
    formula: str,
    fields: Optional[List[str]] = None,
    sort: Optional[List[Dict[str, str]]] = None,
    max_records: Optional[int] = None
) -> dict:
    """
    Search records using Airtable formula filters.

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name
        formula: Airtable formula filter (e.g., "AND({Status} = 'Active', {Age} > 25)")
        fields: List of field names to return (optional)
        sort: List of sort objects (optional)
        max_records: Maximum number of records to return (optional)

    Returns:
        Dictionary containing matching records
    """
    return await list_records(
        base_id=base_id,
        table_id_or_name=table_id_or_name,
        fields=fields,
        filter_by_formula=formula,
        max_records=max_records,
        sort=sort
    )


@mcp.tool()
async def bulk_create_records(
    base_id: str,
    table_id_or_name: str,
    records: List[Dict[str, Any]]
) -> dict:
    """
    Create multiple records at once (up to 10 per request).

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name
        records: List of record objects with 'fields' (max: 10 records)

    Returns:
        Dictionary containing list of created records with IDs
    """
    async with httpx.AsyncClient() as client:
        # Ensure records have the correct format
        formatted_records = [{"fields": r} if "fields" not in r else r for r in records]

        data = {"records": formatted_records[:10]}  # Limit to 10 records

        response = await client.post(
            f"{BASE_URL}/{base_id}/{table_id_or_name}",
            headers=get_headers(),
            json=data,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def bulk_update_records(
    base_id: str,
    table_id_or_name: str,
    records: List[Dict[str, Any]],
    replace_all: bool = False
) -> dict:
    """
    Update multiple records at once (up to 10 per request).

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name
        records: List of record objects with 'id' and 'fields' (max: 10 records)
        replace_all: If True, replace all fields. If False, merge fields. Default: False

    Returns:
        Dictionary containing list of updated records
    """
    async with httpx.AsyncClient() as client:
        data = {"records": records[:10]}  # Limit to 10 records

        if replace_all:
            response = await client.put(
                f"{BASE_URL}/{base_id}/{table_id_or_name}",
                headers=get_headers(),
                json=data,
            )
        else:
            response = await client.patch(
                f"{BASE_URL}/{base_id}/{table_id_or_name}",
                headers=get_headers(),
                json=data,
            )

        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_table_fields(
    base_id: str,
    table_id_or_name: str
) -> dict:
    """
    Get field definitions for a specific table.

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name

    Returns:
        Dictionary containing field definitions with types, options, and descriptions
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
            headers=get_headers(),
        )
        response.raise_for_status()
        schema = response.json()

        # Find the specific table
        for table in schema.get("tables", []):
            if table["id"] == table_id_or_name or table["name"] == table_id_or_name:
                return {
                    "table_id": table["id"],
                    "table_name": table["name"],
                    "fields": table.get("fields", [])
                }

        return {"error": "Table not found"}


@mcp.tool()
async def list_views(
    base_id: str,
    table_id_or_name: str
) -> dict:
    """
    List all views in a table.

    Args:
        base_id: Base ID (e.g., 'appXXXXXXXXXXXXXX')
        table_id_or_name: Table ID or URL-encoded table name

    Returns:
        Dictionary containing list of views with IDs, names, and types
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
            headers=get_headers(),
        )
        response.raise_for_status()
        schema = response.json()

        # Find the specific table
        for table in schema.get("tables", []):
            if table["id"] == table_id_or_name or table["name"] == table_id_or_name:
                return {
                    "table_id": table["id"],
                    "table_name": table["name"],
                    "views": table.get("views", [])
                }

        return {"error": "Table not found"}


if __name__ == "__main__":
    mcp.run()
