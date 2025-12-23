/**
 * NimbleTools MCP Registry API Server
 * Main entry point for production
 */

import 'dotenv/config';
import { createServer } from './server-factory.js';

const PORT = parseInt(process.env.PORT || '8080', 10);
const HOST = process.env.HOST || '0.0.0.0';

async function start() {
  try {
    const fastify = await createServer();

    await fastify.listen({ port: PORT, host: HOST });

    console.log(`
🚀 NimbleTools MCP Registry API is running!

   API:     http://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT}
   Docs:    http://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT}/docs
   Health:  http://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT}/v0.1/health
    `);
  } catch (err) {
    console.error('Failed to start server:', err);
    process.exit(1);
  }
}

start();