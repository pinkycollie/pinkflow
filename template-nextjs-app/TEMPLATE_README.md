# Next.js Template Repository

This is a template repository for auto-provisioning Next.js applications through PinkFlow's auto-deploy system.

## Purpose

This template is used by the PinkFlow provisioning system to automatically create new repositories when customers purchase a plan through Stripe. It includes:

- Next.js 14 with App Router
- TypeScript configuration
- GitHub Actions workflows
- Security scanning
- Accessibility features
- Vercel deployment configuration

## Using This Template

### For System Administrators

1. **Mark as Template**
   - Go to repository Settings
   - Check "Template repository"

2. **Configure in PinkFlow**
   - Set `GH_TEMPLATE_OWNER` to the owner of this repository
   - Set `GH_TEMPLATE_REPO` to the name of this repository

3. **Test Provisioning**
   - Use the Stripe test mode to trigger a checkout
   - Verify a new repository is created from this template
   - Check that secrets are configured correctly
   - Verify Vercel deployment succeeds

### For Developers

When you receive a repository provisioned from this template:

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/your-repo.git
   cd your-repo
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env.local`
   - Fill in any additional variables you need

4. **Start development**
   ```bash
   npm run dev
   ```

5. **Make your changes**
   - Edit files in the `app` directory
   - Customize styling in `app/globals.css`
   - Update branding in `public` directory

6. **Push changes**
   - Changes to `main` branch automatically deploy to production
   - Pull requests create preview deployments

## Included Files

### Configuration
- `package.json` - Dependencies and scripts
- `next.config.js` - Next.js configuration
- `tsconfig.json` - TypeScript configuration
- `.env.example` - Environment variable template
- `.gitignore` - Git ignore rules

### Application
- `app/layout.tsx` - Root layout component
- `app/page.tsx` - Home page
- `app/globals.css` - Global styles

### GitHub Actions
- `.github/workflows/ci.yml` - CI checks on PRs
- `.github/workflows/preview.yml` - Preview deployments
- `.github/workflows/deploy.yml` - Production deployments
- `.github/workflows/audit.yml` - Security scanning

### Documentation
- `README.md` - User-facing documentation

## Customization

### Adding Features

You can customize this template for different use cases:

1. **Add API routes**
   - Create files in `app/api/`
   - Follow Next.js App Router conventions

2. **Add dependencies**
   - Update `package.json`
   - Common additions: database clients, UI libraries, authentication

3. **Add environment variables**
   - Update `.env.example`
   - Document in README
   - Configure in Vercel

4. **Add workflows**
   - Create new files in `.github/workflows/`
   - Examples: E2E tests, performance monitoring

### Creating Variants

You can create multiple templates for different use cases:

1. **nextjs-template** (this one) - Basic Next.js app
2. **nextjs-saas-template** - SaaS starter with auth
3. **nextjs-ecommerce-template** - E-commerce features
4. **nextjs-blog-template** - Blog/content platform

For each variant:
- Create a separate repository
- Mark as template
- Configure in Stripe product metadata: `template_repo: "nextjs-saas-template"`

## Maintenance

### Regular Updates

Update this template regularly to keep it current:

1. **Monthly**
   - Update Next.js and dependencies
   - Test build and deployment
   - Review security advisories

2. **Quarterly**
   - Review and update documentation
   - Add new best practices
   - Optimize performance

3. **Annually**
   - Major version updates
   - Architecture review
   - Security audit

### Testing Changes

Before updating the template:

1. Create a test repository from template
2. Make changes in test repository
3. Verify build and deployment
4. Test all workflows
5. Merge changes to template when verified

## Troubleshooting

### Common Issues

**Template not found**
- Verify repository is marked as template
- Check `GH_TEMPLATE_OWNER` and `GH_TEMPLATE_REPO` values
- Ensure GitHub App has access to template repository

**Workflows don't run**
- Check that `.github/workflows/` directory is included
- Verify GitHub Actions are enabled on new repository
- Check that secrets are configured

**Build fails**
- Review `package.json` for missing dependencies
- Check Node.js version in workflows matches requirements
- Verify `next.config.js` is valid

**Deployment fails**
- Check Vercel secrets are configured
- Verify project ID is correct (set per repository)
- Review Vercel deployment logs

## Support

For issues with this template:
- Create an issue in this repository
- Contact the platform team
- Refer to [PinkFlow Documentation](https://github.com/pinkycollie/pinkflow)

## License

TBD - License to be defined by maintainers.
