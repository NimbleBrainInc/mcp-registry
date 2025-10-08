"""
Google Gemini MCP Server
Provides tools for accessing Google Gemini multimodal AI API.
"""

import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Google Gemini MCP Server")

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


def get_url_with_key(endpoint: str) -> str:
    """Construct URL with API key parameter."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is required")
    return f"{BASE_URL}/{endpoint}?key={GEMINI_API_KEY}"


@mcp.tool()
async def generate_text(
    prompt: str,
    model: str = "gemini-1.5-flash-latest",
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
    system_instruction: Optional[str] = None
) -> dict:
    """
    Generate text with Gemini models.

    Args:
        prompt: Input text prompt
        model: Model name (gemini-1.5-pro-latest, gemini-1.5-flash-latest, gemini-2.0-flash-exp)
        temperature: Sampling temperature 0-2
        top_p: Nucleus sampling parameter
        top_k: Top-k sampling parameter
        max_output_tokens: Maximum tokens to generate
        system_instruction: System instruction for model behavior

    Returns:
        Dictionary with generated text
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        generation_config = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if top_p is not None:
            generation_config["topP"] = top_p
        if top_k is not None:
            generation_config["topK"] = top_k
        if max_output_tokens is not None:
            generation_config["maxOutputTokens"] = max_output_tokens

        if generation_config:
            payload["generationConfig"] = generation_config

        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        response = await client.post(
            get_url_with_key(f"models/{model}:generateContent"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def chat(
    messages: List[Dict[str, str]],
    model: str = "gemini-1.5-flash-latest",
    temperature: Optional[float] = None,
    system_instruction: Optional[str] = None
) -> dict:
    """
    Multi-turn conversation with context.

    Args:
        messages: List of messages with 'role' ('user'/'model') and 'text'
        model: Model name
        temperature: Sampling temperature
        system_instruction: System instruction

    Returns:
        Dictionary with generated response
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        contents = []
        for msg in messages:
            contents.append({
                "role": msg["role"],
                "parts": [{"text": msg["text"]}]
            })

        payload = {"contents": contents}

        if temperature is not None:
            payload["generationConfig"] = {"temperature": temperature}

        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        response = await client.post(
            get_url_with_key(f"models/{model}:generateContent"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def analyze_image(
    prompt: str,
    image_base64: str,
    mime_type: str = "image/jpeg",
    model: str = "gemini-1.5-flash-latest"
) -> dict:
    """
    Analyze images with vision capabilities.

    Args:
        prompt: Question or instruction about the image
        image_base64: Base64 encoded image
        mime_type: Image MIME type (image/jpeg, image/png, image/webp)
        model: Model name

    Returns:
        Dictionary with analysis results
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": image_base64
                        }
                    }
                ]
            }]
        }

        response = await client.post(
            get_url_with_key(f"models/{model}:generateContent"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def analyze_video(
    prompt: str,
    video_base64: str,
    mime_type: str = "video/mp4",
    model: str = "gemini-1.5-pro-latest"
) -> dict:
    """
    Analyze video content (frames, audio, transcription).

    Args:
        prompt: Question or instruction about the video
        video_base64: Base64 encoded video
        mime_type: Video MIME type (video/mp4, video/mpeg, video/mov)
        model: Model name (use gemini-1.5-pro-latest for video)

    Returns:
        Dictionary with video analysis
    """
    async with httpx.AsyncClient(timeout=300.0) as client:
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": video_base64
                        }
                    }
                ]
            }]
        }

        response = await client.post(
            get_url_with_key(f"models/{model}:generateContent"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def analyze_pdf(
    prompt: str,
    pdf_base64: str,
    model: str = "gemini-1.5-pro-latest"
) -> dict:
    """
    Extract and analyze PDF documents.

    Args:
        prompt: Question or instruction about the PDF
        pdf_base64: Base64 encoded PDF
        model: Model name

    Returns:
        Dictionary with PDF analysis
    """
    async with httpx.AsyncClient(timeout=180.0) as client:
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "application/pdf",
                            "data": pdf_base64
                        }
                    }
                ]
            }]
        }

        response = await client.post(
            get_url_with_key(f"models/{model}:generateContent"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def count_tokens(
    text: str,
    model: str = "gemini-1.5-flash-latest"
) -> dict:
    """
    Estimate token usage before generation.

    Args:
        text: Input text to count tokens
        model: Model name

    Returns:
        Dictionary with token count
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {
            "contents": [{"parts": [{"text": text}]}]
        }

        response = await client.post(
            get_url_with_key(f"models/{model}:countTokens"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def generate_with_tools(
    prompt: str,
    tools: List[Dict[str, Any]],
    model: str = "gemini-1.5-flash-latest"
) -> dict:
    """
    Function calling and tool use.

    Args:
        prompt: Input prompt
        tools: List of tool definitions with function schemas
        model: Model name

    Returns:
        Dictionary with generated response and function calls
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": tools
        }

        response = await client.post(
            get_url_with_key(f"models/{model}:generateContent"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def stream_generate(
    prompt: str,
    model: str = "gemini-1.5-flash-latest",
    temperature: Optional[float] = None
) -> dict:
    """
    Stream text generation responses.

    Args:
        prompt: Input text prompt
        model: Model name
        temperature: Sampling temperature

    Returns:
        Dictionary with streaming response chunks
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        if temperature is not None:
            payload["generationConfig"] = {"temperature": temperature}

        response = await client.post(
            get_url_with_key(f"models/{model}:streamGenerateContent?alt=sse"),
            json=payload,
        )
        response.raise_for_status()
        return {"stream": response.text}


@mcp.tool()
async def embed_text(
    text: str,
    model: str = "text-embedding-004",
    task_type: str = "RETRIEVAL_DOCUMENT"
) -> dict:
    """
    Generate embeddings with text-embedding-004.

    Args:
        text: Input text to embed
        model: Embedding model (text-embedding-004)
        task_type: Task type (RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, CLASSIFICATION, CLUSTERING)

    Returns:
        Dictionary with embedding vector
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        payload = {
            "model": f"models/{model}",
            "content": {"parts": [{"text": text}]},
            "taskType": task_type
        }

        response = await client.post(
            get_url_with_key("models/text-embedding-004:embedContent"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_models() -> dict:
    """
    List available Gemini models.

    Returns:
        Dictionary with available models and their capabilities
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            get_url_with_key("models"),
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def batch_generate(
    prompts: List[str],
    model: str = "gemini-1.5-flash-latest",
    temperature: Optional[float] = None
) -> dict:
    """
    Generate multiple responses in parallel.

    Args:
        prompts: List of prompts to process
        model: Model name
        temperature: Sampling temperature

    Returns:
        Dictionary with list of generated responses
    """
    async with httpx.AsyncClient(timeout=180.0) as client:
        requests = []
        for prompt in prompts:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            if temperature is not None:
                payload["generationConfig"] = {"temperature": temperature}
            requests.append(payload)

        # Note: Gemini API doesn't have native batch endpoint, so we process sequentially
        # In production, this should use asyncio.gather for true parallelism
        results = []
        for req in requests:
            response = await client.post(
                get_url_with_key(f"models/{model}:generateContent"),
                json=req,
            )
            response.raise_for_status()
            results.append(response.json())

        return {"results": results}


@mcp.tool()
async def generate_json(
    prompt: str,
    json_schema: Dict[str, Any],
    model: str = "gemini-1.5-flash-latest"
) -> dict:
    """
    Generate structured JSON output.

    Args:
        prompt: Input prompt
        json_schema: JSON schema for response format
        model: Model name

    Returns:
        Dictionary with structured JSON response
    """
    async with httpx.AsyncClient(timeout=120.0) as client:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": json_schema
            }
        }

        response = await client.post(
            get_url_with_key(f"models/{model}:generateContent"),
            json=payload,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run()
