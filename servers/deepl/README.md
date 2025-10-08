# DeepL MCP Server

MCP server for DeepL Translation API. Professional-grade translation for 30+ languages with superior quality, document translation support, custom glossaries, and formality control.

## Features

- **High-Quality Translation**: Superior to Google Translate in quality
- **30+ Languages**: European and Asian languages
- **Document Translation**: PDF, DOCX, PPTX, XLSX, HTML, TXT
- **Custom Glossaries**: Consistent terminology across translations
- **Formality Control**: Formal/informal tone for supported languages
- **Context-Aware**: Nuanced, natural translations
- **Tag Handling**: Preserve XML/HTML markup
- **Batch Translation**: Translate multiple texts in one request
- **Usage Tracking**: Monitor character consumption

## Setup

### Prerequisites

- DeepL account (free or Pro)
- API key

### Environment Variables

- `DEEPL_API_KEY` (required): Your DeepL API key

**How to get credentials:**
1. Go to [deepl.com/pro-api](https://www.deepl.com/pro-api)
2. Sign up for an account (Free or Pro)
3. Go to Account Settings
4. Find your API key under "Authentication Key for DeepL API"
5. Copy the key and store as `DEEPL_API_KEY`

**API Key Format:**
- Free tier keys end with `:fx` (e.g., `abc123:fx`)
- Pro keys do not have the `:fx` suffix
- The server automatically detects which endpoint to use

## Rate Limits

**Free Tier:**
- 500,000 characters per month
- Suitable for testing and small projects

**Pro Plans:**
- Unlimited characters based on plan
- Higher priority processing
- Additional features

Monitor usage with `get_usage()` tool.

## Supported Languages

**European Languages:**
- Bulgarian (BG)
- Czech (CS)
- Danish (DA)
- German (DE)
- Greek (EL)
- English (EN) - British (EN-GB), American (EN-US)
- Spanish (ES)
- Estonian (ET)
- Finnish (FI)
- French (FR)
- Hungarian (HU)
- Indonesian (ID)
- Italian (IT)
- Lithuanian (LT)
- Latvian (LV)
- Dutch (NL)
- Polish (PL)
- Portuguese (PT) - Brazilian (PT-BR), European (PT-PT)
- Romanian (RO)
- Russian (RU)
- Slovak (SK)
- Slovenian (SL)
- Swedish (SV)
- Turkish (TR)
- Ukrainian (UK)

**Asian Languages:**
- Chinese (ZH) - Simplified only
- Japanese (JA)
- Korean (KO)

## Available Tools

### Text Translation

#### `translate_text`
Translate text between languages.

**Parameters:**
- `text` (string or list, required): Text to translate
- `target_lang` (string, required): Target language code
- `source_lang` (string, optional): Source language (auto-detect if not provided)
- `formality` (string, optional): Formality level
- `preserve_formatting` (bool, optional): Preserve formatting (default: false)
- `tag_handling` (string, optional): Tag handling mode (xml, html)
- `split_sentences` (string, optional): Sentence splitting (0, 1, nonewlines)

**Formality Levels** (for DE, FR, IT, ES, NL, PL, PT-BR, PT-PT, JA, RU):
- `default`: Default formality
- `more`: More formal
- `less`: Less formal (more casual)
- `prefer_more`: Prefer formal but not guaranteed
- `prefer_less`: Prefer casual but not guaranteed

**Example:**
```python
# Simple translation
result = await translate_text(
    text="Hello, world!",
    target_lang="DE"
)

# With source language
result = await translate_text(
    text="Hello, world!",
    source_lang="EN",
    target_lang="FR"
)

# Formal translation
result = await translate_text(
    text="How are you?",
    target_lang="DE",
    formality="more"
)

# Batch translation
result = await translate_text(
    text=["Hello", "Goodbye", "Thank you"],
    target_lang="ES"
)

# HTML with tag preservation
result = await translate_text(
    text="<p>Hello <strong>world</strong>!</p>",
    target_lang="IT",
    tag_handling="html"
)

# Returns:
# {
#   "translations": [
#     {
#       "detected_source_language": "EN",
#       "text": "Hallo Welt!"
#     }
#   ]
# }
```

### Language Detection

#### `detect_language`
Detect the language of text.

**Parameters:**
- `text` (string, required): Text to analyze

**Example:**
```python
result = await detect_language(text="Bonjour le monde")

# Returns:
# {
#   "detected_language": "FR",
#   "text": "Bonjour le monde"
# }
```

#### `list_languages`
List all supported languages.

**Parameters:**
- `language_type` (string, optional): Type of languages (source or target, default: target)

**Example:**
```python
# List target languages
languages = await list_languages(language_type="target")

# List source languages
languages = await list_languages(language_type="source")

# Returns:
# {
#   "languages": [
#     {
#       "language": "DE",
#       "name": "German",
#       "supports_formality": true
#     },
#     {
#       "language": "FR",
#       "name": "French",
#       "supports_formality": true
#     }
#   ]
# }
```

### Document Translation

#### `translate_document`
Translate entire documents while preserving formatting.

**Supported Formats:**
- PDF (with and without OCR)
- Microsoft Word (DOCX)
- PowerPoint (PPTX)
- Excel (XLSX)
- HTML
- Plain text (TXT)

**Parameters:**
- `document_path` (string, required): Path or URL to document
- `target_lang` (string, required): Target language code
- `source_lang` (string, optional): Source language
- `formality` (string, optional): Formality level
- `filename` (string, optional): Original filename

**Example:**
```python
# Upload document for translation
result = await translate_document(
    document_path="/path/to/document.pdf",
    target_lang="DE",
    source_lang="EN"
)

# Returns document_id and document_key for status checking
```

#### `get_document_status`
Check document translation status.

**Parameters:**
- `document_id` (string, required): Document ID from upload
- `document_key` (string, required): Document key from upload

**Example:**
```python
status = await get_document_status(
    document_id="abc123",
    document_key="def456"
)

# Returns:
# {
#   "document_id": "abc123",
#   "status": "done",
#   "seconds_remaining": 0,
#   "billed_characters": 1234
# }
```

**Status Values:**
- `queued`: Waiting to be processed
- `translating`: Currently being translated
- `done`: Translation complete
- `error`: Translation failed

#### `download_translated_document`
Download completed document translation.

**Parameters:**
- `document_id` (string, required): Document ID
- `document_key` (string, required): Document key

**Example:**
```python
document = await download_translated_document(
    document_id="abc123",
    document_key="def456"
)

# Returns translated document data
```

### Glossaries

Custom glossaries ensure consistent translation of specific terms across all your content.

#### `list_glossaries`
List all custom glossaries.

**Example:**
```python
glossaries = await list_glossaries()

# Returns:
# {
#   "glossaries": [
#     {
#       "glossary_id": "abc123",
#       "name": "Product Terms",
#       "ready": true,
#       "source_lang": "EN",
#       "target_lang": "DE",
#       "creation_time": "2025-10-08T12:00:00",
#       "entry_count": 50
#     }
#   ]
# }
```

#### `create_glossary`
Create a custom glossary.

**Parameters:**
- `name` (string, required): Glossary name
- `source_lang` (string, required): Source language code
- `target_lang` (string, required): Target language code
- `entries` (dict, required): Source:target translation pairs
- `entries_format` (string, optional): Format (tsv or csv, default: tsv)

**Example:**
```python
# Create product terminology glossary
glossary = await create_glossary(
    name="Product Terms",
    source_lang="EN",
    target_lang="DE",
    entries={
        "smartphone": "Smartphone",
        "tablet": "Tablet-PC",
        "app": "App",
        "cloud": "Cloud"
    }
)

# Returns:
# {
#   "glossary_id": "abc123",
#   "name": "Product Terms",
#   "ready": true,
#   "source_lang": "EN",
#   "target_lang": "DE",
#   "creation_time": "2025-10-08T12:00:00",
#   "entry_count": 4
# }
```

#### `get_glossary`
Get glossary details.

**Parameters:**
- `glossary_id` (string, required): Glossary ID

**Example:**
```python
glossary = await get_glossary(glossary_id="abc123")
```

#### `delete_glossary`
Delete a glossary.

**Parameters:**
- `glossary_id` (string, required): Glossary ID

**Example:**
```python
result = await delete_glossary(glossary_id="abc123")
```

#### `translate_with_glossary`
Translate using a custom glossary.

**Parameters:**
- `text` (string or list, required): Text to translate
- `target_lang` (string, required): Target language code
- `glossary_id` (string, required): Glossary ID
- `source_lang` (string, optional): Source language
- `formality` (string, optional): Formality level

**Example:**
```python
result = await translate_with_glossary(
    text="Our new smartphone app uses the cloud",
    target_lang="DE",
    glossary_id="abc123"
)

# Ensures consistent translation of terms from glossary
```

### Usage Tracking

#### `get_usage`
Get API usage statistics.

**Example:**
```python
usage = await get_usage()

# Returns:
# {
#   "character_count": 123456,
#   "character_limit": 500000,
#   "document_count": 5,
#   "document_limit": 10,
#   "team_document_count": 5,
#   "team_document_limit": 10
# }
```

## Common Workflows

### Website Localization
```python
# Translate web page content
html_content = """
<div>
    <h1>Welcome to our site</h1>
    <p>We offer <strong>quality products</strong></p>
</div>
"""

result = await translate_text(
    text=html_content,
    target_lang="DE",
    tag_handling="html",
    preserve_formatting=True
)

# Preserve HTML structure while translating content
```

### Document Translation Workflow
```python
# 1. Upload document
upload = await translate_document(
    document_path="report.pdf",
    target_lang="FR",
    source_lang="EN",
    formality="more"
)

# 2. Check status
status = await get_document_status(
    document_id=upload["document_id"],
    document_key=upload["document_key"]
)

# 3. Download when ready
if status["status"] == "done":
    document = await download_translated_document(
        document_id=upload["document_id"],
        document_key=upload["document_key"]
    )
```

### Product Catalog Translation
```python
# 1. Create glossary for brand terms
glossary = await create_glossary(
    name="Brand Terms",
    source_lang="EN",
    target_lang="ES",
    entries={
        "Premium Edition": "Edición Premium",
        "Pro Version": "Versión Pro",
        "Basic Plan": "Plan Básico"
    }
)

# 2. Translate product descriptions
products = [
    "Premium Edition includes all features",
    "Pro Version for professionals",
    "Basic Plan for individuals"
]

for product in products:
    result = await translate_with_glossary(
        text=product,
        target_lang="ES",
        glossary_id=glossary["glossary_id"]
    )
    print(result["translations"][0]["text"])
```

### Customer Support Translation
```python
# Detect customer's language
message = "¿Cómo puedo devolver mi pedido?"
detection = await detect_language(text=message)

# Translate to English for support team
translation = await translate_text(
    text=message,
    source_lang=detection["detected_language"],
    target_lang="EN"
)

# Reply in customer's language
reply = await translate_text(
    text="You can return your order within 30 days",
    target_lang=detection["detected_language"],
    formality="more"  # Polite tone
)
```

## Best Practices

1. **Use source language**: Specify when known for better accuracy
2. **Leverage glossaries**: Ensure consistent terminology
3. **Choose formality**: Match your audience and context
4. **Batch translations**: More efficient for multiple texts
5. **Preserve formatting**: Use tag_handling for markup
6. **Monitor usage**: Track character consumption
7. **Cache translations**: Avoid re-translating same content
8. **Test formality**: Different levels for different audiences
9. **Handle errors**: Implement retry logic
10. **Document format**: Use appropriate format for documents

## Formality Examples

**German (DE):**
```python
# Casual
await translate_text("How are you?", target_lang="DE", formality="less")
# → "Wie geht's?"

# Formal
await translate_text("How are you?", target_lang="DE", formality="more")
# → "Wie geht es Ihnen?"
```

**French (FR):**
```python
# Casual (tu form)
await translate_text("How are you?", target_lang="FR", formality="less")
# → "Comment vas-tu?"

# Formal (vous form)
await translate_text("How are you?", target_lang="FR", formality="more")
# → "Comment allez-vous?"
```

## Tag Handling

Preserve markup in translations:

```python
# XML tags
await translate_text(
    text="<note>This is important</note>",
    target_lang="DE",
    tag_handling="xml"
)

# HTML tags
await translate_text(
    text="<p>Visit our <a href='#'>website</a></p>",
    target_lang="FR",
    tag_handling="html"
)
```

## Error Handling

Common errors:

- **403 Forbidden**: Invalid API key
- **456 Quota Exceeded**: Character limit reached
- **400 Bad Request**: Invalid parameters
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **503 Service Unavailable**: Server temporarily unavailable

## API Documentation

- [DeepL API Documentation](https://www.deepl.com/docs-api)
- [Text Translation](https://www.deepl.com/docs-api/translate-text/)
- [Document Translation](https://www.deepl.com/docs-api/translate-documents/)
- [Glossaries](https://www.deepl.com/docs-api/glossaries/)
- [Language Codes](https://www.deepl.com/docs-api/translate-text/request/)

## Support

- [Help Center](https://support.deepl.com/)
- [Contact Support](https://www.deepl.com/contact)
- [API Status](https://status.deepl.com/)
- [Developer Forum](https://forum.deepl.com/)
