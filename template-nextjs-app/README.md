# Auto-Provisioned Next.js App

This application was automatically provisioned through PinkFlow's auto-deploy system.

## Overview

This is a Next.js application configured with:
- TypeScript support
- Vercel deployment
- GitHub Actions CI/CD
- Security scanning
- Accessibility features

## Getting Started

### Prerequisites

- Node.js 16 or higher
- npm or yarn

### Installation

1. Clone this repository
2. Copy `.env.example` to `.env.local`
3. Fill in required environment variables
4. Install dependencies:

```bash
npm install
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

### Building

Build the application for production:

```bash
npm run build
```

### Testing

Run tests:

```bash
npm test
```

Run linter:

```bash
npm run lint
```

Type checking:

```bash
npm run typecheck
```

## Deployment

This application is automatically deployed to Vercel when changes are pushed to the main branch.

### Environment Variables

Configure these in Vercel Project Settings:

- `NEXT_PUBLIC_APP_NAME` - Your application name
- `FIBONROSE_BASE_URL` - FibonRose trust service URL
- `PLAN` - Your subscription plan
- `CUSTOMER_EMAIL` - Your email address

## Configuration

### App Configuration

Edit `app/config.ts` to customize your application:
- Application name
- Theme colors
- Feature flags

### Branding

Update branding assets in the `public/` directory:
- `favicon.ico` - Browser tab icon
- `logo.svg` - Application logo

### Styling

This app uses Tailwind CSS. Configuration is in `tailwind.config.ts`.

## Features

### Built-in Features

- ✅ TypeScript support
- ✅ ESLint configuration
- ✅ Automatic deployments
- ✅ Preview deployments for PRs
- ✅ Security scanning
- ✅ Dependency updates via Dependabot

### Accessibility

This application follows WCAG 2.1 Level AA guidelines:
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader support

## GitHub Actions Workflows

### CI (ci.yml)
Runs on every pull request:
- Linting
- Type checking
- Tests
- Build verification

### Preview (preview.yml)
Creates preview deployments for pull requests.

### Deploy (deploy.yml)
Deploys to production on push to main branch.

### Security Audit (audit.yml)
Runs weekly security scans:
- npm audit
- Secret scanning with TruffleHog

## Support

### Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [PinkFlow Documentation](https://github.com/pinkycollie/pinkflow)

### Getting Help
- Create an issue in this repository
- Contact your support team
- Refer to the [Coaches & Specialists Network](https://www.notion.so/b3232d553824475593455090a7c49b8f)

### Reporting Bugs
Use the bug report template in `.github/ISSUE_TEMPLATE/bug.yml`

### Requesting Features
Use the feature request template in `.github/ISSUE_TEMPLATE/feature.yml`

## Contributing

### Development Workflow

1. Create a feature branch from `main`
2. Make your changes
3. Run tests and linting
4. Create a pull request
5. Wait for review and CI checks
6. Merge when approved

### Code Standards

- Use TypeScript for type safety
- Follow ESLint rules
- Write meaningful commit messages
- Add tests for new features
- Update documentation

## License

TBD - License to be defined by maintainers.

## Acknowledgments

Provisioned by PinkFlow - Part of the MBTQ.dev Deaf-First Innovation Ecosystem.

**Built with ❤️ by the Deaf-First community**
