import { successResponse, errorResponse } from '../utils/responses.js';

/**
 * Workspace routes for file system operations
 * @param {import('fastify').FastifyInstance} fastify
 */
export default async function workspaceRoutes(fastify) {
  // Get file tree
  fastify.get('/tree', {
    schema: {
      description: 'Get workspace file tree structure',
      tags: ['Workspace'],
      response: {
        200: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            message: { type: 'string' },
            data: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  id: { type: 'string' },
                  name: { type: 'string' },
                  path: { type: 'string' },
                  type: { type: 'string', enum: ['file', 'directory'] },
                  children: { type: 'array' },
                },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    // Mock file tree
    const mockTree = [
      {
        id: '1',
        name: 'src',
        path: '/src',
        type: 'directory',
        children: [
          {
            id: '2',
            name: 'index.js',
            path: '/src/index.js',
            type: 'file',
          },
          {
            id: '3',
            name: 'utils.js',
            path: '/src/utils.js',
            type: 'file',
          },
        ],
      },
      {
        id: '4',
        name: 'README.md',
        path: '/README.md',
        type: 'file',
      },
    ];

    return reply.send(successResponse(mockTree));
  });

  // Get file content
  fastify.get('/file', {
    schema: {
      description: 'Get file content by path',
      tags: ['Workspace'],
      querystring: {
        type: 'object',
        required: ['path'],
        properties: {
          path: { type: 'string' },
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
                path: { type: 'string' },
                content: { type: 'string' },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { path } = request.query;

    // TODO: Implement actual file reading
    const mockContent = {
      path,
      content: '// File content for: ' + path,
    };

    return reply.send(successResponse(mockContent));
  });

  // Update file content
  fastify.put('/file', {
    schema: {
      description: 'Update file content',
      tags: ['Workspace'],
      querystring: {
        type: 'object',
        required: ['path'],
        properties: {
          path: { type: 'string' },
        },
      },
      body: {
        type: 'object',
        required: ['content'],
        properties: {
          content: { type: 'string' },
        },
      },
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
    const { path } = request.query;
    const { content } = request.body;

    // TODO: Implement actual file writing
    return reply.send(successResponse(null, 'File updated successfully'));
  });

  // Create new file
  fastify.post('/file', {
    schema: {
      description: 'Create a new file',
      tags: ['Workspace'],
      body: {
        type: 'object',
        required: ['path', 'content'],
        properties: {
          path: { type: 'string' },
          content: { type: 'string' },
        },
      },
      response: {
        201: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            message: { type: 'string' },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { path, content } = request.body;

    // TODO: Implement actual file creation
    return reply.code(201).send(successResponse(null, 'File created successfully'));
  });

  // Commit changes
  fastify.post('/commit', {
    schema: {
      description: 'Commit staged files (Git integration)',
      tags: ['Workspace'],
      body: {
        type: 'object',
        required: ['message'],
        properties: {
          message: { type: 'string' },
          files: {
            type: 'array',
            items: { type: 'string' },
          },
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
                commitHash: { type: 'string' },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { message, files } = request.body;

    // TODO: Implement Git integration
    const mockCommitHash = 'abc123def456';

    return reply.send(successResponse(
      { commitHash: mockCommitHash },
      'Changes committed successfully'
    ));
  });
}
