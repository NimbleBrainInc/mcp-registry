# MCP Registry

Server metadata registry for NimbleTools MCP servers.

## Server.json Updates

When updating a server version:
1. Update top-level `version`
2. Update each package's `identifier` URL
3. Update each package's `version`
4. Recalculate and update `fileSha256`

MCPB URL format: `nimblebraininc-<name>-<version>-<arch>.mcpb`
Example: `nimblebraininc-echo-0.1.3-linux-amd64.mcpb`

Get hash: `curl -sL <url> -o /tmp/file.mcpb && shasum -a 256 /tmp/file.mcpb`

## Adding New Servers

1. Create directory: `mkdir servers/<name>`
2. Create `servers/<name>/server.json` following existing patterns
3. **Important:** Ensure file permissions are `644` (not `600`):
   ```bash
   chmod 644 servers/<name>/server.json
   ```
   The Docker container runs as a non-root user and cannot read `600` files.
4. Run `npm run validate-servers` to verify
5. Deploy with `fly deploy`

## Resource Specs

All servers use standardized resources under `_meta.ai.nimbletools.mcp/v1`:
```json
"resources": {
  "requests": { "cpu": "250m", "memory": "256Mi" },
  "limits": { "cpu": "1000m", "memory": "512Mi" }
}
```

## Audit Workflow

```bash
# Check latest tag in source repo
cd ../../mcp-servers/<name> && git tag --sort=-v:refname | head -1

# Verify release assets
gh release view <tag> --repo NimbleBrainInc/<repo> --json assets -q '.assets[].name'
```

## Commands

```bash
npm run validate-servers   # Validate server.json files
npm run typecheck          # Type checking
```
