import { useState } from 'react'
import { 
  CheckCircle, 
  Clock, 
  AlertTriangle, 
  ArrowRight,
  Play,
  Settings,
  ExternalLink
} from 'lucide-react'

interface Tool {
  id: string
  name: string
  description: string
  category: string
  status: 'available' | 'beta' | 'coming_soon' | 'maintenance'
  icon: string
  features: string[]
  deafScore?: number
}

const tools: Tool[] = [
  {
    id: 'model-testing',
    name: 'Model Testing',
    description: 'Test sign language AI models against real accessibility standards. Submit any GitHub repo and get comprehensive metrics.',
    category: 'model_testing',
    status: 'available',
    icon: '🧪',
    features: [
      'Test GitHub repos automatically',
      'ASL recognition accuracy testing',
      'Fingerspelling validation',
      'Caption quality scoring',
      'Performance benchmarks',
      'Detailed reports'
    ],
    deafScore: 98
  },
  {
    id: 'captions',
    name: 'Smart Captions',
    description: 'Generate high-quality, Deaf-friendly captions for any video content with speaker identification and custom styling.',
    category: 'captions',
    status: 'available',
    icon: '📝',
    features: [
      'Real-time captioning',
      'Speaker identification',
      'Multiple language support',
      'Custom styling options',
      'Export to SRT/VTT formats',
      'Sync with video timeline'
    ],
    deafScore: 95
  },
  {
    id: 'transcription',
    name: 'Audio Transcription',
    description: 'Convert audio to text with high accuracy. Perfect for meetings, lectures, podcasts, and more.',
    category: 'transcription',
    status: 'available',
    icon: '🎤',
    features: [
      'Multi-speaker detection',
      'Timestamp generation',
      'Background noise filtering',
      'Technical vocabulary support',
      'Real-time mode',
      'Batch processing'
    ],
    deafScore: 92
  },
  {
    id: 'visual-alerts',
    name: 'Visual Alerts',
    description: 'Convert audio alerts and environmental sounds to visual and haptic notifications.',
    category: 'visual_alerts',
    status: 'beta',
    icon: '🔔',
    features: [
      'Doorbell detection',
      'Phone ring alerts',
      'Baby cry detection',
      'Smoke alarm alerts',
      'Custom sound training',
      'Smart home integration'
    ],
    deafScore: 88
  },
  {
    id: 'sign-recognition',
    name: 'Sign Language Recognition',
    description: 'Real-time ASL to text translation using your webcam. Supports alphabet, common words, and continuous signing.',
    category: 'sign_recognition',
    status: 'beta',
    icon: '✋',
    features: [
      'Real-time processing',
      'ASL alphabet support',
      'Common phrases library',
      'Gesture detection',
      'Continuous signing mode',
      'Learning mode'
    ],
    deafScore: 85
  },
  {
    id: 'video-relay',
    name: 'Video Relay Service',
    description: 'Connect with certified sign language interpreters 24/7 for phone calls and video meetings.',
    category: 'video_relay',
    status: 'coming_soon',
    icon: '📹',
    features: [
      '24/7 availability',
      'ASL interpreters',
      'International Sign support',
      'Emergency priority',
      'Business scheduling',
      'HIPAA compliant'
    ]
  },
  {
    id: 'text-to-sign',
    name: 'Text to Sign',
    description: 'Convert written text to sign language animations with a customizable avatar.',
    category: 'text_to_sign',
    status: 'coming_soon',
    icon: '🤟',
    features: [
      'Animated avatar',
      'Multiple sign languages',
      'Customizable speed',
      'Export to video',
      'API integration',
      'Educational mode'
    ]
  }
]

const categories = [
  { id: 'all', label: 'All Tools' },
  { id: 'model_testing', label: 'Testing' },
  { id: 'captions', label: 'Captions' },
  { id: 'transcription', label: 'Transcription' },
  { id: 'visual_alerts', label: 'Alerts' },
  { id: 'sign_recognition', label: 'Recognition' },
]

export default function Tools() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedTool, setSelectedTool] = useState<Tool | null>(null)

  const filteredTools = selectedCategory === 'all'
    ? tools
    : tools.filter(t => t.category === selectedCategory)

  const getStatusBadge = (status: Tool['status']) => {
    switch (status) {
      case 'available':
        return (
          <span className="flex items-center gap-1 px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full">
            <CheckCircle size={12} />
            Available
          </span>
        )
      case 'beta':
        return (
          <span className="flex items-center gap-1 px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full">
            <AlertTriangle size={12} />
            Beta
          </span>
        )
      case 'coming_soon':
        return (
          <span className="flex items-center gap-1 px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded-full">
            <Clock size={12} />
            Coming Soon
          </span>
        )
      case 'maintenance':
        return (
          <span className="flex items-center gap-1 px-2 py-1 bg-orange-500/20 text-orange-400 text-xs rounded-full">
            <Settings size={12} />
            Maintenance
          </span>
        )
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <section>
        <h1 className="text-3xl font-bold mb-2">Accessibility Tools</h1>
        <p className="text-gray-400">
          A complete suite of Deaf-First accessibility tools designed by and for the Deaf community.
        </p>
      </section>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              selectedCategory === cat.id
                ? 'bg-pink-500 text-white'
                : 'bg-white/10 hover:bg-white/20 text-gray-300'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Tools Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredTools.map((tool) => (
          <div
            key={tool.id}
            className="card group cursor-pointer"
            onClick={() => setSelectedTool(tool)}
          >
            <div className="flex items-start justify-between mb-4">
              <span className="text-4xl" role="img" aria-hidden="true">{tool.icon}</span>
              {getStatusBadge(tool.status)}
            </div>
            
            <h3 className="text-xl font-bold mb-2 group-hover:text-pink-400 transition-colors">
              {tool.name}
            </h3>
            <p className="text-gray-400 text-sm mb-4 line-clamp-2">
              {tool.description}
            </p>

            {tool.deafScore && (
              <div className="flex items-center gap-2 mb-4">
                <span className="text-sm text-gray-500">Deaf-First Score:</span>
                <span className={`font-bold ${tool.deafScore >= 90 ? 'text-green-400' : 'text-yellow-400'}`}>
                  {tool.deafScore}%
                </span>
              </div>
            )}

            <div className="flex items-center justify-between pt-4 border-t border-white/10">
              <span className="text-sm text-gray-500">{tool.features.length} features</span>
              <ArrowRight className="text-gray-500 group-hover:text-pink-400 transition-colors" size={18} />
            </div>
          </div>
        ))}
      </div>

      {/* Tool Detail Modal */}
      {selectedTool && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedTool(null)}
        >
          <div 
            className="bg-gray-900 border border-white/20 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center gap-4">
                  <span className="text-5xl" role="img" aria-hidden="true">{selectedTool.icon}</span>
                  <div>
                    <h2 className="text-2xl font-bold">{selectedTool.name}</h2>
                    <div className="flex items-center gap-2 mt-1">
                      {getStatusBadge(selectedTool.status)}
                      {selectedTool.deafScore && (
                        <span className="text-sm text-gray-400">
                          Deaf-First Score: <span className="text-pink-400 font-bold">{selectedTool.deafScore}%</span>
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedTool(null)}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                  aria-label="Close"
                >
                  ✕
                </button>
              </div>

              <p className="text-gray-300 mb-6">{selectedTool.description}</p>

              <div className="mb-6">
                <h3 className="font-bold mb-3">Features</h3>
                <ul className="grid md:grid-cols-2 gap-2">
                  {selectedTool.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm text-gray-400">
                      <CheckCircle className="text-green-400 flex-shrink-0" size={16} />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="flex gap-3">
                {selectedTool.status === 'available' && (
                  <button className="btn-primary flex items-center gap-2">
                    <Play size={18} />
                    Launch Tool
                  </button>
                )}
                {selectedTool.status === 'beta' && (
                  <button className="btn-primary flex items-center gap-2">
                    <Play size={18} />
                    Try Beta
                  </button>
                )}
                {selectedTool.status === 'coming_soon' && (
                  <button className="px-6 py-3 rounded-lg font-semibold bg-white/10 border border-white/20 cursor-not-allowed opacity-60">
                    Coming Soon
                  </button>
                )}
                <button className="px-6 py-3 rounded-lg font-semibold border border-white/20 hover:bg-white/10 transition-all flex items-center gap-2">
                  <ExternalLink size={18} />
                  Documentation
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* API Section */}
      <section className="card bg-gradient-to-r from-purple-900/30 to-pink-900/30 border-purple-500/20">
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="flex-1">
            <h2 className="text-2xl font-bold mb-2">Developer API</h2>
            <p className="text-gray-300 mb-4">
              Integrate PinkFlow accessibility tools into your own applications with our REST API.
              Available for all production-ready tools.
            </p>
            <div className="flex gap-3">
              <a href="/docs" className="btn-primary inline-flex items-center gap-2">
                View API Docs
                <ExternalLink size={18} />
              </a>
            </div>
          </div>
          <div className="bg-black/30 rounded-lg p-4 font-mono text-sm text-gray-300 max-w-md w-full">
            <code>
              <span className="text-purple-400">POST</span> /api/test/model<br />
              <span className="text-gray-500">{`{`}</span><br />
              <span className="text-pink-400 ml-4">"repo_url"</span>: <span className="text-green-400">"github.com/..."</span><br />
              <span className="text-gray-500">{`}`}</span>
            </code>
          </div>
        </div>
      </section>
    </div>
  )
}
