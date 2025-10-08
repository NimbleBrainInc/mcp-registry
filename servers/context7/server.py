"""
Context7 MCP Server
Provides access to Context7 API for up-to-date code documentation retrieval.
Context7 delivers accurate, context-aware documentation for libraries and frameworks.
"""

import os
from typing import Optional, List, Dict, Any
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Context7 Documentation API")

# Context7 API configuration
CONTEXT7_API_KEY = os.getenv("CONTEXT7_API_KEY")
CONTEXT7_BASE_URL = "https://api.context7.com/v1"

if not CONTEXT7_API_KEY:
    raise ValueError("CONTEXT7_API_KEY environment variable is required")


async def make_context7_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Any:
    """Make a request to Context7 API"""
    headers = {
        "Authorization": f"Bearer {CONTEXT7_API_KEY}",
        "Content-Type": "application/json"
    }
    
    url = f"{CONTEXT7_BASE_URL}/{endpoint}"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        if method == "GET":
            response = await client.get(url, headers=headers, params=params)
        elif method == "POST":
            response = await client.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def search_documentation(
    query: str,
    language: Optional[str] = None,
    framework: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for documentation across supported libraries and frameworks.
    
    Args:
        query: Search query (e.g., "how to use useState in React")
        language: Filter by programming language (e.g., "javascript", "python", "go")
        framework: Filter by framework (e.g., "react", "django", "nextjs")
        limit: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        List of documentation results with content, source, and relevance scores
    """
    params = {
        "q": query,
        "limit": min(limit, 50)
    }
    
    if language:
        params["language"] = language
    if framework:
        params["framework"] = framework
    
    result = await make_context7_request("GET", "search", params=params)
    return result.get("results", [])


@mcp.tool()
async def get_library_docs(
    library: str,
    version: Optional[str] = None,
    topic: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get documentation for a specific library or framework.
    
    Args:
        library: Library name (e.g., "react", "numpy", "express")
        version: Specific version (e.g., "18.2.0", "latest")
        topic: Specific topic or module (e.g., "hooks", "components")
    
    Returns:
        Documentation content with examples and API references
    """
    params = {
        "library": library
    }
    
    if version:
        params["version"] = version
    if topic:
        params["topic"] = topic
    
    result = await make_context7_request("GET", "docs", params=params)
    return result


@mcp.tool()
async def get_code_examples(
    library: str,
    use_case: str,
    language: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get code examples for a specific library and use case.
    
    Args:
        library: Library name (e.g., "react", "pandas", "express")
        use_case: What you're trying to accomplish (e.g., "authentication", "data filtering")
        language: Programming language (auto-detected if not provided)
    
    Returns:
        List of code examples with explanations
    """
    data = {
        "library": library,
        "use_case": use_case
    }
    
    if language:
        data["language"] = language
    
    result = await make_context7_request("POST", "examples", data=data)
    return result.get("examples", [])


@mcp.tool()
async def explain_code(
    code: str,
    language: Optional[str] = None,
    context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get an explanation of code with relevant documentation references.
    
    Args:
        code: Code snippet to explain
        language: Programming language (auto-detected if not provided)
        context: Additional context about what the code is for
    
    Returns:
        Explanation with line-by-line breakdown and documentation links
    """
    data = {
        "code": code
    }
    
    if language:
        data["language"] = language
    if context:
        data["context"] = context
    
    result = await make_context7_request("POST", "explain", data=data)
    return result


@mcp.tool()
async def get_api_reference(
    library: str,
    api_name: str,
    version: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed API reference for a specific function, class, or method.
    
    Args:
        library: Library name (e.g., "react", "express", "pandas")
        api_name: API/function/class name (e.g., "useState", "Router", "DataFrame")
        version: Library version (default: latest)
    
    Returns:
        Detailed API documentation including parameters, return types, and examples
    """
    params = {
        "library": library,
        "api": api_name
    }
    
    if version:
        params["version"] = version
    
    result = await make_context7_request("GET", "api-reference", params=params)
    return result


@mcp.tool()
async def compare_libraries(
    libraries: List[str],
    use_case: str,
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Compare multiple libraries for a specific use case.
    
    Args:
        libraries: List of library names to compare (e.g., ["react", "vue", "svelte"])
        use_case: What you're trying to accomplish
        language: Programming language context
    
    Returns:
        Comparison with pros, cons, and code examples for each library
    """
    data = {
        "libraries": libraries,
        "use_case": use_case
    }
    
    if language:
        data["language"] = language
    
    result = await make_context7_request("POST", "compare", data=data)
    return result


@mcp.tool()
async def get_migration_guide(
    from_library: str,
    to_library: str,
    from_version: Optional[str] = None,
    to_version: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a migration guide between libraries or versions.
    
    Args:
        from_library: Current library name
        to_library: Target library name
        from_version: Current version (if same library)
        to_version: Target version (if same library)
    
    Returns:
        Migration guide with breaking changes, code examples, and step-by-step instructions
    """
    data = {
        "from": from_library,
        "to": to_library
    }
    
    if from_version:
        data["from_version"] = from_version
    if to_version:
        data["to_version"] = to_version
    
    result = await make_context7_request("POST", "migrate", data=data)
    return result


@mcp.tool()
async def get_best_practices(
    library: str,
    topic: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get best practices and recommendations for a library.
    
    Args:
        library: Library name (e.g., "react", "django", "express")
        topic: Specific topic (e.g., "performance", "security", "testing")
    
    Returns:
        Best practices, patterns, and anti-patterns with examples
    """
    params = {
        "library": library
    }
    
    if topic:
        params["topic"] = topic
    
    result = await make_context7_request("GET", "best-practices", params=params)
    return result


@mcp.tool()
async def troubleshoot_error(
    error_message: str,
    library: Optional[str] = None,
    code_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get help troubleshooting an error with documentation references.
    
    Args:
        error_message: The error message you're seeing
        library: Library where the error occurred (if known)
        code_context: Code that's causing the error
    
    Returns:
        Possible causes, solutions, and relevant documentation
    """
    data = {
        "error": error_message
    }
    
    if library:
        data["library"] = library
    if code_context:
        data["code_context"] = code_context
    
    result = await make_context7_request("POST", "troubleshoot", data=data)
    return result


@mcp.tool()
async def list_supported_libraries(
    language: Optional[str] = None,
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List all libraries supported by Context7.
    
    Args:
        language: Filter by programming language
        category: Filter by category (e.g., "web-framework", "data-science", "testing")
    
    Returns:
        List of supported libraries with versions and categories
    """
    params = {}
    
    if language:
        params["language"] = language
    if category:
        params["category"] = category
    
    result = await make_context7_request("GET", "libraries", params=params)
    return result.get("libraries", [])


@mcp.tool()
async def get_changelog(
    library: str,
    from_version: Optional[str] = None,
    to_version: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get changelog and release notes for a library.
    
    Args:
        library: Library name
        from_version: Starting version
        to_version: Ending version (default: latest)
    
    Returns:
        Changelog with breaking changes, new features, and bug fixes
    """
    params = {
        "library": library
    }
    
    if from_version:
        params["from_version"] = from_version
    if to_version:
        params["to_version"] = to_version
    
    result = await make_context7_request("GET", "changelog", params=params)
    return result