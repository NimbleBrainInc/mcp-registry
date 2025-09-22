/**
 * API endpoint tests for NimbleBrain MCP Registry
 */

import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { FastifyInstance } from 'fastify';
import { createServer } from '../src/server-factory';

describe('MCP Registry API', () => {
  let app: FastifyInstance;

  beforeAll(async () => {
    app = await createServer();
    await app.ready();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('GET /', () => {
    it('should return API information', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/'
      });

      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body);
      expect(body).toHaveProperty('name', 'NimbleBrain MCP Registry API');
      expect(body).toHaveProperty('version', 'v0');
      expect(body).toHaveProperty('endpoints');
      expect(body.endpoints).toHaveProperty('listServers', '/v0/servers');
      expect(body.endpoints).toHaveProperty('getServer', '/v0/servers/{server_id}');
    });
  });

  describe('GET /v0/servers', () => {
    it('should return a list of servers', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/v0/servers'
      });

      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body);
      expect(body).toHaveProperty('servers');
      expect(Array.isArray(body.servers)).toBe(true);
      expect(body).toHaveProperty('metadata');
      expect(body.metadata).toHaveProperty('count');
    });

    it('should support pagination with limit', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/v0/servers?limit=2'
      });

      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body);
      expect(body.servers.length).toBeLessThanOrEqual(2);
    });

    it('should support pagination with cursor', async () => {
      const firstResponse = await app.inject({
        method: 'GET',
        url: '/v0/servers?limit=1'
      });

      const firstBody = JSON.parse(firstResponse.body);

      if (firstBody.metadata?.next_cursor) {
        const secondResponse = await app.inject({
          method: 'GET',
          url: `/v0/servers?cursor=${firstBody.metadata.next_cursor}&limit=1`
        });

        expect(secondResponse.statusCode).toBe(200);
        const secondBody = JSON.parse(secondResponse.body);
        expect(secondBody.servers[0]?.name).not.toBe(firstBody.servers[0]?.name);
      }
    });
  });

  describe('GET /v0/servers/:server_id', () => {
    it('should return server details by name', async () => {
      // First get a server from the list
      const listResponse = await app.inject({
        method: 'GET',
        url: '/v0/servers?limit=1'
      });

      const listBody = JSON.parse(listResponse.body);

      if (listBody.servers.length > 0) {
        const serverName = listBody.servers[0].name;
        const encodedName = encodeURIComponent(serverName);

        const response = await app.inject({
          method: 'GET',
          url: `/v0/servers/${encodedName}`
        });

        expect(response.statusCode).toBe(200);
        const body = JSON.parse(response.body);
        expect(body).toHaveProperty('name', serverName);
        expect(body).toHaveProperty('version');
        expect(body).toHaveProperty('description');
      }
    });

    it('should return 404 for non-existent server', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/v0/servers/non.existent%2Fserver'
      });

      expect(response.statusCode).toBe(404);
      const body = JSON.parse(response.body);
      expect(body).toHaveProperty('error');
      expect(body.error).toContain('not found');
    });

    it('should handle URL-encoded server names', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/v0/servers/ai.nimblebrain%2Fecho'
      });

      // Either 200 (if exists) or 404 (if not), but should not error
      expect([200, 404]).toContain(response.statusCode);
    });

    it('should handle version query parameter', async () => {
      const listResponse = await app.inject({
        method: 'GET',
        url: '/v0/servers?limit=1'
      });

      const listBody = JSON.parse(listResponse.body);

      if (listBody.servers.length > 0) {
        const server = listBody.servers[0];
        const encodedName = encodeURIComponent(server.name);

        const response = await app.inject({
          method: 'GET',
          url: `/v0/servers/${encodedName}?version=${server.version}`
        });

        expect(response.statusCode).toBe(200);
      }
    });

    it('should return 404 for wrong version', async () => {
      const listResponse = await app.inject({
        method: 'GET',
        url: '/v0/servers?limit=1'
      });

      const listBody = JSON.parse(listResponse.body);

      if (listBody.servers.length > 0) {
        const serverName = listBody.servers[0].name;
        const encodedName = encodeURIComponent(serverName);

        const response = await app.inject({
          method: 'GET',
          url: `/v0/servers/${encodedName}?version=99.99.99`
        });

        expect(response.statusCode).toBe(404);
        const body = JSON.parse(response.body);
        expect(body.error).toContain('Version 99.99.99 not found');
      }
    });
  });

  describe('GET /v0/servers/:server_id/versions', () => {
    it('should return server versions', async () => {
      const listResponse = await app.inject({
        method: 'GET',
        url: '/v0/servers?limit=1'
      });

      const listBody = JSON.parse(listResponse.body);

      if (listBody.servers.length > 0) {
        const serverName = listBody.servers[0].name;
        const encodedName = encodeURIComponent(serverName);

        const response = await app.inject({
          method: 'GET',
          url: `/v0/servers/${encodedName}/versions`
        });

        expect(response.statusCode).toBe(200);
        const body = JSON.parse(response.body);
        expect(body).toHaveProperty('servers');
        expect(Array.isArray(body.servers)).toBe(true);
        expect(body.servers.length).toBeGreaterThan(0);
      }
    });

    it('should return 404 for non-existent server versions', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/v0/servers/non.existent%2Fserver/versions'
      });

      expect(response.statusCode).toBe(404);
      const body = JSON.parse(response.body);
      expect(body).toHaveProperty('error');
    });
  });

  describe('GET /health', () => {
    it('should return health status', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/health'
      });

      expect(response.statusCode).toBe(200);
      const body = JSON.parse(response.body);
      expect(body).toHaveProperty('status');
      expect(['healthy', 'unhealthy']).toContain(body.status);
      expect(body).toHaveProperty('servers_loaded');
      expect(typeof body.servers_loaded).toBe('number');
    });
  });

  describe('Server metadata', () => {
    it('should include enhanced metadata fields if present', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/v0/servers/ai.nimblebrain%2Ffinnhub'
      });

      if (response.statusCode === 200) {
        const body = JSON.parse(response.body);

        if (body._meta?.['ai.nimblebrain.mcp/v1']?.registry) {
          const registry = body._meta['ai.nimblebrain.mcp/v1'].registry;

          // Check for enhanced metadata fields
          if (registry.categories) {
            expect(Array.isArray(registry.categories)).toBe(true);
          }

          if (registry.tags) {
            expect(Array.isArray(registry.tags)).toBe(true);
          }

          if (registry.branding) {
            expect(typeof registry.branding).toBe('object');
          }

          if (registry.documentation) {
            expect(typeof registry.documentation).toBe('object');
          }
        }
      }
    });
  });
});