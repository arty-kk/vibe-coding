---
name: vibe-realtime
description: "Audit, repair or verify client query state, optimistic mutations, event continuity, reconnect and rendering costs."
---

# Realtime interfaces

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Realtime Frontend Audit → Improve Realtime Frontend → Realtime Interface Profiling & Recovery Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry entity/query and principal identity, pending operation IDs, authoritative version/event order and expected rendered state between prompts. A known race/reconnect defect starts at correction; verification-only work uses the check without editing.

Find the first wrong ownership or ordering decision across query cache, optimistic operations, responses, events and render. Correct that boundary, then replay the same delayed/failing mutation or reconnect gap alongside a normal control. Rolling back one operation must preserve successful or still-pending independent operations.

Return failed state convergence or measured resource/latency evidence to its owner, rerun affected cases and finish patch review. Distinguish server/network delay from cache churn and rendering; a faster screenshot is not a performance measurement. Missing continuity requires the accepted resync path rather than assuming reconnect filled the gap.

## Recipes

| Recipe | Operation |
|---|---|
| [Realtime Frontend Audit](references/realtime-frontend-audit.md) | audit |
| [Improve Realtime Frontend](references/realtime-frontend-polish.md) | implement |
| [Realtime Interface Profiling & Recovery Check](references/realtime-interface-profiling-recovery-check.md) | check |


Shared cache invalidation belongs to [Cache](../vibe-cache/SKILL.md); initial server rendering and hydration belong to [Web](../vibe-web/SKILL.md). This skill owns client state reconciliation and reconnect.
