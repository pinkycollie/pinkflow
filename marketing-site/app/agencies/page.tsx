import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Agency Profiles | MBTQ.dev - PinkFlow',
  description: 'Public accessibility scorecards and compliance reports for agencies and organizations',
}

export default function AgenciesPage() {
  const agencies = [
    {
      name: 'TechForGood Agency',
      score: 94,
      status: 'Excellent',
      lastUpdated: 'Dec 2025',
      features: {
        wcag: 'AA Compliant',
        asl: 'Supported',
        captions: 'All Videos',
        visualAlerts: 'Implemented'
      }
    },
    {
      name: 'AccessFirst Solutions',
      score: 88,
      status: 'Very Good',
      lastUpdated: 'Dec 2025',
      features: {
        wcag: 'AA Compliant',
        asl: 'Partial',
        captions: 'Most Videos',
        visualAlerts: 'Implemented'
      }
    },
    {
      name: 'Inclusive Design Co',
      score: 91,
      status: 'Excellent',
      lastUpdated: 'Dec 2025',
      features: {
        wcag: 'AAA Compliant',
        asl: 'Supported',
        captions: 'All Videos',
        visualAlerts: 'Implemented'
      }
    }
  ]

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-50'
    if (score >= 75) return 'text-blue-600 bg-blue-50'
    if (score >= 60) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const getScoreBadgeColor = (score: number) => {
    if (score >= 90) return 'bg-green-600'
    if (score >= 75) return 'bg-blue-600'
    if (score >= 60) return 'bg-yellow-600'
    return 'bg-red-600'
  }

  return (
    <div className="container mx-auto px-4 py-16">
      <h1 className="text-5xl font-bold mb-8 text-purple-900">Agency Profiles</h1>
      <p className="text-xl text-gray-700 mb-12">
        Public accessibility scorecards for agencies participating in the PinkFlow ecosystem
      </p>

      <div className="mb-12 bg-purple-50 border-l-4 border-purple-600 p-6 rounded">
        <h3 className="font-semibold text-lg mb-2">About Accessibility Scores</h3>
        <p className="text-gray-700">
          Our accessibility scores are based on comprehensive analysis including WCAG compliance, 
          ASL support, caption availability, visual alert implementation, and overall Deaf-First design principles.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {agencies.map((agency, index) => (
          <div key={index} className="bg-white border rounded-lg overflow-hidden shadow-md hover:shadow-lg transition">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold text-gray-900">{agency.name}</h2>
                <div className={`text-3xl font-bold px-4 py-2 rounded ${getScoreColor(agency.score)}`}>
                  {agency.score}
                </div>
              </div>
              
              <div className={`inline-block px-3 py-1 rounded text-sm font-semibold ${getScoreBadgeColor(agency.score)} text-white mb-4`}>
                {agency.status}
              </div>
              
              <div className="space-y-3 mb-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">WCAG Compliance</span>
                  <span className="font-semibold">{agency.features.wcag}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">ASL Support</span>
                  <span className="font-semibold">{agency.features.asl}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Video Captions</span>
                  <span className="font-semibold">{agency.features.captions}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Visual Alerts</span>
                  <span className="font-semibold">{agency.features.visualAlerts}</span>
                </div>
              </div>
              
              <div className="text-sm text-gray-500 mb-4">
                Last updated: {agency.lastUpdated}
              </div>
              
              <a 
                href={`/agencies/${agency.name.toLowerCase().replace(/\s+/g, '-')}`}
                className="block w-full text-center bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition"
              >
                View Full Report
              </a>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-16 bg-white border rounded-lg p-8">
        <h2 className="text-3xl font-bold mb-4">Want your agency featured?</h2>
        <p className="text-gray-700 mb-6">
          Sign up for MBTQ.dev to get your comprehensive accessibility scorecard and public profile. 
          Show funders, clients, and partners that you're committed to accessibility.
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
          <a 
            href="https://pinkycollie.github.io/pinkflow/"
            className="inline-block bg-purple-600 text-white px-6 py-3 rounded hover:bg-purple-700 transition text-center"
          >
            Get Your Scorecard
          </a>
          <a 
            href="/docs"
            className="inline-block border-2 border-purple-600 text-purple-600 px-6 py-3 rounded hover:bg-purple-50 transition text-center"
          >
            Learn More
          </a>
        </div>
      </div>
    </div>
  )
}
