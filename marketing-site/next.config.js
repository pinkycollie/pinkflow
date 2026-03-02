/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for self-contained deployment
  output: 'standalone',
  
  // Optimize images
  images: {
    unoptimized: false,
    // Only allow images from trusted domains
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'github.com',
      },
      {
        protocol: 'https',
        hostname: '*.githubusercontent.com',
      },
      {
        protocol: 'https',
        hostname: 'mbtq.dev',
      },
      {
        protocol: 'https',
        hostname: '*.mbtq.dev',
      },
    ],
  },

  // Enable React strict mode for better error detection
  reactStrictMode: true,

  // Configure paths
  basePath: '',
  
  // Environment variables that should be available on client-side
  env: {
    NEXT_PUBLIC_SITE_NAME: 'MBTQ.dev - PinkFlow Marketing',
    NEXT_PUBLIC_SITE_DESCRIPTION: 'Deaf-First Innovation Ecosystem - Marketing & Content Hub',
  },

  // Headers for security and performance
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin'
          }
        ]
      }
    ]
  },

  // Redirects for legacy URLs
  async redirects() {
    return []
  },

  // Rewrites for API proxy if needed
  async rewrites() {
    return []
  }
}

module.exports = nextConfig
