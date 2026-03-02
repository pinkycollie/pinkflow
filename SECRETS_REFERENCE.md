# Secrets & Environment Variables Reference

This document provides a comprehensive reference for all secrets and environment variables required for the auto-deploy system.

## Environment Variables Table

| Service | Key / ID | Description | Example Value | Where to Store |
|---------|----------|-------------|---------------|----------------|
| **Stripe** |
| Stripe | `STRIPE_SECRET_KEY` | Stripe API secret key | `sk_live_xxx` or `sk_test_xxx` | Vercel env + GitHub secret |
| Stripe | `STRIPE_WEBHOOK_SECRET` | Webhook signing secret | `whsec_xxx` | Vercel env |
| Stripe | `PRICE_ID_STARTER` | Starter plan price ID | `price_xxx` | Vercel env |
| Stripe | `PRICE_ID_PRO` | Pro plan price ID | `price_xxx` | Vercel env |
| Stripe | `PRICE_ID_ENTERPRISE` | Enterprise plan price ID | `price_xxx` | Vercel env |
| **GitHub App** |
| GitHub | `GH_APP_ID` | GitHub App ID | `123456` | Vercel env |
| GitHub | `GH_APP_INSTALLATION_ID` | Installation ID for your org | `987654` | Vercel env |
| GitHub | `GH_APP_PRIVATE_KEY` | GitHub App private key (PEM) | `-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----` | Vercel encrypted env |
| GitHub | `GH_APP_INSTALLATION_TOKEN` | Installation token (alternative) | `ghs_xxx` | Vercel env (if not using private key) |
| **GitHub Configuration** |
| GitHub | `GH_TEMPLATE_OWNER` | Template repo owner | `your-org` | Vercel env |
| GitHub | `GH_TEMPLATE_REPO` | Template repo name | `nextjs-template` | Vercel env |
| GitHub | `GH_TARGET_OWNER` | Target org for new repos | `your-org` | Vercel env |
| **Vercel** |
| Vercel | `VERCEL_TOKEN` | Vercel API token | `vercel_token_xxx` | GitHub secret |
| Vercel | `VERCEL_ORG_ID` | Vercel organization ID | `org_xxx` or `team_xxx` | Vercel env + GitHub secret |
| Vercel | `VERCEL_PROJECT_ID` | Vercel project ID | `prj_xxx` | Vercel env + GitHub secret |
| **Application** |
| App | `NEXT_PUBLIC_APP_NAME` | Application display name | `JobMagician` | Vercel env + GitHub secret |
| App | `NEXT_PUBLIC_BASE_URL` | Base URL of the app | `https://yourdomain.com` | Vercel env |
| **FibonRose Trust** |
| Trust | `FIBONROSE_BASE_URL` | FibonRose API base URL | `https://trust.yourdomain.com` | Vercel env + GitHub secret |

## Detailed Descriptions

### Stripe Configuration

#### STRIPE_SECRET_KEY
**Required:** Yes  
**Type:** Secret  
**Format:** `sk_test_xxx` (test) or `sk_live_xxx` (production)

Your Stripe API secret key. Use test key for development and live key for production.

**How to get:**
1. Log in to Stripe Dashboard
2. Go to Developers → API keys
3. Copy "Secret key"

**Security:** Never commit to repository. Store in Vercel environment variables and use different keys for test/production environments.

#### STRIPE_WEBHOOK_SECRET
**Required:** Yes  
**Type:** Secret  
**Format:** `whsec_xxx`

Webhook signing secret for verifying webhook events from Stripe.

**How to get:**
1. Log in to Stripe Dashboard
2. Go to Developers → Webhooks
3. Add endpoint or view existing endpoint
4. Copy "Signing secret"

**Security:** Different secret for each environment (test/production). Store in Vercel environment variables.

#### PRICE_ID_* (STARTER, PRO, ENTERPRISE)
**Required:** Yes (at least one)  
**Type:** Configuration  
**Format:** `price_xxx`

Price IDs for different subscription tiers.

**How to get:**
1. Log in to Stripe Dashboard
2. Go to Products
3. Click on a product
4. Copy the price ID for each pricing option

**Note:** Add metadata to each price:
```json
{
  "plan": "pro",
  "template_repo": "nextjs-template"
}
```

### GitHub App Configuration

#### GH_APP_ID
**Required:** Yes  
**Type:** Configuration  
**Format:** Numeric ID

Your GitHub App's unique identifier.

**How to get:**
1. Go to GitHub Settings → Developer settings → GitHub Apps
2. Select your app
3. Find "App ID" near the top

#### GH_APP_INSTALLATION_ID
**Required:** Yes  
**Type:** Configuration  
**Format:** Numeric ID

Installation ID for your organization.

**How to get:**
1. Install GitHub App on your organization
2. Go to Settings → Installations
3. Click "Configure" on your app
4. Check URL: `https://github.com/settings/installations/XXXXX` (XXXXX is the installation ID)

Or use API:
```bash
curl -H "Authorization: Bearer YOUR_JWT" \
  https://api.github.com/app/installations
```

#### GH_APP_PRIVATE_KEY
**Required:** Yes (if not using installation token directly)  
**Type:** Secret  
**Format:** PEM format private key

Private key for generating installation tokens.

**How to get:**
1. Go to your GitHub App settings
2. Scroll to "Private keys"
3. Click "Generate a private key"
4. Download the .pem file

**Security:** Store in Vercel encrypted environment variables. Never commit to repository. Use newline escape (`\n`) when storing as string.

**Format for environment variable:**
```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
-----END PRIVATE KEY-----
```

Store as single line with `\n`:
```
-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----
```

#### GH_APP_INSTALLATION_TOKEN
**Required:** Alternative to private key  
**Type:** Secret  
**Format:** `ghs_xxx`

Pre-generated installation token (expires after 1 hour by default).

**How to get:**
```bash
# Generate JWT from private key, then:
curl -X POST \
  -H "Authorization: Bearer YOUR_JWT" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/app/installations/INSTALLATION_ID/access_tokens
```

**Note:** Tokens expire. Consider using private key instead for automatic token generation.

### GitHub Repository Configuration

#### GH_TEMPLATE_OWNER
**Required:** Yes  
**Type:** Configuration  
**Format:** GitHub username or organization name

Owner of the template repository.

**Example:** `my-org`

#### GH_TEMPLATE_REPO
**Required:** Yes  
**Type:** Configuration  
**Format:** Repository name

Name of the template repository to use for provisioning.

**Example:** `nextjs-template`

**Note:** Repository must be marked as a template in GitHub settings.

#### GH_TARGET_OWNER
**Required:** Yes  
**Type:** Configuration  
**Format:** GitHub username or organization name

Organization where new repositories will be created.

**Example:** `my-org` (can be same as template owner)

### Vercel Configuration

#### VERCEL_TOKEN
**Required:** Yes  
**Type:** Secret  
**Format:** Long alphanumeric string

Vercel API authentication token.

**How to get:**
1. Log in to Vercel
2. Go to Settings → Tokens
3. Create a new token with appropriate scope
4. Copy the token immediately (only shown once)

**Security:** Store in GitHub secrets for Actions workflows. Different token for different environments recommended.

#### VERCEL_ORG_ID
**Required:** Yes  
**Type:** Configuration  
**Format:** `org_xxx` or `team_xxx`

Your Vercel organization or team ID.

**How to get:**
1. Log in to Vercel
2. Go to Settings → General
3. Find "Team ID" or "Organization ID"

Or via API:
```bash
curl -H "Authorization: Bearer VERCEL_TOKEN" \
  https://api.vercel.com/v2/teams
```

#### VERCEL_PROJECT_ID
**Required:** Yes (for existing projects)  
**Type:** Configuration  
**Format:** `prj_xxx`

Vercel project identifier.

**How to get:**
1. Go to your project in Vercel
2. Go to Settings
3. Find "Project ID"

Or via API:
```bash
curl -H "Authorization: Bearer VERCEL_TOKEN" \
  https://api.vercel.com/v9/projects
```

**Note:** For auto-provisioning, new projects will have their own project IDs.

### Application Configuration

#### NEXT_PUBLIC_APP_NAME
**Required:** Yes  
**Type:** Configuration  
**Format:** String

Display name for the application.

**Example:** `JobMagician`

**Note:** Prefix `NEXT_PUBLIC_` makes it available to client-side code.

#### NEXT_PUBLIC_BASE_URL
**Required:** Yes  
**Type:** Configuration  
**Format:** URL

Base URL of your deployed application.

**Example:** `https://yourdomain.com`

**Note:** Used for generating webhook callbacks and links.

### FibonRose Trust

#### FIBONROSE_BASE_URL
**Required:** Optional  
**Type:** Configuration  
**Format:** URL

Base URL for FibonRose trust verification service.

**Example:** `https://trust.yourdomain.com`

**Note:** Used for creating verified deployment events and trust scoring.

## Security Best Practices

### Storage Guidelines

1. **Never commit secrets to repository**
   - Use `.env.local` for local development
   - Add `.env*` to `.gitignore`

2. **Use environment-specific secrets**
   - Different keys for development, staging, production
   - Rotate regularly

3. **Principle of least privilege**
   - Minimal scopes for tokens
   - Limited permissions for GitHub App
   - Restricted Vercel team roles

4. **Encryption at rest**
   - Use Vercel encrypted environment variables for sensitive data
   - Use GitHub encrypted secrets

5. **Regular rotation**
   - Rotate API tokens monthly
   - Regenerate webhook secrets quarterly
   - Update GitHub App keys annually

### Access Control

1. **Limit access to secrets**
   - Only platform team can view/edit production secrets
   - Use Vercel team permissions
   - Use GitHub organization secrets for shared values

2. **Audit access**
   - Review who has access to secrets monthly
   - Log secret access when possible
   - Remove access for departed team members immediately

3. **Monitor usage**
   - Set up alerts for unusual API usage
   - Monitor webhook delivery failures
   - Track provisioning failures

## Troubleshooting

### Common Issues

#### Invalid Stripe signature
- Check `STRIPE_WEBHOOK_SECRET` matches Stripe Dashboard
- Ensure webhook endpoint receives raw body
- Verify webhook secret is for correct environment (test/live)

#### GitHub API authentication fails
- Verify `GH_APP_ID` and `GH_APP_INSTALLATION_ID` are correct
- Check private key format (PEM with proper newlines)
- Ensure GitHub App is installed on organization
- Verify GitHub App has required permissions

#### Vercel deployment fails
- Check `VERCEL_TOKEN` is valid and not expired
- Verify `VERCEL_ORG_ID` is correct
- Ensure token has appropriate scope
- Check Vercel usage limits

#### Repository creation fails
- Verify template repository exists and is marked as template
- Check `GH_TEMPLATE_OWNER` and `GH_TEMPLATE_REPO` values
- Ensure GitHub App has repository creation permission
- Verify target organization allows repository creation

## Migration Notes

### Moving from Test to Production

1. Update all Stripe keys to live mode
2. Create production webhook endpoint
3. Generate new GitHub App for production (or use same with caution)
4. Create separate Vercel project for production
5. Use separate environment in Vercel (production vs. preview)
6. Update all environment variables in production environment
7. Test end-to-end before going live

### Rotating Secrets

#### Stripe Keys
1. Generate new secret key in Stripe Dashboard
2. Update in Vercel immediately
3. Test webhook endpoint
4. Revoke old key after verification

#### GitHub App Private Key
1. Generate new private key in GitHub App settings
2. Update in Vercel immediately
3. Test provisioning workflow
4. Delete old key file after verification

#### Vercel Token
1. Generate new token in Vercel settings
2. Update in GitHub secrets immediately
3. Test deployment workflow
4. Revoke old token after verification

## Backup and Recovery

### Backup Procedures

1. **Document all secret locations**
   - Keep encrypted backup of all keys and secrets
   - Store in secure password manager (1Password, LastPass, etc.)
   - Document access procedures

2. **Test recovery procedures**
   - Quarterly test of secret restoration
   - Document recovery time objectives
   - Verify backup completeness

3. **Disaster recovery plan**
   - Document steps to regenerate all secrets
   - List dependencies and order of recovery
   - Test full system recovery annually

## Support

For questions or issues with secrets management:
- Contact platform team
- Review security policy: [SECURITY.md](SECURITY.md)
- Create private security advisory for sensitive issues

## License

TBD - License to be defined by maintainers.
