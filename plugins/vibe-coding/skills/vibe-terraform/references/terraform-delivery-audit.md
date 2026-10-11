# Terraform Delivery Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit Terraform ownership from configuration and module contracts through state, plan review, apply serialization, refactor, and recovery.

## Domain invariants

- Each environment has an explicit backend/state identity, access boundary, encryption/retention policy, and locking or apply-serialization mechanism.
- Module inputs, outputs, provider requirements, resource addresses, lifecycle rules, and ownership form a stable public contract rather than leaking environment internals.
- The reviewed plan is generated from the exact commit, variable set, workspace/backend, provider lock file, and credentials intended for apply.
- Destroy, replacement, force-new, unknown, sensitive, and externally managed fields are surfaced explicitly; targeted apply is not used as routine convergence.
- Address refactors use declarative moved/import mechanisms or a reviewed state operation so identity is preserved instead of recreating live resources.
- Provider and module versions are constrained and locked; credentials and sensitive values do not enter code, state outputs, plan logs, or generated artifacts unnecessarily.
- Drift is classified as desired adoption, intentional external ownership, or unauthorized change before configuration is modified.
- Interrupted apply, partial provider success, lock loss, and rollback/forward-fix behavior have an operator-safe recovery path.

## Audit method

1. Map configuration addresses, module boundaries, provider aliases, backend/workspace, variable sources, generated plan, state ownership, and apply identity.
2. Inspect the exact plan for replacements, destroys, unknown values, dependency order, lifecycle suppression, sensitive exposure, and cross-environment references.
3. Compare configuration, state, and provider reality for the selected resources; classify drift without blindly importing or overwriting it.
4. For refactors, prove old-to-new address identity and determine whether moved/import blocks or a controlled state operation is required.
5. Trace CI approvals, concurrency/locking, artifact retention, credentials, failure notification, and recovery after partial apply.

Saved plan/state and `terraform show -json` output can contain sensitive values. Inspect only needed metadata and redact values from reports; do not print complete state or plan JSON. See the [Terraform show reference](https://developer.hashicorp.com/terraform/cli/commands/show).
