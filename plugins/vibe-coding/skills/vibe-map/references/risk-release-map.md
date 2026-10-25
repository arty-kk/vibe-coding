# Risk & Release Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map material release risks and verification gates to their trigger, affected contract, owner and recovery path.

Suggested saved map: `docs/risk_release_map.md`.

## Build the view

Fix the release/artifact and environment being considered. Follow changed contracts through mixed versions, migrations, rollout gates and recovery owners. For each material risk, identify the trigger, observable failure, preventive check and an evidenced rollback or forward-fix path. Distinguish a written recovery procedure from a successful recovery drill; do not mark an operator capability verified merely because a runbook names it.

## Inspect

Release docs, CI/CD workflows, deployment manifests, migrations, feature flags, config/env changes, schemas, API/event contracts, data jobs, observability, runbooks, backup/restore docs, incident notes supplied by the user, and tests/checks.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: risk `RISK-*`, release gate `REL-*`, rollout `ROL-*`, rollback `RB-*`, migration `MIG-*`, operator action `OPS-*`.
- Anchor every risk or gate to current repository evidence. Do not invent production capacity, compliance status, SLA, or operator capability.

### Coverage

Cover migrations, mixed-version compatibility, rollback/forward-fix, feature flags, provider dependencies, secrets/config, capacity/performance, data integrity, privacy/security, observability, runbooks, backup/restore, manual gates, and release blockers.

### Entry details

For each risk, capture affected contract, owner, trigger, impact, likelihood only when evidence supports it, prevention/mitigation, validation gate, rollout/rollback/forward-fix path, and residual unknowns.
