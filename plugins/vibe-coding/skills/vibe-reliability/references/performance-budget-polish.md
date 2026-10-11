# Improve Performance Budget

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Bring the selected path within its evidenced latency, resource or cost budget while preserving correctness.

## Domain rules

- Optimize the dominant owner and preserve end-to-end deadlines, cancellation, fairness, and failure semantics.
- Add bounded admission/backpressure before increasing concurrency or cache complexity.
- Keep measurement cheap, stable, and representative; avoid high-cardinality or per-request heavy telemetry.
- Update performance tests/budgets/docs/alerts only where the measured contract changed.

## Validation

- Re-run the same workload and report before/after distributions, resource use, and variance.
- Run correctness/failure tests for changed caching, batching, concurrency, or query behavior.
- State production topology/traffic/hardware assumptions not proven.
