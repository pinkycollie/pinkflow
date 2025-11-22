import { successResponse, errorResponse } from '../utils/responses.js';
import config from '../config/index.js';

/**
 * AI proxy routes for Gemini API
 * @param {import('fastify').FastifyInstance} fastify
 */
export default async function aiRoutes(fastify) {
  // Summarize content
  fastify.post('/summarize', {
    schema: {
      description: 'Summarize text using Gemini API',
      tags: ['AI'],
      body: {
        type: 'object',
        required: ['text'],
        properties: {
          text: { type: 'string' },
          maxLength: { type: 'integer', minimum: 50, maximum: 1000 },
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
                summary: { type: 'string' },
                originalLength: { type: 'integer' },
                summaryLength: { type: 'integer' },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { text, maxLength = 200 } = request.body;

    // TODO: Implement actual Gemini API call with config.gemini.apiKey
    // For security, API key is never exposed to client
    const mockSummary = `This is a summarized version of the text. Original length: ${text.length} characters.`;

    return reply.send(successResponse({
      summary: mockSummary,
      originalLength: text.length,
      summaryLength: mockSummary.length,
    }));
  });

  // Generate content
  fastify.post('/generate', {
    schema: {
      description: 'Generate content using Gemini API',
      tags: ['AI'],
      body: {
        type: 'object',
        required: ['prompt'],
        properties: {
          prompt: { type: 'string' },
          temperature: { type: 'number', minimum: 0, maximum: 2 },
          maxTokens: { type: 'integer', minimum: 1, maximum: 4096 },
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
                generated: { type: 'string' },
                tokensUsed: { type: 'integer' },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { prompt, temperature = 0.7, maxTokens = 1024 } = request.body;

    // TODO: Implement actual Gemini API call
    const mockGenerated = `Generated response for prompt: "${prompt.substring(0, 50)}..."`;

    return reply.send(successResponse({
      generated: mockGenerated,
      tokensUsed: 125,
    }));
  });

  // Chat completion
  fastify.post('/chat', {
    schema: {
      description: 'Chat with Gemini AI',
      tags: ['AI'],
      body: {
        type: 'object',
        required: ['messages'],
        properties: {
          messages: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                role: { type: 'string', enum: ['user', 'assistant', 'system'] },
                content: { type: 'string' },
              },
            },
          },
          temperature: { type: 'number', minimum: 0, maximum: 2 },
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
                response: { type: 'string' },
                role: { type: 'string' },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { messages, temperature = 0.7 } = request.body;

    // TODO: Implement actual Gemini chat API call
    const lastMessage = messages[messages.length - 1];
    const mockResponse = `AI response to: "${lastMessage.content.substring(0, 50)}..."`;

    return reply.send(successResponse({
      response: mockResponse,
      role: 'assistant',
    }));
  });

  // Code analysis
  fastify.post('/analyze-code', {
    schema: {
      description: 'Analyze code using Gemini AI',
      tags: ['AI'],
      body: {
        type: 'object',
        required: ['code'],
        properties: {
          code: { type: 'string' },
          language: { type: 'string' },
          analysisType: {
            type: 'string',
            enum: ['bugs', 'performance', 'security', 'style'],
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
                analysis: { type: 'string' },
                suggestions: {
                  type: 'array',
                  items: { type: 'string' },
                },
              },
            },
          },
        },
      },
    },
  }, async (request, reply) => {
    const { code, language, analysisType = 'bugs' } = request.body;

    // TODO: Implement actual code analysis with Gemini
    const mockAnalysis = {
      analysis: `Code analysis for ${language} (${analysisType})`,
      suggestions: [
        'Consider adding error handling',
        'Optimize loop performance',
        'Add input validation',
      ],
    };

    return reply.send(successResponse(mockAnalysis));
  });
}
