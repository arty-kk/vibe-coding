# Improve Realtime Frontend

## Goal

Correct the selected client-state or subscription behavior under overlapping mutations, reconnect and identity changes.

## Domain rules

- Centralize query-key and entity/version rules and change every affected query, mutation, prefetch, subscription, and persistence path together.
- When the repository uses TanStack Query, use its cancellation, invalidation, mutation, structural-sharing and persistence boundaries. Otherwise use equivalent capabilities of the existing state library; do not introduce a new library merely to follow this recipe.
- Make optimistic operations concurrency-safe with operation-scoped snapshots/context and authoritative response/event reconciliation.
- Reconnect by proving continuity through sequence/resume token or fetching a fresh snapshot; bound backoff, buffers, and refetch fan-out.
- Optimize only measured dominant render/cache/network work and preserve correctness under errors, offline, hidden tabs, and unmount.

## Validation

- Run component/integration tests with deterministic query client, network/event fixtures, fake time where appropriate, and real browser profiling for performance claims.
- Exercise overlapping mutations, rollback, duplicate/out-of-order/gap events, reconnect/focus/offline, persisted-cache user switch, unmount, and slow consumer behavior.
- Compare before/after request count, cache transitions, commit duration/count, long tasks, memory, event lag, and recovery.

Repair the key, operation-scoped rollback, version/continuity or lifecycle owner without adding a second mutable server-state store. Replay the original interleaving and inspect accepted server state plus remaining optimistic operations, then feed that sequence and any measured workload to the profiling/recovery check. Recheck failures at their owner and finish Patch Checking; do not discard newer independent work merely to restore an old snapshot.
