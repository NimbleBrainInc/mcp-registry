# Stripe MCP Server

MCP server for interacting with the Stripe payment API. Manage customers, payments, subscriptions, invoices, and products.

## Features

- **Customer Management**: List, search, and get customer details
- **Payment Processing**: List charges, get payment details, create payment intents
- **Subscription Management**: List and get subscription details
- **Product Management**: List products from your Stripe catalog
- **Invoice Management**: List and get invoice details

## Setup

### Prerequisites

- Stripe account
- Stripe API key (get from [Stripe Dashboard](https://stripe.com/dashboard/apikeys))

### Environment Variables

- `STRIPE_API_KEY` (required): Your Stripe API key (secret or restricted key)

## Available Tools

### Customer Tools

- `list_customers` - List customers with pagination
- `get_customer` - Get details of a specific customer
- `search_customers` - Search for customers by query

### Payment Tools

- `list_charges` - List charges/payments with optional filters
- `get_charge` - Get details of a specific charge
- `create_payment_intent` - Create a new payment intent

### Subscription Tools

- `list_subscriptions` - List subscriptions with optional filters
- `get_subscription` - Get details of a specific subscription

### Product Tools

- `list_products` - List products from your catalog

### Invoice Tools

- `list_invoices` - List invoices with optional filters
- `get_invoice` - Get details of a specific invoice

## Usage Example

```python
# List recent customers
customers = await list_customers(limit=10)

# Search for a customer by email
results = await search_customers(query="email:'customer@example.com'")

# Get customer details
customer = await get_customer(customer_id="cus_xxx")

# Create a payment intent
payment = await create_payment_intent(
    amount=2000,  # $20.00 in cents
    currency="usd",
    customer="cus_xxx",
    description="Payment for order #123"
)

# List subscriptions for a customer
subscriptions = await list_subscriptions(customer="cus_xxx", status="active")
```

## API Documentation

For detailed information about the Stripe API, visit:
- [Stripe API Documentation](https://stripe.com/docs/api)
- [Stripe API Reference](https://stripe.com/docs/api/authentication)

## Notes

- All amount values are in the smallest currency unit (e.g., cents for USD)
- API keys should be kept secure and never committed to version control
- Use test mode keys for development and live keys for production
- Pagination is supported via `starting_after` parameter for list endpoints
