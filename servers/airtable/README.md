# Airtable MCP Server

MCP server for managing Airtable bases, tables, records, and views. Perform CRUD operations, search with formulas, and manage your Airtable data programmatically.

## Features

- **Base Management**: List and explore accessible bases
- **Schema Access**: Get table structures and field definitions
- **Record Operations**: Create, read, update, and delete records
- **Advanced Search**: Filter records using Airtable formulas
- **Bulk Operations**: Create or update up to 10 records at once
- **View Management**: List and work with table views
- **Pagination**: Handle large datasets with offset-based pagination
- **Flexible Filtering**: Sort and filter records with powerful queries

## Setup

### Prerequisites

- Airtable account
- Access token with appropriate scopes

### Environment Variables

- `AIRTABLE_ACCESS_TOKEN` (required): Your Airtable personal access token

**How to create an access token:**
1. Go to [airtable.com/create/tokens](https://airtable.com/create/tokens)
2. Click "Create new token"
3. Give your token a name (e.g., "MCP Server Access")
4. Add the required scopes:
   - `data.records:read` - Read records
   - `data.records:write` - Create, update, delete records
   - `schema.bases:read` - Read base schemas
5. Add access to specific bases or select "All current and future bases"
6. Click "Create token" and copy it immediately
7. Store it securely as `AIRTABLE_ACCESS_TOKEN`

## Available Tools

### Base Management Tools

#### `list_bases`
List all accessible Airtable bases.

**Example:**
```python
bases = await list_bases()
```

**Response includes:**
- Base IDs
- Base names
- Permission levels

#### `get_base_schema`
Get complete schema for a base including tables and fields.

**Parameters:**
- `base_id` (string, required): Base ID (e.g., 'appXXXXXXXXXXXXXX')

**Example:**
```python
schema = await get_base_schema(base_id="appAbc123")
```

**Response includes:**
- Table IDs and names
- Field definitions with types
- View information

### Record Listing & Search Tools

#### `list_records`
List records from a table with advanced filtering and sorting.

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name
- `fields` (list, optional): Specific fields to return
- `filter_by_formula` (string, optional): Airtable formula filter
- `max_records` (int, optional): Maximum records to return
- `page_size` (int, optional): Records per page (max: 100)
- `sort` (list, optional): Sort configuration
- `view` (string, optional): View name or ID
- `offset` (string, optional): Pagination offset

**Example:**
```python
# List all records
records = await list_records(
    base_id="appAbc123",
    table_id_or_name="Contacts"
)

# List with filters and sorting
records = await list_records(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    fields=["Name", "Email", "Status"],
    filter_by_formula="{Status} = 'Active'",
    sort=[{"field": "Name", "direction": "asc"}],
    max_records=50
)

# Pagination
page1 = await list_records(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    page_size=100
)
# Use offset from page1 response for next page
page2 = await list_records(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    page_size=100,
    offset=page1["offset"]
)
```

#### `search_records`
Search records using Airtable formula filters.

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name
- `formula` (string, required): Airtable formula
- `fields` (list, optional): Fields to return
- `sort` (list, optional): Sort configuration
- `max_records` (int, optional): Maximum records

**Example:**
```python
# Search with complex formula
results = await search_records(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    formula="AND({Status} = 'Active', {Age} > 25, FIND('gmail', {Email}))",
    fields=["Name", "Email", "Age"],
    sort=[{"field": "Age", "direction": "desc"}],
    max_records=20
)
```

#### `get_record`
Get a specific record by ID.

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name
- `record_id` (string, required): Record ID (e.g., 'recXXXXXXXXXXXXXX')

**Example:**
```python
record = await get_record(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    record_id="recDef456"
)
```

### Record Creation & Update Tools

#### `create_record`
Create a new record in a table.

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name
- `fields` (dict, required): Field names and values

**Example:**
```python
new_record = await create_record(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    fields={
        "Name": "John Doe",
        "Email": "john@example.com",
        "Age": 30,
        "Status": "Active"
    }
)
```

#### `update_record`
Update an existing record.

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name
- `record_id` (string, required): Record ID
- `fields` (dict, required): Fields to update
- `replace_all` (bool, optional): If True, replace all fields (PUT). If False, merge (PATCH). Default: False

**Example:**
```python
# Partial update (merge fields)
updated = await update_record(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    record_id="recDef456",
    fields={
        "Status": "Inactive",
        "Notes": "Updated status"
    },
    replace_all=False
)

# Complete replacement
replaced = await update_record(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    record_id="recDef456",
    fields={
        "Name": "Jane Smith",
        "Email": "jane@example.com",
        "Age": 28
    },
    replace_all=True
)
```

#### `delete_record`
Delete a record from a table.

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name
- `record_id` (string, required): Record ID

**Example:**
```python
result = await delete_record(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    record_id="recDef456"
)
```

### Bulk Operations Tools

#### `bulk_create_records`
Create multiple records at once (up to 10 per request).

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name
- `records` (list, required): List of record objects with fields (max: 10)

**Example:**
```python
results = await bulk_create_records(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    records=[
        {"Name": "Alice", "Email": "alice@example.com", "Age": 25},
        {"Name": "Bob", "Email": "bob@example.com", "Age": 30},
        {"Name": "Charlie", "Email": "charlie@example.com", "Age": 35}
    ]
)
```

#### `bulk_update_records`
Update multiple records at once (up to 10 per request).

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name
- `records` (list, required): List with 'id' and 'fields' (max: 10)
- `replace_all` (bool, optional): Replace all fields or merge. Default: False

**Example:**
```python
results = await bulk_update_records(
    base_id="appAbc123",
    table_id_or_name="Contacts",
    records=[
        {
            "id": "recDef456",
            "fields": {"Status": "Active"}
        },
        {
            "id": "recGhi789",
            "fields": {"Status": "Inactive"}
        }
    ],
    replace_all=False
)
```

### Schema & View Tools

#### `get_table_fields`
Get field definitions for a specific table.

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name

**Example:**
```python
fields = await get_table_fields(
    base_id="appAbc123",
    table_id_or_name="Contacts"
)
```

**Response includes:**
- Field IDs
- Field names
- Field types
- Field options

#### `list_views`
List all views in a table.

**Parameters:**
- `base_id` (string, required): Base ID
- `table_id_or_name` (string, required): Table ID or name

**Example:**
```python
views = await list_views(
    base_id="appAbc123",
    table_id_or_name="Contacts"
)
```

**Response includes:**
- View IDs
- View names
- View types (grid, form, calendar, etc.)

## Airtable Formula Syntax

Airtable uses a formula language similar to Excel for filtering and calculations.

### Basic Operators
- **Comparison**: `=`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical**: `AND()`, `OR()`, `NOT()`
- **Text**: `FIND()`, `SEARCH()`, `LEFT()`, `RIGHT()`, `MID()`, `LEN()`
- **Math**: `+`, `-`, `*`, `/`, `MOD()`, `ROUND()`
- **Date**: `TODAY()`, `NOW()`, `DATEADD()`, `DATEDIF()`, `IS_AFTER()`, `IS_BEFORE()`

### Formula Examples

**Filter by single condition:**
```python
"{Status} = 'Active'"
```

**Filter by multiple conditions:**
```python
"AND({Status} = 'Active', {Age} > 25)"
```

**Filter with OR:**
```python
"OR({Status} = 'Active', {Status} = 'Pending')"
```

**Text search:**
```python
"FIND('gmail', {Email})"  # Contains gmail
```

**Date filters:**
```python
"IS_AFTER({Created}, '2024-01-01')"
```

**Complex formula:**
```python
"AND(
    OR({Status} = 'Active', {Status} = 'Pending'),
    {Age} >= 18,
    FIND('@company.com', {Email})
)"
```

**Empty/not empty:**
```python
"{Email} != ''"  # Email is not empty
"{Phone} = ''"   # Phone is empty
```

## Sorting Records

Sort by one or more fields:

```python
# Single field
sort=[{"field": "Name", "direction": "asc"}]

# Multiple fields
sort=[
    {"field": "Status", "direction": "desc"},
    {"field": "Name", "direction": "asc"}
]
```

Directions: `asc` (ascending) or `desc` (descending)

## Field Types

Airtable supports various field types:

### Basic Types
- **Single line text**: Short text strings
- **Long text**: Multi-line text
- **Number**: Integers or decimals
- **Checkbox**: Boolean true/false
- **Date**: Date values
- **Phone number**: Phone numbers
- **Email**: Email addresses
- **URL**: Website URLs

### Selection Types
- **Single select**: Choose one option
- **Multiple select**: Choose multiple options
- **Collaborator**: Airtable users

### Advanced Types
- **Attachment**: Files and images
- **Link to another record**: Relationships
- **Lookup**: Values from linked records
- **Rollup**: Aggregations from linked records
- **Formula**: Calculated values
- **Count**: Count of linked records
- **Rating**: Star ratings
- **Barcode**: Barcode scanner
- **Button**: Action buttons

## Pagination

Airtable returns up to 100 records per request. Use pagination for more:

```python
all_records = []
offset = None

while True:
    response = await list_records(
        base_id="appAbc123",
        table_id_or_name="Contacts",
        page_size=100,
        offset=offset
    )

    all_records.extend(response["records"])

    # Check if there are more pages
    if "offset" in response:
        offset = response["offset"]
    else:
        break  # No more records
```

## Rate Limits

Airtable enforces rate limits:

- **5 requests per second per base**
- Applies to all API operations on a specific base
- Exceeding limits returns HTTP 429 error

**Best practices:**
- Implement exponential backoff for retries
- Use bulk operations when possible (10 records per request)
- Cache frequently accessed data
- Batch multiple operations together

## ID Formats

### Base ID
- Format: `app` + 14 alphanumeric characters
- Example: `appAbc123Def456Gh`

### Table ID
- Can use table ID or URL-encoded table name
- Table ID format: `tbl` + alphanumeric
- Example: `tblXyz789` or `Contacts`

### Record ID
- Format: `rec` + 14 alphanumeric characters
- Example: `recDef456Ghi789Jk`

### View ID
- Format: `viw` + alphanumeric
- Example: `viwMno012Pqr345St`

## Working with Attachments

Upload attachments as URLs:

```python
await create_record(
    base_id="appAbc123",
    table_id_or_name="Documents",
    fields={
        "Name": "My Document",
        "Files": [
            {"url": "https://example.com/file1.pdf"},
            {"url": "https://example.com/image.jpg"}
        ]
    }
)
```

## Error Handling

Common error codes:

- **401 Unauthorized**: Invalid or missing access token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Base, table, or record doesn't exist
- **422 Unprocessable**: Invalid field values or formula syntax
- **429 Too Many Requests**: Rate limit exceeded
- **503 Service Unavailable**: Airtable service issue

**Error response format:**
```json
{
  "error": {
    "type": "INVALID_REQUEST_UNKNOWN",
    "message": "Error description"
  }
}
```

## Best Practices

1. **Use bulk operations**: Create/update up to 10 records per request
2. **Cache base schemas**: Schemas don't change frequently
3. **Filter on the server**: Use formulas instead of filtering locally
4. **Limit returned fields**: Request only needed fields
5. **Handle rate limits**: Implement retry logic with backoff
6. **Use views**: Leverage Airtable views for pre-filtered data
7. **Validate data**: Check field types before creating/updating
8. **URL-encode table names**: Use proper encoding for table names with spaces

## Use Cases

- **CRM Integration**: Sync customer data with Airtable
- **Project Management**: Track tasks and milestones
- **Content Management**: Manage blog posts and media
- **Inventory Tracking**: Monitor stock levels and orders
- **Event Management**: Coordinate attendees and schedules
- **Form Processing**: Store and manage form submissions
- **Data Migration**: Import/export data programmatically
- **Automation**: Build workflows with Airtable as data store

## API Documentation

For detailed information:
- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
- [Formula Field Reference](https://support.airtable.com/docs/formula-field-reference)
- [API Authentication](https://airtable.com/developers/web/api/authentication)
- [Rate Limits](https://airtable.com/developers/web/api/rate-limits)
- [Field Types](https://airtable.com/developers/web/api/field-model)

## Security Notes

- **Never commit tokens**: Store access tokens securely
- **Scope permissions**: Grant minimum required access
- **Rotate tokens**: Regularly update access tokens
- **Use HTTPS**: All API calls use HTTPS
- **Audit access**: Review token usage regularly
- **Revoke unused tokens**: Delete tokens no longer needed

## Support

- [Airtable Community](https://community.airtable.com/)
- [Airtable Support](https://support.airtable.com/)
- [Developer Documentation](https://airtable.com/developers/web)
