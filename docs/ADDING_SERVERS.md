# Guide: Adding MCP Servers to the Registry

This guide helps you add new MCP servers to the NimbleTools registry. Follow these steps to create a proper `server.json` and `test.json` for any MCP server.

## Prerequisites

Before adding a server, you need:
1. A GitHub repository URL for the MCP server
2. An OCI container image (Docker Hub, GHCR, etc.)
3. Knowledge of the server's tools/capabilities
4. Any required environment variables/API keys

## Step 1: Analyze the MCP Server

Review the GitHub repository to understand:

- **Transport type**: Does it support HTTP (`streamable-http`) or only `stdio`?
  - ✅ Prefer `streamable-http` (runs as HTTP server)
  - ⚠️ Use `stdio` only if HTTP not available
  - ❌ SSE is NOT supported

- **Container details**:
  - Health check endpoint (usually `/health`)
  - Port (usually `8000`)
  - MCP endpoint path (usually `/mcp`)

- **Environment variables**:
  - API keys (mark as `isSecret: true, isRequired: true`)
  - Configuration options (mark as `isRequired: false`)

- **Available tools**:
  - List all tools the server provides
  - Note their input parameters

## Step 2: Create server.json

Create `servers/{server-name}/server.json` following this template:

```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-09-22/nimbletools-server.schema.json",
  "name": "ai.nimbletools/{server-name}",
  "version": "1.0.0",
  "description": "Brief description of what the server does",
  "status": "active",
  "repository": {
    "url": "https://github.com/owner/repo",
    "source": "github",
    "branch": "main"
  },
  "websiteUrl": "https://github.com/owner/repo",
  "packages": [
    {
      "registryType": "oci",
      "registryBaseUrl": "https://docker.io",
      "identifier": "owner/image-name",
      "version": "1.0.0",
      "transport": {
        "type": "streamable-http",
        "url": "https://mcp.nimbletools.ai/mcp"
      },
      "environmentVariables": [
        {
          "name": "API_KEY",
          "description": "API key for the service",
          "isRequired": true,
          "isSecret": true
        }
      ]
    }
  ],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "container": {
        "healthCheck": {
          "path": "/health",
          "port": 8000
        }
      },
      "capabilities": {
        "tools": true,
        "resources": false,
        "prompts": false
      },
      "resources": {
        "limits": {
          "memory": "256Mi",
          "cpu": "100m"
        },
        "requests": {
          "memory": "128Mi",
          "cpu": "50m"
        }
      },
      "deployment": {
        "protocol": "http",
        "port": 8000,
        "mcpPath": "/mcp"
      },
      "display": {
        "name": "Display Name",
        "documentation": {
          "readmeUrl": "https://raw.githubusercontent.com/owner/repo/main/README.md"
        },
        "branding": {
          "iconUrl": "https://example.com/icon.png"
        }
      }
    }
  }
}
```

### Key Fields

**Required fields**:
- `name`: Format `ai.nimbletools/{server-name}` (use lowercase with hyphens)
- `version`: Semantic version of the server
- `description`: Clear, concise description (max 200 chars)
- `status`: Usually `"active"`
- `packages[0].identifier`: Container image name
- `packages[0].transport.type`: `"streamable-http"` or `"stdio"`

**Transport types**:

For `streamable-http` (preferred):
```json
{
  "transport": {
    "type": "streamable-http",
    "url": "https://mcp.nimbletools.ai/mcp"
  }
}
```

For `stdio` (fallback):
```json
{
  "transport": {
    "type": "stdio"
  }
}
```

**Environment variables**:
```json
{
  "environmentVariables": [
    {
      "name": "API_KEY",
      "description": "Description of the variable",
      "isRequired": true,    // true if server won't work without it
      "isSecret": true       // true for API keys, tokens, passwords
    }
  ]
}
```

**Container metadata**:
- `healthCheck.path`: Usually `/health`
- `healthCheck.port`: Usually `8000`
- `deployment.mcpPath`: Usually `/mcp`
- `resources`: Adjust based on server needs (default: 256Mi memory, 100m CPU)

**Capabilities**: Set to `true` only for what the server actually supports:
- `tools`: Server has callable tools
- `resources`: Server provides resources
- `prompts`: Server has prompts

## Step 3: Create test.json

Create `servers/{server-name}/test.json` to validate the server works:

### Basic test (no secrets required)

```json
{
  "skip": false,
  "tests": [
    {
      "name": "Test basic functionality",
      "tool": "tool_name",
      "arguments": {
        "param": "value"
      },
      "expect": {
        "type": "text",
        "contains": "expected output"
      }
    }
  ]
}
```

### Test requiring secrets

```json
{
  "skip": false,
  "skipReason": "Requires API_KEY",
  "environment": {
    "API_KEY": "${API_KEY}"
  },
  "tests": [
    {
      "name": "Test with API key",
      "tool": "tool_name",
      "arguments": {
        "query": "test"
      },
      "expect": {
        "type": "json"
      }
    }
  ]
}
```

### Expectation types

**Text validation**:
```json
{
  "expect": {
    "type": "text",
    "contains": "substring to find"
  }
}
```

**JSON validation**:
```json
{
  "expect": {
    "type": "json"
  }
}
```

**Any response**:
```json
{
  "expect": {
    "type": "any"
  }
}
```

## Step 4: Validate

Run validation to ensure your server definition is correct:

```bash
# Validate server schema
npm run validate-servers

# Run E2E test (if you have credentials)
npm run test:e2e -- --server={server-name}
```

## Examples

### Example 1: Simple HTTP server (echo)

`servers/echo/server.json`:
```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-09-22/nimbletools-server.schema.json",
  "name": "ai.nimbletools/echo",
  "version": "1.0.0",
  "description": "Simple echo service for testing",
  "status": "active",
  "repository": {
    "url": "https://github.com/NimbleBrainInc/mcp-echo",
    "source": "github",
    "branch": "main"
  },
  "packages": [{
    "registryType": "oci",
    "identifier": "nimbletools/mcp-echo",
    "version": "1.0.0",
    "transport": {
      "type": "streamable-http"
    }
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "container": {
        "healthCheck": {
          "path": "/health",
          "port": 8000
        }
      },
      "deployment": {
        "protocol": "http",
        "port": 8000,
        "mcpPath": "/mcp"
      }
    }
  }
}
```

`servers/echo/test.json`:
```json
{
  "tests": [{
    "name": "Echo test",
    "tool": "echo",
    "arguments": { "message": "hello" },
    "expect": { "type": "text", "contains": "hello" }
  }]
}
```

### Example 2: Server with API key (finnhub)

`servers/finnhub/server.json`:
```json
{
  "name": "ai.nimbletools/finnhub",
  "packages": [{
    "registryType": "oci",
    "identifier": "nimbletools/mcp-finnhub",
    "version": "1.0.0",
    "transport": {
      "type": "streamable-http"
    },
    "environmentVariables": [{
      "name": "FINNHUB_API_KEY",
      "description": "Finnhub API key",
      "isRequired": true,
      "isSecret": true
    }]
  }]
}
```

`servers/finnhub/test.json`:
```json
{
  "skip": false,
  "environment": {
    "FINNHUB_API_KEY": "${FINNHUB_API_KEY}"
  },
  "tests": [{
    "name": "Get stock quote",
    "tool": "get_stock_quote",
    "arguments": { "symbol": "AAPL" },
    "expect": { "type": "json" }
  }]
}
```

## Checklist

Before submitting:

- [ ] `server.json` validates with schema
- [ ] Transport type is `streamable-http` (or `stdio` if no HTTP support)
- [ ] Health check endpoint is correct
- [ ] Environment variables marked as `isSecret` and `isRequired` appropriately
- [ ] `test.json` includes at least one basic test
- [ ] Test runs successfully with `npm run test:e2e -- --server={name}`
- [ ] Container image is publicly accessible
- [ ] README URL points to valid documentation

## Common Issues

**Issue**: Server fails to start
- Check container logs: `kubectl logs -n {namespace} {pod-name}`
- Verify environment variables are set correctly
- Check health endpoint returns 200 OK

**Issue**: MCP connection fails (406 Not Acceptable)
- Client must send `Accept: application/json, text/event-stream`
- Verify server supports MCP protocol version `2024-11-05`

**Issue**: Test fails validation
- Check tool response format matches expectation
- Use `"type": "any"` for initial testing, then refine

**Issue**: stdio transport not working
- Ensure container entrypoint executes MCP server correctly
- stdio transport requires wrapper/adapter for HTTP communication

## Getting Help

- Review existing servers in `servers/` directory for examples
- Check schema documentation: https://registry.nimbletools.ai/schemas
- Test locally with `npm run test:e2e` before submitting
- Open an issue if you need assistance

## Agent Workflow

If you are an AI agent adding a server:

1. **Fetch repository**: Clone or analyze the GitHub repo
2. **Identify transport**: Check if server supports HTTP endpoints (look for Express, Fastify, HTTP server code)
3. **Find container**: Look for Dockerfile, docker-compose.yml, or published images on Docker Hub/GHCR
4. **Extract tools**: Read server code or documentation to list available MCP tools
5. **Map environment variables**: Find all required configuration/secrets
6. **Generate server.json**: Use the template above
7. **Create test.json**: Write at least one test for the primary tool
8. **Validate**: Run `npm run validate-servers`

When in doubt, prefer:
- `streamable-http` over `stdio`
- Simple tests with `"type": "any"` expectations
- Conservative resource limits (256Mi/100m)
- Marking variables as `isSecret: true` if they look sensitive