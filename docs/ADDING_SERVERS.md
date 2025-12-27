# Guide: Adding MCP Servers to the Registry

This guide helps you add new MCP servers to the NimbleTools registry. Follow these steps to create a proper `server.json` and `test.json` for any MCP server.

## Prerequisites

Before adding a server, you need:
1. A GitHub repository URL for the MCP server
2. A package source: either an OCI container image OR an MCPB bundle release
3. Knowledge of the server's tools/capabilities
4. Any required environment variables/API keys

## Package Types

The registry supports two package types:

### OCI (Pre-built HTTP containers)
Use OCI when the server already exposes `streamable-http` in its container:
- Server has a Dockerfile that runs an HTTP server
- Container exposes `/mcp` endpoint directly
- Examples: servers with built-in FastAPI, Express, or HTTP frameworks

### MCPB (MCP Bundles)
Use MCPB when the server needs a runtime provided by NimbleTools:
- **python:3.13** / **python:3.14** - Python servers using FastMCP or similar
- **node:24** - Node.js/TypeScript servers
- **supergateway-python:3.14** - Python stdio servers wrapped with HTTP
- **binary** - Pre-compiled Go/Rust binaries

For stdio-based MCP servers that don't expose HTTP natively, use MCPB with the `supergateway-python` runtime which wraps stdio to HTTP.

## Step 1: Analyze the MCP Server

Review the GitHub repository to understand:

- **Package type**: Does it have an HTTP server or need a runtime?
  - ✅ Has HTTP server → Use OCI
  - ✅ Python/Node source → Use MCPB with appropriate runtime
  - ✅ Stdio only → Use MCPB with `supergateway-python` runtime
  - ❌ SSE is NOT supported

- **Container/runtime details**:
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
  "$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/{server-name}",
  "version": "1.0.0",
  "title": "Display Name",
  "description": "Brief description of what the server does",
  "icons": [
    { "src": "https://static.nimbletools.ai/icons/{server-name}.png", "sizes": ["64x64"] },
    { "src": "https://static.nimbletools.ai/logos/{server-name}.png", "sizes": ["256x256"] }
  ],
  "repository": {
    "url": "https://github.com/owner/repo",
    "source": "github"
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
          "isSecret": true,
          "placeholder": "your_api_key_here"
        }
      ]
    }
  ],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "status": "active",
      "repository": {
        "branch": "main"
      },
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
        "category": "developer-tools",
        "tags": ["example"],
        "documentation": {
          "readmeUrl": "https://raw.githubusercontent.com/owner/repo/main/README.md"
        }
      }
    }
  }
}
```

### Key Fields

**Required fields (core schema)**:
- `name`: Format `ai.nimbletools/{server-name}` (use lowercase with hyphens)
- `version`: Semantic version of the server
- `description`: Clear, concise description (max 100 chars)
- `packages[0].registryType`: `"oci"` or `"mcpb"`
- `packages[0].identifier`: Container image name (OCI) or bundle identifier (MCPB)
- `packages[0].transport.type`: `"streamable-http"`

**Recommended fields (core schema)**:
- `title`: Human-readable display name
- `icons`: Array of icon objects with `src` and `sizes`
- `repository`: GitHub/source code location

**NimbleTools extension fields** (`_meta.ai.nimbletools.mcp/v1`):
- `status`: Server lifecycle (`active`, `deprecated`, `beta`)
- `repository.branch`: Git branch (moved from core)
- `container`: Health check configuration
- `capabilities`: MCP capability flags
- `display.category`: Taxonomy category
- `display.tags`: Searchable tags

**Package configuration by type**:

For OCI packages:
```json
{
  "registryType": "oci",
  "registryBaseUrl": "https://docker.io",
  "identifier": "owner/image-name",
  "version": "1.0.0",
  "transport": {
    "type": "streamable-http",
    "url": "https://mcp.nimbletools.ai/mcp"
  }
}
```

For MCPB packages (one entry per architecture):
```json
{
  "registryType": "mcpb",
  "identifier": "https://github.com/owner/repo/releases/download/v1.0.0/bundle-v1.0.0-linux-amd64.mcpb",
  "version": "1.0.0",
  "fileSha256": "sha256-hash-for-this-architecture",
  "transport": {
    "type": "streamable-http",
    "url": "http://localhost:8000/mcp"
  }
}
```

MCPB bundles require:
- One package entry per architecture (linux-amd64, linux-arm64)
- `identifier` as the full download URL
- `fileSha256` for integrity verification (compute with `shasum -a 256 bundle.mcpb`)

**Environment variables**:
```json
{
  "environmentVariables": [
    {
      "name": "API_KEY",
      "description": "Description of the variable",
      "isRequired": true,      // true if server won't work without it
      "isSecret": true,        // true for API keys, tokens, passwords
      "placeholder": "your_api_key_here"  // example value for documentation
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
  "$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/echo",
  "version": "1.0.0",
  "title": "Echo",
  "description": "Simple echo service for testing",
  "icons": [
    { "src": "https://static.nimbletools.ai/icons/echo.png", "sizes": ["64x64"] }
  ],
  "repository": {
    "url": "https://github.com/NimbleBrainInc/mcp-echo",
    "source": "github"
  },
  "packages": [{
    "registryType": "oci",
    "identifier": "nimbletools/mcp-echo",
    "version": "1.0.0",
    "transport": {
      "type": "streamable-http",
      "url": "https://mcp.nimbletools.ai/mcp"
    }
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "status": "active",
      "repository": { "branch": "main" },
      "container": {
        "healthCheck": { "path": "/health", "port": 8000 }
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
  "$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/finnhub",
  "version": "1.0.0",
  "title": "Finnhub",
  "description": "Real-time stock prices, company financials, and market data",
  "icons": [
    { "src": "https://static.nimbletools.ai/icons/finnhub.png", "sizes": ["64x64"] }
  ],
  "packages": [{
    "registryType": "oci",
    "identifier": "nimbletools/mcp-finnhub",
    "version": "1.0.0",
    "transport": {
      "type": "streamable-http",
      "url": "https://mcp.nimbletools.ai/mcp"
    },
    "environmentVariables": [{
      "name": "FINNHUB_API_KEY",
      "description": "Finnhub API key",
      "isRequired": true,
      "isSecret": true,
      "placeholder": "your_finnhub_api_key"
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

### Example 3: MCPB bundle (ipinfo)

`servers/ipinfo/server.json` (showing both architecture packages):
```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/ipinfo",
  "version": "0.1.0",
  "title": "IPInfo",
  "description": "IP geolocation, ASN, and network information via IPInfo API",
  "icons": [
    { "src": "https://static.nimbletools.ai/icons/ipinfo.png", "sizes": ["64x64"] }
  ],
  "repository": {
    "url": "https://github.com/NimbleBrainInc/mcp-ipinfo",
    "source": "github"
  },
  "packages": [
    {
      "registryType": "mcpb",
      "identifier": "https://github.com/NimbleBrainInc/mcp-ipinfo/releases/download/v0.1.0/mcp-ipinfo-v0.1.0-linux-amd64.mcpb",
      "version": "0.1.0",
      "fileSha256": "5e5627aa28fc0fbac041090ffe9c9524e6afe7d701e3f02efed8897487e81495",
      "transport": { "type": "streamable-http", "url": "http://localhost:8000/mcp" },
      "environmentVariables": [{
        "name": "IPINFO_API_TOKEN",
        "description": "IPInfo API token",
        "isRequired": false,
        "isSecret": true
      }]
    },
    {
      "registryType": "mcpb",
      "identifier": "https://github.com/NimbleBrainInc/mcp-ipinfo/releases/download/v0.1.0/mcp-ipinfo-v0.1.0-linux-arm64.mcpb",
      "version": "0.1.0",
      "fileSha256": "3ec1fb06719c378c47120ad240d827195e206af10e1afd84107b2832fdd41c23",
      "transport": { "type": "streamable-http", "url": "http://localhost:8000/mcp" },
      "environmentVariables": [{
        "name": "IPINFO_API_TOKEN",
        "description": "IPInfo API token",
        "isRequired": false,
        "isSecret": true
      }]
    }
  ],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "runtime": "python:3.14",
      "status": "active",
      "container": { "healthCheck": { "path": "/health", "port": 8000 } },
      "deployment": { "protocol": "http", "port": 8000, "mcpPath": "/mcp" }
    }
  }
}
```

Note the key differences from OCI:
- `registryType`: `"mcpb"` instead of `"oci"`
- `identifier`: Full download URL for the bundle
- `fileSha256`: Checksum for this specific architecture bundle
- One package entry per architecture (amd64 and arm64)
- `runtime`: Specified in `_meta` (e.g., `python:3.14`, `node:24`, `supergateway-python:3.14`)

## Checklist

Before submitting:

- [ ] `server.json` validates with schema
- [ ] Package type is `oci` or `mcpb` with appropriate configuration
- [ ] For MCPB: One package entry per architecture with correct `fileSha256`
- [ ] For MCPB: Runtime is specified in `_meta.ai.nimbletools.mcp/v1.runtime`
- [ ] Health check endpoint is correct
- [ ] Environment variables marked as `isSecret` and `isRequired` appropriately
- [ ] `test.json` includes at least one basic test
- [ ] Test runs successfully with `npm run test:e2e -- --server={name}`
- [ ] Container image (OCI) or GitHub releases (MCPB) are publicly accessible
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

**Issue**: MCPB checksum mismatch
- Re-download the bundle from GitHub releases
- Compute SHA256: `shasum -a 256 bundle.mcpb`
- Update `fileSha256` in the corresponding package entry

**Issue**: Stdio server not working
- For stdio-based servers, use MCPB with `supergateway-python:3.14` runtime
- The supergateway runtime wraps stdio servers to expose HTTP

## Getting Help

- Review existing servers in `servers/` directory for examples
- Check schema documentation: https://registry.nimbletools.ai/schemas
- Test locally with `npm run test:e2e` before submitting
- Open an issue if you need assistance

## Agent Workflow

If you are an AI agent adding a server:

1. **Fetch repository**: Clone or analyze the GitHub repo
2. **Identify package type**:
   - Has Dockerfile with HTTP server? → Use OCI
   - Python/Node source code? → Use MCPB with appropriate runtime
   - Stdio-only server? → Use MCPB with `supergateway-python:3.14` runtime
3. **Find package source**:
   - OCI: Look for published images on Docker Hub/GHCR
   - MCPB: Check for GitHub releases with `.mcpb` bundles
4. **Extract tools**: Read server code or documentation to list available MCP tools
5. **Map environment variables**: Find all required configuration/secrets
6. **Generate server.json**: Use the appropriate template (OCI or MCPB)
7. **For MCPB**: Download bundles and compute SHA256 checksums
8. **Create test.json**: Write at least one test for the primary tool
9. **Validate**: Run `npm run validate-servers`

When in doubt, prefer:
- MCPB over OCI (simpler to maintain)
- Simple tests with `"type": "any"` expectations
- Conservative resource limits (256Mi/100m)
- Marking variables as `isSecret: true` if they look sensitive