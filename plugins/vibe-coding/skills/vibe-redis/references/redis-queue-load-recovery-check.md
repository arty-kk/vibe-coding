# Redis Queue Load & Recovery Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

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
