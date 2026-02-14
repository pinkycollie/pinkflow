# Marketing Site Deployment Guide

This guide covers various deployment options for the PinkFlow Marketing Site built with Next.js standalone output.

## Prerequisites

- Docker installed (for container-based deployment)
- Node.js 18+ (for direct deployment)
- Access to deployment platform

## Deployment Options

### Option 1: Docker Container (Recommended)

#### Build the Docker image

```bash
cd marketing-site
docker build -t pinkflow-marketing:latest .
```

#### Run locally

```bash
docker run -p 3000:3000 \
  -e NODE_ENV=production \
  -e NEXT_PUBLIC_SITE_NAME="MBTQ.dev" \
  pinkflow-marketing:latest
```

#### Or use Docker Compose

```bash
docker-compose up -d
```

### Option 2: Next.js Standalone

#### Build

```bash
cd marketing-site
npm install
npm run build
```

#### Deploy

```bash
# Copy standalone output to server
scp -r .next/standalone/* user@server:/app/
scp -r .next/static user@server:/app/.next/
scp -r public user@server:/app/

# On server, run:
cd /app
node server.js
```

### Option 3: Google Cloud Run

#### Prerequisites

- Google Cloud account
- gcloud CLI installed
- Project with Cloud Run API enabled

#### Deploy

```bash
# Build and push to Container Registry
gcloud builds submit \
  --tag gcr.io/PROJECT_ID/pinkflow-marketing \
  --project PROJECT_ID \
  marketing-site/

# Deploy to Cloud Run
gcloud run deploy pinkflow-marketing \
  --image gcr.io/PROJECT_ID/pinkflow-marketing \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 3000 \
  --memory 512Mi \
  --set-env-vars "NODE_ENV=production"
```

### Option 4: Railway

#### Via CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
cd marketing-site
railway up
```

#### Via GitHub Integration

1. Connect Railway to your GitHub repository
2. Select the `marketing-site` directory as root
3. Railway auto-detects Dockerfile and deploys

### Option 5: Render

#### Create render.yaml

```yaml
services:
  - type: web
    name: pinkflow-marketing
    env: docker
    dockerfilePath: ./marketing-site/Dockerfile
    dockerContext: .
    plan: starter
    healthCheckPath: /api/health
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 3000
```

Deploy via Render dashboard or CLI.

### Option 6: Fly.io

#### Prerequisites

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login
```

#### Deploy

```bash
cd marketing-site
flyctl launch

# Follow prompts to configure
# Fly.io will detect Dockerfile and deploy
```

### Option 7: AWS (ECS/Fargate)

#### Build and push to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t pinkflow-marketing marketing-site/
docker tag pinkflow-marketing:latest \
  ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/pinkflow-marketing:latest

# Push
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/pinkflow-marketing:latest
```

#### Create ECS service

Use AWS Console or AWS CLI to create:
- Task definition using the ECR image
- ECS service with load balancer
- Configure environment variables

## Environment Variables

### Required

- `NODE_ENV` - Set to `production`
- `PORT` - Port to run on (default: 3000)

### Optional

- `NEXT_PUBLIC_SITE_NAME` - Site name for metadata
- `NEXT_PUBLIC_SITE_DESCRIPTION` - Site description
- `NEXT_PUBLIC_PLATFORM_URL` - URL to platform app
- `NEXT_PUBLIC_API_URL` - Backend API URL (if needed)

## Health Checks

The site includes a health check endpoint at `/api/health`

```bash
curl http://localhost:3000/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-21T06:53:00.000Z",
  "service": "pinkflow-marketing-site",
  "version": "0.1.0"
}
```

## Performance Optimization

### CDN Configuration

For optimal performance, configure a CDN:

**Cloudflare**:
1. Add site to Cloudflare
2. Configure DNS
3. Enable caching rules
4. Set up page rules for static assets

**AWS CloudFront**:
1. Create distribution
2. Set origin to your deployment
3. Configure cache behaviors
4. Enable compression

### Cache Headers

Next.js automatically sets cache headers for static assets. For additional optimization:

- Static assets: `Cache-Control: public, max-age=31536000, immutable`
- HTML pages: `Cache-Control: public, max-age=3600, s-maxage=3600`
- API routes: Configure per endpoint

## Monitoring

### Logging

The application logs to stdout/stderr. Configure your platform to capture logs:

**Cloud Run**: Logs automatically in Cloud Logging
**Railway**: Built-in log viewer
**Fly.io**: `flyctl logs`
**Docker**: `docker logs container-name`

### Metrics

Monitor these key metrics:

- Request rate
- Response time
- Error rate
- Memory usage
- CPU usage

Tools:
- Google Cloud Monitoring
- Datadog
- New Relic
- Sentry (for errors)

## SSL/TLS

Most platforms provide automatic SSL:

- **Cloud Run**: Automatic with custom domains
- **Railway**: Automatic for all deployments
- **Render**: Automatic with custom domains
- **Fly.io**: Automatic

For manual setup, use Let's Encrypt with Certbot.

## Custom Domain

### Cloud Run

```bash
gcloud run domain-mappings create \
  --service pinkflow-marketing \
  --domain marketing.mbtq.dev \
  --region us-central1
```

Then add DNS records as instructed.

### Railway

1. Go to project settings
2. Add custom domain
3. Configure DNS records

### Fly.io

```bash
flyctl certs add marketing.mbtq.dev
```

## CI/CD

The repository includes a GitHub Actions workflow at `.github/workflows/deploy-marketing-site.yml`

It automatically:
1. Runs type checking
2. Runs linting
3. Builds the application
4. Creates Docker image
5. Pushes to GitHub Container Registry
6. (Optional) Deploys to Cloud Run

## Rollback

### Docker-based deployments

```bash
# List previous images
docker images pinkflow-marketing

# Run previous version
docker run -p 3000:3000 pinkflow-marketing:previous-tag
```

### Cloud Run

```bash
# List revisions
gcloud run revisions list --service pinkflow-marketing

# Route traffic to previous revision
gcloud run services update-traffic pinkflow-marketing \
  --to-revisions=REVISION_NAME=100
```

## Troubleshooting

### Build fails

```bash
# Clear cache and rebuild
cd marketing-site
rm -rf .next node_modules
npm install
npm run build
```

### Container won't start

```bash
# Check logs
docker logs container-name

# Run interactively
docker run -it --entrypoint sh pinkflow-marketing:latest
```

### Health check fails

```bash
# Test locally
curl http://localhost:3000/api/health

# Check if port is correct
docker run -p 3000:3000 pinkflow-marketing:latest
```

### Out of memory

Increase memory allocation:

**Cloud Run**: `--memory 1Gi`
**Docker**: `docker run -m 1g`
**Kubernetes**: Update resource limits

## Cost Estimates

### Cloud Run (US)
- First 2 million requests/month: Free
- Additional requests: $0.40 per million
- CPU: $0.00002400 per vCPU-second
- Memory: $0.00000250 per GiB-second
- **Estimated**: $5-20/month for moderate traffic

### Railway
- Starter: $5/month (500 GB-hours)
- **Estimated**: $5-10/month

### Render
- Starter: $7/month
- **Estimated**: $7-15/month

### Fly.io
- Free tier: 3 shared VMs
- Paid: $1.94/month per VM
- **Estimated**: Free to $5/month

## Security Checklist

- [ ] Environment variables stored securely
- [ ] HTTPS enabled
- [ ] Security headers configured (done in next.config.js)
- [ ] Rate limiting configured (if needed)
- [ ] DDoS protection enabled (via CDN)
- [ ] Regular dependency updates
- [ ] Container image scanning
- [ ] Access logs monitored

## Support

For deployment issues:
1. Check application logs
2. Verify health check endpoint
3. Review environment variables
4. Test locally with Docker
5. Check platform status page

For additional help, see:
- [Next.js Deployment Docs](https://nextjs.org/docs/deployment)
- [Docker Documentation](https://docs.docker.com/)
- Platform-specific documentation
