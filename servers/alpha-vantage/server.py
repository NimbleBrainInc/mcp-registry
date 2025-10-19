"""
Alpha Vantage MCP Server
Provides tools for accessing stock market data, forex, crypto, and technical indicators.
"""

import os
from typing import Optional
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Alpha Vantage MCP Server")

# Get API key from environment
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"


def get_base_params() -> dict:
    """Get base parameters for Alpha Vantage API requests."""
    if not ALPHAVANTAGE_API_KEY:
        raise ValueError("ALPHAVANTAGE_API_KEY environment variable is required")
    return {
        "apikey": ALPHAVANTAGE_API_KEY,
    }


@mcp.tool()
async def get_stock_quote(symbol: str) -> dict:
    """
    Get real-time stock quote with price, volume, and change data.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')

    Returns:
        Dictionary containing current price, volume, change, change percent, and trading times
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "GLOBAL_QUOTE"
        params["symbol"] = symbol

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_intraday_data(
    symbol: str,
    interval: str = "5min",
    outputsize: str = "compact"
) -> dict:
    """
    Get intraday time series data with specified intervals.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        interval: Time interval ('1min', '5min', '15min', '30min', '60min', default: '5min')
        outputsize: Data size ('compact' for last 100 points, 'full' for full history, default: 'compact')

    Returns:
        Dictionary containing intraday time series data with open, high, low, close, volume
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "TIME_SERIES_INTRADAY"
        params["symbol"] = symbol
        params["interval"] = interval
        params["outputsize"] = outputsize

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_daily_data(
    symbol: str,
    outputsize: str = "compact"
) -> dict:
    """
    Get daily time series data (open, high, low, close, volume).

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        outputsize: Data size ('compact' for last 100 days, 'full' for 20+ years, default: 'compact')

    Returns:
        Dictionary containing daily time series data
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "TIME_SERIES_DAILY"
        params["symbol"] = symbol
        params["outputsize"] = outputsize

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_weekly_data(symbol: str) -> dict:
    """
    Get weekly aggregated time series data.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        Dictionary containing weekly time series data (20+ years)
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "TIME_SERIES_WEEKLY"
        params["symbol"] = symbol

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_monthly_data(symbol: str) -> dict:
    """
    Get monthly aggregated time series data.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        Dictionary containing monthly time series data (20+ years)
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "TIME_SERIES_MONTHLY"
        params["symbol"] = symbol

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_symbol(keywords: str) -> dict:
    """
    Search for stock symbols by company name or keywords.

    Args:
        keywords: Search keywords (e.g., 'Apple', 'Microsoft', 'Tesla')

    Returns:
        Dictionary containing matching symbols with name, type, region, and currency
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "SYMBOL_SEARCH"
        params["keywords"] = keywords

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_technical_indicator(
    symbol: str,
    indicator: str,
    interval: str = "daily",
    time_period: int = 14,
    series_type: str = "close"
) -> dict:
    """
    Get technical indicator data (SMA, EMA, RSI, MACD, BBANDS, etc.).

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        indicator: Indicator type (e.g., 'SMA', 'EMA', 'RSI', 'MACD', 'BBANDS', 'ADX', 'CCI', 'AROON', 'STOCH')
        interval: Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly', default: 'daily')
        time_period: Number of data points for calculation (default: 14)
        series_type: Price type ('close', 'open', 'high', 'low', default: 'close')

    Returns:
        Dictionary containing technical indicator values over time
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = indicator.upper()
        params["symbol"] = symbol
        params["interval"] = interval
        params["time_period"] = time_period
        params["series_type"] = series_type

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_forex_rate(
    from_currency: str,
    to_currency: str
) -> dict:
    """
    Get real-time foreign exchange rate.

    Args:
        from_currency: Source currency code (e.g., 'USD', 'EUR', 'GBP', 'JPY')
        to_currency: Target currency code (e.g., 'USD', 'EUR', 'GBP', 'JPY')

    Returns:
        Dictionary containing exchange rate, bid/ask prices, and last update time
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "CURRENCY_EXCHANGE_RATE"
        params["from_currency"] = from_currency
        params["to_currency"] = to_currency

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_crypto_price(
    symbol: str,
    market: str = "USD"
) -> dict:
    """
    Get real-time cryptocurrency price.

    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH', 'LTC', 'XRP', 'DOGE')
        market: Market currency (e.g., 'USD', 'EUR', 'CNY', default: 'USD')

    Returns:
        Dictionary containing crypto price, volume, market cap, and change data
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "CURRENCY_EXCHANGE_RATE"
        params["from_currency"] = symbol
        params["to_currency"] = market

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_company_overview(symbol: str) -> dict:
    """
    Get fundamental data and company information.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        Dictionary containing company description, market cap, P/E ratio, dividends,
        52-week high/low, analyst ratings, and financial metrics
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "OVERVIEW"
        params["symbol"] = symbol

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_earnings(symbol: str) -> dict:
    """
    Get earnings reports and estimates.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        Dictionary containing quarterly and annual earnings, EPS, surprise percentage,
        and estimated vs actual earnings
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "EARNINGS"
        params["symbol"] = symbol

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_market_sentiment(
    tickers: str,
    topics: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    sort: str = "LATEST",
    limit: int = 50
) -> dict:
    """
    Get news sentiment analysis for stocks.

    Args:
        tickers: Comma-separated stock symbols (e.g., 'AAPL,MSFT,GOOGL')
        topics: Filter by topics (e.g., 'technology', 'finance', 'earnings', optional)
        time_from: Start time in YYYYMMDDTHHMM format (optional)
        time_to: End time in YYYYMMDDTHHMM format (optional)
        sort: Sort order ('LATEST', 'EARLIEST', 'RELEVANCE', default: 'LATEST')
        limit: Number of results (max: 1000, default: 50)

    Returns:
        Dictionary containing news articles with sentiment scores, relevance, and source
    """
    async with httpx.AsyncClient() as client:
        params = get_base_params()
        params["function"] = "NEWS_SENTIMENT"
        params["tickers"] = tickers
        params["sort"] = sort
        params["limit"] = limit

        if topics:
            params["topics"] = topics
        if time_from:
            params["time_from"] = time_from
        if time_to:
            params["time_to"] = time_to

        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
