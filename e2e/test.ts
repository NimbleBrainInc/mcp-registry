#!/usr/bin/env tsx

/**
 * End-to-end test for NimbleTools MCP Registry servers.
 * Tests workspace creation, server deployment, and MCP connectivity.
 *
 * Supports parallel execution with --concurrency=N flag.
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { interpolateEnv, loadFixture, ServerTestFixture, validateResponse } from './fixtures.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Simple concurrency limiter
function createPool(concurrency: number) {
  let running = 0;
  const queue: Array<() => void> = [];

  const next = () => {
    if (queue.length > 0 && running < concurrency) {
      running++;
      const resolve = queue.shift()!;
      resolve();
    }
  };

  return async <T>(fn: () => Promise<T>): Promise<T> => {
    await new Promise<void>((resolve) => {
      queue.push(resolve);
      next();
    });

    try {
      return await fn();
    } finally {
      running--;
      next();
    }
  };
}

// Load .env.e2e at startup
dotenv.config({ path: path.join(__dirname, '..', '.env.e2e') });

// Allow self-signed certificates for local testing
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

interface ServerDefinition {
  name: string;
  version: string;
  title?: string;
  description: string;
  packages?: any[];
  remotes?: Array<{
    type: string;
    url: string;
    description?: string;
  }>;
  environmentVariables?: Array<{
    name: string;
    description?: string;
    isRequired?: boolean;
    isSecret?: boolean;
    header?: string; // Header name for remote server auth
    format?: string; // Format string, e.g., "Bearer ${TAVILY_API_KEY}"
  }>;
  _meta?: {
    'ai.nimbletools.mcp/v1'?: {
      status?: string;
      serverType?: string;
      [key: string]: any;
    };
    [key: string]: any;
  };
}

class NimbleToolsE2ETest {
  private domain: string;
  private protocol: string;
  private port: string | null;
  private skipCleanup: boolean;
  private workspaceId: string | null = null;
  private serverId: string | null = null;
  private mcpSessionId: string | null = null;
  private outputBuffer: string[] = [];
  private bufferedMode: boolean;
  private serverName: string = '';

  constructor(domain = 'nimbletools.dev', protocol = 'http', port: string | null = null, skipCleanup = false, bufferedMode = false) {
    this.domain = domain;
    this.protocol = protocol;
    this.port = port;
    this.skipCleanup = skipCleanup;
    this.bufferedMode = bufferedMode;
  }

  private log(message: string): void {
    if (this.bufferedMode) {
      this.outputBuffer.push(message);
    } else {
      console.log(message);
    }
  }

  getOutput(): string[] {
    return this.outputBuffer;
  }

  getServerName(): string {
    return this.serverName;
  }

  private getApiUrl(): string {
    const baseUrl = `${this.protocol}://api.${this.domain}`;
    return this.port ? `${baseUrl}:${this.port}` : baseUrl;
  }

  private getMcpUrl(): string {
    const baseUrl = `${this.protocol}://mcp.${this.domain}`;
    return this.port ? `${baseUrl}:${this.port}` : baseUrl;
  }

  private async request(method: string, url: string, body?: any, isMcp = false, isNotification = false, extraHeaders: Record<string, string> = {}): Promise<any> {
    try {
      const headers: Record<string, string> = body ? { 'Content-Type': 'application/json' } : {};
      Object.assign(headers, extraHeaders);

      // When using a custom port, set Host header without port (nginx ingress expects this)
      if (this.port) {
        const urlObj = new URL(url);
        headers['Host'] = urlObj.hostname;
      }

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
          this.log(`  Session ID: ${sessionId}`);
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

      // Parse SSE format if present (may have multiple events)
      if (text.startsWith('event:')) {
        // SSE format: "event: message\ndata: {...}\n\nevent: message\ndata: {...}\n\n"
        // Find all data lines and return the last one with an id (the actual response)
        const dataMatches = text.matchAll(/data: (.+)/g);
        let lastResult: any = null;
        for (const match of dataMatches) {
          try {
            const parsed = JSON.parse(match[1]);
            // Prefer responses with id (actual RPC responses) over notifications
            if (parsed.id !== undefined || lastResult === null) {
              lastResult = parsed;
            }
          } catch {
            // Skip unparseable data lines
          }
        }
        if (lastResult) {
          return lastResult;
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
    const data = await this.request('POST', `${this.getApiUrl()}/v1/workspaces`, {
      name: `test-${Date.now()}`,
      description: 'E2E test workspace',
    });
    return data.workspace_id;
  }

  async setSecret(key: string, value: string): Promise<void> {
    await this.request(
      'PUT',
      `${this.getApiUrl()}/v1/workspaces/${this.workspaceId}/secrets/${key}`,
      { secret_value: value }
    );
  }

  async deployServer(serverDef: ServerDefinition, environment: Record<string, string> = {}): Promise<string> {
    const data = await this.request(
      'POST',
      `${this.getApiUrl()}/v1/workspaces/${this.workspaceId}/servers`,
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
        `${this.getApiUrl()}/v1/workspaces/${this.workspaceId}/servers/${this.serverId}`
      );

      const currentStatus = `${data.status.phase} (ready: ${data.status.deployment_ready}, replicas: ${data.status.ready_replicas}/${data.status.replicas})`;

      if (currentStatus !== lastStatus) {
        this.log(`  Status: ${currentStatus}`);
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
      `${this.getApiUrl()}/v1/workspaces/${this.workspaceId}/servers/${this.serverId}`
    );

    // MCP endpoints use mcp subdomain
    const mcpUrl = `${this.getMcpUrl()}${serverDetails.status.service_endpoint}`;
    this.log(`  MCP URL: ${mcpUrl}`);

    // Wait for MCP endpoint to be available (with retries)
    let resp: any;
    let retries = 3;
    let lastError: Error | null = null;

    // Initialize with retries
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
        retries--;
        if (error instanceof Error && (error.message.includes('502') || error.message.includes('503'))) {
          if (retries > 0) {
            this.log(`  Waiting for MCP endpoint... (${retries} retries left)`);
            await new Promise((resolve) => setTimeout(resolve, 5000));
            continue;
          }
        }
        throw error; // Don't retry other errors or if retries exhausted
      }
    }

    if (!resp?.result) {
      throw new Error(`Initialize failed after retries: ${lastError?.message}`);
    }

    // Send notifications/initialized (required by MCP protocol) with retries
    retries = 3;
    while (retries > 0) {
      try {
        await this.request('POST', mcpUrl, {
          jsonrpc: '2.0',
          method: 'notifications/initialized',
        }, true, true); // isMcp = true, isNotification = true
        break;
      } catch (error) {
        retries--;
        if (error instanceof Error && (error.message.includes('502') || error.message.includes('503')) && retries > 0) {
          this.log(`  Waiting for MCP endpoint... (${retries} retries left)`);
          await new Promise((resolve) => setTimeout(resolve, 5000));
          continue;
        }
        throw error;
      }
    }

    // List tools (no params field!) with retries
    retries = 3;
    while (retries > 0) {
      try {
        resp = await this.request('POST', mcpUrl, {
          jsonrpc: '2.0',
          id: 2,
          method: 'tools/list',
        }, true); // isMcp = true
        break;
      } catch (error) {
        retries--;
        if (error instanceof Error && (error.message.includes('502') || error.message.includes('503')) && retries > 0) {
          this.log(`  Waiting for MCP endpoint... (${retries} retries left)`);
          await new Promise((resolve) => setTimeout(resolve, 5000));
          continue;
        }
        throw error;
      }
    }

    if (!resp.result?.tools?.length) throw new Error('No tools found');

    // Call first tool with retries
    const toolName = resp.result.tools[0].name;
    retries = 3;
    while (retries > 0) {
      try {
        resp = await this.request('POST', mcpUrl, {
          jsonrpc: '2.0',
          id: 3,
          method: 'tools/call',
          params: { name: toolName, arguments: { message: 'Test' } },
        }, true); // isMcp = true
        break;
      } catch (error) {
        retries--;
        if (error instanceof Error && (error.message.includes('502') || error.message.includes('503')) && retries > 0) {
          this.log(`  Waiting for MCP endpoint... (${retries} retries left)`);
          await new Promise((resolve) => setTimeout(resolve, 5000));
          continue;
        }
        throw error;
      }
    }

    if (!resp.result) {
      this.log(`  Tool call response: ${JSON.stringify(resp, null, 2)}`);
      throw new Error('Tool call failed');
    }
  }

  async runFixtureTests(fixture: ServerTestFixture): Promise<void> {
    if (!fixture.tests) return;

    const serverDetails = await this.request(
      'GET',
      `${this.getApiUrl()}/v1/workspaces/${this.workspaceId}/servers/${this.serverId}`
    );
    const mcpUrl = `${this.getMcpUrl()}${serverDetails.status.service_endpoint}`;

    for (const test of fixture.tests) {
      try {
        let resp: any;
        let retries = 3;

        // Retry logic for fixture test calls
        while (retries > 0) {
          try {
            resp = await this.request('POST', mcpUrl, {
              jsonrpc: '2.0',
              id: 99,
              method: 'tools/call',
              params: { name: test.tool, arguments: test.arguments },
            }, true);
            break;
          } catch (error) {
            retries--;
            if (error instanceof Error && (error.message.includes('502') || error.message.includes('503')) && retries > 0) {
              this.log(`  Waiting for MCP endpoint... (${retries} retries left)`);
              await new Promise((resolve) => setTimeout(resolve, 5000));
              continue;
            }
            throw error;
          }
        }

        // Debug: log the actual response
        this.log(`  Response: ${JSON.stringify(resp, null, 2)}`);

        // Check for error response
        if (resp.result?.isError) {
          const errorText = resp.result.content?.[0]?.text || 'Unknown error';
          throw new Error(`Tool returned error: ${errorText}`);
        }

        if (test.expect && !validateResponse(resp, test.expect)) {
          throw new Error(`Test failed validation: ${test.name}`);
        }

        this.log(`  ✓ Test passed: ${test.name}`);
      } catch (error) {
        throw new Error(`Test failed: ${test.name} - ${error}`);
      }
    }
  }

  async cleanup(): Promise<void> {
    if (this.skipCleanup) {
      if (this.workspaceId) {
        this.log(`  ⚠ Skipping cleanup (--skip-cleanup). Workspace: ${this.workspaceId}`);
      }
      return;
    }
    if (this.workspaceId) {
      try {
        await this.request('DELETE', `${this.getApiUrl()}/v1/workspaces/${this.workspaceId}`);
      } catch (e) {
        console.warn(`Warning: Cleanup failed: ${e}`);
      }
    }
  }

  async testRemoteServer(
    serverPath: string,
    serverDef: ServerDefinition,
    fixture: ServerTestFixture | null,
    envVars: Record<string, string>
  ): Promise<boolean> {
    const serverName = path.basename(path.dirname(serverPath));
    const mcpUrl = serverDef.remotes![0].url;

    // Build auth headers from environmentVariables with header field
    const authHeaders: Record<string, string> = {};
    if (serverDef.environmentVariables) {
      for (const envVar of serverDef.environmentVariables) {
        if (envVar.header && envVars[envVar.name]) {
          // Apply format if specified (e.g., "Bearer ${TAVILY_API_KEY}")
          let headerValue = envVars[envVar.name];
          if (envVar.format) {
            headerValue = envVar.format.replace(`\${${envVar.name}}`, envVars[envVar.name]);
          }
          authHeaders[envVar.header] = headerValue;
        }
      }
    }

    try {
      // Reset state
      this.mcpSessionId = null;

      this.log(`Testing ${serverName} (remote)...`);
      this.log(`  MCP URL: ${mcpUrl}`);
      if (Object.keys(authHeaders).length > 0) {
        this.log(`  Auth headers: ${Object.keys(authHeaders).join(', ')}`);
      }

      // Initialize MCP connection
      let resp: any;
      let retries = 3;

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
          }, true, false, authHeaders);

          if (resp.result) break;
        } catch (error) {
          retries--;
          if (error instanceof Error && (error.message.includes('502') || error.message.includes('503')) && retries > 0) {
            this.log(`  Waiting for MCP endpoint... (${retries} retries left)`);
            await new Promise((resolve) => setTimeout(resolve, 5000));
            continue;
          }
          throw error;
        }
      }

      if (!resp?.result) {
        throw new Error('Initialize failed');
      }
      this.log(`  ✓ MCP initialized`);

      // Send notifications/initialized
      await this.request('POST', mcpUrl, {
        jsonrpc: '2.0',
        method: 'notifications/initialized',
      }, true, true, authHeaders);

      // List tools
      resp = await this.request('POST', mcpUrl, {
        jsonrpc: '2.0',
        id: 2,
        method: 'tools/list',
      }, true, false, authHeaders);

      if (!resp.result?.tools?.length) {
        throw new Error('No tools found');
      }
      this.log(`  ✓ Tools listed: ${resp.result.tools.map((t: any) => t.name).join(', ')}`);

      // Run fixture tests
      if (fixture?.tests && fixture.tests.length > 0) {
        await this.runFixtureTestsRemote(fixture, mcpUrl, authHeaders);
      }

      this.log(`✓ ${serverName}: PASSED (remote)`);
      return true;
    } catch (e) {
      this.log(`✗ ${serverName}: FAILED - ${e}`);
      return false;
    }
  }

  async runFixtureTestsRemote(fixture: ServerTestFixture, mcpUrl: string, authHeaders: Record<string, string>): Promise<void> {
    if (!fixture.tests) return;

    for (const test of fixture.tests) {
      try {
        let resp: any;
        let retries = 3;

        while (retries > 0) {
          try {
            resp = await this.request('POST', mcpUrl, {
              jsonrpc: '2.0',
              id: 99,
              method: 'tools/call',
              params: { name: test.tool, arguments: test.arguments },
            }, true, false, authHeaders);
            break;
          } catch (error) {
            retries--;
            if (error instanceof Error && (error.message.includes('502') || error.message.includes('503')) && retries > 0) {
              this.log(`  Waiting for MCP endpoint... (${retries} retries left)`);
              await new Promise((resolve) => setTimeout(resolve, 5000));
              continue;
            }
            throw error;
          }
        }

        this.log(`  Response: ${JSON.stringify(resp, null, 2)}`);

        if (resp.result?.isError) {
          const errorText = resp.result.content?.[0]?.text || 'Unknown error';
          throw new Error(`Tool returned error: ${errorText}`);
        }

        if (test.expect && !validateResponse(resp, test.expect)) {
          throw new Error(`Test failed validation: ${test.name}`);
        }

        this.log(`  ✓ Test passed: ${test.name}`);
      } catch (error) {
        throw new Error(`Test failed: ${test.name} - ${error}`);
      }
    }
  }

  async testServer(serverPath: string, envVars: Record<string, string>): Promise<boolean> {
    const serverName = path.basename(path.dirname(serverPath));
    this.serverName = serverName;

    try {
      // Reset state for each test
      this.workspaceId = null;
      this.serverId = null;
      this.mcpSessionId = null;
      this.outputBuffer = [];

      // Load server definition
      const serverDef = JSON.parse(await fs.readFile(serverPath, 'utf-8')) as ServerDefinition;

      // Skip non-active servers (status is in _meta.ai.nimbletools.mcp/v1.status)
      const serverStatus = serverDef._meta?.['ai.nimbletools.mcp/v1']?.status;
      if (serverStatus !== 'active') {
        this.log(`⊘ ${serverName}: Skipped (status: ${serverStatus})`);
        return true;
      }

      // Load test fixture
      const fixture = await loadFixture(serverPath);

      // Check if server should be skipped
      if (fixture?.skip) {
        this.log(`⊘ ${serverName}: Skipped (${fixture.skipReason || 'no reason given'})`);
        return true;
      }

      // Check if this is a remote server (has remotes array)
      if (serverDef.remotes && serverDef.remotes.length > 0) {
        return await this.testRemoteServer(serverPath, serverDef, fixture, envVars);
      }

      this.log(`Testing ${serverName}...`);

      // Create workspace
      this.workspaceId = await this.createWorkspace();
      this.log(`  ✓ Workspace created: ${this.workspaceId}`);

      // Interpolate environment variables if fixture exists
      let environment = {};
      if (fixture?.environment) {
        const interpolated = interpolateEnv(fixture, envVars);
        environment = interpolated.environment || {};

        // Set secrets in workspace before deployment
        for (const [key, value] of Object.entries(environment)) {
          await this.setSecret(key, value);
          this.log(`  ✓ Secret set: ${key}`);
        }
      }

      // Deploy server (secrets are auto-injected)
      this.serverId = await this.deployServer(serverDef);
      this.log(`  ✓ Server deployed: ${this.serverId}`);

      // Wait for ready
      await this.waitForServerReady();
      this.log(`  ✓ Server ready`);

      // Test MCP connection
      await this.testMcpConnection();
      this.log(`  ✓ MCP connection verified`);

      // Run fixture tests if they exist
      if (fixture?.tests && fixture.tests.length > 0) {
        await this.runFixtureTests(fixture);
      }

      // Cleanup
      await this.cleanup();
      this.log(`✓ ${serverName}: PASSED`);
      return true;
    } catch (e) {
      this.log(`✗ ${serverName}: FAILED - ${e}`);
      await this.cleanup();
      return false;
    }
  }
}

interface TestResult {
  name: string;
  passed: boolean;
  output: string[];
}

async function main() {
  // Parse arguments
  const args = process.argv.slice(2);
  let domain = 'nimbletools.dev';
  let serverFilter: string | null = null;
  let insecure = false;
  let port: string | null = null;
  let skipCleanup = false;
  let concurrency = 4;

  for (const arg of args) {
    if (arg.startsWith('--server=')) {
      serverFilter = arg.split('=')[1];
    } else if (arg.startsWith('--domain=')) {
      domain = arg.substring('--domain='.length);
    } else if (arg.startsWith('--port=')) {
      port = arg.substring('--port='.length);
    } else if (arg.startsWith('--concurrency=')) {
      concurrency = parseInt(arg.substring('--concurrency='.length), 10);
      if (isNaN(concurrency) || concurrency < 1) concurrency = 4;
    } else if (arg === '--insecure') {
      insecure = true;
    } else if (arg === '--skip-cleanup') {
      skipCleanup = true;
    } else if (arg === '--sequential') {
      concurrency = 1;
    } else if (arg === '--help' || arg === '-h') {
      console.log(`NimbleTools MCP Registry E2E Test

Usage:
  npm run test:e2e -- [options]

Options:
  --domain=<domain>       Base domain (default: nimbletools.dev)
  --port=<port>           Custom port
  --server=<name>         Test only this server
  --concurrency=<n>       Run up to N tests in parallel (default: 4)
  --sequential            Run tests one at a time (same as --concurrency=1)
  --insecure              Use HTTP instead of HTTPS
  --skip-cleanup          Don't delete workspace after test (for debugging)
  --help, -h              Show this help

Examples:
  # Test all servers in parallel (4 at a time)
  npm run test:e2e

  # Test with higher parallelism
  npm run test:e2e -- --concurrency=8

  # Test echo server only
  npm run test:e2e -- --server=echo

  # Test against local cluster with port
  npm run test:e2e -- --domain=nt.dev --port=8080 --insecure --server=echo
`);
      process.exit(0);
    }
  }

  const protocol = insecure ? 'http' : 'https';
  const registryPath = path.join(__dirname, '..', 'servers');
  const isParallel = concurrency > 1;

  console.log(`NimbleTools MCP Registry E2E Test`);
  console.log(`Domain: ${domain}`);
  console.log(`Protocol: ${protocol}`);
  if (port) console.log(`Port: ${port}`);
  console.log(`API URL: ${protocol}://api.${domain}${port ? ':' + port : ''}`);
  console.log(`MCP URL: ${protocol}://mcp.${domain}${port ? ':' + port : ''}`);
  console.log(`Registry: ${registryPath}`);
  console.log(`Concurrency: ${concurrency}${isParallel ? ' (parallel)' : ' (sequential)'}`);
  if (serverFilter) console.log(`Filter: ${serverFilter}`);
  console.log();

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

  const sortedFiles = validServerFiles.sort();
  const results: TestResult[] = [];
  let completedCount = 0;

  // Progress tracker for parallel mode
  const printProgress = () => {
    if (isParallel) {
      process.stdout.write(`\rProgress: ${completedCount}/${sortedFiles.length} completed`);
    }
  };

  if (isParallel) {
    // Parallel execution with concurrency limit
    console.log(`Running ${sortedFiles.length} tests with concurrency ${concurrency}...\n`);

    const pool = createPool(concurrency);

    const testPromises = sortedFiles.map((serverFile) =>
      pool(async (): Promise<TestResult> => {
        const tester = new NimbleToolsE2ETest(domain, protocol, port, skipCleanup, true);
        const passed = await tester.testServer(serverFile, process.env as Record<string, string>);
        completedCount++;
        printProgress();
        return {
          name: tester.getServerName(),
          passed,
          output: tester.getOutput(),
        };
      })
    );

    const testResults = await Promise.all(testPromises);
    results.push(...testResults);

    // Clear progress line
    process.stdout.write('\r' + ' '.repeat(50) + '\r');

    // Print all outputs in order
    console.log('\n' + '='.repeat(50));
    console.log('Test Output');
    console.log('='.repeat(50) + '\n');

    for (const result of results) {
      for (const line of result.output) {
        console.log(line);
      }
      console.log();
    }
  } else {
    // Sequential execution (original behavior)
    const tester = new NimbleToolsE2ETest(domain, protocol, port, skipCleanup, false);

    // Cleanup on exit for sequential mode
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

    for (const serverFile of sortedFiles) {
      const passed = await tester.testServer(serverFile, process.env as Record<string, string>);
      results.push({
        name: path.basename(path.dirname(serverFile)),
        passed,
        output: [],
      });
      console.log();
    }
  }

  // Summary
  const passed = results.filter((r) => r.passed).length;
  const total = results.length;

  console.log('='.repeat(50));
  console.log(`Results: ${passed}/${total} passed`);
  console.log('='.repeat(50));

  for (const result of results) {
    const status = result.passed ? '✓ PASSED' : '✗ FAILED';
    console.log(`${status}: ${result.name}`);
  }

  process.exit(passed === total ? 0 : 1);
}

main();