#!/usr/bin/env tsx

/**
 * Migrate all server.json files from 2025-09-22 to 2025-12-11 schema format.
 *
 * Changes:
 * - Update $schema URL
 * - Add top-level `title` from `_meta.display.name`
 * - Add top-level `icons[]` from `_meta.display.branding.iconUrl/logoUrl`
 * - Move `status` to `_meta.ai.nimbletools.mcp/v1.status`
 * - Move `repository.branch` to `_meta.ai.nimbletools.mcp/v1.repository.branch`
 * - Rename `example` to `placeholder` in environmentVariables
 * - Remove migrated fields from _meta.display
 */

import { readdir, readFile, writeFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SERVERS_DIR = join(__dirname, '..', 'servers');
const NEW_SCHEMA = 'https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json';

interface Icon {
  src: string;
  sizes?: string[];
}

interface ServerJson {
  $schema: string;
  name: string;
  version: string;
  title?: string;
  description: string;
  status?: string;
  icons?: Icon[];
  repository?: {
    url: string;
    source: string;
    branch?: string;
  };
  websiteUrl?: string;
  packages?: any[];
  _meta?: {
    'ai.nimbletools.mcp/v1'?: any;
  };
}

function migrateServer(server: ServerJson): ServerJson {
  const nimbletools = server._meta?.['ai.nimbletools.mcp/v1'] || {};
  const display = nimbletools.display || {};
  const branding = display.branding || {};

  // Build the new server object with correct field ordering
  const migrated: any = {
    $schema: NEW_SCHEMA,
    name: server.name,
    version: server.version,
  };

  // Add title from _meta.display.name
  if (display.name) {
    migrated.title = display.name;
  }

  // Add description
  migrated.description = server.description;

  // Build icons array from branding URLs
  const icons: Icon[] = [];
  if (branding.iconUrl) {
    icons.push({ src: branding.iconUrl, sizes: ['64x64'] });
  }
  if (branding.logoUrl) {
    icons.push({ src: branding.logoUrl, sizes: ['256x256'] });
  }
  if (icons.length > 0) {
    migrated.icons = icons;
  }

  // Add repository (without branch at top level)
  if (server.repository) {
    migrated.repository = {
      url: server.repository.url,
      source: server.repository.source,
    };
  }

  // Add websiteUrl
  if (server.websiteUrl) {
    migrated.websiteUrl = server.websiteUrl;
  }

  // Migrate packages (rename example -> placeholder in environmentVariables)
  if (server.packages) {
    migrated.packages = server.packages.map(pkg => {
      const newPkg = { ...pkg };
      if (newPkg.environmentVariables) {
        newPkg.environmentVariables = newPkg.environmentVariables.map((envVar: any) => {
          const newEnvVar = { ...envVar };
          if ('example' in newEnvVar) {
            newEnvVar.placeholder = newEnvVar.example;
            delete newEnvVar.example;
          }
          return newEnvVar;
        });
      }
      return newPkg;
    });
  }

  // Build new _meta with restructured nimbletools extension
  const newNimbletools: any = {};

  // Move status from top-level to extension
  if (server.status) {
    newNimbletools.status = server.status;
  }

  // Move repository.branch to extension
  if (server.repository?.branch) {
    newNimbletools.repository = { branch: server.repository.branch };
  }

  // Copy over existing extension fields (container, resources, scaling, etc.)
  const extensionFields = [
    'container', 'resources', 'scaling', 'observability',
    'security', 'networking', 'deployment', 'capabilities'
  ];
  for (const field of extensionFields) {
    if (nimbletools[field] !== undefined) {
      newNimbletools[field] = nimbletools[field];
    }
  }

  // Build new display object (without name, iconUrl, logoUrl which moved to core)
  const newDisplay: any = {};
  if (display.category) newDisplay.category = display.category;
  if (display.tags) newDisplay.tags = display.tags;

  // Keep branding but only colors (iconUrl/logoUrl moved to icons[])
  if (branding.primaryColor || branding.accentColor) {
    newDisplay.branding = {};
    if (branding.primaryColor) newDisplay.branding.primaryColor = branding.primaryColor;
    if (branding.accentColor) newDisplay.branding.accentColor = branding.accentColor;
  }

  if (display.documentation) newDisplay.documentation = display.documentation;
  if (display.showcase) newDisplay.showcase = display.showcase;

  if (Object.keys(newDisplay).length > 0) {
    newNimbletools.display = newDisplay;
  }

  // Add _meta if we have any nimbletools data
  if (Object.keys(newNimbletools).length > 0) {
    migrated._meta = {
      'ai.nimbletools.mcp/v1': newNimbletools
    };
  }

  return migrated;
}

async function main() {
  console.log('🔄 Migrating servers to 2025-12-11 schema...\n');

  const entries = await readdir(SERVERS_DIR, { withFileTypes: true });
  const serverDirs = entries.filter(entry => entry.isDirectory());

  let migrated = 0;
  let skipped = 0;
  let errors = 0;

  for (const dir of serverDirs) {
    const serverJsonPath = join(SERVERS_DIR, dir.name, 'server.json');

    try {
      const content = await readFile(serverJsonPath, 'utf-8');
      const server = JSON.parse(content) as ServerJson;

      // Check if already migrated
      if (server.$schema.includes('2025-12-11')) {
        console.log(`⏭️  ${dir.name} - Already on 2025-12-11, skipping`);
        skipped++;
        continue;
      }

      // Migrate
      const migratedServer = migrateServer(server);

      // Write back with nice formatting
      await writeFile(serverJsonPath, JSON.stringify(migratedServer, null, 2) + '\n');

      console.log(`✅ ${dir.name} - Migrated`);
      migrated++;
    } catch (error: any) {
      console.error(`❌ ${dir.name} - Error: ${error.message}`);
      errors++;
    }
  }

  console.log('\n═══════════════════════════════');
  console.log('📊 Migration Summary');
  console.log('═══════════════════════════════');
  console.log(`Migrated: ${migrated}`);
  console.log(`Skipped:  ${skipped}`);
  console.log(`Errors:   ${errors}`);

  if (errors > 0) {
    process.exit(1);
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
