# Implement a Scoped Change

## Scope

Implement the named behavior when no specialized recipe applies. Use the user’s requirement or a supported finding to establish the target and intended result; a prior audit document is optional.

## Procedure

1. Locate the defining code, schema or configuration and directly affected contracts. Recover ordinary implementation context from current sources.
2. Define acceptance and the compatibility/failure behavior that matters to the change. Ask only for an unresolved decision that changes it.
3. Correct the owner and necessary producers/consumers, generated outputs or migrations. Preserve unrelated behavior and architecture.
4. Run the native checks or controlled reproduction that exercise the selected contract. Record actual outcomes and required missing evidence.

## Result

Report the implemented behavior, relevant changes, verification and remaining required work. Do not substitute another improvement when the target cannot be established.

Pass the expected/observed transition and actual changed paths to Behavior Check when verification needs a controlled reproduction beyond native tests. A failed check returns the same contract to this implementation step; correct the owner and repeat the affected scenario. Once acceptance is supported, run Patch Checking on the whole resulting patch until its clean marker or a concrete gate.
