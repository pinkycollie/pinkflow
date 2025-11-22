import { successResponse, errorResponse, paginateResponse } from '../utils/responses.js';

/**
 * Governance and curation routes
 * @param {import('fastify').FastifyInstance} fastify
 */
export default async function governanceRoutes(fastify) {
  // Get active ballots
  fastify.get('/ballots', {
    schema: {
      description: 'List all active governance proposals',
      tags: ['Governance'],
      querystring: {
        type: 'object',
        properties: {
          page: { type: 'integer', minimum: 1, default: 1 },
          perPage: { type: 'integer', minimum: 1, maximum: 100, default: 20 },
          status: { type: 'string', enum: ['active', 'closed', 'pending'] },
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
                items: {
                  type: 'array',
                  items: {
                    type: 'object',
                    properties: {
                      id: { type: 'string' },
                      title: { type: 'string' },
                      description: { type: 'string' },
                      status: { type: 'string' },
                      createdBy: { type: 'string' },
                      votes: {
                        type: 'object',
                        properties: {
                          for: { type: 'integer' },
                          against: { type: 'integer' },
                        },
                      },
                      createdAt: { type: 'string' },
                    },
                  },
                },
                pagination: {
                  type: 'object',
                  properties: {
                    page: { type: 'integer' },
                    perPage: { type: 'integer' },
                    total: { type: 'integer' },
                    totalPages: { type: 'integer' },
                  },
                },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { page = 1, perPage = 20, status } = request.query;

    // Mock ballots data
    const mockBallots = [
      {
        id: 'ballot-1',
        title: 'Add new feature to IDE',
        description: 'Proposal to add real-time collaboration feature',
        status: 'active',
        createdBy: 'user-123',
        votes: { for: 45, against: 12 },
        createdAt: new Date().toISOString(),
      },
      {
        id: 'ballot-2',
        title: 'Update governance rules',
        description: 'Proposal to modify voting threshold',
        status: 'active',
        createdBy: 'user-456',
        votes: { for: 30, against: 25 },
        createdAt: new Date().toISOString(),
      },
    ];

    const total = mockBallots.length;
    const paginatedData = paginateResponse(mockBallots, page, perPage, total);

    return reply.send(successResponse(paginatedData));
  });

  // Vouch for a ballot
  fastify.post('/ballots/:id/vouch', {
    schema: {
      description: 'Vouch for a proposal with trust validation',
      tags: ['Governance'],
      params: {
        type: 'object',
        properties: {
          id: { type: 'string' },
        },
      },
      body: {
        type: 'object',
        required: ['vote'],
        properties: {
          vote: { type: 'string', enum: ['for', 'against'] },
          comment: { type: 'string' },
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
                vouchId: { type: 'string' },
                trustScoreApplied: { type: 'number' },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { id } = request.params;
    const { vote, comment } = request.body;

    // TODO: Validate trust score with FibonRose
    // TODO: Record vouch in database
    const mockResponse = {
      vouchId: 'vouch-' + Date.now(),
      trustScoreApplied: 85,
    };

    return reply.send(successResponse(mockResponse, 'Vouch recorded successfully'));
  });

  // Get approved contributions
  fastify.get('/contributions/approved', {
    schema: {
      description: 'List approved contributions',
      tags: ['Governance'],
      querystring: {
        type: 'object',
        properties: {
          page: { type: 'integer', minimum: 1, default: 1 },
          perPage: { type: 'integer', minimum: 1, maximum: 100, default: 20 },
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
                items: {
                  type: 'array',
                  items: {
                    type: 'object',
                    properties: {
                      id: { type: 'string' },
                      title: { type: 'string' },
                      contributor: { type: 'string' },
                      type: { type: 'string' },
                      approvedAt: { type: 'string' },
                    },
                  },
                },
                pagination: { type: 'object' },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { page = 1, perPage = 20 } = request.query;

    // Mock contributions data
    const mockContributions = [
      {
        id: 'contrib-1',
        title: 'Fix authentication bug',
        contributor: 'user-789',
        type: 'bugfix',
        approvedAt: new Date().toISOString(),
      },
      {
        id: 'contrib-2',
        title: 'Add documentation',
        contributor: 'user-456',
        type: 'documentation',
        approvedAt: new Date().toISOString(),
      },
    ];

    const total = mockContributions.length;
    const paginatedData = paginateResponse(mockContributions, page, perPage, total);

    return reply.send(successResponse(paginatedData));
  });
}
