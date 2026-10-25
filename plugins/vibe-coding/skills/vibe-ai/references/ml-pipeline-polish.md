# Improve ML Pipeline

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected data, training or inference path while preserving reproducible inputs and compatible model artifacts.

## Domain rules

- Fix data/split/feature ownership before tuning model complexity.
- Version code, data snapshot/query, schema, preprocessing, model, threshold, and evaluation result as one release lineage.
- Keep test data untouched by iterative selection and add slice/failure analysis where product risk is concentrated.
- Make backfill/retraining, artifact promotion, compatibility, and rollback explicit.

## Validation

- Run data-contract/quality/leakage/split tests and reproduce the selected training/evaluation path where feasible.
- Compare against baseline with uncertainty and named slices; verify artifact load and preprocessing compatibility.
- List unavailable private data, accelerator, long-running training, or production-drift gates.

Repair the selected data, preprocessing or artifact compatibility owner before retraining or tuning. Reproduce the failing observation/slice with versioned decision-time inputs and compare the fixed pipeline against the same baseline. Promote an artifact only through the requested, authorized release path after its compatibility/quality gates. Recheck failed slices at their owner, then run Patch Checking on the code/configuration change.
