import type {Metadata} from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Vibe Coding Library — Engineering workflows via MCP',
  description: 'Engineering workflows for MCP-compatible coding agents. Connect the public Streamable HTTP endpoint with no authentication or library API key.',
  metadataBase: new URL('https://vibe-coding-library.swift-seal-1081.chatgpt.site'),
  alternates: {canonical: '/'},
  icons: {icon: '/icon.png', shortcut: '/icon.png'}
};

export default function RootLayout({children}: Readonly<{children: React.ReactNode}>) {
  return <html lang="en"><body>{children}</body></html>;
}
