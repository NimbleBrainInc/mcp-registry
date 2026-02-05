# NimbleBrain MCP Registry

[![Live Registry](https://img.shields.io/badge/Live%20Registry-registry.nimblebrain.ai-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMiA3VjE3TDEyIDIyTDIyIDE3VjdMMTIgMloiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIvPgo8L3N2Zz4=)](https://registry.nimblebrain.ai)

![GitHub License](https://img.shields.io/github/license/NimbleBrainInc/mcp-registry)
[![Actions status](https://github.com/NimbleBrainInc/mcp-registry/actions/workflows/ci.yml/badge.svg)](https://github.com/NimbleBrainInc/mcp-registry/actions)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white)](https://www.nimbletools.ai/discord?utm_source=github&utm_medium=readme&utm_campaign=mcp-registry&utm_content=header-badge)

A curated registry of Model Context Protocol (MCP) servers optimized for the NimbleBrain runtime platform.

🌐 **Live at: https://registry.nimblebrain.ai**

📚 **API Docs: https://registry.nimblebrain.ai/docs**

## Overview

This registry provides a REST API for discovering MCP servers, implementing a subset of the [official MCP Registry API](https://github.com/modelcontextprotocol/registry/). While the official registry focuses on broad ecosystem support, this registry is specifically curated for servers that work well with the NimbleBrain platform.

### Why This Registry?

- **Curated Selection**: Only includes servers tested and optimized for NimbleBrain's runtime
- **Extended Metadata**: Adds platform-specific configuration for health checks, resource limits, and deployment settings
- **Deployment-Ready**: Servers are packaged as OCI containers or MCPB bundles for seamless deployment
- **API Compatibility**: Implements the core MCP Registry API for easy integration

## API Endpoints

```
GET /                                              # API info and available endpoints
GET /v0.1/servers                                  # List all servers (with search, pagination)
GET /v0.1/servers/{name}/versions/{version}        # Get specific server version
GET /v0.1/health                                   # Health check
GET /schemas                                       # List available schema versions
GET /docs                                          # Interactive API documentation (Swagger UI)
```

### Query Parameters (GET /v0.1/servers)

| Parameter | Description |
|-----------|-------------|
| `search` | Case-insensitive search on name, title, description |
| `version` | Filter by version (`latest` supported) |
| `limit` | Results per page (default 100, max 500) |
| `cursor` | Pagination cursor |

### Example API Calls

```bash
# List all servers
curl https://registry.nimblebrain.ai/v0.1/servers

# Search for servers
curl "https://registry.nimblebrain.ai/v0.1/servers?search=weather"

# Get specific server version
curl https://registry.nimblebrain.ai/v0.1/servers/ai.nimbletools%2Ffinnhub/versions/latest

# Check health
curl https://registry.nimblebrain.ai/v0.1/health
```

## Server Schema

Servers follow the [MCP server schema (2025-12-11)](https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json) with additional NimbleBrain-specific metadata:

```json
{
  "$schema": "https://registry.nimblebrain.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/example",
  "version": "1.0.0",
  "title": "Example Server",
  "description": "Example MCP server",
  "packages": [{
    "registryType": "mcpb",
    "identifier": "https://github.com/example/releases/download/v1.0.0/example.mcpb",
    "version": "1.0.0",
    "transport": { "type": "streamable-http" },
    "environmentVariables": [{
      "name": "API_KEY",
      "isRequired": true,
      "isSecret": true
    }]
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "runtime": "python:3.14",
      "status": "active"
    }
  }
}
```

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Validate all server definitions
npm run validate-servers

# Run tests
npm test
```

## Deployment

```bash
# Deploy to production
make deploy ENV=production

# Check deployment status
make status

# View logs
make logs
```

## Releasing

Use `npm version` to bump the version and create a git tag:

```bash
npm version patch   # 1.0.0 -> 1.0.1 (bug fixes)
npm version minor   # 1.0.0 -> 1.1.0 (new features)
npm version major   # 1.0.0 -> 2.0.0 (breaking changes)

git push && git push --tags
```

Verify after deployment:

```bash
curl https://registry.nimblebrain.ai/
# Returns: { "version": "v0.2.1", ... }
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new servers to the registry.

## License

Apache 2.0 - See [LICENSE](LICENSE) file for details.
