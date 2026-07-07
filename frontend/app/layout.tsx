// Import the Analytics component from the Vercel Analytics package
import { Analytics } from '@vercel/analytics/next'
// Import only the TypeScript types Metadata and Viewport from Next.js
import type { Metadata, Viewport } from 'next'
// Import the global stylesheet for the entire application
import './globals.css'

// Export metadata information about the website
export const metadata: Metadata = {
  title: 'Enterprise AI Knowledge Assistant',
  description: 'Premium RAG chatbot with vector database integration, cross-encoder reranking, and intelligent document retrieval',
  // Configure website icons
  icons: {
    // List of favicon icons
    icon: [
      {
        // Light mode favicon
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        // Dark mode favicon
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        // SVG favicon
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    // Apple Touch Icon
    apple: '/apple-icon.png',
  },
}

// Export viewport settings
export const viewport: Viewport = {
  colorScheme: 'dark',
  themeColor: [
    {
      media: '(prefers-color-scheme: dark)',
      color: '#0a0e27',
    },
  ],
}

// Export the main layout component
export default function RootLayout({
  // Receive the page that should be displayed inside the layout
  children,
  // Ensure that the children prop is read-only and cannot be modified
}: Readonly<{
  // Children can be any valid React element
  children: React.ReactNode
}>) {
  // Return the HTML structure of the application
  return (
    // Root HTML element
    <html lang="en" className="bg-background dark">
      <body className="antialiased bg-background text-foreground">
        {/* Render the current page */}
        {children}
        {/* Render Analytics only in production */}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}