# PinkSync Deployment Guide

This guide covers deploying PinkSync to various platforms.

## Prerequisites

- Docker (for containerized deployment)
- Node.js 18+ (for direct deployment)
- Environment variables configured

## Environment Variables

Required environment variables:

```bash
PORT=3000
HOST=0.0.0.0
NODE_ENV=production
JWT_SECRET=your-secure-secret-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
GEMINI_API_KEY=your-gemini-api-key
CORS_ORIGIN=https://your-frontend-domain.com
LOG_LEVEL=info
```

## Deployment Options

### 1. Docker Deployment

#### Build Docker Image

```bash
docker build -t pinksync:latest .
```

#### Run Container

```bash
docker run -d \
  --name pinksync \
  -p 3000:3000 \
  -e PORT=3000 \
  -e NODE_ENV=production \
  -e JWT_SECRET=your-secret \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_KEY=your-key \
  -e GEMINI_API_KEY=your-api-key \
  -e CORS_ORIGIN=https://your-frontend.com \
  pinksync:latest
```

#### Using Docker Compose

```bash
# Create .env file with required variables
cp .env.example .env
# Edit .env with your values

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Google Cloud Run

#### Prerequisites
- Google Cloud SDK installed
- Project created in Google Cloud Console

#### Deploy

```bash
# Set project ID
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID

# Build and push image to Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/pinksync

# Deploy to Cloud Run
gcloud run deploy pinksync \
  --image gcr.io/$PROJECT_ID/pinksync \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "NODE_ENV=production" \
  --set-secrets "JWT_SECRET=jwt-secret:latest" \
  --set-secrets "SUPABASE_KEY=supabase-key:latest" \
  --set-secrets "GEMINI_API_KEY=gemini-key:latest"
```

### 3. Vercel Deployment

Create `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/server.js"
    }
  ]
}
```

Deploy:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### 4. AWS ECS/Fargate

#### Create ECR Repository

```bash
aws ecr create-repository --repository-name pinksync
```

#### Build and Push Image

```bash
# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t pinksync .
docker tag pinksync:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/pinksync:latest

# Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/pinksync:latest
```

#### Create ECS Task Definition

Use AWS Console or CLI to create task definition with the image.

### 5. Kubernetes Deployment

#### Create Kubernetes Manifests

**deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pinksync
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pinksync
  template:
    metadata:
      labels:
        app: pinksync
    spec:
      containers:
      - name: pinksync
        image: pinksync:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: PORT
          value: "3000"
        envFrom:
        - secretRef:
            name: pinksync-secrets
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 250m
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
```

**service.yaml:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: pinksync
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 3000
  selector:
    app: pinksync
```

**secrets.yaml:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: pinksync-secrets
type: Opaque
stringData:
  JWT_SECRET: your-secret
  SUPABASE_URL: your-url
  SUPABASE_KEY: your-key
  GEMINI_API_KEY: your-api-key
  CORS_ORIGIN: https://your-frontend.com
```

Deploy:

```bash
kubectl apply -f secrets.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 6. Direct Deployment (VPS/Bare Metal)

#### Using PM2 Process Manager

```bash
# Install PM2 globally
npm install -g pm2

# Start application
cd /path/to/pinksync
pm2 start src/server.js --name pinksync

# Save PM2 process list
pm2 save

# Setup PM2 to start on system boot
pm2 startup
```

#### Using systemd

Create `/etc/systemd/system/pinksync.service`:

```ini
[Unit]
Description=PinkSync Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/pinksync
ExecStart=/usr/bin/node src/server.js
Restart=on-failure
Environment=NODE_ENV=production
EnvironmentFile=/opt/pinksync/.env

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable pinksync
sudo systemctl start pinksync
sudo systemctl status pinksync
```

## Load Balancing

For production deployments, use a reverse proxy:

### Nginx Configuration

```nginx
upstream pinksync {
    server localhost:3000;
    # Add more servers for load balancing
    # server localhost:3001;
    # server localhost:3002;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://pinksync;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://pinksync;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```

## SSL/TLS Configuration

### Using Let's Encrypt with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

## Monitoring

### Health Checks

The service provides two health endpoints:

- `/` - Detailed status including WebSocket client count
- `/health` - Simple health check

### Logging

Logs are output to stdout/stderr. Capture them using:

- **Docker**: `docker logs pinksync`
- **PM2**: `pm2 logs pinksync`
- **systemd**: `journalctl -u pinksync -f`

### Metrics

Consider integrating monitoring tools:

- Prometheus
- Grafana
- DataDog
- New Relic

## Scaling

### Horizontal Scaling

Run multiple instances behind a load balancer:

```bash
# Start multiple instances
PORT=3000 node src/server.js &
PORT=3001 node src/server.js &
PORT=3002 node src/server.js &
```

Configure Nginx to balance load across instances.

### Auto-scaling (Kubernetes)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pinksync-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pinksync
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Security Best Practices

1. **Use HTTPS**: Always use SSL/TLS in production
2. **Environment Variables**: Never commit secrets to version control
3. **CORS**: Configure CORS_ORIGIN to your frontend domain only
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Firewall**: Use firewall rules to restrict access
6. **Updates**: Keep dependencies updated regularly

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000
# Kill the process
kill -9 <PID>
```

### Memory Issues

Increase Node.js memory limit:

```bash
node --max-old-space-size=4096 src/server.js
```

### WebSocket Connection Issues

Ensure your reverse proxy supports WebSocket upgrades.

## Rollback

### Docker

```bash
# Tag previous version
docker tag pinksync:latest pinksync:rollback
# Pull previous version and restart
docker-compose down
docker-compose up -d
```

### Kubernetes

```bash
kubectl rollout undo deployment/pinksync
```

## Support

For deployment issues:
- Check logs first
- Review configuration
- Consult documentation at `/docs` endpoint
- Contact MBTQ.dev support

---

Built for the Deaf-First innovation ecosystem at MBTQ.dev
