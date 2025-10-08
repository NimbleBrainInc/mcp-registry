"""
OpenWeatherMap MCP Server
Provides tools for accessing weather data, forecasts, alerts, and air quality information.
"""

import os
from typing import Optional
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("OpenWeatherMap MCP Server")

# Get API key from environment
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
GEO_URL = "https://api.openweathermap.org/geo/1.0"


def get_params(units: str = "metric") -> dict:
    """Get base parameters for OpenWeatherMap API requests."""
    if not OPENWEATHERMAP_API_KEY:
        raise ValueError("OPENWEATHERMAP_API_KEY environment variable is required")
    return {
        "appid": OPENWEATHERMAP_API_KEY,
        "units": units,
    }


@mcp.tool()
async def get_current_weather(
    city: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    units: str = "metric"
) -> dict:
    """
    Get current weather conditions for a location.

    Args:
        city: City name (e.g., 'London', 'New York,US', 'Tokyo,JP')
        lat: Latitude coordinate (use with lon)
        lon: Longitude coordinate (use with lat)
        units: Units of measurement ('metric' for Celsius, 'imperial' for Fahrenheit, 'standard' for Kelvin)

    Returns:
        Dictionary containing current weather data including temperature, humidity, pressure, wind, clouds

    Note: Provide either city name OR coordinates (lat/lon), not both
    """
    async with httpx.AsyncClient() as client:
        params = get_params(units)

        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise ValueError("Must provide either city name or coordinates (lat/lon)")

        response = await client.get(
            f"{BASE_URL}/weather",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_forecast(
    city: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    units: str = "metric",
    cnt: Optional[int] = None
) -> dict:
    """
    Get 5-day weather forecast with 3-hour intervals (up to 40 data points).

    Args:
        city: City name (e.g., 'London', 'New York,US')
        lat: Latitude coordinate (use with lon)
        lon: Longitude coordinate (use with lat)
        units: Units of measurement ('metric', 'imperial', 'standard', default: 'metric')
        cnt: Number of timestamps to return (max: 40, optional)

    Returns:
        Dictionary containing 5-day forecast data with 3-hour intervals

    Note: Provide either city name OR coordinates (lat/lon), not both
    """
    async with httpx.AsyncClient() as client:
        params = get_params(units)

        if city:
            params["q"] = city
        elif lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise ValueError("Must provide either city name or coordinates (lat/lon)")

        if cnt:
            params["cnt"] = cnt

        response = await client.get(
            f"{BASE_URL}/forecast",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_hourly_forecast(
    lat: float,
    lon: float,
    units: str = "metric",
    cnt: Optional[int] = None
) -> dict:
    """
    Get hourly weather forecast for 48 hours (requires coordinates).

    Args:
        lat: Latitude coordinate (required)
        lon: Longitude coordinate (required)
        units: Units of measurement ('metric', 'imperial', 'standard', default: 'metric')
        cnt: Number of hours to return (max: 96, optional)

    Returns:
        Dictionary containing hourly forecast data for next 48 hours
    """
    async with httpx.AsyncClient() as client:
        params = get_params(units)
        params["lat"] = lat
        params["lon"] = lon

        if cnt:
            params["cnt"] = cnt

        response = await client.get(
            f"{BASE_URL}/forecast/hourly",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_weather_alerts(
    lat: float,
    lon: float
) -> dict:
    """
    Get severe weather alerts for a location.

    Args:
        lat: Latitude coordinate (required)
        lon: Longitude coordinate (required)

    Returns:
        Dictionary containing weather alerts and warnings for the location
    """
    async with httpx.AsyncClient() as client:
        params = {
            "appid": OPENWEATHERMAP_API_KEY,
            "lat": lat,
            "lon": lon,
        }

        response = await client.get(
            f"https://api.openweathermap.org/data/3.0/onecall",
            params=params,
        )
        response.raise_for_status()
        data = response.json()

        # Extract alerts if available
        return {
            "lat": lat,
            "lon": lon,
            "alerts": data.get("alerts", []),
            "timezone": data.get("timezone", ""),
        }


@mcp.tool()
async def get_air_quality(
    lat: float,
    lon: float
) -> dict:
    """
    Get air quality index and pollutant data for a location.

    Args:
        lat: Latitude coordinate (required)
        lon: Longitude coordinate (required)

    Returns:
        Dictionary containing air quality index (AQI) and pollutant concentrations
        (CO, NO, NO2, O3, SO2, PM2.5, PM10, NH3)
    """
    async with httpx.AsyncClient() as client:
        params = {
            "appid": OPENWEATHERMAP_API_KEY,
            "lat": lat,
            "lon": lon,
        }

        response = await client.get(
            f"{BASE_URL}/air_pollution",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_weather_by_zip(
    zip_code: str,
    country_code: Optional[str] = None,
    units: str = "metric"
) -> dict:
    """
    Get current weather by ZIP/postal code.

    Args:
        zip_code: ZIP or postal code
        country_code: 2-letter country code (optional, e.g., 'US', 'GB', 'CA')
        units: Units of measurement ('metric', 'imperial', 'standard', default: 'metric')

    Returns:
        Dictionary containing current weather data for the ZIP code location
    """
    async with httpx.AsyncClient() as client:
        params = get_params(units)

        if country_code:
            params["zip"] = f"{zip_code},{country_code}"
        else:
            params["zip"] = zip_code

        response = await client.get(
            f"{BASE_URL}/weather",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_city(
    city_name: str,
    limit: int = 5
) -> dict:
    """
    Search for cities by name and get their coordinates.

    Args:
        city_name: City name to search for
        limit: Number of results to return (max: 5, default: 5)

    Returns:
        List of cities matching the search with name, country, state, and coordinates
    """
    async with httpx.AsyncClient() as client:
        params = {
            "appid": OPENWEATHERMAP_API_KEY,
            "q": city_name,
            "limit": limit,
        }

        response = await client.get(
            f"{GEO_URL}/direct",
            params=params,
        )
        response.raise_for_status()
        return {"results": response.json()}


@mcp.tool()
async def get_historical_weather(
    lat: float,
    lon: float,
    dt: int,
    units: str = "metric"
) -> dict:
    """
    Get historical weather data for a specific date (last 5 days).

    Args:
        lat: Latitude coordinate (required)
        lon: Longitude coordinate (required)
        dt: Unix timestamp (UTC) for the historical date
        units: Units of measurement ('metric', 'imperial', 'standard', default: 'metric')

    Returns:
        Dictionary containing historical weather data for the specified date
    """
    async with httpx.AsyncClient() as client:
        params = get_params(units)
        params["lat"] = lat
        params["lon"] = lon
        params["dt"] = dt

        response = await client.get(
            f"https://api.openweathermap.org/data/3.0/onecall/timemachine",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_uv_index(
    lat: float,
    lon: float
) -> dict:
    """
    Get UV index for a location.

    Args:
        lat: Latitude coordinate (required)
        lon: Longitude coordinate (required)

    Returns:
        Dictionary containing UV index and related data
    """
    async with httpx.AsyncClient() as client:
        params = {
            "appid": OPENWEATHERMAP_API_KEY,
            "lat": lat,
            "lon": lon,
        }

        response = await client.get(
            f"{BASE_URL}/uvi",
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_weather_map(
    layer: str,
    z: int,
    x: int,
    y: int
) -> dict:
    """
    Get weather map layer tile data (for visualizations).

    Args:
        layer: Map layer type ('temp_new', 'precipitation_new', 'clouds_new', 'pressure_new', 'wind_new')
        z: Zoom level (0-15)
        x: Tile X coordinate
        y: Tile Y coordinate

    Returns:
        Dictionary containing map tile information and URL
    """
    tile_url = f"https://tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid={OPENWEATHERMAP_API_KEY}"

    return {
        "layer": layer,
        "zoom": z,
        "x": x,
        "y": y,
        "tile_url": tile_url,
        "info": "Use this URL to fetch the weather map tile image"
    }


if __name__ == "__main__":
    mcp.run()
