export default function MarketingPage() {
  return (
    <div className="container mx-auto px-4 py-16">
      <h1 className="text-5xl font-bold mb-8 text-purple-900">Marketing Hub</h1>
      
      <section className="mb-16">
        <h2 className="text-3xl font-semibold mb-6">Why PinkFlow?</h2>
        <div className="prose prose-lg max-w-none">
          <p className="text-lg text-gray-700 mb-4">
            PinkFlow is the first Deaf-First innovation ecosystem built from the ground up with 
            accessibility, visual communication, and asynchronous collaboration at its core.
          </p>
          <p className="text-lg text-gray-700">
            Our platform empowers developers, researchers, and contributors to build accessible 
            applications that truly serve the Deaf community.
          </p>
        </div>
      </section>

      <section className="mb-16">
        <h2 className="text-3xl font-semibold mb-6">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[
            {
              title: 'Model Testing',
              description: 'Test sign language AI models from GitHub repos against real accessibility standards'
            },
            {
              title: 'Smart Captions',
              description: 'Generate high-quality captions for video content'
            },
            {
              title: 'Audio Transcription',
              description: 'Convert audio to text with speaker detection'
            },
            {
              title: 'Visual Alerts',
              description: 'Convert audio alerts to visual notifications'
            },
            {
              title: 'Sign Recognition',
              description: 'Real-time ASL to text translation'
            },
            {
              title: 'Accessibility Scoring',
              description: 'Comprehensive accessibility compliance reports'
            }
          ].map((feature, index) => (
            <div key={index} className="bg-white border rounded-lg p-6 shadow-sm hover:shadow-md transition">
              <h3 className="text-xl font-semibold mb-2 text-purple-700">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-3xl font-semibold mb-6">Success Metrics</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-purple-50 p-8 rounded-lg text-center">
            <div className="text-4xl font-bold text-purple-600 mb-2">100+</div>
            <div className="text-gray-700">Projects Analyzed</div>
          </div>
          <div className="bg-purple-50 p-8 rounded-lg text-center">
            <div className="text-4xl font-bold text-purple-600 mb-2">95%</div>
            <div className="text-gray-700">Accessibility Improvement</div>
          </div>
          <div className="bg-purple-50 p-8 rounded-lg text-center">
            <div className="text-4xl font-bold text-purple-600 mb-2">50+</div>
            <div className="text-gray-700">Contributing Developers</div>
          </div>
        </div>
      </section>
    </div>
  )
}
