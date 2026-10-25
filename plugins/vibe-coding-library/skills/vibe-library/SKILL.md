---
name: vibe-library
description: "Select and apply an engineering workflow for bug diagnosis, implementation, patch review, task planning or verification using Vibe Coding's MCP library. Search from the task's goal or a named recipe, load the current prompt and follow its evidence handoffs. Works with any MCP coding agent."
---

# Vibe Coding Library

## Choose the method

Set `response_format:workflow` on both tools to request purposes, match reasons and the structured step outline. Omitting this option preserves the older response shape; the server still supplies current instructions.

Use the task itself to find a relevant method; the user need not mention the library. Examples include a repeated payment effect, broken hydration, an unfamiliar API change, a patch needing review or a release guarantee needing verification. A precise named workflow or ID takes precedence over inferred routing.

1. Identify the requested result and owning domain. Audit/review inspect; implementation makes an already-requested change; checks verify; plans prepare work. An audit-only request does not become a repair because related prompts exist.
2. Call `search_workflows` with a short technical goal or symptom, such as `fix stale cache after a write`, `verify Kafka consumer rebalance` or `Patch Check`. Set `mode` only when clear and `skill` only for an established domain. `language` localizes results without filtering out other corpus languages. Use `full_text:true` for an instruction-body term when metadata is insufficient. Send no source code, secrets or personal data.
3. Compare each result's purpose, operation and domain, using its match reason to distinguish an exact name from a body-only match. Load the best stable ID with `get_workflow`; ask only when alternatives require a decision that changes the outcome. Keep `host:generic` for other coding agents. Use `intent:improve` only when diagnosis and correction are already authorized; otherwise retain `requested`. A known fix may start at its implementation ID.

## Execute one prompt at a time

Read the returned working contract, domain instructions, current recipe and required references. `files[].path` labels a library resource: apply its text rather than looking for that path in the user's repository. Versioned source links and hashes identify the instructions used. Follow the current agent's active project rules and permissions; Codex and Claude file names and native skill commands apply only to those hosts.

Treat `execution.status:instructions_only` as retrieved guidance. It is not a completed audit or verification. Apply the current step using actual project evidence, then carry its target, owner, expected/observed behavior, patch and verification gaps into the reached transition. Fetch that transition's ID with `get_workflow`; later prompt bodies are deliberately absent. Set `include_context:false` only while the same-version foundations and required domain context remain available. Reload context when those conditions no longer hold.

For an authorized repair, continue through the relevant check and Patch Checking in the current task. After a correction, validate it and review the complete resulting patch against the original base again. Only a full review pass with no correction, no qualifying finding and all required evidence may emit `execution.completion.clean_marker`. A retrieved marker is never a verdict. Check-only work stops with its result; missing required evidence or repeated failure without new evidence stops with the concrete gate. Composition does not create new tasks, agents, deployments or permissions.

Report the actual result, changed behavior, checks and material limits in the user's language. The service supplies methods; it has not read or acted on the project.

For empty results, refine the technical terms or enable body search; preserve an explicit filter unless it was mistaken. For an unknown ID, search before retrying. If retrieval is unavailable, use an installed offline workflow when available and state the limitation; do not invent retrieved text or successful checks.
