import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Blog | MBTQ.dev - PinkFlow',
  description: 'Latest updates, insights, and stories from the PinkFlow Deaf-First innovation ecosystem',
}

export default function BlogPage() {
  const posts = [
    {
      title: 'Introducing PinkFlow: A Deaf-First Innovation Ecosystem',
      date: 'December 2025',
      excerpt: 'Learn how PinkFlow is revolutionizing accessibility with a Deaf-First approach to technology and innovation.',
      slug: 'introducing-pinkflow'
    },
    {
      title: 'Building Accessible AI: Sign Language Model Testing',
      date: 'December 2025',
      excerpt: 'Explore how we test and validate sign language AI models against real accessibility standards.',
      slug: 'accessible-ai-sign-language'
    },
    {
      title: 'The Architecture Behind Next.js Standalone',
      date: 'December 2025',
      excerpt: 'Deep dive into how we use Next.js standalone output to power our marketing content engine.',
      slug: 'nextjs-standalone-architecture'
    }
  ]

  return (
    <div className="container mx-auto px-4 py-16">
      <h1 className="text-5xl font-bold mb-8 text-purple-900">Blog</h1>
      <p className="text-xl text-gray-700 mb-12">
        Updates, insights, and stories from the PinkFlow community
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {posts.map((post, index) => (
          <article key={index} className="bg-white border rounded-lg overflow-hidden hover:shadow-lg transition">
            <div className="h-48 bg-gradient-to-br from-purple-400 to-purple-600"></div>
            <div className="p-6">
              <div className="text-sm text-gray-500 mb-2">{post.date}</div>
              <h2 className="text-2xl font-semibold mb-3 text-gray-900">
                <a href={`/blog/${post.slug}`} className="hover:text-purple-600">
                  {post.title}
                </a>
              </h2>
              <p className="text-gray-600 mb-4">{post.excerpt}</p>
              <a 
                href={`/blog/${post.slug}`} 
                className="text-purple-600 font-semibold hover:underline"
              >
                Read more →
              </a>
            </div>
          </article>
        ))}
      </div>

      <div className="mt-12 text-center">
        <p className="text-gray-600">More blog posts coming soon!</p>
      </div>
    </div>
  )
}
