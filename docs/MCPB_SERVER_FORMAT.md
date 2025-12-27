# MCPB Server Format

Guide for defining MCPB-based servers in the NimbleTools registry.

## Overview

All servers in the registry use MCPB (MCP Bundle) format with streamable-http transport. Bundles are hosted on GitHub Releases and downloaded by the runtime at deployment time.

## Server Definition

### Basic Structure

```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/echo",
  "version": "1.0.0",
  "title": "Echo Server",
  "description": "Echo server for testing and debugging MCP connections",
  "packages": [{
    "registryType": "mcpb",
    "registryBaseUrl": "https://github.com/NimbleBrainInc/mcp-echo/releases/download",
    "identifier": "mcp-echo",
    "version": "1.0.0",
    "transport": {
      "type": "streamable-http"
    },
    "environmentVariables": []
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "runtime": "python:3.14",
      "status": "active",
      "resources": {...},
      "scaling": {...},
      "display": {...}
    }
  }
}
```

### Package Configuration

#### registryType

Always `mcpb` for bundle-based servers.

```json
"registryType": "mcpb"
```

#### registryBaseUrl

GitHub Releases base URL for the bundle.

```json
"registryBaseUrl": "https://github.com/NimbleBrainInc/mcp-echo/releases/download"
```

The full bundle URL is constructed as:
```
{registryBaseUrl}/v{version}/{identifier}-v{version}.mcpb
```

Example:
```
https://github.com/NimbleBrainInc/mcp-echo/releases/download/v1.0.0/mcp-echo-v1.0.0.mcpb
```

#### identifier

Bundle filename prefix (without version).

```json
"identifier": "mcp-echo"
```

#### version

Semantic version matching the GitHub Release tag.

```json
"version": "1.0.0"
```

#### transport

Always streamable-http for MCPB servers.

```json
"transport": {
  "type": "streamable-http"
}
```

#### environmentVariables

User-configurable environment variables.

```json
"environmentVariables": [
  {
    "name": "API_KEY",
    "description": "API key for authentication",
    "isRequired": true,
    "isSecret": true
  },
  {
    "name": "DEBUG",
    "description": "Enable debug logging",
    "isRequired": false,
    "isSecret": false,
    "default": "false"
  }
]
```

### Runtime Configuration

The `_meta.ai.nimbletools.mcp/v1.runtime` field determines which base image to use.

| runtime | Base Image |
|---------|------------|
| `python` | ghcr.io/nimblebrain/mcpb-python:latest |
| `python:3.14` | ghcr.io/nimblebrain/mcpb-python:3.14 |
| `python:3.13` | ghcr.io/nimblebrain/mcpb-python:3.13 |
| `node` | ghcr.io/nimblebrain/mcpb-node:latest |
| `node:24` | ghcr.io/nimblebrain/mcpb-node:24 |
| `node:22` | ghcr.io/nimblebrain/mcpb-node:22 |

## Complete Example

### Python Server

```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/echo",
  "version": "1.0.0",
  "title": "Echo Server",
  "description": "Echo server for testing and debugging MCP connections",
  "icons": [
    {
      "src": "https://raw.githubusercontent.com/NimbleBrainInc/mcp-echo/main/icons/icon-64.png",
      "sizes": ["64x64"]
    }
  ],
  "repository": {
    "url": "https://github.com/NimbleBrainInc/mcp-echo",
    "source": "github"
  },
  "packages": [{
    "registryType": "mcpb",
    "registryBaseUrl": "https://github.com/NimbleBrainInc/mcp-echo/releases/download",
    "identifier": "mcp-echo",
    "version": "1.0.0",
    "transport": {
      "type": "streamable-http"
    },
    "environmentVariables": [
      {
        "name": "DEBUG",
        "description": "Enable debug logging",
        "isRequired": false,
        "isSecret": false
      }
    ]
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "runtime": "python:3.14",
      "status": "active",
      "container": {
        "healthCheck": {
          "enabled": true,
          "path": "/health",
          "port": 8000,
          "initialDelaySeconds": 15,
          "periodSeconds": 10
        }
      },
      "resources": {
        "requests": {"memory": "128Mi", "cpu": "50m"},
        "limits": {"memory": "256Mi", "cpu": "200m"}
      },
      "scaling": {
        "enabled": true,
        "minReplicas": 1,
        "maxReplicas": 3,
        "targetCPUUtilizationPercentage": 80
      },
      "deployment": {
        "protocol": "http",
        "port": 8000,
        "mcpPath": "/mcp"
      },
      "capabilities": {
        "tools": true,
        "resources": false,
        "prompts": false
      },
      "display": {
        "category": "developer-tools",
        "tags": ["testing", "debugging"],
        "documentation": {
          "readmeUrl": "https://github.com/NimbleBrainInc/mcp-echo/blob/main/README.md"
        }
      }
    }
  }
}
```

### Node.js Server

```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/github",
  "version": "1.0.0",
  "title": "GitHub",
  "description": "GitHub API integration for repositories, issues, and PRs",
  "packages": [{
    "registryType": "mcpb",
    "registryBaseUrl": "https://github.com/NimbleBrainInc/mcp-github/releases/download",
    "identifier": "mcp-github",
    "version": "1.0.0",
    "transport": {
      "type": "streamable-http"
    },
    "environmentVariables": [
      {
        "name": "GITHUB_TOKEN",
        "description": "GitHub personal access token",
        "isRequired": true,
        "isSecret": true
      }
    ]
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "runtime": "node:24",
      "status": "active",
      "resources": {
        "requests": {"memory": "128Mi", "cpu": "50m"},
        "limits": {"memory": "256Mi", "cpu": "200m"}
      },
      "display": {
        "category": "developer-tools",
        "tags": ["github", "version-control"]
      }
    }
  }
}
```

## Migration from Legacy Formats

### From OCI/Docker

Before:
```json
{
  "packages": [{
    "registryType": "oci",
    "registryBaseUrl": "https://docker.io",
    "identifier": "nimbletools/mcp-echo",
    "version": "1.0.0",
    "transport": {"type": "streamable-http"}
  }]
}
```

After:
```json
{
  "packages": [{
    "registryType": "mcpb",
    "registryBaseUrl": "https://github.com/NimbleBrainInc/mcp-echo/releases/download",
    "identifier": "mcp-echo",
    "version": "1.0.0",
    "transport": {"type": "streamable-http"}
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "runtime": "python:3.14"
    }
  }
}
```

### From npm/npx

Before:
```json
{
  "packages": [{
    "registryType": "npm",
    "identifier": "@modelcontextprotocol/server-tavily",
    "version": "0.2.9",
    "transport": {"type": "stdio"},
    "runtimeHint": "npx",
    "runtimeArguments": [
      {"type": "positional", "value": "@modelcontextprotocol/server-tavily"}
    ]
  }]
}
```

After:
```json
{
  "packages": [{
    "registryType": "mcpb",
    "registryBaseUrl": "https://github.com/NimbleBrainInc/mcp-tavily/releases/download",
    "identifier": "mcp-tavily",
    "version": "1.0.0",
    "transport": {"type": "streamable-http"}
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "runtime": "node:24"
    }
  }
}
```

### From pypi/uvx

Before:
```json
{
  "packages": [{
    "registryType": "pypi",
    "identifier": "postgres-mcp",
    "version": "0.3.0",
    "transport": {"type": "stdio"},
    "runtimeHint": "uvx"
  }]
}
```

After:
```json
{
  "packages": [{
    "registryType": "mcpb",
    "registryBaseUrl": "https://github.com/NimbleBrainInc/mcp-postgres/releases/download",
    "identifier": "mcp-postgres",
    "version": "1.0.0",
    "transport": {"type": "streamable-http"}
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "runtime": "python:3.14"
    }
  }
}
```

## Bundle URL Patterns

### GitHub Releases (Standard)

```json
"registryBaseUrl": "https://github.com/{org}/{repo}/releases/download"
```

URL: `https://github.com/{org}/{repo}/releases/download/v{version}/{identifier}-v{version}.mcpb`

### Direct URL (Custom)

For non-GitHub hosting, use `bundleUrl` instead:

```json
"packages": [{
  "registryType": "mcpb",
  "bundleUrl": "https://example.com/bundles/my-server-v1.0.0.mcpb",
  "version": "1.0.0",
  "transport": {"type": "streamable-http"}
}]
```

## Validation

Run validation before committing:

```bash
npm run validate-servers
```

Validates:
- Schema compliance
- Required fields present
- registryType is "mcpb"
- transport.type is "streamable-http"
- runtime is specified in _meta
- Bundle URL is constructable

## Creating a New Server Entry

1. Create the MCP server and publish bundle to GitHub Releases
2. Create `servers/{name}/server.json`:
   ```bash
   mkdir -p servers/my-server
   ```
3. Add server definition following the template above
4. Add test fixtures in `servers/{name}/test.json`
5. Run validation:
   ```bash
   npm run validate-servers
   ```
6. Submit PR

See [ADDING_SERVERS.md](./ADDING_SERVERS.md) for detailed instructions.
