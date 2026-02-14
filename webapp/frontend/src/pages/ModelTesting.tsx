import { useState } from 'react'
import { 
  GitBranch, 
  Play, 
  CheckCircle, 
  XCircle, 
  Clock, 
  AlertCircle,
  Download,
  ExternalLink
} from 'lucide-react'

interface TestResult {
  id: string
  repoUrl: string
  status: 'pending' | 'running' | 'passed' | 'failed' | 'error'
  accuracy?: number
  precision?: number
  recall?: number
  f1Score?: number
  processingTime?: number
  errors: string[]
  modelType?: string
  testedAt?: Date
}

// Mock test results - replace with API calls
const mockResults: TestResult[] = [
  {
    id: '1',
    repoUrl: 'https://github.com/sign-language-processing/signbert',
    status: 'passed',
    accuracy: 94.2,
    precision: 92.0,
    recall: 96.4,
    f1Score: 94.2,
    processingTime: 2.34,
    errors: [],
    modelType: 'asl_recognition',
    testedAt: new Date('2024-11-14T10:30:00')
  },
  {
    id: '2',
    repoUrl: 'https://github.com/dxli94/WLASL',
    status: 'passed',
    accuracy: 89.7,
    precision: 87.5,
    recall: 92.0,
    f1Score: 89.7,
    processingTime: 3.12,
    errors: [],
    modelType: 'asl_recognition',
    testedAt: new Date('2024-11-14T09:15:00')
  },
  {
    id: '3',
    repoUrl: 'https://github.com/example/failed-model',
    status: 'failed',
    accuracy: 62.1,
    precision: 58.0,
    recall: 66.2,
    f1Score: 61.8,
    processingTime: 1.87,
    errors: ['Accuracy below 70% threshold'],
    modelType: 'asl_recognition',
    testedAt: new Date('2024-11-13T15:45:00')
  }
]

export default function ModelTesting() {
  const [repoUrl, setRepoUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<TestResult[]>(mockResults)
  const [activeTab, setActiveTab] = useState<'test' | 'results'>('test')

  const handleTest = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!repoUrl.trim()) return

    setIsLoading(true)
    
    // Simulate API call
    setTimeout(() => {
      const newResult: TestResult = {
        id: Date.now().toString(),
        repoUrl: repoUrl,
        status: Math.random() > 0.3 ? 'passed' : 'failed',
        accuracy: 85 + Math.random() * 15,
        precision: 83 + Math.random() * 15,
        recall: 85 + Math.random() * 13,
        f1Score: 84 + Math.random() * 14,
        processingTime: 1 + Math.random() * 3,
        errors: [],
        modelType: 'asl_recognition',
        testedAt: new Date()
      }
      
      setResults([newResult, ...results])
      setRepoUrl('')
      setIsLoading(false)
      setActiveTab('results')
    }, 2000)
  }

  const getStatusIcon = (status: TestResult['status']) => {
    switch (status) {
      case 'passed':
        return <CheckCircle className="text-green-400" size={20} />
      case 'failed':
        return <XCircle className="text-red-400" size={20} />
      case 'running':
        return <Clock className="text-yellow-400 animate-spin" size={20} />
      case 'error':
        return <AlertCircle className="text-orange-400" size={20} />
      default:
        return <Clock className="text-gray-400" size={20} />
    }
  }

  const getStatusBadge = (status: TestResult['status']) => {
    const styles = {
      passed: 'bg-green-500/20 text-green-400 border-green-500/30',
      failed: 'bg-red-500/20 text-red-400 border-red-500/30',
      running: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
      error: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      pending: 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }

    return (
      <span className={`px-3 py-1 rounded-full text-sm border ${styles[status]}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <section>
        <h1 className="text-3xl font-bold mb-2">Model Testing</h1>
        <p className="text-gray-400">
          Test sign language AI models from any GitHub repository against real accessibility standards.
        </p>
      </section>

      {/* Tabs */}
      <div className="flex border-b border-white/10">
        <button
          onClick={() => setActiveTab('test')}
          className={`px-6 py-3 font-medium transition-colors ${
            activeTab === 'test'
              ? 'text-pink-400 border-b-2 border-pink-400'
              : 'text-gray-400 hover:text-white'
          }`}
        >
          New Test
        </button>
        <button
          onClick={() => setActiveTab('results')}
          className={`px-6 py-3 font-medium transition-colors ${
            activeTab === 'results'
              ? 'text-pink-400 border-b-2 border-pink-400'
              : 'text-gray-400 hover:text-white'
          }`}
        >
          Results ({results.length})
        </button>
      </div>

      {/* New Test Form */}
      {activeTab === 'test' && (
        <section className="card">
          <h2 className="text-xl font-bold mb-4">Test a GitHub Repository</h2>
          <form onSubmit={handleTest} className="space-y-6">
            <div>
              <label htmlFor="repo-url" className="block text-sm font-medium mb-2">
                GitHub Repository URL
              </label>
              <div className="relative">
                <GitBranch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                <input
                  id="repo-url"
                  type="url"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  placeholder="https://github.com/username/model-repo"
                  className="w-full pl-12 pr-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:border-pink-500 focus:ring-1 focus:ring-pink-500 transition-colors"
                  required
                />
              </div>
              <p className="text-sm text-gray-500 mt-2">
                Enter the URL of a GitHub repository containing a sign language model.
              </p>
            </div>

            <div className="bg-white/5 rounded-lg p-4">
              <h3 className="font-medium mb-2">What will be tested:</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li className="flex items-center gap-2">
                  <CheckCircle className="text-green-400" size={16} />
                  Model accuracy on standard datasets
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="text-green-400" size={16} />
                  Precision, recall, and F1 score
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="text-green-400" size={16} />
                  Processing speed (FPS)
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="text-green-400" size={16} />
                  Model structure and documentation
                </li>
              </ul>
            </div>

            <button
              type="submit"
              disabled={isLoading || !repoUrl.trim()}
              className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <div className="spinner w-5 h-5" aria-hidden="true" />
                  Testing...
                </>
              ) : (
                <>
                  <Play size={20} />
                  Run Test
                </>
              )}
            </button>
          </form>
        </section>
      )}

      {/* Results List */}
      {activeTab === 'results' && (
        <section className="space-y-4">
          {results.length === 0 ? (
            <div className="card text-center py-12">
              <p className="text-gray-400 mb-4">No test results yet.</p>
              <button
                onClick={() => setActiveTab('test')}
                className="text-pink-400 hover:text-pink-300"
              >
                Run your first test →
              </button>
            </div>
          ) : (
            results.map((result) => (
              <div key={result.id} className="card">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                  <div className="flex items-center gap-3">
                    {getStatusIcon(result.status)}
                    <div>
                      <a
                        href={result.repoUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium hover:text-pink-400 transition-colors flex items-center gap-2"
                      >
                        {result.repoUrl.replace('https://github.com/', '')}
                        <ExternalLink size={14} />
                      </a>
                      <p className="text-sm text-gray-500">
                        {result.testedAt?.toLocaleString()} • {result.modelType}
                      </p>
                    </div>
                  </div>
                  {getStatusBadge(result.status)}
                </div>

                {result.accuracy && (
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    <div>
                      <p className="text-sm text-gray-400">Accuracy</p>
                      <p className={`text-xl font-bold ${result.accuracy >= 90 ? 'text-green-400' : result.accuracy >= 70 ? 'text-yellow-400' : 'text-red-400'}`}>
                        {result.accuracy.toFixed(1)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Precision</p>
                      <p className="text-xl font-bold">{result.precision?.toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Recall</p>
                      <p className="text-xl font-bold">{result.recall?.toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">F1 Score</p>
                      <p className="text-xl font-bold">{result.f1Score?.toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Time</p>
                      <p className="text-xl font-bold">{result.processingTime?.toFixed(2)}s</p>
                    </div>
                  </div>
                )}

                {result.errors.length > 0 && (
                  <div className="mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                    <p className="text-sm text-red-400 font-medium mb-1">Issues Found:</p>
                    <ul className="text-sm text-red-300">
                      {result.errors.map((error, i) => (
                        <li key={i}>• {error}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="flex gap-2 mt-4 pt-4 border-t border-white/10">
                  <button className="px-4 py-2 text-sm bg-white/5 hover:bg-white/10 rounded-lg transition-colors flex items-center gap-2">
                    <Download size={16} />
                    Download Report
                  </button>
                  <button className="px-4 py-2 text-sm bg-white/5 hover:bg-white/10 rounded-lg transition-colors">
                    View Details
                  </button>
                </div>
              </div>
            ))
          )}
        </section>
      )}

      {/* Scoring Guide */}
      <section className="card">
        <h2 className="text-xl font-bold mb-4">Scoring Guide</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-4 h-4 rounded-full status-green" />
              <span className="font-bold text-green-400">GREEN</span>
            </div>
            <p className="text-sm text-gray-300">≥90% accuracy</p>
            <p className="text-xs text-gray-500 mt-1">Production ready, meets accessibility standards</p>
          </div>
          <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-4 h-4 rounded-full status-yellow" />
              <span className="font-bold text-yellow-400">YELLOW</span>
            </div>
            <p className="text-sm text-gray-300">70-89% accuracy</p>
            <p className="text-xs text-gray-500 mt-1">Works but needs improvement</p>
          </div>
          <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-4 h-4 rounded-full status-red" />
              <span className="font-bold text-red-400">RED</span>
            </div>
            <p className="text-sm text-gray-300">&lt;70% accuracy</p>
            <p className="text-xs text-gray-500 mt-1">Does not meet minimum standards</p>
          </div>
        </div>
      </section>
    </div>
  )
}
