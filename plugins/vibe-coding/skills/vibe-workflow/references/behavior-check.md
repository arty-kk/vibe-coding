# Verify a Behavior

## Scope

Verify the requested behavior when no specialized check applies. Establish the target, expected input/output or state transition, defining source and available environment from the request and repository.

## Procedure

1. Translate required acceptance into relevant scenarios; specify expected results and allowed effects before running them.
2. Find native commands or a controlled reproduction that reaches the real defining rule. Pair rejection/failure cases with a valid control.
3. Compare the returned result and stored/externally observable state where side effects matter.
4. Distinguish source inspection, local execution and external behavior. An unavailable required layer remains a verification gap.

## Result

Return passed, failed or blocked with expected/observed evidence for required criteria, exact checks and the narrow next action for any failure or missing evidence. Do not turn verification into an unrequested implementation.
