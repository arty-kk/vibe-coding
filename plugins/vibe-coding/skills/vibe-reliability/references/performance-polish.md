# Improve Performance

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

First reproduce and attribute the baseline bottleneck. Change the owning query, work structure, data access or render path, then repeat an equivalent workload with relevant normal/failure controls. Report observed distributions/resources and measurement limits rather than a single favourable run. A correctness or budget regression returns to the same owner before Patch Checking.
