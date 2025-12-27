# Contributing to NimbleTools MCP Registry

Thank you for your interest in contributing MCP servers to the NimbleTools registry!

## Adding a New Server

### 1. Prerequisites

Before submitting a server, ensure it:
- Implements the [Model Context Protocol](https://modelcontextprotocol.io) specification
- Has a public GitHub repository
- Is packaged as either:
  - **OCI container** (Docker image that exposes HTTP endpoints), OR
  - **MCPB bundle** (GitHub release with `.mcpb` artifacts)
- Has clear documentation and examples

### 2. Create Server Definition

Create a new directory under `servers/` with your server name:

```bash
servers/
└── your-server-name/
    └── server.json
```

### 3. Server JSON Structure

Your `server.json` must follow the 2025-12-11 schema:

```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json",
  "name": "ai.nimbletools/your-server",
  "version": "1.0.0",
  "title": "Your Server Display Name",
  "description": "Brief description under 100 characters",
  "icons": [
    { "src": "https://static.nimbletools.ai/icons/your-server.png", "sizes": ["64x64"] }
  ],
  "repository": {
    "url": "https://github.com/yourusername/your-server",
    "source": "github"
  },
  "websiteUrl": "https://your-documentation-site.com",
  "packages": [
    {
      "registryType": "oci",
      "registryBaseUrl": "https://docker.io",
      "identifier": "yourdockerhub/your-server",
      "version": "1.0.0",
      "transport": {
        "type": "streamable-http",
        "url": "https://mcp.nimbletools.ai/mcp"
      },
      "environmentVariables": [
        {
          "name": "API_KEY",
          "description": "Your API key description",
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
      }
    }
  }
}
```

### 4. Validation

Validate your server definition:

```bash
npm run validate-servers
```

This ensures your server:
- Has all required fields
- Uses semantic versioning (not "latest")
- Has descriptions under 100 characters
- Follows the MCP schema requirements

### 5. Testing

#### Prerequisites

Install NimbleTools Core:

```bash
curl -sSL https://raw.githubusercontent.com/NimbleBrainInc/nimbletools-core/refs/heads/main/install.sh | bash
```

#### Running E2E Tests

Run all tests (parallel by default):
```bash
npm run test:e2e
```

Run individual server tests:
```bash
npm run test:e2e -- --server=github
```

See `npm run test:e2e -- --help` for all CLI options including `--concurrency`, `--domain`, and `--insecure`.

#### Test Definition

Create a `test.json` file alongside your `server.json`:

```json
{
  "skip": false,
  "tests": [
    {
      "name": "Echo basic message",
      "tool": "echo_message",
      "arguments": {
        "message": "Hello E2E Test"
      },
      "expect": {
        "type": "json",
        "field": "echoed_message",
        "equals": "Hello E2E Test"
      }
    }
  ]
}
```

- `skip`: Set to `true` to skip tests for this server
- `name`: Descriptive test name
- `tool`: Tool name to invoke
- `arguments`: Input parameters for the tool
- `expect`: Expected output validation
  - `type`: Response type (`"json"`)
  - `field`: JSON field to validate
  - `equals`: Expected value

### 6. Submit Pull Request

1. Fork this repository
2. Create a feature branch: `git checkout -b add-your-server-name`
3. Add your server definition
4. Run validation: `npm run validate-servers`
5. Commit your changes: `git commit -m "Add your-server-name MCP server"`
6. Push to your fork: `git push origin add-your-server-name`
7. Create a Pull Request

## Server Requirements

### Required Fields

- `name`: Must use namespace format (e.g., `ai.nimbletools/server-name`)
- `version`: Semantic version (e.g., `1.0.0`, not `latest`)
- `description`: Clear, concise description (max 100 characters)
- `packages`: At least one package definition with:
  - `registryType`: `"oci"` for Docker containers or `"mcpb"` for bundles
  - `identifier`: Docker image name (OCI) or bundle identifier (MCPB)
  - `version`: Specific version (not `latest`)
  - `transport.type`: `"streamable-http"`
  - For MCPB: `fileSha256` checksum (one package entry per architecture)

### NimbleTools Metadata

The `_meta["ai.nimbletools.mcp/v1"]` section should include:

- **runtime** (MCPB only): Base runtime for the bundle (e.g., `python:3.13`, `node:24`, `supergateway-python:3.14`, `binary`)
- **capabilities**: List of tools, resources, and prompts your server provides
- **resources**: Memory and CPU limits/requests for Kubernetes
- **container**: Health check configuration
- **deployment**: Protocol and port configuration

## Guidelines

### Naming Conventions

- Server names should be lowercase with hyphens (e.g., `my-server`)
- Tool names should use snake_case (e.g., `get_data`)
- Use clear, descriptive names

### Versioning

- Follow [Semantic Versioning](https://semver.org/)
- Update version when making breaking changes
- Never use `latest` as a version

## Questions?

If you have questions about contributing, please:
1. Check existing servers in `servers/` for examples
2. Review the [MCP documentation](https://modelcontextprotocol.io)
3. Open an issue for discussion

Thank you for contributing to the NimbleTools MCP ecosystem!