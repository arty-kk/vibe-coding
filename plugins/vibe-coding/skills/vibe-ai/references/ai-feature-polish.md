# Improve AI Feature

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Implement the selected AI feature change while preserving output validation, authorization, bounded execution and truthful user states.

## Domain rules

- Validate and normalize model output at a typed boundary before side effects or user-visible state.
- Keep authorization, tenant filters, quotas, irreversible actions, and product decisions outside model control.
- Bound attempts, tool calls, context, output size, latency, and spend; expose truthful pending/failure/fallback states.
- Version prompts/config/artifacts with affected evals, caches, docs, and rollout controls.

## Validation

- Run deterministic unit/integration/eval fixtures plus malformed output, timeout, refusal, fallback, auth, and schema cases.
- Repeat stochastic evaluations enough to report variance rather than one lucky sample.
- Record live-provider/model-version, safety review, cost, and production telemetry gates separately.
