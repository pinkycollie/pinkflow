# 🟣 Pinkflow DAO Sync Engine

**Decentralized deployment governance for the MBTQ Universe**

The Pinkflow DAO Sync Engine is a comprehensive system that enables decentralized governance over deployment processes. It integrates with Vercel, GitHub, and various DAO platforms to provide automated deployment approval workflows with community voting.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   mbtq.dev      │    │   Pinkflow      │    │   Production    │
│   (Frontend)    │───▶│   DAO Sync      │───▶│   Domains       │
│                 │    │   Engine        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   DAO Backend   │
                       │   (Voting &     │
                       │   Governance)   │
                       └─────────────────┘
```

## 🚀 Key Features

### 🔄 Automated Deployment Sync
- **Vercel Integration**: Automatically detects new preview deployments
- **GitHub Integration**: Links deployments to PRs and commits
- **Real-time Updates**: Live status updates and notifications

### 🗳️ DAO Governance
- **Community Voting**: Allow community members to vote on deployments
- **Approval Thresholds**: Configurable approval rates (default: 75%)
- **Voting Power**: Weighted voting based on user roles and contributions
- **Audit Trail**: Complete history of all votes and decisions

### 🛡️ Security & Compliance
- **Access Control**: Role-based permissions for voters
- **Audit Logging**: Comprehensive logging of all operations
- **Rate Limiting**: Protection against spam and abuse
- **PinkSync Integration**: Accessibility compliance verification

### 📊 Analytics & Monitoring
- **Deployment Metrics**: Success rates, approval times, community engagement
- **Voter Analytics**: Participation rates, voting patterns
- **Performance Monitoring**: Response times, error rates
- **Health Checks**: System status and component monitoring

## 📁 Project Structure

```
pinkflow/
├── api/                          # API endpoints
│   ├── deployments/
│   │   ├── sync.js              # Sync deployment metadata
│   │   ├── status.js            # Query deployment status
│   │   └── deploy.js            # Trigger production deploys
│   └── dao/
│       └── votes.js             # Submit and query votes
├── services/                     # Business logic services
│   ├── daoBackend.js            # DAO data management
│   ├── vercel.js                # Vercel API integration
│   ├── github.js                # GitHub API integration
│   ├── notion.js                # Notion integration
│   └── claudeAI.js              # AI-powered reviews
├── workers/                      # Background workers
│   ├── pollVercelDeployments.js # Poll for new deployments
│   └── monitorProdDeploy.js     # Monitor production status
├── utils/                        # Shared utilities
│   ├── logger.js                # Centralized logging
│   └── helpers.js               # Helper functions
└── config/                       # Configuration
    ├── env.example              # Environment template
    └── secrets.json             # Secure secrets (gitignored)
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/360magicians/pinkflow.git
cd pinkflow

# Install dependencies
npm install

# Copy environment template
cp config/env.example .env

# Configure your environment variables
# (See Configuration section below)
```

### 2. Configuration

Edit your `.env` file with the required credentials:

```env
# Vercel Configuration
VERCEL_TOKEN=your_vercel_token_here
VERCEL_TEAM_ID=your_team_id_here

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_APP_ID=your_app_id_here

# DAO Configuration
DAO_APPROVAL_THRESHOLD=75
DAO_MIN_VOTES=3
DAO_VOTING_PERIOD=86400000

# Other configurations...
```

### 3. Start the Services

```bash
# Start the Vercel deployment poller
node workers/pollVercelDeployments.js

# Start the API server (if using Express/Node.js)
npm start

# Or deploy to Vercel for serverless functions
vercel deploy
```

## 📖 API Reference

### Deployment Sync

**POST** `/api/deployments/sync`

Sync deployment metadata to the DAO backend.

```json
{
  "project": "my-app",
  "pr_number": 123,
  "deploy_url": "https://my-app-git-feature.vercel.app",
  "status": "ready",
  "timestamp": "2024-01-15T10:30:00Z",
  "commit_sha": "abc123...",
  "branch": "feature/new-feature",
  "author": "alice"
}
```

### Deployment Status

**GET** `/api/deployments/status?deploymentId=123`

Get deployment status and voting results.

```json
{
  "deployment": {
    "id": "my-app-123",
    "project": "my-app",
    "pr_number": 123,
    "deploy_url": "https://my-app-git-feature.vercel.app",
    "status": "pending_approval",
    "votes": {
      "total": 5,
      "approvals": 4,
      "rejections": 1,
      "approvalRate": 80,
      "isApproved": true
    }
  }
}
```

### Submit Vote

**POST** `/api/dao/votes`

Submit a vote for a deployment.

```json
{
  "deploymentId": "my-app-123",
  "vote": "approve",
  "comment": "Looks good! All tests passing.",
  "voterId": "user123"
}
```

### Trigger Production Deploy

**POST** `/api/deployments/deploy`

Trigger production deployment (requires approval).

```json
{
  "deploymentId": "my-app-123",
  "project": "my-app",
  "pr_number": 123,
  "force": false
}
```

## 🗳️ DAO Governance Workflow

### 1. Deployment Detection
- Vercel creates preview deployment for PR
- Poller detects new deployment
- Metadata synced to DAO backend

### 2. Community Review
- Deployment appears in governance dashboard
- Community members can review and vote
- AI-powered code reviews (optional)

### 3. Approval Process
- Votes collected and weighted
- Approval threshold checked (default: 75%)
- Deployment status updated

### 4. Production Deployment
- Approved deployments can be promoted
- Production deployment triggered
- Status tracked and logged

## 🔧 Configuration Options

### DAO Settings

```env
# Approval threshold (percentage)
DAO_APPROVAL_THRESHOLD=75

# Minimum votes required
DAO_MIN_VOTES=3

# Voting period (milliseconds)
DAO_VOTING_PERIOD=86400000

# Enable AI reviews
ENABLE_AI_REVIEWS=true

# Auto-deployment on approval
ENABLE_AUTO_DEPLOYMENT=false
```

### Polling Configuration

```env
# Poll interval (milliseconds)
POLL_INTERVAL=300000

# Max retries on failure
MAX_RETRIES=3

# Retry delay (milliseconds)
RETRY_DELAY=30000
```

### Rate Limiting

```env
# Rate limit window (milliseconds)
RATE_LIMIT_WINDOW=900000

# Max requests per window
RATE_LIMIT_MAX_REQUESTS=100
```

## 🛠️ Development

### Adding New Services

1. Create service file in `services/`
2. Add API endpoints in `api/`
3. Update types and validation
4. Add tests and documentation

### Extending DAO Logic

```javascript
// Example: Custom voting logic
export async function submitVote(voteData) {
  // Validate voter permissions
  const voter = await validateVoter(voteData.voterId);
  
  // Apply custom voting rules
  if (voter.role === 'admin') {
    voteData.votingPower = 3;
  } else if (voter.role === 'reviewer') {
    voteData.votingPower = 2;
  } else {
    voteData.votingPower = 1;
  }
  
  // Submit vote
  return await saveVote(voteData);
}
```

### Custom Integrations

```javascript
// Example: Custom deployment provider
export async function fetchCustomDeployments() {
  // Implement custom deployment detection
  const deployments = await customApi.getDeployments();
  
  return deployments.map(deploy => ({
    id: deploy.id,
    project: deploy.project,
    pr_number: deploy.pr,
    deploy_url: deploy.url,
    status: deploy.state,
    timestamp: deploy.created_at
  }));
}
```

## 📊 Monitoring & Analytics

### Health Checks

```bash
# Check system health
curl https://your-api.vercel.app/api/health

# Check Vercel integration
curl https://your-api.vercel.app/api/health/vercel

# Check DAO backend
curl https://your-api.vercel.app/api/health/dao
```

### Metrics

The system provides various metrics:

- **Deployment Success Rate**: Percentage of successful deployments
- **Approval Rate**: Average approval rate across deployments
- **Voter Participation**: Percentage of eligible voters who participated
- **Response Times**: API response times and performance metrics
- **Error Rates**: Error rates by endpoint and service

### Logging

Comprehensive logging is available:

```javascript
// Structured logging
logger.info('Deployment processed', {
  project: 'my-app',
  pr: 123,
  status: 'approved',
  approvalRate: 85
});

// Error logging with context
logger.error('Deployment failed', {
  project: 'my-app',
  pr: 123,
  error: error.message,
  stack: error.stack
});
```

## 🔒 Security Considerations

### Access Control
- Role-based permissions for voters
- JWT-based authentication
- Rate limiting to prevent abuse

### Data Protection
- Sensitive data encrypted at rest
- Secure API communication (HTTPS)
- Audit logging for all operations

### Compliance
- PinkSync accessibility compliance
- GDPR-compliant data handling
- SOC 2 compliance ready

## 🚀 Deployment

### Vercel Deployment

```bash
# Deploy to Vercel
vercel

# Set environment variables
vercel env add VERCEL_TOKEN
vercel env add GITHUB_TOKEN
# ... other variables

# Deploy to production
vercel --prod
```

### Docker Deployment

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
EXPOSE 3000

CMD ["npm", "start"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pinkflow-dao-sync
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pinkflow-dao-sync
  template:
    metadata:
      labels:
        app: pinkflow-dao-sync
    spec:
      containers:
      - name: pinkflow-dao-sync
        image: pinkflow/dao-sync:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        # ... other environment variables
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

### Development Guidelines

- Follow TypeScript best practices
- Add comprehensive tests
- Update documentation
- Ensure PinkSync compliance
- Follow security best practices

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- **Documentation**: [Main README](../README.md)
- **Issues**: [GitHub Issues](https://github.com/360magicians/pinkflow/issues)
- **Discussions**: [GitHub Discussions](https://github.com/360magicians/pinkflow/discussions)

## 🎯 Roadmap

- [ ] **Multi-DAO Support**: Support for multiple DAO platforms
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Mobile App**: Native mobile application
- [ ] **Webhooks**: Real-time notifications
- [ ] **Plugin System**: Extensible architecture
- [ ] **Governance Templates**: Pre-built governance models

---

**Built with ❤️ by the 360 Magicians Group for decentralized deployment governance** 