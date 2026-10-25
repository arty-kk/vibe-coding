# Cache Invalidation Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit one cache, CDN, browser cache, server cache, query cache, materialized view, or invalidation boundary for correctness, tenant safety, freshness, and failure behavior.

## Domain invariants

- Cache identity includes each dimension that changes the authorized result. Deliberately shared public data need not be fragmented by user identity.
- Invalidations or TTLs match the authoritative data change and direct consumers.
- Stale reads, optimistic updates, concurrent writes, retries, and rollback behavior are intentional.
- Sensitive or unauthorized data cannot be served from shared caches.
- Tests or checks prove freshness and coherency for the selected boundary.

## Audit method

Trace selected data from authoritative write through cache population, reads, invalidation, TTL, background refresh, client state, CDN/browser layers, and tests. Identify stale, over-broad, missing, or unsafe cache keys.

Choose a permitted freshness window and concrete resource/principal pair. Compare a cache hit with the authoritative result before and after the write commits. Include an in-flight old fill or permission change when it can race invalidation. Pass the first violated key, ordering or refresh guarantee and the exact read/write sequence to Improve Cache Invalidation; do not propose a shorter TTL without identifying why it satisfies that guarantee.
