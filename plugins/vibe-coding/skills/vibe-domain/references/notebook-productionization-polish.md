# Improve Notebook Productionization

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Make the selected notebook workflow reproducible, parameterized and verifiable in its intended execution environment.

## Domain rules

- Choose the project’s supported notebook or module execution model. Extract reusable code when it improves the selected reliability or testability requirement; a notebook is not a defect by itself.
- Pin environment and data/query identity, pass secrets through the established runtime boundary, and remove hidden state/manual edits.
- Make stages idempotent or atomically published with checkpoints and cleanup for partial output.
- Add tests for transformations, schema/data quality, boundary cases, and one end-to-end representative run.
- Bound resources and publish metadata linking output to code, inputs, parameters, and environment.

## Validation

- Run top-to-bottom from a clean environment and compare deterministic outputs or documented stochastic tolerance.
- Run the relevant transformation or notebook tests and selected resource/restart/partial-failure scenarios.
- Verify published artifact lineage, freshness, privacy, and consumer compatibility; list unavailable data/scheduler gates.
