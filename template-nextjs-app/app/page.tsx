export default function Home() {
  const appName = process.env.NEXT_PUBLIC_APP_NAME || 'Your App';
  const plan = process.env.PLAN || 'Starter';
  
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8 bg-gradient-to-b from-blue-50 to-white">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4 text-gray-900">
          Welcome to {appName}
        </h1>
        <p className="text-xl mb-2 text-gray-600">
          Your {plan} plan application is ready!
        </p>
        <p className="text-md mb-8 text-gray-500">
          Auto-provisioned by PinkFlow
        </p>
        
        <div className="grid md:grid-cols-2 gap-6 mt-12">
          <div className="p-6 bg-white border-2 border-blue-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-2xl font-bold mb-3 text-blue-600">🚀 Get Started</h2>
            <p className="text-gray-600 mb-4">
              Clone this repository and start building your application.
            </p>
            <a 
              href="/README.md" 
              className="text-blue-600 hover:underline font-medium"
            >
              Read Documentation →
            </a>
          </div>
          
          <div className="p-6 bg-white border-2 border-green-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <h2 className="text-2xl font-bold mb-3 text-green-600">✨ Features</h2>
            <ul className="text-left text-gray-600 space-y-2">
              <li>✅ TypeScript support</li>
              <li>✅ Automatic deployments</li>
              <li>✅ Security scanning</li>
              <li>✅ Accessible design</li>
            </ul>
          </div>
        </div>
        
        <div className="mt-12 p-6 bg-white border-2 border-purple-200 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-purple-600">
            📚 Resources
          </h3>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <a 
              href="https://nextjs.org/docs" 
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              Next.js Docs
            </a>
            <a 
              href="https://vercel.com/docs" 
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              Vercel Docs
            </a>
            <a 
              href="https://github.com/pinkycollie/pinkflow" 
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              PinkFlow
            </a>
          </div>
        </div>
        
        <footer className="mt-12 text-sm text-gray-500">
          <p>Built with ❤️ by the Deaf-First community</p>
          <p className="mt-2">Part of the MBTQ.dev ecosystem</p>
        </footer>
      </div>
    </main>
  )
}
