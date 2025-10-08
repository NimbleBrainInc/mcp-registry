# Mailchimp MCP Server

MCP server for Mailchimp Marketing API. Manage email marketing campaigns, audiences, members, segments, and analytics with comprehensive automation features.

## Features

- **Audience Management**: Create and manage subscriber lists
- **Member Operations**: Add, update, and organize subscribers
- **Campaign Management**: Create, send, and schedule email campaigns
- **Segmentation**: Target specific audience groups
- **Tags**: Organize and categorize members
- **Analytics**: Track campaign performance metrics
- **Templates**: Manage email templates
- **Automation**: Workflow automation support

## Setup

### Prerequisites

- Mailchimp account (free or paid)
- API key with data center identifier

### Environment Variables

- `MAILCHIMP_API_KEY` (required): Your Mailchimp API key with data center

**How to get credentials:**
1. Go to [mailchimp.com](https://mailchimp.com/)
2. Log in to your account
3. Click your profile icon → Account & Billing
4. Go to Extras → API keys
5. Click "Create A Key"
6. Copy the API key (format: `abc123-us1`)
7. Store as `MAILCHIMP_API_KEY`

Direct link: https://admin.mailchimp.com/account/api/

**Understanding API Key Format:**
- API keys include a data center identifier after the dash
- Example: `abc123def456-us1`
- The `us1` part is the data center (can be us1-us20, etc.)
- This determines your API base URL: `https://us1.api.mailchimp.com/3.0`

## Rate Limits

- **Standard**: 10 requests per second for most endpoints
- **Batch operations**: 1 request per second
- Higher limits available for paid accounts
- HTTP 429 response when limit exceeded

## Available Tools

### Audience Management

#### `list_audiences`
List all audience lists.

**Parameters:**
- `count` (int, optional): Number of audiences to return (default: 10, max: 1000)
- `offset` (int, optional): Number to skip for pagination (default: 0)

**Example:**
```python
audiences = await list_audiences(count=20)

# Returns:
# {
#   "lists": [
#     {
#       "id": "abc123",
#       "name": "Newsletter Subscribers",
#       "stats": {
#         "member_count": 5432,
#         "unsubscribe_count": 123,
#         "open_rate": 23.5,
#         "click_rate": 4.2
#       }
#     }
#   ],
#   "total_items": 5
# }
```

#### `get_audience`
Get audience details and statistics.

**Parameters:**
- `list_id` (string, required): Audience list ID

**Example:**
```python
audience = await get_audience(list_id="abc123")

# Returns detailed stats:
# - member_count, unsubscribe_count
# - open_rate, click_rate
# - date_created, modules (signup forms, etc.)
# - contact info, permission_reminder
# - campaign_defaults (from_name, from_email, subject)
```

### Member Management

#### `list_audience_members`
List members in an audience.

**Parameters:**
- `list_id` (string, required): Audience list ID
- `status` (string, optional): Filter by status
- `count` (int, optional): Number to return (default: 10, max: 1000)
- `offset` (int, optional): Number to skip (default: 0)

**Member Status Values:**
- **subscribed**: Active subscribers
- **unsubscribed**: Unsubscribed members
- **cleaned**: Bounced or invalid emails
- **pending**: Awaiting opt-in confirmation
- **transactional**: Transactional-only subscribers

**Example:**
```python
# All members
members = await list_audience_members(list_id="abc123")

# Active subscribers only
active = await list_audience_members(
    list_id="abc123",
    status="subscribed",
    count=100
)

# Unsubscribed members
unsubscribed = await list_audience_members(
    list_id="abc123",
    status="unsubscribed"
)
```

#### `add_member`
Add a member to an audience.

**Parameters:**
- `list_id` (string, required): Audience list ID
- `email_address` (string, required): Member email
- `status` (string, optional): Member status (default: subscribed)
- `merge_fields` (dict, optional): Custom fields
- `tags` (list, optional): Tag names to apply
- `vip` (bool, optional): Mark as VIP (default: false)

**Common Merge Fields:**
- `FNAME`: First name
- `LNAME`: Last name
- `PHONE`: Phone number
- `BIRTHDAY`: Birthday (MM/DD format)
- `ADDRESS`: Address object
- Custom fields defined in your audience

**Example:**
```python
# Simple subscription
member = await add_member(
    list_id="abc123",
    email_address="user@example.com",
    status="subscribed"
)

# Full member with custom fields
member = await add_member(
    list_id="abc123",
    email_address="john@example.com",
    status="subscribed",
    merge_fields={
        "FNAME": "John",
        "LNAME": "Doe",
        "PHONE": "+1-555-0123"
    },
    tags=["customer", "vip"],
    vip=True
)

# Pending confirmation (double opt-in)
member = await add_member(
    list_id="abc123",
    email_address="user@example.com",
    status="pending"
)
```

#### `update_member`
Update member information.

**Parameters:**
- `list_id` (string, required): Audience list ID
- `email_address` (string, required): Member email
- `status` (string, optional): Updated status
- `merge_fields` (dict, optional): Updated fields
- `vip` (bool, optional): Updated VIP status

**Example:**
```python
# Update status (subscribe)
member = await update_member(
    list_id="abc123",
    email_address="user@example.com",
    status="subscribed"
)

# Update information
member = await update_member(
    list_id="abc123",
    email_address="user@example.com",
    merge_fields={
        "FNAME": "Jane",
        "PHONE": "+1-555-9999"
    }
)

# Unsubscribe member
member = await update_member(
    list_id="abc123",
    email_address="user@example.com",
    status="unsubscribed"
)

# Make VIP
member = await update_member(
    list_id="abc123",
    email_address="user@example.com",
    vip=True
)
```

#### `delete_member`
Remove a member from audience (permanent deletion).

**Parameters:**
- `list_id` (string, required): Audience list ID
- `email_address` (string, required): Member email

**Example:**
```python
result = await delete_member(
    list_id="abc123",
    email_address="user@example.com"
)

# Note: This permanently deletes the member
# To unsubscribe instead, use update_member with status="unsubscribed"
```

### Campaign Management

#### `list_campaigns`
List email campaigns.

**Parameters:**
- `status` (string, optional): Filter by status
- `count` (int, optional): Number to return (default: 10, max: 1000)
- `offset` (int, optional): Number to skip (default: 0)

**Campaign Status Values:**
- **save**: Draft campaign
- **paused**: Paused campaign
- **schedule**: Scheduled to send
- **sending**: Currently sending
- **sent**: Completed campaign

**Example:**
```python
# All campaigns
campaigns = await list_campaigns(count=20)

# Sent campaigns only
sent = await list_campaigns(status="sent")

# Draft campaigns
drafts = await list_campaigns(status="save")
```

#### `get_campaign`
Get campaign details and statistics.

**Parameters:**
- `campaign_id` (string, required): Campaign ID

**Example:**
```python
campaign = await get_campaign(campaign_id="xyz789")

# Returns:
# - id, type, status
# - settings (subject_line, from_name, reply_to, etc.)
# - recipients (list_id, segment info)
# - send_time, create_time
# - report_summary (opens, clicks, etc.)
```

#### `create_campaign`
Create a new email campaign.

**Parameters:**
- `campaign_type` (string, required): Campaign type
- `list_id` (string, required): Audience list ID
- `subject_line` (string, required): Email subject
- `from_name` (string, required): Sender name
- `reply_to` (string, required): Reply-to email
- `title` (string, optional): Internal campaign title

**Campaign Types:**
- **regular**: Standard email campaign
- **plaintext**: Plain text only
- **absplit**: A/B split test
- **rss**: RSS-driven campaign
- **variate**: Multivariate test

**Example:**
```python
# Create regular campaign
campaign = await create_campaign(
    campaign_type="regular",
    list_id="abc123",
    subject_line="Monthly Newsletter - October 2025",
    from_name="Company Name",
    reply_to="hello@company.com",
    title="October Newsletter"
)

# Create A/B test campaign
ab_campaign = await create_campaign(
    campaign_type="absplit",
    list_id="abc123",
    subject_line="Subject Line A",
    from_name="Company",
    reply_to="hello@company.com"
)

# After creation, add content with Mailchimp's content endpoints
```

#### `send_campaign`
Send or schedule a campaign.

**Parameters:**
- `campaign_id` (string, required): Campaign ID
- `schedule_time` (string, optional): ISO 8601 datetime for scheduling

**Example:**
```python
# Send immediately
result = await send_campaign(campaign_id="xyz789")

# Schedule for later
result = await send_campaign(
    campaign_id="xyz789",
    schedule_time="2025-10-15T10:00:00Z"
)

# Note: Campaign must have content before sending
```

#### `list_templates`
List email templates.

**Parameters:**
- `count` (int, optional): Number to return (default: 10, max: 1000)
- `offset` (int, optional): Number to skip (default: 0)

**Example:**
```python
templates = await list_templates(count=50)

# Returns:
# {
#   "templates": [
#     {
#       "id": 123,
#       "name": "Newsletter Template",
#       "type": "user",
#       "category": "custom"
#     }
#   ]
# }
```

### Analytics

#### `get_campaign_reports`
Get campaign performance metrics.

**Parameters:**
- `campaign_id` (string, required): Campaign ID

**Example:**
```python
report = await get_campaign_reports(campaign_id="xyz789")

# Returns comprehensive stats:
# {
#   "id": "xyz789",
#   "type": "regular",
#   "emails_sent": 10000,
#   "opens": {
#     "opens_total": 2500,
#     "unique_opens": 2100,
#     "open_rate": 21.0
#   },
#   "clicks": {
#     "clicks_total": 450,
#     "unique_clicks": 380,
#     "click_rate": 3.8
#   },
#   "bounces": {
#     "hard_bounces": 15,
#     "soft_bounces": 25
#   },
#   "unsubscribed": 12,
#   "industry_stats": {
#     "open_rate": 18.5,
#     "click_rate": 2.3
#   }
# }
```

### Segmentation

#### `list_segments`
List audience segments.

**Parameters:**
- `list_id` (string, required): Audience list ID
- `count` (int, optional): Number to return (default: 10, max: 1000)
- `offset` (int, optional): Number to skip (default: 0)

**Example:**
```python
segments = await list_segments(list_id="abc123")

# Returns:
# {
#   "segments": [
#     {
#       "id": 456,
#       "name": "VIP Customers",
#       "member_count": 250,
#       "type": "saved"
#     }
#   ]
# }
```

#### `create_segment`
Create a new segment.

**Parameters:**
- `list_id` (string, required): Audience list ID
- `name` (string, required): Segment name
- `static_segment` (list, optional): List of member emails (for static segments)

**Example:**
```python
# Static segment with specific members
segment = await create_segment(
    list_id="abc123",
    name="Beta Testers",
    static_segment=[
        "user1@example.com",
        "user2@example.com",
        "user3@example.com"
    ]
)

# For dynamic segments, use Mailchimp's condition builder in the UI
# or advanced API endpoints
```

### Tags

#### `list_tags`
List audience tags.

**Parameters:**
- `list_id` (string, required): Audience list ID
- `count` (int, optional): Number to return (default: 10, max: 1000)
- `offset` (int, optional): Number to skip (default: 0)

**Example:**
```python
tags = await list_tags(list_id="abc123")

# Returns:
# {
#   "tags": [
#     {
#       "id": 789,
#       "name": "customer"
#     },
#     {
#       "id": 790,
#       "name": "vip"
#     }
#   ]
# }
```

#### `add_tags_to_member`
Tag audience members.

**Parameters:**
- `list_id` (string, required): Audience list ID
- `email_address` (string, required): Member email
- `tags` (list, required): Tag names to add
- `is_syncing` (bool, optional): External sync flag (default: false)

**Example:**
```python
# Add tags to a member
result = await add_tags_to_member(
    list_id="abc123",
    email_address="user@example.com",
    tags=["customer", "premium", "engaged"]
)

# Tags are useful for:
# - Segmentation
# - Campaign targeting
# - Automation triggers
# - Member categorization
```

## Common Workflows

### Newsletter Signup Flow
```python
# 1. Add new subscriber
member = await add_member(
    list_id="abc123",
    email_address="new@example.com",
    status="subscribed",
    merge_fields={
        "FNAME": "Sarah",
        "LNAME": "Smith"
    },
    tags=["newsletter", "new-subscriber"]
)

# 2. Create welcome campaign
campaign = await create_campaign(
    campaign_type="regular",
    list_id="abc123",
    subject_line="Welcome to Our Newsletter!",
    from_name="Company Name",
    reply_to="hello@company.com"
)

# 3. Send campaign
await send_campaign(campaign_id=campaign["id"])
```

### Campaign Creation and Analysis
```python
# 1. Create campaign
campaign = await create_campaign(
    campaign_type="regular",
    list_id="abc123",
    subject_line="Special Offer - 20% Off",
    from_name="Company Store",
    reply_to="sales@company.com",
    title="October Sale Campaign"
)

# 2. Schedule for optimal time
await send_campaign(
    campaign_id=campaign["id"],
    schedule_time="2025-10-15T09:00:00Z"
)

# 3. After sending, check performance
report = await get_campaign_reports(campaign_id=campaign["id"])

print(f"Open Rate: {report['opens']['open_rate']}%")
print(f"Click Rate: {report['clicks']['click_rate']}%")
print(f"Unsubscribes: {report['unsubscribed']}")
```

### Segmentation for Targeted Campaigns
```python
# 1. Get audience members
members = await list_audience_members(
    list_id="abc123",
    status="subscribed"
)

# 2. Tag engaged members
for member in members["members"]:
    if member.get("stats", {}).get("avg_open_rate", 0) > 25:
        await add_tags_to_member(
            list_id="abc123",
            email_address=member["email_address"],
            tags=["engaged", "high-open-rate"]
        )

# 3. Create segment for VIP campaign
segment = await create_segment(
    list_id="abc123",
    name="Engaged Subscribers"
)
```

### Member Management
```python
# Update member status
member = await update_member(
    list_id="abc123",
    email_address="user@example.com",
    status="subscribed",
    merge_fields={
        "FNAME": "John",
        "LNAME": "Updated"
    }
)

# Add VIP status
await update_member(
    list_id="abc123",
    email_address="vip@example.com",
    vip=True
)

# Tag for specific campaign
await add_tags_to_member(
    list_id="abc123",
    email_address="user@example.com",
    tags=["product-launch-2025"]
)
```

## Best Practices

1. **Double opt-in**: Use `status="pending"` for GDPR compliance
2. **Merge fields**: Collect useful data during signup
3. **Tags**: Organize members for better segmentation
4. **Segments**: Target specific groups for campaigns
5. **VIP members**: Prioritize high-value subscribers
6. **Test campaigns**: Use A/B testing for optimization
7. **Monitor analytics**: Track open rates and click rates
8. **Clean lists**: Remove bounced emails regularly
9. **Respect unsubscribes**: Update status immediately
10. **Rate limiting**: Implement retry logic for 429 errors

## Merge Field Examples

Common merge fields for personalization:

```python
merge_fields = {
    "FNAME": "John",           # First name
    "LNAME": "Doe",            # Last name
    "PHONE": "+1-555-0123",    # Phone number
    "BIRTHDAY": "05/15",       # Birthday (MM/DD)
    "ADDRESS": {               # Address object
        "addr1": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "US"
    },
    "COMPANY": "Acme Corp",    # Company name
    "WEBSITE": "example.com"   # Website
}
```

Use merge tags in email content: `*|FNAME|*`, `*|LNAME|*`

## Campaign Performance Metrics

Key metrics to track:

- **Open Rate**: % of recipients who opened
- **Click Rate**: % of recipients who clicked
- **Bounce Rate**: Invalid/rejected emails
- **Unsubscribe Rate**: % who unsubscribed
- **Revenue**: E-commerce tracking (if enabled)
- **Industry Averages**: Compare to your industry

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid API key or wrong data center
- **400 Bad Request**: Invalid parameters or missing required fields
- **404 Not Found**: List, campaign, or member not found
- **429 Too Many Requests**: Rate limit exceeded (10 req/sec)
- **500 Internal Server Error**: Mailchimp service issue

## API Documentation

- [Mailchimp Marketing API](https://mailchimp.com/developer/marketing/api/)
- [Getting Started](https://mailchimp.com/developer/marketing/guides/quick-start/)
- [API Reference](https://mailchimp.com/developer/marketing/api/root/)
- [Merge Fields Guide](https://mailchimp.com/developer/marketing/docs/merge-fields/)
- [Segmentation](https://mailchimp.com/developer/marketing/api/list-segments/)

## Support

- [Help Center](https://mailchimp.com/help/)
- [API Support](https://mailchimp.com/contact/)
- [Developer Forums](https://stackoverflow.com/questions/tagged/mailchimp)
- [Status Page](https://status.mailchimp.com/)
