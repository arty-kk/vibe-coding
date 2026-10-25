# Validate and Clarify a Task

## Scope

Check whether the proposed task has a clear outcome, correct owner and verifiable acceptance. Refine the task rather than rejecting it for missing implementation details the repository can supply.

## Procedure

1. Compare the requested outcome with current requirements, code and tests. Distinguish a proven defect, requested new behavior and behavior already implemented.
2. Check the suggested owner and directly affected contracts. Correct a misplaced implementation target when the intended outcome is clear.
3. Identify compatibility, data, permission or rollout decisions that constrain the change. Resolve them from authoritative sources where possible.
4. Split independent outcomes only when they can be implemented and verified separately. Preserve the full objective.

## Result

Return one result with the revised brief or supporting evidence:

- `TASK_READY`: outcome, owner, acceptance, dependencies and verification are sufficient to start the authorized work.
- `TASK_REVISE`: a material contradiction or incomplete contract can be corrected from available evidence. Revise the affected part and validate it again; preserve everything still valid.
- `TASK_BLOCKED`: name the missing decision or evidence, who can supply it and which work depends on it. Continue independent work when the user's task includes it.
- `ALREADY_SATISFIED`: show evidence that the requested outcome is already met; do not create a redundant implementation task.

Pass a ready brief to the appropriate domain implementation step only when changes are authorized. Return to Task Shaping when the goal or workstream boundary needs restructuring, not for cosmetic wording. Stop revising once the brief is ready or the same unresolved decision prevents progress.

Cite current sources for non-obvious conclusions. A missing formal specification or existing bug is not itself grounds to block a new user requirement.
