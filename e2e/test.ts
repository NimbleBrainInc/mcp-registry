#!/usr/bin/env tsx

/**
 * End-to-end test for NimbleTools MCP Registry servers.
 * Tests workspace creation, server deployment, and MCP connectivity.
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { interpolateEnv, loadEnvFile, loadFixture, ServerTestFixture, validateResponse } from './fixtures.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Allow self-signed certificates for local testing
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

interface ServerDefinition {
  name: string;
  version: string;
  description: string;
  status: string;
  packages: any[];
  _meta: any;
}

class NimbleToolsE2ETest {
  private baseUrl: string;
  private workspaceId: string | null = null;
  private serverId: string | null = null;
  private mcpSessionId: string | null = null;

  constructor(baseUrl = 'http://api.nt.dev') {
    this.baseUrl = baseUrl;
  }

  private async request(method: string, url: string, body?: any, isMcp = false, isNotification = false): Promise<any> {
    try {
      const headers: Record<string, string> = body ? { 'Content-Type': 'application/json' } : {};

      // MCP requires accepting both application/json and text/event-stream
      if (isMcp) {
        headers['Accept'] = 'application/json, text/event-stream';

        // Include session ID after initialization
        if (this.mcpSessionId) {
          headers['mcp-session-id'] = this.mcpSessionId;
        }
      }

      const response = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`${method} ${url} failed: ${response.status} ${response.statusText}\n${text}`);
      }

      // Extract session ID from response headers on first MCP call
      if (isMcp && !this.mcpSessionId) {
        const sessionId = response.headers.get('mcp-session-id');
        if (sessionId) {
          this.mcpSessionId = sessionId;
          console.log(`  Session ID: ${sessionId}`);
        }
      }

      // Notifications might not have a response body
      if (isNotification) {
        return null;
      }

      const text = await response.text();

      // Handle empty responses
      if (!text || text.trim() === '') {
        return null;
      }

      // Parse SSE format if present
      if (text.startsWith('event:')) {
        // SSE format: "event: message\ndata: {...}\n\n"
        const dataMatch = text.match(/data: (.+)/);
        if (dataMatch) {
          return JSON.parse(dataMatch[1]);
        }
      }

      return JSON.parse(text);
    } catch (error) {
      if (error instanceof Error && error.message.includes('fetch failed')) {
        throw new Error(`${method} ${url} failed: ${error.message}\nCause: ${(error as any).cause}`);
      }
      throw error;
    }
  }

  async createWorkspace(): Promise<string> {
    const data = await this.request('POST', `${this.baseUrl}/v1/workspaces`, {
      name: `test-${Date.now()}`,
      description: 'E2E test workspace',
    });
    return data.workspace_id;
  }

  async setSecret(key: string, value: string): Promise<void> {
    await this.request(
      'PUT',
      `${this.baseUrl}/v1/workspaces/${this.workspaceId}/secrets/${key}`,
      { secret_value: value }
    );
  }

  async deployServer(serverDef: ServerDefinition, environment: Record<string, string> = {}): Promise<string> {
    const data = await this.request(
      'POST',
      `${this.baseUrl}/v1/workspaces/${this.workspaceId}/servers`,
      { server: serverDef, replicas: 1, environment }
    );
    return data.server_id;
  }

  async waitForServerReady(timeout = 120000): Promise<void> {
    const startTime = Date.now();
    let lastStatus = '';

    while (Date.now() - startTime < timeout) {
      const data = await this.request(
        'GET',
        `${this.baseUrl}/v1/workspaces/${this.workspaceId}/servers/${this.serverId}`
      );

      const currentStatus = `${data.status.phase} (ready: ${data.status.deployment_ready}, replicas: ${data.status.ready_replicas}/${data.status.replicas})`;

      if (currentStatus !== lastStatus) {
        console.log(`  Status: ${currentStatus}`);
        lastStatus = currentStatus;
      }

      // Check if server is ready (phase can be Unknown initially)
      if (data.status.deployment_ready && data.status.ready_replicas > 0) {
        return;
      }

      // Fail fast on error states
      if (data.status.phase === 'Failed') {
        throw new Error(`Server deployment failed: ${JSON.stringify(data.status)}`);
      }

      await new Promise((resolve) => setTimeout(resolve, 5000));
    }

    throw new Error(`Server ${this.serverId} not ready after ${timeout}ms`);
  }

  async testMcpConnection(): Promise<void> {
    // Get the actual service endpoint from the server details
    const serverDetails = await this.request(
      'GET',
      `${this.baseUrl}/v1/workspaces/${this.workspaceId}/servers/${this.serverId}`
    );

    // MCP endpoints use mcp.nt.dev instead of api.nt.dev
    const mcpBaseUrl = this.baseUrl.replace('api.nt.dev', 'mcp.nt.dev');
    const mcpUrl = `${mcpBaseUrl}${serverDetails.status.service_endpoint}`;
    console.log(`  MCP URL: ${mcpUrl}`);

    // Wait for MCP endpoint to be available (with retries)
    let resp: any;
    let retries = 6; // 30 seconds total
    let lastError: Error | null = null;

    while (retries > 0) {
      try {
        resp = await this.request('POST', mcpUrl, {
          jsonrpc: '2.0',
          id: 1,
          method: 'initialize',
          params: {
            protocolVersion: '2024-11-05',
            capabilities: {},
            clientInfo: { name: 'registry-test-client', version: '1.0.0' },
          },
        }, true); // isMcp = true

        if (resp.result) break; // Success
      } catch (error) {
        lastError = error as Error;
        if (error instanceof Error && !error.message.includes('503')) {
          throw error; // Don't retry non-503 errors
        }
        console.log(`  Waiting for MCP endpoint... (${retries} retries left)`);
        await new Promise((resolve) => setTimeout(resolve, 5000));
        retries--;
      }
    }

    if (!resp?.result) {
      throw new Error(`Initialize failed after retries: ${lastError?.message}`);
    }

    // Send notifications/initialized (required by MCP protocol)
    await this.request('POST', mcpUrl, {
      jsonrpc: '2.0',
      method: 'notifications/initialized',
    }, true, true); // isMcp = true, isNotification = true

    // List tools (no params field!)
    resp = await this.request('POST', mcpUrl, {
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/list',
    }, true); // isMcp = true

    if (!resp.result?.tools?.length) throw new Error('No tools found');

    // Call first tool
    const toolName = resp.result.tools[0].name;
    resp = await this.request('POST', mcpUrl, {
      jsonrpc: '2.0',
      id: 3,
      method: 'tools/call',
      params: { name: toolName, arguments: { message: 'Test' } },
    }, true); // isMcp = true

    if (!resp.result) throw new Error('Tool call failed');
  }

  async runFixtureTests(fixture: ServerTestFixture): Promise<void> {
    if (!fixture.tests) return;

    const mcpBaseUrl = this.baseUrl.replace('api.nt.dev', 'mcp.nt.dev');
    const serverDetails = await this.request(
      'GET',
      `${this.baseUrl}/v1/workspaces/${this.workspaceId}/servers/${this.serverId}`
    );
    const mcpUrl = `${mcpBaseUrl}${serverDetails.status.service_endpoint}`;

    for (const test of fixture.tests) {
      try {
        const resp = await this.request('POST', mcpUrl, {
          jsonrpc: '2.0',
          id: 99,
          method: 'tools/call',
          params: { name: test.tool, arguments: test.arguments },
        }, true);

        // Debug: log the actual response
        console.log(`  Response:`, JSON.stringify(resp, null, 2));

        if (test.expect && !validateResponse(resp, test.expect)) {
          throw new Error(`Test failed validation: ${test.name}`);
        }

        console.log(`  ✓ Test passed: ${test.name}`);
      } catch (error) {
        throw new Error(`Test failed: ${test.name} - ${error}`);
      }
    }
  }

  async cleanup(): Promise<void> {
    // if (this.workspaceId) {
    //   try {
    //     await this.request('DELETE', `${this.baseUrl}/v1/workspaces/${this.workspaceId}`);
    //   } catch (e) {
    //     console.warn(`Warning: Cleanup failed: ${e}`);
    //   }
    // }
  }

  async testServer(serverPath: string, envVars: Record<string, string>): Promise<boolean> {
    const serverName = path.basename(path.dirname(serverPath));

    try {
      // Reset state for each test
      this.workspaceId = null;
      this.serverId = null;
      this.mcpSessionId = null;

      // Load server definition
      const serverDef = JSON.parse(await fs.readFile(serverPath, 'utf-8')) as ServerDefinition;

      // Skip non-active servers
      if (serverDef.status !== 'active') {
        console.log(`⊘ ${serverName}: Skipped (status: ${serverDef.status})`);
        return true;
      }

      // Load test fixture
      const fixture = await loadFixture(serverPath);

      // Check if server should be skipped
      if (fixture?.skip) {
        console.log(`⊘ ${serverName}: Skipped (${fixture.skipReason || 'no reason given'})`);
        return true;
      }

      console.log(`Testing ${serverName}...`);

      // Create workspace
      this.workspaceId = await this.createWorkspace();
      console.log(`  ✓ Workspace created: ${this.workspaceId}`);

      // Interpolate environment variables if fixture exists
      let environment = {};
      if (fixture?.environment) {
        const interpolated = interpolateEnv(fixture, envVars);
        environment = interpolated.environment || {};

        // Set secrets in workspace before deployment
        for (const [key, value] of Object.entries(environment)) {
          await this.setSecret(key, value);
          console.log(`  ✓ Secret set: ${key}`);
        }
      }

      // Deploy server (secrets are auto-injected)
      this.serverId = await this.deployServer(serverDef);
      console.log(`  ✓ Server deployed: ${this.serverId}`);

      // Wait for ready
      await this.waitForServerReady();
      console.log(`  ✓ Server ready`);

      // Test MCP connection
      await this.testMcpConnection();
      console.log(`  ✓ MCP connection verified`);

      // Run fixture tests if they exist
      if (fixture?.tests && fixture.tests.length > 0) {
        await this.runFixtureTests(fixture);
      }

      // Cleanup
      await this.cleanup();
      console.log(`✓ ${serverName}: PASSED`);
      return true;
    } catch (e) {
      console.log(`✗ ${serverName}: FAILED - ${e}`);
      await this.cleanup();
      return false;
    }
  }
}

async function main() {
  // Parse arguments
  const args = process.argv.slice(2);
  let baseUrl = 'http://api.nt.dev';
  let serverFilter: string | null = null;

  for (const arg of args) {
    if (arg.startsWith('--server=')) {
      serverFilter = arg.split('=')[1];
    } else if (!arg.startsWith('--')) {
      baseUrl = arg;
    }
  }

  const registryPath = path.join(__dirname, '..', 'servers');

  console.log(`NimbleTools MCP Registry E2E Test`);
  console.log(`API: ${baseUrl}`);
  console.log(`Registry: ${registryPath}`);
  if (serverFilter) console.log(`Filter: ${serverFilter}`);
  console.log();

  // Load environment variables for tests
  const envVars = { ...process.env, ...await loadEnvFile() } as Record<string, string>;

  // Test each server
  const tester = new NimbleToolsE2ETest(baseUrl);
  const results: Array<[string, boolean]> = [];

  // Cleanup on exit
  const cleanup = async () => {
    console.log('\n\nCleaning up...');
    await tester.cleanup();
    process.exit(1);
  };

  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
  process.on('uncaughtException', async (error) => {
    console.error('Uncaught exception:', error);
    await cleanup();
  });

  // Find all server.json files
  const dirs = await fs.readdir(registryPath);
  const serverFiles = await Promise.all(
    dirs.map(async (dir) => {
      // Apply server filter if specified
      if (serverFilter && dir !== serverFilter) {
        return null;
      }

      const serverPath = path.join(registryPath, dir, 'server.json');
      try {
        await fs.access(serverPath);
        return serverPath;
      } catch {
        return null;
      }
    })
  );

  const validServerFiles = serverFiles.filter(Boolean) as string[];

  if (!validServerFiles.length) {
    console.log(serverFilter ? `Server '${serverFilter}' not found` : 'No servers found in registry');
    process.exit(1);
  }

  for (const serverFile of validServerFiles.sort()) {
    const passed = await tester.testServer(serverFile, envVars);
    results.push([path.basename(path.dirname(serverFile)), passed]);
    console.log();
  }

  // Summary
  const passed = results.filter(([, p]) => p).length;
  const total = results.length;

  console.log('='.repeat(50));
  console.log(`Results: ${passed}/${total} passed`);
  console.log('='.repeat(50));

  for (const [name, p] of results) {
    const status = p ? '✓ PASSED' : '✗ FAILED';
    console.log(`${status}: ${name}`);
  }

  process.exit(passed === total ? 0 : 1);
}

main();