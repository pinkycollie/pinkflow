# PinkFlow Architecture - Content Engine & Platform Separation

## Overview

PinkFlow uses a layered architecture with clear separation between marketing/content, platform runtime, and analytics. This design creates a self-reinforcing content flywheel where insights feed marketing content that attracts more users.

## Architecture Layers

### 1. Next.js Marketing Site (`marketing-site/`)

**Purpose**: Public-facing content engine for SEO, lead generation, and conversion

**Technology Stack**:
- Next.js 16+ with standalone output
- Tailwind CSS for styling
- TypeScript for type safety
- Static generation + Server-side rendering

**Content Types**:
- **Marketing Pages** - Features, benefits, pricing, about
- **Documentation** - Guides, API references, tutorials
- **SEO Pages** - Optimized landing pages for search visibility
- **Agency Profiles** - Public accessibility scorecards
- **Blog** - Updates, insights, community stories
- **Case Studies** - Real-world success stories with metrics
- **Landing Pages** - Targeted conversion funnels

**Deployment**:
- Next.js standalone output (self-contained)
- Docker containerizable
- Can run on: Cloud Run, Railway, Render, Fly.io, any Node.js host
- Build: `npm run build` → `.next/standalone/`
- Run: `node server.js`

**Key Features**:
- SEO optimized with metadata and OpenGraph tags
- Security headers configured
- Fast page loads with static generation
- Responsive, mobile-first design
- Accessible (WCAG 2.1 AA)

### 2. Platform Frontend (`webapp/frontend/`)

**Purpose**: Interactive platform runtime for authenticated users

**Technology Stack**:
- React 18+ with hooks
- Vite for build tooling
- TypeScript
- Tailwind CSS

**Features**:
- Role-based UI (Developer, Researcher, Contributor)
- Model testing for sign language AI
- Smart captions and audio transcription
- Visual alerts and sign recognition
- Workspace management
- Voting and governance

**Deployment**:
- Static hosting (GitHub Pages, Netlify, CDN)
- Or containerized on Cloud Run
- Build: `npm run build` → optimized static assets

### 3. Backend Services

**FastAPI Backend**:
- DeafAuth (Identity & Authentication)
- PinkSync (Real-time sync & notifications)
- FibonRose (Trust & Ethics Engine)
- 360Magicians (AI Business Agents)
- SQLAlchemy ORM with PostgreSQL/Cloud SQL

**PinkSync Node.js Service**:
- WebSocket backbone for real-time collaboration
- Multi-user workspace updates
- Presence indicators
- Notification delivery

**Deployment**:
- FastAPI services on Cloud Run
- PinkSync on Cloud Run with WebSocket support
- Cloud SQL for database

### 4. Analytics Engine (PinkFlow)

**Purpose**: Analyze repositories, generate insights, and produce data for content

**Capabilities**:
- Repo metadata collection
- Accessibility scoring
- Compliance checking
- Visualization generation
- Pattern detection
- Trust score calculation (Fibonrose)

**Data Flow**:
- Collects repo data
- Analyzes accessibility
- Generates reports
- Publishes insights to content engine

## Content Flywheel

The architecture creates a self-reinforcing cycle:

```
1. PinkFlow Analyzes
   ↓
2. Generates Insights & Scores
   ↓
3. Next.js Publishes Content
   ↓
4. SEO Attracts Visitors
   ↓
5. Visitors Convert to Users
   ↓
6. Users Generate More Data
   ↓
Back to 1. PinkFlow Analyzes
```

### Example Flow:

1. Agency runs their code through PinkFlow
2. PinkFlow generates accessibility score (85%)
3. Next.js publishes public profile page
4. Page ranks for "agency accessibility score"
5. Other agencies find page via Google
6. They sign up to get their own score
7. More data flows into PinkFlow
8. More content generated
9. Better SEO rankings
10. More signups

## Lead Capture Strategy

### Public Pages (Next.js)

**Free Content**:
- Agency name and basic score
- High-level accessibility metrics
- Partial compliance report
- "Top 10 agencies" lists
- Before/after stories

**Gated Content**:
- Full accessibility audit
- Detailed recommendations
- Historical trend data
- Competitor comparisons
- Downloadable reports

**Call-to-Action**:
- "Get Your Full Report" → Sign up required
- "Claim Your Profile" → Verification needed
- "Improve Your Score" → Platform access

### Conversion Path

```
Google Search
    ↓
Next.js Landing Page (public content)
    ↓
Interest triggered by partial data
    ↓
"See Full Report" CTA
    ↓
Platform Signup (Fresh/React)
    ↓
Full Feature Access
    ↓
Paid Subscription
```

## Deployment Architecture

### Production Setup

```
┌─────────────────────────────────────────────┐
│           CDN / Load Balancer               │
└─────────────┬───────────────────────────────┘
              │
      ┌───────┴────────┐
      │                │
┌─────▼──────┐  ┌─────▼──────────────┐
│  Next.js   │  │  Platform Frontend │
│  Marketing │  │   (Static/CDN)     │
│ (Cloud Run)│  └────────────────────┘
└────────────┘
      │
      │ API Calls
      │
┌─────▼──────────────────────────────────┐
│      Backend Services (Cloud Run)      │
│  ┌──────────┐  ┌──────────┐          │
│  │ FastAPI  │  │ PinkSync │          │
│  │ Services │  │ Node.js  │          │
│  └─────┬────┘  └─────┬────┘          │
│        │             │                │
│        └─────┬───────┘                │
└──────────────┼────────────────────────┘
               │
        ┌──────▼──────┐
        │  Cloud SQL  │
        │ (PostgreSQL)│
        └─────────────┘
```

### Environment Variables

**Marketing Site**:
```env
NEXT_PUBLIC_SITE_NAME=MBTQ.dev
NEXT_PUBLIC_SITE_DESCRIPTION=Deaf-First Innovation
NEXT_PUBLIC_PLATFORM_URL=https://app.mbtq.dev
```

**Platform Frontend**:
```env
REACT_APP_API_URL=https://api.mbtq.dev
REACT_APP_WS_URL=wss://sync.mbtq.dev
```

**Backend**:
```env
DATABASE_URL=postgresql://...
JWT_SECRET=...
GEMINI_API_KEY=...
REDIS_URL=...
```

## Security Considerations

### Next.js Marketing Site
- Security headers configured
- No sensitive data exposed
- Rate limiting on contact forms
- HTTPS enforced
- CSP headers

### Platform Frontend
- Auth tokens in httpOnly cookies
- No API keys in client code
- CORS configured properly
- XSS protection
- Input sanitization

### Backend
- JWT authentication
- API key rotation
- Database encryption at rest
- Secrets in environment variables
- Rate limiting per user/IP
- Audit logging

## Monitoring & Analytics

### Marketing Site (Next.js)
- Google Analytics / Plausible
- Page view tracking
- Conversion funnel analysis
- A/B testing support
- Core Web Vitals monitoring

### Platform Frontend
- User behavior analytics
- Feature usage tracking
- Error tracking (Sentry)
- Performance monitoring

### Backend
- Request logging
- Error tracking
- Performance metrics
- Database query monitoring
- API usage analytics

## Scaling Strategy

### Next.js Marketing
- Horizontal scaling with containers
- CDN for static assets
- Edge caching
- Image optimization
- Code splitting

### Platform Frontend
- CDN distribution
- Browser caching
- Service worker for offline
- Lazy loading components

### Backend
- Horizontal service scaling
- Database connection pooling
- Redis for caching
- Message queue for async tasks
- Load balancing

## Cost Optimization

### Marketing Site
- Static pages cached at edge
- Minimal server compute
- Pay only for dynamic pages
- Estimated: $10-50/month

### Platform
- Static hosting: $0-10/month
- Backend: Usage-based
- Database: ~$20-100/month
- Total: ~$50-200/month initially

## Migration Path

### Phase 1: Marketing Site (Current)
- ✅ Create Next.js marketing site
- ✅ Set up standalone output
- ✅ Create essential pages
- ✅ Configure SEO
- 🔄 Deploy to production
- 🔄 Set up custom domain

### Phase 2: Content Generation
- Generate agency profile pages
- Create case study content
- Build blog infrastructure
- Set up CMS (optional)

### Phase 3: Integration
- Connect to PinkFlow analytics
- Auto-generate content from data
- Implement lead capture forms
- Set up email notifications

### Phase 4: Optimization
- A/B test landing pages
- Optimize conversion funnels
- Improve SEO rankings
- Scale infrastructure

## Success Metrics

### Marketing Site
- Organic search traffic
- Page views per month
- Time on site
- Bounce rate
- Conversion rate (visitor → signup)

### Platform
- Active users
- Feature adoption rate
- User retention
- Session duration
- Feature usage

### Business
- Lead generation rate
- Cost per acquisition
- Customer lifetime value
- Monthly recurring revenue
- Net Promoter Score

## Conclusion

This architecture separates concerns effectively:
- **Next.js** handles content and marketing
- **Fresh/React** powers the interactive platform
- **PinkFlow** generates insights and data
- **Flywheel effect** drives growth

The separation allows each layer to use the best tool for its purpose while creating a cohesive user journey from discovery to conversion.
