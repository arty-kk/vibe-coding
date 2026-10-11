---
name: vibe-cache
description: "Audit, repair or verify shared cache identity, invalidation and freshness. Redis job delivery belongs to vibe-redis."
---

# Caching & freshness

Apply [the working contract](../../references/workflow.md) once; read only the recipe for the requested result.

## Recipes

| Recipe | Operation |
|---|---|
| [Cache Coherency Check](references/cache-coherency-check.md) | check |
| [Cache Invalidation Audit](references/cache-invalidation-audit.md) | audit |
| [Improve Cache Invalidation](references/cache-invalidation-polish.md) | implement |


Client optimistic state and reconnect belong to [Realtime](../vibe-realtime/SKILL.md); server rendering and serialized responses belong to [Web](../vibe-web/SKILL.md). This skill owns shared cache identity, invalidation and freshness.
