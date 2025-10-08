import os
from typing import Optional, List
import httpx
from fastmcp import FastMCP

mcp = FastMCP("AbstractAPI")

API_KEY = os.getenv("ABSTRACT_API_KEY")


@mcp.tool()
async def validate_email(email: str) -> dict:
    """Validate email address and check deliverability.

    Args:
        email: Email address to validate
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://emailvalidation.abstractapi.com/v1/",
            params={"api_key": API_KEY, "email": email}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def validate_phone(
    phone: str,
    country_code: Optional[str] = None
) -> dict:
    """Validate phone number and get carrier info.

    Args:
        phone: Phone number to validate
        country_code: ISO 3166-1 alpha-2 country code (optional)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"api_key": API_KEY, "phone": phone}
        if country_code:
            params["country_code"] = country_code

        response = await client.get(
            "https://phonevalidation.abstractapi.com/v1/",
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def validate_vat(vat_number: str) -> dict:
    """Validate EU VAT numbers.

    Args:
        vat_number: VAT number to validate (e.g., "SE556656688001")
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://vatapi.abstractapi.com/v1/",
            params={"api_key": API_KEY, "vat_number": vat_number}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def geolocate_ip(
    ip_address: str,
    fields: Optional[str] = None
) -> dict:
    """Get location data from IP address.

    Args:
        ip_address: IP address to geolocate
        fields: Comma-separated fields to return (e.g., "city,country,timezone")
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"api_key": API_KEY, "ip_address": ip_address}
        if fields:
            params["fields"] = fields

        response = await client.get(
            "https://ipgeolocation.abstractapi.com/v1/",
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_ip_info(ip_address: str) -> dict:
    """Get detailed IP information (ISP, ASN, etc.).

    Args:
        ip_address: IP address to query
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://ipgeolocation.abstractapi.com/v1/",
            params={"api_key": API_KEY, "ip_address": ip_address}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def check_vpn(ip_address: str) -> dict:
    """Detect if IP is from VPN/proxy/datacenter.

    Args:
        ip_address: IP address to check
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://ipgeolocation.abstractapi.com/v1/",
            params={
                "api_key": API_KEY,
                "ip_address": ip_address,
                "fields": "security"
            }
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_timezone(
    location: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
) -> dict:
    """Get timezone from location or coordinates.

    Args:
        location: Location name (e.g., "New York")
        latitude: Latitude coordinate
        longitude: Longitude coordinate
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"api_key": API_KEY}

        if location:
            params["location"] = location
        elif latitude is not None and longitude is not None:
            params["latitude"] = latitude
            params["longitude"] = longitude
        else:
            raise ValueError("Either location or latitude/longitude must be provided")

        response = await client.get(
            "https://timezone.abstractapi.com/v1/current_time/",
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def convert_timezone(
    base_location: str,
    base_datetime: str,
    target_location: str
) -> dict:
    """Convert time between timezones.

    Args:
        base_location: Source location/timezone
        base_datetime: Datetime in ISO 8601 format
        target_location: Target location/timezone
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://timezone.abstractapi.com/v1/convert_time/",
            params={
                "api_key": API_KEY,
                "base_location": base_location,
                "base_datetime": base_datetime,
                "target_location": target_location
            }
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_holidays(
    country: str,
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None
) -> dict:
    """Get public holidays for a country and year.

    Args:
        country: ISO 3166-1 alpha-2 country code (e.g., "US")
        year: Year (e.g., 2025)
        month: Month (1-12, optional)
        day: Day (1-31, optional)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {
            "api_key": API_KEY,
            "country": country,
            "year": year
        }
        if month:
            params["month"] = month
        if day:
            params["day"] = day

        response = await client.get(
            "https://holidays.abstractapi.com/v1/",
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_exchange_rates(
    base: str = "USD",
    target: Optional[str] = None
) -> dict:
    """Get current currency exchange rates.

    Args:
        base: Base currency code (e.g., "USD")
        target: Target currency code (optional, returns all if not specified)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"api_key": API_KEY, "base": base}
        if target:
            params["target"] = target

        response = await client.get(
            "https://exchange-rates.abstractapi.com/v1/live/",
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def convert_currency(
    base: str,
    target: str,
    amount: float,
    date: Optional[str] = None
) -> dict:
    """Convert amount between currencies.

    Args:
        base: Base currency code (e.g., "USD")
        target: Target currency code (e.g., "EUR")
        amount: Amount to convert
        date: Historical date in YYYY-MM-DD format (optional)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {
            "api_key": API_KEY,
            "base": base,
            "target": target
        }

        endpoint = "live" if not date else "historical"
        if date:
            params["date"] = date

        response = await client.get(
            f"https://exchange-rates.abstractapi.com/v1/{endpoint}/",
            params=params
        )
        response.raise_for_status()

        result = response.json()
        if "exchange_rates" in result and target in result["exchange_rates"]:
            rate = result["exchange_rates"][target]
            result["converted_amount"] = amount * rate
            result["amount"] = amount

        return result


@mcp.tool()
async def get_company_info(domain: str) -> dict:
    """Get company data from domain name.

    Args:
        domain: Company domain (e.g., "google.com")
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://companyenrichment.abstractapi.com/v1/",
            params={"api_key": API_KEY, "domain": domain}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def scrape_url(
    url: str,
    render_js: bool = False
) -> dict:
    """Extract structured data from web pages.

    Args:
        url: URL to scrape
        render_js: Render JavaScript (default: false)
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            "https://scrape.abstractapi.com/v1/",
            params={
                "api_key": API_KEY,
                "url": url,
                "render_js": str(render_js).lower()
            }
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def generate_screenshot(
    url: str,
    width: int = 1920,
    height: int = 1080,
    full_page: bool = False
) -> dict:
    """Generate website screenshot.

    Args:
        url: URL to screenshot
        width: Screenshot width in pixels (default: 1920)
        height: Screenshot height in pixels (default: 1080)
        full_page: Capture full page (default: false)
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            "https://screenshot.abstractapi.com/v1/",
            params={
                "api_key": API_KEY,
                "url": url,
                "width": width,
                "height": height,
                "full_page": str(full_page).lower()
            }
        )
        response.raise_for_status()

        # Screenshot API returns image data
        return {
            "success": True,
            "url": url,
            "image_data": response.content.hex()[:100] + "...",  # First 100 chars
            "content_type": response.headers.get("content-type"),
            "note": "Full image data available in response"
        }


if __name__ == "__main__":
    mcp.run()
