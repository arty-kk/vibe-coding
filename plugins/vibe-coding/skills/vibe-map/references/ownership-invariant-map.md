# Ownership & Invariant Map

## Operation

Map the requested area using current repository evidence.

## Goal

Connect the selected business, data, permission or runtime rules to their defining source and direct producers/consumers.

Suggested saved map: `docs/owner_invariant_map.md`.

## Build the view

Express a selected invariant as an input/state that must allow, reject or preserve a particular result. Locate where that rule is defined and enforced, then trace direct producers and consumers. Distinguish authoritative policy from derived validation and duplicated checks. When two places disagree, preserve the conflicting evidence and decision boundary instead of declaring a convenient file the owner. Link the rule to the assertion or scenario that can falsify it.

## Inspect

Schemas/models, domain services, policy engines, state machines, validators, API handlers, workers, migrations, feature flags, pricing/entitlement code, generated types, tests, docs, and runtime config.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: invariant `INV-*`, owner `OWN-*`, decision `DEC-*`, state machine `STM-*`, policy `POL-*`, producer/consumer edge `EDGE-*`.
- Anchor every invariant to its current owner with `path:line[-line]` plus symbol when possible.
- A map entry is not proof by itself. Audits and implementation tasks must re-check the owner source when stale or risky.

### Coverage

Cover permissions, tenancy, plans/quotas, lifecycle state transitions, validation rules, pricing/billing activation, idempotency rules, data integrity constraints, external provider contracts, audit logs, rollout/rollback constraints, and duplicated or ambiguous rules.

### Entry details

For each invariant, capture the owner source, human-readable rule, producers, consumers, failure/error semantics, direct tests, docs/spec links, generated artifacts, rollout/rollback notes, and known drift or duplication. Mark owner ambiguity as a first-class risk.
