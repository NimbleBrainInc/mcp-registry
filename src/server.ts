/**
 * NimbleBrain MCP Registry API Server
 *
 * A lightweight, spec-compliant API server for the NimbleBrain MCP Registry.
 * Serves server definitions from JSON files with proper REST endpoints.
 */

import 'dotenv/config';
import cors from '@fastify/cors';
import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui';
import Fastify from 'fastify';
import { readdir, readFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { v4 as uuidv4, v5 as uuidv5 } from 'uuid';
import type {
  ErrorResponse,
  MCPServerDetail,
  RegistryMetadata,
  ServerListResponse
} from './types/generated.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Constants
const SERVERS_DIR = join(__dirname, '..', 'servers');
const SCHEMAS_DIR = join(__dirname, '..', 'schemas');
const LATEST_SCHEMA_VERSION = '2025-09-22'; // Update this when releasing new schema versions
const DNS_NAMESPACE = '6ba7b810-9dad-11d1-80b4-00c04fd430c8';
const PORT = parseInt(process.env.PORT || '8080', 10);
const HOST = process.env.HOST || '0.0.0.0';

// Server cache
let serversCache: Map<string, MCPServerDetail> = new Map();
let lastCacheUpdate = 0;
const CACHE_TTL = 60000; // 1 minute cache

/**
 * Generate consistent UUID from server name
 */
function generateServerId(name: string): string {
  return uuidv5(name, DNS_NAMESPACE);
}

/**
 * Load all server definitions from JSON files
 */
async function loadServers(): Promise<Map<string, MCPServerDetail>> {
  const now = Date.now();

  // Return cached data if still valid
  if (serversCache.size > 0 && (now - lastCacheUpdate) < CACHE_TTL) {
    return serversCache;
  }

  const servers = new Map<string, MCPServerDetail>();

  try {
    const dirs = await readdir(SERVERS_DIR, { withFileTypes: true });

    for (const dir of dirs) {
      if (!dir.isDirectory()) continue;

      const serverJsonPath = join(SERVERS_DIR, dir.name, 'server.json');

      try {
        const content = await readFile(serverJsonPath, 'utf-8');
        const serverData = JSON.parse(content) as MCPServerDetail;

        // Generate consistent server ID
        const serverId = generateServerId(serverData.name);

        // Add registry metadata if not present
        if (!serverData._meta) {
          serverData._meta = {
            'ai.nimblebrain.mcp/v1': {}
          };
        }

        const registryMeta: RegistryMetadata = {
          serverId,
          versionId: uuidv4(),
          publishedAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          isLatest: true
        };

        serverData._meta['io.modelcontextprotocol.registry/official'] = registryMeta;

        servers.set(serverId, serverData);
      } catch (error) {
        console.error(`Error loading ${serverJsonPath}:`, error);
      }
    }
  } catch (error) {
    console.error('Error reading servers directory:', error);
  }

  serversCache = servers;
  lastCacheUpdate = now;

  return servers;
}

/**
 * Create and configure Fastify server
 */
async function createServer() {
  const fastify = Fastify({
    logger: {
      level: process.env.LOG_LEVEL || 'info'
    }
  });

  // Register CORS - completely open for public API
  await fastify.register(cors, {
    origin: true,  // Allow all origins
    credentials: true
  });

  // Register Swagger for API documentation
  await fastify.register(swagger, {
    openapi: {
      info: {
        title: 'NimbleBrain MCP Registry API',
        description: 'A curated registry of Model Context Protocol servers',
        version: 'v0'
      },
      servers: [
        {
          url: process.env.API_URL || 'https://registry.nimblebrain.ai'
        }
      ]
    }
  });

  await fastify.register(swaggerUi, {
    routePrefix: '/docs',
    uiConfig: {
      docExpansion: 'list',
      deepLinking: false,
      tryItOutEnabled: true,
      persistAuthorization: true
    },
    staticCSP: false,  // Disable CSP for Swagger UI
    transformStaticCSP: (header) => header  // Keep original CSP
  });

  // Root endpoint
  fastify.get('/', async () => {
    return {
      name: 'NimbleBrain MCP Registry API',
      version: 'v0',
      endpoints: {
        listServers: '/v0/servers',
        getServer: '/v0/servers/{server_id}',
        getServerVersions: '/v0/servers/{server_id}/versions',
        schemas: '/schemas',
        schemaByVersion: '/schemas/{version}/{filename}',
        latestSchema: '/schemas/latest/{filename}'
      },
      documentation: '/docs'
    };
  });

  // List servers endpoint
  fastify.get<{
    Querystring: { cursor?: string; limit?: string };
    Reply: ServerListResponse | ErrorResponse;
  }>('/v0/servers', {
    schema: {
      querystring: {
        type: 'object',
        properties: {
          cursor: { type: 'string' },
          limit: { type: 'string' }
        }
      }
    }
  }, async (request) => {
    const servers = await loadServers();
    const serverList = Array.from(servers.values());

    // Parse pagination parameters
    const limit = Math.min(parseInt(request.query.limit || '100', 10), 500);
    const startIdx = request.query.cursor ? parseInt(request.query.cursor, 10) : 0;
    const endIdx = startIdx + limit;

    // Paginate results
    const paginated = serverList.slice(startIdx, endIdx);

    const response: ServerListResponse = {
      servers: paginated,
      metadata: {
        count: paginated.length
      }
    };

    // Add next cursor if there are more results
    if (endIdx < serverList.length && response.metadata) {
      response.metadata.next_cursor = String(endIdx);
    }

    return response;
  });

  // Get server by ID endpoint
  fastify.get<{
    Params: { server_id: string };
    Querystring: { version?: string };
    Reply: MCPServerDetail | ErrorResponse;
  }>('/v0/servers/:server_id', {
    schema: {
      params: {
        type: 'object',
        properties: {
          server_id: { type: 'string' }
        },
        required: ['server_id']
      },
      querystring: {
        type: 'object',
        properties: {
          version: { type: 'string' }
        }
      }
    }
  }, async (request, reply) => {
    const servers = await loadServers();
    const server = servers.get(request.params.server_id);

    if (!server) {
      reply.code(404);
      return { error: 'Server not found' };
    }

    // Check version if specified
    if (request.query.version && server.version !== request.query.version) {
      reply.code(404);
      return { error: `Version ${request.query.version} not found for this server` };
    }

    return server;
  });

  // Get server versions endpoint
  fastify.get<{
    Params: { server_id: string };
    Reply: ServerListResponse | ErrorResponse;
  }>('/v0/servers/:server_id/versions', {
    schema: {
      params: {
        type: 'object',
        properties: {
          server_id: { type: 'string' }
        },
        required: ['server_id']
      }
    }
  }, async (request, reply) => {
    const servers = await loadServers();
    const server = servers.get(request.params.server_id);

    if (!server) {
      reply.code(404);
      return { error: 'Server not found' };
    }

    // For now, return just the current version
    // In the future, this could return historical versions from git history
    return {
      servers: [server],
      metadata: {
        count: 1
      }
    };
  });

  // Schema endpoints
  fastify.get('/schemas/:version/:filename', async (request, reply) => {
    const { version, filename } = request.params as { version: string; filename: string };
    const schemaPath = join(SCHEMAS_DIR, version, filename);

    try {
      const schema = await readFile(schemaPath, 'utf-8');
      reply.type('application/json');
      return JSON.parse(schema);
    } catch (error) {
      reply.code(404);
      return { error: 'Schema not found' };
    }
  });

  // Latest schema endpoint - redirects to the current latest version
  fastify.get('/schemas/latest/:filename', async (request, reply) => {
    const { filename } = request.params as { filename: string };
    const schemaPath = join(SCHEMAS_DIR, LATEST_SCHEMA_VERSION, filename);

    try {
      const schema = await readFile(schemaPath, 'utf-8');
      reply.type('application/json');
      return JSON.parse(schema);
    } catch (error) {
      reply.code(404);
      return { error: 'Schema not found' };
    }
  });

  // List available schemas
  fastify.get('/schemas', async () => {
    try {
      const entries = await readdir(SCHEMAS_DIR, { withFileTypes: true });
      const versions = entries
        .filter(entry => entry.isDirectory() && /^\d{4}-\d{2}-\d{2}$/.test(entry.name))
        .map(entry => entry.name)
        .sort()
        .reverse();

      const schemas: any = {};
      for (const version of versions) {
        const versionPath = join(SCHEMAS_DIR, version);
        try {
          const files = await readdir(versionPath);
          schemas[version] = files.filter(f => f.endsWith('.json'));
        } catch {
          // Skip if directory doesn't exist or can't be read
        }
      }

      return {
        versions: schemas,
        latest: LATEST_SCHEMA_VERSION,
        availableVersions: versions
      };
    } catch (error) {
      return { error: 'Failed to list schemas' };
    }
  });

  // Health check endpoint
  fastify.get('/health', async () => {
    const servers = await loadServers();
    return {
      status: 'healthy',
      servers_loaded: servers.size,
      cache_age_ms: Date.now() - lastCacheUpdate
    };
  });

  return fastify;
}

/**
 * Start the server
 */
async function start() {
  try {
    const server = await createServer();

    await server.listen({
      port: PORT,
      host: HOST
    });

    console.log(`🚀 NimbleBrain MCP Registry API`);
    console.log(`   Listening on: http://${HOST}:${PORT}`);
    console.log(`   Documentation: http://${HOST}:${PORT}/docs`);
    console.log(`   Servers loaded: ${serversCache.size}`);
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Start the server
start();