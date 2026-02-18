# [DEPRECATED] NimbleBrain MCP Registry

> **This project has been deprecated and archived.**
>
> The MCP Registry has been superseded by **[mpak](https://github.com/NimbleBrainInc/mpak)** — the MCP package registry at [mpak.dev](https://mpak.dev).
>
> All server discovery, search, and package management is now handled by mpak. Please use mpak for all MCP server registry needs going forward.

---

_The original README is preserved below for historical reference._

---

A curated registry of Model Context Protocol (MCP) servers optimized for the NimbleBrain runtime platform.

## API Endpoints

```
GET /                                              # API info and available endpoints
GET /v0.1/servers                                  # List all servers (with search, pagination)
GET /v0.1/servers/{name}/versions/{version}        # Get specific server version
GET /v0.1/health                                   # Health check
GET /schemas                                       # List available schema versions
GET /docs                                          # Interactive API documentation (Swagger UI)
```

## License

Apache 2.0 - See [LICENSE](LICENSE) file for details.
