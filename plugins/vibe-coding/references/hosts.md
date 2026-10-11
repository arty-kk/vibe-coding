# Host integration

Use the host running this task. A product name inside a copied prompt does not switch hosts.

| Host | Project instructions | Invocation |
|---|---|---|
| Codex | Active `AGENTS.md` files and scoped rules | `$vibe-review` or the plugin picker |
| Claude Code | Active `CLAUDE.md`, `.claude/CLAUDE.md` and loaded `.claude/rules/` | `/vibe-coding:vibe-review` |
| Claude Cowork/cloud | Instructions and tools actually supplied by that workspace | The enabled plugin skill picker or exposed namespace |

The entry skill is `$vibe` in Codex and `/vibe-coding:vibe` in Claude Code. These are assistant invocations, not shell commands. Honor `AGENTS.md` in Claude only when the host loads it or the project explicitly adopts it; it does not supersede Claude's active rules. Keep the host's normal instruction precedence and permissions.

## Paths and tools

Resolve a reference relative to the instruction file containing its link, using the installed plugin directory exposed by the host. Project code stays in the task's repository. Do not resolve plugin links from the project root or edit installed caches. `agents/openai.yaml` contains Codex discovery metadata; it is not a set of Claude agents.

Use the session's exposed file, terminal, browser and service tools. Do not translate a recipe into unavailable Codex app APIs, Claude hooks or a background scheduler. A local Claude Code installation does not enable the plugin in a claude.ai account or Cowork workspace.

In Cowork/cloud, use shared project files and return artifacts through the available output surface. A local path or connector document is not automatically an editable checkout. If execution lacks a required repository, runtime, browser or provider, report that verification gap; do not infer a runtime pass from chat-only inspection.
