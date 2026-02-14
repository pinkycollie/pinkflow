import { 
  Heart, 
  Users, 
  Shield, 
  Target,
  Github,
  ExternalLink
} from 'lucide-react'

export default function About() {
  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="text-center py-8">
        <span className="text-6xl mb-6 block" role="img" aria-label="PinkFlow">🌸</span>
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          About <span className="gradient-text">PinkFlow</span>
        </h1>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto">
          A Deaf-First accessibility platform built to empower the Deaf community 
          with real, tested, and verified tools.
        </p>
      </section>

      {/* Mission */}
      <section className="card bg-gradient-to-r from-pink-900/20 to-purple-900/20 border-pink-500/20">
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-3">
          <Target className="text-pink-400" />
          Our Mission
        </h2>
        <p className="text-gray-300 text-lg leading-relaxed">
          PinkFlow exists because deaf accessibility deserves real standards, not marketing claims. 
          We test, verify, and curate sign language AI models and accessibility tools so the 
          Deaf community can trust what they use.
        </p>
      </section>

      {/* Values */}
      <section>
        <h2 className="text-2xl font-bold mb-6">Our Values</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="card">
            <Heart className="text-pink-400 mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2">Deaf-First Design</h3>
            <p className="text-gray-400">
              Everything we build is designed with the Deaf community at the center. 
              Visual, text-based, and asynchronous by default.
            </p>
          </div>
          <div className="card">
            <Shield className="text-green-400 mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2">Real Standards</h3>
            <p className="text-gray-400">
              We test every model against actual accessibility benchmarks. 
              No marketing claims—just verified performance data.
            </p>
          </div>
          <div className="card">
            <Users className="text-purple-400 mb-4" size={32} />
            <h3 className="text-xl font-bold mb-2">Community Driven</h3>
            <p className="text-gray-400">
              Built by and for the Deaf community. Open source, transparent, 
              and always listening to feedback.
            </p>
          </div>
        </div>
      </section>

      {/* What We Test */}
      <section>
        <h2 className="text-2xl font-bold mb-6">What We Test</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-bold mb-3 text-pink-400">For ASL Recognition Models</h3>
            <ul className="space-y-2 text-gray-400">
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Accuracy on standard ASL dataset
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Precision (false positives)
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Recall (false negatives)
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Processing speed (FPS)
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Model structure quality
              </li>
            </ul>
          </div>
          <div className="card">
            <h3 className="text-lg font-bold mb-3 text-purple-400">For Caption Models</h3>
            <ul className="space-y-2 text-gray-400">
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Caption timing accuracy
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Text quality and readability
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Reading speed (WPM)
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Synchronization quality
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Speaker identification
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Passing Criteria */}
      <section className="card">
        <h2 className="text-2xl font-bold mb-6">Passing Criteria</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-white/10">
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Accuracy</th>
                <th className="py-3 px-4">What It Means</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-white/5">
                <td className="py-4 px-4">
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 rounded-full status-green" />
                    <span className="font-bold text-green-400">GREEN</span>
                  </span>
                </td>
                <td className="py-4 px-4">≥90%</td>
                <td className="py-4 px-4 text-gray-400">Production ready, actually works</td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="py-4 px-4">
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 rounded-full status-yellow" />
                    <span className="font-bold text-yellow-400">YELLOW</span>
                  </span>
                </td>
                <td className="py-4 px-4">70-89%</td>
                <td className="py-4 px-4 text-gray-400">Works but needs improvement</td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="py-4 px-4">
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 rounded-full status-red" />
                    <span className="font-bold text-red-400">RED</span>
                  </span>
                </td>
                <td className="py-4 px-4">&lt;70%</td>
                <td className="py-4 px-4 text-gray-400">Not good enough, don't use</td>
              </tr>
              <tr>
                <td className="py-4 px-4">
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 rounded-full bg-orange-500" />
                    <span className="font-bold text-orange-400">ERROR</span>
                  </span>
                </td>
                <td className="py-4 px-4">N/A</td>
                <td className="py-4 px-4 text-gray-400">Can't even test it</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* What This Is NOT */}
      <section>
        <h2 className="text-2xl font-bold mb-6">What PinkFlow Is NOT</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="card bg-red-500/5 border-red-500/20">
            <p className="flex items-center gap-2 text-red-400">
              <span>❌</span> Not a training framework
            </p>
          </div>
          <div className="card bg-red-500/5 border-red-500/20">
            <p className="flex items-center gap-2 text-red-400">
              <span>❌</span> Not a model builder
            </p>
          </div>
          <div className="card bg-red-500/5 border-red-500/20">
            <p className="flex items-center gap-2 text-red-400">
              <span>❌</span> Not a data labeling tool
            </p>
          </div>
          <div className="card bg-red-500/5 border-red-500/20">
            <p className="flex items-center gap-2 text-red-400">
              <span>❌</span> Not vaporware
            </p>
          </div>
        </div>
        <p className="text-center text-gray-400 mt-6 text-lg">
          <strong>It's JUST a testing tool. That works. Today.</strong>
        </p>
      </section>

      {/* MBTQ Ecosystem */}
      <section className="card bg-gradient-to-r from-purple-900/30 to-pink-900/30 border-purple-500/20">
        <h2 className="text-2xl font-bold mb-4">Part of the MBTQ Universe</h2>
        <p className="text-gray-300 mb-6">
          PinkFlow is part of the larger MBTQ.dev ecosystem, a Deaf-First innovation hub 
          built to empower entrepreneurs, researchers, and creators with AI-driven, 
          accessible business tools.
        </p>
        <div className="grid md:grid-cols-4 gap-4">
          <div className="bg-white/5 rounded-lg p-4 text-center">
            <p className="font-bold text-pink-400">DeafAUTH</p>
            <p className="text-sm text-gray-500">Identity & Auth</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4 text-center">
            <p className="font-bold text-purple-400">PinkSync</p>
            <p className="text-sm text-gray-500">Real-time Sync</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4 text-center">
            <p className="font-bold text-blue-400">FibonRose</p>
            <p className="text-sm text-gray-500">Trust Engine</p>
          </div>
          <div className="bg-white/5 rounded-lg p-4 text-center">
            <p className="font-bold text-green-400">360Magicians</p>
            <p className="text-sm text-gray-500">AI Agents</p>
          </div>
        </div>
      </section>

      {/* Links */}
      <section className="text-center">
        <h2 className="text-2xl font-bold mb-6">Get Involved</h2>
        <div className="flex flex-wrap justify-center gap-4">
          <a 
            href="https://github.com/pinkycollie/pinkflow"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary flex items-center gap-2"
          >
            <Github size={20} />
            GitHub
          </a>
          <a 
            href="https://mbtq.dev"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 rounded-lg font-semibold border border-white/20 hover:bg-white/10 transition-all flex items-center gap-2"
          >
            MBTQ.dev
            <ExternalLink size={18} />
          </a>
          <a 
            href="https://github.com/pinkycollie/pinkflow/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 rounded-lg font-semibold border border-white/20 hover:bg-white/10 transition-all flex items-center gap-2"
          >
            Report Issues
            <ExternalLink size={18} />
          </a>
        </div>
      </section>
    </div>
  )
}
