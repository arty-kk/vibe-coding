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

First reproduce the failed boundary using the smallest safe case. Correct the owning parser, prompt, context builder, policy or product-state transition, then replay the same input and its relevant refusal/error control. Compare semantic changes on the same evaluation inputs rather than a newly favourable example. A failed case returns to that owner; supported acceptance proceeds to Patch Checking on the full change.
