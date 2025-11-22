# Migration Guide: FastAPI to Fastify

This guide helps developers migrate from the planned FastAPI implementation to the Fastify implementation for PinkSync.

## Overview

PinkSync has been implemented using Fastify (Node.js) instead of FastAPI (Python) to provide better performance, WebSocket support, and seamless integration with the Node.js ecosystem.

## Key Differences

### Technology Stack

| Aspect | FastAPI | Fastify |
|--------|---------|---------|
| Language | Python | JavaScript/Node.js |
| Runtime | Python 3.8+ | Node.js 18+ |
| Async Model | asyncio/await | Promises/async-await |
| Documentation | Auto-generated OpenAPI | Auto-generated OpenAPI |
| WebSocket | Requires additional library | Native support via plugin |
| Performance | Fast | Faster (benchmarks show 20-40% improvement) |

### API Response Format

Both implementations use the same response format for consistency:

**Success Response:**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { }
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error message",
  "statusCode": 400,
  "details": null
}
```

### Route Structure Comparison

#### FastAPI (Python)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    # Implementation
    return {"success": True, "data": {}}
```

#### Fastify (JavaScript)
```javascript
export default async function authRoutes(fastify) {
  fastify.post('/login', {
    schema: {
      body: {
        type: 'object',
        required: ['email', 'password'],
        properties: {
          email: { type: 'string', format: 'email' },
          password: { type: 'string' }
        }
      }
    }
  }, async (request, reply) => {
    // Implementation
    return reply.send({ success: true, data: {} });
  });
}
```

## Migration Steps

### 1. Environment Setup

**FastAPI:**
```bash
pip install fastapi uvicorn
```

**Fastify:**
```bash
npm install fastify
```

### 2. Route Migration

#### Authentication Routes

**FastAPI:**
```python
@router.post("/login")
async def login(credentials: LoginCredentials):
    user = await authenticate(credentials)
    return {"token": create_jwt(user), "user": user}
```

**Fastify:**
```javascript
fastify.post('/login', async (request, reply) => {
  const user = await authenticate(request.body);
  return reply.send({
    success: true,
    data: { token: createJWT(user), user }
  });
});
```

#### Validation

**FastAPI (Pydantic):**
```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
```

**Fastify (JSON Schema):**
```javascript
const userSchema = {
  type: 'object',
  required: ['email', 'password'],
  properties: {
    email: { type: 'string', format: 'email' },
    password: { type: 'string', minLength: 6 }
  }
};
```

### 3. Middleware Migration

**FastAPI (Dependency Injection):**
```python
from fastapi import Depends, HTTPException

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401)
    return user

@router.get("/user")
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user
```

**Fastify (Hooks):**
```javascript
export async function verifyToken(request, reply) {
  const token = request.headers.authorization?.split(' ')[1];
  const user = await verify(token);
  if (!user) {
    return reply.code(401).send({ success: false });
  }
  request.user = user;
}

fastify.get('/user', {
  preHandler: verifyToken
}, async (request, reply) => {
  return request.user;
});
```

### 4. Database Integration

**FastAPI (SQLAlchemy):**
```python
from sqlalchemy.orm import Session
from . import models

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
```

**Fastify (Supabase/PostgreSQL):**
```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(url, key);

async function getUser(userId) {
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', userId)
    .single();
  return data;
}
```

### 5. WebSocket Implementation

**FastAPI (requires additional library):**
```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
```

**Fastify (native support):**
```javascript
fastify.get('/ws', { websocket: true }, (connection, request) => {
  connection.socket.on('message', (message) => {
    connection.socket.send('Message: ' + message);
  });
});
```

## Feature Parity Checklist

- [x] REST API endpoints
- [x] OpenAPI/Swagger documentation
- [x] Request validation
- [x] Error handling
- [x] Authentication middleware
- [x] WebSocket support
- [x] CORS configuration
- [x] Environment configuration
- [x] Logging
- [x] Testing framework

## Performance Comparison

Based on industry benchmarks:

| Metric | FastAPI | Fastify | Improvement |
|--------|---------|---------|-------------|
| Requests/sec | ~20,000 | ~30,000 | +50% |
| Latency (ms) | 5-10 | 3-6 | 40% faster |
| Memory (MB) | 50-80 | 40-60 | 25% less |

## Advantages of Fastify

1. **Better WebSocket Support**: Native, production-ready WebSocket implementation
2. **Lower Latency**: Faster request processing
3. **Ecosystem**: Direct integration with Node.js packages
4. **TypeScript Support**: Optional TypeScript for type safety
5. **Plugin System**: Robust and efficient plugin architecture
6. **Community**: Large, active community

## Frontend Integration

No changes needed for frontend integration! The API contract remains the same:

```javascript
// Works with both FastAPI and Fastify
const response = await fetch('http://localhost:3000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});

const data = await response.json();
```

## Testing Migration

**FastAPI (pytest):**
```python
def test_login():
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password"
    })
    assert response.status_code == 200
```

**Fastify (Jest):**
```javascript
test('should login successfully', async () => {
  const response = await app.inject({
    method: 'POST',
    url: '/api/auth/login',
    payload: { email: 'test@example.com', password: 'password' }
  });
  expect(response.statusCode).toBe(200);
});
```

## Deployment

### FastAPI
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Fastify
```bash
node src/server.js
# or with npm
npm start
```

## Docker

**FastAPI Dockerfile:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

**Fastify Dockerfile:**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "src/server.js"]
```

## Common Pitfalls

1. **Async/Await**: Both use async/await but with different syntaxes
2. **Error Handling**: Fastify uses reply.code() instead of raising exceptions
3. **Request Body**: FastAPI uses request models, Fastify uses request.body
4. **Path Parameters**: Similar but accessed differently (request.params)

## Support and Resources

- **Fastify Documentation**: https://www.fastify.io/
- **Migration Support**: Contact PinkFlow team
- **Community**: MBTQ.dev Discord/Forums

## Conclusion

The Fastify implementation provides all the features planned for FastAPI with better performance and native WebSocket support. The API contract remains consistent, ensuring smooth frontend integration.
