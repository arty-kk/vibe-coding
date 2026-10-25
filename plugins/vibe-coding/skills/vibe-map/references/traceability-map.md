# Traceability Map

## Operation

Map the requested area using current repository evidence.

## Goal

Connect selected requirements or decisions to defining code, direct contracts, tests, documentation and release gates.

Suggested saved map: `docs/traceability_map.md`.

## Build the view

Use the accepted requirement as the left-hand anchor, then join it to the rule owner, implementation path and an assertion of the same behavior. Check each join independently; a matching feature name is insufficient. Preserve requirement and test IDs already used by the project. Classify a missing owner, unimplemented requirement and absent verification as different gaps so the next audit/task addresses the actual missing edge.

## Inspect

Product docs, PRDs, README/design docs, issue text supplied by the user, existing maps, routes/components/API/jobs, schemas, tests, generated artifacts, release/deploy docs, migrations, feature flags, analytics events, and known audit outputs.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: trace row `TRC-*`, requirement `REQ-*`, invariant `INV-*`, code owner `CODE-*`, test anchor `TEST-*`, release gate `REL-*`.
- A trace row must include direct evidence for each link when available; missing links are explicit gaps, not invented references.

### Coverage

Cover requirement → owner → implementation surfaces → API/data/runtime/auth contracts → tests → docs → release/rollout gates. Include acceptance coverage, stale docs, orphan code, orphan tests, missing tests, and decisions that lack owner evidence.

### Entry details

For each trace row, capture source requirement or decision, expected behavior, implementation owners, affected contracts, tests/checks, docs/maps, release gate, residual gaps, and recommended next prompt-skill.
