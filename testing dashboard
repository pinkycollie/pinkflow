import React, { useState, useEffect } from ‘react’;
import { Search, GitBranch, Zap, Award, TrendingUp, ExternalLink, Play, CheckCircle, XCircle, Clock } from ‘lucide-react’;

const PinkFlowDashboard = () => {
const [models, setModels] = useState([]);
const [filter, setFilter] = useState(‘all’);
const [search, setSearch] = useState(’’);
const [loading, setLoading] = useState(true);

// Mock data - replace with actual API call to api.mbtq.dev
useEffect(() => {
// Simulating API call
setTimeout(() => {
setModels([
{
id: 1,
name: ‘SignBERT’,
task: ‘SLT’,
accuracy: 94.2,
fps: 30,
deafScore: 98,
status: ‘tested’,
repo: ‘https://github.com/sign-language-processing/signbert’,
paper: ‘https://arxiv.org/abs/2104.00990’,
tested: ‘2025-11-14T10:30:00Z’
},
{
id: 2,
name: ‘WLASL-Pose’,
task: ‘SLR’,
accuracy: 89.7,
fps: 60,
deafScore: 95,
status: ‘tested’,
repo: ‘https://github.com/dxli94/WLASL’,
paper: ‘https://arxiv.org/abs/1910.11006’,
tested: ‘2025-11-14T09:15:00Z’
},
{
id: 3,
name: ‘PHOENIX-2014T’,
task: ‘SLT’,
accuracy: 91.3,
fps: 25,
deafScore: 92,
status: ‘tested’,
repo: ‘https://github.com/neccam/slt’,
paper: ‘https://arxiv.org/abs/1801.05613’,
tested: ‘2025-11-14T08:00:00Z’
},
{
id: 4,
name: ‘MediaPipe-Hands’,
task: ‘Pose’,
accuracy: 96.5,
fps: 120,
deafScore: 97,
status: ‘tested’,
repo: ‘https://github.com/google/mediapipe’,
paper: ‘https://arxiv.org/abs/2006.10214’,
tested: ‘2025-11-13T22:45:00Z’
},
{
id: 5,
name: ‘TSPNet’,
task: ‘SLP’,
accuracy: 88.4,
fps: 15,
deafScore: 90,
status: ‘testing’,
repo: ‘https://github.com/Sign-Language-Processing’,
paper: ‘https://arxiv.org/abs/2203.04287’,
tested: null
},
{
id: 6,
name: ‘OpenASL’,
task: ‘SLR’,
accuracy: null,
fps: null,
deafScore: null,
status: ‘queued’,
repo: ‘https://github.com/OpenASL’,
paper: null,
tested: null
}
]);
setLoading(false);
}, 800);
}, []);

const taskColors = {
SLR: ‘bg-blue-500’,
SLT: ‘bg-purple-500’,
SLP: ‘bg-green-500’,
Pose: ‘bg-orange-500’
};

const statusIcons = {
tested: <CheckCircle className="w-4 h-4 text-green-400" />,
testing: <Clock className="w-4 h-4 text-yellow-400 animate-pulse" />,
queued: <Clock className="w-4 h-4 text-gray-400" />,
failed: <XCircle className="w-4 h-4 text-red-400" />
};

const filteredModels = models.filter(m => {
const matchesFilter = filter === ‘all’ || m.task === filter;
const matchesSearch = m.name.toLowerCase().includes(search.toLowerCase());
return matchesFilter && matchesSearch;
});

const stats = {
total: models.length,
tested: models.filter(m => m.status === ‘tested’).length,
avgAccuracy: models.filter(m => m.accuracy).reduce((sum, m) => sum + m.accuracy, 0) / models.filter(m => m.accuracy).length || 0,
avgDeafScore: models.filter(m => m.deafScore).reduce((sum, m) => sum + m.deafScore, 0) / models.filter(m => m.deafScore).length || 0
};

return (
<div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-pink-900 text-white p-6">
{/* Header */}
<header className="mb-8">
<div className="flex items-center justify-between mb-4">
<div>
<h1 className="text-4xl font-bold bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
PinkFlow
</h1>
<p className="text-gray-300 mt-1">Sign Language Model Testing & Validation</p>
<p className="text-sm text-purple-300 mt-1">pinkflow.mbtq.dev</p>
</div>
<div className="text-right">
<div className="text-sm text-gray-400">Powered by</div>
<div className="text-lg font-semibold text-pink-400">MBTQ Universe</div>
</div>
</div>

```
    {/* Stats Cards */}
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-4 border border-white/20">
        <div className="flex items-center gap-2 mb-2">
          <GitBranch className="w-5 h-5 text-blue-400" />
          <span className="text-sm text-gray-300">Total Models</span>
        </div>
        <div className="text-3xl font-bold">{stats.total}</div>
      </div>
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-4 border border-white/20">
        <div className="flex items-center gap-2 mb-2">
          <CheckCircle className="w-5 h-5 text-green-400" />
          <span className="text-sm text-gray-300">Tested</span>
        </div>
        <div className="text-3xl font-bold">{stats.tested}</div>
      </div>
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-4 border border-white/20">
        <div className="flex items-center gap-2 mb-2">
          <TrendingUp className="w-5 h-5 text-purple-400" />
          <span className="text-sm text-gray-300">Avg Accuracy</span>
        </div>
        <div className="text-3xl font-bold">{stats.avgAccuracy.toFixed(1)}%</div>
      </div>
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-4 border border-white/20">
        <div className="flex items-center gap-2 mb-2">
          <Award className="w-5 h-5 text-pink-400" />
          <span className="text-sm text-gray-300">Deaf Score</span>
        </div>
        <div className="text-3xl font-bold">{stats.avgDeafScore.toFixed(1)}%</div>
      </div>
    </div>

    {/* Filters */}
    <div className="flex flex-col md:flex-row gap-4">
      <div className="flex-1 relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search models..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-3 bg-white/10 backdrop-blur-lg border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500"
        />
      </div>
      <div className="flex gap-2">
        {['all', 'SLR', 'SLT', 'SLP', 'Pose'].map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-3 rounded-lg font-medium transition-all ${
              filter === f
                ? 'bg-pink-500 text-white'
                : 'bg-white/10 backdrop-blur-lg border border-white/20 hover:bg-white/20'
            }`}
          >
            {f === 'all' ? 'All' : f}
          </button>
        ))}
      </div>
    </div>
  </header>

  {/* Models Grid */}
  {loading ? (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-4 border-pink-500 border-t-transparent"></div>
    </div>
  ) : (
    <div className="grid gap-4">
      {filteredModels.map(model => (
        <div
          key={model.id}
          className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-lg p-6 hover:bg-white/15 transition-all"
        >
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <h3 className="text-xl font-bold">{model.name}</h3>
                <span className={`${taskColors[model.task]} px-3 py-1 rounded-full text-xs font-semibold`}>
                  {model.task}
                </span>
                <div className="flex items-center gap-1">
                  {statusIcons[model.status]}
                  <span className="text-sm text-gray-300 capitalize">{model.status}</span>
                </div>
              </div>
              
              {model.tested && (
                <div className="text-sm text-gray-400 mb-3">
                  Tested: {new Date(model.tested).toLocaleString()}
                </div>
              )}

              <div className="flex flex-wrap gap-4 text-sm">
                {model.accuracy !== null && (
                  <div>
                    <span className="text-gray-400">Accuracy:</span>
                    <span className="ml-2 font-semibold text-green-400">{model.accuracy}%</span>
                  </div>
                )}
                {model.fps !== null && (
                  <div>
                    <span className="text-gray-400">Speed:</span>
                    <span className="ml-2 font-semibold text-blue-400">{model.fps} fps</span>
                  </div>
                )}
                {model.deafScore !== null && (
                  <div>
                    <span className="text-gray-400">Deaf-First Score:</span>
                    <span className="ml-2 font-semibold text-pink-400">{model.deafScore}%</span>
                  </div>
                )}
              </div>
            </div>

            <div className="flex gap-2">
              {model.repo && (
                <a
                  href={model.repo}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
                >
                  <GitBranch className="w-4 h-4" />
                  <span>Repo</span>
                </a>
              )}
              {model.paper && (
                <a
                  href={model.paper}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>Paper</span>
                </a>
              )}
              {model.status === 'tested' && (
                <button className="flex items-center gap-2 px-4 py-2 bg-pink-600 hover:bg-pink-700 rounded-lg transition-colors">
                  <Play className="w-4 h-4" />
                  <span>Deploy</span>
                </button>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  )}

  {/* Footer */}
  <footer className="mt-12 pt-6 border-t border-white/20 text-center text-sm text-gray-400">
    <p>Part of the MBTQ Universe Ecosystem</p>
    <p className="mt-2">DeafAUTH • PinkSync • Fibonrose • 360Magicians</p>
    <p className="mt-2">
      <a href="https://github.com/VIPL-SLP/Awesome-Sign-Language-Processing" target="_blank" rel="noopener noreferrer" className="text-pink-400 hover:text-pink-300">
        Data source: Awesome Sign Language Processing
      </a>
    </p>
  </footer>
</div>
```

);
};

export default PinkFlowDashboard;