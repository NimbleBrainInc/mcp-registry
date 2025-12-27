#!/usr/bin/env tsx

/**
 * Validate all server.json files against the nimbletools-server.schema.json
 */

import Ajv2020 from 'ajv/dist/2020.js';
import ajvFormats from 'ajv-formats';
import { readdir, readFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SERVERS_DIR = join(__dirname, '..', 'servers');
const SCHEMAS_DIR = join(__dirname, '..', 'schemas');

// Current schema version
const SCHEMA_VERSION = '2025-12-11';

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

async function loadSchema() {
  // Use bundled schema (all $refs resolved) to avoid network fetches
  const schemaPath = join(SCHEMAS_DIR, SCHEMA_VERSION, 'nimbletools-server.bundled.schema.json');
  try {
    const schemaContent = await readFile(schemaPath, 'utf-8');
    return JSON.parse(schemaContent);
  } catch (error) {
    console.error(`${colors.red}❌ Failed to load schema from ${schemaPath}${colors.reset}`);
    throw error;
  }
}

async function validateServers() {
  console.log(`${colors.blue}🔍 Validating server definitions...${colors.reset}`);
  console.log(`${colors.blue}   Schema version: ${SCHEMA_VERSION}${colors.reset}\n`);

  // Initialize AJV with draft 2020-12 support (for unevaluatedProperties)
  const ajv = new Ajv2020({
    allErrors: true,
    verbose: true,
    strict: false
  });
  ajvFormats(ajv);

  // Compile validator (bundled schema has all $refs resolved)
  console.log(`${colors.blue}📦 Loading schema ${SCHEMA_VERSION}...${colors.reset}`);
  const schema = await loadSchema();
  const validate = ajv.compile(schema);
  console.log(`${colors.green}   ✓ Schema compiled${colors.reset}\n`);

  // Get all server directories
  const entries = await readdir(SERVERS_DIR, { withFileTypes: true });
  const serverDirs = entries.filter(entry => entry.isDirectory());

  let totalServers = 0;
  let validServers = 0;
  let invalidServers = 0;
  const errors: { server: string; errors: any[] }[] = [];

  // Validate each server
  for (const dir of serverDirs) {
    const serverJsonPath = join(SERVERS_DIR, dir.name, 'server.json');

    try {
      const serverContent = await readFile(serverJsonPath, 'utf-8');
      const serverData = JSON.parse(serverContent);

      totalServers++;

      // Check schema version matches
      const schemaUrl = serverData.$schema;
      if (schemaUrl && !schemaUrl.includes(SCHEMA_VERSION)) {
        invalidServers++;
        console.log(`${colors.red}❌ ${dir.name}${colors.reset} - Wrong schema version: ${schemaUrl}`);
        console.log(`   ${colors.yellow}└─ Expected: ${SCHEMA_VERSION}${colors.reset}`);
        errors.push({
          server: dir.name,
          errors: [{ message: `Wrong schema version. Expected ${SCHEMA_VERSION}, got ${schemaUrl}` }]
        });
        continue;
      }

      const valid = validate(serverData);

      if (valid) {
        validServers++;
        console.log(`${colors.green}✅ ${dir.name}${colors.reset}`);
      } else {
        invalidServers++;
        console.log(`${colors.red}❌ ${dir.name}${colors.reset} - Invalid`);
        errors.push({
          server: dir.name,
          errors: validate.errors || []
        });

        // Print errors for this server
        if (validate.errors) {
          validate.errors.forEach(error => {
            console.log(`   ${colors.yellow}└─ ${error.instancePath || '/'}: ${error.message}${colors.reset}`);
            if (error.params) {
              console.log(`      ${colors.yellow}Parameters: ${JSON.stringify(error.params)}${colors.reset}`);
            }
          });
        }
      }
    } catch (error: any) {
      totalServers++;
      invalidServers++;
      console.log(`${colors.red}❌ ${dir.name}${colors.reset} - Failed to read or parse`);
      console.log(`   ${colors.yellow}└─ ${error.message}${colors.reset}`);
      errors.push({
        server: dir.name,
        errors: [{ message: error.message }]
      });
    }
  }

  // Print summary
  console.log(`\n${colors.blue}═══════════════════════════════${colors.reset}`);
  console.log(`${colors.blue}📊 Validation Summary${colors.reset}`);
  console.log(`${colors.blue}═══════════════════════════════${colors.reset}`);
  console.log(`Total servers: ${totalServers}`);
  console.log(`${colors.green}Valid: ${validServers}${colors.reset}`);
  console.log(`${colors.red}Invalid: ${invalidServers}${colors.reset}`);

  if (invalidServers > 0) {
    console.log(`\n${colors.red}❌ Validation failed! Fix the errors above.${colors.reset}`);
    process.exit(1);
  } else {
    console.log(`\n${colors.green}✨ All servers are valid!${colors.reset}`);
  }
}

// Run validation
validateServers().catch(error => {
  console.error(`${colors.red}Fatal error:${colors.reset}`, error);
  process.exit(1);
});
