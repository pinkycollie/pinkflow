# Performance Benchmarking Guide

This guide helps you benchmark PinkSync performance and compare it with other implementations.

## Prerequisites

Install benchmarking tools:

```bash
npm install -g autocannon
npm install -g clinic
```

## Quick Benchmark

### Using autocannon

Benchmark a specific endpoint:

```bash
# Benchmark root endpoint
autocannon -c 100 -d 30 http://localhost:3000/

# Benchmark API endpoint
autocannon -c 100 -d 30 -m POST \
  -H "Content-Type: application/json" \
  -b '{"email":"test@example.com","password":"password123"}' \
  http://localhost:3000/api/auth/login

# Benchmark with more connections
autocannon -c 500 -d 60 http://localhost:3000/api/workspace/tree
```

Parameters:
- `-c`: Number of concurrent connections
- `-d`: Duration in seconds
- `-m`: HTTP method
- `-H`: Headers
- `-b`: Request body

### Expected Results

Typical performance on a modern server:

```
Running 30s test @ http://localhost:3000/
100 connections

┌─────────┬──────┬──────┬───────┬──────┬─────────┬─────────┬──────────┐
│ Stat    │ 2.5% │ 50%  │ 97.5% │ 99%  │ Avg     │ Stdev   │ Max      │
├─────────┼──────┼──────┼───────┼──────┼─────────┼─────────┼──────────┤
│ Latency │ 2 ms │ 3 ms │ 8 ms  │ 12 ms│ 3.5 ms  │ 2.1 ms  │ 45 ms    │
└─────────┴──────┴──────┴───────┴──────┴─────────┴─────────┴──────────┘
┌───────────┬─────────┬─────────┬─────────┬─────────┬──────────┬─────────┬─────────┐
│ Stat      │ 1%      │ 2.5%    │ 50%     │ 97.5%   │ Avg      │ Stdev   │ Min     │
├───────────┼─────────┼─────────┼─────────┼─────────┼──────────┼─────────┼─────────┤
│ Req/Sec   │ 25,000  │ 25,000  │ 30,000  │ 32,000  │ 29,500   │ 2,100   │ 25,000  │
├───────────┼─────────┼─────────┼─────────┼─────────┼──────────┼─────────┼─────────┤
│ Bytes/Sec │ 5.2 MB  │ 5.2 MB  │ 6.2 MB  │ 6.6 MB  │ 6.1 MB   │ 430 kB  │ 5.2 MB  │
└───────────┴─────────┴─────────┴─────────┴─────────┴──────────┴─────────┴─────────┘

Req/Bytes counts sampled once per second.
900k requests in 30.03s, 183 MB read
```

## Comprehensive Benchmarking

### Create Benchmark Script

Save as `benchmark.sh`:

```bash
#!/bin/bash

echo "PinkSync Performance Benchmark"
echo "==============================="
echo ""

# Start server in background
npm start &
SERVER_PID=$!
sleep 3

echo "1. Root Endpoint"
echo "----------------"
autocannon -c 100 -d 10 http://localhost:3000/
echo ""

echo "2. Health Check"
echo "---------------"
autocannon -c 100 -d 10 http://localhost:3000/health
echo ""

echo "3. Login Endpoint"
echo "----------------"
autocannon -c 100 -d 10 -m POST \
  -H "Content-Type: application/json" \
  -b '{"email":"test@example.com","password":"password123"}' \
  http://localhost:3000/api/auth/login
echo ""

echo "4. Workspace Tree"
echo "----------------"
autocannon -c 100 -d 10 http://localhost:3000/api/workspace/tree
echo ""

echo "5. Governance Ballots"
echo "--------------------"
autocannon -c 100 -d 10 http://localhost:3000/api/governance/ballots
echo ""

# Kill server
kill $SERVER_PID

echo "Benchmark Complete!"
```

Run:

```bash
chmod +x benchmark.sh
./benchmark.sh
```

## Profiling with Clinic.js

### CPU Profiling

```bash
clinic doctor -- node src/server.js
```

Run load tests in another terminal, then stop the server (Ctrl+C).
Open the generated HTML report.

### Flame Graph

```bash
clinic flame -- node src/server.js
```

### Heap Profiling

```bash
clinic heapprofiler -- node src/server.js
```

### Bubble Profiler

```bash
clinic bubbleprof -- node src/server.js
```

## Load Testing

### Using Artillery

Install:

```bash
npm install -g artillery
```

Create `load-test.yml`:

```yaml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Peak load"

scenarios:
  - name: "API Test"
    flow:
      - get:
          url: "/"
      - post:
          url: "/api/auth/login"
          json:
            email: "test@example.com"
            password: "password123"
      - get:
          url: "/api/workspace/tree"
      - get:
          url: "/api/governance/ballots"
```

Run:

```bash
artillery run load-test.yml
```

## WebSocket Benchmarking

Create `ws-bench.js`:

```javascript
const WebSocket = require('ws');

const CONNECTIONS = 100;
const MESSAGES_PER_CONNECTION = 100;

let completed = 0;
let totalTime = 0;

for (let i = 0; i < CONNECTIONS; i++) {
  const ws = new WebSocket('ws://localhost:3000/ws');
  
  ws.on('open', () => {
    const startTime = Date.now();
    let received = 0;
    
    ws.on('message', () => {
      received++;
      if (received === MESSAGES_PER_CONNECTION) {
        totalTime += Date.now() - startTime;
        completed++;
        ws.close();
        
        if (completed === CONNECTIONS) {
          const avgTime = totalTime / CONNECTIONS;
          const totalMessages = CONNECTIONS * MESSAGES_PER_CONNECTION;
          console.log(`Total connections: ${CONNECTIONS}`);
          console.log(`Messages per connection: ${MESSAGES_PER_CONNECTION}`);
          console.log(`Total messages: ${totalMessages}`);
          console.log(`Average time per connection: ${avgTime.toFixed(2)}ms`);
          console.log(`Messages per second: ${(totalMessages / (totalTime / 1000)).toFixed(2)}`);
          process.exit(0);
        }
      }
    });
    
    for (let j = 0; j < MESSAGES_PER_CONNECTION; j++) {
      ws.send(JSON.stringify({ type: 'ping' }));
    }
  });
}
```

Run:

```bash
node ws-bench.js
```

## Performance Comparison

### Fastify vs FastAPI

Expected metrics (approximate):

| Metric | FastAPI | Fastify | Improvement |
|--------|---------|---------|-------------|
| Requests/sec | 20,000 | 30,000 | +50% |
| Latency (p50) | 5ms | 3ms | 40% faster |
| Latency (p99) | 20ms | 12ms | 40% faster |
| Memory usage | 60MB | 45MB | 25% less |
| CPU usage | 35% | 25% | 29% less |

### Benchmarking Script for Comparison

```bash
#!/bin/bash

echo "Comparative Benchmark Results"
echo "=============================="

# Fastify (PinkSync)
echo "Testing Fastify Implementation..."
npm start &
FASTIFY_PID=$!
sleep 3
FASTIFY_RESULT=$(autocannon -c 100 -d 30 -j http://localhost:3000/ | jq -r '.requests.average')
kill $FASTIFY_PID

echo "Fastify avg requests/sec: $FASTIFY_RESULT"

# Add FastAPI comparison if available
# Similar commands for FastAPI endpoint

echo ""
echo "Performance comparison complete!"
```

## Optimization Tips

### 1. Enable Clustering

Create `cluster.js`:

```javascript
import cluster from 'cluster';
import os from 'os';
import { buildApp } from './src/server.js';

if (cluster.isPrimary) {
  const numCPUs = os.cpus().length;
  console.log(`Master process starting ${numCPUs} workers...`);
  
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork();
  });
} else {
  const app = await buildApp();
  await app.listen({ port: 3000, host: '0.0.0.0' });
  console.log(`Worker ${process.pid} started`);
}
```

### 2. Enable HTTP/2

```javascript
import { readFileSync } from 'fs';

const fastify = Fastify({
  http2: true,
  https: {
    key: readFileSync('./key.pem'),
    cert: readFileSync('./cert.pem')
  }
});
```

### 3. Response Compression

```bash
npm install @fastify/compress
```

```javascript
import compress from '@fastify/compress';
await fastify.register(compress);
```

### 4. Caching

```bash
npm install @fastify/caching
```

### 5. Connection Pooling

For database connections, use proper pooling:

```javascript
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
});
```

## Monitoring Performance in Production

### 1. Response Time Tracking

Add to routes:

```javascript
fastify.addHook('onRequest', (request, reply, done) => {
  request.startTime = Date.now();
  done();
});

fastify.addHook('onResponse', (request, reply, done) => {
  const responseTime = Date.now() - request.startTime;
  fastify.log.info({ responseTime, url: request.url });
  done();
});
```

### 2. Request Rate Limiting

```bash
npm install @fastify/rate-limit
```

```javascript
import rateLimit from '@fastify/rate-limit';

await fastify.register(rateLimit, {
  max: 100,
  timeWindow: '1 minute'
});
```

### 3. Metrics Export

Use Prometheus metrics:

```bash
npm install fastify-metrics
```

## Troubleshooting Performance Issues

### High Latency

1. Check database query performance
2. Review async operations
3. Enable response caching
4. Use clustering

### High Memory Usage

1. Check for memory leaks with `clinic heapprofiler`
2. Review WebSocket connection management
3. Implement connection limits
4. Use streaming for large responses

### Low Throughput

1. Enable clustering
2. Optimize database connections
3. Use caching
4. Review middleware overhead

## Reporting

Generate benchmark report:

```bash
autocannon -c 100 -d 30 http://localhost:3000/ > benchmark-report.txt
```

Share results with the team for continuous improvement.

---

For more detailed profiling, refer to:
- Fastify Performance: https://www.fastify.io/docs/latest/Guides/Getting-Started/#your-first-server
- Clinic.js Documentation: https://clinicjs.org/
- Node.js Performance: https://nodejs.org/en/docs/guides/simple-profiling/
