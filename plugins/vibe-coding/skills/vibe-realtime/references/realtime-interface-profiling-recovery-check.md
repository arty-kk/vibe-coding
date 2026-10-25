# Realtime Interface Profiling & Recovery Check

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

## Execute and decide

Use deterministic server/entity versions and controllable response/event order. Establish a normal query/mutation/render control, then hold one selected response or event while a newer operation completes, fails or changes identity. Inspect the displayed entity, pending operations and cache under that exact order.

For reconnect, retain the last accepted sequence/resume identity and authoritative snapshot; inject the selected duplicate or gap and verify the actual continuity/resync result. For performance, preserve data size, event rate, device/browser and observation window, and attribute network/cache/render work separately.

Return passed, failed or blocked with the interleaving, expected/observed state and measured resource evidence. Feed a failure into the authorized owner repair, rerun its control/sequence and finish Patch Checking for changed code. A deterministic component fixture does not establish unmeasured browser responsiveness.
