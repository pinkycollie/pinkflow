import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'PinkFlow Auto-Deploy',
  description: 'Auto-deploy React apps with Stripe integration',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
