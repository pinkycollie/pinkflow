# Auto-Deploy System Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Customer Journey                            │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │   Customer Checkout   │
                        │   (Stripe Payment)    │
                        └───────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Stripe Platform                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  checkout.session.completed                                  │    │
│  │  - Customer Email                                            │    │
│  │  - Price ID                                                  │    │
│  │  - Metadata: {plan: "pro", template_repo: "nextjs-template"}│    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     PinkFlow Next.js Application                     │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  /api/stripe/webhook                                         │    │
│  │  1. Verify Stripe signature                                  │    │
│  │  2. Parse event data                                         │    │
│  │  3. Extract metadata (plan, template_repo)                   │    │
│  │  4. Call /api/provision                                      │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                    │                                 │
│                                    ▼                                 │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  /api/provision                                              │    │
│  │  1. Authenticate with GitHub App                             │    │
│  │  2. Create repository from template                          │    │
│  │  3. Set repository secrets                                   │    │
│  │  4. Create Vercel project                                    │    │
│  │  5. Trigger deployment                                       │    │
│  │  6. Return app URL                                           │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                   │                │                │
          ┌────────┘                │                └────────┐
          ▼                         ▼                         ▼
┌───────────────────┐  ┌────────────────────┐  ┌──────────────────────┐
│  GitHub Platform  │  │  Vercel Platform   │  │  Customer Receives   │
│                   │  │                    │  │                      │
│ ┌───────────────┐ │  │ ┌────────────────┐ │  │ - Repository URL     │
│ │ New Repo      │ │  │ │ New Project    │ │  │ - Deployment URL     │
│ │ - From template│ │  │ │ - Env vars set │ │  │ - Access granted     │
│ │ - Private     │ │  │ │ - Deployed     │ │  │                      │
│ │ - Secrets set │ │  │ │ - Production   │ │  │                      │
│ └───────────────┘ │  │ └────────────────┘ │  └──────────────────────┘
│                   │  │                    │
│ ┌───────────────┐ │  │ ┌────────────────┐ │
│ │ Actions       │ │  │ │ Automatic      │ │
│ │ - CI on PRs   │ │  │ │ - Preview      │ │
│ │ - Deploy main │ │  │ │ - Production   │ │
│ │ - Security    │ │  │ │ - Monitoring   │ │
│ └───────────────┘ │  │ └────────────────┘ │
└───────────────────┘  └────────────────────┘
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────────────────┐
│                        External Services                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Stripe                    GitHub                    Vercel           │
│  ┌─────────┐              ┌─────────┐              ┌─────────┐      │
│  │Webhooks │──────────────▶│ App     │◀─────────────│  API    │      │
│  │Products │              │ API     │              │Projects │      │
│  │Prices   │              │Template │              │Deploy   │      │
│  └─────────┘              └─────────┘              └─────────┘      │
│       │                        │                         │           │
└───────┼────────────────────────┼─────────────────────────┼───────────┘
        │                        │                         │
        ▼                        ▼                         ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        PinkFlow Application                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐    ┌──────────────────┐   ┌─────────────────┐│
│  │ Webhook Handler  │    │ Provision API    │   │ Configuration   ││
│  ├──────────────────┤    ├──────────────────┤   ├─────────────────┤│
│  │ - Verify sig     │───▶│ - GitHub create  │   │ - Env vars      ││
│  │ - Parse event    │    │ - Set secrets    │◀──│ - Credentials   ││
│  │ - Trigger flow   │    │ - Vercel deploy  │   │ - Templates     ││
│  └──────────────────┘    └──────────────────┘   └─────────────────┘│
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
        │                        │                         │
        ▼                        ▼                         ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        Provisioned Resources                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  New Repository                 Vercel Project           Customer     │
│  ┌─────────────┐               ┌──────────────┐        ┌──────────┐ │
│  │ - Code      │──────────────▶│ - Build      │───────▶│ App URL  │ │
│  │ - Workflows │               │ - Deploy     │        │ Access   │ │
│  │ - Secrets   │               │ - Monitor    │        └──────────┘ │
│  └─────────────┘               └──────────────┘                      │
│        │                                │                            │
│        ▼                                ▼                            │
│  ┌─────────────┐               ┌──────────────┐                     │
│  │ CI/CD       │               │ Production   │                     │
│  │ - Test      │               │ - Live       │                     │
│  │ - Preview   │               │ - Monitored  │                     │
│  │ - Deploy    │               │ - Secured    │                     │
│  └─────────────┘               └──────────────┘                     │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Customer Purchase
    │
    ├─> Stripe creates checkout session
    │   └─> Metadata: {plan, template_repo}
    │
    ├─> Payment successful
    │   └─> Webhook: checkout.session.completed
    │
    ├─> PinkFlow receives webhook
    │   ├─> Verify signature (security)
    │   ├─> Parse metadata
    │   └─> Extract: email, plan, template
    │
    ├─> Provision API called
    │   ├─> GitHub: Create repo from template
    │   │   ├─> Repository name: {plan}-{timestamp}
    │   │   ├─> Visibility: Private
    │   │   └─> Secrets: NEXT_PUBLIC_APP_NAME, etc.
    │   │
    │   ├─> Vercel: Create project
    │   │   ├─> Link to GitHub repo
    │   │   ├─> Set environment variables
    │   │   └─> Trigger first deployment
    │   │
    │   └─> Return: {repo_url, deployment_url}
    │
    └─> Customer receives
        ├─> Repository access (GitHub)
        ├─> Live application URL (Vercel)
        └─> Configured CI/CD (GitHub Actions)
```

## Security Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      Security Measures                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Webhook Verification                                         │
│     ┌──────────────────────────────────────────────┐           │
│     │ Stripe Signature → Verify → Reject if invalid│           │
│     └──────────────────────────────────────────────┘           │
│                                                                  │
│  2. Authentication                                               │
│     ┌──────────────────────────────────────────────┐           │
│     │ GitHub App → JWT Token → Installation Token  │           │
│     │ Vercel API → Bearer Token → Scoped Access    │           │
│     └──────────────────────────────────────────────┘           │
│                                                                  │
│  3. Secrets Management                                           │
│     ┌──────────────────────────────────────────────┐           │
│     │ Environment Variables → Encrypted at Rest     │           │
│     │ No Secrets in Code → All in Vercel/GitHub   │           │
│     │ Rotation Policy → Monthly/Quarterly          │           │
│     └──────────────────────────────────────────────┘           │
│                                                                  │
│  4. Repository Security                                          │
│     ┌──────────────────────────────────────────────┐           │
│     │ Private by Default → Access Control          │           │
│     │ Branch Protection → Required Reviews         │           │
│     │ Status Checks → CI Must Pass                 │           │
│     └──────────────────────────────────────────────┘           │
│                                                                  │
│  5. CI/CD Security                                               │
│     ┌──────────────────────────────────────────────┐           │
│     │ Minimal Permissions → Read-only by Default   │           │
│     │ Secret Scanning → TruffleHog Weekly          │           │
│     │ Dependency Audit → npm audit on PRs          │           │
│     │ CodeQL Analysis → Automated Security Scan    │           │
│     └──────────────────────────────────────────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```
