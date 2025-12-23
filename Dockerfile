FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci

# Copy source files and scripts
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY schemas/ ./schemas/

# Build TypeScript (types generated via prebuild)
RUN npm run build

# Production stage
FROM node:22-alpine

WORKDIR /app

# Copy package files and install production dependencies only
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

# Copy built application and server definitions
COPY --from=builder /app/dist ./dist
COPY servers/ ./servers/
COPY schemas/ ./schemas/

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

USER nodejs

# Set production environment
ENV NODE_ENV=production

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "fetch('http://localhost:8080/v0.1/health').then(r => process.exit(r.ok ? 0 : 1))" || exit 1

# Run the server
CMD ["node", "dist/server.js"]