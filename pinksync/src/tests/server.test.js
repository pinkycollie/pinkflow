import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import { buildApp } from '../server.js';

describe('PinkSync Server', () => {
  let app;

  beforeAll(async () => {
    app = await buildApp({ logger: false });
  });

  afterAll(async () => {
    await app.close();
  });

  describe('Health Endpoints', () => {
    it('should return server status on root endpoint', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/',
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.status).toBe('ok');
      expect(json.service).toBe('PinkSync');
    });

    it('should return healthy status on /health', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/health',
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.status).toBe('healthy');
    });
  });

  describe('Authentication Routes', () => {
    it('should login with valid credentials', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/auth/login',
        payload: {
          email: 'test@example.com',
          password: 'password123',
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.token).toBeDefined();
      expect(json.data.user.email).toBe('test@example.com');
    });

    it('should logout successfully', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/auth/logout',
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
    });

    it('should get current user', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/api/auth/user',
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.email).toBeDefined();
    });

    it('should sync user profile', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/auth/user/profile/sync',
        payload: {
          trustScore: 90,
          vouches: 15,
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
    });
  });

  describe('Workspace Routes', () => {
    it('should get file tree', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/api/workspace/tree',
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(Array.isArray(json.data)).toBe(true);
    });

    it('should get file content', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/api/workspace/file?path=/src/index.js',
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.path).toBe('/src/index.js');
    });

    it('should update file content', async () => {
      const response = await app.inject({
        method: 'PUT',
        url: '/api/workspace/file?path=/src/index.js',
        payload: {
          content: 'console.log("Hello World");',
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
    });

    it('should create new file', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/workspace/file',
        payload: {
          path: '/src/newfile.js',
          content: '// New file',
        },
      });

      expect(response.statusCode).toBe(201);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
    });

    it('should commit changes', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/workspace/commit',
        payload: {
          message: 'Test commit',
          files: ['/src/index.js'],
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.commitHash).toBeDefined();
    });
  });

  describe('Governance Routes', () => {
    it('should get active ballots', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/api/governance/ballots',
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.items).toBeDefined();
      expect(json.data.pagination).toBeDefined();
    });

    it('should vouch for a ballot', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/governance/ballots/ballot-1/vouch',
        payload: {
          vote: 'for',
          comment: 'Great proposal',
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.vouchId).toBeDefined();
    });

    it('should get approved contributions', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/api/governance/contributions/approved',
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.items).toBeDefined();
    });
  });

  describe('AI Routes', () => {
    it('should summarize text', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/ai/summarize',
        payload: {
          text: 'This is a long text that needs to be summarized for better understanding.',
          maxLength: 200,
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.summary).toBeDefined();
    });

    it('should generate content', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/ai/generate',
        payload: {
          prompt: 'Write a function to add two numbers',
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.generated).toBeDefined();
    });

    it('should handle chat messages', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/ai/chat',
        payload: {
          messages: [
            { role: 'user', content: 'Hello' },
          ],
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.response).toBeDefined();
    });

    it('should analyze code', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/ai/analyze-code',
        payload: {
          code: 'function add(a, b) { return a + b; }',
          language: 'javascript',
          analysisType: 'bugs',
        },
      });

      expect(response.statusCode).toBe(200);
      const json = JSON.parse(response.body);
      expect(json.success).toBe(true);
      expect(json.data.analysis).toBeDefined();
    });
  });
});
