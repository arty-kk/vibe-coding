# Workflow cycles

Choose stages from the requested outcome. A straightforward fix needs neither a preliminary map nor a separate plan. Work stays in the current conversation; separate tasks and delegation are not implied.

| Situation | Useful sequence | Completion condition |
|---|---|---|
| Early idea needing a plan | Task Shaping → Validation & Clarification | TASK_READY, ALREADY_SATISFIED or the specific blocked decision |
| Unfamiliar repository | Project Atlas → a relevant detailed map | Needed areas and relationships are evidenced |
| Unclear defect | Domain audit → implementation when requested → relevant domain check → Patch Checking loop if a patch exists | Requested behavior verified and final patch clean, or a concrete gate |
| Known bug | Domain implementation → relevant check → Patch Checking loop | The affected contract and resulting patch are accepted |
| One new bug | One probe → authorized repair → verification → Patch Checking loop | The selected area's fixed, found, clean or blocked outcome |
| Several reports | Evidence Normalization → Synthesis | Duplicates and contradictions are resolved |
| Patch review | Review → authorized fixes → validation → review again on the complete resulting patch | A full pass makes no correction and satisfies required verification |
| Stale maps | Map Staleness Check → authorized Map Refresh → freshness check again → Patch Checking for saved changes | Affected entries agree with current sources and retain stable IDs |
| Complex runtime contract | Domain implementation → corresponding check → repair/recheck if needed → Patch Checking loop | Selected failure/retry/recovery guarantees supported; external gaps remain visible |
| Iteration closure | Iteration Closure | Done / next slice / replan / blocked |

Carry only relevant context between stages: objective, boundary, rule and owner, evidence, intended behavior, changes, verification and unresolved limits. Distinguish observations from hypotheses. A plan or stale map alone does not prove a defect.

## Step handoff

Each prompt consumes one current context and produces the input to the next:

- Audit → a supported defect, its owner, trigger, expected behavior and a falsifiable acceptance check.
- Implementation → the resulting patch, preserved contracts and actual validation results.
- Domain check → expected/observed behavior, environment and failed or unavailable criteria.
- Patch Checking → the reviewed patch state and clean, findings, recheck or blocked outcome.
- Synthesis/plan/map → the requested evidence-backed artifact and explicit decisions still needed; these steps do not grant implementation permission.

Load only the prompt reached by that transition. Reuse valid evidence, but re-evaluate the parts whose source, environment or input changed. A domain check failure returns to the corresponding owner-level repair when changes are authorized. Once the repair passes its affected checks, review the new patch rather than reusing an earlier clean verdict.

## Patch Checking loop

Use the same original diff/branch boundary across corrective commits:

```text
Patch Checking → no qualifying findings + required checks passed + no correction in this pass → clean
Patch Checking → corrections applied → validate → Patch Checking again
Patch Checking → findings, no repair authority → report findings and stop
Patch Checking → required gate or no progress → blocked with the missing condition
```

Only the final clean pass starts with `✅ Everything is fine. No changes required 👌`. A pass that applies fixes cannot issue that marker. No patch uses the no-patch outcome; unavailable required checks cannot be converted into success.

Continue a requested multi-step workflow in the current task without requiring a user message for every prompt. Stop at its accepted result, a concrete gate, the user's resource/attempt limit or a repeated failure with no new evidence. Do not create a new chat, parallel agent or background loop merely because the workflow has several steps.
