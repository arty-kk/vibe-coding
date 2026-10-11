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
