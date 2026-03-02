import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'MBTQ.dev - PinkFlow | Deaf-First Innovation Ecosystem',
  description: 'Marketing, documentation, and public content hub for MBTQ.dev PinkFlow - The Deaf-First innovation ecosystem empowering entrepreneurs, researchers, and creators.',
  keywords: ['deaf-first', 'accessibility', 'innovation', 'pinkflow', 'mbtq', 'ASL', 'sign language', 'inclusive tech'],
  authors: [{ name: 'PinkFlow Team' }],
  openGraph: {
    title: 'MBTQ.dev - PinkFlow Marketing',
    description: 'Deaf-First Innovation Ecosystem',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'MBTQ.dev - PinkFlow Marketing',
    description: 'Deaf-First Innovation Ecosystem',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="antialiased">
        <header className="border-b">
          <nav className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <a href="/" className="text-2xl font-bold text-purple-600">
                MBTQ.dev
              </a>
              <div className="hidden md:flex space-x-6">
                <a href="/marketing" className="hover:text-purple-600">Marketing</a>
                <a href="/docs" className="hover:text-purple-600">Docs</a>
                <a href="/blog" className="hover:text-purple-600">Blog</a>
                <a href="/case-studies" className="hover:text-purple-600">Case Studies</a>
                <a href="/agencies" className="hover:text-purple-600">Agencies</a>
              </div>
              <a 
                href="https://pinkycollie.github.io/pinkflow/" 
                className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
                target="_blank"
                rel="noopener noreferrer"
              >
                Try Platform
              </a>
            </div>
          </nav>
        </header>
        <main className="min-h-screen">
          {children}
        </main>
        <footer className="border-t mt-16">
          <div className="container mx-auto px-4 py-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div>
                <h3 className="font-bold mb-4">MBTQ.dev</h3>
                <p className="text-sm text-gray-600">
                  Deaf-First Innovation Ecosystem
                </p>
              </div>
              <div>
                <h4 className="font-semibold mb-4">Product</h4>
                <ul className="space-y-2 text-sm">
                  <li><a href="/marketing" className="hover:text-purple-600">Features</a></li>
                  <li><a href="/docs" className="hover:text-purple-600">Documentation</a></li>
                  <li><a href="/case-studies" className="hover:text-purple-600">Case Studies</a></li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-4">Resources</h4>
                <ul className="space-y-2 text-sm">
                  <li><a href="/blog" className="hover:text-purple-600">Blog</a></li>
                  <li><a href="/agencies" className="hover:text-purple-600">Agency Profiles</a></li>
                  <li><a href="/docs" className="hover:text-purple-600">API Reference</a></li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-4">Community</h4>
                <ul className="space-y-2 text-sm">
                  <li><a href="https://github.com/pinkycollie/pinkflow" className="hover:text-purple-600">GitHub</a></li>
                  <li><a href="/docs/contributing" className="hover:text-purple-600">Contributing</a></li>
                  <li><a href="/docs/code-of-conduct" className="hover:text-purple-600">Code of Conduct</a></li>
                </ul>
              </div>
            </div>
            <div className="mt-8 pt-8 border-t text-center text-sm text-gray-600">
              <p>© 2025 MBTQ.dev - Built with ❤️ by the Deaf-First community</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  )
}
