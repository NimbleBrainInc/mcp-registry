#!/usr/bin/env tsx

/**
 * Generate TypeScript types from schemas
 * All types are auto-generated from the schema files
 */

import { quicktype, InputData, JSONSchemaInput, JSONSchemaStore } from 'quicktype-core';
import { readFile, writeFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function generateAllTypes() {
  console.log('🔧 Generating all types from schemas...\n');

  let allTypes = `/**
 * Auto-generated TypeScript types for NimbleBrain MCP Registry
 * DO NOT EDIT MANUALLY
 * Generated: ${new Date().toISOString()}
 */

`;

  // Load our NimbleBrain schema which extends MCP
  console.log('📥 Loading NimbleBrain server schema...');
  const schemaPath = join(__dirname, '..', 'schemas', '2025-09-22', 'nimblebrain-server.schema.json');
  const nimbleSchemaText = await readFile(schemaPath, 'utf-8');
  const nimbleSchema = JSON.parse(nimbleSchemaText);

  // Fetch the MCP schema that our schema extends
  console.log('📥 Fetching MCP server schema...');
  const mcpResponse = await fetch('https://static.modelcontextprotocol.io/schemas/2025-09-16/server.schema.json');
  if (!mcpResponse.ok) {
    throw new Error(`Failed to fetch MCP schema: ${mcpResponse.status}`);
  }
  const mcpSchemaText = await mcpResponse.text();
  const mcpSchema = JSON.parse(mcpSchemaText);

  // Create a merged schema that includes both MCP base and our extensions
  // Since our schema uses allOf to extend MCP, we need to handle this properly
  const mergedSchema = {
    ...mcpSchema,
    title: nimbleSchema.title,
    description: nimbleSchema.description,
    properties: {
      ...mcpSchema.properties,
      ...(nimbleSchema.allOf?.[1]?.properties || {})
    },
    definitions: {
      ...mcpSchema.definitions,
      ...nimbleSchema.definitions
    }
  };

  // Generate types from the merged schema
  const inputData = new InputData();
  const schemaInput = new JSONSchemaInput(new JSONSchemaStore());

  await schemaInput.addSource({
    name: 'NimbleBrainServer',
    schema: JSON.stringify(mergedSchema)
  });

  inputData.addInput(schemaInput);

  const result = await quicktype({
    inputData,
    lang: 'typescript',
    rendererOptions: {
      'just-types': 'true',
      'prefer-unions': 'true',
      'prefer-const-values': 'true',
      'nice-property-names': 'false',  // Keep original property names
      'explicit-unions': 'true'
    }
  });

  allTypes += '// ============================================================================\n';
  allTypes += '// Generated Types from NimbleBrain Server Schema\n';
  allTypes += '// ============================================================================\n\n';
  allTypes += result.lines.join('\n') + '\n\n';

  // Add convenient type aliases
  allTypes += '// ============================================================================\n';
  allTypes += '// Type Aliases for Convenience\n';
  allTypes += '// ============================================================================\n\n';
  allTypes += `// Main server type
export type MCPServerDetail = NimbleBrainServer;

`;

  // Add API response types (these are specific to our API, not in the schema)
  allTypes += '// ============================================================================\n';
  allTypes += '// API Response Types\n';
  allTypes += '// ============================================================================\n\n';
  allTypes += `export interface ServerListResponse {
  servers: MCPServerDetail[];
  metadata?: {
    next_cursor?: string;
    count?: number;
  };
}

export interface ErrorResponse {
  error: string;
}

export interface VersionListResponse {
  servers: MCPServerDetail[];
  metadata?: {
    count?: number;
  };
}

export interface HealthResponse {
  status: 'healthy' | 'unhealthy';
  servers_loaded: number;
  cache_age_ms?: number;
}

export interface RootResponse {
  name: string;
  version: string;
  endpoints: {
    listServers: string;
    getServer: string;
    getServerVersions: string;
    schemas: string;
    schemaByVersion: string;
    latestSchema: string;
  };
  documentation: string;
}

// Registry metadata we add to servers at runtime
export interface RegistryMetadata {
  serverId: string;
  versionId: string;
  publishedAt: string;
  updatedAt: string;
  isLatest: boolean;
}
`;

  return allTypes;
}

async function main() {
  try {
    const types = await generateAllTypes();

    // Write to single file
    const outputPath = join(__dirname, '..', 'src', 'types', 'generated.ts');
    await writeFile(outputPath, types);

    console.log(`\n✅ Generated ${outputPath}`);
    console.log('✨ All types generated successfully from schemas!');

  } catch (error) {
    console.error('❌ Error generating types:', error);
    process.exit(1);
  }
}

main();