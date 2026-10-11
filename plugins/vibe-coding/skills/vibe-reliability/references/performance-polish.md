# Improve Performance

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Improve the measured bottleneck in the selected path and compare equivalent before/after workloads.

## Domain rules

- Change the limiting owner rather than hiding latency with unbounded concurrency, cache, retry, or batching.
- Preserve cancellation, deadlines, fairness, memory bounds, and failure visibility.
- Keep cache keys, invalidation, query semantics, and result ordering explicit when optimization changes data access.
- Remove temporary profiling noise or gate it safely before completion.

## Validation

- Re-run the same measurement shape and report before/after evidence with variance and environment limits.
- Run correctness tests for the optimized path and representative failure/cancellation cases.
- Inspect resource ceilings and downstream call amplification under bounded concurrency.
