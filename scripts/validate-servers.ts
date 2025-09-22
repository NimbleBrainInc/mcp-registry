#!/usr/bin/env tsx

/**
 * Validate all server.json files against the nimbletools-server.schema.json
 */

import { readdir, readFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SERVERS_DIR = join(__dirname, '..', 'servers');
const SCHEMA_PATH = join(__dirname, '..', 'schemas', '2025-09-22', 'nimblebrain-server.schema.json');

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

async function loadSchema() {
  try {
    const schemaContent = await readFile(SCHEMA_PATH, 'utf-8');
    return JSON.parse(schemaContent);
  } catch (error) {
    console.error(`${colors.red}❌ Failed to load schema from ${SCHEMA_PATH}${colors.reset}`);
    throw error;
  }
}

async function fetchExternalSchema(url: string) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    const schema = await response.json();
    return schema;
  } catch (error) {
    console.error(`${colors.yellow}⚠️  Failed to fetch external schema from ${url}${colors.reset}`);
    throw error;
  }
}

async function validateServers() {
  console.log(`${colors.blue}🔍 Validating server definitions...${colors.reset}\n`);

  // Load schema
  const schema = await loadSchema();

  // Initialize AJV with formats support and external schema loading
  const ajv = new Ajv({
    allErrors: true,
    verbose: true,
    strict: false, // Allow additional properties
    loadSchema: fetchExternalSchema // Function to load external schemas
  });
  addFormats(ajv);

  // Compile schema with async loading of external schemas
  let validate;
  try {
    validate = await ajv.compileAsync(schema);
  } catch (error) {
    console.error(`${colors.red}❌ Failed to compile schema:${colors.reset}`, error);
    process.exit(1);
  }

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

      const valid = validate(serverData);

      if (valid) {
        validServers++;
        console.log(`${colors.green}✅ ${dir.name}${colors.reset} - Valid`);
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