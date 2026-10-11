# Improve Model Serving & Monitoring

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected model-serving path, preserving artifact identity, bounded load, fallback semantics and rollout checks.

## Domain rules

- Make artifact and preprocessing identity immutable for a deployment and surface it in logs/metrics/traces.
- Bound queueing, batch wait, concurrency, memory, retries, and fallback; shed load explicitly rather than amplifying it.
- Use canary/shadow/flag rollout only with comparison metrics, isolation, and rollback criteria.
- Keep monitoring tied to the decision contract and avoid raw sensitive inputs/outputs in telemetry.

## Validation

- Run load/concurrency/cancel/fallback/artifact-compatibility tests with representative inputs.
- Verify readiness, rollout, rollback/disable, and one degraded-dependency trace.
- Report production traffic, hardware, provider quota, and long-window drift gates separately.
