import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

mcp = FastMCP("PDFco")

API_KEY = os.getenv("PDFCO_API_KEY")
BASE_URL = "https://api.pdf.co/v1"


def get_headers() -> dict:
    """Get headers with API key authentication."""
    return {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }


@mcp.tool()
async def pdf_to_text(
    url: str,
    pages: Optional[str] = None,
    async_mode: bool = False
) -> dict:
    """Extract text from PDF.

    Args:
        url: URL or base64 encoded PDF
        pages: Page range (e.g., "1-3" or "1,3,5")
        async_mode: Process asynchronously (default: false)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": url,
            "async": async_mode
        }
        if pages:
            payload["pages"] = pages

        response = await client.post(
            f"{BASE_URL}/pdf/convert/to/text",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_to_json(
    url: str,
    pages: Optional[str] = None
) -> dict:
    """Extract structured data from PDF.

    Args:
        url: URL or base64 encoded PDF
        pages: Page range (e.g., "1-3")
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {"url": url}
        if pages:
            payload["pages"] = pages

        response = await client.post(
            f"{BASE_URL}/pdf/convert/to/json",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_to_html(
    url: str,
    pages: Optional[str] = None,
    simple: bool = False
) -> dict:
    """Convert PDF to HTML.

    Args:
        url: URL or base64 encoded PDF
        pages: Page range (e.g., "1-3")
        simple: Use simple HTML mode (default: false)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": url,
            "simple": simple
        }
        if pages:
            payload["pages"] = pages

        response = await client.post(
            f"{BASE_URL}/pdf/convert/to/html",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_to_csv(
    url: str,
    pages: Optional[str] = None
) -> dict:
    """Extract tables from PDF to CSV.

    Args:
        url: URL or base64 encoded PDF
        pages: Page range (e.g., "1-3")
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {"url": url}
        if pages:
            payload["pages"] = pages

        response = await client.post(
            f"{BASE_URL}/pdf/convert/to/csv",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_merge(
    urls: List[str],
    name: str = "merged.pdf",
    async_mode: bool = False
) -> dict:
    """Merge multiple PDFs into one.

    Args:
        urls: List of PDF URLs or base64 encoded PDFs
        name: Output filename (default: merged.pdf)
        async_mode: Process asynchronously (default: false)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": ",".join(urls),
            "name": name,
            "async": async_mode
        }

        response = await client.post(
            f"{BASE_URL}/pdf/merge",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_split(
    url: str,
    pages: Optional[str] = None,
    split_by_pages: bool = False
) -> dict:
    """Split PDF into separate pages or ranges.

    Args:
        url: URL or base64 encoded PDF
        pages: Page ranges to extract (e.g., "1-3,5-7")
        split_by_pages: Split into individual pages (default: false)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {"url": url}
        if pages:
            payload["pages"] = pages
        if split_by_pages:
            payload["splitByPages"] = True

        response = await client.post(
            f"{BASE_URL}/pdf/split",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_info(url: str) -> dict:
    """Get PDF metadata (pages, size, etc.).

    Args:
        url: URL or base64 encoded PDF
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"url": url}

        response = await client.post(
            f"{BASE_URL}/pdf/info",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def html_to_pdf(
    html: str,
    name: str = "document.pdf",
    margins: Optional[str] = None,
    orientation: str = "Portrait",
    page_size: str = "Letter"
) -> dict:
    """Convert HTML to PDF.

    Args:
        html: HTML content or URL
        name: Output filename (default: document.pdf)
        margins: Margins in format "top,right,bottom,left" (e.g., "10mm,10mm,10mm,10mm")
        orientation: Portrait or Landscape (default: Portrait)
        page_size: Letter, A4, Legal, etc. (default: Letter)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "html": html,
            "name": name,
            "orientation": orientation,
            "pageSize": page_size
        }
        if margins:
            payload["margins"] = margins

        response = await client.post(
            f"{BASE_URL}/pdf/convert/from/html",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def url_to_pdf(
    url: str,
    name: str = "webpage.pdf",
    orientation: str = "Portrait",
    page_size: str = "Letter"
) -> dict:
    """Convert web page URL to PDF.

    Args:
        url: Web page URL
        name: Output filename (default: webpage.pdf)
        orientation: Portrait or Landscape (default: Portrait)
        page_size: Letter, A4, Legal, etc. (default: Letter)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": url,
            "name": name,
            "orientation": orientation,
            "pageSize": page_size
        }

        response = await client.post(
            f"{BASE_URL}/pdf/convert/from/url",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def image_to_pdf(
    images: List[str],
    name: str = "images.pdf"
) -> dict:
    """Convert images to PDF.

    Args:
        images: List of image URLs or base64 encoded images
        name: Output filename (default: images.pdf)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": ",".join(images),
            "name": name
        }

        response = await client.post(
            f"{BASE_URL}/pdf/convert/from/image",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_add_watermark(
    url: str,
    text: str,
    x: int = 100,
    y: int = 100,
    font_size: int = 24,
    color: str = "FF0000",
    opacity: float = 0.5
) -> dict:
    """Add text watermark to PDF.

    Args:
        url: URL or base64 encoded PDF
        text: Watermark text
        x: X position (default: 100)
        y: Y position (default: 100)
        font_size: Font size (default: 24)
        color: Hex color without # (default: FF0000 red)
        opacity: Opacity 0.0-1.0 (default: 0.5)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": url,
            "text": text,
            "x": x,
            "y": y,
            "fontSize": font_size,
            "color": color,
            "opacity": opacity
        }

        response = await client.post(
            f"{BASE_URL}/pdf/edit/add-text",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_rotate(
    url: str,
    angle: int,
    pages: Optional[str] = None
) -> dict:
    """Rotate PDF pages.

    Args:
        url: URL or base64 encoded PDF
        angle: Rotation angle (90, 180, 270, -90)
        pages: Page range (e.g., "1-3")
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": url,
            "angle": angle
        }
        if pages:
            payload["pages"] = pages

        response = await client.post(
            f"{BASE_URL}/pdf/edit/rotate",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_compress(
    url: str,
    compression_level: str = "balanced"
) -> dict:
    """Compress PDF file size.

    Args:
        url: URL or base64 encoded PDF
        compression_level: low, balanced, high, extreme (default: balanced)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": url,
            "compressionLevel": compression_level
        }

        response = await client.post(
            f"{BASE_URL}/pdf/optimize",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_protect(
    url: str,
    owner_password: str,
    user_password: Optional[str] = None,
    allow_print: bool = True,
    allow_copy: bool = False
) -> dict:
    """Add password protection to PDF.

    Args:
        url: URL or base64 encoded PDF
        owner_password: Owner password for full access
        user_password: User password for restricted access (optional)
        allow_print: Allow printing (default: true)
        allow_copy: Allow copying text (default: false)
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": url,
            "ownerPassword": owner_password,
            "allowPrint": allow_print,
            "allowCopy": allow_copy
        }
        if user_password:
            payload["userPassword"] = user_password

        response = await client.post(
            f"{BASE_URL}/pdf/security/add",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def pdf_unlock(
    url: str,
    password: str
) -> dict:
    """Remove password from PDF.

    Args:
        url: URL or base64 encoded PDF
        password: PDF password
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "url": url,
            "password": password
        }

        response = await client.post(
            f"{BASE_URL}/pdf/security/remove",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def barcode_generate(
    value: str,
    barcode_type: str = "QRCode",
    format: str = "png"
) -> dict:
    """Generate barcode images.

    Args:
        value: Barcode value/text
        barcode_type: QRCode, Code128, Code39, EAN13, etc. (default: QRCode)
        format: png, jpg, svg (default: png)
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "value": value,
            "type": barcode_type,
            "format": format
        }

        response = await client.post(
            f"{BASE_URL}/barcode/generate",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def barcode_read(
    url: str,
    barcode_types: Optional[List[str]] = None
) -> dict:
    """Read barcodes from images.

    Args:
        url: Image URL or base64 encoded image
        barcode_types: List of barcode types to detect (QRCode, Code128, etc.)
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {"url": url}
        if barcode_types:
            payload["types"] = ",".join(barcode_types)

        response = await client.post(
            f"{BASE_URL}/barcode/read/from/url",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def ocr_pdf(
    url: str,
    pages: Optional[str] = None,
    lang: str = "eng"
) -> dict:
    """OCR scanned PDFs to searchable text.

    Args:
        url: URL or base64 encoded PDF
        pages: Page range (e.g., "1-3")
        lang: Language code (eng, spa, fra, deu, etc.) (default: eng)
    """
    async with httpx.AsyncClient(timeout=180.0) as client:
        payload = {
            "url": url,
            "lang": lang
        }
        if pages:
            payload["pages"] = pages

        response = await client.post(
            f"{BASE_URL}/pdf/ocr",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
