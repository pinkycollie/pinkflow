import { successResponse, errorResponse } from '../utils/responses.js';

/**
 * Authentication routes
 * @param {import('fastify').FastifyInstance} fastify
 */
export default async function authRoutes(fastify) {
  // Login endpoint
  fastify.post('/login', {
    schema: {
      description: 'User login with DeafAuth/FibonRose/GitHub OAuth',
      tags: ['Authentication'],
      body: {
        type: 'object',
        required: ['email', 'password'],
        properties: {
          email: { type: 'string', format: 'email' },
          password: { type: 'string', minLength: 6 },
        },
      },
      response: {
        200: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            message: { type: 'string' },
            data: {
              type: 'object',
              properties: {
                token: { type: 'string' },
                user: {
                  type: 'object',
                  properties: {
                    id: { type: 'string' },
                    email: { type: 'string' },
                    role: { type: 'string' },
                    fibonRoseProfile: {
                      type: 'object',
                      properties: {
                        trustScore: { type: 'number' },
                        vouches: { type: 'number' },
                      },
                    },
                  },
                },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { email, password } = request.body;

    // TODO: Implement actual authentication with DeafAuth/Supabase
    // This is a mock implementation
    const mockUser = {
      id: 'user-123',
      email,
      role: 'developer',
      fibonRoseProfile: {
        trustScore: 85,
        vouches: 12,
      },
    };

    const mockToken = 'mock-jwt-token-' + Date.now();

    return reply.send(successResponse({
      token: mockToken,
      user: mockUser,
    }, 'Login successful'));
  });

  // Logout endpoint
  fastify.post('/logout', {
    schema: {
      description: 'Invalidate user session',
      tags: ['Authentication'],
      response: {
        200: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            message: { type: 'string' },
          },
        },
      },
    },
  }, async (request, reply) => {
    // TODO: Implement token invalidation
    return reply.send(successResponse(null, 'Logout successful'));
  });

  // Get current user
  fastify.get('/user', {
    schema: {
      description: 'Get current user profile',
      tags: ['Authentication'],
      response: {
        200: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            message: { type: 'string' },
            data: {
              type: 'object',
              properties: {
                id: { type: 'string' },
                email: { type: 'string' },
                role: { type: 'string' },
                fibonRoseProfile: { type: 'object' },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    // TODO: Get user from JWT token
    const mockUser = {
      id: 'user-123',
      email: 'user@example.com',
      role: 'developer',
      fibonRoseProfile: {
        trustScore: 85,
        vouches: 12,
      },
    };

    return reply.send(successResponse(mockUser));
  });

  // Sync user profile
  fastify.post('/user/profile/sync', {
    schema: {
      description: 'Sync/update FibonRose trust profile',
      tags: ['Authentication'],
      body: {
        type: 'object',
        properties: {
          trustScore: { type: 'number' },
          vouches: { type: 'number' },
        },
      },
      response: {
        200: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            message: { type: 'string' },
            data: { type: 'object' },
          },
        },
      },
    },
  }, async (request, reply) => {
    const profileUpdate = request.body;

    // TODO: Sync with FibonRose service
    return reply.send(successResponse(profileUpdate, 'Profile synced successfully'));
  });
}
