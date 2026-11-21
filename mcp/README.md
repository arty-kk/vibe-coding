# Vibe Coding Library MCP service

Connect any coding agent that supports MCP over Streamable HTTP. Use `get_workflow` to select and load an engineering method from the user's ordinary goal or symptom. Cover planning, schema changes, access, diagnosis, tests, review, compatibility and rollout. Use `get_website_plan_workflow` for a website plan or `search_workflows` to compare methods. The host and model select tools. Runtime 1.7.9 serves the versioned 1.7.2 instructions.

## Codex startup

Start Codex with the MCP connection required when the first prompt should use the library.

```sh
codex -c 'mcp_servers.vibe_library.url="https://vibe-coding-library.artem-satsuk.chatgpt.site/library/mcp"' \
  -c 'mcp_servers.vibe_library.required=true'
```

Ask for the task in ordinary words once Codex starts. Keep the same settings in your MCP connection configuration for repeated use.

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

The local endpoint binds to `127.0.0.1:3105/mcp`. `generate.py` validates catalog hashes and workflow ownership and projects the same search engine used by the website into an ES module. Connect and list tools from the compact generated metadata. The service loads the instruction corpus on a tool call and prepares the search index only for a search. Give `run-review.js` a public endpoint and an optional report path to check the five positive and three negative cases through the official client.

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

Use `response_format:workflow` on both tools for purposes and structured outlines. Omit it to get the original shape on search and exact-ID calls, or the structured outline on a `get_workflow` query.

For a website plan, load the planning workflow in one call. Choose `sections` for page structure and enquiries, `offer` for audience and positioning, or `architecture` for the stack and modules.

```text
get_website_plan_workflow({"focus":"sections","language":"ru"})
get_workflow({"query":"Бэкэнд глючит, иногда ответ не приходит","language":"ru"})
get_workflow({"query":"Тесты то проходят, то падают без правок","language":"ru"})
```

Compare results with `search_workflows` when the top matches tie. If a description misses, retry with the technical area and one concrete symptom. Browse the catalog when the area is unclear.

```text
search_workflows({"view":"catalog"})
search_workflows({"view":"catalog","skill":"vibe-domain"})
search_workflows({"topic":"auth-permissions","mode":"implement","response_format":"workflow"})
get_workflow({"id":"auth-permissions-polish","response_format":"workflow"})
```

The compact catalog lists actual domain/topic keys and canonical English keywords without instruction bodies. Choose by the meaning of the user’s request; reuse known keys for the same library version. Topic lookup uses explicit membership, not an invented query term. Text search remains available, including Russian authorization forms. Unknown topic keys return catalog guidance. A miss does not authorize dropping an explicit filter. No embedding model, API key or external query processing is required. Existing requests that omit the new catalog/topic arguments retain their previous result shapes.

Match everyday symptoms by their subject and distinguishing condition. Recover longer requests that mention a catalog subject and an independent tag for the same workflow. Browse with an empty query. A description containing only generic request words yields no match. Correct words of at least five letters by one edit or one adjacent transposition when the catalog vocabulary gives an unambiguous correction. Pass exact topic and workflow IDs as identifiers.
