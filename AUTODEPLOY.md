# Auto-Deploy React App System

This document describes the auto-deploy system for provisioning React apps when customers make a purchase through Stripe.

## Overview

The system automatically:
1. Receives Stripe webhook events when a buyer purchases a plan
2. Creates a private GitHub repository from a template
3. Configures repository secrets
4. Creates and deploys a Vercel project
5. Returns the app URL to the buyer

## Architecture

### Components

1. **Stripe Webhook Handler** (`app/api/stripe/webhook/route.ts`)
   - Verifies Stripe webhook signatures
   - Processes `checkout.session.completed` events
   - Triggers provisioning workflow

2. **Provisioning API** (`app/api/provision/route.ts`)
   - Creates GitHub repository from template
   - Sets repository secrets
   - Creates Vercel project
   - Deploys application

3. **GitHub Actions Workflows**
   - `ci.yml` - Pull request checks (lint, typecheck, test, build)
   - `preview.yml` - Preview deployments for PRs
   - `deploy.yml` - Production deployments
   - `release.yml` - Tag-based releases
   - `audit.yml` - Security audits (npm audit, TruffleHog)
   - `issue-ops.yml` - Slash commands for issues

## Setup Instructions

### 1. Configure Stripe

Create products and prices in Stripe Dashboard with metadata:

```json
{
  "plan": "pro",
  "template_repo": "nextjs-template"
}
```

Set up webhook endpoint in Stripe:
- URL: `https://yourdomain.com/api/stripe/webhook`
- Events: `checkout.session.completed`, `invoice.paid`

### 2. Configure GitHub App

1. Create a GitHub App with permissions:
   - Repository contents: Read & write
   - Secrets: Read & write
   - Metadata: Read-only

2. Install the app on your organization

3. Generate and download private key

4. Note the App ID and Installation ID

### 3. Configure Vercel

1. Create a Vercel project or use API
2. Get organization ID and project ID from settings
3. Create an authentication token with appropriate scope

### 4. Set Environment Variables

Copy `.env.example` to `.env.local` and fill in all values:

#### Stripe
- `STRIPE_SECRET_KEY` - Your Stripe secret key
- `STRIPE_WEBHOOK_SECRET` - Webhook signing secret
- `PRICE_ID_*` - Price IDs for different plans

#### GitHub
- `GH_APP_ID` - GitHub App ID
- `GH_APP_INSTALLATION_ID` - Installation ID
- `GH_APP_PRIVATE_KEY` - Private key (PEM format)
- `GH_TEMPLATE_OWNER` - Template repository owner
- `GH_TEMPLATE_REPO` - Template repository name
- `GH_TARGET_OWNER` - Target organization for new repos

#### Vercel
- `VERCEL_TOKEN` - Vercel authentication token
- `VERCEL_ORG_ID` - Organization ID
- `VERCEL_PROJECT_ID` - Project ID

#### Application
- `NEXT_PUBLIC_APP_NAME` - Application name
- `FIBONROSE_BASE_URL` - FibonRose trust service URL

### 5. Deploy to Vercel

```bash
npm install
npm run build
vercel --prod
```

Or connect GitHub repository to Vercel for automatic deployments.

### 6. Configure GitHub Secrets

For GitHub Actions workflows, add these secrets:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `NEXT_PUBLIC_APP_NAME`
- `FIBONROSE_BASE_URL`

## Testing

### Local Testing

1. Start the development server:
```bash
npm install
npm run dev
```

2. Use Stripe CLI to forward webhooks:
```bash
stripe login
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

3. Create a test checkout session:
```bash
stripe checkout sessions create \
  --mode=subscription \
  --customer-email test@example.com \
  --line-items price=price_test_123,quantity=1 \
  --success-url http://localhost:3000/success \
  --cancel-url http://localhost:3000/cancel \
  --metadata plan=pro template_repo=nextjs-template
```

### End-to-End Testing

1. Create a test purchase in Stripe Dashboard
2. Verify webhook is received and processed
3. Check GitHub for new repository
4. Verify Vercel deployment
5. Test the deployed application

## Security

### Best Practices

1. **Never commit secrets** - Use environment variables
2. **Verify webhook signatures** - Always validate Stripe signatures
3. **Use least privilege** - Minimal GitHub App permissions
4. **Rotate tokens** - Regularly rotate API tokens
5. **Enable branch protection** - Require reviews and status checks
6. **Use secret scanning** - Enable GitHub secret scanning
7. **Audit dependencies** - Run security audits regularly

### Branch Protection Rules

Recommended settings for main branch:
- Require pull request reviews (1+ approvals)
- Require status checks: CI, Preview, Security Audit
- Require conversation resolution
- Require linear history
- Restrict force pushes
- Require signed commits (optional)

## Monitoring and Logging

### Key Metrics

- Provisioning success rate
- Deployment time
- Webhook processing time
- Error rates

### Logging

All provisioning events are logged with:
- Customer email
- Plan type
- Repository name
- Deployment URL
- Timestamps
- Error details (if any)

## Troubleshooting

### Common Issues

1. **Webhook signature verification fails**
   - Check `STRIPE_WEBHOOK_SECRET` is correct
   - Ensure webhook endpoint is using raw body

2. **GitHub repository creation fails**
   - Verify GitHub App has correct permissions
   - Check installation token is valid
   - Ensure template repository exists

3. **Vercel deployment fails**
   - Verify Vercel token is valid
   - Check organization and project IDs
   - Ensure repository is accessible

4. **Secrets not set correctly**
   - Verify GitHub App has secrets permission
   - Check encryption is implemented correctly

## Maintenance

### Regular Tasks

1. **Weekly**
   - Review provisioning logs
   - Check for failed deployments
   - Monitor webhook health

2. **Monthly**
   - Rotate API tokens
   - Update dependencies
   - Review security scan results
   - Test end-to-end flow

3. **Quarterly**
   - Review and update documentation
   - Audit GitHub App permissions
   - Review Vercel usage and costs

## Support

For issues or questions:
- Create an issue in this repository
- Contact the platform team
- Check the troubleshooting guide

## License

TBD - License to be defined by maintainers.
