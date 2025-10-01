#!/usr/bin/env tsx
/**
 * Standalone MCP Server Deployment Script
 *
 * Deploy an MCP server to NimbleTools platform from a server.json file.
 * No dependencies on the registry codebase - fully portable.
 *
 * Usage:
 *   tsx deploy-server.ts <path-to-server.json> [options]
 *
 * Options:
 *   --api <url>         API base URL (default: https://api.nt.dev)
 *   --workspace <id>    Workspace ID (required)
 *   --env KEY=VALUE     Set environment variable/secret
 *   --replicas <n>      Number of replicas (default: 1)
 *
 * Examples:
 *   tsx deploy-server.ts ./server.json --workspace abc-123
 *   tsx deploy-server.ts ./server.json --workspace abc-123 --env API_KEY=secret123
 *   tsx deploy-server.ts ./server.json --api https://api.nimbletools.ai --workspace abc-123
 */

import fs from 'fs/promises';
import path from 'path';

interface DeployOptions {
  apiUrl: string;
  workspaceId: string;
  environment: Record<string, string>;
  replicas: number;
}

async function deployServer(serverJsonPath: string, options: DeployOptions): Promise<void> {
  try {
    // Read server.json
    console.log(`📄 Reading server definition: ${serverJsonPath}`);
    const serverJson = await fs.readFile(serverJsonPath, 'utf-8');
    const serverDef = JSON.parse(serverJson);

    console.log(`📦 Server: ${serverDef.name} v${serverDef.version}`);
    console.log(`📝 Description: ${serverDef.description}`);

    // Set secrets if environment variables provided
    if (Object.keys(options.environment).length > 0) {
      console.log(`\n🔐 Setting secrets...`);
      for (const [key, value] of Object.entries(options.environment)) {
        await setSecret(options.apiUrl, options.workspaceId, key, value);
        console.log(`  ✓ ${key} set`);
      }
    }

    // Deploy server
    console.log(`\n🚀 Deploying server to workspace ${options.workspaceId}...`);
    const deployment = await createDeployment(
      options.apiUrl,
      options.workspaceId,
      serverDef,
      options.replicas
    );

    console.log(`\n✅ Server deployed successfully!`);
    console.log(`  Server ID: ${deployment.server_id}`);
    console.log(`  Status: ${deployment.status}`);
    console.log(`  Endpoint: ${deployment.service_endpoint}`);

    // Wait for ready
    console.log(`\n⏳ Waiting for server to be ready...`);
    await waitForReady(options.apiUrl, options.workspaceId, deployment.server_id);

    console.log(`\n🎉 Server is ready and running!`);
    console.log(`\nMCP Endpoint: ${options.apiUrl.replace('api.nt', 'mcp.nt')}${deployment.service_endpoint}`);

  } catch (error) {
    console.error(`\n❌ Deployment failed:`, error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

async function setSecret(apiUrl: string, workspaceId: string, key: string, value: string): Promise<void> {
  const response = await fetch(
    `${apiUrl}/v1/workspaces/${workspaceId}/secrets/${key}`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ secret_value: value })
    }
  );

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Failed to set secret ${key}: ${response.status} ${text}`);
  }
}

async function createDeployment(
  apiUrl: string,
  workspaceId: string,
  serverDef: any,
  replicas: number
): Promise<any> {
  const response = await fetch(
    `${apiUrl}/v1/workspaces/${workspaceId}/servers`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        server: serverDef,
        replicas,
        environment: {}
      })
    }
  );

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Deployment failed: ${response.status} ${text}`);
  }

  return response.json();
}

async function waitForReady(
  apiUrl: string,
  workspaceId: string,
  serverId: string,
  timeout = 120000
): Promise<void> {
  const startTime = Date.now();
  let lastStatus = '';

  while (Date.now() - startTime < timeout) {
    const response = await fetch(
      `${apiUrl}/v1/workspaces/${workspaceId}/servers/${serverId}`
    );

    if (!response.ok) {
      throw new Error(`Failed to get server status: ${response.status}`);
    }

    const data = await response.json();
    const status = `${data.status.phase} (ready: ${data.status.deployment_ready}, replicas: ${data.status.ready_replicas}/${data.status.replicas})`;

    if (status !== lastStatus) {
      console.log(`  Status: ${status}`);
      lastStatus = status;
    }

    if (data.status.deployment_ready && data.status.ready_replicas > 0) {
      return;
    }

    if (data.status.phase === 'Failed') {
      throw new Error(`Server deployment failed: ${JSON.stringify(data.status)}`);
    }

    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  throw new Error(`Server not ready after ${timeout}ms`);
}

// Parse command line arguments
function parseArgs(): { serverJsonPath: string; options: DeployOptions } {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0].startsWith('--')) {
    console.error('Usage: tsx deploy-server.ts <server.json> [options]');
    console.error('\nOptions:');
    console.error('  --api <url>         API base URL (default: https://api.nt.dev)');
    console.error('  --workspace <id>    Workspace ID (required)');
    console.error('  --env KEY=VALUE     Set environment variable/secret');
    console.error('  --replicas <n>      Number of replicas (default: 1)');
    process.exit(1);
  }

  const serverJsonPath = args[0];
  const options: DeployOptions = {
    apiUrl: 'https://api.nt.dev',
    workspaceId: '',
    environment: {},
    replicas: 1
  };

  for (let i = 1; i < args.length; i++) {
    switch (args[i]) {
      case '--api':
        options.apiUrl = args[++i];
        break;
      case '--workspace':
        options.workspaceId = args[++i];
        break;
      case '--env':
        const [key, value] = args[++i].split('=');
        if (key && value) {
          options.environment[key] = value;
        }
        break;
      case '--replicas':
        options.replicas = parseInt(args[++i]);
        break;
    }
  }

  if (!options.workspaceId) {
    console.error('Error: --workspace is required');
    process.exit(1);
  }

  return { serverJsonPath, options };
}

// Main execution
const { serverJsonPath, options } = parseArgs();
deployServer(serverJsonPath, options);