# Improve Infra Ops

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected runtime configuration or delivery path and verify the affected startup, failure or recovery behavior.

## Domain rules

- Keep configuration ownership singular and fail safely on missing or incompatible critical values.
- Make readiness distinct from process liveness and include graceful drain/cancel for accepted work.
- Bound retries, pools, queues, memory, and downstream concurrency; expose saturation and recovery.
- Update CI/deploy config, examples, tests, runbooks, alerts, and rollback instructions directly affected.

## Validation

- Run repository-native config/build/smoke/lifecycle checks and render generated deployment artifacts.
- Exercise restart, missing config/secret, degraded dependency, drain, and rollback where safe.
- List environment-only IAM/network/provider gates precisely.
