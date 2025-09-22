# NimbleBrain MCP Registry

A curated registry of Model Context Protocol (MCP) servers optimized for the NimbleBrain runtime platform.

## Overview

This registry provides a REST API for discovering MCP servers, implementing a subset of the [official MCP Registry API](https://github.com/modelcontextprotocol/registry/). While the official registry focuses on broad ecosystem support, this registry is specifically curated for servers that work well with the NimbleBrain platform.

### Why This Registry?

- **Curated Selection**: Only includes servers tested and optimized for NimbleBrain's runtime
- **Extended Metadata**: Adds platform-specific configuration for health checks, resource limits, and deployment settings
- **Container-Ready**: All servers are packaged as OCI containers for seamless deployment
- **API Compatibility**: Implements the core MCP Registry API for easy integration

## API Endpoints

The registry provides the following REST endpoints:

```
GET /                                    # API info and available endpoints
GET /v0/servers                         # List all servers
GET /v0/servers/{server_id}            # Get specific server details
GET /v0/servers/{server_id}/versions   # Get server versions
GET /schemas                           # List available schema versions
GET /schemas/latest/{filename}         # Get latest schema
GET /schemas/{version}/{filename}      # Get specific schema version
GET /health                            # Health check
```

Base URL: `https://registry.nimblebrain.ai`

## Server Schema

Our servers follow the [MCP server schema](https://modelcontextprotocol.io/schemas) with additional NimbleBrain-specific metadata:

```json
{
  "$schema": "https://registry.nimblebrain.ai/schemas/2025-09-22/nimblebrain-server.schema.json",
  "name": "ai.nimblebrain/example",
  "version": "1.0.0",
  "description": "Example MCP server",
  "packages": [{
    "registryType": "oci",
    "identifier": "nimbletools/example",
    "version": "1.0.0",
    "transport": { "type": "stdio" }
  }],
  "_meta": {
    "ai.nimblebrain.mcp/v1": {
      "container": {
        "healthCheck": {
          "path": "/health",
          "port": 8000
        }
      },
      "resources": {
        "limits": { "memory": "256Mi", "cpu": "100m" }
      }
    }
  }
}
```

## Development

### Prerequisites

- Node.js 22+
- Docker (for building server images)

### Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Validate all server definitions
npm run validate-servers

# Build for production
npm run build

# Run tests
npm test
```

### Docker

```bash
# Build Docker image
docker build -t nimblebrain-registry .

# Run container
docker run -p 8080:8080 nimblebrain-registry
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new servers to the registry.

## License

Apache 2.0 - See [LICENSE](LICENSE) file for details.