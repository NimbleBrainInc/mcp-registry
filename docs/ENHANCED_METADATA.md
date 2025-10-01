# Enhanced Metadata for MCP Registry

This document describes the enhanced metadata capabilities added to the NimbleBrain MCP Registry for better discoverability, branding, and documentation.

## Overview

The enhanced metadata system adds support for:
- **Categories & Tags**: Improve searchability and organization
- **Branding**: Visual identity with logos and colors
- **Documentation**: Automatic README fetching and rendering
- **Showcase**: Screenshots, videos, and featured content
- **Metrics**: Usage statistics and popularity indicators

## Categories

The registry supports the following standard categories:

| Category | Description | Use Case |
|----------|-------------|----------|
| `ai-ml` | AI and Machine Learning | LLMs, vision models, NLP |
| `data` | Data Processing & ETL | Data pipelines, transformations |
| `development` | Development Tools | Code editors, linters, formatters |
| `productivity` | Productivity Tools | Task management, notes, calendars |
| `communication` | Communication | Email, chat, notifications |
| `finance` | Financial Services | Trading, accounting, payments |
| `media` | Media Processing | Images, video, audio |
| `security` | Security Tools | Authentication, encryption, scanning |
| `devops` | DevOps & CI/CD | Deployment, monitoring, testing |
| `monitoring` | Monitoring & Observability | Metrics, logs, traces |
| `storage` | Storage & Databases | File storage, databases, caching |
| `web` | Web Services | HTTP, REST, GraphQL |
| `blockchain` | Blockchain & Crypto | Web3, smart contracts, wallets |
| `gaming` | Gaming Services | Game engines, multiplayer, assets |
| `education` | Educational Tools | Learning, courses, documentation |
| `health` | Health & Fitness | Medical, fitness tracking |
| `utilities` | General Utilities | Converters, calculators, helpers |
| `integration` | Integration Platforms | Zapier, IFTTT alternatives |
| `analytics` | Analytics & BI | Data analysis, reporting |
| `automation` | Automation Tools | Workflows, scripts, bots |

## Usage Example

Add the enhanced metadata to your `server.json` file within the `_meta["ai.nimbletools.mcp/v1"].registry` section:

```json
{
  "$schema": "https://registry.nimbletools.ai/schemas/2025-09-22/nimbletools-server.schema.json",
  "name": "ai.nimbletools/your-server",
  "version": "1.0.0",
  "description": "Your MCP server description",
  "repository": {
    "url": "https://github.com/yourusername/your-server",
    "source": "github",
    "branch": "main"
  },
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "registry": {
        "categories": ["development", "productivity"],
        "tags": ["code", "automation", "assistant", "tools"],
        "branding": {
          "logoUrl": "https://example.com/logo.svg",
          "iconUrl": "https://example.com/icon.png",
          "primaryColor": "#0066CC",
          "accentColor": "#FF6B6B"
        },
        "documentation": {
          "readmeUrl": "https://raw.githubusercontent.com/yourusername/your-server/main/README.md",
          "changelogUrl": "https://github.com/yourusername/your-server/blob/main/CHANGELOG.md",
          "licenseUrl": "https://github.com/yourusername/your-server/blob/main/LICENSE",
          "examplesUrl": "https://github.com/yourusername/your-server/tree/main/examples"
        },
        "showcase": {
          "featured": false,
          "screenshots": [
            {
              "url": "https://example.com/screenshot1.png",
              "caption": "Main interface showing key features",
              "thumbnail": "https://example.com/screenshot1-thumb.png"
            }
          ],
          "videoUrl": "https://www.youtube.com/watch?v=your-video-id"
        }
      }
    }
  }
}
```

## Automatic README Fetching

The registry automatically fetches and caches README files from GitHub repositories. This happens in two ways:

1. **Automatic**: If your server has a `repository.url` field pointing to GitHub, the README will be fetched automatically.

2. **Explicit**: You can specify a custom README URL in the `documentation.readmeUrl` field.

The README content is:
- Fetched from the repository's default branch
- Cached for 1 hour to reduce API calls
- Sanitized to remove potentially dangerous HTML/scripts
- Available in the API response for rendering in the UI

## Best Practices

1. **Categories**: Choose 1-3 most relevant categories. Be specific rather than broad.

2. **Tags**: Use lowercase, hyphenated tags. Keep them relevant and searchable.

3. **Logos**:
   - Use SVG for logos when possible (scalable, small file size)
   - Provide both logo (wide) and icon (square) versions
   - Keep file sizes under 500KB

4. **Screenshots**:
   - Use descriptive captions
   - Provide thumbnails for faster loading
   - Limit to 5 most important views

5. **Colors**:
   - Use your brand's primary colors
   - Ensure good contrast for accessibility
   - Use standard hex format (#RRGGBB)

## API Response

When fetching server details, the enhanced metadata is included in the response:

```json
{
  "name": "ai.nimbletools/your-server",
  "version": "1.0.0",
  "description": "Your server description",
  "_meta": {
    "ai.nimbletools.mcp/v1": {
      "registry": {
        "categories": ["development"],
        "tags": ["code", "tools"],
        "documentation": {
          "readmeContent": "# Your Server\n\nFull markdown content...",
          "readmeUrl": "https://..."
        }
        // ... other metadata
      }
    }
  }
}
```

## Migration Guide

To migrate existing servers to use enhanced metadata:

1. Update your `server.json` schema reference to the latest version
2. Add the `registry` section under `_meta["ai.nimbletools.mcp/v1"]`
3. Start with categories and tags (most important for discoverability)
4. Add branding assets as they become available
5. The README will be fetched automatically if you have a repository URL

## Validation

Use the schema validation to ensure your metadata is correct:

```bash
npm run validate-server path/to/server.json
```

This will check that:
- Categories are from the approved list
- Tags follow the naming convention
- URLs are valid format
- Colors are valid hex codes
- Required fields are present