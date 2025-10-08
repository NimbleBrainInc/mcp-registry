# PDF.co MCP Server

MCP server for PDF.co API. Comprehensive PDF manipulation, conversion, OCR, text extraction, and document automation with support for barcodes, watermarks, and security features.

## Features

- **Text Extraction**: Extract text from PDFs
- **Format Conversion**: PDF ↔ HTML, images, CSV
- **OCR**: Optical Character Recognition for scanned documents
- **Merging & Splitting**: Combine or separate PDFs
- **Watermarking**: Add text or image watermarks
- **Security**: Password protection and removal
- **Compression**: Reduce PDF file sizes
- **Table Extraction**: Extract tables to structured CSV
- **Barcode Operations**: Generate and read barcodes
- **Web to PDF**: Convert URLs to PDF documents

## Setup

### Prerequisites

- PDF.co account (free or paid)
- API key

### Environment Variables

- `PDFCO_API_KEY` (required): Your PDF.co API key

**How to get credentials:**
1. Go to [pdf.co](https://pdf.co/)
2. Sign up or log in
3. Go to Dashboard (app.pdf.co/dashboard)
4. Find your API key in the API section
5. Copy the key and store as `PDFCO_API_KEY`

Direct link: https://app.pdf.co/dashboard

## Rate Limits

- **Free Tier**: 150 requests per month
- **Paid Plans**: Unlimited requests based on plan
- Monitor usage in dashboard
- Consider caching results for frequently accessed documents

## Input Formats

PDF.co supports multiple input methods:

1. **Public URL**: Direct link to a PDF or image
2. **Base64**: Base64-encoded file content
3. **Temporary Storage**: Upload to PDF.co temp storage first

## Available Tools

### Text Extraction

#### `pdf_to_text`
Extract text from PDF.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `pages` (string, optional): Page range (e.g., "1-3" or "1,3,5")
- `async_mode` (bool, optional): Async processing (default: false)

**Example:**
```python
# Extract all text
result = await pdf_to_text(
    url="https://example.com/document.pdf"
)

# Extract specific pages
result = await pdf_to_text(
    url="https://example.com/document.pdf",
    pages="1-5"
)

# Async for large files
result = await pdf_to_text(
    url="https://example.com/large.pdf",
    async_mode=True
)
# Check job status with returned job ID
```

#### `pdf_to_json`
Extract structured data from PDF.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `pages` (string, optional): Page range

**Example:**
```python
result = await pdf_to_json(
    url="https://example.com/invoice.pdf"
)

# Returns structured JSON with:
# - Text content
# - Positioning information
# - Formatting details
```

### Format Conversion

#### `pdf_to_html`
Convert PDF to HTML.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `pages` (string, optional): Page range
- `simple` (bool, optional): Simple HTML mode (default: false)

**Example:**
```python
# Full HTML with formatting
result = await pdf_to_html(
    url="https://example.com/report.pdf"
)

# Simple HTML without complex formatting
result = await pdf_to_html(
    url="https://example.com/report.pdf",
    simple=True
)
```

#### `html_to_pdf`
Convert HTML to PDF.

**Parameters:**
- `html` (string, required): HTML content or URL
- `name` (string, optional): Output filename (default: document.pdf)
- `margins` (string, optional): Margins "top,right,bottom,left"
- `orientation` (string, optional): Portrait or Landscape (default: Portrait)
- `page_size` (string, optional): Letter, A4, Legal, etc. (default: Letter)

**Page Sizes:**
- Letter (8.5 x 11 inches)
- Legal (8.5 x 14 inches)
- A4 (210 x 297 mm)
- A3 (297 x 420 mm)

**Example:**
```python
# From HTML string
result = await html_to_pdf(
    html="<html><body><h1>Invoice</h1><p>Total: $100</p></body></html>",
    name="invoice.pdf",
    page_size="Letter",
    orientation="Portrait"
)

# From URL
result = await html_to_pdf(
    html="https://example.com/report.html",
    margins="10mm,10mm,10mm,10mm"
)
```

#### `url_to_pdf`
Convert web page URL to PDF.

**Parameters:**
- `url` (string, required): Web page URL
- `name` (string, optional): Output filename (default: webpage.pdf)
- `orientation` (string, optional): Portrait or Landscape
- `page_size` (string, optional): Letter, A4, Legal, etc.

**Example:**
```python
result = await url_to_pdf(
    url="https://example.com/article",
    name="article.pdf",
    page_size="A4"
)

# Useful for:
# - Archiving web pages
# - Generating reports from dashboards
# - Saving online content
```

#### `image_to_pdf`
Convert images to PDF.

**Parameters:**
- `images` (list, required): List of image URLs or base64
- `name` (string, optional): Output filename (default: images.pdf)

**Example:**
```python
# Multiple images to single PDF
result = await image_to_pdf(
    images=[
        "https://example.com/page1.jpg",
        "https://example.com/page2.jpg",
        "https://example.com/page3.jpg"
    ],
    name="scanned-doc.pdf"
)

# Each image becomes a page
```

### Table Extraction

#### `pdf_to_csv`
Extract tables from PDF to CSV.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `pages` (string, optional): Page range

**Example:**
```python
result = await pdf_to_csv(
    url="https://example.com/financial-report.pdf",
    pages="1-10"
)

# Returns CSV with table data
# Preserves:
# - Column structure
# - Row alignment
# - Cell values
```

### PDF Manipulation

#### `pdf_merge`
Merge multiple PDFs into one.

**Parameters:**
- `urls` (list, required): List of PDF URLs or base64
- `name` (string, optional): Output filename (default: merged.pdf)
- `async_mode` (bool, optional): Async processing (default: false)

**Example:**
```python
result = await pdf_merge(
    urls=[
        "https://example.com/part1.pdf",
        "https://example.com/part2.pdf",
        "https://example.com/part3.pdf"
    ],
    name="complete-document.pdf"
)

# Useful for:
# - Combining reports
# - Merging invoices
# - Creating compilations
```

#### `pdf_split`
Split PDF into separate pages or ranges.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `pages` (string, optional): Page ranges (e.g., "1-3,5-7")
- `split_by_pages` (bool, optional): Split into individual pages (default: false)

**Example:**
```python
# Extract specific pages
result = await pdf_split(
    url="https://example.com/document.pdf",
    pages="1-3,10-12"
)

# Split into individual pages
result = await pdf_split(
    url="https://example.com/document.pdf",
    split_by_pages=True
)
```

#### `pdf_rotate`
Rotate PDF pages.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `angle` (int, required): Rotation angle (90, 180, 270, -90)
- `pages` (string, optional): Page range

**Example:**
```python
# Rotate all pages
result = await pdf_rotate(
    url="https://example.com/sideways.pdf",
    angle=90
)

# Rotate specific pages
result = await pdf_rotate(
    url="https://example.com/mixed.pdf",
    angle=180,
    pages="2,4,6"
)
```

### Information & Metadata

#### `pdf_info`
Get PDF metadata (pages, size, etc.).

**Parameters:**
- `url` (string, required): PDF URL or base64

**Example:**
```python
info = await pdf_info(url="https://example.com/document.pdf")

# Returns:
# {
#   "pageCount": 25,
#   "info": {
#     "Title": "Annual Report",
#     "Author": "Company Name",
#     "CreationDate": "2025-01-01",
#     "Producer": "Adobe PDF",
#     "fileSize": 1024000
#   }
# }
```

### Watermarking

#### `pdf_add_watermark`
Add text watermark to PDF.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `text` (string, required): Watermark text
- `x` (int, optional): X position (default: 100)
- `y` (int, optional): Y position (default: 100)
- `font_size` (int, optional): Font size (default: 24)
- `color` (string, optional): Hex color without # (default: FF0000)
- `opacity` (float, optional): Opacity 0.0-1.0 (default: 0.5)

**Example:**
```python
# Add "CONFIDENTIAL" watermark
result = await pdf_add_watermark(
    url="https://example.com/document.pdf",
    text="CONFIDENTIAL",
    x=200,
    y=400,
    font_size=48,
    color="FF0000",
    opacity=0.3
)

# Add "DRAFT" watermark
result = await pdf_add_watermark(
    url="https://example.com/draft.pdf",
    text="DRAFT",
    font_size=72,
    color="808080",
    opacity=0.5
)
```

### Compression

#### `pdf_compress`
Compress PDF file size.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `compression_level` (string, optional): low, balanced, high, extreme (default: balanced)

**Compression Levels:**
- **low**: Minimal compression, best quality
- **balanced**: Good balance of size and quality
- **high**: Aggressive compression, smaller files
- **extreme**: Maximum compression, may reduce quality

**Example:**
```python
# Balanced compression
result = await pdf_compress(
    url="https://example.com/large.pdf",
    compression_level="balanced"
)

# Extreme compression for email
result = await pdf_compress(
    url="https://example.com/photos.pdf",
    compression_level="extreme"
)

# Typical size reductions:
# - low: 10-20%
# - balanced: 30-50%
# - high: 50-70%
# - extreme: 70-90%
```

### Security

#### `pdf_protect`
Add password protection to PDF.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `owner_password` (string, required): Owner password (full access)
- `user_password` (string, optional): User password (restricted access)
- `allow_print` (bool, optional): Allow printing (default: true)
- `allow_copy` (bool, optional): Allow copying text (default: false)

**Example:**
```python
# Protect with owner password
result = await pdf_protect(
    url="https://example.com/sensitive.pdf",
    owner_password="admin123",
    user_password="user123",
    allow_print=True,
    allow_copy=False
)

# Owner password: Full permissions
# User password: View-only or restricted permissions
```

#### `pdf_unlock`
Remove password from PDF.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `password` (string, required): PDF password

**Example:**
```python
result = await pdf_unlock(
    url="https://example.com/protected.pdf",
    password="secret123"
)
```

### OCR

#### `ocr_pdf`
OCR scanned PDFs to searchable text.

**Parameters:**
- `url` (string, required): PDF URL or base64
- `pages` (string, optional): Page range
- `lang` (string, optional): Language code (default: eng)

**Supported Languages:**
- eng: English
- spa: Spanish
- fra: French
- deu: German
- ita: Italian
- por: Portuguese
- rus: Russian
- chi_sim: Chinese Simplified
- jpn: Japanese
- kor: Korean

**Example:**
```python
# OCR scanned document
result = await ocr_pdf(
    url="https://example.com/scanned-invoice.pdf",
    lang="eng"
)

# OCR specific pages
result = await ocr_pdf(
    url="https://example.com/mixed.pdf",
    pages="1-5",
    lang="eng"
)

# Useful for:
# - Scanned invoices
# - Old documents
# - Faxes
# - Screenshots
```

### Barcode Operations

#### `barcode_generate`
Generate barcode images.

**Parameters:**
- `value` (string, required): Barcode value/text
- `barcode_type` (string, optional): Barcode type (default: QRCode)
- `format` (string, optional): png, jpg, svg (default: png)

**Barcode Types:**
- **QRCode**: 2D QR codes
- **Code128**: Common 1D barcode
- **Code39**: Alphanumeric barcode
- **EAN13**: 13-digit product barcode
- **EAN8**: 8-digit product barcode
- **UPC-A**: 12-digit product barcode
- **ITF**: Interleaved 2 of 5
- **Codabar**: Numeric with special chars

**Example:**
```python
# Generate QR code
result = await barcode_generate(
    value="https://example.com/product/12345",
    barcode_type="QRCode",
    format="png"
)

# Generate product barcode
result = await barcode_generate(
    value="012345678905",
    barcode_type="EAN13",
    format="png"
)

# Generate Code128
result = await barcode_generate(
    value="ABC-123-XYZ",
    barcode_type="Code128"
)
```

#### `barcode_read`
Read barcodes from images.

**Parameters:**
- `url` (string, required): Image URL or base64
- `barcode_types` (list, optional): Types to detect

**Example:**
```python
# Auto-detect all barcode types
result = await barcode_read(
    url="https://example.com/product-image.jpg"
)

# Detect specific types only
result = await barcode_read(
    url="https://example.com/qr-code.png",
    barcode_types=["QRCode", "Code128"]
)

# Returns:
# {
#   "barcodes": [
#     {
#       "type": "QRCode",
#       "value": "https://example.com/product",
#       "position": {...}
#     }
#   ]
# }
```

## Common Workflows

### Invoice Text Extraction
```python
# 1. Extract text from invoice
text_result = await pdf_to_text(
    url="https://example.com/invoice.pdf"
)

# 2. Extract tables for line items
csv_result = await pdf_to_csv(
    url="https://example.com/invoice.pdf"
)

# 3. Process extracted data
invoice_text = text_result["body"]
table_data = csv_result["body"]

# Parse amounts, dates, etc.
```

### Document Archival
```python
# 1. Compress for storage
compressed = await pdf_compress(
    url="https://example.com/document.pdf",
    compression_level="high"
)

# 2. Add password protection
protected = await pdf_protect(
    url=compressed["url"],
    owner_password="archive2025",
    allow_print=True,
    allow_copy=False
)

# 3. Add watermark
archived = await pdf_add_watermark(
    url=protected["url"],
    text="ARCHIVED 2025",
    opacity=0.2
)
```

### Receipt OCR and Parsing
```python
# 1. OCR scanned receipt
ocr_result = await ocr_pdf(
    url="https://example.com/receipt-scan.pdf",
    lang="eng"
)

# 2. Extract text
text = ocr_result["body"]

# 3. Parse for:
# - Total amount
# - Date
# - Vendor name
# - Line items
```

### Report Generation
```python
# 1. Convert HTML template to PDF
report = await html_to_pdf(
    html=f"""
    <html>
    <body>
        <h1>Monthly Report</h1>
        <p>Generated: {date}</p>
        <table>...</table>
    </body>
    </html>
    """,
    page_size="Letter"
)

# 2. Add watermark
watermarked = await pdf_add_watermark(
    url=report["url"],
    text="CONFIDENTIAL"
)
```

### Contract Merging
```python
# 1. Merge contract sections
merged = await pdf_merge(
    urls=[
        "https://example.com/contract-cover.pdf",
        "https://example.com/terms.pdf",
        "https://example.com/signature-page.pdf"
    ],
    name="complete-contract.pdf"
)

# 2. Add password protection
protected = await pdf_protect(
    url=merged["url"],
    owner_password="legal2025",
    user_password="client123"
)
```

## Best Practices

1. **Use async for large files**: Enable async mode for PDFs over 10MB
2. **Specify page ranges**: Extract only needed pages to save time
3. **Choose compression wisely**: Balance quality and file size
4. **Cache results**: Store processed files to avoid repeated operations
5. **Use OCR selectively**: Only OCR scanned documents (check with pdf_info first)
6. **Validate barcodes**: Check barcode format before generation
7. **Secure sensitive documents**: Use password protection
8. **Monitor usage**: Track API calls in dashboard
9. **Handle timeouts**: Use appropriate timeout values for large operations
10. **Test watermark positioning**: Preview watermark placement

## Error Handling

Common errors:

- **401 Unauthorized**: Invalid API key
- **402 Payment Required**: Quota exceeded (free tier limit)
- **400 Bad Request**: Invalid parameters or file format
- **404 Not Found**: URL not accessible
- **500 Internal Server Error**: Processing error
- **Timeout**: File too large, use async mode

## Async Processing

For large files or batch operations:

```python
# Start async job
result = await pdf_to_text(
    url="https://example.com/large.pdf",
    async_mode=True
)

job_id = result["jobId"]

# Check status (implement polling)
# GET /v1/job/check/{job_id}
```

## API Documentation

- [PDF.co Documentation](https://apidocs.pdf.co/)
- [PDF Operations](https://apidocs.pdf.co/02-pdf-to-text)
- [Conversion APIs](https://apidocs.pdf.co/07-html-to-pdf)
- [OCR API](https://apidocs.pdf.co/12-pdf-ocr)
- [Barcode API](https://apidocs.pdf.co/24-barcode-generate)

## Support

- [Help Center](https://pdf.co/support)
- [API Documentation](https://apidocs.pdf.co/)
- [Contact Support](https://pdf.co/contact)
- [Status Page](https://status.pdf.co/)
