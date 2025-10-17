/**
 * Test fixture types and utilities for E2E testing
 */

export interface TestExpectation {
  type: 'text' | 'json' | 'any' | 'object';
  contains?: string;
  equals?: any;
  schema?: Record<string, any>;
  field?: string; // For JSON: check specific field value
  hasKeys?: string[]; // For object: check if specific keys exist
}

export interface ToolTest {
  name: string;
  tool: string;
  arguments: Record<string, any>;
  expect?: TestExpectation;
}

export interface ServerTestFixture {
  skip?: boolean;
  skipReason?: string;
  environment?: Record<string, string>;
  tests?: ToolTest[];
}

/**
 * Load test fixture for a server
 */
export async function loadFixture(serverPath: string): Promise<ServerTestFixture | null> {
  try {
    const fixturePath = serverPath.replace('server.json', 'test.json');
    const { default: fs } = await import('fs/promises');
    const content = await fs.readFile(fixturePath, 'utf-8');
    return JSON.parse(content);
  } catch {
    return null; // No fixture = default tests only
  }
}

/**
 * Interpolate environment variables in fixture
 */
export function interpolateEnv(fixture: ServerTestFixture, envVars: Record<string, string>): ServerTestFixture {
  const result = { ...fixture };

  if (result.environment) {
    const env: Record<string, string> = {};
    for (const [key, value] of Object.entries(result.environment)) {
      // Replace ${VAR_NAME} with actual value
      if (value.startsWith('${') && value.endsWith('}')) {
        const varName = value.slice(2, -1);
        const envValue = envVars[varName];
        if (!envValue) {
          throw new Error(`Missing required environment variable: ${varName}`);
        }
        env[key] = envValue;
      } else {
        env[key] = value;
      }
    }
    result.environment = env;
  }

  return result;
}

/**
 * Validate tool response against expectation
 */
export function validateResponse(response: any, expect?: TestExpectation): boolean {
  // Always fail if response indicates an error
  if (response.result?.isError === true) {
    return false;
  }

  if (!expect) return true; // No expectation = pass

  const content = response.result?.content?.[0];
  if (!content) return false;

  switch (expect.type) {
    case 'text':
      const text = content.text || JSON.stringify(content);
      if (expect.contains) {
        return text.includes(expect.contains);
      }
      if (expect.equals !== undefined) {
        return text === expect.equals;
      }
      return true;

    case 'json':
      try {
        const data = typeof content.text === 'string' ? JSON.parse(content.text) : content;

        // Check specific field if specified
        if (expect.field) {
          const fieldValue = data[expect.field];
          if (expect.contains) {
            return String(fieldValue).includes(expect.contains);
          }
          if (expect.equals !== undefined) {
            return fieldValue === expect.equals;
          }
          return fieldValue !== undefined;
        }

        if (expect.equals !== undefined) {
          return JSON.stringify(data) === JSON.stringify(expect.equals);
        }
        return true;
      } catch {
        return false;
      }

    case 'any':
      return true;

    case 'object':
      // Check structuredContent for object validation
      const structuredContent = response.result?.structuredContent;
      if (!structuredContent) return false;

      // If hasKeys is specified, check all keys exist
      if (expect.hasKeys) {
        return expect.hasKeys.every(key => key in structuredContent);
      }

      return true;

    default:
      return false;
  }
}

/**
 * Load environment variables from .env.e2e
 */
export async function loadEnvFile(path: string = '.env.e2e'): Promise<Record<string, string>> {
  try {
    const { default: fs } = await import('fs/promises');
    const { default: pathModule } = await import('path');
    const { fileURLToPath } = await import('url');

    const __dirname = pathModule.dirname(fileURLToPath(import.meta.url));
    const envPath = pathModule.join(__dirname, '..', path);
    const content = await fs.readFile(envPath, 'utf-8');

    const env: Record<string, string> = {};
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;

      const [key, ...valueParts] = trimmed.split('=');
      if (key && valueParts.length > 0) {
        env[key.trim()] = valueParts.join('=').trim();
      }
    }

    return env;
  } catch {
    return {}; // No .env.e2e file = use system env only
  }
}