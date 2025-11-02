"""
Stripe MCP Server
Provides tools for interacting with the Stripe payment API.
"""

import os
from typing import Optional
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Stripe MCP Server")

# Get API key from environment
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
BASE_URL = "https://api.stripe.com/v1"


def get_headers():
    """Get headers for Stripe API requests."""
    if not STRIPE_API_KEY:
        raise ValueError("STRIPE_API_KEY environment variable is required")
    return {
        "Authorization": f"Bearer {STRIPE_API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded",
    }


@mcp.tool()
async def list_customers(limit: int = 10, starting_after: Optional[str] = None) -> dict:
    """
    List customers from Stripe.

    Args:
        limit: Number of customers to return (default: 10, max: 100)
        starting_after: Cursor for pagination (customer ID)

    Returns:
        Dictionary containing customer list and pagination info
    """
    async with httpx.AsyncClient() as client:
        params = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after

        response = await client.get(
            f"{BASE_URL}/customers",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_customer(customer_id: str) -> dict:
    """
    Get details of a specific customer.

    Args:
        customer_id: The Stripe customer ID (e.g., cus_xxx)

    Returns:
        Dictionary containing customer details
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/customers/{customer_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_customers(query: str, limit: int = 10) -> dict:
    """
    Search for customers using Stripe's search API.

    Args:
        query: Search query (e.g., "email:'customer@example.com'" or "name:'John'")
        limit: Number of results to return (default: 10, max: 100)

    Returns:
        Dictionary containing search results
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/customers/search",
            headers=get_headers(),
            params={"query": query, "limit": limit},
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_charges(limit: int = 10, customer: Optional[str] = None, starting_after: Optional[str] = None) -> dict:
    """
    List charges/payments from Stripe.

    Args:
        limit: Number of charges to return (default: 10, max: 100)
        customer: Filter by customer ID (optional)
        starting_after: Cursor for pagination (charge ID)

    Returns:
        Dictionary containing charge list and pagination info
    """
    async with httpx.AsyncClient() as client:
        params = {"limit": limit}
        if customer:
            params["customer"] = customer
        if starting_after:
            params["starting_after"] = starting_after

        response = await client.get(
            f"{BASE_URL}/charges",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_charge(charge_id: str) -> dict:
    """
    Get details of a specific charge/payment.

    Args:
        charge_id: The Stripe charge ID (e.g., ch_xxx)

    Returns:
        Dictionary containing charge details
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/charges/{charge_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_subscriptions(limit: int = 10, customer: Optional[str] = None, status: Optional[str] = None, starting_after: Optional[str] = None) -> dict:
    """
    List subscriptions from Stripe.

    Args:
        limit: Number of subscriptions to return (default: 10, max: 100)
        customer: Filter by customer ID (optional)
        status: Filter by status (e.g., 'active', 'canceled', 'past_due')
        starting_after: Cursor for pagination (subscription ID)

    Returns:
        Dictionary containing subscription list and pagination info
    """
    async with httpx.AsyncClient() as client:
        params = {"limit": limit}
        if customer:
            params["customer"] = customer
        if status:
            params["status"] = status
        if starting_after:
            params["starting_after"] = starting_after

        response = await client.get(
            f"{BASE_URL}/subscriptions",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_subscription(subscription_id: str) -> dict:
    """
    Get details of a specific subscription.

    Args:
        subscription_id: The Stripe subscription ID (e.g., sub_xxx)

    Returns:
        Dictionary containing subscription details
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/subscriptions/{subscription_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_payment_intent(amount: int, currency: str = "usd", customer: Optional[str] = None, description: Optional[str] = None, metadata: Optional[dict] = None) -> dict:
    """
    Create a payment intent for processing a payment.

    Args:
        amount: Amount in smallest currency unit (e.g., cents for USD)
        currency: Three-letter ISO currency code (default: 'usd')
        customer: Customer ID to associate with this payment (optional)
        description: Description of the payment (optional)
        metadata: Additional metadata as key-value pairs (optional)

    Returns:
        Dictionary containing payment intent details
    """
    async with httpx.AsyncClient() as client:
        data = {
            "amount": amount,
            "currency": currency,
        }
        if customer:
            data["customer"] = customer
        if description:
            data["description"] = description
        if metadata:
            for key, value in metadata.items():
                data[f"metadata[{key}]"] = value

        response = await client.post(
            f"{BASE_URL}/payment_intents",
            headers=get_headers(),
            data=data,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_products(limit: int = 10, active: Optional[bool] = None, starting_after: Optional[str] = None) -> dict:
    """
    List products from Stripe.

    Args:
        limit: Number of products to return (default: 10, max: 100)
        active: Filter by active status (true/false, optional)
        starting_after: Cursor for pagination (product ID)

    Returns:
        Dictionary containing product list and pagination info
    """
    async with httpx.AsyncClient() as client:
        params = {"limit": limit}
        if active is not None:
            params["active"] = str(active).lower()
        if starting_after:
            params["starting_after"] = starting_after

        response = await client.get(
            f"{BASE_URL}/products",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_invoice(invoice_id: str) -> dict:
    """
    Get details of a specific invoice.

    Args:
        invoice_id: The Stripe invoice ID (e.g., in_xxx)

    Returns:
        Dictionary containing invoice details
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/invoices/{invoice_id}",
            headers=get_headers(),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_invoices(limit: int = 10, customer: Optional[str] = None, status: Optional[str] = None, starting_after: Optional[str] = None) -> dict:
    """
    List invoices from Stripe.

    Args:
        limit: Number of invoices to return (default: 10, max: 100)
        customer: Filter by customer ID (optional)
        status: Filter by status (e.g., 'draft', 'open', 'paid', 'void')
        starting_after: Cursor for pagination (invoice ID)

    Returns:
        Dictionary containing invoice list and pagination info
    """
    async with httpx.AsyncClient() as client:
        params = {"limit": limit}
        if customer:
            params["customer"] = customer
        if status:
            params["status"] = status
        if starting_after:
            params["starting_after"] = starting_after

        response = await client.get(
            f"{BASE_URL}/invoices",
            headers=get_headers(),
            params=params,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
