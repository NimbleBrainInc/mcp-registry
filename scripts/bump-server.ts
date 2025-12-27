#!/usr/bin/env npx tsx
/**
 * Bump a server version in the registry by fetching SHA256 hashes from GitHub releases.
 *
 * Usage:
 *   npx tsx scripts/bump-server.ts <server-name> <version>
 *
 * Example:
 *   npx tsx scripts/bump-server.ts ipinfo 1.0.2
 *
 * This will:
 *   1. Fetch the release from GitHub (e.g., NimbleBrainInc/mcp-ipinfo v1.0.2)
 *   2. Download SHA256 hashes from the release assets
 *   3. Update servers/<server-name>/server.json with new version and hashes
 */

import { readFileSync, writeFileSync, existsSync } from "fs";
import { join } from "path";

interface ServerJson {
  version: string;
  repository: {
    url: string;
  };
  packages: Array<{
    version: string;
    sha256?: Record<string, string>;
    [key: string]: unknown;
  }>;
  [key: string]: unknown;
}

interface GitHubRelease {
  tag_name: string;
  assets: Array<{
    name: string;
    browser_download_url: string;
  }>;
}

async function fetchRelease(
  owner: string,
  repo: string,
  version: string
): Promise<GitHubRelease> {
  const tag = version.startsWith("v") ? version : `v${version}`;
  const url = `https://api.github.com/repos/${owner}/${repo}/releases/tags/${tag}`;

  const response = await fetch(url, {
    headers: {
      Accept: "application/vnd.github.v3+json",
      "User-Agent": "nimbletools-registry",
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch release: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

async function fetchSha256FromRelease(release: GitHubRelease): Promise<Record<string, string>> {
  const sha256Asset = release.assets.find((a) => a.name === "sha256sums.txt");

  if (!sha256Asset) {
    throw new Error(
      "No sha256sums.txt found in release assets. Available assets: " +
        release.assets.map((a) => a.name).join(", ")
    );
  }

  const response = await fetch(sha256Asset.browser_download_url);
  if (!response.ok) {
    throw new Error(`Failed to fetch sha256sums.txt: ${response.status}`);
  }

  const content = await response.text();
  const hashes: Record<string, string> = {};

  // Parse sha256sums.txt format: "<hash>  <filename>"
  for (const line of content.trim().split("\n")) {
    const match = line.match(/^([a-f0-9]{64})\s+(.+)$/);
    if (match) {
      const [, hash, filename] = match;
      // Extract architecture from filename like "mcp-ipinfo-v1.0.1-linux-amd64.mcpb"
      const archMatch = filename.match(/linux-(amd64|arm64)/);
      if (archMatch) {
        hashes[`linux-${archMatch[1]}`] = hash;
      }
    }
  }

  if (Object.keys(hashes).length === 0) {
    throw new Error(`No valid hashes found in sha256sums.txt:\n${content}`);
  }

  return hashes;
}

function parseGitHubUrl(url: string): { owner: string; repo: string } {
  const match = url.match(/github\.com\/([^/]+)\/([^/]+)/);
  if (!match) {
    throw new Error(`Invalid GitHub URL: ${url}`);
  }
  return { owner: match[1], repo: match[2].replace(/\.git$/, "") };
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error("Usage: npx tsx scripts/bump-server.ts <server-name> <version>");
    console.error("Example: npx tsx scripts/bump-server.ts ipinfo 1.0.2");
    process.exit(1);
  }

  const [serverName, version] = args;
  const serverDir = join(process.cwd(), "servers", serverName);
  const serverJsonPath = join(serverDir, "server.json");

  if (!existsSync(serverJsonPath)) {
    console.error(`Server not found: ${serverJsonPath}`);
    process.exit(1);
  }

  console.log(`Bumping ${serverName} to version ${version}...`);

  // Read current server.json
  const serverJson: ServerJson = JSON.parse(readFileSync(serverJsonPath, "utf-8"));

  // Parse GitHub URL to get owner/repo
  const { owner, repo } = parseGitHubUrl(serverJson.repository.url);
  console.log(`Fetching release from ${owner}/${repo}...`);

  // Fetch release from GitHub
  const release = await fetchRelease(owner, repo, version);
  console.log(`Found release: ${release.tag_name}`);

  // Fetch SHA256 hashes
  console.log("Fetching SHA256 hashes...");
  const hashes = await fetchSha256FromRelease(release);
  console.log(`Found hashes for: ${Object.keys(hashes).join(", ")}`);

  // Update server.json
  const cleanVersion = version.replace(/^v/, "");
  serverJson.version = cleanVersion;

  if (serverJson.packages && serverJson.packages.length > 0) {
    serverJson.packages[0].version = cleanVersion;
    serverJson.packages[0].sha256 = hashes;
  }

  // Write updated server.json
  writeFileSync(serverJsonPath, JSON.stringify(serverJson, null, 2) + "\n");

  console.log(`\nUpdated ${serverJsonPath}:`);
  console.log(`  version: ${cleanVersion}`);
  console.log(`  sha256:`);
  for (const [arch, hash] of Object.entries(hashes)) {
    console.log(`    ${arch}: ${hash}`);
  }

  console.log("\nDone! Review the changes and commit when ready.");
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
