export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-4xl font-bold mb-4">
          PinkFlow Auto-Deploy System
        </h1>
        <p className="text-xl mb-8 text-gray-600">
          Automatically provision and deploy React apps when customers purchase through Stripe
        </p>
        
        <div className="grid md:grid-cols-3 gap-6 mt-12">
          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-bold mb-2">1. Purchase</h2>
            <p className="text-gray-600">
              Customer completes checkout through Stripe
            </p>
          </div>
          
          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-bold mb-2">2. Provision</h2>
            <p className="text-gray-600">
              GitHub repo created from template with secrets configured
            </p>
          </div>
          
          <div className="p-6 border rounded-lg">
            <h2 className="text-2xl font-bold mb-2">3. Deploy</h2>
            <p className="text-gray-600">
              Vercel project created and app deployed automatically
            </p>
          </div>
        </div>
        
        <div className="mt-12 p-6 bg-blue-50 rounded-lg">
          <h3 className="text-lg font-semibold mb-2">Documentation</h3>
          <div className="flex flex-col gap-2">
            <a href="/AUTODEPLOY.md" className="text-blue-600 hover:underline">
              Setup Guide
            </a>
            <a href="/AUTODEPLOY_CHECKLIST.md" className="text-blue-600 hover:underline">
              Implementation Checklist
            </a>
            <a href="/SECRETS_REFERENCE.md" className="text-blue-600 hover:underline">
              Secrets Reference
            </a>
          </div>
        </div>
      </div>
    </main>
  )
}
