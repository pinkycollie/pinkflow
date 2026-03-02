# PinkFlow Marketing Site - Next.js Standalone

This is the **marketing and content engine** for MBTQ.dev PinkFlow, built with Next.js using standalone output for self-contained deployment.

## 🎯 Purpose

This Next.js application serves as the **public-facing content layer** for PinkFlow, separate from the platform runtime. It handles:

- ✨ **Marketing Site** - Showcasing PinkFlow features and benefits
- 📚 **Documentation** - Comprehensive guides and API references
- 🔍 **SEO Pages** - Optimized content for search visibility
- 🏢 **Agency Profiles** - Public accessibility scorecards
- 📝 **Blog** - Updates, insights, and community stories
- 📊 **Case Studies** - Real-world success stories
- 🎯 **Landing Pages** - Lead capture and conversion

## 🏗️ Architecture

```
Next.js (This Site) → Marketing & Content
    ↓
Fresh (Deno Deploy) → Platform Runtime
    ↓
PinkFlow → Analytics Engine
```

### Why Separate?

- **Next.js** excels at static generation, SEO, and content management
- **Fresh (Deno Deploy)** powers the interactive platform runtime
- **PinkFlow** provides the data and analytics

This separation allows each layer to use the best tool for its purpose.

## 🚀 Getting Started

### Prerequisites

- Node.js v16 or higher
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production (standalone output)
npm start            # Start production server
npm run lint         # Run ESLint
npm run type-check   # TypeScript type checking
```

## 📁 Project Structure

```
marketing-site/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Root layout with navigation
│   ├── page.tsx             # Homepage
│   ├── globals.css          # Global styles
│   ├── marketing/           # Marketing pages
│   ├── docs/                # Documentation
│   ├── blog/                # Blog posts
│   ├── case-studies/        # Case studies
│   ├── agencies/            # Agency profiles
│   └── landing/             # Landing pages
├── components/              # Reusable React components
├── lib/                     # Utility functions
├── public/                  # Static assets
├── styles/                  # Additional stylesheets
├── next.config.js           # Next.js configuration (standalone output)
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies and scripts
```

## ⚙️ Configuration

### Standalone Output

This site uses Next.js standalone output for self-contained deployment:

```javascript
// next.config.js
module.exports = {
  output: 'standalone',
  // ... other config
}
```

The standalone output includes:
- All necessary dependencies
- Self-contained server
- Optimized for containerization
- No need for node_modules in production

### Building for Production

```bash
# Build the application
npm run build

# The standalone output is in .next/standalone/
# Copy static files
cp -r .next/static .next/standalone/.next/
cp -r public .next/standalone/

# Start the server
cd .next/standalone
node server.js
```

## 🎨 Styling

This project uses **Tailwind CSS** for styling with a custom purple theme matching PinkFlow branding.

### Color Palette

- Primary: Purple (`#9333ea`)
- Accent shades: Purple-50 through Purple-900
- Semantic colors for accessibility scores

## 🔐 Security Features

The site includes security headers configured in `next.config.js`:

- X-DNS-Prefetch-Control
- Strict-Transport-Security (HSTS)
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Referrer-Policy

## 📊 SEO Optimization

Each page includes:
- Metadata with title and description
- OpenGraph tags for social sharing
- Twitter Card support
- Semantic HTML structure
- Optimized for Core Web Vitals

## 🚢 Deployment

### Option 1: Standalone (Recommended)

```bash
# Build
npm run build

# Deploy the .next/standalone directory
# Run with: node server.js
```

### Option 2: Docker

```dockerfile
FROM node:18-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

### Option 3: Traditional Hosting

Deploy to any Node.js hosting platform:
- Vercel (native Next.js support)
- Railway
- Render
- Fly.io
- Cloud Run (Google Cloud)

## 🔗 Integration with Platform

This marketing site links to the main PinkFlow platform:

- **Live Demo**: https://pinkycollie.github.io/pinkflow/
- **GitHub**: https://github.com/pinkycollie/pinkflow

Users who engage with marketing content are directed to the platform for signup and usage.

## 📝 Content Management

### Adding New Pages

1. Create a new directory in `app/`
2. Add a `page.tsx` file
3. Export metadata for SEO
4. Add navigation link in `app/layout.tsx`

Example:
```typescript
// app/new-page/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'New Page | MBTQ.dev',
  description: 'Page description',
}

export default function NewPage() {
  return <div>Content</div>
}
```

### Adding Blog Posts

Create MDX files or dynamic routes in `app/blog/[slug]/page.tsx`

### Updating Agency Profiles

Edit the agency data in `app/agencies/page.tsx` or connect to a CMS/API.

## 🧪 Testing

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build test
npm run build
```

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Next.js Standalone Output](https://nextjs.org/docs/advanced-features/output-file-tracing)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [PinkFlow Main Repository](https://github.com/pinkycollie/pinkflow)

## 🤝 Contributing

This is part of the PinkFlow ecosystem. See the main repository for contributing guidelines:
- [Contributing Guide](../CONTRIBUTING.md)
- [Code of Conduct](../CODE_OF_CONDUCT.md)

## 📄 License

See [LICENSE](../LICENSE) in the root of the repository.

## 💬 Support

- Open an issue in the main repository
- Check the documentation at `/docs`
- Join community discussions

---

**Built with ❤️ by the Deaf-First community**
