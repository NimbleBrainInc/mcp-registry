"""
Brave Search MCP Server
Provides access to Brave Search API for web search, news, and images.
Privacy-focused search alternative with no tracking.
"""

import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Brave Search API")

# Brave Search API configuration
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
BRAVE_BASE_URL = "https://api.search.brave.com/res/v1"

if not BRAVE_API_KEY:
    raise ValueError("BRAVE_API_KEY environment variable is required")


async def make_brave_request(
    endpoint: str,
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """Make a request to Brave Search API"""
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    
    url = f"{BRAVE_BASE_URL}/{endpoint}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def web_search(
    query: str,
    count: int = 10,
    offset: int = 0,
    country: Optional[str] = None,
    search_lang: Optional[str] = None,
    safesearch: str = "moderate",
    freshness: Optional[str] = None,
    text_decorations: bool = True,
    spellcheck: bool = True
) -> Dict[str, Any]:
    """
    Perform a web search using Brave Search.
    
    Args:
        query: Search query string
        count: Number of results (1-20, default: 10)
        offset: Pagination offset (default: 0)
        country: Country code for localized results (e.g., "US", "GB", "FR")
        search_lang: Language for search (e.g., "en", "es", "fr")
        safesearch: Safe search level ("off", "moderate", "strict")
        freshness: Time filter ("pd" = past day, "pw" = past week, "pm" = past month, "py" = past year)
        text_decorations: Include text decorations (default: True)
        spellcheck: Enable spell checking (default: True)
    
    Returns:
        Search results with web pages, descriptions, and metadata
    """
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": offset,
        "safesearch": safesearch,
        "text_decorations": text_decorations,
        "spellcheck": spellcheck
    }
    
    if country:
        params["country"] = country
    if search_lang:
        params["search_lang"] = search_lang
    if freshness:
        params["freshness"] = freshness
    
    result = await make_brave_request("web/search", params)
    return result


@mcp.tool()
async def news_search(
    query: str,
    count: int = 10,
    offset: int = 0,
    country: Optional[str] = None,
    search_lang: Optional[str] = None,
    freshness: Optional[str] = None,
    spellcheck: bool = True
) -> Dict[str, Any]:
    """
    Search for news articles using Brave Search.
    
    Args:
        query: Search query string
        count: Number of results (1-20, default: 10)
        offset: Pagination offset
        country: Country code for localized news
        search_lang: Language for search
        freshness: Time filter (pd, pw, pm, py)
        spellcheck: Enable spell checking (default: True)
    
    Returns:
        News articles with titles, descriptions, sources, and publication dates
    """
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": offset,
        "spellcheck": spellcheck
    }
    
    if country:
        params["country"] = country
    if search_lang:
        params["search_lang"] = search_lang
    if freshness:
        params["freshness"] = freshness
    
    result = await make_brave_request("news/search", params)
    return result


@mcp.tool()
async def image_search(
    query: str,
    count: int = 10,
    offset: int = 0,
    country: Optional[str] = None,
    search_lang: Optional[str] = None,
    safesearch: str = "moderate",
    spellcheck: bool = True
) -> Dict[str, Any]:
    """
    Search for images using Brave Search.
    
    Args:
        query: Search query string
        count: Number of results (1-20, default: 10)
        offset: Pagination offset
        country: Country code for localized results
        search_lang: Language for search
        safesearch: Safe search level ("off", "moderate", "strict")
        spellcheck: Enable spell checking (default: True)
    
    Returns:
        Image results with URLs, thumbnails, dimensions, and source information
    """
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": offset,
        "safesearch": safesearch,
        "spellcheck": spellcheck
    }
    
    if country:
        params["country"] = country
    if search_lang:
        params["search_lang"] = search_lang
    
    result = await make_brave_request("images/search", params)
    return result


@mcp.tool()
async def video_search(
    query: str,
    count: int = 10,
    offset: int = 0,
    country: Optional[str] = None,
    search_lang: Optional[str] = None,
    safesearch: str = "moderate",
    spellcheck: bool = True
) -> Dict[str, Any]:
    """
    Search for videos using Brave Search.
    
    Args:
        query: Search query string
        count: Number of results (1-20, default: 10)
        offset: Pagination offset
        country: Country code for localized results
        search_lang: Language for search
        safesearch: Safe search level ("off", "moderate", "strict")
        spellcheck: Enable spell checking (default: True)
    
    Returns:
        Video results with URLs, thumbnails, duration, and source information
    """
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": offset,
        "safesearch": safesearch,
        "spellcheck": spellcheck
    }
    
    if country:
        params["country"] = country
    if search_lang:
        params["search_lang"] = search_lang
    
    result = await make_brave_request("videos/search", params)
    return result


@mcp.tool()
async def suggest(
    query: str,
    country: Optional[str] = None,
    search_lang: Optional[str] = None
) -> List[str]:
    """
    Get search suggestions/autocomplete for a query.
    
    Args:
        query: Partial search query
        country: Country code for localized suggestions
        search_lang: Language for suggestions
    
    Returns:
        List of suggested search queries
    """
    params = {
        "q": query
    }
    
    if country:
        params["country"] = country
    if search_lang:
        params["search_lang"] = search_lang
    
    result = await make_brave_request("suggest", params)
    return result.get("results", [])


@mcp.tool()
async def local_search(
    query: str,
    count: int = 10,
    offset: int = 0,
    country: Optional[str] = None,
    search_lang: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for local businesses and places.
    
    Args:
        query: Search query (e.g., "pizza near me", "hotels in San Francisco")
        count: Number of results (1-20, default: 10)
        offset: Pagination offset
        country: Country code for localized results
        search_lang: Language for search
    
    Returns:
        Local business results with addresses, ratings, hours, and contact info
    """
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": offset
    }
    
    if country:
        params["country"] = country
    if search_lang:
        params["search_lang"] = search_lang
    
    result = await make_brave_request("local/search", params)
    return result


@mcp.tool()
async def summarize_search(
    query: str,
    count: int = 5,
    entity_info: bool = True
) -> Dict[str, Any]:
    """
    Get AI-powered search summary with key information.
    
    Args:
        query: Search query
        count: Number of source results to use for summary (1-20, default: 5)
        entity_info: Include entity information (default: True)
    
    Returns:
        AI-generated summary with key facts and source citations
    """
    params = {
        "q": query,
        "count": min(count, 20),
        "summary": True,
        "entity_info": entity_info
    }
    
    result = await make_brave_request("web/search", params)
    
    # Extract summary and related info
    summary_data = {
        "summary": result.get("summarizer", {}).get("key", ""),
        "entities": result.get("entities", []) if entity_info else [],
        "infobox": result.get("infobox", {}),
        "sources": []
    }
    
    # Add source citations
    for item in result.get("web", {}).get("results", [])[:count]:
        summary_data["sources"].append({
            "title": item.get("title"),
            "url": item.get("url"),
            "description": item.get("description")
        })
    
    return summary_data