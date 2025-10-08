import os
import hashlib
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("Mailchimp")

API_KEY = os.getenv("MAILCHIMP_API_KEY")

# Extract data center from API key (e.g., "abc123-us1" -> "us1")
def get_base_url() -> str:
    """Extract data center from API key and construct base URL."""
    if not API_KEY or "-" not in API_KEY:
        raise ValueError("Invalid MAILCHIMP_API_KEY format. Expected format: key-dc (e.g., abc123-us1)")
    dc = API_KEY.split("-")[-1]
    return f"https://{dc}.api.mailchimp.com/3.0"


def get_auth() -> tuple:
    """Get Basic Auth credentials (anystring, api_key)."""
    return ("anystring", API_KEY)


def md5_hash(email: str) -> str:
    """Generate MD5 hash of lowercase email for member endpoints."""
    return hashlib.md5(email.lower().encode()).hexdigest()


@mcp.tool()
async def list_audiences(
    count: int = 10,
    offset: int = 0
) -> dict:
    """List all audience lists.

    Args:
        count: Number of audiences to return (default: 10, max: 1000)
        offset: Number of audiences to skip (default: 0)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{get_base_url()}/lists",
            auth=get_auth(),
            params={"count": count, "offset": offset}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_audience(list_id: str) -> dict:
    """Get audience details and statistics.

    Args:
        list_id: Audience list ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{get_base_url()}/lists/{list_id}",
            auth=get_auth()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_audience_members(
    list_id: str,
    status: Optional[str] = None,
    count: int = 10,
    offset: int = 0
) -> dict:
    """List members in an audience.

    Args:
        list_id: Audience list ID
        status: Filter by status (subscribed, unsubscribed, cleaned, pending, transactional)
        count: Number of members to return (default: 10, max: 1000)
        offset: Number of members to skip (default: 0)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"count": count, "offset": offset}
        if status:
            params["status"] = status

        response = await client.get(
            f"{get_base_url()}/lists/{list_id}/members",
            auth=get_auth(),
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def add_member(
    list_id: str,
    email_address: str,
    status: str = "subscribed",
    merge_fields: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    vip: bool = False
) -> dict:
    """Add a member to an audience.

    Args:
        list_id: Audience list ID
        email_address: Member email address
        status: Member status (subscribed, pending, unsubscribed, cleaned, transactional)
        merge_fields: Custom merge fields (e.g., {"FNAME": "John", "LNAME": "Doe"})
        tags: List of tag names to apply
        vip: Mark as VIP member
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "email_address": email_address,
            "status": status,
            "vip": vip
        }

        if merge_fields:
            payload["merge_fields"] = merge_fields
        if tags:
            payload["tags"] = tags

        response = await client.post(
            f"{get_base_url()}/lists/{list_id}/members",
            auth=get_auth(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_member(
    list_id: str,
    email_address: str,
    status: Optional[str] = None,
    merge_fields: Optional[Dict[str, Any]] = None,
    vip: Optional[bool] = None
) -> dict:
    """Update member information.

    Args:
        list_id: Audience list ID
        email_address: Member email address
        status: Updated status (subscribed, unsubscribed, cleaned, pending, transactional)
        merge_fields: Updated merge fields
        vip: Updated VIP status
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        subscriber_hash = md5_hash(email_address)
        payload = {}

        if status:
            payload["status"] = status
        if merge_fields:
            payload["merge_fields"] = merge_fields
        if vip is not None:
            payload["vip"] = vip

        response = await client.patch(
            f"{get_base_url()}/lists/{list_id}/members/{subscriber_hash}",
            auth=get_auth(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def delete_member(
    list_id: str,
    email_address: str
) -> dict:
    """Remove a member from audience.

    Args:
        list_id: Audience list ID
        email_address: Member email address
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        subscriber_hash = md5_hash(email_address)
        response = await client.delete(
            f"{get_base_url()}/lists/{list_id}/members/{subscriber_hash}",
            auth=get_auth()
        )
        response.raise_for_status()
        return {"success": True, "email": email_address}


@mcp.tool()
async def list_campaigns(
    status: Optional[str] = None,
    count: int = 10,
    offset: int = 0
) -> dict:
    """List email campaigns.

    Args:
        status: Filter by status (save, paused, schedule, sending, sent)
        count: Number of campaigns to return (default: 10, max: 1000)
        offset: Number of campaigns to skip (default: 0)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {"count": count, "offset": offset}
        if status:
            params["status"] = status

        response = await client.get(
            f"{get_base_url()}/campaigns",
            auth=get_auth(),
            params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_campaign(campaign_id: str) -> dict:
    """Get campaign details and statistics.

    Args:
        campaign_id: Campaign ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{get_base_url()}/campaigns/{campaign_id}",
            auth=get_auth()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_campaign(
    campaign_type: str,
    list_id: str,
    subject_line: str,
    from_name: str,
    reply_to: str,
    title: Optional[str] = None
) -> dict:
    """Create a new email campaign.

    Args:
        campaign_type: Campaign type (regular, plaintext, absplit, rss, variate)
        list_id: Audience list ID
        subject_line: Email subject line
        from_name: Sender name
        reply_to: Reply-to email address
        title: Internal campaign title
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "type": campaign_type,
            "recipients": {
                "list_id": list_id
            },
            "settings": {
                "subject_line": subject_line,
                "from_name": from_name,
                "reply_to": reply_to
            }
        }

        if title:
            payload["settings"]["title"] = title

        response = await client.post(
            f"{get_base_url()}/campaigns",
            auth=get_auth(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def send_campaign(
    campaign_id: str,
    schedule_time: Optional[str] = None
) -> dict:
    """Send or schedule a campaign.

    Args:
        campaign_id: Campaign ID
        schedule_time: ISO 8601 datetime to schedule send (None for immediate send)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        if schedule_time:
            # Schedule campaign
            response = await client.post(
                f"{get_base_url()}/campaigns/{campaign_id}/actions/schedule",
                auth=get_auth(),
                json={"schedule_time": schedule_time}
            )
        else:
            # Send immediately
            response = await client.post(
                f"{get_base_url()}/campaigns/{campaign_id}/actions/send",
                auth=get_auth()
            )

        response.raise_for_status()
        return {"success": True, "campaign_id": campaign_id, "scheduled": bool(schedule_time)}


@mcp.tool()
async def list_templates(
    count: int = 10,
    offset: int = 0
) -> dict:
    """List email templates.

    Args:
        count: Number of templates to return (default: 10, max: 1000)
        offset: Number of templates to skip (default: 0)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{get_base_url()}/templates",
            auth=get_auth(),
            params={"count": count, "offset": offset}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_campaign_reports(
    campaign_id: str
) -> dict:
    """Get campaign performance metrics.

    Args:
        campaign_id: Campaign ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{get_base_url()}/reports/{campaign_id}",
            auth=get_auth()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_segments(
    list_id: str,
    count: int = 10,
    offset: int = 0
) -> dict:
    """List audience segments.

    Args:
        list_id: Audience list ID
        count: Number of segments to return (default: 10, max: 1000)
        offset: Number of segments to skip (default: 0)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{get_base_url()}/lists/{list_id}/segments",
            auth=get_auth(),
            params={"count": count, "offset": offset}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_segment(
    list_id: str,
    name: str,
    static_segment: Optional[List[str]] = None
) -> dict:
    """Create a new segment.

    Args:
        list_id: Audience list ID
        name: Segment name
        static_segment: List of member email addresses (for static segments)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {"name": name}

        if static_segment:
            payload["static_segment"] = static_segment

        response = await client.post(
            f"{get_base_url()}/lists/{list_id}/segments",
            auth=get_auth(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_tags(
    list_id: str,
    count: int = 10,
    offset: int = 0
) -> dict:
    """List audience tags.

    Args:
        list_id: Audience list ID
        count: Number of tags to return (default: 10, max: 1000)
        offset: Number of tags to skip (default: 0)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{get_base_url()}/lists/{list_id}/tag-search",
            auth=get_auth(),
            params={"count": count, "offset": offset}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def add_tags_to_member(
    list_id: str,
    email_address: str,
    tags: List[str],
    is_syncing: bool = False
) -> dict:
    """Tag audience members.

    Args:
        list_id: Audience list ID
        email_address: Member email address
        tags: List of tag names to add
        is_syncing: Whether tags are being synced from external source
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        subscriber_hash = md5_hash(email_address)
        payload = {
            "tags": [{"name": tag, "status": "active"} for tag in tags],
            "is_syncing": is_syncing
        }

        response = await client.post(
            f"{get_base_url()}/lists/{list_id}/members/{subscriber_hash}/tags",
            auth=get_auth(),
            json=payload
        )
        response.raise_for_status()
        return {"success": True, "email": email_address, "tags_added": len(tags)}


if __name__ == "__main__":
    mcp.run()
