# Realtime Interface Profiling & Recovery Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify the selected interface’s state convergence and measured responsiveness under concurrent changes or reconnect.

## Context

Identify actual frontend/state library, selected entity/query key, mutation/event identities, sequence or resync contract, supported browser and representative update load.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Profile a representative interaction and sustained event stream; attribute network, query-cache, reconciliation, and the actual framework’s render/commit costs separately.
- Run concurrent optimistic mutations with one delayed/failing and out-of-order responses/events; verify operation-scoped rollback and final server truth.
- Drop and resume WebSocket/SSE with duplicate/out-of-order events and a sequence gap; verify backoff, continuity proof, targeted invalidation/full resync, and bounded buffers.
- Toggle focus/online state and persisted cache across logout/login/tenant switch; verify no refetch storm or cross-user stale data.
- Saturate update frequency/list size and verify commit budget, virtualization/structural sharing, memory stability, input responsiveness, and recovery.

## Verification

Compare final authoritative and displayed state, failed-operation rollback, reconnect continuity, request count and measured framework/browser work.
