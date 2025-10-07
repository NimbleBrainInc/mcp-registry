import { describe, it, expect } from 'vitest';
import AjvModule from 'ajv';
import type { AnySchemaObject } from 'ajv';
import addFormatsModule from 'ajv-formats';

const Ajv = AjvModule.default || AjvModule;
const addFormats = addFormatsModule.default || addFormatsModule;
import { readFile } from 'fs/promises';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

describe('Server Validation', () => {
  const SCHEMA_PATH = join(__dirname, '..', '..', 'schemas', '2025-09-22', 'nimbletools-server.schema.json');

  async function loadSchema() {
    const schemaContent = await readFile(SCHEMA_PATH, 'utf-8');
    return JSON.parse(schemaContent);
  }

  async function fetchExternalSchema(url: string): Promise<AnySchemaObject> {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json() as AnySchemaObject;
  }

  it('should validate a valid server definition', async () => {
    const schema = await loadSchema();
    const ajv = new Ajv({
      allErrors: true,
      verbose: true,
      strict: false,
      loadSchema: fetchExternalSchema
    });
    addFormats(ajv);

    const validate = await ajv.compileAsync(schema);

    const validServer = {
      "$schema": "https://registry.nimbletools.ai/schemas/2025-09-22/nimbletools-server.schema.json",
      name: 'ai.nimbletools/test-server',
      version: '1.0.0',
      description: 'A test server',
      status: 'active',
      repository: {
        url: 'https://github.com/test/test-server',
        source: 'github',
        branch: 'main'
      },
      packages: [
        {
          registryType: 'oci',
          registryBaseUrl: 'https://docker.io',
          identifier: 'test/test-server',
          version: '1.0.0',
          transport: {
            type: 'streamable-http',
            url: 'https://test.example.com/mcp'
          }
        }
      ],
      _meta: {
        'ai.nimbletools.mcp/v1': {
          capabilities: {
            tools: true,
            resources: false,
            prompts: false
          }
        }
      }
    };

    const valid = validate(validServer);
    expect(valid).toBe(true);
    expect(validate.errors).toBeNull();
  });

  it('should reject server without required fields', async () => {
    const schema = await loadSchema();
    const ajv = new Ajv({
      allErrors: true,
      verbose: true,
      strict: false,
      loadSchema: fetchExternalSchema
    });
    addFormats(ajv);

    const validate = await ajv.compileAsync(schema);

    const invalidServer = {
      name: 'test-server'
      // missing required fields
    };

    const valid = validate(invalidServer);
    expect(valid).toBe(false);
    expect(validate.errors).toBeTruthy();
    expect(validate.errors?.length).toBeGreaterThan(0);
  });

  it('should reject server with invalid transport type', async () => {
    const schema = await loadSchema();
    const ajv = new Ajv({
      allErrors: true,
      verbose: true,
      strict: false,
      loadSchema: fetchExternalSchema
    });
    addFormats(ajv);

    const validate = await ajv.compileAsync(schema);

    const invalidServer = {
      name: 'test-server',
      version: '1.0.0',
      description: 'A test server',
      transport: {
        type: 'invalid-type',
        command: 'node'
      },
      config: {
        tools: []
      }
    };

    const valid = validate(invalidServer);
    expect(valid).toBe(false);
    expect(validate.errors).toBeTruthy();
  });

  it('should validate server with secrets', async () => {
    const schema = await loadSchema();
    const ajv = new Ajv({
      allErrors: true,
      verbose: true,
      strict: false,
      loadSchema: fetchExternalSchema
    });
    addFormats(ajv);

    const validate = await ajv.compileAsync(schema);

    const serverWithSecrets = {
      "$schema": "https://registry.nimbletools.ai/schemas/2025-09-22/nimbletools-server.schema.json",
      name: 'ai.nimbletools/test-server-with-secrets',
      version: '1.0.0',
      description: 'A test server with secrets',
      status: 'active',
      repository: {
        url: 'https://github.com/test/test-server',
        source: 'github',
        branch: 'main'
      },
      packages: [
        {
          registryType: 'oci',
          registryBaseUrl: 'https://docker.io',
          identifier: 'test/test-server',
          version: '1.0.0',
          transport: {
            type: 'streamable-http',
            url: 'https://test.example.com/mcp',
            env: {
              API_KEY: {
                secret: true
              }
            }
          }
        }
      ],
      _meta: {
        'ai.nimbletools.mcp/v1': {
          capabilities: {
            tools: true,
            resources: false,
            prompts: false
          }
        }
      }
    };

    const valid = validate(serverWithSecrets);
    expect(valid).toBe(true);
    expect(validate.errors).toBeNull();
  });
});
