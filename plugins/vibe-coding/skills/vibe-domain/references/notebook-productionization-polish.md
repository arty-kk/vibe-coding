# Improve Notebook Productionization

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

Start from a clean execution that exposes the selected hidden input or partial-output failure. Correct its parameter, data/environment identity, transform or publication owner in the project's supported execution model. Run the same ordered notebook/pipeline twice under its documented deterministic or stochastic tolerance, then exercise the selected restart case. Recheck failures at that owner and finish Patch Checking on the notebook/code/config change.
