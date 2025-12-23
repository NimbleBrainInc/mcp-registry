#!/usr/bin/env tsx

/**
 * Bundle the NimbleTools server schema by resolving all $ref references
 *
 * This creates a self-contained schema that type generators can use directly
 * without needing to resolve HTTP references.
 */

import $RefParser from '@apidevtools/json-schema-ref-parser';
import { writeFile, mkdir } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SCHEMA_VERSION = '2025-12-11';
const SCHEMAS_DIR = join(__dirname, '..', 'schemas', SCHEMA_VERSION);

async function bundleSchema() {
  const inputPath = join(SCHEMAS_DIR, 'nimbletools-server.schema.json');
  const outputPath = join(SCHEMAS_DIR, 'nimbletools-server.bundled.schema.json');

  console.log(`📦 Bundling schema ${SCHEMA_VERSION}...`);
  console.log(`   Input:  ${inputPath}`);
  console.log(`   Output: ${outputPath}`);

  try {
    // Dereference all $ref pointers, resolving external HTTP references
    const bundled = await $RefParser.dereference(inputPath, {
      resolve: {
        http: {
          // Allow fetching external schemas over HTTP/HTTPS
          read: async (file) => {
            console.log(`   Fetching: ${file.url}`);
            const response = await fetch(file.url);
            if (!response.ok) {
              throw new Error(`Failed to fetch ${file.url}: ${response.status}`);
            }
            return await response.text();
          }
        }
      },
      dereference: {
        circular: 'ignore' // Handle circular references gracefully
      }
    });

    // Update the $id to reflect that this is the bundled version
    if (bundled.$id) {
      bundled.$id = bundled.$id.replace('.schema.json', '.bundled.schema.json');
    }

    // Add a note that this is auto-generated
    const output = {
      $comment: `AUTO-GENERATED: This is a bundled schema with all $refs resolved. Do not edit directly. Generated at ${new Date().toISOString()}`,
      ...bundled
    };

    // Write the bundled schema
    await writeFile(outputPath, JSON.stringify(output, null, 2));

    console.log(`\n✅ Bundled schema written to ${outputPath}`);

    // Show size comparison
    const { statSync } = await import('fs');
    const inputSize = statSync(inputPath).size;
    const outputSize = statSync(outputPath).size;
    console.log(`   Original: ${(inputSize / 1024).toFixed(1)} KB`);
    console.log(`   Bundled:  ${(outputSize / 1024).toFixed(1)} KB`);

  } catch (error) {
    console.error('❌ Failed to bundle schema:', error);
    process.exit(1);
  }
}

bundleSchema();
