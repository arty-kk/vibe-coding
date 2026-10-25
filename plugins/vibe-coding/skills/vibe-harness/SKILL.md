---
name: vibe-harness
description: "Audit, repair or verify an application's agent-run state machine, checkpoint/resume and durable effects. This concerns orchestration code, not creating assistant chats or delegating the user's task."
---

# Agent execution

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Agent Harness Audit → Improve Agent Harness → Agent Harness Replay & Failure Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry one run/step/attempt identity, transition table, effect/checkpoint boundary and expected terminal outcome between prompts. A known transition bug starts at correction; a replay-only request invokes the check without product edits.

Locate the first durable decision that can lose state, replay an effect or accept a stale worker. Correct that owner rather than adding another loop or retry layer. Reproduce the selected crash/lease/join interleaving and inspect durable effects independently of local run status.

Failure returns to the same transition/effect owner, followed by the same replay/control and final patch review. Stop at supported recovery or the exact missing store/provider/fencing evidence. Parallel branches described by this workflow are application behavior; they do not authorize this assistant to spawn agents, conversations or background work.

## Recipes

| Recipe | Operation |
|---|---|
| [Agent Harness Audit](references/agent-harness-audit.md) | audit |
| [Improve Agent Harness](references/agent-harness-polish.md) | implement |
| [Agent Harness Replay & Failure Check](references/agent-harness-replay-failure-check.md) | check |


Model selection, grounding and tool-choice quality belong to [AI](../vibe-ai/SKILL.md); wire protocol/tool discovery belongs to [MCP](../vibe-mcp/SKILL.md). This skill owns durable run state and side-effect recovery.
