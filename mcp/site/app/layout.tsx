import type {Metadata} from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Vibe Coding Library — Engineering workflows via MCP',
  description: 'Search 241 engineering workflows and load only the selected working context. A public, read-only MCP server for Codex, Claude Code and compatible clients.',
  metadataBase: new URL('https://vibe-coding-library.swift-seal-1081.chatgpt.site'),
  alternates: {canonical: '/'},
  icons: {icon: '/icon.png', shortcut: '/icon.png'}
};

export default function RootLayout({children}: Readonly<{children: React.ReactNode}>) {
  return <html lang="en"><body>{children}</body></html>;
}
