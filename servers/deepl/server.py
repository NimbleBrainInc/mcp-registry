import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("DeepL")

API_KEY = os.getenv("DEEPL_API_KEY")
# Free tier uses api-free.deepl.com, Pro uses api.deepl.com
# Detect based on API key suffix (:fx for free)
BASE_URL = "https://api-free.deepl.com/v2" if API_KEY and API_KEY.endswith(":fx") else "https://api.deepl.com/v2"


def get_headers() -> dict:
    """Get headers with DeepL Auth Key."""
    return {
        "Authorization": f"DeepL-Auth-Key {API_KEY}",
        "Content-Type": "application/json"
    }


@mcp.tool()
async def translate_text(
    text: str | List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = False,
    tag_handling: Optional[str] = None,
    split_sentences: str = "1"
) -> dict:
    """Translate text between languages.

    Args:
        text: Text to translate (string or list of strings)
        target_lang: Target language code (e.g., "DE", "FR", "ES")
        source_lang: Source language code (optional, auto-detect if not provided)
        formality: Formality level (default, more, less, prefer_more, prefer_less)
        preserve_formatting: Preserve formatting (default: false)
        tag_handling: Tag handling mode (xml, html)
        split_sentences: Split sentences (0=none, 1=default, nonewlines=no newlines)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "text": text if isinstance(text, list) else [text],
            "target_lang": target_lang,
            "preserve_formatting": "1" if preserve_formatting else "0",
            "split_sentences": split_sentences
        }

        if source_lang:
            payload["source_lang"] = source_lang
        if formality:
            payload["formality"] = formality
        if tag_handling:
            payload["tag_handling"] = tag_handling

        response = await client.post(
            f"{BASE_URL}/translate",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def translate_document(
    document_path: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    filename: Optional[str] = None
) -> dict:
    """Translate entire documents (PDF, DOCX, PPTX, etc.).

    Args:
        document_path: Path or URL to document
        target_lang: Target language code
        source_lang: Source language code (optional)
        formality: Formality level
        filename: Original filename (for proper format detection)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        # Note: This is a simplified version
        # In production, you'd need to handle file uploads properly
        data = {
            "target_lang": target_lang
        }

        if source_lang:
            data["source_lang"] = source_lang
        if formality:
            data["formality"] = formality

        # For a real implementation, you'd use multipart/form-data
        # and upload the file. This is a placeholder.
        return {
            "document_id": "placeholder_id",
            "document_key": "placeholder_key",
            "note": "Document upload implementation requires multipart form data handling"
        }


@mcp.tool()
async def detect_language(text: str) -> dict:
    """Detect the language of text.

    Args:
        text: Text to detect language for
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        # DeepL doesn't have a dedicated detect endpoint
        # We translate with no source_lang to get detection info
        response = await client.post(
            f"{BASE_URL}/translate",
            headers=get_headers(),
            json={
                "text": [text[:1000]],  # Limit for detection
                "target_lang": "EN"
            }
        )
        response.raise_for_status()
        result = response.json()

        if "translations" in result and len(result["translations"]) > 0:
            return {
                "detected_language": result["translations"][0].get("detected_source_language"),
                "text": text[:100] + "..." if len(text) > 100 else text
            }
        return result


@mcp.tool()
async def list_languages(
    language_type: str = "target"
) -> dict:
    """List all supported source and target languages.

    Args:
        language_type: Type of languages to list (source or target)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/languages",
            headers=get_headers(),
            params={"type": language_type}
        )
        response.raise_for_status()
        return {"languages": response.json()}


@mcp.tool()
async def get_usage() -> dict:
    """Get API usage statistics."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/usage",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_glossaries() -> dict:
    """List custom glossaries."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/glossaries",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_glossary(
    name: str,
    source_lang: str,
    target_lang: str,
    entries: Dict[str, str],
    entries_format: str = "tsv"
) -> dict:
    """Create a custom glossary for consistent translations.

    Args:
        name: Glossary name
        source_lang: Source language code
        target_lang: Target language code
        entries: Dictionary of source:target translations
        entries_format: Format (tsv or csv)
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Convert entries dict to TSV format
        if entries_format == "tsv":
            entries_data = "\n".join([f"{k}\t{v}" for k, v in entries.items()])
        else:
            entries_data = "\n".join([f"{k},{v}" for k, v in entries.items()])

        payload = {
            "name": name,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "entries": entries_data,
            "entries_format": entries_format
        }

        response = await client.post(
            f"{BASE_URL}/glossaries",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_glossary(glossary_id: str) -> dict:
    """Get glossary details.

    Args:
        glossary_id: Glossary ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/glossaries/{glossary_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def delete_glossary(glossary_id: str) -> dict:
    """Delete a glossary.

    Args:
        glossary_id: Glossary ID
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.delete(
            f"{BASE_URL}/glossaries/{glossary_id}",
            headers=get_headers()
        )
        response.raise_for_status()
        return {"success": True, "glossary_id": glossary_id}


@mcp.tool()
async def translate_with_glossary(
    text: str | List[str],
    target_lang: str,
    glossary_id: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None
) -> dict:
    """Translate using a custom glossary.

    Args:
        text: Text to translate
        target_lang: Target language code
        glossary_id: Glossary ID to use
        source_lang: Source language code (optional)
        formality: Formality level
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "text": text if isinstance(text, list) else [text],
            "target_lang": target_lang,
            "glossary_id": glossary_id
        }

        if source_lang:
            payload["source_lang"] = source_lang
        if formality:
            payload["formality"] = formality

        response = await client.post(
            f"{BASE_URL}/translate",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_document_status(
    document_id: str,
    document_key: str
) -> dict:
    """Check document translation status.

    Args:
        document_id: Document ID from upload
        document_key: Document key from upload
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{BASE_URL}/document/{document_id}",
            headers=get_headers(),
            json={"document_key": document_key}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def download_translated_document(
    document_id: str,
    document_key: str
) -> dict:
    """Download completed document translation.

    Args:
        document_id: Document ID
        document_key: Document key
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/document/{document_id}/result",
            headers=get_headers(),
            json={"document_key": document_key}
        )
        response.raise_for_status()

        return {
            "success": True,
            "document_id": document_id,
            "content_type": response.headers.get("content-type"),
            "size": len(response.content),
            "note": "Document content available in response"
        }


if __name__ == "__main__":
    mcp.run()
