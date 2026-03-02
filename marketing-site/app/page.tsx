export default function HomePage() {
  return (
    <div className="bg-gradient-to-b from-purple-50 to-white">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 text-purple-900">
            Deaf-First Innovation Ecosystem
          </h1>
          <p className="text-xl md:text-2xl text-gray-700 mb-8">
            Empowering entrepreneurs, researchers, and creators with accessible, AI-driven business tools
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="https://pinkycollie.github.io/pinkflow/" 
              className="bg-purple-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-purple-700 transition"
              target="_blank"
              rel="noopener noreferrer"
            >
              Try PinkFlow Platform
            </a>
            <a 
              href="/docs" 
              className="border-2 border-purple-600 text-purple-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-purple-50 transition"
            >
              View Documentation
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-4xl font-bold text-center mb-12">Content Engine Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold mb-4 text-purple-700">Marketing Hub</h3>
            <p className="text-gray-600">
              Showcase PinkFlow features, updates, and success stories to attract agencies and organizations.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold mb-4 text-purple-700">Documentation</h3>
            <p className="text-gray-600">
              Comprehensive guides, API references, and tutorials for developers and users.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold mb-4 text-purple-700">SEO Optimized</h3>
            <p className="text-gray-600">
              Static generation and server-side rendering for maximum search visibility and performance.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold mb-4 text-purple-700">Public Profiles</h3>
            <p className="text-gray-600">
              Agency accessibility scorecards and compliance reports that attract leads.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold mb-4 text-purple-700">Blog & Updates</h3>
            <p className="text-gray-600">
              Share insights, improvements, and community stories through our content platform.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-2xl font-semibold mb-4 text-purple-700">Case Studies</h3>
            <p className="text-gray-600">
              Real-world examples of accessibility improvements and success metrics.
            </p>
          </div>
        </div>
      </section>

      {/* Architecture Section */}
      <section className="bg-purple-50 py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Architecture Overview</h2>
          <div className="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow-md">
            <div className="space-y-4">
              <div className="border-l-4 border-purple-600 pl-4">
                <h3 className="font-bold text-lg">Next.js (This Site)</h3>
                <p className="text-gray-600">Marketing site, docs, SEO pages, public profiles, blog, case studies</p>
              </div>
              <div className="border-l-4 border-blue-600 pl-4">
                <h3 className="font-bold text-lg">Fresh (Deno Deploy)</h3>
                <p className="text-gray-600">MBTQ.dev dashboard, PinkSync real-time layer, DeafAUTH, Fibonrose trust system</p>
              </div>
              <div className="border-l-4 border-green-600 pl-4">
                <h3 className="font-bold text-lg">PinkFlow</h3>
                <p className="text-gray-600">Analyzes repos, metadata, accessibility scores, generates insights</p>
              </div>
            </div>
            <p className="mt-6 text-sm text-gray-500 italic">
              Next.js attracts visitors → Fresh converts them → PinkFlow powers the analytics
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-3xl mx-auto text-center bg-purple-600 text-white p-12 rounded-lg">
          <h2 className="text-4xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-xl mb-8">
            Join the Deaf-First innovation ecosystem and see how we're transforming accessibility.
          </p>
          <a 
            href="https://pinkycollie.github.io/pinkflow/" 
            className="bg-white text-purple-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100 transition inline-block"
            target="_blank"
            rel="noopener noreferrer"
          >
            Launch Platform
          </a>
        </div>
      </section>
    </div>
  )
}
