# Integration Guide: Stripe → GitHub → Hosting

This guide walks through integrating all components of the auto-deploy system.

## Overview

The auto-deploy system connects core services and optional hosting providers:
1. **Stripe** - Handles payments and triggers webhooks (required)
2. **GitHub** - Creates repositories and manages code (required)
3. **Vercel** - Hosts and deploys applications (optional)

## Architecture Flow

```
Customer Purchase (Stripe)
    ↓
Webhook Event (checkout.session.completed)
    ↓
PinkFlow API (app/api/stripe/webhook/route.ts)
    ↓
Verify Signature & Parse Metadata
    ↓
Provision API (app/api/provision/route.ts)
    ↓
┌─────────────────────┬───────────────────────┬──────────────────────────┐
│                     │                       │                          │
Create GitHub Repo    Set Repo Secrets    Optional: Create Hosting     │
(from template)       (optional)          Project & Deploy             │
│                     │                       │                          │
└─────────────────────┴───────────────────────┴──────────────────────────┘
    ↓
Return App URL to Customer (if deployment enabled)
```

## Step-by-Step Integration

### Phase 1: Stripe Setup

#### 1.1 Create Products

In Stripe Dashboard:

1. Go to Products
2. Click "Add product"
3. Fill in details:
   - Name: "Starter Plan"
   - Description: Plan details
   - Pricing: Set up recurring or one-time pricing

4. Add metadata to the **Price** (not the product):
   ```json
   {
     "plan": "starter",
     "template_repo": "nextjs-template"
   }
   ```

5. Copy the Price ID (starts with `price_`)

Repeat for each plan (Pro, Enterprise, etc.)

#### 1.2 Configure Webhook

1. Go to Developers → Webhooks
2. Click "Add endpoint"
3. Enter endpoint URL:
   - Test: Use Stripe CLI forward (see testing section)
   - Production: `https://yourdomain.com/api/stripe/webhook`

4. Select events to listen for:
   - `checkout.session.completed`
   - `invoice.paid` (for subscriptions)

5. Copy the signing secret (starts with `whsec_`)

#### 1.3 Test with Stripe CLI

Install Stripe CLI:
```bash
# macOS
brew install stripe/stripe-cli/stripe

# Other platforms
# Download from https://stripe.com/docs/stripe-cli
```

Login and forward webhooks:
```bash
stripe login
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

Create test checkout:
```bash
stripe checkout sessions create \
  --mode=subscription \
  --customer-email test@example.com \
  --line-items price=price_YOUR_PRICE_ID,quantity=1 \
  --success-url http://localhost:3000/success \
  --cancel-url http://localhost:3000/cancel \
  --metadata plan=starter \
  --metadata template_repo=nextjs-template
```

### Phase 2: GitHub App Setup

#### 2.1 Create GitHub App

1. Go to Organization Settings → Developer settings → GitHub Apps
2. Click "New GitHub App"
3. Fill in details:
   - **GitHub App name**: "PinkFlow Provisioner"
   - **Homepage URL**: Your organization URL
   - **Webhook**: Uncheck "Active" (not needed for this app)

4. Set permissions:
   - Repository permissions:
     - Contents: Read & write
     - Metadata: Read-only
     - Secrets: Read & write (if setting repo secrets)

5. Choose where it can be installed:
   - Select "Only on this account"

6. Click "Create GitHub App"

#### 2.2 Install GitHub App

1. After creation, click "Install App"
2. Select your organization
3. Choose repositories:
   - Select "All repositories" or specific repos
4. Click "Install"

5. Note the installation ID from the URL:
   `https://github.com/settings/installations/XXXXX`

#### 2.3 Generate Private Key

1. In GitHub App settings, scroll to "Private keys"
2. Click "Generate a private key"
3. Download the `.pem` file
4. Store securely - you'll need this for environment variables

#### 2.4 Create Template Repository

1. Create a new repository in your organization
2. Copy files from `template-nextjs-app/` directory
3. Go to repository Settings
4. Check "Template repository"
5. Test by clicking "Use this template" manually

### Phase 3: Vercel Setup (Optional)

**Note:** This phase is optional. If you want to enable automatic Vercel deployments, follow these steps and set `ENABLE_VERCEL_DEPLOY=true` in your environment variables.

#### 3.1 Create Vercel Organization

1. Sign up at vercel.com
2. Create a team/organization
3. Note your team/org ID:
   - Go to Settings → General
   - Find "Team ID" or "Organization ID"

#### 3.2 Generate API Token

1. Go to Settings → Tokens
2. Click "Create"
3. Name: "PinkFlow Provisioner"
4. Scope: Full access or create with specific permissions
5. Expiration: Set based on security policy
6. Copy token immediately (only shown once)

#### 3.3 Create Base Project (Optional)

You can create a base project to test, or let the system create projects automatically.

For manual testing:
1. Click "Add New Project"
2. Import your template repository
3. Configure build settings
4. Note the Project ID from Settings → General

### Phase 4: PinkFlow Deployment

#### 4.1 Configure Environment Variables

Create `.env.local` with all values:

```bash
# Stripe
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
PRICE_ID_STARTER=price_xxx
PRICE_ID_PRO=price_xxx

# GitHub App
GH_APP_ID=123456
GH_APP_INSTALLATION_ID=987654
GH_APP_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nXXX\n-----END PRIVATE KEY-----"
GH_TEMPLATE_OWNER=your-org
GH_TEMPLATE_REPO=nextjs-template
GH_TARGET_OWNER=your-org

# Vercel (Optional - only if ENABLE_VERCEL_DEPLOY=true)
ENABLE_VERCEL_DEPLOY=false
VERCEL_TOKEN=xxx
VERCEL_ORG_ID=team_xxx
VERCEL_PROJECT_ID=prj_xxx

# App
NEXT_PUBLIC_APP_NAME=JobMagician
NEXT_PUBLIC_BASE_URL=http://localhost:3000
FIBONROSE_BASE_URL=https://trust.yourdomain.com
```

#### 4.2 Test Locally

```bash
npm install
npm run dev
```

In another terminal, forward Stripe webhooks:
```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook
```

Create a test checkout and verify:
- Webhook is received
- Repository is created
- If Vercel is enabled, verify project is created and deployment succeeds

#### 4.3 Deploy to Production

You can deploy this application to any hosting platform. Here are two common options:

**Option A: Deploy to Vercel**
```bash
npm run build
vercel --prod
```

**Option B: Connect GitHub to Vercel**
1. Go to vercel.com
2. Click "Import Project"
3. Select this repository
4. Configure build settings
5. Add all environment variables in Settings → Environment Variables
6. Deploy

**Option C: Other Hosting Platforms**

This is a standard Next.js application and can be deployed to any platform that supports Node.js applications (e.g., AWS, Azure, Google Cloud, Railway, Render, etc.).

#### 4.4 Configure Production Webhook

1. Update Stripe webhook endpoint to production URL
2. Copy new webhook signing secret
3. Update `STRIPE_WEBHOOK_SECRET` in Vercel environment variables
4. Redeploy

### Phase 5: GitHub Actions Configuration

#### 5.1 Add Organization Secrets

Go to Organization Settings → Secrets and variables → Actions:

1. Add secrets that apply to all repositories:
   - `NEXT_PUBLIC_APP_NAME`
   - `FIBONROSE_BASE_URL`

2. If using Vercel deployment, also add:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`

3. Repository-specific secrets (added per provisioned repo):
   - `VERCEL_PROJECT_ID` (unique per project, if using Vercel)

#### 5.2 Test Workflows

Create a test repository from template:

1. Verify CI runs on pull requests
2. Check preview deployments work
3. Test production deployment on merge to main
4. Verify security audit runs

### Phase 6: Monitoring & Operations

#### 6.1 Set Up Monitoring

1. **Stripe Dashboard**
   - Monitor webhook delivery success rate
   - Set up alerts for failed webhooks

2. **GitHub**
   - Enable Actions notifications
   - Monitor repository creation rate
   - Set up alerts for failed workflows

3. **Hosting Platform** (if enabled)
   - Monitor deployment success rate
   - Set up build alerts
   - Configure budget alerts

#### 6.2 Create Runbook

Document procedures for:
- Webhook failures
- Provisioning failures
- Deployment failures
- Secret rotation
- Emergency rollback

#### 6.3 Set Up Logging

Configure centralized logging:
```typescript
// Add to provisioning code
console.log(JSON.stringify({
  event: 'provisioning_started',
  timestamp: new Date().toISOString(),
  customerEmail: session.customer_email,
  plan: plan,
  correlationId: session.id
}));
```

Use correlation IDs to track requests across services.

## Testing Checklist

### Pre-Launch Testing

- [ ] Stripe test mode checkout completes successfully
- [ ] Webhook signature verification works
- [ ] Repository created from template
- [ ] Repository is private
- [ ] Secrets are set (if configured)
- [ ] If Vercel enabled: project created and first deployment succeeds
- [ ] If Vercel enabled: app URL is accessible
- [ ] CI workflow runs on PRs
- [ ] Preview deployments work (if configured)
- [ ] Production deployment works (if configured)
- [ ] Security audit runs
- [ ] Error handling works (test with invalid data)

### Production Testing

- [ ] Production webhook endpoint is accessible
- [ ] HTTPS/TLS configured correctly
- [ ] Real purchase flow works end-to-end
- [ ] Customer receives app URL
- [ ] All monitoring is in place
- [ ] Alert notifications work
- [ ] Documentation is complete

## Troubleshooting

### Webhook Issues

**Webhook not received**
- Check Stripe Dashboard → Developers → Webhooks → Attempts
- Verify endpoint URL is correct and accessible
- Check firewall/security rules

**Signature verification fails**
- Verify webhook secret matches Stripe Dashboard
- Ensure request body is raw (not parsed)
- Check that secret is for correct environment (test/live)

**Webhook times out**
- Provisioning takes too long (>30 seconds)
- Consider async processing with queue
- Return 200 immediately, process in background

### GitHub Issues

**Repository creation fails**
- Verify GitHub App permissions
- Check installation token is valid
- Ensure template repository exists
- Verify template is marked as template

**Template not found**
- Check `GH_TEMPLATE_OWNER` and `GH_TEMPLATE_REPO`
- Verify GitHub App has access to template
- Try manual "Use this template" to test

**Secrets not set**
- Verify GitHub App has secrets permission
- Check encryption is implemented correctly
- Use GitHub API to verify secret was set

### Vercel Issues (If Enabled)

**Note:** These issues only apply if `ENABLE_VERCEL_DEPLOY=true`

**Project creation fails**
- Verify `ENABLE_VERCEL_DEPLOY` is set to `true`
- Verify Vercel token is valid
- Check organization/team ID is correct
- Ensure repository is accessible to Vercel
- Review Vercel usage limits

**Deployment fails**
- Check build settings in project
- Verify environment variables are set
- Review deployment logs in Vercel Dashboard
- Test build locally: `npm run build`

**Environment variables not set**
- Use correct API endpoint for env vars
- Verify token has appropriate scope
- Check target (production/preview/development)
- Review Vercel API response for errors

## Security Considerations

### Secrets Management

1. **Never commit secrets**
   - Use environment variables only
   - Add `.env*` to `.gitignore`
   - Use Vercel encrypted variables

2. **Rotate regularly**
   - Stripe keys: quarterly
   - GitHub App key: annually
   - Hosting platform tokens: quarterly (if used)

3. **Use least privilege**
   - Minimal GitHub App permissions
   - Scoped hosting platform tokens (if used)
   - Restricted Stripe API keys

### Network Security

1. **HTTPS only**
   - All webhooks over HTTPS
   - TLS 1.2 or higher

2. **Signature verification**
   - Always verify Stripe signatures
   - Reject unsigned requests

3. **Rate limiting**
   - Implement on webhook endpoint
   - Prevent abuse

### Access Control

1. **Team permissions**
   - Limit who can view secrets
   - Audit access regularly
   - Remove departed members immediately

2. **Repository permissions**
   - Created repos are private by default
   - Add collaborators explicitly
   - Use teams for access management

## Support Resources

- [Stripe API Documentation](https://stripe.com/docs/api)
- [GitHub Apps Documentation](https://docs.github.com/en/apps)
- [Vercel API Documentation](https://vercel.com/docs/rest-api) (if using Vercel)
- [PinkFlow Repository](https://github.com/pinkycollie/pinkflow)

## Next Steps

After successful integration:

1. [ ] Document your specific configuration
2. [ ] Train team on operations
3. [ ] Set up monitoring dashboards
4. [ ] Schedule regular maintenance
5. [ ] Plan for scaling (if needed)
6. [ ] Collect customer feedback
7. [ ] Iterate and improve

## License

TBD - License to be defined by maintainers.
