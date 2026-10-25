# Improve Cache Invalidation

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Restore the selected cache freshness or invalidation guarantee from the authoritative write through directly affected readers.

## Scope selection

Use the selected data/resource, stale-read bug, cache key, audit finding, failing test, or explicit performance/correctness task. Do not replace the whole caching strategy unless the selected fix requires a refactor plan.

## Change targets

- Cache key construction and tenant/identity/role/locale/plan dimensions.
- Write-side invalidation, event-based refresh, TTL/stale-while-revalidate, optimistic update reconciliation, and rollback behavior.
- Server/client/CDN/browser cache readers directly affected.
- Tests/fixtures proving fresh, stale, unauthorized, and concurrent states.

## Implementation principles

- Preserve the authoritative data source and avoid masking owner-layer bugs with local cache workarounds.
- Prefer targeted invalidation over broad flushes unless the repository already uses broad invalidation safely.
- Avoid serving protected data from shared caches.
- Keep performance and correctness validation explicit.

## Validation

Run repository-native tests and bounded scenarios for write → read freshness, stale cache, concurrent update, permission/tenant change, logout/session change, and rollback where relevant. Report CDN/managed-cache gates honestly.

Correct key construction, write-side invalidation or refresh/version ownership at the first violating boundary. Reproduce the old fill/commit/read ordering with controlled time or synchronization; observe actual cached and authoritative versions separately. Feed the resulting patch and sequence into Cache Coherency Check. A failure returns to the same owner; a passing scenario proceeds to Patch Checking without broad production flushes.
