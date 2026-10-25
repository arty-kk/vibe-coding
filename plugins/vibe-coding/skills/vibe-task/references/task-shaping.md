# Shape an Implementation Task

## Scope

Turn the request into a brief that an implementing agent can act on. Use the stated outcome and current repository; a new requested capability does not require evidence of an existing defect.

## Procedure

1. Identify the actor/input, requested behavior and accepted outcome. Locate the code, schema or policy that should define it and directly affected consumers.
2. Recover relevant constraints, existing patterns and commands from current sources. Mark unresolved product decisions rather than inventing them.
3. Group changes that must be delivered together to satisfy one contract. Split only independently useful outcomes, preserving dependencies and the complete requested objective.
4. Define observable acceptance: normal behavior, relevant failure or denied states and compatibility when a contract changes.

## Brief

Include the problem/change, target and defining owner, necessary evidence, expected behavior, exclusions, dependencies and verification. Add domain-specific details only when they affect implementation:

- Access policy: subject, action, resource, attributes and scope, with backend enforcement.
- API/integration: input/output/error contract, operation identity, supported consumers and side effects.
- UI: entry/state/interaction, data contract, recovery and accessible behavior.

Ask only for a missing decision that changes the result. Return the brief in the requested format; do not start separate agent conversations.

## Handoff

Pass the brief to Validation & Clarification with the source request intact. Make each acceptance criterion observable: identify the action/input, expected state or response and the check that distinguishes success from the prior behavior. Carry unresolved decisions explicitly; an implementing agent should not have to infer a product choice from a suggested file path.

If the request already supplied an implementable brief, refine only material gaps. Do not rewrite it into a new project or add discovery artifacts that do not change the implementation decision.
