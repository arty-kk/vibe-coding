---
name: vibe-task
description: "Turn requests or findings into implementation-ready tasks, validate their acceptance and dependencies, or close an iteration against evidence. Use for task design and synthesis, not as a compulsory prelude to a known fix."
---

# Tasks & synthesis

Apply [the working contract](../../references/workflow.md) once. Choose the entry step from the input already available; preserve the user's requested output format.

## Workflows

- **A request needs an executable brief:** Task Shaping → Validation & Clarification. Carry the goal, owner, constraints, acceptance and verification into validation. Resolve repository facts directly; return to shaping only when the required outcome or delivery boundary changes.
- **Several audits describe overlapping work:** Synthesis → Task Shaping for briefs that still need detail → Validation & Clarification. Merge only findings solved by the same correction and acceptance check. Keep conflicting evidence or product decisions visible.
- **The objective has dependent outcomes:** Workstream Decomposition → validate the next dependency-ready brief. Keep shared migrations, policy changes and producer/consumer transitions together unless a compatible intermediate state is explicit. Execute workstreams only when implementation was requested.
- **Several maps must be reconciled:** Map Synthesis → the selected task/audit step if requested. Verify contradictions against current owners before using a map claim as an implementation premise.
- **An improvement direction is requested:** Evolution & Improvement → shape the selected item after its priority and outcome are chosen. A roadmap is not permission to implement every opportunity.
- **An iteration may be finished:** Iteration Closure → DONE, NEXT_SLICE, REPLAN or BLOCKED, based on the stage's acceptance evidence. A remaining defect returns to its owning repair workflow; a changed patch goes through Patch Checking again.

## Handoff to implementation

A validated brief supplies the next domain workflow with its authorized behavior, target, acceptance checks, dependencies and unresolved gates. Start implementation in the current task only if the user asked for it. For planning-only work, return the brief and stop. A known, already precise fix may start directly in its domain workflow.

After implementation, use [Patch Checking](../vibe-review/references/patch-checking.md) until its clean marker or a concrete gate, then assess the requested completion stage. Do not manufacture new tasks or expand a completed objective to keep the cycle running.

## Recipes

| Recipe | Operation |
|---|---|
| [Evolution & Improvement](references/evolution-improvement.md) | plan |
| [Iteration Closure](references/iteration-closure.md) | closure |
| [Map Synthesis](references/map-synthesis.md) | plan |
| [Synthesis](references/synthesis.md) | plan |
| [Task Shaping](references/task-shaping.md) | plan |
| [Validation & Clarification](references/validation-clarification.md) | plan |
| [Workstream Decomposition](references/workstream-decomposition.md) | plan |
