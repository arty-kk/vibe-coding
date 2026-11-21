# Vibe Coding Library MCP service

Two read-only tools provide engineering methods to coding agents that support MCP over Streamable HTTP. Start a relevant task by searching for the user's ordinary goal or symptom, then load a matching workflow. The host and model select tools. Runtime 1.7.3 serves the versioned 1.7.2 instructions.

Explicit composition in `plugins/vibe-coding/workflows.json` preserves all 260 IDs. Read-only requests stay read-only; authorized corrections carry evidence through repair, relevant checks and repeated Patch Checking. Later prompts load when reached. `include_context:false` reuses available same-version foundations. Missing required evidence and repeated unchanged failure cannot become a clean verdict.

The canonical browser engine is `plugins/vibe-coding/assets/catalog/engine.js`. The public site uses an identical copy, and the CLI uses equivalent Python ranking. Search preserves exact IDs and filters, recognizes task goals in the supported languages, and can retry an empty metadata search using the request's known terms. Body search is explicit in MCP and the public site. The offline catalog and CLI also search instruction bodies.

The official TypeScript MCP SDK 2.3.1 serves both 2025 initialization-era clients and MCP 2026-07-28 self-contained requests. Inputs are strict and bounded. The HTTP entry rejects conflicting protocol headers, invalid origins and bodies over 64 KiB. There is no runtime outbound lookup or filesystem access. Errors are logged without arguments or results.

## Local development

```sh
npm ci --prefix mcp --ignore-scripts --no-audit --no-fund
python3 mcp/generate.py
npm test --prefix mcp
node mcp/run-review.js
node mcp/dev.js
```

The local endpoint binds to `127.0.0.1:3105/mcp`. `generate.py` validates catalog hashes and workflow ownership and projects the same search engine used by the website into an ES module. `run-review.js` executes the five positive and three negative tool cases with the official client, using a real loopback server by default. Give it a public endpoint and optional report path to check deployment. This harness tests tool behavior, not natural-language model selection.

## Hosting

The deployed public endpoint is `https://vibe-coding-library.artem-satsuk.chatgpt.site/library/mcp`. `site/app` contains the reviewed routes, console and policies for a Sites Vinext checkout. Set up the standard Sites starter in an isolated checkout, retain its build integration and configure `@modelcontextprotocol/server` 2.3.1 and Zod 4.3.6. Persist the Site's returned project ID, then stage with:

```sh
python3 mcp/generate.py
python3 mcp/stage-site.py /absolute/path/to/isolated-hosting-checkout
```

Build, source synchronization, packaging and deployment use the Sites source workflow. The hosting checkout contains the full reproducible starter and lockfile. The public read-only library runs as a regular HTTP service; it does not provision Sites' separate private MCP connection. Keep the public library's audience and privacy contract explicit. The OpenAI challenge route returns exactly the token provided by the publisher portal after domain setup; it serves 404 before configuration.

After deployment, verify the production endpoint with the same review harness, inspect the public console and record the reviewer walkthrough. Package only the explicit client-side plugin inventory with `scripts/package_openai_mcp.py`; infrastructure source, dependencies and credentials are excluded.

## Review contract

`review-cases.json` contains five positive cases and three negative cases, with exact tool inputs for deterministic replay. The package builder imports the reviewer fields and excludes the replay-only `calls` field. The walkthrough demonstrates live MCP requests and their responses through the public console. Reviewers can inspect the raw requests, source links and exact hashes.

Use `response_format:workflow` on both tools for the current purposes and structured outline. Calls that omit the option retain the exact 1.5.1 response shape while still using current search and instruction content; this keeps previously published schemas working during continuous review.

Search with a brief description of the user's goal. Load the matching ID.

```text
search_workflows({"query":"Хочу красивый сайт для студии. Какие разделы нужны?","language":"ru","response_format":"workflow"})
get_workflow({"id":"web-page-architecture","language":"ru","response_format":"workflow"})
```

Use the catalog when a description produces no useful match or the caller wants to explore the available topics.

```text
search_workflows({"view":"catalog"})
search_workflows({"view":"catalog","skill":"vibe-domain"})
search_workflows({"topic":"auth-permissions","mode":"implement","response_format":"workflow"})
get_workflow({"id":"auth-permissions-polish","response_format":"workflow"})
```

The compact catalog lists actual domain/topic keys and canonical English keywords without instruction bodies. Choose by the meaning of the user’s request; reuse known keys for the same library version. Topic lookup uses explicit membership, not an invented query term. Text search remains available, including Russian authorization forms. Unknown topic keys return catalog guidance. A miss does not authorize dropping an explicit filter. No embedding model, API key or external query processing is required. Existing requests that omit the new catalog/topic arguments retain their previous result shapes.

Text typo repair uses only the actual metadata vocabulary and registered concepts: words of at least five letters may be corrected by one edit or an adjacent transposition when the semantic target is unambiguous. Exact topic/workflow ID arguments are never fuzzy-corrected. Unknown or ambiguous phrases remain eligible for catalog-guided selection by the caller.
