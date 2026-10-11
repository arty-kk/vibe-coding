# Vibe Coding Library MCP service

Two read-only tools provide the 241-workflow public library without requiring repository uploads or user accounts. Search returns up to ten concise records. Retrieval returns one complete recipe, its domain skill, the working contract and directly linked shared references; host guidance is opt-in. The compiled instruction bytes and SHA-256 hashes come from the unchanged offline library version 1.4.1.

The official TypeScript MCP SDK 2.3.1 serves both 2025 initialization-era clients and MCP 2026-07-28 self-contained requests. Inputs are strict and bounded. The HTTP entry rejects conflicting protocol headers, invalid origins and bodies over 64 KiB. There is no runtime outbound lookup or filesystem access. Errors are logged without arguments or results.

## Local development

```sh
npm ci --prefix mcp --ignore-scripts --no-audit --no-fund
python3 mcp/generate.py
npm test --prefix mcp
node mcp/run-review.js
node mcp/dev.js
```

The local endpoint binds to `127.0.0.1:3105/mcp`. `generate.py` validates catalog hashes and projects the same search engine used by the website into an ES module. `run-review.js` executes the five positive and three negative tool cases with the official client, using a real loopback server by default. Give it a public endpoint and optional report path to check deployment. This harness tests tool behavior, not natural-language model selection.

## Hosting

The deployed public endpoint is `https://vibe-coding-library.swift-seal-1081.chatgpt.site/library/mcp`. `site/app` contains the reviewed routes, console and policies for a Sites Vinext checkout. Set up the standard Sites starter in an isolated checkout, retain its build integration and configure `@modelcontextprotocol/server` 2.3.1 and Zod 4.3.6. Persist the Site's returned project ID, then stage with:

```sh
python3 mcp/generate.py
python3 mcp/stage-site.py /absolute/path/to/isolated-hosting-checkout
```

Build, source synchronization, packaging and deployment use the Sites source workflow. The hosting checkout contains the full reproducible starter and lockfile. The public read-only library runs as a regular HTTP service; it does not provision Sites' separate private MCP connection. Keep the public library's audience and privacy contract explicit. The OpenAI challenge route returns exactly the token provided by the publisher portal after domain setup; it serves 404 before configuration.

After deployment, verify the production endpoint with the same review harness, inspect the public console and record the reviewer walkthrough. Package only the explicit client-side plugin inventory with `scripts/package_openai_mcp.py`; infrastructure source, dependencies and credentials are excluded.

## Review contract

`review-cases.json` contains five positive cases and three negative cases, with exact tool inputs for deterministic replay. The package builder imports the reviewer fields and excludes the replay-only `calls` field. The walkthrough demonstrates live MCP requests and their responses through the public console. Reviewers can inspect the raw requests, source links and exact hashes.
