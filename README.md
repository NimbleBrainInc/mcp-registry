# NimbleBrain MCP Registry

[![Live Registry](https://img.shields.io/badge/Live%20Registry-registry.nimbletools.ai-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMiA3VjE3TDEyIDIyTDIyIDE3VjdMMTIgMloiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIvPgo8L3N2Zz4=)](https://registry.nimbletools.ai)

![GitHub License](https://img.shields.io/github/license/NimbleBrainInc/mcp-registry)
[![Actions status](https://github.com/NimbleBrainInc/mcp-registry/actions/workflows/ci.yml/badge.svg)](https://github.com/NimbleBrainInc/mcp-registry/actions)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white)](https://www.nimbletools.ai/discord?utm_source=github&utm_medium=readme&utm_campaign=mcp-registry&utm_content=header-badge)

A curated registry of Model Context Protocol (MCP) servers optimized for the NimbleBrain runtime platform.

🌐 **Live at: https://registry.nimbletools.ai**

📚 **API Docs: https://registry.nimbletools.ai/docs**

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
GET /docs                              # Interactive API documentation (Swagger UI)
```

**Base URL:** `https://registry.nimbletools.ai`
**API Documentation:** `https://registry.nimbletools.ai/docs` (Interactive Swagger UI)

### Example API Calls

```bash
# List all servers
curl https://registry.nimbletools.ai/v0/servers

# Get specific server
curl https://registry.nimbletools.ai/v0/servers/ai.nimbletools%2Ffinnhub

# Check health
curl https://registry.nimbletools.ai/health
```

## Server Schema

Our servers follow the [MCP server schema](https://modelcontextprotocol.io/schemas) with additional NimbleBrain-specific metadata:

```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-09-22/nimbletools-server.schema.json",
  "name": "ai.nimbletools/example",
  "version": "1.0.0",
  "description": "Example MCP server",
  "packages": [{
    "registryType": "oci",
    "identifier": "nimbletools/example",
    "version": "1.0.0",
    "transport": { "type": "stdio" }
  }],
  "_meta": {
    "ai.nimbletools.mcp/v1": {
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

## Deployment

This registry is automatically deployed to **https://registry.nimbletools.ai** via GitHub Actions on every push to the main branch.

### Infrastructure
- **Hosting:** Fly.io
- **Region:** Global (auto-scaled)
- **API:** Fastify + Node.js 22
- **CI/CD:** GitHub Actions

### Deployment Process
1. Push to `main` branch triggers CI/CD pipeline
2. Tests and type checking run
3. Docker image built and pushed to registry
4. Automatic deployment to Fly.io
5. Health checks verify deployment

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

# Run end-to-end tests
npm run test:e2e                    # Test all servers
npm run test:e2e -- --server=echo   # Test specific server
```

### End-to-End Testing

The registry includes a comprehensive E2E testing framework that validates servers from deployment through MCP connectivity:

```bash
# Test all servers
npm run test:e2e

# Test a specific server
npm run test:e2e -- --server=echo

# Test against a different API endpoint
npm run test:e2e http://api.custom.dev
```

**Test Fixtures**: Each server can define custom tests in `servers/{name}/test.json`:

```json
{
  "environment": {
    "API_KEY": "${API_KEY}"
  },
  "tests": [{
    "name": "Test description",
    "tool": "tool_name",
    "arguments": { "param": "value" },
    "expect": { "type": "text", "contains": "expected" }
  }]
}
```

**Environment Variables**: Create `.env.e2e` for secrets:

```bash
cp .env.e2e.example .env.e2e
# Edit .env.e2e with your API keys
```

The test runner automatically:
- Creates workspaces
- Sets secrets from fixtures
- Deploys servers
- Validates MCP connectivity
- Runs custom tool tests
- Cleans up resources

### Docker

```bash
# Build Docker image
docker build -t nimbletools-registry .

# Run container
docker run -p 8080:8080 nimbletools-registry
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new servers to the registry.

## License

Apache 2.0 - See [LICENSE](LICENSE) file for details.