"""
CoinGecko MCP Server
Provides tools for accessing cryptocurrency market data, prices, and trends.
"""

import os
from typing import Optional, List
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("CoinGecko MCP Server")

# Get API key from environment
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3"


def get_headers() -> dict:
    """Get headers for CoinGecko API requests."""
    if not COINGECKO_API_KEY:
        raise ValueError("COINGECKO_API_KEY environment variable is required")

    # CoinGecko uses different header names depending on plan
    # Try to detect plan level from key or use demo header
    return {
        "X-CG-DEMO-API-KEY": COINGECKO_API_KEY,
    }


@mcp.tool()
async def get_coin_price(
    ids: str,
    vs_currencies: str = "usd",
    include_market_cap: bool = False,
    include_24hr_vol: bool = False,
    include_24hr_change: bool = False,
    include_last_updated_at: bool = False
) -> dict:
    """
    Get current price of coins in multiple currencies.

    Args:
        ids: Comma-separated coin IDs (e.g., 'bitcoin,ethereum,cardano')
        vs_currencies: Comma-separated target currencies (e.g., 'usd,eur,btc', default: 'usd')
        include_market_cap: Include market cap (default: False)
        include_24hr_vol: Include 24h trading volume (default: False)
        include_24hr_change: Include 24h price change (default: False)
        include_last_updated_at: Include last updated timestamp (default: False)

    Returns:
        Dictionary with coin prices and optional market data
    """
    async with httpx.AsyncClient() as client:
        params = {
            "ids": ids,
            "vs_currencies": vs_currencies,
            "include_market_cap": str(include_market_cap).lower(),
            "include_24hr_vol": str(include_24hr_vol).lower(),
            "include_24hr_change": str(include_24hr_change).lower(),
            "include_last_updated_at": str(include_last_updated_at).lower(),
        }

        response = await client.get(
            f"{BASE_URL}/simple/price",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_coin_details(
    coin_id: str,
    localization: bool = False,
    tickers: bool = False,
    market_data: bool = True,
    community_data: bool = False,
    developer_data: bool = False,
    sparkline: bool = False
) -> dict:
    """
    Get detailed information for a coin.

    Args:
        coin_id: Coin ID (e.g., 'bitcoin', 'ethereum')
        localization: Include localized languages (default: False)
        tickers: Include ticker data (default: False)
        market_data: Include market data (price, volume, market cap, etc., default: True)
        community_data: Include community stats (default: False)
        developer_data: Include developer stats (default: False)
        sparkline: Include 7-day price sparkline (default: False)

    Returns:
        Dictionary with comprehensive coin information
    """
    async with httpx.AsyncClient() as client:
        params = {
            "localization": str(localization).lower(),
            "tickers": str(tickers).lower(),
            "market_data": str(market_data).lower(),
            "community_data": str(community_data).lower(),
            "developer_data": str(developer_data).lower(),
            "sparkline": str(sparkline).lower(),
        }

        response = await client.get(
            f"{BASE_URL}/coins/{coin_id}",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_coin_market_chart(
    coin_id: str,
    vs_currency: str = "usd",
    days: str = "7",
    interval: Optional[str] = None
) -> dict:
    """
    Get historical price data for a coin.

    Args:
        coin_id: Coin ID (e.g., 'bitcoin', 'ethereum')
        vs_currency: Target currency (e.g., 'usd', 'eur', 'btc', default: 'usd')
        days: Time range ('1', '7', '14', '30', '90', '180', '365', 'max', default: '7')
        interval: Data interval ('daily' for 90+ days, optional, auto-selected if not specified)

    Returns:
        Dictionary with price, market cap, and volume data over time
    """
    async with httpx.AsyncClient() as client:
        params = {
            "vs_currency": vs_currency,
            "days": days,
        }
        if interval:
            params["interval"] = interval

        response = await client.get(
            f"{BASE_URL}/coins/{coin_id}/market_chart",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_coins(query: str) -> dict:
    """
    Search for coins by name or symbol.

    Args:
        query: Search query (coin name or symbol)

    Returns:
        Dictionary with matching coins, exchanges, and categories
    """
    async with httpx.AsyncClient() as client:
        params = {"query": query}

        response = await client.get(
            f"{BASE_URL}/search",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_trending_coins() -> dict:
    """
    Get trending coins in the last 24 hours.

    Returns:
        Dictionary with trending coins and NFTs
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/search/trending",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_top_coins(
    vs_currency: str = "usd",
    order: str = "market_cap_desc",
    per_page: int = 100,
    page: int = 1,
    sparkline: bool = False,
    price_change_percentage: Optional[str] = None
) -> dict:
    """
    Get top coins by market cap with market data.

    Args:
        vs_currency: Target currency (default: 'usd')
        order: Sort order ('market_cap_desc', 'volume_desc', 'id_asc', 'id_desc', default: 'market_cap_desc')
        per_page: Results per page (1-250, default: 100)
        page: Page number (default: 1)
        sparkline: Include 7-day sparkline (default: False)
        price_change_percentage: Price change timeframes ('1h,24h,7d', optional)

    Returns:
        List of coins with market data
    """
    async with httpx.AsyncClient() as client:
        params = {
            "vs_currency": vs_currency,
            "order": order,
            "per_page": per_page,
            "page": page,
            "sparkline": str(sparkline).lower(),
        }
        if price_change_percentage:
            params["price_change_percentage"] = price_change_percentage

        response = await client.get(
            f"{BASE_URL}/coins/markets",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_supported_coins(include_platform: bool = False) -> dict:
    """
    List all supported coins with IDs and symbols.

    Args:
        include_platform: Include platform contract addresses (default: False)

    Returns:
        List of all coins with IDs, symbols, and names
    """
    async with httpx.AsyncClient() as client:
        params = {
            "include_platform": str(include_platform).lower(),
        }

        response = await client.get(
            f"{BASE_URL}/coins/list",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_global_market_data() -> dict:
    """
    Get global cryptocurrency market statistics.

    Returns:
        Dictionary with total market cap, volume, BTC dominance, and market cap change
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/global",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_exchange_info(
    exchange_id: str
) -> dict:
    """
    Get detailed information about a specific exchange.

    Args:
        exchange_id: Exchange ID (e.g., 'binance', 'coinbase_exchange', 'kraken')

    Returns:
        Dictionary with exchange details, volume, trust score, and tickers
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/exchanges/{exchange_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_exchanges(
    per_page: int = 100,
    page: int = 1
) -> dict:
    """
    List all exchanges with volume rankings.

    Args:
        per_page: Results per page (1-250, default: 100)
        page: Page number (default: 1)

    Returns:
        List of exchanges with volume, trust score, and rankings
    """
    async with httpx.AsyncClient() as client:
        params = {
            "per_page": per_page,
            "page": page,
        }

        response = await client.get(
            f"{BASE_URL}/exchanges",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_coin_categories(order: str = "market_cap_desc") -> dict:
    """
    Get coin categories with market data.

    Args:
        order: Sort order ('market_cap_desc', 'market_cap_asc', 'name_desc', 'name_asc',
               'market_cap_change_24h_desc', 'market_cap_change_24h_asc', default: 'market_cap_desc')

    Returns:
        List of categories (DeFi, NFT, Gaming, etc.) with market stats
    """
    async with httpx.AsyncClient() as client:
        params = {"order": order}

        response = await client.get(
            f"{BASE_URL}/coins/categories",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_nft_data(nft_id: str) -> dict:
    """
    Get NFT collection data including floor price and volume.

    Args:
        nft_id: NFT collection ID (e.g., 'bored-ape-yacht-club', 'cryptopunks')

    Returns:
        Dictionary with NFT floor price, volume, market cap, and holders
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/nfts/{nft_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
