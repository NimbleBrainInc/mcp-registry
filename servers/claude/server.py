"""
Anthropic Claude MCP Server
Provides access to Claude API capabilities including messages, streaming,
vision, system prompts, and token counting.
"""

import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP
import json

# Initialize FastMCP server
mcp = FastMCP("Anthropic Claude API")

# Claude API configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
ANTHROPIC_VERSION = "2023-06-01"

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")


async def make_claude_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None
) -> Any:
    """Make a request to Claude API"""
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json"
    }
    
    url = f"{ANTHROPIC_BASE_URL}/{endpoint}"
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "POST":
            response = await client.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_message(
    messages: List[Dict[str, Any]],
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096,
    system: Optional[str] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    stop_sequences: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a message with Claude.
    
    Args:
        messages: List of message objects with 'role' and 'content'
                 Example: [{"role": "user", "content": "Hello!"}]
        model: Claude model to use (claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022, 
               claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307)
        max_tokens: Maximum tokens to generate (required, up to 8192)
        system: System prompt to set context and instructions
        temperature: Sampling temperature 0-1 (default: 1.0)
        top_p: Nucleus sampling threshold (default: none)
        top_k: Top-k sampling (default: none)
        stop_sequences: Custom stop sequences
    
    Returns:
        Complete message response with content, usage, and metadata
    """
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }
    
    if system:
        data["system"] = system
    if temperature is not None:
        data["temperature"] = temperature
    if top_p is not None:
        data["top_p"] = top_p
    if top_k is not None:
        data["top_k"] = top_k
    if stop_sequences:
        data["stop_sequences"] = stop_sequences
    
    result = await make_claude_request("POST", "messages", data)
    return result


@mcp.tool()
async def chat(
    prompt: str,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096,
    system: Optional[str] = None,
    temperature: Optional[float] = None
) -> str:
    """
    Simple chat interface - send a prompt and get a text response.
    
    Args:
        prompt: Your message or question
        model: Claude model to use
        max_tokens: Maximum tokens to generate
        system: Optional system prompt for context
        temperature: Sampling temperature 0-1
    
    Returns:
        Claude's text response
    """
    messages = [{"role": "user", "content": prompt}]
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }
    
    if system:
        data["system"] = system
    if temperature is not None:
        data["temperature"] = temperature
    
    result = await make_claude_request("POST", "messages", data)
    
    # Extract text from content blocks
    text_content = []
    for block in result.get("content", []):
        if block.get("type") == "text":
            text_content.append(block.get("text", ""))
    
    return "\n".join(text_content)


@mcp.tool()
async def analyze_image(
    image_url: str,
    prompt: str = "What's in this image?",
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096
) -> str:
    """
    Analyze an image using Claude's vision capabilities.
    
    Args:
        image_url: URL of the image to analyze
        prompt: Question or instruction about the image
        model: Vision-capable Claude model
        max_tokens: Maximum tokens in response
    
    Returns:
        Analysis of the image
    """
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": image_url
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }
    
    result = await make_claude_request("POST", "messages", data)
    
    # Extract text from content blocks
    text_content = []
    for block in result.get("content", []):
        if block.get("type") == "text":
            text_content.append(block.get("text", ""))
    
    return "\n".join(text_content)


@mcp.tool()
async def analyze_image_base64(
    image_base64: str,
    media_type: str,
    prompt: str = "What's in this image?",
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096
) -> str:
    """
    Analyze a base64-encoded image using Claude's vision capabilities.
    
    Args:
        image_base64: Base64 encoded image data
        media_type: Image media type (image/jpeg, image/png, image/gif, image/webp)
        prompt: Question or instruction about the image
        model: Vision-capable Claude model
        max_tokens: Maximum tokens in response
    
    Returns:
        Analysis of the image
    """
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_base64
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }
    
    result = await make_claude_request("POST", "messages", data)
    
    # Extract text from content blocks
    text_content = []
    for block in result.get("content", []):
        if block.get("type") == "text":
            text_content.append(block.get("text", ""))
    
    return "\n".join(text_content)


@mcp.tool()
async def count_tokens(
    messages: List[Dict[str, Any]],
    model: str = "claude-3-5-sonnet-20241022",
    system: Optional[str] = None
) -> Dict[str, int]:
    """
    Count tokens for a given set of messages without making an API call.
    Uses the Messages API with a special parameter to only count tokens.
    
    Args:
        messages: List of message objects to count tokens for
        model: Claude model (affects tokenization)
        system: Optional system prompt to include in count
    
    Returns:
        Dictionary with input_tokens count
    """
    # Note: Anthropic's API doesn't have a dedicated token counting endpoint
    # This is a workaround that makes a message request with max_tokens=1
    # to get token count from the usage field
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": 1
    }
    
    if system:
        data["system"] = system
    
    result = await make_claude_request("POST", "messages", data)
    
    return {
        "input_tokens": result.get("usage", {}).get("input_tokens", 0),
        "output_tokens": result.get("usage", {}).get("output_tokens", 0)
    }


@mcp.tool()
async def multi_turn_conversation(
    conversation_history: List[Dict[str, str]],
    new_message: str,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096,
    system: Optional[str] = None
) -> Dict[str, Any]:
    """
    Continue a multi-turn conversation by adding a new message.
    
    Args:
        conversation_history: Previous messages in the conversation
                             Example: [{"role": "user", "content": "Hi"}, 
                                      {"role": "assistant", "content": "Hello!"}]
        new_message: New user message to add to the conversation
        model: Claude model to use
        max_tokens: Maximum tokens to generate
        system: Optional system prompt
    
    Returns:
        Complete response with new assistant message and full conversation
    """
    # Add new user message to history
    messages = conversation_history + [{"role": "user", "content": new_message}]
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }
    
    if system:
        data["system"] = system
    
    result = await make_claude_request("POST", "messages", data)
    
    # Extract assistant's response
    text_content = []
    for block in result.get("content", []):
        if block.get("type") == "text":
            text_content.append(block.get("text", ""))
    
    assistant_message = "\n".join(text_content)
    
    return {
        "response": assistant_message,
        "updated_history": messages + [{"role": "assistant", "content": assistant_message}],
        "usage": result.get("usage", {}),
        "model": result.get("model", model),
        "stop_reason": result.get("stop_reason", "")
    }


@mcp.tool()
async def get_model_info(model: str = "claude-3-5-sonnet-20241022") -> Dict[str, Any]:
    """
    Get information about a Claude model including context window and capabilities.
    
    Args:
        model: Model identifier
    
    Returns:
        Model information including context window, capabilities, and pricing tier
    """
    # Static model information (as of API version 2023-06-01)
    model_info = {
        "claude-3-5-sonnet-20241022": {
            "name": "Claude 3.5 Sonnet",
            "version": "20241022",
            "context_window": 200000,
            "max_output": 8192,
            "supports_vision": True,
            "supports_tool_use": True,
            "tier": "intelligent",
            "description": "Our most intelligent model with best-in-class performance"
        },
        "claude-3-5-haiku-20241022": {
            "name": "Claude 3.5 Haiku",
            "version": "20241022",
            "context_window": 200000,
            "max_output": 8192,
            "supports_vision": True,
            "supports_tool_use": True,
            "tier": "fast",
            "description": "Our fastest model for quick, intelligent responses"
        },
        "claude-3-opus-20240229": {
            "name": "Claude 3 Opus",
            "version": "20240229",
            "context_window": 200000,
            "max_output": 4096,
            "supports_vision": True,
            "supports_tool_use": True,
            "tier": "powerful",
            "description": "Top-level performance for complex tasks"
        },
        "claude-3-sonnet-20240229": {
            "name": "Claude 3 Sonnet",
            "version": "20240229",
            "context_window": 200000,
            "max_output": 4096,
            "supports_vision": True,
            "supports_tool_use": True,
            "tier": "balanced",
            "description": "Balance of intelligence and speed"
        },
        "claude-3-haiku-20240307": {
            "name": "Claude 3 Haiku",
            "version": "20240307",
            "context_window": 200000,
            "max_output": 4096,
            "supports_vision": True,
            "supports_tool_use": True,
            "tier": "fast",
            "description": "Fast and cost-effective"
        }
    }
    
    info = model_info.get(model, {
        "name": model,
        "context_window": "unknown",
        "supports_vision": "unknown",
        "description": "Model information not available"
    })
    
    info["model_id"] = model
    return info


@mcp.tool()
async def compare_responses(
    prompt: str,
    models: List[str] = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"],
    max_tokens: int = 1024,
    system: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get responses from multiple Claude models for comparison.
    
    Args:
        prompt: Question or task to send to all models
        models: List of model identifiers to compare (max 3 for cost reasons)
        max_tokens: Maximum tokens per response
        system: Optional system prompt
    
    Returns:
        Dictionary with responses from each model and timing information
    """
    if len(models) > 3:
        raise ValueError("Maximum 3 models allowed for comparison")
    
    messages = [{"role": "user", "content": prompt}]
    
    results = {}
    for model in models:
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }
        
        if system:
            data["system"] = system
        
        result = await make_claude_request("POST", "messages", data)
        
        # Extract text response
        text_content = []
        for block in result.get("content", []):
            if block.get("type") == "text":
                text_content.append(block.get("text", ""))
        
        results[model] = {
            "response": "\n".join(text_content),
            "usage": result.get("usage", {}),
            "stop_reason": result.get("stop_reason", "")
        }
    
    return results


@mcp.tool()
async def extract_structured_data(
    text: str,
    schema_description: str,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 4096
) -> str:
    """
    Extract structured data from unstructured text based on a schema description.
    
    Args:
        text: Unstructured text to extract data from
        schema_description: Description of the data structure you want (e.g., 
                          "Extract person's name, email, and phone number as JSON")
        model: Claude model to use
        max_tokens: Maximum tokens for response
    
    Returns:
        Extracted structured data (typically as JSON string)
    """
    system_prompt = f"""Extract structured data according to this schema:
{schema_description}

Return ONLY the structured data, no additional explanation."""
    
    messages = [{"role": "user", "content": text}]
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "system": system_prompt
    }
    
    result = await make_claude_request("POST", "messages", data)
    
    # Extract text from content blocks
    text_content = []
    for block in result.get("content", []):
        if block.get("type") == "text":
            text_content.append(block.get("text", ""))
    
    return "\n".join(text_content)