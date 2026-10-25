# Improve Terraform Delivery

## Goal

Correct the selected Terraform configuration or resource-address contract while preserving intended remote resource identity.

## Domain rules

- Preserve resource identity with moved/import declarations where supported and keep them long enough for all maintained state lineages.
- Make destructive or replacement behavior explicit and stage dependent/data migrations before infrastructure removal.
- Preserve the module’s documented provider contract and make inputs and aliases explicit; avoid hidden environment selection that defeats plan review.
- Pin provider/module constraints and update dependency locks intentionally; keep secrets in the established secret-delivery boundary.
- Never bypass backend locking or use routine `-target`/manual state edits to make an incomplete configuration appear converged.

## Repair sequence

1. Record the intended remote resources and allowed actions before changing configuration. For an address refactor, write the old-to-new mapping; for drift, establish whether to adopt, restore or retain externally owned behavior.
2. Change the module, configuration or CI owner of the mismatch. Preserve provider aliases, maintained module consumers and state lineage. Prefer a declarative move/import where it represents the intended operation; do not recreate a resource merely to silence a plan.
3. Generate and inspect a plan with the selected environment inputs. Compare allowed actions and remote identity, including dependent resources. Keep sensitive state/plan artifacts within the established access boundary.
4. If apply or state mutation is outside the authorized task, finish with the verified configuration and a concrete execution/recovery handoff. If execution is authorized, use the established serialized delivery path and re-plan after any partial result.

## Handoff

Give the check step the configuration revision, plan identity, address mapping, expected actions and any recovery prerequisites. Pass the patch and plan evidence to Patch Checking; a changed configuration invalidates the previous plan as evidence for that new configuration.

## Validation

- Run format, validate, repository policy/tests, and a saved plan for each directly affected environment using documented non-secret inputs.
- Inspect machine-readable or textual plan for address identity, replacement/destruction, unknowns, sensitive output, and expected resource count/change set.
- For state/refactor work, prove no unintended recreate and document backup, lock, apply order, and recovery procedure.

Saved plan/state and `terraform show -json` output can contain sensitive values. Inspect only needed metadata and redact values from reports; do not print complete state or plan JSON. See the [Terraform show reference](https://developer.hashicorp.com/terraform/cli/commands/show).
