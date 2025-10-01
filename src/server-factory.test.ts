import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { FastifyInstance } from 'fastify';
import { createServer } from './server-factory.js';

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
      expect(json).toHaveProperty('version', 'v0');
      expect(json).toHaveProperty('endpoints');
      expect(json).toHaveProperty('documentation', '/docs');
    });
  });

  describe('GET /v0/servers', () => {
    it('should return a list of servers', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0/servers'
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
        url: '/v0/servers?limit=2'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json.servers.length).toBeLessThanOrEqual(2);
    });

    it('should support cursor-based pagination', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0/servers?cursor=0&limit=1'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json.metadata).toHaveProperty('count');
    });
  });

  describe('GET /v0/servers/:server_id', () => {
    it('should return a specific server by ID', async () => {
      // First get the list to find a valid server ID
      const listResponse = await server.inject({
        method: 'GET',
        url: '/v0/servers'
      });
      const serverList = listResponse.json();

      if (serverList.servers.length > 0) {
        const firstServer = serverList.servers[0];
        const serverId = encodeURIComponent(firstServer.name);

        const response = await server.inject({
          method: 'GET',
          url: `/v0/servers/${serverId}`
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
        url: '/v0/servers/non-existent-server-xyz'
      });

      expect(response.statusCode).toBe(404);
      const json = response.json();
      expect(json).toHaveProperty('error');
    });
  });

  describe('GET /v0/servers/:server_id/versions', () => {
    it('should return versions for a specific server', async () => {
      // First get a valid server
      const listResponse = await server.inject({
        method: 'GET',
        url: '/v0/servers'
      });
      const serverList = listResponse.json();

      if (serverList.servers.length > 0) {
        const firstServer = serverList.servers[0];
        const serverId = encodeURIComponent(firstServer.name);

        const response = await server.inject({
          method: 'GET',
          url: `/v0/servers/${serverId}/versions`
        });

        expect(response.statusCode).toBe(200);
        const json = response.json();
        expect(json).toHaveProperty('servers');
        expect(json).toHaveProperty('metadata');
        expect(Array.isArray(json.servers)).toBe(true);
      }
    });

    it('should return 404 for non-existent server versions', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/v0/servers/non-existent-server-xyz/versions'
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

  describe('GET /schemas/:filename/:version', () => {
    it('should return a specific schema version', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/nimbletools-server/2025-09-22'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json).toHaveProperty('$schema');
    });

    it('should return 404 for non-existent schema', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/non-existent-schema/2025-09-22'
      });

      expect(response.statusCode).toBe(404);
      const json = response.json();
      expect(json).toHaveProperty('error');
    });

    it('should reject paths with directory traversal', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/..%2Fsecrets/2025-09-22'
      });

      expect(response.statusCode).toBe(400);
      const json = response.json();
      expect(json).toHaveProperty('error', 'Invalid filename');
    });
  });

  describe('GET /schemas/:filename/latest', () => {
    it('should return the latest schema version', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/nimbletools-server/latest'
      });

      expect(response.statusCode).toBe(200);
      const json = response.json();
      expect(json).toHaveProperty('$schema');
    });

    it('should reject paths with directory traversal', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/schemas/..%2Fsecrets/latest'
      });

      expect(response.statusCode).toBe(400);
      const json = response.json();
      expect(json).toHaveProperty('error', 'Invalid filename');
    });
  });

  describe('GET /health', () => {
    it('should return health status', async () => {
      const response = await server.inject({
        method: 'GET',
        url: '/health'
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
        url: '/health'
      });

      const json = response.json();
      if (json.servers_loaded > 0) {
        expect(json.status).toBe('healthy');
      }
    });
  });
});
