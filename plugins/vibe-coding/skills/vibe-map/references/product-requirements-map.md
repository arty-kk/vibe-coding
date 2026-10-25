# Product Requirements Map

## Operation

Map the requested area using current repository evidence.

## Goal

Connect supplied product requirements and accepted outcomes to implemented surfaces, owners and verification.

Suggested saved map: `docs/product_requirements_map.md`.

## Build the view

Extract each requirement from the accepted decision or supplied request, preserving actor, condition and expected outcome. Link it to the implementation owner and a check of that exact outcome. Mark absent implementation, missing acceptance evidence and conflicts with current behavior as different gaps. Do not derive a new requirement from a convenient existing component or erase a requirement because the current code violates it.

## Inspect

Product specs, README/design docs, issue text supplied by the user, route/component/API behavior, analytics events, feature flags, tests, copy/localization, onboarding states, pricing/plan docs, release notes, and existing traceability or project maps.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: requirement `REQ-*`, acceptance criterion `AC-*`, persona/actor `ACT-*`, job/outcome `JOB-*`, metric `MET-*`, product state `STATE-*`, non-goal `NG-*`.
- Anchor each requirement to repository or supplied evidence. Distinguish canonical product decisions from inferred behavior and implementation details.
- Do not invent product strategy, pricing, legal policy, launch date, or metric targets. Mark missing business decisions as unknowns.

### Coverage

Cover target actors, problem statement, expected behavior, user journeys, critical states, access/plan/no-access states, success metrics, analytics events, acceptance criteria, tests, docs, implementation owners, release gates, non-goals, assumptions, and unresolved product decisions.

### Entry details

For each requirement, capture actor, trigger, expected user/system outcome, owner surface, impacted API/data/auth/runtime contracts, acceptance criteria, tests or validation route, metric/event links, release/rollout notes, and explicit exclusions.
