"""
Pinecone MCP Server
Provides tools for managing vector databases with Pinecone.
"""

import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Pinecone MCP Server")

# Get API credentials from environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
CONTROL_PLANE_URL = "https://api.pinecone.io"


def get_headers() -> dict:
    """Get headers for Pinecone API requests."""
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY environment variable is required")
    return {
        "Api-Key": PINECONE_API_KEY,
        "Content-Type": "application/json",
    }


def get_index_host(index_name: str) -> str:
    """Construct index host URL."""
    if not PINECONE_ENVIRONMENT:
        raise ValueError("PINECONE_ENVIRONMENT environment variable is required")
    return f"https://{index_name}-{PINECONE_ENVIRONMENT}.svc.pinecone.io"


@mcp.tool()
async def list_indexes() -> dict:
    """
    List all indexes in the project.

    Returns:
        Dictionary with list of indexes and their configurations
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{CONTROL_PLANE_URL}/indexes",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_index(
    name: str,
    dimension: int,
    metric: str = "cosine",
    spec_type: str = "serverless",
    cloud: str = "aws",
    region: str = "us-east-1"
) -> dict:
    """
    Create a new vector index.

    Args:
        name: Index name
        dimension: Vector dimension (e.g., 1536 for OpenAI, 768 for sentence-transformers)
        metric: Distance metric ('cosine', 'euclidean', 'dotproduct', default: 'cosine')
        spec_type: Index type ('serverless' or 'pod', default: 'serverless')
        cloud: Cloud provider ('aws', 'gcp', 'azure', default: 'aws')
        region: Region (e.g., 'us-east-1', 'us-west-2', default: 'us-east-1')

    Returns:
        Dictionary with index creation status
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "name": name,
            "dimension": dimension,
            "metric": metric,
            "spec": {
                spec_type: {
                    "cloud": cloud,
                    "region": region
                }
            }
        }

        response = await client.post(
            f"{CONTROL_PLANE_URL}/indexes",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def describe_index(index_name: str) -> dict:
    """
    Get index configuration and stats.

    Args:
        index_name: Name of the index

    Returns:
        Dictionary with index details including dimension, metric, and status
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{CONTROL_PLANE_URL}/indexes/{index_name}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def delete_index(index_name: str) -> dict:
    """
    Delete an index.

    Args:
        index_name: Name of the index to delete

    Returns:
        Dictionary with deletion status
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.delete(
            f"{CONTROL_PLANE_URL}/indexes/{index_name}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return {"status": "deleted", "index": index_name}


@mcp.tool()
async def upsert_vectors(
    index_name: str,
    vectors: List[Dict[str, Any]],
    namespace: str = ""
) -> dict:
    """
    Insert or update vectors with metadata.

    Args:
        index_name: Name of the index
        vectors: List of vector objects with 'id', 'values', and optional 'metadata'
        namespace: Namespace for data isolation (default: "" for default namespace)

    Returns:
        Dictionary with upsert count

    Example vector: {"id": "vec1", "values": [0.1, 0.2, ...], "metadata": {"key": "value"}}
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        index_host = get_index_host(index_name)
        payload = {
            "vectors": vectors,
            "namespace": namespace
        }

        response = await client.post(
            f"{index_host}/vectors/upsert",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def query_vectors(
    index_name: str,
    vector: Optional[List[float]] = None,
    id: Optional[str] = None,
    top_k: int = 10,
    namespace: str = "",
    include_values: bool = False,
    include_metadata: bool = True,
    filter: Optional[Dict[str, Any]] = None
) -> dict:
    """
    Query similar vectors by vector or ID.

    Args:
        index_name: Name of the index
        vector: Query vector values (use this OR id, not both)
        id: ID of vector to use as query (use this OR vector, not both)
        top_k: Number of results to return (default: 10)
        namespace: Namespace to query (default: "")
        include_values: Include vector values in response (default: False)
        include_metadata: Include metadata in response (default: True)
        filter: Metadata filter for hybrid search (optional)

    Returns:
        Dictionary with matches including ids, scores, and optional metadata

    Filter example: {"genre": {"$eq": "drama"}, "year": {"$gte": 2020}}
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        index_host = get_index_host(index_name)
        payload = {
            "topK": top_k,
            "namespace": namespace,
            "includeValues": include_values,
            "includeMetadata": include_metadata
        }

        if vector:
            payload["vector"] = vector
        elif id:
            payload["id"] = id
        else:
            raise ValueError("Must provide either 'vector' or 'id' parameter")

        if filter:
            payload["filter"] = filter

        response = await client.post(
            f"{index_host}/query",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def fetch_vectors(
    index_name: str,
    ids: List[str],
    namespace: str = ""
) -> dict:
    """
    Fetch vectors by IDs.

    Args:
        index_name: Name of the index
        ids: List of vector IDs to fetch
        namespace: Namespace (default: "")

    Returns:
        Dictionary with vectors including values and metadata
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        index_host = get_index_host(index_name)
        params = {
            "ids": ids,
            "namespace": namespace
        }

        response = await client.get(
            f"{index_host}/vectors/fetch",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def delete_vectors(
    index_name: str,
    ids: Optional[List[str]] = None,
    delete_all: bool = False,
    namespace: str = "",
    filter: Optional[Dict[str, Any]] = None
) -> dict:
    """
    Delete vectors by IDs or metadata filter.

    Args:
        index_name: Name of the index
        ids: List of vector IDs to delete (optional)
        delete_all: Delete all vectors in namespace (default: False)
        namespace: Namespace (default: "")
        filter: Metadata filter for deletion (optional)

    Returns:
        Dictionary with deletion status

    Note: Provide either ids, delete_all=True, or filter
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        index_host = get_index_host(index_name)
        payload = {"namespace": namespace}

        if ids:
            payload["ids"] = ids
        elif delete_all:
            payload["deleteAll"] = True
        elif filter:
            payload["filter"] = filter
        else:
            raise ValueError("Must provide 'ids', 'delete_all=True', or 'filter'")

        response = await client.post(
            f"{index_host}/vectors/delete",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return {"status": "deleted"}


@mcp.tool()
async def update_vector(
    index_name: str,
    id: str,
    values: Optional[List[float]] = None,
    set_metadata: Optional[Dict[str, Any]] = None,
    namespace: str = ""
) -> dict:
    """
    Update vector values or metadata.

    Args:
        index_name: Name of the index
        id: Vector ID to update
        values: New vector values (optional)
        set_metadata: Metadata to set (optional)
        namespace: Namespace (default: "")

    Returns:
        Dictionary with update status

    Note: Provide either values, set_metadata, or both
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        index_host = get_index_host(index_name)
        payload = {
            "id": id,
            "namespace": namespace
        }

        if values:
            payload["values"] = values
        if set_metadata:
            payload["setMetadata"] = set_metadata

        if not values and not set_metadata:
            raise ValueError("Must provide 'values' or 'set_metadata'")

        response = await client.post(
            f"{index_host}/vectors/update",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return {"status": "updated", "id": id}


@mcp.tool()
async def describe_index_stats(
    index_name: str,
    filter: Optional[Dict[str, Any]] = None
) -> dict:
    """
    Get index statistics including vector count and dimension.

    Args:
        index_name: Name of the index
        filter: Optional metadata filter to get stats for subset

    Returns:
        Dictionary with total vector count, dimension, index fullness, and namespace stats
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        index_host = get_index_host(index_name)
        payload = {}
        if filter:
            payload["filter"] = filter

        response = await client.post(
            f"{index_host}/describe_index_stats",
            headers=get_headers(),
            json=payload if filter else None,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_vector_ids(
    index_name: str,
    namespace: str = "",
    prefix: Optional[str] = None,
    limit: Optional[int] = None
) -> dict:
    """
    List all vector IDs in a namespace.

    Args:
        index_name: Name of the index
        namespace: Namespace (default: "")
        prefix: Filter IDs by prefix (optional)
        limit: Maximum number of IDs to return (optional)

    Returns:
        Dictionary with list of vector IDs
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        index_host = get_index_host(index_name)
        payload = {"namespace": namespace}

        if prefix:
            payload["prefix"] = prefix
        if limit:
            payload["limit"] = limit

        response = await client.post(
            f"{index_host}/vectors/list",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_collection(
    name: str,
    source_index: str
) -> dict:
    """
    Create a collection from an index (for backups).

    Args:
        name: Collection name
        source_index: Source index name

    Returns:
        Dictionary with collection creation status
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "name": name,
            "source": source_index
        }

        response = await client.post(
            f"{CONTROL_PLANE_URL}/collections",
            headers=get_headers(),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
