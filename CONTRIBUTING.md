# Contributing to NimbleTools MCP Registry

Thank you for your interest in contributing MCP servers to the NimbleTools registry!

## Adding a New Server

### 1. Prerequisites

Before submitting a server, ensure it:
- Implements the [Model Context Protocol](https://modelcontextprotocol.io) specification
- Has a public GitHub repository
- Is packaged as a Docker container
- Has clear documentation and examples

### 2. Create Server Definition

Create a new directory under `servers/` with your server name:

```bash
servers/
└── your-server-name/
    └── server.json
```

### 3. Server JSON Structure

Your `server.json` must follow our schema:

```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-09-22/nimbletools-server.schema.json",
  "name": "ai.nimbletools/your-server",
  "version": "1.0.0",
  "description": "Brief description under 100 characters",
  "status": "active",
  "repository": {
    "url": "https://github.com/yourusername/your-server",
    "source": "github",
    "branch": "main"
  },
  "websiteUrl": "https://your-documentation-site.com",
  "packages": [
    {
      "registryType": "oci",
      "registryBaseUrl": "https://docker.io",
      "identifier": "yourdockerhub/your-server",
      "version": "1.0.0",
      "transport": {
        "type": "stdio"
      },
      "environmentVariables": [
        {
          "name": "API_KEY",
          "description": "Your API key description",
          "isRequired": true,
          "isSecret": true,
          "example": "your_api_key_here"
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
        "tools": [
          {
            "name": "tool_name",
            "description": "What this tool does",
            "schema": {
              "type": "object",
              "properties": {
                "input": {
                  "type": "string",
                  "description": "Input description"
                }
              },
              "required": ["input"]
            }
          }
        ]
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

Test that your server works:

1. **Docker Image**: Ensure your Docker image is publicly accessible
2. **MCP Compliance**: Verify your server implements MCP correctly
3. **Health Check**: If using HTTP transport, ensure health endpoint works

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
  - `registryType`: Usually `"oci"` for Docker containers
  - `identifier`: Docker image name
  - `version`: Specific version (not `latest`)
  - `transport`: Either `"stdio"` or `"http"`

### NimbleTools Metadata

The `_meta["ai.nimbletools.mcp/v1"]` section should include:

- **capabilities**: List of tools, resources, and prompts your server provides
- **resources**: Memory and CPU limits/requests for Kubernetes
- **container**: Health check configuration for HTTP servers
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

### Documentation

Include in your server repository:
- Clear README with usage examples
- API documentation for all tools
- Environment variable descriptions
- Docker usage instructions

## Questions?

If you have questions about contributing, please:
1. Check existing servers in `servers/` for examples
2. Review the [MCP documentation](https://modelcontextprotocol.io)
3. Open an issue for discussion

Thank you for contributing to the NimbleTools MCP ecosystem!