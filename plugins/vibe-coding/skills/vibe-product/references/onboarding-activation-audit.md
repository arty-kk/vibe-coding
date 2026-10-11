# Onboarding Activation Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit the path from first entry to meaningful activation: public entry, signup/login, first-run state, workspace/project setup, permissions, plan gates, sample data, checklist/progress, handoff into core workflow, and activation measurement. Keep only issues supported by repository evidence.

## Inspect

Public routes, auth flows, onboarding routes/components, empty states, setup wizards, workspace/project/team creation, invitations, plan/trial/quota gates, seed/demo/sample data, emails/notifications, analytics events, feature flags, docs, tests, and navigation maps.

## Issue classes

- Entry-to-value continuity: unclear next step, dead ends after signup/login, missing first-run state, inconsistent redirect, setup steps not aligned with core workflow.
- Setup correctness: workspace/project/team/role/plan context not established, sample data conflicts with permissions, incomplete defaults, or invalid states after partial setup.
- Activation clarity: checklist/progress/CTA copy does not match implemented behavior, success state lacks next step, upgrade/trial/no-access states block without explanation.
- Recovery: failed invite/payment/setup/import/integration states lose user input or do not provide a safe retry path.
- Measurement: activation-critical events missing, duplicated, fired before success, leaking PII, or impossible to connect to funnel state using existing instrumentation patterns.
- Regression resistance: no tests/previews for primary first-run path, stale docs, or route guards that make onboarding fragile.

## Finding quality

- Include affected role/plan/tenant state, expected behavior, acceptance criteria, and validation direction.
- Merge symptoms that share the same onboarding owner/source of truth.
