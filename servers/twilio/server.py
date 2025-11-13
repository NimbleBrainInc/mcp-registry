"""
Twilio MCP Server
Provides tools for interacting with the Twilio communication API.
"""

import os
from typing import Optional
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Twilio MCP Server")

# Get API credentials from environment
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
BASE_URL = "https://api.twilio.com/2010-04-01"


def get_auth():
    """Get HTTP Basic Auth credentials for Twilio API."""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        raise ValueError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables are required")
    return (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@mcp.tool()
async def send_sms(to: str, from_: str, body: str, media_url: Optional[str] = None) -> dict:
    """
    Send an SMS message via Twilio.

    Args:
        to: Recipient phone number in E.164 format (e.g., +1234567890)
        from_: Your Twilio phone number in E.164 format
        body: Message content (up to 1600 characters)
        media_url: Optional URL of media to send (MMS)

    Returns:
        Dictionary containing message details including SID and status
    """
    async with httpx.AsyncClient() as client:
        data = {
            "To": to,
            "From": from_,
            "Body": body,
        }
        if media_url:
            data["MediaUrl"] = media_url

        response = await client.post(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
            auth=get_auth(),
            data=data,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def send_whatsapp(to: str, from_: str, body: str, media_url: Optional[str] = None) -> dict:
    """
    Send a WhatsApp message via Twilio.

    Args:
        to: Recipient WhatsApp number in E.164 format with 'whatsapp:' prefix (e.g., whatsapp:+1234567890)
        from_: Your Twilio WhatsApp number with 'whatsapp:' prefix
        body: Message content
        media_url: Optional URL of media to send

    Returns:
        Dictionary containing message details including SID and status
    """
    async with httpx.AsyncClient() as client:
        # Ensure whatsapp: prefix
        if not to.startswith("whatsapp:"):
            to = f"whatsapp:{to}"
        if not from_.startswith("whatsapp:"):
            from_ = f"whatsapp:{from_}"

        data = {
            "To": to,
            "From": from_,
            "Body": body,
        }
        if media_url:
            data["MediaUrl"] = media_url

        response = await client.post(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
            auth=get_auth(),
            data=data,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_messages(to: Optional[str] = None, from_: Optional[str] = None, date_sent: Optional[str] = None, page_size: int = 50) -> dict:
    """
    List sent and received messages.

    Args:
        to: Filter by recipient phone number (optional)
        from_: Filter by sender phone number (optional)
        date_sent: Filter by date sent in YYYY-MM-DD format (optional)
        page_size: Number of results to return (default: 50, max: 1000)

    Returns:
        Dictionary containing list of messages
    """
    async with httpx.AsyncClient() as client:
        params = {"PageSize": page_size}
        if to:
            params["To"] = to
        if from_:
            params["From"] = from_
        if date_sent:
            params["DateSent"] = date_sent

        response = await client.get(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
            auth=get_auth(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_message(message_sid: str) -> dict:
    """
    Get details of a specific message.

    Args:
        message_sid: The Twilio message SID (e.g., SMxxxxx or MMxxxxx)

    Returns:
        Dictionary containing message details
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/Messages/{message_sid}.json",
            auth=get_auth(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def make_call(to: str, from_: str, url: str, method: str = "POST", status_callback: Optional[str] = None) -> dict:
    """
    Initiate an outbound phone call.

    Args:
        to: Recipient phone number in E.164 format
        from_: Your Twilio phone number in E.164 format
        url: URL that returns TwiML instructions for the call
        method: HTTP method to use for url (GET or POST, default: POST)
        status_callback: Optional URL for call status updates

    Returns:
        Dictionary containing call details including SID and status
    """
    async with httpx.AsyncClient() as client:
        data = {
            "To": to,
            "From": from_,
            "Url": url,
            "Method": method,
        }
        if status_callback:
            data["StatusCallback"] = status_callback

        response = await client.post(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/Calls.json",
            auth=get_auth(),
            data=data,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_calls(to: Optional[str] = None, from_: Optional[str] = None, status: Optional[str] = None, page_size: int = 50) -> dict:
    """
    List call logs.

    Args:
        to: Filter by recipient phone number (optional)
        from_: Filter by caller phone number (optional)
        status: Filter by status (queued, ringing, in-progress, completed, etc.)
        page_size: Number of results to return (default: 50, max: 1000)

    Returns:
        Dictionary containing list of calls
    """
    async with httpx.AsyncClient() as client:
        params = {"PageSize": page_size}
        if to:
            params["To"] = to
        if from_:
            params["From"] = from_
        if status:
            params["Status"] = status

        response = await client.get(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/Calls.json",
            auth=get_auth(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_call(call_sid: str) -> dict:
    """
    Get details of a specific call.

    Args:
        call_sid: The Twilio call SID (e.g., CAxxxxx)

    Returns:
        Dictionary containing call details
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/Calls/{call_sid}.json",
            auth=get_auth(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_account_balance() -> dict:
    """
    Get the current account balance.

    Returns:
        Dictionary containing balance information including currency and amount
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/Balance.json",
            auth=get_auth(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_phone_numbers(page_size: int = 50, phone_number: Optional[str] = None, friendly_name: Optional[str] = None) -> dict:
    """
    List phone numbers owned by your Twilio account.

    Args:
        page_size: Number of results to return (default: 50, max: 1000)
        phone_number: Filter by specific phone number (optional)
        friendly_name: Filter by friendly name (optional)

    Returns:
        Dictionary containing list of phone numbers
    """
    async with httpx.AsyncClient() as client:
        params = {"PageSize": page_size}
        if phone_number:
            params["PhoneNumber"] = phone_number
        if friendly_name:
            params["FriendlyName"] = friendly_name

        response = await client.get(
            f"{BASE_URL}/Accounts/{TWILIO_ACCOUNT_SID}/IncomingPhoneNumbers.json",
            auth=get_auth(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def lookup_phone_number(phone_number: str, country_code: Optional[str] = None, type_: Optional[str] = None) -> dict:
    """
    Validate and get information about a phone number using Twilio Lookup API.

    Args:
        phone_number: Phone number to lookup in E.164 format or national format
        country_code: ISO country code if using national format (e.g., 'US')
        type_: Additional data to retrieve ('carrier' or 'caller-name', optional)

    Returns:
        Dictionary containing phone number details, validation status, and carrier info
    """
    async with httpx.AsyncClient() as client:
        params = {}
        if country_code:
            params["CountryCode"] = country_code
        if type_:
            params["Type"] = type_

        response = await client.get(
            f"https://lookups.twilio.com/v1/PhoneNumbers/{phone_number}",
            auth=get_auth(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
