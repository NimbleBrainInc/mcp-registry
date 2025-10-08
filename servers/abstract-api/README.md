# Abstract API MCP Server

MCP server for Abstract API suite. Comprehensive validation, geolocation, timezone, holidays, exchange rates, and web utilities - all services unified under one API key.

## Features

- **Email Validation**: Syntax, deliverability, disposable detection
- **Phone Validation**: Format, carrier, country, line type
- **IP Geolocation**: Location, ISP, timezone, currency, security
- **VAT Validation**: EU VAT number verification
- **Timezone**: Convert times, get timezone info, DST support
- **Holidays**: Public holidays for 200+ countries
- **Exchange Rates**: 170+ currencies, historical rates
- **Company Enrichment**: Get company data from domain
- **Web Scraping**: Extract structured data from web pages
- **Screenshots**: Generate website screenshots

## Setup

### Prerequisites

- Abstract API account (free or paid)
- API key (one key for all services)

### Environment Variables

- `ABSTRACT_API_KEY` (required): Your Abstract API key

**How to get credentials:**
1. Go to [abstractapi.com](https://www.abstractapi.com/)
2. Sign up or log in
3. Go to app.abstractapi.com
4. Find your API key in the dashboard
5. Copy the key and store as `ABSTRACT_API_KEY`

Direct link: https://app.abstractapi.com/

**Note**: One API key works for all Abstract API services!

## Rate Limits

**Free Tier** (per service):
- Email Validation: 100 requests/month
- Phone Validation: 100 requests/month
- IP Geolocation: 20,000 requests/month
- VAT Validation: 100 requests/month
- Timezone: 1,000 requests/month
- Holidays: 1,000 requests/month
- Exchange Rates: 1,000 requests/month
- Company Enrichment: 100 requests/month
- Web Scraping: 100 requests/month

**Paid Plans**: Unlimited requests based on tier

## Available Tools

### Email Validation

#### `validate_email`
Validate email address and check deliverability.

**Parameters:**
- `email` (string, required): Email address to validate

**Example:**
```python
result = await validate_email(email="user@example.com")

# Returns:
# {
#   "email": "user@example.com",
#   "autocorrect": "",
#   "deliverability": "DELIVERABLE",
#   "quality_score": 0.99,
#   "is_valid_format": {
#     "value": true,
#     "text": "TRUE"
#   },
#   "is_free_email": {
#     "value": false,
#     "text": "FALSE"
#   },
#   "is_disposable_email": {
#     "value": false,
#     "text": "FALSE"
#   },
#   "is_role_email": {
#     "value": false,
#     "text": "FALSE"
#   },
#   "is_catchall_email": {
#     "value": true,
#     "text": "TRUE"
#   },
#   "is_mx_found": {
#     "value": true,
#     "text": "TRUE"
#   },
#   "is_smtp_valid": {
#     "value": true,
#     "text": "TRUE"
#   }
# }
```

**Deliverability Scores:**
- `DELIVERABLE`: Email is valid and deliverable
- `UNDELIVERABLE`: Email will bounce
- `RISKY`: Email may bounce
- `UNKNOWN`: Cannot determine deliverability

**Use Cases:**
- Form validation
- List cleaning
- Fraud prevention
- Bounce reduction

### Phone Validation

#### `validate_phone`
Validate phone number and get carrier info.

**Parameters:**
- `phone` (string, required): Phone number to validate
- `country_code` (string, optional): ISO 3166-1 alpha-2 country code

**Example:**
```python
# With country code
result = await validate_phone(
    phone="14152007986",
    country_code="US"
)

# Without country code (auto-detect)
result = await validate_phone(phone="+14152007986")

# Returns:
# {
#   "phone": "14152007986",
#   "valid": true,
#   "format": {
#     "international": "+14152007986",
#     "local": "(415) 200-7986"
#   },
#   "country": {
#     "code": "US",
#     "name": "United States",
#     "prefix": "+1"
#   },
#   "location": "California",
#   "type": "mobile",
#   "carrier": "T-Mobile USA, Inc."
# }
```

**Line Types:**
- `mobile`: Mobile phone
- `landline`: Landline phone
- `voip`: VoIP number
- `unknown`: Cannot determine

**Use Cases:**
- SMS verification
- Contact validation
- Fraud detection
- 2FA setup

### IP Geolocation

#### `geolocate_ip`
Get location data from IP address.

**Parameters:**
- `ip_address` (string, required): IP address to geolocate
- `fields` (string, optional): Comma-separated fields to return

**Example:**
```python
# Full geolocation data
result = await geolocate_ip(ip_address="8.8.8.8")

# Specific fields only
result = await geolocate_ip(
    ip_address="8.8.8.8",
    fields="city,country,timezone"
)

# Returns:
# {
#   "ip_address": "8.8.8.8",
#   "city": "Mountain View",
#   "city_geoname_id": 5375480,
#   "region": "California",
#   "region_iso_code": "CA",
#   "region_geoname_id": 5332921,
#   "postal_code": "94035",
#   "country": "United States",
#   "country_code": "US",
#   "country_geoname_id": 6252001,
#   "country_is_eu": false,
#   "continent": "North America",
#   "continent_code": "NA",
#   "continent_geoname_id": 6255149,
#   "longitude": -122.0574,
#   "latitude": 37.4192,
#   "timezone": {
#     "name": "America/Los_Angeles",
#     "abbreviation": "PST",
#     "gmt_offset": -8,
#     "current_time": "11:24:07",
#     "is_dst": false
#   },
#   "currency": {
#     "currency_name": "USD",
#     "currency_code": "USD"
#   },
#   "connection": {
#     "autonomous_system_number": 15169,
#     "autonomous_system_organization": "Google LLC",
#     "connection_type": "Corporate",
#     "isp_name": "Google LLC",
#     "organization_name": "Google LLC"
#   }
# }
```

#### `get_ip_info`
Get detailed IP information (ISP, ASN, etc.).

**Parameters:**
- `ip_address` (string, required): IP address to query

**Example:**
```python
info = await get_ip_info(ip_address="1.1.1.1")

# Returns full geolocation plus ISP details
```

#### `check_vpn`
Detect if IP is from VPN/proxy/datacenter.

**Parameters:**
- `ip_address` (string, required): IP address to check

**Example:**
```python
result = await check_vpn(ip_address="1.1.1.1")

# Returns:
# {
#   "security": {
#     "is_vpn": false,
#     "is_proxy": false,
#     "is_tor": false,
#     "is_relay": false,
#     "is_hosting": true,
#     "is_cloud_provider": true
#   }
# }
```

**Use Cases:**
- Fraud prevention
- Geographic restrictions
- Security monitoring
- Compliance checks

### VAT Validation

#### `validate_vat`
Validate EU VAT numbers.

**Parameters:**
- `vat_number` (string, required): VAT number (e.g., "SE556656688001")

**Example:**
```python
result = await validate_vat(vat_number="SE556656688001")

# Returns:
# {
#   "vat_number": "SE556656688001",
#   "valid": true,
#   "company": {
#     "name": "GOOGLE SWEDEN AB",
#     "address": "GOOGLE IRLAND LTD, GOOGLE SWEDEN AB, KARLAVÄGEN 100, 115 26, STOCKHOLM"
#   },
#   "country": {
#     "code": "SE",
#     "name": "Sweden"
#   }
# }
```

**Supported Countries**: All EU member states

**Use Cases:**
- B2B transactions
- Tax compliance
- Invoice validation
- Business verification

### Timezone

#### `get_timezone`
Get timezone from location or coordinates.

**Parameters:**
- `location` (string, optional): Location name
- `latitude` (float, optional): Latitude coordinate
- `longitude` (float, optional): Longitude coordinate

**Example:**
```python
# By location
result = await get_timezone(location="New York")

# By coordinates
result = await get_timezone(
    latitude=40.7128,
    longitude=-74.0060
)

# Returns:
# {
#   "datetime": "2025-10-08 11:24:07",
#   "timezone_name": "America/New_York",
#   "timezone_abbreviation": "EDT",
#   "timezone_offset": -4,
#   "timezone_location": "New York",
#   "is_dst": true,
#   "requested_location": "New York",
#   "latitude": 40.7128,
#   "longitude": -74.0060
# }
```

#### `convert_timezone`
Convert time between timezones.

**Parameters:**
- `base_location` (string, required): Source location/timezone
- `base_datetime` (string, required): Datetime in ISO 8601 format
- `target_location` (string, required): Target location/timezone

**Example:**
```python
result = await convert_timezone(
    base_location="New York",
    base_datetime="2025-10-08T12:00:00",
    target_location="London"
)

# Returns:
# {
#   "base_location": "New York",
#   "base_datetime": "2025-10-08 12:00:00",
#   "target_location": "London",
#   "target_datetime": "2025-10-08 17:00:00",
#   "timezone_difference": "+5 hours"
# }
```

**Use Cases:**
- Meeting schedulers
- Event coordination
- Travel planning
- Global team management

### Holidays

#### `get_holidays`
Get public holidays for a country and year.

**Parameters:**
- `country` (string, required): ISO 3166-1 alpha-2 country code
- `year` (int, required): Year (e.g., 2025)
- `month` (int, optional): Month (1-12)
- `day` (int, optional): Day (1-31)

**Example:**
```python
# All holidays for a year
holidays = await get_holidays(country="US", year=2025)

# Holidays for a specific month
holidays = await get_holidays(
    country="US",
    year=2025,
    month=12
)

# Check if specific date is a holiday
holidays = await get_holidays(
    country="US",
    year=2025,
    month=7,
    day=4
)

# Returns:
# [
#   {
#     "name": "Independence Day",
#     "name_local": "",
#     "language": "",
#     "description": "",
#     "country": "US",
#     "location": "United States",
#     "type": "National",
#     "date": "07/04/2025",
#     "date_year": "2025",
#     "date_month": "07",
#     "date_day": "04",
#     "week_day": "Friday"
#   }
# ]
```

**Supported**: 200+ countries

**Use Cases:**
- Delivery planning
- Business hours
- Scheduling systems
- Compliance calendars

### Exchange Rates

#### `get_exchange_rates`
Get current currency exchange rates.

**Parameters:**
- `base` (string, optional): Base currency code (default: USD)
- `target` (string, optional): Target currency code (returns all if not specified)

**Example:**
```python
# All rates from USD
rates = await get_exchange_rates(base="USD")

# Specific currency pair
rates = await get_exchange_rates(
    base="USD",
    target="EUR"
)

# Returns:
# {
#   "base": "USD",
#   "last_updated": 1728396000,
#   "exchange_rates": {
#     "EUR": 0.92,
#     "GBP": 0.79,
#     "JPY": 149.5,
#     ...
#   }
# }
```

#### `convert_currency`
Convert amount between currencies.

**Parameters:**
- `base` (string, required): Base currency code
- `target` (string, required): Target currency code
- `amount` (float, required): Amount to convert
- `date` (string, optional): Historical date (YYYY-MM-DD)

**Example:**
```python
# Current rates
result = await convert_currency(
    base="USD",
    target="EUR",
    amount=100.00
)

# Historical rates
result = await convert_currency(
    base="USD",
    target="EUR",
    amount=100.00,
    date="2024-01-01"
)

# Returns:
# {
#   "base": "USD",
#   "target": "EUR",
#   "amount": 100.00,
#   "converted_amount": 92.00,
#   "exchange_rate": 0.92,
#   "date": "2025-10-08"
# }
```

**Supported**: 170+ currencies

**Use Cases:**
- E-commerce pricing
- Financial reporting
- Travel budgets
- International invoicing

### Company Enrichment

#### `get_company_info`
Get company data from domain name.

**Parameters:**
- `domain` (string, required): Company domain

**Example:**
```python
company = await get_company_info(domain="google.com")

# Returns:
# {
#   "name": "Google",
#   "domain": "google.com",
#   "year_founded": 1998,
#   "industry": "Internet",
#   "employees_count": 100000,
#   "locality": "Mountain View",
#   "country": "United States",
#   "country_code": "US",
#   "linkedin_url": "linkedin.com/company/google"
# }
```

**Use Cases:**
- Lead enrichment
- Sales intelligence
- Market research
- Contact discovery

### Web Utilities

#### `scrape_url`
Extract structured data from web pages.

**Parameters:**
- `url` (string, required): URL to scrape
- `render_js` (bool, optional): Render JavaScript (default: false)

**Example:**
```python
# Static content
data = await scrape_url(url="https://example.com")

# JavaScript-rendered content
data = await scrape_url(
    url="https://example.com",
    render_js=True
)

# Returns:
# {
#   "url": "https://example.com",
#   "title": "Example Domain",
#   "meta": {...},
#   "text": "...",
#   "html": "...",
#   "links": [...]
# }
```

#### `generate_screenshot`
Generate website screenshot.

**Parameters:**
- `url` (string, required): URL to screenshot
- `width` (int, optional): Width in pixels (default: 1920)
- `height` (int, optional): Height in pixels (default: 1080)
- `full_page` (bool, optional): Capture full page (default: false)

**Example:**
```python
screenshot = await generate_screenshot(
    url="https://example.com",
    width=1920,
    height=1080,
    full_page=False
)

# Returns image data
```

**Use Cases:**
- Website monitoring
- Visual testing
- Documentation
- Archiving

## Common Workflows

### Form Validation
```python
# Validate email
email_result = await validate_email(email="user@example.com")

if email_result["deliverability"] == "DELIVERABLE":
    # Validate phone
    phone_result = await validate_phone(
        phone="+14152007986",
        country_code="US"
    )

    if phone_result["valid"]:
        # Continue with registration
        pass
```

### Fraud Detection
```python
# Check email
email = await validate_email(email="user@temp-mail.com")

if email["is_disposable_email"]["value"]:
    # Block disposable email
    pass

# Check IP
ip = await check_vpn(ip_address="1.2.3.4")

if ip["security"]["is_vpn"] or ip["security"]["is_proxy"]:
    # Flag suspicious activity
    pass
```

### E-commerce Pricing
```python
# Get user's location
location = await geolocate_ip(ip_address="1.2.3.4")
user_currency = location["currency"]["currency_code"]

# Convert price to user's currency
price_usd = 99.99
converted = await convert_currency(
    base="USD",
    target=user_currency,
    amount=price_usd
)

# Display price in user's currency
display_price = converted["converted_amount"]
```

### Meeting Scheduler
```python
# Get user's timezone
user_tz = await get_timezone(location="New York")

# Convert meeting time
meeting = await convert_timezone(
    base_location="Los Angeles",
    base_datetime="2025-10-15T14:00:00",
    target_location="New York"
)

# Show meeting time in user's timezone
print(f"Meeting at: {meeting['target_datetime']}")
```

## Best Practices

1. **Cache results**: Many validations can be cached
2. **Batch validations**: Process multiple items efficiently
3. **Handle errors gracefully**: Plan for API failures
4. **Use specific fields**: Request only needed data for IP geolocation
5. **Monitor usage**: Track API calls per service
6. **Validate inputs**: Check format before API calls
7. **Use country codes**: Improves phone validation accuracy
8. **Historical rates**: Use for financial reporting
9. **Secure API key**: Never expose in client-side code
10. **Test thoroughly**: Validate with various inputs

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid API key
- **402 Payment Required**: Quota exceeded
- **400 Bad Request**: Invalid parameters
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Service issue

## API Documentation

- [Abstract API Documentation](https://docs.abstractapi.com/)
- [Email Validation](https://docs.abstractapi.com/email-validation)
- [Phone Validation](https://docs.abstractapi.com/phone-validation)
- [IP Geolocation](https://docs.abstractapi.com/ip-geolocation)
- [VAT Validation](https://docs.abstractapi.com/vat-validation)
- [Timezone](https://docs.abstractapi.com/timezone)
- [Holidays](https://docs.abstractapi.com/holidays)
- [Exchange Rates](https://docs.abstractapi.com/exchange-rates)

## Support

- [Help Center](https://help.abstractapi.com/)
- [Contact Support](https://www.abstractapi.com/contact)
- [API Status](https://status.abstractapi.com/)
- [Community](https://community.abstractapi.com/)
