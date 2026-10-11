# Improve Terraform Delivery

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected Terraform configuration or resource-address contract while preserving intended remote resource identity.

## Domain rules

- Preserve resource identity with moved/import declarations where supported and keep them long enough for all maintained state lineages.
- Make destructive or replacement behavior explicit and stage dependent/data migrations before infrastructure removal.
- Preserve the module’s documented provider contract and make inputs and aliases explicit; avoid hidden environment selection that defeats plan review.
- Pin provider/module constraints and update dependency locks intentionally; keep secrets in the established secret-delivery boundary.
- Never bypass backend locking or use routine `-target`/manual state edits to make an incomplete configuration appear converged.

## Validation

- Run format, validate, repository policy/tests, and a saved plan for each directly affected environment using documented non-secret inputs.
- Inspect machine-readable or textual plan for address identity, replacement/destruction, unknowns, sensitive output, and expected resource count/change set.
- For state/refactor work, prove no unintended recreate and document backup, lock, apply order, and recovery procedure.

Saved plan/state and `terraform show -json` output can contain sensitive values. Inspect only needed metadata and redact values from reports; do not print complete state or plan JSON. See the [Terraform show reference](https://developer.hashicorp.com/terraform/cli/commands/show).
