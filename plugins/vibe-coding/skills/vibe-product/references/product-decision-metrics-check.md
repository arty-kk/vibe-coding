# Product Decision & Metrics Check

## Goal

Verify one selected product decision, requirement, journey step, or metric/event contract through bounded evidence. This check proves alignment; it does not redesign the product or perform a broad audit.

## Context

Identify the product decision or requirement, target actor/state, expected behavior, metric/event or acceptance criterion, safe environment, and validation route. If the required decision is missing or contradictory, return `blocked`.

## Check scenarios

Exercise or inspect only the selected contract:

- happy path and relevant empty/error/no-access/no-plan/over-quota/destructive states;
- UI/API/backend consistency for the same actor and scope;
- analytics event name/properties/timing/dedup/identity when metrics are part of the requirement;
- copy/docs claims against observable behavior;
- test or preview evidence for the defined behavior.

## Execute and decide

Bind the decision/criterion to its defining source and select one representative actor/state/action. Trace the implemented outcome and, when required, its event identity, timing, grain, transform and metric consumer using fixed observation windows.

Compare both normal and relevant denied/failed/duplicate outcomes with the same accepted wording. Distinguish correct instrumentation from an unmeasured business effect; code can establish emission semantics without proving conversion uplift.

Return passed, failed or blocked for the selected decision/metric contract. Pass a failure with its exact action/event/value and owner into the authorized repair, rerun the affected check and finish Patch Checking for changed code. Missing product decisions and unavailable warehouse/field evidence remain explicit gates.
