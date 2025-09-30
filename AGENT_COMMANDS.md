# Agent Commands for Registry Management

Quick reference for common agent-assisted tasks.

## Adding a New Server

Use the general-purpose agent to add a new MCP server from a GitHub repository:

```
Add the MCP server from [GITHUB_URL] to the registry. Follow ADDING_SERVERS.md to:
1. Analyze the repository structure and determine transport type (prefer streamable-http)
2. Create servers/[name]/server.json with proper configuration
3. Create servers/[name]/test.json with at least one test
4. Validate with npm run validate-servers
```

**Example**:
```
Add the MCP server from https://github.com/example/weather-mcp to the registry.
Follow ADDING_SERVERS.md to create the server.json and test.json files.
```

## Testing a Server

```
Run E2E tests for the [server-name] server and fix any issues found
```

## Updating Server Metadata

```
Update the server.json for [server-name] to change [field] to [value]
```

## Batch Operations

```
Analyze all servers in the registry and ensure they follow the latest schema version
```

## Common Workflows

### Quick Add (with known details)
```
Add a new server:
- Name: weather-api
- GitHub: https://github.com/example/weather-mcp
- Image: example/weather-mcp:1.0.0
- Transport: streamable-http
- Tool: get_weather (takes location string)
- No secrets required
```

### Add with Secrets
```
Add a new server from https://github.com/example/api-mcp:
- Requires API_KEY environment variable (secret)
- Test should use ${API_KEY} from .env.e2e
- Primary tool: query_api
```