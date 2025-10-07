/**
 * Factory for creating the Fastify server instance
 * Separated for testing purposes
 */

import cors from '@fastify/cors';
import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui';
import Fastify, { FastifyInstance } from 'fastify';
import { readdir, readFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { v4 as uuidv4 } from 'uuid';
import type {
  ErrorResponse,
  MCPServerDetail,
  RegistryMetadata,
  ServerListResponse
} from './types/api.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Constants
const SERVERS_DIR = join(__dirname, '..', 'servers');
const SCHEMAS_DIR = join(__dirname, '..', 'schemas');
const LATEST_SCHEMA_VERSION = '2025-09-22';

// Server cache
let serversCache: Map<string, MCPServerDetail> = new Map();
let lastCacheUpdate = 0;
const CACHE_TTL = 60000; // 1 minute cache

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

        // Use server name as the ID
        const serverId = serverData.name;

        // Add registry metadata if not present
        if (!serverData._meta) {
          serverData._meta = {
            'ai.nimbletools.mcp/v1': {}
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

  // Update cache
  serversCache = servers;
  lastCacheUpdate = Date.now();

  return servers;
}

/**
 * Create and configure Fastify server instance
 */
export async function createServer(): Promise<FastifyInstance> {
  const fastify = Fastify({
    logger: process.env.NODE_ENV !== 'test'  // Enable logging except in test environment
  });

  // Register CORS
  await fastify.register(cors, {
    origin: true,
    credentials: true
  });

  // Register Swagger for API documentation
  await fastify.register(swagger, {
    openapi: {
      info: {
        title: 'NimbleTools MCP Registry API',
        description: 'A curated registry of Model Context Protocol servers',
        version: 'v0'
      },
      servers: [
        {
          url: process.env.API_URL || 'https://registry.nimbletools.ai'
        }
      ]
    }
  });

  if (process.env.NODE_ENV !== 'test') {
    await fastify.register(swaggerUi, {
      routePrefix: '/docs',
      uiConfig: {
        docExpansion: 'list',
        deepLinking: false,
        tryItOutEnabled: true,
        persistAuthorization: true
      },
      staticCSP: false,
      transformStaticCSP: (header) => header
    });
  }

  // Root endpoint
  fastify.get('/', async () => {
    return {
      name: 'NimbleTools MCP Registry API',
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

    // Decode the server ID (which is the server name)
    const decodedName = decodeURIComponent(request.params.server_id);
    const server = servers.get(decodedName);

    if (!server) {
      reply.code(404);
      return { error: `Server '${request.params.server_id}' not found` };
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

    // Decode the server ID (which is the server name)
    const decodedName = decodeURIComponent(request.params.server_id);
    const server = servers.get(decodedName);

    if (!server) {
      reply.code(404);
      return { error: `Server '${request.params.server_id}' not found` };
    }

    // For now, return just the current version
    // In the future, this could query a version history
    return {
      servers: [server],
      metadata: {
        count: 1
      }
    };
  });

  // List schemas endpoint
  fastify.get('/schemas', async () => {
    try {
      const versions = await readdir(SCHEMAS_DIR, { withFileTypes: true });
      const schemaVersions = versions
        .filter(d => d.isDirectory())
        .map(d => d.name)
        .sort()
        .reverse();

      // Get all unique schema filenames across all versions
      const schemaFilesMap = new Map<string, Set<string>>();

      for (const version of schemaVersions) {
        const versionDir = join(SCHEMAS_DIR, version);
        const files = await readdir(versionDir);
        const schemaFiles = files.filter(f => f.endsWith('.schema.json'));

        for (const file of schemaFiles) {
          if (!schemaFilesMap.has(file)) {
            schemaFilesMap.set(file, new Set());
          }
          schemaFilesMap.get(file)!.add(version);
        }
      }

      // Build response array
      const schemas = Array.from(schemaFilesMap.entries()).map(([filename, versions]) => {
        const versionList = Array.from(versions).sort().reverse();
        return {
          name: filename,
          versions: versionList,
          latest: versionList[0],
          urls: {
            latest: `/schemas/latest/${filename}`,
            versioned: versionList.map(v => `/schemas/${v}/${filename}`)
          }
        };
      });

      return schemas;
    } catch (error) {
      return [];
    }
  });

  // Get schema by version
  fastify.get<{
    Params: { version: string; filename: string };
  }>('/schemas/:version/:filename', async (request, reply) => {
    const { version, filename } = request.params;

    // Validate version and filename to prevent directory traversal
    if (version.includes('..') || version.includes('/') || filename.includes('..') || filename.includes('/')) {
      reply.code(400);
      return { error: 'Invalid version or filename' };
    }

    try {
      const schemaPath = join(SCHEMAS_DIR, version, filename);
      const content = await readFile(schemaPath, 'utf-8');
      reply.type('application/json');
      return JSON.parse(content);
    } catch (error) {
      reply.code(404);
      return { error: 'Schema not found' };
    }
  });

  // Get latest schema
  fastify.get<{
    Params: { filename: string };
  }>('/schemas/latest/:filename', async (request, reply) => {
    const { filename } = request.params;

    // Validate filename
    if (filename.includes('..') || filename.includes('/')) {
      reply.code(400);
      return { error: 'Invalid filename' };
    }

    try {
      const schemaPath = join(SCHEMAS_DIR, LATEST_SCHEMA_VERSION, filename);
      const content = await readFile(schemaPath, 'utf-8');
      reply.type('application/json');
      return JSON.parse(content);
    } catch (error) {
      reply.code(404);
      return { error: 'Schema not found' };
    }
  });

  // Health check endpoint
  fastify.get('/health', async () => {
    const servers = await loadServers();

    return {
      status: servers.size > 0 ? 'healthy' : 'unhealthy',
      servers_loaded: servers.size,
      cache_age_ms: Date.now() - lastCacheUpdate
    };
  });

  return fastify;
}