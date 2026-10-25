---
name: vibe-redis
description: "Audit, repair or verify Redis Streams, BullMQ or ARQ job identity, leases, acknowledgment, retention and recovery."
---

# Redis & queues

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Redis Job Queues Audit → Improve Redis Job Queues → Redis Queue Load & Recovery Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry framework/version/topology, key/job/operation identity, lease/ack policy, retention and expected durable effect between prompts. A known recovery defect starts at implementation; a check-only request does not alter production queue state.

Trace enqueue → claim/lock → effect → completion/ack → retention/replay using Streams, BullMQ or ARQ semantics actually present. Correct the first identity, ownership, completion or resource boundary, then replay the same crash/expiry sequence with a normal control.

Inspect business effects independently of pending/stalled/complete flags. A reclaimed lease or retained job ID alone cannot prove that a stale worker stopped or that effects remain deduplicated after cleanup. Return failed evidence to its owner, recheck and finish patch review. Keep queue persistence guarantees separate from reconstructible cache behavior.

## Recipes

| Recipe | Operation |
|---|---|
| [Redis Job Queues Audit](references/redis-job-queues-audit.md) | audit |
| [Improve Redis Job Queues](references/redis-job-queues-polish.md) | implement |
| [Redis Queue Load & Recovery Check](references/redis-queue-load-recovery-check.md) | check |
