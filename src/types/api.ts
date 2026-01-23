/**
 * Custom API types for NimbleTools MCP Registry
 * These are manually defined types specific to our API implementation
 */

import type { NimbleToolsMCPServer, NimbleToolsRuntime } from './generated.js';

// Extended server type with runtime additions
export interface MCPServerDetail extends NimbleToolsMCPServer {
  _meta?: {
    'ai.nimbletools.mcp/v1'?: NimbleToolsRuntime;
    'io.modelcontextprotocol.registry/official'?: RegistryMetadata;
  };
}

// API Response types specific to our implementation
export interface ServerListResponse {
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

// Registry metadata added at runtime
export interface RegistryMetadata {
  serverId: string;
  versionId: string;
  publishedAt: string;
  updatedAt: string;
  isLatest: boolean;
}

/**
 * Base fields shared by all skill reference types
 */
interface SkillReferenceBase {
  /** Skill artifact identifier (e.g., '@nimbletools/folk-crm') */
  name: string;
  /** Semver version (e.g., '1.0.0') */
  version: string;
  /** SHA256 integrity hash (format: 'sha256-hexdigest') */
  integrity?: string;
}

/**
 * Skill reference from mpak registry
 */
export interface MpakSkillReference extends SkillReferenceBase {
  source: 'mpak';
}

/**
 * Skill reference from GitHub repository
 */
export interface GithubSkillReference extends SkillReferenceBase {
  source: 'github';
  /** GitHub repository (owner/repo) */
  repo: string;
  /** Path to skill file in repo */
  path: string;
}

/**
 * Skill reference from direct URL
 */
export interface UrlSkillReference extends SkillReferenceBase {
  source: 'url';
  /** Direct download URL */
  url: string;
}

/**
 * Discriminated union of skill reference types
 * Used in server metadata to point to associated skill content
 */
export type SkillReference = MpakSkillReference | GithubSkillReference | UrlSkillReference;