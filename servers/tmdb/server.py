import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("TMDB")

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def get_url(endpoint: str, **params) -> str:
    """Build URL with API key and parameters."""
    params["api_key"] = API_KEY
    param_str = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
    return f"{BASE_URL}/{endpoint}?{param_str}"


@mcp.tool()
async def search_movies(
    query: str,
    language: str = "en-US",
    page: int = 1,
    include_adult: bool = False,
    year: Optional[int] = None
) -> dict:
    """Search for movies by title.

    Args:
        query: Movie title to search for
        language: Language code (default: en-US)
        page: Page number for pagination
        include_adult: Include adult content
        year: Filter by release year
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                "search/movie",
                query=query,
                language=language,
                page=page,
                include_adult=include_adult,
                year=year
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_tv_shows(
    query: str,
    language: str = "en-US",
    page: int = 1,
    include_adult: bool = False,
    first_air_date_year: Optional[int] = None
) -> dict:
    """Search for TV shows by title.

    Args:
        query: TV show title to search for
        language: Language code (default: en-US)
        page: Page number for pagination
        include_adult: Include adult content
        first_air_date_year: Filter by first air date year
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                "search/tv",
                query=query,
                language=language,
                page=page,
                include_adult=include_adult,
                first_air_date_year=first_air_date_year
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_people(
    query: str,
    language: str = "en-US",
    page: int = 1,
    include_adult: bool = False
) -> dict:
    """Search for actors, directors, and crew members.

    Args:
        query: Person name to search for
        language: Language code (default: en-US)
        page: Page number for pagination
        include_adult: Include adult content
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                "search/person",
                query=query,
                language=language,
                page=page,
                include_adult=include_adult
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_movie_details(
    movie_id: int,
    language: str = "en-US",
    append_to_response: Optional[str] = None
) -> dict:
    """Get detailed movie information including runtime, budget, revenue, ratings, and more.

    Args:
        movie_id: TMDB movie ID
        language: Language code (default: en-US)
        append_to_response: Comma-separated list of additional data (credits, videos, images, etc.)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"movie/{movie_id}",
                language=language,
                append_to_response=append_to_response
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_tv_details(
    tv_id: int,
    language: str = "en-US",
    append_to_response: Optional[str] = None
) -> dict:
    """Get TV show details including seasons, episodes, networks, and more.

    Args:
        tv_id: TMDB TV show ID
        language: Language code (default: en-US)
        append_to_response: Comma-separated list of additional data (credits, videos, images, etc.)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"tv/{tv_id}",
                language=language,
                append_to_response=append_to_response
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_person_details(
    person_id: int,
    language: str = "en-US",
    append_to_response: Optional[str] = None
) -> dict:
    """Get person biography, filmography, and credits.

    Args:
        person_id: TMDB person ID
        language: Language code (default: en-US)
        append_to_response: Comma-separated list of additional data (movie_credits, tv_credits, images, etc.)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"person/{person_id}",
                language=language,
                append_to_response=append_to_response
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_trending(
    media_type: str = "movie",
    time_window: str = "day",
    language: str = "en-US",
    page: int = 1
) -> dict:
    """Get trending movies or TV shows.

    Args:
        media_type: Type of media (movie, tv, or all)
        time_window: Time window for trending (day or week)
        language: Language code (default: en-US)
        page: Page number for pagination
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"trending/{media_type}/{time_window}",
                language=language,
                page=page
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_popular(
    media_type: str = "movie",
    language: str = "en-US",
    page: int = 1,
    region: Optional[str] = None
) -> dict:
    """Get popular movies or TV shows.

    Args:
        media_type: Type of media (movie or tv)
        language: Language code (default: en-US)
        page: Page number for pagination
        region: ISO 3166-1 code for region filtering
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"{media_type}/popular",
                language=language,
                page=page,
                region=region
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_top_rated(
    media_type: str = "movie",
    language: str = "en-US",
    page: int = 1,
    region: Optional[str] = None
) -> dict:
    """Get top rated movies or TV shows.

    Args:
        media_type: Type of media (movie or tv)
        language: Language code (default: en-US)
        page: Page number for pagination
        region: ISO 3166-1 code for region filtering
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"{media_type}/top_rated",
                language=language,
                page=page,
                region=region
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def discover_movies(
    language: str = "en-US",
    page: int = 1,
    sort_by: str = "popularity.desc",
    with_genres: Optional[str] = None,
    year: Optional[int] = None,
    primary_release_year: Optional[int] = None,
    vote_average_gte: Optional[float] = None,
    vote_average_lte: Optional[float] = None,
    with_runtime_gte: Optional[int] = None,
    with_runtime_lte: Optional[int] = None,
    region: Optional[str] = None
) -> dict:
    """Discover movies with filters for genre, year, rating, and more.

    Args:
        language: Language code (default: en-US)
        page: Page number for pagination
        sort_by: Sort results (popularity.desc, vote_average.desc, release_date.desc, revenue.desc, etc.)
        with_genres: Comma-separated genre IDs
        year: Filter by release year
        primary_release_year: Filter by primary release year
        vote_average_gte: Minimum rating (0-10)
        vote_average_lte: Maximum rating (0-10)
        with_runtime_gte: Minimum runtime in minutes
        with_runtime_lte: Maximum runtime in minutes
        region: ISO 3166-1 code for region filtering
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                "discover/movie",
                language=language,
                page=page,
                sort_by=sort_by,
                with_genres=with_genres,
                year=year,
                primary_release_year=primary_release_year,
                **{
                    "vote_average.gte": vote_average_gte,
                    "vote_average.lte": vote_average_lte,
                    "with_runtime.gte": with_runtime_gte,
                    "with_runtime.lte": with_runtime_lte,
                    "region": region
                }
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def discover_tv(
    language: str = "en-US",
    page: int = 1,
    sort_by: str = "popularity.desc",
    with_genres: Optional[str] = None,
    first_air_date_year: Optional[int] = None,
    vote_average_gte: Optional[float] = None,
    vote_average_lte: Optional[float] = None,
    with_runtime_gte: Optional[int] = None,
    with_runtime_lte: Optional[int] = None,
    with_networks: Optional[str] = None
) -> dict:
    """Discover TV shows with filters for genre, year, rating, and more.

    Args:
        language: Language code (default: en-US)
        page: Page number for pagination
        sort_by: Sort results (popularity.desc, vote_average.desc, first_air_date.desc, etc.)
        with_genres: Comma-separated genre IDs
        first_air_date_year: Filter by first air date year
        vote_average_gte: Minimum rating (0-10)
        vote_average_lte: Maximum rating (0-10)
        with_runtime_gte: Minimum runtime in minutes
        with_runtime_lte: Maximum runtime in minutes
        with_networks: Comma-separated network IDs
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                "discover/tv",
                language=language,
                page=page,
                sort_by=sort_by,
                with_genres=with_genres,
                first_air_date_year=first_air_date_year,
                with_networks=with_networks,
                **{
                    "vote_average.gte": vote_average_gte,
                    "vote_average.lte": vote_average_lte,
                    "with_runtime.gte": with_runtime_gte,
                    "with_runtime.lte": with_runtime_lte
                }
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_genres(
    media_type: str = "movie",
    language: str = "en-US"
) -> dict:
    """Get list of all genres for movies or TV shows.

    Args:
        media_type: Type of media (movie or tv)
        language: Language code (default: en-US)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"genre/{media_type}/list",
                language=language
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_movie_credits(
    movie_id: int,
    language: str = "en-US"
) -> dict:
    """Get cast and crew for a movie.

    Args:
        movie_id: TMDB movie ID
        language: Language code (default: en-US)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"movie/{movie_id}/credits",
                language=language
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_tv_credits(
    tv_id: int,
    language: str = "en-US"
) -> dict:
    """Get cast and crew for a TV show.

    Args:
        tv_id: TMDB TV show ID
        language: Language code (default: en-US)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"tv/{tv_id}/credits",
                language=language
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_recommendations(
    media_type: str,
    media_id: int,
    language: str = "en-US",
    page: int = 1
) -> dict:
    """Get similar movies or TV shows based on a title.

    Args:
        media_type: Type of media (movie or tv)
        media_id: TMDB media ID
        language: Language code (default: en-US)
        page: Page number for pagination
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(
                f"{media_type}/{media_id}/recommendations",
                language=language,
                page=page
            )
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_streaming_providers(
    media_type: str,
    media_id: int
) -> dict:
    """Get streaming availability for a movie or TV show by region.

    Args:
        media_type: Type of media (movie or tv)
        media_id: TMDB media ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url(f"{media_type}/{media_id}/watch/providers")
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
