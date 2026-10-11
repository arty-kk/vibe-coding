---
name: vibe-library
description: "Find and load a Vibe Coding engineering workflow when the user invokes the library, asks which workflow fits a task, or requests a named recipe. Use the public MCP catalog; do not activate for every coding task."
---

# Vibe Coding Library

1. Identify the requested result and domain. Audit and review mean inspection; implement means authorized changes; check means verification. Preserve an explicit named workflow or ID.
2. Use `search_workflows` with concise technical keywords. Set `mode` only when the requested operation is clear; use a returned `skill` identifier to narrow an ambiguous domain. Choose the user's catalog language. Search instruction bodies only when catalog search is insufficient. Do not send source code, credentials or personal data.
3. Select the closest workflow by its title, domain and operation. Ask only when competing workflows require a decision that changes the result. Call `get_workflow` for that stable ID; select `host` only when the current environment is known.
4. Apply the returned working contract, domain skill and selected recipe using the user's project tools and permissions. Read the supplied instruction files once. `files[].path` identifies a library resource; use its returned text rather than resolving it from the user's repository. Source links identify versioned originals. Invocation examples for the full offline plugin apply only when those skills are installed. Follow `AGENTS.md` in Codex and the active `CLAUDE.md` and loaded rules in Claude.
5. For a linked alternative recipe, search and load that recipe only if the task needs it. Report actual changes, checks and limitations in the user's language. These tools supply guidance; repository evidence comes from the environment where the agent works.

For empty search results, revise the domain keywords or filter. For an unknown ID, search before retrying. If the server is unavailable, use an installed offline Vibe Coding skill when available and state the retrieval limitation; do not invent retrieved instructions or a successful check.
