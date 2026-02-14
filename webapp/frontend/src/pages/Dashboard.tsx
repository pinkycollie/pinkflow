import { Link } from 'react-router-dom'
import { 
  TestTube, 
  Wrench, 
  CheckCircle, 
  Clock, 
  TrendingUp,
  Award,
  GitBranch,
  ArrowRight
} from 'lucide-react'

// Mock data for dashboard - replace with API calls
const stats = {
  totalModels: 24,
  passedTests: 18,
  avgAccuracy: 89.5,
  avgDeafScore: 92.3,
}

const recentTests = [
  { id: 1, name: 'SignBERT', status: 'passed', accuracy: 94.2, time: '2 hours ago' },
  { id: 2, name: 'WLASL-Pose', status: 'passed', accuracy: 89.7, time: '5 hours ago' },
  { id: 3, name: 'OpenASL', status: 'failed', accuracy: 62.1, time: '1 day ago' },
  { id: 4, name: 'MediaPipe-Hands', status: 'passed', accuracy: 96.5, time: '2 days ago' },
]

const featuredTools = [
  { id: 'captions', name: 'Smart Captions', icon: '📝', status: 'available' },
  { id: 'transcription', name: 'Audio Transcription', icon: '🎤', status: 'available' },
  { id: 'visual-alerts', name: 'Visual Alerts', icon: '🔔', status: 'beta' },
  { id: 'sign-recognition', name: 'Sign Recognition', icon: '✋', status: 'beta' },
]

export default function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <section className="text-center py-8">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="gradient-text">Deaf-First</span> Accessibility Tools
        </h1>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto mb-8">
          Test sign language models, generate captions, transcribe audio, and more.
          Built by and for the Deaf community.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link to="/testing" className="btn-primary flex items-center gap-2">
            <TestTube size={20} />
            Test a Model
          </Link>
          <Link to="/tools" className="px-6 py-3 rounded-lg font-semibold border border-white/20 hover:bg-white/10 transition-all flex items-center gap-2">
            <Wrench size={20} />
            Explore Tools
          </Link>
        </div>
      </section>

      {/* Stats Grid */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4" aria-label="Statistics">
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <GitBranch className="w-5 h-5 text-blue-400" aria-hidden="true" />
            <span className="text-sm text-gray-400">Total Models</span>
          </div>
          <div className="text-3xl font-bold">{stats.totalModels}</div>
        </div>
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="w-5 h-5 text-green-400" aria-hidden="true" />
            <span className="text-sm text-gray-400">Passed Tests</span>
          </div>
          <div className="text-3xl font-bold">{stats.passedTests}</div>
        </div>
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-5 h-5 text-purple-400" aria-hidden="true" />
            <span className="text-sm text-gray-400">Avg Accuracy</span>
          </div>
          <div className="text-3xl font-bold">{stats.avgAccuracy}%</div>
        </div>
        <div className="card">
          <div className="flex items-center gap-2 mb-2">
            <Award className="w-5 h-5 text-pink-400" aria-hidden="true" />
            <span className="text-sm text-gray-400">Deaf Score</span>
          </div>
          <div className="text-3xl font-bold">{stats.avgDeafScore}%</div>
        </div>
      </section>

      {/* Recent Tests & Featured Tools */}
      <div className="grid md:grid-cols-2 gap-8">
        {/* Recent Tests */}
        <section>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Recent Tests</h2>
            <Link to="/testing" className="text-pink-400 hover:text-pink-300 flex items-center gap-1 text-sm">
              View all <ArrowRight size={16} />
            </Link>
          </div>
          <div className="space-y-3">
            {recentTests.map((test) => (
              <div key={test.id} className="card flex items-center justify-between py-4">
                <div className="flex items-center gap-3">
                  <div 
                    className={`w-3 h-3 rounded-full ${
                      test.status === 'passed' ? 'status-green' : 'status-red'
                    }`}
                    aria-hidden="true"
                  />
                  <div>
                    <p className="font-medium">{test.name}</p>
                    <p className="text-sm text-gray-400">{test.time}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`font-bold ${test.status === 'passed' ? 'text-green-400' : 'text-red-400'}`}>
                    {test.accuracy}%
                  </p>
                  <p className="text-xs text-gray-500 capitalize">{test.status}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Featured Tools */}
        <section>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Accessibility Tools</h2>
            <Link to="/tools" className="text-pink-400 hover:text-pink-300 flex items-center gap-1 text-sm">
              View all <ArrowRight size={16} />
            </Link>
          </div>
          <div className="space-y-3">
            {featuredTools.map((tool) => (
              <Link key={tool.id} to={`/tools#${tool.id}`} className="card flex items-center justify-between py-4 group">
                <div className="flex items-center gap-3">
                  <span className="text-2xl" role="img" aria-hidden="true">{tool.icon}</span>
                  <div>
                    <p className="font-medium group-hover:text-pink-400 transition-colors">{tool.name}</p>
                    <p className="text-sm text-gray-400 capitalize">{tool.status}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {tool.status === 'beta' && (
                    <span className="px-2 py-1 text-xs bg-yellow-500/20 text-yellow-400 rounded-full">
                      Beta
                    </span>
                  )}
                  <ArrowRight className="text-gray-500 group-hover:text-pink-400 transition-colors" size={18} />
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>

      {/* Call to Action */}
      <section className="text-center py-12 card bg-gradient-to-r from-pink-900/30 to-purple-900/30 border-pink-500/20">
        <h2 className="text-2xl font-bold mb-4">Have a Model to Test?</h2>
        <p className="text-gray-300 mb-6 max-w-xl mx-auto">
          Submit any GitHub repository with a sign language model and get it tested 
          against real accessibility standards within minutes.
        </p>
        <Link to="/testing" className="btn-primary inline-flex items-center gap-2">
          <TestTube size={20} />
          Start Testing Now
        </Link>
      </section>
    </div>
  )
}
