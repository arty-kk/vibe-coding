# Terraform Plan & State Check

## Goal

Verify the selected Terraform plan preserves approved actions, backend identity and intended remote resource ownership.

## Context

Identify exact configuration revision, provider locks, backend/workspace identity, selected resource addresses, approved changes and authorized state/plan fixtures.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Initialize against a safe backend or fixture and verify backend/workspace/provider lock identity.
- Generate a saved plan from the exact change; compare expected addresses and actions; reject unapproved destruction/replacement and identify unknowns that prevent assessing the intended change.
- Exercise a moved/import refactor against representative state and prove stable remote identity.
- Model interrupted/failed apply and verify lock release, partial-state refresh, rerun convergence, and operator recovery steps.
- Run module contract/policy tests for required inputs, outputs, provider aliases, and sensitive handling.

## Verification

Compare address and remote identity, planned actions and recovery expectations. Unknown provider-computed values are not defects unless they prevent assessing the intended change.

For each affected address, compare the approved action and remote identity with the actual plan. Include an unchanged control and inspect dependent replacements rather than relying only on summary resource counts. Record whether recovery was tested with a fixture, observed in an authorized environment or only reviewed as a procedure; these establish different evidence.

Return a failing address/action pair to the repair step and repeat against a newly generated plan after correction. Missing target-state access, unresolved replacement or a stale plan stays unverified. When the relevant checks pass, hand the complete patch to Patch Checking; do not treat a review request as authorization to apply.

Saved plan/state and `terraform show -json` output can contain sensitive values. Inspect only needed metadata and redact values from reports; do not print complete state or plan JSON. See the [Terraform show reference](https://developer.hashicorp.com/terraform/cli/commands/show).
