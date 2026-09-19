# Installation

## Public marketplace

```sh
codex plugin marketplace add arty-kk/vibe-coding
```

Open the desktop Plugins Directory, select the Vibe Coding source and install Vibe Coding. Start a new task. On hosts exposing `codex plugin add`, the plugin identifier is `vibe-coding@vibe-coding`.

## Fixed release

```sh
codex plugin marketplace add arty-kk/vibe-coding --ref v1.0.3
```

## Local checkout

```sh
git clone https://github.com/arty-kk/vibe-coding.git
codex plugin marketplace add ./vibe-coding
```

The repository marketplace lives at `.agents/plugins/marketplace.json`; its `./plugins/vibe-coding` source resolves relative to the repository root. The plugin ZIP contains the plugin folder only. Clone the repository when you need a complete marketplace source.

## Update

```sh
codex plugin marketplace upgrade vibe-coding
```

Install the updated plugin through the desktop Plugins Directory and start a new task. A marketplace pinned to a release stays on that release; select a newer ref to advance it. Edit the source checkout during development, then reinstall; installed cache contents are managed by the host.
