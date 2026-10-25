# Migration & Refactor Plan

## Operation

Return an actionable plan for the requested outcome.

## Goal

Produce an implementation-ready migration or refactor plan that preserves behavior, data, compatibility, rollout safety, and rollback or forward-fix options. Do not edit product code.

## Plan

Use repository evidence to define current owner/contract and target owner/contract. Enumerate affected callers, readers/writers, schemas/data, generated artifacts, runtime configuration, deployments, and operators. Select an expand/migrate/contract, adapter, dual-read/write, moved-resource, versioned API/event, or other repository-native transition only when required.

Every step must have entry criteria, acceptance, validation, observability, and rollback/forward-fix. Keep unrelated cleanup outside the migration.

- Ground every step in exact `path:line[-line]` evidence and identify the authoritative owner of each moved invariant.
- Separate mechanical moves from behavior changes; do not hide product changes inside cleanup.
- Define compatibility windows, migration ordering, generated artifacts, tests, observability, deploy gates, rollback limits, and forward-fix when rollback is unsafe.
- Split independent work only when owner, rollout, rollback, and validation are truly separable.

## Handoff

Identify the first executable transition and the exact contract a downstream step may rely on after it passes acceptance. Pass that slice to Improve Refactor Boundary when execution is authorized. If a validation disproves a compatibility or data assumption, return the affected transition to this plan before continuing; do not advance a dependent rollout on the old assumption. Planning-only work ends with the plan and unresolved decisions.
