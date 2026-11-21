---
name: vibe-library
description: "Select a workflow for planning a website or codebase, changing data or permissions, diagnosing a defect, stabilizing tests, reviewing a patch, or preparing a release. Load the current method from the user's ordinary request."
---

# Vibe Coding Library

## Choose the method

Use the ordinary request to choose a workflow. Cover planning, implementation, diagnosis, review, and verification in the task's domain. For website sections and enquiries, start at `web-page-architecture`. Choose `web-offer-synthesis` for an undefined offer or `web-project-architecture` for a stack or modular code structure. Choose `homepage-landing-build` for a build, `homepage-landing-polish` for a redesign, and `homepage-landing-audit` for inspection. Diagnose a vague backend hang with `instant-backend-probe`.

1. Identify the requested operation and preserve its scope. Keep planning and inspection read-only. Use `intent:improve` when the user has authorized both diagnosis and repair.
2. Load website planning with `get_website_plan_workflow` when the client exposes it. Choose the focus according to the task. For other tasks or older clients, load a known matching ID with `get_workflow`. Pass the brief goal in `query` if the live schema offers it. Otherwise search the ordinary goal with `search_workflows`, compare purpose and operation, and load the matching ID.
3. Browse with `view:catalog` and an empty query when several results fit or the first search is empty. Select a returned domain and topic key. Preserve explicit filters. Use `full_text:true` for a term needed from an instruction body.
4. Request `response_format:workflow` for the current step and conditional outline. Keep `host:generic` for other MCP agents. Send a public technical goal or symptom and omit source code, credentials, and personal data.

If the live schema does not advertise `view` or `topic`, omit those arguments and browse with an empty query plus an established domain/operation filter. Do not send unsupported parameters. A catalog that does not cover the task is an explicit coverage limit, not permission to force an unrelated method.

If a visible domain key is rejected by a cached connector enum, search by a short goal without the inferred `skill` argument. Use at most ten hits. Preserve explicit user constraints by checking the returned method's domain and operation before loading it.

## Execute one prompt at a time

Read the returned working contract, domain instructions, current recipe and required references. `files[].path` labels a library resource: apply its text rather than looking for that path in the user's repository. Versioned source links and hashes identify the instructions used. Follow the current agent's active project rules and permissions; Codex and Claude file names and native skill commands apply only to those hosts.

Treat `execution.status:instructions_only` as retrieved guidance. It is not a completed audit or verification. Apply the current step using actual project evidence, then carry its target, owner, expected/observed behavior, patch and verification gaps into the reached transition. Fetch that transition's ID with `get_workflow`; later prompt bodies are deliberately absent. Set `include_context:false` only while the same-version foundations and required domain context remain available. Reload context when those conditions no longer hold.

For an authorized repair, continue through the relevant check and Patch Checking in the current task. After a correction, validate it and review the complete resulting patch against the original base again. Only a full review pass with no correction, no qualifying finding and all required evidence may emit `execution.completion.clean_marker`. A retrieved marker is never a verdict. Check-only work stops with its result; missing required evidence or repeated failure without new evidence stops with the concrete gate. Composition does not create new tasks, agents, deployments or permissions.

Report the actual result, changed behavior, checks and material limits in the user's language. The service supplies methods; it has not read or acted on the project.

For empty results, inspect the topic catalog and the available operations; preserve an explicit user filter. For an unknown ID, search before retrying. If retrieval is unavailable, use an installed offline workflow when available and state the limitation; do not invent retrieved text or successful checks.
