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