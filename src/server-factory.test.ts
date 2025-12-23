import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { FastifyInstance } from 'fastify';
import { createServer } from './server-factory.js';
import { statSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

describe('Server Factory - API Endpoints', () => {
  let server: FastifyInstance;

  beforeAll(async () => {
    server = await createServer();
    await server.ready();
  });

  afterAll(async () => {
    await server.close();
  });

  describe('GET /', () => {
    it('should return API information', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json).toHaveProperty('name', 'NimbleTools MCP Registry API');
      expect(json).toHaveProperty('version', 'v0.1');
      expect(json).toHaveProperty('endpoints');
      expect(json).toHaveProperty('documentation', '/docs');
    });
  });

  describe('GET /v0.1/servers', () => {
    it('should return a list of servers', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/servers'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json).toHaveProperty('servers');
      expect(json).toHaveProperty('metadata');
      expect(Array.isArray(json.servers)).toBe(true);
      expect(json.metadata).toHaveProperty('count');
    });

    it('should support pagination with limit parameter', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/servers?limit=2'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json.servers.length).toBeLessThanOrEqual(2);
    });

    it('should support cursor-based pagination', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/servers?cursor=0&limit=1'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json.metadata).toHaveProperty('count');
    });

    it('should support search parameter', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/servers?search=echo'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(Array.isArray(json.servers)).toBe(true);
      // If there's an echo server, it should be in the results
      if (json.servers.length > 0) {
        const hasMatch = json.servers.some((s: any) =>
          s.name.toLowerCase().includes('echo') ||
          s.title?.toLowerCase().includes('echo') ||
          s.description.toLowerCase().includes('echo')
        );
        expect(hasMatch).toBe(true);
      }
    });

    it('should support version=latest parameter', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/servers?version=latest'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(Array.isArray(json.servers)).toBe(true);
    });

    it('should support updated_since parameter', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/servers?updated_since=2020-01-01T00:00:00Z'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(Array.isArray(json.servers)).toBe(true);
    });
  });

  describe('GET /v0.1/servers/:name/versions/:version', () => {
    it('should return a specific server by name and version', async () => {
      // First get the list to find a valid server
      const listResponse = await server.inject({
        method: 'GET',
        url: '/v0.1/servers'
      });
      const serverList = listResponse.json();

      if (serverList.servers.length > 0) {
        const firstServer = serverList.servers[0];
        const serverName = encodeURIComponent(firstServer.name);
        const serverVersion = firstServer.version;

        const response = await server.inject({
          method: 'GET',
          url: `/v0.1/servers/${serverName}/versions/${serverVersion}`
        });

        expect(response.statusCode).toBe(200);
        const json = response.json();
        expect(json).toHaveProperty('name', firstServer.name);
        expect(json).toHaveProperty('version', serverVersion);
        expect(json).toHaveProperty('description');
      }
    });

    it('should support "latest" as version', async () => {
      // First get the list to find a valid server
      const listResponse = await server.inject({
        method: 'GET',
        url: '/v0.1/servers'
      });
      const serverList = listResponse.json();

      if (serverList.servers.length > 0) {
        const firstServer = serverList.servers[0];
        const serverName = encodeURIComponent(firstServer.name);

        const response = await server.inject({
          method: 'GET',
          url: `/v0.1/servers/${serverName}/versions/latest`
        });

        expect(response.statusCode).toBe(200);
        const json = response.json();
        expect(json).toHaveProperty('name', firstServer.name);
      }
    });

    it('should return 404 for non-existent server', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/servers/non-existent-server-xyz/versions/latest'
      });

      expect(response.statusCode).toBe(404);
      const json = response.json();
      expect(json).toHaveProperty('error');
    });

    it('should return 404 for non-existent version', async () => {
      // First get a valid server
      const listResponse = await server.inject({
        method: 'GET',
        url: '/v0.1/servers'
      });
      const serverList = listResponse.json();

      if (serverList.servers.length > 0) {
        const firstServer = serverList.servers[0];
        const serverName = encodeURIComponent(firstServer.name);

        const response = await server.inject({
          method: 'GET',
          url: `/v0.1/servers/${serverName}/versions/99.99.99`
        });

        expect(response.statusCode).toBe(404);
        const json = response.json();
        expect(json).toHaveProperty('error');
      }
    });
  });

  describe('GET /v0.1/servers/:server_id (legacy)', () => {
    it('should return a specific server by ID for backwards compatibility', async () => {
      // First get the list to find a valid server ID
      const listResponse = await server.inject({
        method: 'GET',
        url: '/v0.1/servers'
      });
      const serverList = listResponse.json();

      if (serverList.servers.length > 0) {
        const firstServer = serverList.servers[0];
        const serverId = encodeURIComponent(firstServer.name);

        const response = await server.inject({
          method: 'GET',
          url: `/v0.1/servers/${serverId}`
        });

        expect(response.statusCode).toBe(200);
        const json = response.json();
        expect(json).toHaveProperty('name', firstServer.name);
        expect(json).toHaveProperty('version');
        expect(json).toHaveProperty('description');
      }
    });

    it('should return 404 for non-existent server', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/servers/non-existent-server-xyz'
      });

      expect(response.statusCode).toBe(404);
      const json = response.json();
      expect(json).toHaveProperty('error');
    });
  });

  describe('GET /schemas', () => {
    it('should return list of available schemas', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(Array.isArray(json)).toBe(true);
    });
  });

  describe('GET /schemas/:version/:filename', () => {
    it('should return a specific schema version', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/2025-12-11/nimbletools-server.schema.json'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json).toHaveProperty('$schema');
    });

    it('should return the bundled schema with no external refs', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/2025-12-11/nimbletools-server.bundled.schema.json'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json).toHaveProperty('$schema');
      expect(json).toHaveProperty('$comment');
      expect(json.$comment).toContain('AUTO-GENERATED');
      // Bundled schema should have definitions inlined
      expect(json).toHaveProperty('allOf');
    });

    it('should return 404 for non-existent schema', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/2025-12-11/non-existent-schema.json'
      });

      expect(response.statusCode).toBe(404);
      const json = response.json();
      expect(json).toHaveProperty('error');
    });

    it('should reject paths with directory traversal', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/2025-12-11/..%2Fsecrets'
      });

      expect(response.statusCode).toBe(400);
      const json = response.json();
      expect(json).toHaveProperty('error', 'Invalid version or filename');
    });
  });

  describe('GET /schemas/latest/:filename', () => {
    it('should return the latest schema version', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/latest/nimbletools-server.schema.json'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json).toHaveProperty('$schema');
    });

    it('should reject paths with directory traversal', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/latest/..%2Fsecrets'
      });

      expect(response.statusCode).toBe(400);
      const json = response.json();
      expect(json).toHaveProperty('error', 'Invalid filename');
    });
  });

  describe('GET /v0.1/health', () => {
    it('should return health status', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/health'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json).toHaveProperty('status');
      expect(json).toHaveProperty('servers_loaded');
      expect(json).toHaveProperty('cache_age_ms');
    });

    it('should report healthy status when servers are loaded', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0.1/health'
      });

      const json = response.json();
      if (json.servers_loaded > 0) {
        expect(json.status).toBe('healthy');
      }
    });
  });
});

describe('Schema Bundling Verification', () => {
  const SCHEMAS_DIR = join(__dirname, '..', 'schemas', '2025-12-11');
  const SOURCE_SCHEMA = join(SCHEMAS_DIR, 'nimbletools-server.schema.json');
  const BUNDLED_SCHEMA = join(SCHEMAS_DIR, 'nimbletools-server.bundled.schema.json');

  it('should have a bundled schema file', () => {
    expect(existsSync(BUNDLED_SCHEMA)).toBe(true);
  });

  it('should have bundled schema that is not older than source schema', () => {
    // This test fails if you modify the source schema but forget to run npm run bundle-schema
    const sourceStat = statSync(SOURCE_SCHEMA);
    const bundledStat = statSync(BUNDLED_SCHEMA);

    const sourceModified = sourceStat.mtimeMs;
    const bundledModified = bundledStat.mtimeMs;

    expect(bundledModified).toBeGreaterThanOrEqual(sourceModified - 1000); // 1 second tolerance
  });
});
