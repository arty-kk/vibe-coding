# Frontend Bug Probe

## Scope

Inspect one client-state or browser behavior: fetch lifecycle, cache, form, route, effect/subscription or component contract. Use the failing state and actual framework/library; do not assume React.

## Procedure

1. Trace input/route identity through request, response, state transition and rendered result. Establish expected state from the product/API contract.
2. Check the relevant stale response, overlapping mutation, reset on identity change, duplicate event, missing cleanup or failed navigation.
3. Locate the state/query/effect owner. If authorized, correct it and its direct consumers instead of duplicating state or adding a second invalidation mechanism.
4. Preserve component props/events, accessible semantics and focus when the correction changes rendering. Inspect lint/dependency warnings rather than suppressing the violated rule.

## Verification

Use the closest component/integration/browser check to replay the trigger and a normal interaction. For hydration, use the actual server HTML and browser; a component snapshot is insufficient. Report unexercised APIs or browsers. Apply the selection/history and result rules in the parent skill.
