# Release Readiness Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit whether a repository or selected feature is ready to ship: correctness, tests, migrations, config, deploy path, observability, security/privacy, UI states, docs, and rollback/recovery. Keep only issues supported by repository evidence and relevant to release risk.

## Inspect

Fix the candidate revision/artifact, target environment and required release criteria first. Reuse current Patch Checking and domain-check evidence only when it covers that candidate. Select the relevant categories below from changed contracts and actual release obligations; an inventory entry is not a requirement to audit every subsystem.

Changed or selected feature areas, product capability/journey/traceability maps, routes/API/jobs/workers, migrations/schemas, RBAC/ABAC and entitlements, payments, notifications, cache/search, feature flags, mobile/extension/desktop delivery surfaces, seed data, env/config, CI/deploy files, tests, docs/runbooks, logs/metrics/health checks, user-facing copy/states, security/privacy boundaries, package/lockfiles, and recent generated maps/plans if present.

## Issue classes

Look for concrete, reachable release blockers or risks in:

- Contract readiness: API/UI/job/schema drift, migration ordering, generated artifact mismatch, missing env/config, version/dependency drift, or external integration mismatch.
- Validation readiness: missing owner-level tests for changed behavior, brittle snapshots, unrun critical checks, no seed/fixture for release path, or visual/regression gaps on main surfaces.
- Operational readiness: missing health/logging/metrics for new failure path, deploy/rollback ambiguity, unsafe cleanup, background job ordering, or absent runbook for critical change.
- Product readiness: missing loading/error/empty/no-access/no-plan/destructive states, misleading copy, unsupported public claims, broken onboarding/billing/permission edge.
- Security/privacy readiness: secret/PII leakage, missing authorization enforcement, unsafe diagnostics, tenant isolation risk, or compliance-sensitive data retention/config issue.

## Finding quality

- Include expected release-safe behavior, acceptance criteria, validation direction, and whether it blocks release or can follow after release.

## Decision and recheck

Classify each required gate as passed, failed or blocked and attach the candidate/environment and observable proof. Separate accepted residual risk from an unresolved requirement; the agent cannot silently waive a gate. Return READY only for the requested release stage, otherwise name the blocker and its owner.

For authorized fixes, pass each blocker and acceptance check to its owning workflow. Recheck affected gates after repair and require a new clean Patch Checking pass for the changed candidate. Do not treat a local package build as proof of store approval, production migration, restore capability or deployment success. Assessment itself does not publish or deploy.
