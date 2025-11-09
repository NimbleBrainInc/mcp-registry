"""
News API MCP Server
Provides tools for accessing news articles, headlines, and sources from News API.
"""

import os
from typing import Optional
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("News API MCP Server")

# Get API key from environment
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"


def get_headers():
    """Get headers for News API requests."""
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY environment variable is required")
    return {
        "X-Api-Key": NEWS_API_KEY,
    }


@mcp.tool()
async def search_everything(
    q: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    sources: Optional[str] = None,
    domains: Optional[str] = None,
    language: Optional[str] = None,
    sort_by: str = "publishedAt",
    page_size: int = 20,
    page: int = 1
) -> dict:
    """
    Search through all articles with advanced filtering.

    Args:
        q: Keywords or phrases to search for (required)
        from_date: Oldest date to retrieve articles from (ISO 8601 format: YYYY-MM-DD)
        to_date: Newest date to retrieve articles to (ISO 8601 format: YYYY-MM-DD)
        sources: Comma-separated list of news source identifiers (e.g., 'bbc-news,cnn')
        domains: Comma-separated list of domains (e.g., 'bbc.co.uk,techcrunch.com')
        language: Language code (e.g., 'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ar', 'zh')
        sort_by: Sort order ('relevancy', 'popularity', 'publishedAt', default: 'publishedAt')
        page_size: Number of results to return (max: 100, default: 20)
        page: Page number (default: 1)

    Returns:
        Dictionary containing articles, total results, and status
    """
    async with httpx.AsyncClient() as client:
        params = {
            "q": q,
            "sortBy": sort_by,
            "pageSize": min(page_size, 100),
            "page": page,
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if sources:
            params["sources"] = sources
        if domains:
            params["domains"] = domains
        if language:
            params["language"] = language

        response = await client.get(
            f"{BASE_URL}/everything",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_top_headlines(
    country: Optional[str] = None,
    category: Optional[str] = None,
    sources: Optional[str] = None,
    q: Optional[str] = None,
    page_size: int = 20,
    page: int = 1
) -> dict:
    """
    Get breaking and top headlines.

    Args:
        country: 2-letter ISO country code (e.g., 'us', 'gb', 'ca', 'au', 'de', 'fr')
        category: Category ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
        sources: Comma-separated list of news source identifiers
        q: Keywords or phrases to search for (optional)
        page_size: Number of results to return (max: 100, default: 20)
        page: Page number (default: 1)

    Returns:
        Dictionary containing top headlines, total results, and status

    Note: Cannot mix 'sources' with 'country' or 'category' parameters
    """
    async with httpx.AsyncClient() as client:
        params = {
            "pageSize": min(page_size, 100),
            "page": page,
        }
        if country:
            params["country"] = country
        if category:
            params["category"] = category
        if sources:
            params["sources"] = sources
        if q:
            params["q"] = q

        response = await client.get(
            f"{BASE_URL}/top-headlines",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_by_source(
    sources: str,
    q: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    sort_by: str = "publishedAt",
    page_size: int = 20,
    page: int = 1
) -> dict:
    """
    Search articles from specific news sources.

    Args:
        sources: Comma-separated list of source IDs (e.g., 'bbc-news,cnn,techcrunch')
        q: Keywords or phrases to search for (optional)
        from_date: Oldest date to retrieve articles from (ISO 8601: YYYY-MM-DD)
        to_date: Newest date to retrieve articles to (ISO 8601: YYYY-MM-DD)
        sort_by: Sort order ('relevancy', 'popularity', 'publishedAt', default: 'publishedAt')
        page_size: Number of results to return (max: 100, default: 20)
        page: Page number (default: 1)

    Returns:
        Dictionary containing articles from specified sources
    """
    async with httpx.AsyncClient() as client:
        params = {
            "sources": sources,
            "sortBy": sort_by,
            "pageSize": min(page_size, 100),
            "page": page,
        }
        if q:
            params["q"] = q
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = await client.get(
            f"{BASE_URL}/everything",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_sources(
    category: Optional[str] = None,
    language: Optional[str] = None,
    country: Optional[str] = None
) -> dict:
    """
    Get all available news sources with optional filters.

    Args:
        category: Filter by category ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
        language: Filter by language code (e.g., 'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ar', 'zh')
        country: Filter by 2-letter ISO country code (e.g., 'us', 'gb', 'ca', 'au')

    Returns:
        Dictionary containing list of available news sources
    """
    async with httpx.AsyncClient() as client:
        params = {}
        if category:
            params["category"] = category
        if language:
            params["language"] = language
        if country:
            params["country"] = country

        response = await client.get(
            f"{BASE_URL}/top-headlines/sources",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_by_category(
    category: str,
    country: Optional[str] = None,
    q: Optional[str] = None,
    page_size: int = 20,
    page: int = 1
) -> dict:
    """
    Get news articles by category.

    Args:
        category: News category (required: 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
        country: 2-letter ISO country code (e.g., 'us', 'gb', 'ca', 'au')
        q: Keywords or phrases to search for (optional)
        page_size: Number of results to return (max: 100, default: 20)
        page: Page number (default: 1)

    Returns:
        Dictionary containing articles in the specified category
    """
    async with httpx.AsyncClient() as client:
        params = {
            "category": category,
            "pageSize": min(page_size, 100),
            "page": page,
        }
        if country:
            params["country"] = country
        if q:
            params["q"] = q

        response = await client.get(
            f"{BASE_URL}/top-headlines",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_by_country(
    country: str,
    category: Optional[str] = None,
    q: Optional[str] = None,
    page_size: int = 20,
    page: int = 1
) -> dict:
    """
    Get news articles by country.

    Args:
        country: 2-letter ISO country code (required: 'us', 'gb', 'ca', 'au', 'de', 'fr', 'in', 'jp', etc.)
        category: News category ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
        q: Keywords or phrases to search for (optional)
        page_size: Number of results to return (max: 100, default: 20)
        page: Page number (default: 1)

    Returns:
        Dictionary containing articles from the specified country
    """
    async with httpx.AsyncClient() as client:
        params = {
            "country": country,
            "pageSize": min(page_size, 100),
            "page": page,
        }
        if category:
            params["category"] = category
        if q:
            params["q"] = q

        response = await client.get(
            f"{BASE_URL}/top-headlines",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_by_language(
    language: str,
    q: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    sort_by: str = "publishedAt",
    page_size: int = 20,
    page: int = 1
) -> dict:
    """
    Get news articles in a specific language.

    Args:
        language: 2-letter ISO language code (required: 'ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh')
        q: Keywords or phrases to search for (required)
        from_date: Oldest date to retrieve articles from (ISO 8601: YYYY-MM-DD)
        to_date: Newest date to retrieve articles to (ISO 8601: YYYY-MM-DD)
        sort_by: Sort order ('relevancy', 'popularity', 'publishedAt', default: 'publishedAt')
        page_size: Number of results to return (max: 100, default: 20)
        page: Page number (default: 1)

    Returns:
        Dictionary containing articles in the specified language
    """
    async with httpx.AsyncClient() as client:
        params = {
            "language": language,
            "q": q,
            "sortBy": sort_by,
            "pageSize": min(page_size, 100),
            "page": page,
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = await client.get(
            f"{BASE_URL}/everything",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_trending_topics(
    country: str = "us",
    category: str = "general",
    page_size: int = 20
) -> dict:
    """
    Get currently trending news topics and headlines.

    Args:
        country: 2-letter ISO country code (default: 'us')
        category: News category (default: 'general')
        page_size: Number of results to return (max: 100, default: 20)

    Returns:
        Dictionary containing trending headlines and topics
    """
    async with httpx.AsyncClient() as client:
        params = {
            "country": country,
            "category": category,
            "pageSize": min(page_size, 100),
        }

        response = await client.get(
            f"{BASE_URL}/top-headlines",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
