# Redis Queue Load & Recovery Check

## Goal

Verify the selected Redis-backed job or stream’s effect, lease and recovery guarantee within its resource limits.

## Context

Identify Redis version/topology and the actual framework (Streams, BullMQ or ARQ), selected job, identity/lease/ack policy, retry/retention limits and expected effect.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Duplicate the same job/operation and crash around side effect/completion; prove stable idempotency and terminal state.
- Expire a BullMQ lock or Stream ownership during long work and verify stall/reclaim does not permit stale double completion.
- Exercise BullMQ flow child failure/rate limit and ARQ retry/defer/cron overlap using deterministic time where possible.
- Restart workers and interrupt Redis connectivity; verify bounded reconnect, no connection storm, pending recovery, and graceful shutdown.
- Drive representative backlog and payload size; measure memory/eviction, command latency, queue age, cleanup, and downstream backpressure.

## Verification

Compare job/stream state, durable effect count, pending or stalled ownership, connection/memory bounds and recovery using the selected framework’s semantics.

## Execute and decide

Use dedicated keys/queues and a controlled durable effect keyed by logical operation. Establish normal enqueue/processing/completion, then hold the selected effect/ack/lock-renewal boundary before interruption, expiry or reclaim.

After recovery, inspect framework ownership/status, actual attempts, business effects and retained deduplication state. A stale worker's completion being rejected does not prove its external effect was prevented. If cleanup permits job-ID reuse, compare that behavior with the separate business-operation contract. For load, preserve payload distribution, concurrency and measurement window.

Return passed, failed or blocked with framework, event order, effects and resource evidence. Pass a failure to the authorized owner repair, replay its control/history after correction and finish Patch Checking. Failover, retention mutation and backlog drills require a suitable test environment.
