---
name: vibe-cache
description: "Audit, repair or verify shared cache identity, invalidation and freshness. Redis job delivery belongs to vibe-redis."
---

# Caching & freshness

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Cache Invalidation Audit → Improve Cache Invalidation → Cache Coherency Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Start with the selected stale/unauthorized result and the authoritative record version. Trace its write/commit, cache identity, invalidation and readers before choosing a TTL or flush. A known fix starts at implementation; a verification-only request starts at the coherency check and does not edit.

Pass the resource/key dimensions, freshness window, commit/invalidation order and reproducing read sequence into correction. Re-run that sequence with a normal reader and another relevant principal/variant. A stale fill after invalidation or a permission leak returns to the same key/refresh owner. Preserve intentionally allowed stale behavior rather than treating every cached old value as a defect.

Finish when the selected freshness/access guarantee is supported and the changed patch completes its review loop. A managed CDN/cache that cannot be exercised remains a named gate; clearing a cache once does not prove invalidation is repaired.

## Recipes

| Recipe | Operation |
|---|---|
| [Cache Coherency Check](references/cache-coherency-check.md) | check |
| [Cache Invalidation Audit](references/cache-invalidation-audit.md) | audit |
| [Improve Cache Invalidation](references/cache-invalidation-polish.md) | implement |


Client optimistic state and reconnect belong to [Realtime](../vibe-realtime/SKILL.md); server rendering and serialized responses belong to [Web](../vibe-web/SKILL.md). This skill owns shared cache identity, invalidation and freshness.
