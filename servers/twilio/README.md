# Twilio MCP Server

MCP server for interacting with the Twilio communication API. Send SMS and WhatsApp messages, make phone calls, and manage your Twilio account.

## Features

- **SMS Messaging**: Send and manage SMS/MMS messages
- **WhatsApp Messaging**: Send WhatsApp messages via Twilio
- **Voice Calls**: Initiate and manage phone calls
- **Phone Number Management**: List and lookup phone numbers
- **Account Management**: Check balance and account status

## Setup

### Prerequisites

- Twilio account (sign up at [twilio.com](https://www.twilio.com/try-twilio))
- Twilio phone number (for sending SMS/calls)
- Account credentials from [Twilio Console](https://console.twilio.com)

### Environment Variables

- `TWILIO_ACCOUNT_SID` (required): Your Twilio Account SID
- `TWILIO_AUTH_TOKEN` (required): Your Twilio Auth Token

**How to get credentials:**
1. Go to [console.twilio.com](https://console.twilio.com)
2. Find your Account SID and Auth Token in the dashboard
3. Keep these secure - they provide full access to your Twilio account

## Available Tools

### Messaging Tools

#### `send_sms`
Send an SMS message.

**Parameters:**
- `to` (string, required): Recipient phone number in E.164 format (e.g., +1234567890)
- `from_` (string, required): Your Twilio phone number in E.164 format
- `body` (string, required): Message content (up to 1600 characters)
- `media_url` (string, optional): URL of media to send (converts to MMS)

**Example:**
```python
result = await send_sms(
    to="+1234567890",
    from_="+1987654321",
    body="Hello from Twilio MCP!",
    media_url="https://example.com/image.jpg"
)
```

#### `send_whatsapp`
Send a WhatsApp message via Twilio.

**Parameters:**
- `to` (string, required): Recipient WhatsApp number (e.g., whatsapp:+1234567890)
- `from_` (string, required): Your Twilio WhatsApp number (e.g., whatsapp:+1987654321)
- `body` (string, required): Message content
- `media_url` (string, optional): URL of media to send

**Example:**
```python
result = await send_whatsapp(
    to="whatsapp:+1234567890",
    from_="whatsapp:+1987654321",
    body="Hello from WhatsApp!",
    media_url="https://example.com/image.jpg"
)
```

#### `list_messages`
List sent and received messages with optional filters.

**Parameters:**
- `to` (string, optional): Filter by recipient phone number
- `from_` (string, optional): Filter by sender phone number
- `date_sent` (string, optional): Filter by date in YYYY-MM-DD format
- `page_size` (int, optional): Number of results (default: 50, max: 1000)

**Example:**
```python
messages = await list_messages(from_="+1987654321", page_size=20)
```

#### `get_message`
Get details of a specific message.

**Parameters:**
- `message_sid` (string, required): The Twilio message SID (e.g., SMxxxxx)

**Example:**
```python
message = await get_message(message_sid="SM1234567890abcdef")
```

### Voice Call Tools

#### `make_call`
Initiate an outbound phone call.

**Parameters:**
- `to` (string, required): Recipient phone number in E.164 format
- `from_` (string, required): Your Twilio phone number in E.164 format
- `url` (string, required): URL that returns TwiML instructions for the call
- `method` (string, optional): HTTP method (GET or POST, default: POST)
- `status_callback` (string, optional): URL for call status updates

**Example:**
```python
call = await make_call(
    to="+1234567890",
    from_="+1987654321",
    url="https://example.com/twiml",
    status_callback="https://example.com/status"
)
```

#### `list_calls`
List call logs with optional filters.

**Parameters:**
- `to` (string, optional): Filter by recipient phone number
- `from_` (string, optional): Filter by caller phone number
- `status` (string, optional): Filter by status (queued, ringing, in-progress, completed, etc.)
- `page_size` (int, optional): Number of results (default: 50, max: 1000)

**Example:**
```python
calls = await list_calls(status="completed", page_size=10)
```

#### `get_call`
Get details of a specific call.

**Parameters:**
- `call_sid` (string, required): The Twilio call SID (e.g., CAxxxxx)

**Example:**
```python
call = await get_call(call_sid="CA1234567890abcdef")
```

### Account & Phone Number Tools

#### `get_account_balance`
Get your current Twilio account balance.

**Example:**
```python
balance = await get_account_balance()
# Returns: {"balance": "100.00", "currency": "USD"}
```

#### `list_phone_numbers`
List phone numbers owned by your Twilio account.

**Parameters:**
- `page_size` (int, optional): Number of results (default: 50, max: 1000)
- `phone_number` (string, optional): Filter by specific phone number
- `friendly_name` (string, optional): Filter by friendly name

**Example:**
```python
numbers = await list_phone_numbers(page_size=10)
```

#### `lookup_phone_number`
Validate and get information about a phone number.

**Parameters:**
- `phone_number` (string, required): Phone number to lookup in E.164 format
- `country_code` (string, optional): ISO country code if using national format (e.g., 'US')
- `type_` (string, optional): Additional data ('carrier' or 'caller-name')

**Example:**
```python
info = await lookup_phone_number(
    phone_number="+1234567890",
    type_="carrier"
)
```

## Phone Number Format

All phone numbers must be in **E.164 format**:
- Start with `+` followed by country code
- Example US number: `+14155552671`
- Example UK number: `+442071838750`

## Rate Limits and Pricing

### Rate Limits
- **SMS**: 100 messages per second per account (contact Twilio to increase)
- **Voice**: 100 concurrent calls per account (contact Twilio to increase)
- **API Requests**: 10,000 requests per second

### Pricing (as of 2024, subject to change)
- **SMS (US)**: $0.0079 per message
- **WhatsApp**: $0.005 per conversation (first 1,000 free monthly)
- **Voice (US)**: $0.0140 per minute
- **Phone Number**: $1.15 per month
- **Lookup API**: $0.005 per request (carrier info extra)

Visit [Twilio Pricing](https://www.twilio.com/pricing) for current rates.

## Security Best Practices

1. **Never commit credentials**: Keep `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` in environment variables
2. **Use API keys**: Consider using [Twilio API Keys](https://www.twilio.com/docs/iam/keys/api-key) for additional security
3. **Enable IP filtering**: Restrict API access to specific IP addresses in Twilio Console
4. **Monitor usage**: Set up usage alerts in Twilio Console to detect unusual activity
5. **Rotate credentials**: Periodically rotate your Auth Token
6. **Use test credentials**: Use test credentials for development (prefix with `AC` for test accounts)

## TwiML Resources

For making calls with `make_call`, you need a URL that returns TwiML (Twilio Markup Language):

**Simple TwiML example:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Hello! This is a call from Twilio.</Say>
</Response>
```

Learn more about TwiML at [twilio.com/docs/voice/twiml](https://www.twilio.com/docs/voice/twiml)

## API Documentation

For detailed information about the Twilio API:
- [Twilio API Documentation](https://www.twilio.com/docs/usage/api)
- [Messaging API](https://www.twilio.com/docs/sms)
- [Voice API](https://www.twilio.com/docs/voice)
- [WhatsApp API](https://www.twilio.com/docs/whatsapp)
- [Lookup API](https://www.twilio.com/docs/lookup)

## Error Handling

Common errors and solutions:

- **21211**: Invalid phone number - Ensure E.164 format
- **21608**: Unverified number - Verify trial account numbers in Console
- **21610**: Message blocked - Check compliance and opt-in requirements
- **20003**: Authentication error - Verify credentials are correct
- **20429**: Rate limit exceeded - Implement exponential backoff

## Support

- [Twilio Support](https://support.twilio.com)
- [Twilio Community](https://www.twilio.com/community)
- [Twilio Console](https://console.twilio.com)
