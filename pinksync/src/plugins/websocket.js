import fp from 'fastify-plugin';

/**
 * WebSocket plugin for real-time collaboration
 * @param {import('fastify').FastifyInstance} fastify
 */
async function websocketPlugin(fastify) {
  const clients = new Map();

  // WebSocket connection handler
  fastify.get('/ws', { websocket: true }, (connection, request) => {
    const clientId = Date.now().toString();
    clients.set(clientId, connection);

    fastify.log.info(`Client connected: ${clientId}`);

    // Send welcome message
    connection.socket.send(JSON.stringify({
      type: 'connected',
      clientId,
      message: 'Connected to PinkSync',
    }));

    // Handle incoming messages
    connection.socket.on('message', (message) => {
      try {
        const data = JSON.parse(message.toString());
        fastify.log.info(`Message from ${clientId}:`, data);

        // Handle different message types
        switch (data.type) {
          case 'ping':
            connection.socket.send(JSON.stringify({
              type: 'pong',
              timestamp: Date.now(),
            }));
            break;

          case 'broadcast':
            // Broadcast to all other clients
            broadcast(data.payload, clientId);
            break;

          case 'file-edit':
            // Handle file editing events
            broadcast({
              type: 'file-changed',
              path: data.path,
              userId: clientId,
              timestamp: Date.now(),
            }, clientId);
            break;

          case 'presence':
            // Handle presence updates
            broadcast({
              type: 'user-presence',
              userId: clientId,
              status: data.status,
              timestamp: Date.now(),
            }, clientId);
            break;

          default:
            connection.socket.send(JSON.stringify({
              type: 'error',
              message: 'Unknown message type',
            }));
        }
      } catch (error) {
        fastify.log.error('WebSocket message error:', error);
        connection.socket.send(JSON.stringify({
          type: 'error',
          message: 'Invalid message format',
        }));
      }
    });

    // Handle disconnection
    connection.socket.on('close', () => {
      clients.delete(clientId);
      fastify.log.info(`Client disconnected: ${clientId}`);

      // Notify others about disconnection
      broadcast({
        type: 'user-disconnected',
        userId: clientId,
        timestamp: Date.now(),
      }, clientId);
    });

    // Handle errors
    connection.socket.on('error', (error) => {
      fastify.log.error(`WebSocket error for ${clientId}:`, error);
      clients.delete(clientId);
    });
  });

  // Broadcast function
  function broadcast(data, excludeClientId = null) {
    const message = JSON.stringify(data);
    clients.forEach((connection, clientId) => {
      if (clientId !== excludeClientId) {
        try {
          connection.socket.send(message);
        } catch (error) {
          fastify.log.error(`Failed to send to ${clientId}:`, error);
          clients.delete(clientId);
        }
      }
    });
  }

  // Add broadcast function to fastify instance
  fastify.decorate('broadcast', broadcast);

  // Add function to get connected clients count
  fastify.decorate('getConnectedClientsCount', () => clients.size);
}

export default fp(websocketPlugin, {
  name: 'websocket-plugin',
  dependencies: ['@fastify/websocket'],
});
