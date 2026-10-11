---
name: vibe-realtime
description: "Audit, repair or verify client query state, optimistic mutations, event continuity, reconnect and rendering costs."
---

# Realtime interfaces

Apply [the working contract](../../references/workflow.md) once; read only the recipe for the requested result.

## Recipes

| Recipe | Operation |
|---|---|
| [Realtime Frontend Audit](references/realtime-frontend-audit.md) | audit |
| [Improve Realtime Frontend](references/realtime-frontend-polish.md) | implement |
| [Realtime Interface Profiling & Recovery Check](references/realtime-interface-profiling-recovery-check.md) | check |


Shared cache invalidation belongs to [Cache](../vibe-cache/SKILL.md); initial server rendering and hydration belong to [Web](../vibe-web/SKILL.md). This skill owns client state reconciliation and reconnect.
