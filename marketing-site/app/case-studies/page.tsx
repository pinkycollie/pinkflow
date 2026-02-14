import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Case Studies | MBTQ.dev - PinkFlow',
  description: 'Real-world examples of accessibility improvements and success stories with PinkFlow',
}

export default function CaseStudiesPage() {
  const caseStudies = [
    {
      title: 'Nonprofit Accessibility Transformation',
      organization: 'Deaf Community Services',
      improvement: '92%',
      description: 'How a nonprofit improved their website accessibility from 45% to 92% using PinkFlow accessibility scoring and recommendations.',
      metrics: {
        before: '45% accessible',
        after: '92% accessible',
        time: '3 months'
      }
    },
    {
      title: 'Government Agency Compliance',
      organization: 'State Education Department',
      improvement: '85%',
      description: 'A state education department achieved WCAG 2.1 AA compliance across all digital properties with PinkFlow analysis.',
      metrics: {
        before: '52% compliant',
        after: '85% compliant',
        time: '6 months'
      }
    },
    {
      title: 'University ASL Integration',
      organization: 'Metropolitan University',
      improvement: '88%',
      description: 'A major university integrated ASL video content and achieved comprehensive accessibility using PinkFlow tools.',
      metrics: {
        before: '38% accessible',
        after: '88% accessible',
        time: '4 months'
      }
    }
  ]

  return (
    <div className="container mx-auto px-4 py-16">
      <h1 className="text-5xl font-bold mb-8 text-purple-900">Case Studies</h1>
      <p className="text-xl text-gray-700 mb-12">
        Real-world examples of organizations improving accessibility with PinkFlow
      </p>

      <div className="space-y-12">
        {caseStudies.map((study, index) => (
          <article key={index} className="bg-white border rounded-lg overflow-hidden shadow-md">
            <div className="md:flex">
              <div className="md:w-1/3 bg-gradient-to-br from-purple-400 to-purple-600 p-8 flex items-center justify-center">
                <div className="text-center text-white">
                  <div className="text-6xl font-bold mb-2">{study.improvement}</div>
                  <div className="text-xl">Improvement</div>
                </div>
              </div>
              <div className="md:w-2/3 p-8">
                <div className="text-sm text-purple-600 font-semibold mb-2">{study.organization}</div>
                <h2 className="text-3xl font-bold mb-4 text-gray-900">{study.title}</h2>
                <p className="text-gray-700 mb-6">{study.description}</p>
                
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-purple-50 p-4 rounded">
                    <div className="text-xs text-gray-600 mb-1">Before</div>
                    <div className="font-semibold text-gray-900">{study.metrics.before}</div>
                  </div>
                  <div className="bg-purple-50 p-4 rounded">
                    <div className="text-xs text-gray-600 mb-1">After</div>
                    <div className="font-semibold text-gray-900">{study.metrics.after}</div>
                  </div>
                  <div className="bg-purple-50 p-4 rounded">
                    <div className="text-xs text-gray-600 mb-1">Timeline</div>
                    <div className="font-semibold text-gray-900">{study.metrics.time}</div>
                  </div>
                </div>
              </div>
            </div>
          </article>
        ))}
      </div>

      <div className="mt-16 bg-purple-600 text-white p-12 rounded-lg text-center">
        <h2 className="text-3xl font-bold mb-4">Want to be featured?</h2>
        <p className="text-xl mb-6">
          Share your accessibility success story with the PinkFlow community
        </p>
        <a 
          href="mailto:contact@mbtq.dev" 
          className="inline-block bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
        >
          Contact Us
        </a>
      </div>
    </div>
  )
}
