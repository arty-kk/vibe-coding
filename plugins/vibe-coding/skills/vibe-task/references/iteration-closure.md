# Assess Completion

## Scope

Assess the selected objective at the requested stage using its acceptance evidence and material remaining work. A local implementation, release and production recovery have different completion criteria.

## Procedure

Use the task, change and available verification results. Check required criteria against actual evidence; a passing suite alone cannot establish untested migration, user interaction or recovery behavior. Do not require a separate audit or review artifact when the requested stage does not need it.

## Decision

- **DONE:** required behavior and verification for this stage are supported; any remaining work is explicitly outside it.
- **NEXT_SLICE:** this part is complete and a previously identified dependent outcome remains.
- **REPLAN:** new evidence changes the required behavior, owner, compatibility or rollout assumptions.
- **BLOCKED:** a required decision, environment or safe action prevents completion.

Name the criteria supporting the decision and the next necessary action. Keep unavailable evidence visible and do not reopen unrelated work.
