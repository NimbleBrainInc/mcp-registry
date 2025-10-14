"""
OpenAI MCP Server
Provides access to OpenAI API capabilities including chat completions, embeddings,
image generation, text-to-speech, speech-to-text, and model management.
"""

import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP
import base64

# Initialize FastMCP server
mcp = FastMCP("OpenAI API")

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = "https://api.openai.com/v1"

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")


async def make_openai_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    is_json: bool = True
) -> Any:
    """Make a request to OpenAI API"""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    if is_json:
        headers["Content-Type"] = "application/json"
    
    url = f"{OPENAI_BASE_URL}/{endpoint}"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "POST":
            if is_json:
                response = await client.post(url, headers=headers, json=data)
            else:
                response = await client.post(url, headers=headers, data=data)
        elif method == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json() if is_json else response.content


@mcp.tool()
async def chat_completion(
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-mini",
    temperature: float = 1.0,
    max_tokens: Optional[int] = None,
    response_format: Optional[str] = None
) -> str:
    """
    Generate a chat completion using OpenAI models.
    
    Args:
        messages: List of message objects with 'role' and 'content'
                 Example: [{"role": "user", "content": "Hello!"}]
        model: Model to use (gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo, etc.)
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens in response
        response_format: Optional response format ("json_object" for JSON mode)
    
    Returns:
        The assistant's response message
    """
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    
    if max_tokens:
        data["max_tokens"] = max_tokens
    
    if response_format:
        data["response_format"] = {"type": response_format}
    
    result = await make_openai_request("POST", "chat/completions", data)
    return result["choices"][0]["message"]["content"]


@mcp.tool()
async def create_embedding(
    text: str,
    model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Create an embedding vector for the given text.
    
    Args:
        text: Text to embed
        model: Embedding model (text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002)
    
    Returns:
        Dictionary with embedding vector and metadata
    """
    data = {
        "input": text,
        "model": model
    }
    
    result = await make_openai_request("POST", "embeddings", data)
    return {
        "embedding": result["data"][0]["embedding"],
        "model": result["model"],
        "dimensions": len(result["data"][0]["embedding"]),
        "usage": result["usage"]
    }


@mcp.tool()
async def generate_image(
    prompt: str,
    model: str = "dall-e-3",
    size: str = "1024x1024",
    quality: str = "standard",
    n: int = 1
) -> List[str]:
    """
    Generate images using DALL-E.
    
    Args:
        prompt: Text description of desired image
        model: Model to use (dall-e-3, dall-e-2)
        size: Image size (1024x1024, 1792x1024, 1024x1792 for dall-e-3)
        quality: Image quality (standard or hd for dall-e-3)
        n: Number of images to generate (1-10, only 1 for dall-e-3)
    
    Returns:
        List of image URLs
    """
    data = {
        "prompt": prompt,
        "model": model,
        "size": size,
        "n": n
    }
    
    if model == "dall-e-3":
        data["quality"] = quality
    
    result = await make_openai_request("POST", "images/generations", data)
    return [img["url"] for img in result["data"]]


@mcp.tool()
async def text_to_speech(
    text: str,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0
) -> str:
    """
    Convert text to speech audio.
    
    Args:
        text: Text to convert to speech
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        model: TTS model (tts-1, tts-1-hd)
        speed: Speech speed (0.25 to 4.0)
    
    Returns:
        Base64 encoded audio data (MP3 format)
    """
    data = {
        "input": text,
        "voice": voice,
        "model": model,
        "speed": speed
    }
    
    audio_bytes = await make_openai_request("POST", "audio/speech", data, is_json=False)
    return base64.b64encode(audio_bytes).decode('utf-8')


@mcp.tool()
async def transcribe_audio(
    audio_file_base64: str,
    model: str = "whisper-1",
    language: Optional[str] = None,
    response_format: str = "json"
) -> Dict[str, Any]:
    """
    Transcribe audio to text using Whisper.
    
    Args:
        audio_file_base64: Base64 encoded audio file
        model: Whisper model to use
        language: Language code (e.g., 'en', 'es') - auto-detected if not provided
        response_format: Response format (json, text, srt, vtt, verbose_json)
    
    Returns:
        Transcription result with text and metadata
    """
    # Decode base64 audio
    audio_bytes = base64.b64decode(audio_file_base64)
    
    # Prepare multipart form data
    files = {
        "file": ("audio.mp3", audio_bytes, "audio/mpeg"),
        "model": (None, model),
        "response_format": (None, response_format)
    }
    
    if language:
        files["language"] = (None, language)
    
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OPENAI_BASE_URL}/audio/transcriptions",
            headers=headers,
            files=files
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_models() -> List[Dict[str, Any]]:
    """
    List all available OpenAI models.
    
    Returns:
        List of model objects with id, created date, and owned_by information
    """
    result = await make_openai_request("GET", "models")
    return result["data"]


@mcp.tool()
async def moderate_content(
    text: str,
    model: str = "text-moderation-latest"
) -> Dict[str, Any]:
    """
    Check if content violates OpenAI's usage policies.
    
    Args:
        text: Text to moderate
        model: Moderation model (text-moderation-latest, text-moderation-stable)
    
    Returns:
        Moderation results with category flags and scores
    """
    data = {
        "input": text,
        "model": model
    }
    
    result = await make_openai_request("POST", "moderations", data)
    return result["results"][0]


@mcp.tool()
async def create_completion(
    prompt: str,
    model: str = "gpt-3.5-turbo-instruct",
    max_tokens: int = 100,
    temperature: float = 1.0,
    stop: Optional[List[str]] = None
) -> str:
    """
    Generate a completion (legacy endpoint, use chat_completion for newer models).
    
    Args:
        prompt: The prompt to generate completion for
        model: Model to use (gpt-3.5-turbo-instruct, davinci-002, babbage-002)
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0-2)
        stop: Sequences where the API will stop generating
    
    Returns:
        Generated completion text
    """
    data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    if stop:
        data["stop"] = stop
    
    result = await make_openai_request("POST", "completions", data)
    return result["choices"][0]["text"]


@mcp.tool()
async def analyze_image(
    image_url: str,
    prompt: str = "What's in this image?",
    model: str = "gpt-4o-mini",
    max_tokens: int = 300
) -> str:
    """
    Analyze an image using GPT-4 Vision.
    
    Args:
        image_url: URL of the image to analyze
        prompt: Question or instruction about the image
        model: Vision-capable model (gpt-4o, gpt-4o-mini, gpt-4-turbo)
        max_tokens: Maximum tokens in response
    
    Returns:
        Analysis of the image
    """
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ]
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }
    
    result = await make_openai_request("POST", "chat/completions", data)
    return result["choices"][0]["message"]["content"]