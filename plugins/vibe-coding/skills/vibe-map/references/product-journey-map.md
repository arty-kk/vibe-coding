# Product Journey Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map the selected user journeys through observable states, decisions, completion and recovery.

Suggested saved map: `docs/product_journey_map.md`.

## Build the view

Choose the actor's initial state and completion criterion. Follow the actual navigation and state-transition owners through the selected journey, branching at decisions, denial and recovery paths. Tie each observable state to its rendering/data source and the action that leaves it. Keep implemented events separate from measured funnel results; code alone cannot establish conversion or drop-off rates.

## Inspect

Routes, navigation shells, onboarding flows, forms, email/notification triggers, billing/upgrade/downgrade states, account/team flows, settings, admin/support paths, analytics, experiments, tests, docs, feature flags, and permission/plan guards.

## Map rules

- Suggested IDs for new entries: journey `JNY-*`, step `STEP-*`, state `STATE-*`, decision `DEC-*`, event `EVT-*`, blocker `BLK-*`.
- Anchor steps to current repository evidence with `path:line[-line]` plus symbol when possible.
- Model observable states and transitions; do not invent funnel assumptions or conversion claims that are not supported by code/docs/runtime evidence.
- Treat analytics, screenshots, and docs as aids; verify critical behavior against owner code/config/tests.

## Coverage

Capture actor, trigger, entry point, step sequence, decisions, permissions/entitlements, loading/empty/error/no-access/no-plan/offline states, analytics events, notifications, cancellation/retry paths, support/recovery, tests, and open gaps.
