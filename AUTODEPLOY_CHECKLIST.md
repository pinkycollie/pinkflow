# Auto-Deploy Setup Checklist

Use this checklist to set up the auto-deploy system for your organization.

## Prerequisites

- [ ] Node.js 16+ installed
- [ ] GitHub organization account
- [ ] Stripe account
- [ ] Vercel account

## Stripe Configuration

- [ ] Create Stripe products for each plan (Starter, Pro, etc.)
- [ ] Add prices to each product
- [ ] Add metadata to each price:
  - [ ] `plan` - Plan identifier (e.g., "starter", "pro")
  - [ ] `template_repo` - Template repository name
- [ ] Copy price IDs to environment variables
- [ ] Create webhook endpoint in Stripe Dashboard
  - [ ] URL: `https://yourdomain.com/api/stripe/webhook`
  - [ ] Events: `checkout.session.completed`, `invoice.paid`
- [ ] Copy webhook signing secret to environment variables
- [ ] Test webhook with Stripe CLI
- [ ] Test checkout flow in test mode

## GitHub Configuration

### GitHub App

- [ ] Create GitHub App in your organization
- [ ] Configure permissions:
  - [ ] Repository contents: Read & write
  - [ ] Repository secrets: Read & write
  - [ ] Repository metadata: Read-only
- [ ] Install app on your organization
- [ ] Generate private key and download
- [ ] Note App ID
- [ ] Note Installation ID
- [ ] Store private key securely (never commit to repo)

### Template Repository

- [ ] Create template repository with Next.js app
- [ ] Add required files:
  - [ ] `package.json` with dependencies
  - [ ] `next.config.js`
  - [ ] `tsconfig.json`
  - [ ] `.env.example`
  - [ ] `.gitignore`
  - [ ] `README.md`
- [ ] Add GitHub Actions workflows:
  - [ ] `.github/workflows/ci.yml`
  - [ ] `.github/workflows/preview.yml`
  - [ ] `.github/workflows/deploy.yml`
- [ ] Mark repository as template in settings
- [ ] Test template by creating a repository from it manually

### Repository Governance

- [ ] Create `.github/CODEOWNERS` file
- [ ] Add PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
- [ ] Add issue templates:
  - [ ] Bug report (`.github/ISSUE_TEMPLATE/bug.yml`)
  - [ ] Feature request (`.github/ISSUE_TEMPLATE/feature.yml`)

### Branch Protections

- [ ] Enable branch protection on main branch
- [ ] Require pull request reviews (1+ approvals)
- [ ] Require status checks to pass:
  - [ ] CI
  - [ ] Preview (if applicable)
  - [ ] Security Audit
- [ ] Require conversation resolution
- [ ] Require linear history
- [ ] Restrict force pushes
- [ ] Restrict deletions
- [ ] Require signed commits (optional)

### Security

- [ ] Enable Dependabot alerts
- [ ] Enable Dependabot security updates
- [ ] Enable secret scanning
- [ ] Enable push protection for secrets
- [ ] Configure CodeQL analysis
- [ ] Add TruffleHog secret scanning to audit workflow

## Vercel Configuration

- [ ] Create Vercel account/organization
- [ ] Create project or prepare for API creation
- [ ] Generate authentication token
  - [ ] Token scope: appropriate for project creation
- [ ] Note organization ID
- [ ] Note project ID (if using existing project)
- [ ] Configure environment variables in Vercel:
  - [ ] `STRIPE_SECRET_KEY`
  - [ ] `STRIPE_WEBHOOK_SECRET`
  - [ ] `GH_APP_ID`
  - [ ] `GH_APP_INSTALLATION_ID`
  - [ ] `GH_APP_PRIVATE_KEY`
  - [ ] `GH_TEMPLATE_OWNER`
  - [ ] `GH_TEMPLATE_REPO`
  - [ ] `GH_TARGET_OWNER`
  - [ ] `VERCEL_TOKEN`
  - [ ] `VERCEL_ORG_ID`
  - [ ] `NEXT_PUBLIC_APP_NAME`
  - [ ] `FIBONROSE_BASE_URL`
- [ ] Configure production protection
- [ ] Set up team member roles and permissions
- [ ] Configure billing alerts

## Deployment

### Main Application

- [ ] Clone this repository
- [ ] Install dependencies: `npm install`
- [ ] Copy `.env.example` to `.env.local`
- [ ] Fill in all environment variables
- [ ] Test locally: `npm run dev`
- [ ] Test webhook endpoint with Stripe CLI
- [ ] Deploy to Vercel: `vercel --prod`
- [ ] Or connect GitHub repo to Vercel for auto-deploy
- [ ] Verify deployment is successful
- [ ] Test webhook endpoint in production

### GitHub Actions Secrets

For repositories created from template:

- [ ] Add `VERCEL_TOKEN` to GitHub organization secrets
- [ ] Add `VERCEL_ORG_ID` to GitHub organization secrets
- [ ] Add `VERCEL_PROJECT_ID` to repository secrets (per project)
- [ ] Add `NEXT_PUBLIC_APP_NAME` to repository secrets
- [ ] Add `FIBONROSE_BASE_URL` to repository secrets

## Testing

### Unit Testing

- [ ] Test Stripe webhook signature verification
- [ ] Test provisioning API with mock data
- [ ] Test GitHub API integration
- [ ] Test Vercel API integration

### Integration Testing

- [ ] Create test Stripe checkout session
- [ ] Verify webhook is received
- [ ] Verify repository is created
- [ ] Verify secrets are set
- [ ] Verify Vercel project is created
- [ ] Verify deployment succeeds
- [ ] Verify deployed app is accessible

### End-to-End Testing

- [ ] Complete full purchase flow in test mode
- [ ] Verify email notifications (if configured)
- [ ] Test subscription renewal
- [ ] Test subscription upgrade/downgrade
- [ ] Test cancellation handling

## Monitoring

- [ ] Set up logging for webhook events
- [ ] Set up logging for provisioning events
- [ ] Configure error alerting
- [ ] Set up uptime monitoring for webhook endpoint
- [ ] Configure Vercel deployment notifications
- [ ] Set up GitHub Actions notifications

## Documentation

- [ ] Update README with setup instructions
- [ ] Document environment variables
- [ ] Document API endpoints
- [ ] Document workflow architecture
- [ ] Create runbook for common issues
- [ ] Document rollback procedures
- [ ] Create customer onboarding guide

## Security Hardening

- [ ] Review all secrets and tokens
- [ ] Ensure no secrets in code or config files
- [ ] Verify webhook signature validation
- [ ] Test with invalid signatures
- [ ] Review GitHub App permissions (principle of least privilege)
- [ ] Review Vercel token scope
- [ ] Enable rate limiting on webhook endpoint
- [ ] Configure CORS policies
- [ ] Review error messages (no sensitive data exposure)
- [ ] Test authentication and authorization

## Compliance

- [ ] Review data handling practices
- [ ] Ensure GDPR compliance (if applicable)
- [ ] Document data retention policies
- [ ] Review PII handling
- [ ] Ensure accessibility standards (WCAG 2.1 Level AA)
- [ ] Document incident response procedures

## Launch Preparation

- [ ] Complete all checklist items
- [ ] Perform full end-to-end test
- [ ] Review with security team
- [ ] Review with legal team (if applicable)
- [ ] Prepare rollback plan
- [ ] Schedule launch date
- [ ] Notify stakeholders
- [ ] Prepare support documentation
- [ ] Brief support team

## Post-Launch

- [ ] Monitor initial deployments closely
- [ ] Review logs for errors
- [ ] Check webhook delivery rate
- [ ] Monitor provisioning success rate
- [ ] Collect user feedback
- [ ] Document lessons learned
- [ ] Schedule first maintenance review

## Maintenance Schedule

### Daily
- [ ] Check webhook health
- [ ] Review error logs

### Weekly
- [ ] Review provisioning metrics
- [ ] Check deployment success rates
- [ ] Review security scan results

### Monthly
- [ ] Update dependencies
- [ ] Rotate API tokens
- [ ] Review and update documentation
- [ ] Audit access permissions

### Quarterly
- [ ] Full security audit
- [ ] Review and update workflows
- [ ] Review costs and optimize
- [ ] Update disaster recovery plan

## Support Resources

- [ ] Create internal knowledge base
- [ ] Document escalation procedures
- [ ] Set up on-call rotation (if needed)
- [ ] Prepare FAQ for common issues
- [ ] Create troubleshooting guide

## Completion

- [ ] All checklist items completed
- [ ] Documented completion date
- [ ] Documented by (name/team)
- [ ] Reviewed and approved by (name/role)

---

**Completion Date:** _______________

**Completed By:** _______________

**Reviewed By:** _______________

**Approved By:** _______________
