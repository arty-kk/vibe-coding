---
name: vibe-harness
description: "Audit, repair or verify application agent-run state, checkpoint/resume, bounded parallel work and durable effects."
---

# Agent execution

Apply [the working contract](../../references/workflow.md) once; read only the recipe for the requested result.

## Recipes

| Recipe | Operation |
|---|---|
| [Agent Harness Audit](references/agent-harness-audit.md) | audit |
| [Improve Agent Harness](references/agent-harness-polish.md) | implement |
| [Agent Harness Replay & Failure Check](references/agent-harness-replay-failure-check.md) | check |


Model selection, grounding and tool-choice quality belong to [AI](../vibe-ai/SKILL.md); wire protocol/tool discovery belongs to [MCP](../vibe-mcp/SKILL.md). This skill owns durable run state and side-effect recovery.
