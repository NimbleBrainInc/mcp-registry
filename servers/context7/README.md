# Context7 MCP Server

MCP server providing access to Context7 API for up-to-date code documentation retrieval.

## Features

### Core Capabilities
- **Documentation Search** - Search across thousands of libraries and frameworks
- **Code Examples** - Get working code examples for specific use cases
- **API Reference** - Detailed API documentation for functions and classes
- **Code Explanation** - Understand code with line-by-line explanations
- **Troubleshooting** - Get help with error messages and bugs
- **Best Practices** - Learn recommended patterns and anti-patterns
- **Migration Guides** - Upgrade between versions or switch libraries
- **Library Comparison** - Compare different libraries for your use case
- **Changelog Access** - View release notes and breaking changes

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your Context7 API key
```

## Configuration

### Get Your Context7 API Key
1. Go to https://context7.com/api
2. Sign up or sign in
3. Generate an API key
4. Copy the key and add it to your `.env` file

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "context7": {
      "command": "fastmcp",
      "args": ["run", "server.py"],
      "env": {
        "CONTEXT7_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### search_documentation
Search for documentation across supported libraries.

**Parameters:**
- `query` (required): Search query
- `language`: Filter by language (javascript, python, go, etc.)
- `framework`: Filter by framework (react, django, nextjs, etc.)
- `limit`: Max results (default: 10, max: 50)

**Example:**
```json
{
  "query": "how to use useState in React",
  "framework": "react",
  "limit": 5
}
```

### get_library_docs
Get documentation for a specific library.

**Parameters:**
- `library` (required): Library name
- `version`: Specific version (default: latest)
- `topic`: Specific topic or module

**Example:**
```json
{
  "library": "react",
  "version": "18.2.0",
  "topic": "hooks"
}
```

### get_code_examples
Get code examples for a specific use case.

**Parameters:**
- `library` (required): Library name
- `use_case` (required): What you're trying to accomplish
- `language`: Programming language

**Example:**
```json
{
  "library": "express",
  "use_case": "JWT authentication middleware"
}
```

### explain_code
Get explanation of code with documentation references.

**Parameters:**
- `code` (required): Code snippet to explain
- `language`: Programming language (auto-detected)
- `context`: Additional context

**Example:**
```json
{
  "code": "const [count, setCount] = useState(0);",
  "language": "javascript",
  "context": "React component"
}
```

### get_api_reference
Get detailed API reference for a function or class.

**Parameters:**
- `library` (required): Library name
- `api_name` (required): API/function/class name
- `version`: Library version (default: latest)

**Example:**
```json
{
  "library": "react",
  "api_name": "useState",
  "version": "18.2.0"
}
```

### compare_libraries
Compare multiple libraries for a use case.

**Parameters:**
- `libraries` (required): List of library names
- `use_case` (required): What you're building
- `language`: Programming language

**Example:**
```json
{
  "libraries": ["react", "vue", "svelte"],
  "use_case": "building a todo app"
}
```

### get_migration_guide
Get migration guide between libraries or versions.

**Parameters:**
- `from_library` (required): Current library
- `to_library` (required): Target library
- `from_version`: Current version
- `to_version`: Target version

**Example:**
```json
{
  "from_library": "react",
  "to_library": "react",
  "from_version": "17.0.0",
  "to_version": "18.0.0"
}
```

### get_best_practices
Get best practices for a library.

**Parameters:**
- `library` (required): Library name
- `topic`: Specific topic (performance, security, testing, etc.)

**Example:**
```json
{
  "library": "react",
  "topic": "performance"
}
```

### troubleshoot_error
Get help with error messages.

**Parameters:**
- `error_message` (required): The error you're seeing
- `library`: Library where error occurred
- `code_context`: Code causing the error

**Example:**
```json
{
  "error_message": "Cannot read property 'map' of undefined",
  "library": "react",
  "code_context": "data.map(item => <div>{item}</div>)"
}
```

### list_supported_libraries
List all supported libraries.

**Parameters:**
- `language`: Filter by language
- `category`: Filter by category

**Example:**
```json
{
  "language": "python",
  "category": "data-science"
}
```

### get_changelog
Get changelog and release notes.

**Parameters:**
- `library` (required): Library name
- `from_version`: Starting version
- `to_version`: Ending version (default: latest)

**Example:**
```json
{
  "library": "react",
  "from_version": "17.0.0",
  "to_version": "18.2.0"
}
```

## Usage Examples

### Search for Documentation
```json
{
  "tool": "search_documentation",
  "query": "authentication with JWT",
  "language": "javascript"
}
```

### Get Code Examples
```json
{
  "tool": "get_code_examples",
  "library": "pandas",
  "use_case": "filter dataframe by multiple conditions"
}
```

### Explain Complex Code
```json
{
  "tool": "explain_code",
  "code": "useEffect(() => { fetchData(); }, [id]);",
  "language": "javascript"
}
```

### Compare Frameworks
```json
{
  "tool": "compare_libraries",
  "libraries": ["express", "fastify", "koa"],
  "use_case": "REST API server"
}
```

### Troubleshoot an Error
```json
{
  "tool": "troubleshoot_error",
  "error_message": "Module not found: Can't resolve 'react'",
  "library": "react"
}
```

### Migration Help
```json
{
  "tool": "get_migration_guide",
  "from_library": "webpack",
  "to_library": "vite"
}
```

## Supported Languages & Frameworks

Context7 supports documentation for:

### Languages
- JavaScript/TypeScript
- Python
- Go
- Rust
- Java
- C#
- PHP
- Ruby
- Swift
- Kotlin

### Popular Frameworks
- **Web**: React, Vue, Angular, Svelte, Next.js, Nuxt
- **Backend**: Express, Django, FastAPI, Spring Boot, Rails
- **Mobile**: React Native, Flutter, SwiftUI
- **Data Science**: Pandas, NumPy, Scikit-learn, TensorFlow
- **DevOps**: Docker, Kubernetes, Terraform, Ansible

## Use Cases

### For Developers
- Quick documentation lookup while coding
- Find working code examples
- Understand unfamiliar code
- Troubleshoot errors faster
- Learn best practices

### For AI Agents
- Provide accurate, up-to-date documentation
- Generate code with proper library usage
- Help debug issues with context
- Recommend appropriate libraries
- Assist with migrations and upgrades

## Error Handling

The server handles:
- Invalid API keys
- Rate limiting
- Network timeouts
- Invalid library names
- Malformed queries

## Rate Limits

Context7 API rate limits depend on your plan:
- Free tier: 100 requests/day
- Pro tier: 10,000 requests/day
- Enterprise: Custom limits

Check your usage at: https://context7.com/dashboard

## Best Practices

1. **Be Specific**: Include library names and versions when possible
2. **Use Filters**: Narrow searches with language/framework filters
3. **Cache Results**: Store frequently accessed documentation
4. **Combine Tools**: Use search + get_api_reference for comprehensive info
5. **Error Context**: Provide code context for better troubleshooting

## Security Notes

- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly
- Monitor usage in dashboard
- Set up usage alerts

## Troubleshooting

### "Invalid API Key" Error
- Verify key in `.env` file
- Check key is active at context7.com
- Ensure no extra spaces

### Rate Limit Errors
- Check current usage in dashboard
- Upgrade plan if needed
- Implement caching

### Library Not Found
- Check library name spelling
- Use list_supported_libraries to verify
- Some libraries may not be indexed yet

## Resources

- [Context7 Website](https://context7.com)
- [API Documentation](https://context7.com/docs)
- [Supported Libraries](https://context7.com/libraries)
- [Model Context Protocol](https://modelcontextprotocol.io)

## License

MIT License - feel free to use in your projects!