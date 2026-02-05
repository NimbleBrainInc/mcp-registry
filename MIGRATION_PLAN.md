# Migration Plan: registry.nimbletools.ai → registry.nimblebrain.ai

## Overview

Migrate the MCP Registry from `registry.nimbletools.ai` to `registry.nimblebrain.ai` with a 301 redirect from the old domain to preserve backwards compatibility.

## Phase 1: Infrastructure (AWS)

### 1.1 Request ACM Certificate for New Domain

```bash
export AWS_PROFILE=nimblebrain

# Request certificate for registry.nimblebrain.ai
aws acm request-certificate \
  --region us-east-1 \
  --domain-name registry.nimblebrain.ai \
  --validation-method DNS \
  --query 'CertificateArn' --output text

# Also request for staging
aws acm request-certificate \
  --region us-east-1 \
  --domain-name registry.preview.nimblebrain.ai \
  --validation-method DNS \
  --query 'CertificateArn' --output text
```

Add DNS validation records to Route53, then wait:
```bash
aws acm wait certificate-validated --region us-east-1 --certificate-arn <ARN>
```

### 1.2 Deploy to New Domain

Update `k8s/production/values.yaml`:
```yaml
ingress:
  host: registry.nimblebrain.ai
  certificateArn: <NEW_CERT_ARN>
```

Update `k8s/staging/values.yaml`:
```yaml
ingress:
  host: registry.preview.nimblebrain.ai
  certificateArn: <NEW_STAGING_CERT_ARN>
```

Deploy:
```bash
make deploy ENV=production
```

ExternalDNS will automatically create DNS records for `registry.nimblebrain.ai`.

### 1.3 Set Up Redirect from Old Domain

**Architecture**: Route53 → CloudFront → S3 Website Redirect

This is slightly different from the standard redirect runbook because we're redirecting to a subdomain, not the root.

#### Create S3 Bucket with Redirect

```bash
DOMAIN="registry.nimbletools.ai"

# Create bucket
aws s3api create-bucket --bucket $DOMAIN --region us-east-1

# Configure website redirect to NEW domain
aws s3api put-bucket-website --bucket $DOMAIN --website-configuration '{
  "RedirectAllRequestsTo": {
    "HostName": "registry.nimblebrain.ai",
    "Protocol": "https"
  }
}'

# Disable public access block
aws s3api put-public-access-block --bucket $DOMAIN --public-access-block-configuration '{
  "BlockPublicAcls": false,
  "IgnorePublicAcls": false,
  "BlockPublicPolicy": false,
  "RestrictPublicBuckets": false
}'
```

#### Create CloudFront Distribution

Use existing ACM cert: `arn:aws:acm:us-east-1:533267450054:certificate/c266057e-f47e-40a3-921d-938a1837ea7c`

```bash
# Create distribution pointing to S3 website endpoint
# Origin: registry.nimbletools.ai.s3-website-us-east-1.amazonaws.com
# Alias: registry.nimbletools.ai
# Certificate: existing nimbletools.ai cert
```

#### Update DNS

Once the new registry is live at `registry.nimblebrain.ai`:
1. Remove the ExternalDNS-managed record for `registry.nimbletools.ai`
2. Point `registry.nimbletools.ai` to CloudFront distribution

---

## Phase 2: Code Updates

### 2.1 Schema Files (2 files)

| File | Change |
|------|--------|
| `schemas/2025-12-11/nimbletools-server.schema.json` | Update `$id` URL |
| `schemas/2025-12-11/nimbletools-server.bundled.schema.json` | Update `$id` URL |

**Before:**
```json
"$id": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json"
```

**After:**
```json
"$id": "https://registry.nimblebrain.ai/schemas/2025-12-11/nimbletools-server.schema.json"
```

### 2.2 Server Manifests (18 files)

All `servers/*/server.json` files need `$schema` updated:

| Server |
|--------|
| abstract |
| clickhouse |
| context7 |
| deepl |
| echo |
| exa |
| finnhub |
| folk |
| github |
| ipinfo |
| liblab |
| nationalparks-mcp |
| openweathermap |
| pdfco |
| postgres-mcp |
| ref-tools-mcp |
| reverse-text |
| tavily-mcp |

**Before:**
```json
"$schema": "https://registry.nimbletools.ai/schemas/2025-12-11/nimbletools-server.schema.json"
```

**After:**
```json
"$schema": "https://registry.nimblebrain.ai/schemas/2025-12-11/nimbletools-server.schema.json"
```

### 2.3 Source Code (1 file)

| File | Line | Change |
|------|------|--------|
| `src/server-factory.ts` | 124 | Update default API_URL |

**Before:**
```typescript
url: process.env.API_URL || 'https://registry.nimbletools.ai'
```

**After:**
```typescript
url: process.env.API_URL || 'https://registry.nimblebrain.ai'
```

### 2.4 Tests (1 file)

| File | Change |
|------|--------|
| `src/utils/validation.test.ts` | Update `$schema` in test fixtures (lines 45, 155) |

### 2.5 Documentation (5 files)

| File | Changes |
|------|---------|
| `README.md` | Multiple URLs (badge, API examples, table) |
| `CLAUDE.md` | Domain references in tables |
| `CONTRIBUTING.md` | Schema URL |
| `docs/ADDING_SERVERS.md` | Schema URLs (4 locations) |
| `docs/ENHANCED_METADATA.md` | Schema URLs (2 locations) |
| `docs/MCPB_SERVER_FORMAT.md` | Schema URLs (3 locations) |

### 2.6 Agent Configuration (1 file)

| File | Change |
|------|--------|
| `.claude/agents/mcp-server-creator.md` | Update schema URL in instructions |

### 2.7 Helm Values (2 files)

| File | Change |
|------|--------|
| `k8s/production/values.yaml` | `host` and `certificateArn` |
| `k8s/staging/values.yaml` | `host` and `certificateArn` |

### 2.8 Parent Repo Updates

| File | Change |
|------|--------|
| `/Users/mgolds02/Code/hq/CLAUDE.md` | Update domain table |

---

## Phase 3: Execution Order

### Step 1: Request Certificates (Day 1)
- [ ] Request ACM cert for `registry.nimblebrain.ai`
- [ ] Request ACM cert for `registry.preview.nimblebrain.ai`
- [ ] Add DNS validation records
- [ ] Wait for validation

### Step 2: Update Code (Day 1, after certs ready)
- [ ] Update all schema `$id` URLs
- [ ] Update all server.json `$schema` URLs
- [ ] Update source code default URL
- [ ] Update test fixtures
- [ ] Update documentation
- [ ] Update agent configuration
- [ ] Update Helm values with new hosts and cert ARNs
- [ ] Run `npm run validate-servers` to verify
- [ ] Run `npm run typecheck`

### Step 3: Deploy New Domain (Day 1)
- [ ] Deploy staging: `make deploy`
- [ ] Verify staging at `registry.preview.nimblebrain.ai`
- [ ] Deploy production: `make deploy ENV=production`
- [ ] Verify production at `registry.nimblebrain.ai`

### Step 4: Set Up Redirect (Day 2, after verification)
- [ ] Create S3 bucket `registry.nimbletools.ai` with redirect
- [ ] Create CloudFront distribution
- [ ] Update Route53 to point old domain to CloudFront
- [ ] Verify redirect works

### Step 5: Update Parent Repo
- [ ] Update `hq/CLAUDE.md` domain table
- [ ] Commit submodule update in hq

---

## Summary

| Category | File Count |
|----------|------------|
| Schema definitions | 2 |
| Server manifests | 18 |
| Source code | 1 |
| Tests | 1 |
| Documentation | 6 |
| Agent config | 1 |
| Helm values | 2 |
| Parent repo | 1 |
| **Total** | **32 files** |

## Rollback Plan

If issues arise:
1. Update Helm values back to `registry.nimbletools.ai`
2. Deploy: `make deploy ENV=production`
3. Revert code changes
4. Remove CloudFront distribution and S3 bucket

The redirect infrastructure can remain in place (it's harmless) until the migration is successfully completed.
