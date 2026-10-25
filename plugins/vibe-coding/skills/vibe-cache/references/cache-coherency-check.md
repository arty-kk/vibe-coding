# Cache Coherency Check

## Operation

Verify the selected behavior against explicit expected results; do not change product code.

## Goal

Verify one cache coherency invariant through bounded write/read/invalidation/permission scenarios without broadening into performance tuning or unrelated refactors.

## Context

Identify selected data/resource, expected freshness and authorization behavior, implementation summary or patch boundary, safe environment, fixtures, and repository-native commands.

## Scenarios

- Populate cache, update authoritative data, and verify invalidation or TTL behavior.
- Exercise stale read and recovery behavior.
- Verify tenant/identity/role/plan/locale cache key separation where relevant.
- Exercise concurrent writes, optimistic updates, rollback, or background refresh only when part of the selected boundary.

## Execute and hand off

1. Record resource/version, key dimensions, reader principals and the allowed stale interval. Establish a cold-read control, then warm the cache.
2. Commit an authoritative update and observe invalidation/refresh and subsequent reads. With controlled time, distinguish an allowed stale response from one outside the promised window.
3. Where relevant, hold an older fill in flight across the commit/invalidation boundary and release it afterwards. Confirm it cannot restore a forbidden stale version.
4. Repeat the relevant tenant/permission/variant case and inspect the returned identity and cached state, not just a hit/miss counter.

Report passed, failed or blocked for the selected guarantee with the ordered events, versions and observed state. Pass a failure to the owning repair when authorized; rerun the failed sequence and its control after correction. A completed implementation then goes through Patch Checking.
