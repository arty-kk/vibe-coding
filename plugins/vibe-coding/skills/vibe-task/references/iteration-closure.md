# Assess Completion

## Scope

Assess the selected objective at the requested stage using its acceptance evidence and material remaining work. A local implementation, release and production recovery have different completion criteria.

## Procedure

Use the task, change and available verification results. Check required criteria against actual evidence; a passing suite alone cannot establish untested migration, user interaction or recovery behavior. Do not require a separate audit or review artifact when the requested stage does not need it.

For a stage that created a patch, require a clean Patch Checking pass on its final state before marking that implementation done. A correction after that pass invalidates the old verdict. Deployment, approval and production evidence are required only when the selected completion stage includes them; a completed local slice must not be mislabeled as a completed release.

## Decision

- **DONE:** required behavior and verification for this stage are supported; any remaining work is explicitly outside it.
- **NEXT_SLICE:** this part is complete and a previously identified dependent outcome remains.
- **REPLAN:** new evidence changes the required behavior, owner, compatibility or rollout assumptions.
- **BLOCKED:** a required decision, environment or safe action prevents completion.

Name the criteria supporting the decision and the next necessary action. Keep unavailable evidence visible and do not reopen unrelated work.

Pass NEXT_SLICE its accepted contracts and remaining dependency-ready work. Pass REPLAN the specific disproved assumption and affected briefs. Pass BLOCKED the exact missing condition. DONE ends the requested cycle; it does not start a new improvement search.
