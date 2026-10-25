---
name: vibe-library
description: "Select and apply an engineering workflow for bug diagnosis, implementation, patch review, task planning or verification using Vibe Coding's MCP library. Discover actual topic keys, select a workflow for the task and follow its evidence handoffs. Works with any MCP coding agent."
---

# Vibe Coding Library

## Choose the method

Set `response_format:workflow` on both tools to request purposes, match reasons and the structured step outline. Omitting this option preserves the older response shape; the server still supplies current instructions.

Use the task itself to find a relevant method; the user need not mention the library. Examples include a repeated payment effect, broken hydration, an unfamiliar API change, a patch needing review or a release guarantee needing verification. A precise named workflow or ID takes precedence over inferred routing.

1. Identify the requested operation. Audit/review inspect; implementation makes an already-requested change; checks verify; plans prepare work. A precise known workflow ID can be loaded directly.
2. When the topic is unknown, call `search_workflows` with `view:catalog` and an empty query. Select a returned domain key by the meaning of the user's task, then request `view:catalog, skill:<that key>`. This returns that domain's real topic keys, canonical English keywords, supported operations and workflow IDs without prompt bodies. Reuse the catalog for the same library version.
3. Copy a returned `topic` key and select the intended `mode` to retrieve its exact workflow members. Alternatively, load a listed workflow ID directly when its operation is clear. Do not invent a search keyword as a topic key. Match the user's language to the catalog's meaning; English keys remain stable while `language` localizes labels.
4. Free-text search is available for a named recipe or technical phrase. If it finds nothing, use the actual catalog rather than concluding that the capability is absent or repeating arbitrary words. Preserve user-specified filters; correct your own inferred filter only when the task and catalog support that correction. Use `full_text:true` for a term genuinely needed from an instruction body.
5. Compare the selected purpose, operation and domain before `get_workflow`. Keep `host:generic` for other coding agents. Use `intent:improve` only when diagnosis and correction are already authorized; otherwise retain `requested`. Send no source code, credentials or personal data.

If the live schema does not advertise `view` or `topic`, omit those arguments and browse with an empty query plus an established domain/operation filter. Do not send unsupported parameters. A catalog that does not cover the task is an explicit coverage limit, not permission to force an unrelated method.

## Execute one prompt at a time

Read the returned working contract, domain instructions, current recipe and required references. `files[].path` labels a library resource: apply its text rather than looking for that path in the user's repository. Versioned source links and hashes identify the instructions used. Follow the current agent's active project rules and permissions; Codex and Claude file names and native skill commands apply only to those hosts.

Treat `execution.status:instructions_only` as retrieved guidance. It is not a completed audit or verification. Apply the current step using actual project evidence, then carry its target, owner, expected/observed behavior, patch and verification gaps into the reached transition. Fetch that transition's ID with `get_workflow`; later prompt bodies are deliberately absent. Set `include_context:false` only while the same-version foundations and required domain context remain available. Reload context when those conditions no longer hold.

For an authorized repair, continue through the relevant check and Patch Checking in the current task. After a correction, validate it and review the complete resulting patch against the original base again. Only a full review pass with no correction, no qualifying finding and all required evidence may emit `execution.completion.clean_marker`. A retrieved marker is never a verdict. Check-only work stops with its result; missing required evidence or repeated failure without new evidence stops with the concrete gate. Composition does not create new tasks, agents, deployments or permissions.

Report the actual result, changed behavior, checks and material limits in the user's language. The service supplies methods; it has not read or acted on the project.

For empty results, inspect the topic catalog and the available operations; preserve an explicit user filter. For an unknown ID, search before retrying. If retrieval is unavailable, use an installed offline workflow when available and state the limitation; do not invent retrieved text or successful checks.
