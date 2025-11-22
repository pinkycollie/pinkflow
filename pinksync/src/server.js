import Fastify from 'fastify';
import cors from '@fastify/cors';
import swagger from '@fastify/swagger';
import swaggerUI from '@fastify/swagger-ui';
import websocket from '@fastify/websocket';
import { pathToFileURL } from 'url';
import config from './config/index.js';
import websocketPlugin from './plugins/websocket.js';
import authRoutes from './routes/auth.js';
import workspaceRoutes from './routes/workspace.js';
import governanceRoutes from './routes/governance.js';
import aiRoutes from './routes/ai.js';

/**
 * Build Fastify application
 */
export async function buildApp(opts = {}) {
  const fastify = Fastify({
    logger: {
      level: config.logging.level,
      transport: config.server.env === 'development' ? {
        target: 'pino-pretty',
        options: {
          translateTime: 'HH:MM:ss Z',
          ignore: 'pid,hostname',
        },
      } : undefined,
    },
    ...opts,
  });

  // Register CORS
  await fastify.register(cors, {
    origin: config.cors.origin,
    credentials: true,
  });

  // Register WebSocket support
  await fastify.register(websocket);

  // Register Swagger for API documentation
  await fastify.register(swagger, {
    openapi: {
      openapi: '3.0.0',
      info: {
        title: 'PinkSync API',
        description: 'Real-time synchronization and WebSocket service for PinkFlow ecosystem',
        version: '1.0.0',
      },
      servers: [
        {
          url: `http://${config.server.host}:${config.server.port}`,
          description: 'Development server',
        },
      ],
      tags: [
        { name: 'Authentication', description: 'User authentication endpoints' },
        { name: 'Workspace', description: 'File system and workspace operations' },
        { name: 'Governance', description: 'Governance and voting endpoints' },
        { name: 'AI', description: 'AI proxy endpoints for Gemini API' },
      ],
    },
  });

  // Register Swagger UI
  await fastify.register(swaggerUI, {
    routePrefix: '/docs',
    uiConfig: {
      docExpansion: 'list',
      deepLinking: false,
    },
    staticCSP: true,
    transformStaticCSP: (header) => header,
  });

  // Health check endpoint
  fastify.get('/', async (request, reply) => {
    return {
      status: 'ok',
      service: 'PinkSync',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      websocketClients: fastify.getConnectedClientsCount ? fastify.getConnectedClientsCount() : 0,
    };
  });

  // Health check endpoint
  fastify.get('/health', async (request, reply) => {
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
    };
  });

  // Register WebSocket plugin
  await fastify.register(websocketPlugin);

  // Register API routes
  await fastify.register(authRoutes, { prefix: '/api/auth' });
  await fastify.register(workspaceRoutes, { prefix: '/api/workspace' });
  await fastify.register(governanceRoutes, { prefix: '/api/governance' });
  await fastify.register(aiRoutes, { prefix: '/api/ai' });

  // Error handler
  fastify.setErrorHandler((error, request, reply) => {
    fastify.log.error(error);
    reply.status(error.statusCode || 500).send({
      success: false,
      message: error.message || 'Internal Server Error',
      statusCode: error.statusCode || 500,
    });
  });

  return fastify;
}

/**
 * Start the server
 */
async function start() {
  try {
    const fastify = await buildApp();

    await fastify.listen({
      port: config.server.port,
      host: config.server.host,
    });

    fastify.log.info(`Server listening on http://${config.server.host}:${config.server.port}`);
    fastify.log.info(`API documentation available at http://${config.server.host}:${config.server.port}/docs`);
  } catch (err) {
    console.error('Error starting server:', err);
    process.exit(1);
  }
}

// Start server if this file is run directly
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  start();
}

export default start;
