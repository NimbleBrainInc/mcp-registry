/**
 * README Fetcher Module
 * Fetches and caches README content from GitHub repositories
 */

import { readFile, writeFile, mkdir } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

const CACHE_DIR = join(process.cwd(), '.cache', 'readmes');
const CACHE_TTL = 3600000; // 1 hour
const GITHUB_API_BASE = 'https://api.github.com';
const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com';

interface CachedReadme {
  content: string;
  fetchedAt: number;
  etag?: string;
}

interface GitHubFile {
  name: string;
  type: string;
  download_url: string;
}

/**
 * Extract owner and repo from GitHub URL
 */
function parseGitHubUrl(url: string): { owner: string; repo: string; branch: string } | null {
  const patterns = [
    /github\.com\/([^\/]+)\/([^\/]+)(?:\/tree\/([^\/]+))?/,
    /github\.com\/([^\/]+)\/([^\/]+)\.git/
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) {
      return {
        owner: match[1],
        repo: match[2].replace('.git', ''),
        branch: match[3] || 'main'
      };
    }
  }

  return null;
}

/**
 * Get cache file path for a repository
 */
function getCachePath(owner: string, repo: string): string {
  return join(CACHE_DIR, `${owner}-${repo}.json`);
}

/**
 * Load cached README if available and not expired
 */
async function loadFromCache(owner: string, repo: string): Promise<CachedReadme | null> {
  try {
    const cachePath = getCachePath(owner, repo);
    if (!existsSync(cachePath)) return null;

    const cached = JSON.parse(await readFile(cachePath, 'utf-8')) as CachedReadme;

    // Check if cache is still valid
    if (Date.now() - cached.fetchedAt < CACHE_TTL) {
      return cached;
    }
  } catch (error) {
    console.error(`Cache read error for ${owner}/${repo}:`, error);
  }

  return null;
}

/**
 * Save README content to cache
 */
async function saveToCache(
  owner: string,
  repo: string,
  content: string,
  etag?: string
): Promise<void> {
  try {
    // Ensure cache directory exists
    if (!existsSync(CACHE_DIR)) {
      await mkdir(CACHE_DIR, { recursive: true });
    }

    const cachePath = getCachePath(owner, repo);
    const cacheData: CachedReadme = {
      content,
      fetchedAt: Date.now(),
      etag
    };

    await writeFile(cachePath, JSON.stringify(cacheData, null, 2));
  } catch (error) {
    console.error(`Cache write error for ${owner}/${repo}:`, error);
  }
}

/**
 * Find README file in repository
 */
async function findReadmeFile(
  owner: string,
  repo: string,
  branch: string = 'main'
): Promise<string | null> {
  const readmeNames = [
    'README.md',
    'readme.md',
    'Readme.md',
    'README.MD',
    'README.markdown',
    'README.rst',
    'README.txt',
    'README'
  ];

  try {
    // Try GitHub API first (rate-limited but reliable)
    const apiUrl = `${GITHUB_API_BASE}/repos/${owner}/${repo}/contents`;
    const headers: Record<string, string> = {
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'NimbleBrain-MCP-Registry'
    };

    // Add GitHub token if available
    if (process.env.GITHUB_TOKEN) {
      headers['Authorization'] = `token ${process.env.GITHUB_TOKEN}`;
    }

    const response = await fetch(apiUrl, { headers });

    if (response.ok) {
      const files = await response.json() as GitHubFile[];

      for (const readmeName of readmeNames) {
        const file = files.find(f => f.name === readmeName && f.type === 'file');
        if (file?.download_url) {
          return file.download_url;
        }
      }
    }

    // Fallback to direct raw URL attempts
    for (const readmeName of readmeNames) {
      const rawUrl = `${GITHUB_RAW_BASE}/${owner}/${repo}/${branch}/${readmeName}`;
      const checkResponse = await fetch(rawUrl, { method: 'HEAD' });

      if (checkResponse.ok) {
        return rawUrl;
      }
    }
  } catch (error) {
    console.error(`Error finding README for ${owner}/${repo}:`, error);
  }

  return null;
}

/**
 * Fetch README content from GitHub
 */
async function fetchReadmeFromGitHub(
  owner: string,
  repo: string,
  branch: string = 'main'
): Promise<string | null> {
  try {
    const readmeUrl = await findReadmeFile(owner, repo, branch);

    if (!readmeUrl) {
      console.warn(`No README found for ${owner}/${repo}`);
      return null;
    }

    const response = await fetch(readmeUrl);

    if (!response.ok) {
      console.error(`Failed to fetch README from ${readmeUrl}: ${response.status}`);
      return null;
    }

    const content = await response.text();
    const etag = response.headers.get('etag') || undefined;

    // Save to cache
    await saveToCache(owner, repo, content, etag);

    return content;
  } catch (error) {
    console.error(`Error fetching README for ${owner}/${repo}:`, error);
    return null;
  }
}

/**
 * Main function to get README content
 */
export async function getReadmeContent(
  repositoryUrl?: string,
  readmeUrl?: string
): Promise<string | null> {
  // If explicit README URL is provided, fetch directly
  if (readmeUrl) {
    try {
      const response = await fetch(readmeUrl);
      if (response.ok) {
        return await response.text();
      }
    } catch (error) {
      console.error(`Failed to fetch README from ${readmeUrl}:`, error);
    }
  }

  // Try to fetch from repository URL
  if (repositoryUrl) {
    const parsed = parseGitHubUrl(repositoryUrl);

    if (parsed) {
      // Check cache first
      const cached = await loadFromCache(parsed.owner, parsed.repo);
      if (cached) {
        return cached.content;
      }

      // Fetch from GitHub
      return await fetchReadmeFromGitHub(parsed.owner, parsed.repo, parsed.branch);
    }
  }

  return null;
}

/**
 * Process README content for safe rendering
 */
export function sanitizeReadme(content: string): string {
  // Remove any potentially dangerous HTML/scripts
  // This is a basic sanitization - consider using a proper markdown sanitizer
  return content
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/<embed\b[^>]*>/gi, '')
    .replace(/<object\b[^<]*(?:(?!<\/object>)<[^<]*)*<\/object>/gi, '');
}

/**
 * Clear cache for a specific repository or all
 */
export async function clearReadmeCache(owner?: string, repo?: string): Promise<void> {
  if (owner && repo) {
    const cachePath = getCachePath(owner, repo);
    if (existsSync(cachePath)) {
      await writeFile(cachePath, '{}');
    }
  } else if (existsSync(CACHE_DIR)) {
    // Clear all cache
    await mkdir(CACHE_DIR, { recursive: true });
  }
}