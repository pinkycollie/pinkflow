# API Documentation

Complete API reference for PinkSync service.

## Base URL

```
http://localhost:3000
```

## Response Format

All endpoints return JSON responses in the following format:

### Success Response

```json
{
  "success": true,
  "message": "Success message",
  "data": { /* response data */ }
}
```

### Error Response

```json
{
  "success": false,
  "message": "Error message",
  "statusCode": 400,
  "details": "Additional error details"
}
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## Authentication Endpoints

### POST /api/auth/login

Authenticate a user and receive a JWT token.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": "user-123",
      "email": "user@example.com",
      "role": "developer",
      "fibonRoseProfile": {
        "trustScore": 85,
        "vouches": 12
      }
    }
  }
}
```

### POST /api/auth/logout

Invalidate the current session.

**Response:**

```json
{
  "success": true,
  "message": "Logout successful"
}
```

### GET /api/auth/user

Get the current authenticated user's profile.

**Headers:**
- Authorization: Bearer <token>

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "id": "user-123",
    "email": "user@example.com",
    "role": "developer",
    "fibonRoseProfile": {
      "trustScore": 85,
      "vouches": 12
    }
  }
}
```

### POST /api/auth/user/profile/sync

Sync or update the user's FibonRose trust profile.

**Request Body:**

```json
{
  "trustScore": 90,
  "vouches": 15
}
```

**Response:**

```json
{
  "success": true,
  "message": "Profile synced successfully",
  "data": {
    "trustScore": 90,
    "vouches": 15
  }
}
```

---

## Workspace Endpoints

### GET /api/workspace/tree

Get the workspace file tree structure.

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": [
    {
      "id": "1",
      "name": "src",
      "path": "/src",
      "type": "directory",
      "children": [
        {
          "id": "2",
          "name": "index.js",
          "path": "/src/index.js",
          "type": "file"
        }
      ]
    }
  ]
}
```

### GET /api/workspace/file

Get file content by path.

**Query Parameters:**
- `path` (required): File path (e.g., `/src/index.js`)

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "path": "/src/index.js",
    "content": "// File content here"
  }
}
```

### PUT /api/workspace/file

Update file content.

**Query Parameters:**
- `path` (required): File path

**Request Body:**

```json
{
  "content": "// Updated file content"
}
```

**Response:**

```json
{
  "success": true,
  "message": "File updated successfully"
}
```

### POST /api/workspace/file

Create a new file.

**Request Body:**

```json
{
  "path": "/src/newfile.js",
  "content": "// New file content"
}
```

**Response:**

```json
{
  "success": true,
  "message": "File created successfully"
}
```

### POST /api/workspace/commit

Commit changes to the workspace (Git integration).

**Request Body:**

```json
{
  "message": "Commit message",
  "files": ["/src/index.js", "/src/utils.js"]
}
```

**Response:**

```json
{
  "success": true,
  "message": "Changes committed successfully",
  "data": {
    "commitHash": "abc123def456"
  }
}
```

---

## Governance Endpoints

### GET /api/governance/ballots

List active governance proposals.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `perPage` (optional): Items per page (default: 20, max: 100)
- `status` (optional): Filter by status (`active`, `closed`, `pending`)

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "ballot-1",
        "title": "Add new feature to IDE",
        "description": "Proposal to add real-time collaboration",
        "status": "active",
        "createdBy": "user-123",
        "votes": {
          "for": 45,
          "against": 12
        },
        "createdAt": "2024-01-15T10:00:00.000Z"
      }
    ],
    "pagination": {
      "page": 1,
      "perPage": 20,
      "total": 50,
      "totalPages": 3
    }
  }
}
```

### POST /api/governance/ballots/:id/vouch

Vouch for a proposal with trust validation.

**Path Parameters:**
- `id`: Ballot ID

**Request Body:**

```json
{
  "vote": "for",
  "comment": "Great proposal"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Vouch recorded successfully",
  "data": {
    "vouchId": "vouch-123",
    "trustScoreApplied": 85
  }
}
```

### GET /api/governance/contributions/approved

List approved contributions.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `perPage` (optional): Items per page (default: 20, max: 100)

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "items": [
      {
        "id": "contrib-1",
        "title": "Fix authentication bug",
        "contributor": "user-789",
        "type": "bugfix",
        "approvedAt": "2024-01-15T10:00:00.000Z"
      }
    ],
    "pagination": {
      "page": 1,
      "perPage": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

---

## AI Proxy Endpoints

### POST /api/ai/summarize

Summarize text using Gemini API.

**Request Body:**

```json
{
  "text": "Long text to summarize...",
  "maxLength": 200
}
```

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "summary": "Summarized text...",
    "originalLength": 500,
    "summaryLength": 150
  }
}
```

### POST /api/ai/generate

Generate content using Gemini API.

**Request Body:**

```json
{
  "prompt": "Write a function to add two numbers",
  "temperature": 0.7,
  "maxTokens": 1024
}
```

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "generated": "function add(a, b) { return a + b; }",
    "tokensUsed": 125
  }
}
```

### POST /api/ai/chat

Chat with Gemini AI.

**Request Body:**

```json
{
  "messages": [
    { "role": "user", "content": "Hello, how are you?" },
    { "role": "assistant", "content": "I'm doing well, thank you!" },
    { "role": "user", "content": "Can you help me with coding?" }
  ],
  "temperature": 0.7
}
```

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "response": "Of course! I'd be happy to help you with coding.",
    "role": "assistant"
  }
}
```

### POST /api/ai/analyze-code

Analyze code for bugs, performance, or security issues.

**Request Body:**

```json
{
  "code": "function add(a, b) { return a + b; }",
  "language": "javascript",
  "analysisType": "bugs"
}
```

**Analysis Types:**
- `bugs`: Find potential bugs
- `performance`: Analyze performance issues
- `security`: Check for security vulnerabilities
- `style`: Review code style

**Response:**

```json
{
  "success": true,
  "message": "Success",
  "data": {
    "analysis": "Code analysis results...",
    "suggestions": [
      "Consider adding error handling",
      "Add input validation",
      "Optimize loop performance"
    ]
  }
}
```

---

## WebSocket Endpoints

### WS /ws

Connect to the WebSocket server for real-time collaboration.

**Connection:**

```javascript
const ws = new WebSocket('ws://localhost:3000/ws');
```

**Events:**

#### Client → Server Messages

**Ping:**
```json
{
  "type": "ping"
}
```

**Broadcast:**
```json
{
  "type": "broadcast",
  "payload": {
    "message": "Hello everyone!"
  }
}
```

**File Edit:**
```json
{
  "type": "file-edit",
  "path": "/src/index.js"
}
```

**Presence Update:**
```json
{
  "type": "presence",
  "status": "online"
}
```

#### Server → Client Messages

**Connected:**
```json
{
  "type": "connected",
  "clientId": "1234567890",
  "message": "Connected to PinkSync"
}
```

**Pong:**
```json
{
  "type": "pong",
  "timestamp": 1642234567890
}
```

**File Changed:**
```json
{
  "type": "file-changed",
  "path": "/src/index.js",
  "userId": "user-123",
  "timestamp": 1642234567890
}
```

**User Presence:**
```json
{
  "type": "user-presence",
  "userId": "user-123",
  "status": "online",
  "timestamp": 1642234567890
}
```

**User Disconnected:**
```json
{
  "type": "user-disconnected",
  "userId": "user-123",
  "timestamp": 1642234567890
}
```

---

## Health Check Endpoints

### GET /

Get server status with detailed information.

**Response:**

```json
{
  "status": "ok",
  "service": "PinkSync",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:00:00.000Z",
  "websocketClients": 5
}
```

### GET /health

Simple health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00.000Z"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Rate Limiting

API rate limits (to be implemented):
- Authenticated users: 1000 requests/hour
- Unauthenticated users: 100 requests/hour

When rate limit is exceeded:

```json
{
  "success": false,
  "message": "Rate limit exceeded",
  "statusCode": 429,
  "details": {
    "retryAfter": 3600
  }
}
```

---

## Interactive Documentation

For interactive API testing, visit:

```
http://localhost:3000/docs
```

The Swagger UI provides:
- Full API documentation
- Request/response examples
- Interactive testing
- Schema validation

---

## Examples

### cURL Examples

**Login:**
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

**Get Workspace Tree:**
```bash
curl http://localhost:3000/api/workspace/tree
```

**Create File:**
```bash
curl -X POST http://localhost:3000/api/workspace/file \
  -H "Content-Type: application/json" \
  -d '{"path":"/src/test.js","content":"// Test file"}'
```

### JavaScript/Fetch Examples

**Login:**
```javascript
const response = await fetch('http://localhost:3000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const data = await response.json();
```

**WebSocket Connection:**
```javascript
const ws = new WebSocket('ws://localhost:3000/ws');

ws.onopen = () => {
  console.log('Connected to PinkSync');
  ws.send(JSON.stringify({ type: 'ping' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

---

For more information, see:
- [README.md](./README.md) - Setup and installation
- [MIGRATION.md](./MIGRATION.md) - Migration guide from FastAPI
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment instructions
- [BENCHMARKING.md](./BENCHMARKING.md) - Performance testing
