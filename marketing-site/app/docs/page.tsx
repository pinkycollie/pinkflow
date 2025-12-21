import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Documentation | MBTQ.dev - PinkFlow',
  description: 'Comprehensive documentation for the PinkFlow Deaf-First innovation ecosystem',
}

export default function DocsPage() {
  return (
    <div className="container mx-auto px-4 py-16">
      <h1 className="text-5xl font-bold mb-8 text-purple-900">Documentation</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Sidebar */}
        <nav className="md:col-span-1">
          <div className="bg-white border rounded-lg p-6 sticky top-4">
            <h3 className="font-semibold mb-4 text-lg">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="#getting-started" className="text-purple-600 hover:underline">Getting Started</a></li>
              <li><a href="#architecture" className="text-purple-600 hover:underline">Architecture</a></li>
              <li><a href="#api-reference" className="text-purple-600 hover:underline">API Reference</a></li>
              <li><a href="#deployment" className="text-purple-600 hover:underline">Deployment</a></li>
              <li><a href="#contributing" className="text-purple-600 hover:underline">Contributing</a></li>
            </ul>
            
            <h3 className="font-semibold mb-4 mt-8 text-lg">External Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="https://github.com/pinkycollie/pinkflow" className="text-purple-600 hover:underline">
                  GitHub Repository
                </a>
              </li>
              <li>
                <a href="https://pinkycollie.github.io/pinkflow/" className="text-purple-600 hover:underline">
                  Live Demo
                </a>
              </li>
            </ul>
          </div>
        </nav>

        {/* Main Content */}
        <div className="md:col-span-2">
          <section id="getting-started" className="mb-12">
            <h2 className="text-3xl font-semibold mb-4">Getting Started</h2>
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 mb-4">
                Welcome to the PinkFlow documentation. This guide will help you understand and use 
                the Deaf-First innovation ecosystem.
              </p>
              
              <h3 className="text-xl font-semibold mt-6 mb-3">Prerequisites</h3>
              <ul className="list-disc list-inside space-y-2 text-gray-700">
                <li>Node.js v16 or higher (for frontend)</li>
                <li>Python 3.8+ (for backend)</li>
                <li>Basic understanding of React and TypeScript</li>
              </ul>

              <h3 className="text-xl font-semibold mt-6 mb-3">Quick Start</h3>
              <div className="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                <pre>
{`# Clone the repository
git clone https://github.com/pinkycollie/PinkFlow.git
cd PinkFlow

# Install frontend dependencies
cd webapp/frontend
npm install

# Start development server
npm run dev`}
                </pre>
              </div>
            </div>
          </section>

          <section id="architecture" className="mb-12">
            <h2 className="text-3xl font-semibold mb-4">Architecture</h2>
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 mb-4">
                PinkFlow uses a layered architecture separating concerns between marketing, 
                platform, and analytics.
              </p>
              
              <div className="bg-purple-50 border-l-4 border-purple-600 p-4 my-6">
                <p className="font-semibold mb-2">Architecture Layers:</p>
                <ul className="list-disc list-inside space-y-1 text-sm">
                  <li><strong>Next.js:</strong> Marketing site, docs, SEO, public profiles</li>
                  <li><strong>Fresh (Deno):</strong> Platform runtime, dashboard, real-time features</li>
                  <li><strong>PinkFlow:</strong> Analytics engine, accessibility scoring</li>
                </ul>
              </div>
            </div>
          </section>

          <section id="api-reference" className="mb-12">
            <h2 className="text-3xl font-semibold mb-4">API Reference</h2>
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 mb-4">
                Comprehensive API documentation for integrating with PinkFlow services.
              </p>
              
              <h3 className="text-xl font-semibold mt-6 mb-3">Authentication API</h3>
              <div className="bg-white border rounded p-4">
                <code className="text-sm">POST /api/auth/login</code>
                <p className="text-sm text-gray-600 mt-2">Authenticate user and receive JWT token</p>
              </div>
            </div>
          </section>

          <section id="deployment" className="mb-12">
            <h2 className="text-3xl font-semibold mb-4">Deployment</h2>
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 mb-4">
                This marketing site uses Next.js standalone output for self-contained deployment.
              </p>
              
              <h3 className="text-xl font-semibold mt-6 mb-3">Building for Production</h3>
              <div className="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                <pre>
{`# Build the application
npm run build

# Start production server
npm start

# The standalone output is in .next/standalone/`}
                </pre>
              </div>
            </div>
          </section>

          <section id="contributing" className="mb-12">
            <h2 className="text-3xl font-semibold mb-4">Contributing</h2>
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-700 mb-4">
                We welcome contributions from everyone! Please see our contributing guidelines 
                in the main repository.
              </p>
              
              <a 
                href="https://github.com/pinkycollie/pinkflow/blob/main/CONTRIBUTING.md"
                className="inline-block bg-purple-600 text-white px-6 py-3 rounded hover:bg-purple-700 transition"
              >
                View Contributing Guide
              </a>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
