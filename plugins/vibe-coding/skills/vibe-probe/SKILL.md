---
name: vibe-probe
description: "Inspect one repository area for a proven bug; fix it when requested. Use for bounded bug discovery, not a whole-project audit."
---

# Find one bug

Apply [the working contract](../../references/workflow.md) once. Select one recipe for the failing behavior:

| Behavior | Recipe |
|---|---|
| Dependency direction or rule ownership | [Architecture](references/instant-architecture-probe.md) |
| Server request, persistence, job or integration | [Backend](references/instant-backend-probe.md) |
| Client state, requests, effects or navigation | [Frontend](references/instant-frontend-probe.md) |
| Layout, presentation, keyboard or accessibility | [UI/UX](references/instant-ui-ux-visual-probe.md) |
| No domain selected | [General bug](references/instant-bug-fix-polish.md) |

## Selection and history

Follow an explicit user target, including revisiting it to complete or verify earlier work. For an unspecified next probe, reconstruct visited primary owners from **all visible probe outcomes** in this conversation and choose one unvisited area. Reading a consumer or test does not make it a new area; a different contract owner does. Do not assume unseen history.

Prioritize a supplied reproduction, failing test or trace, then a changed contract or reachable high-risk path. Inspect the selected owner and necessary dependencies. Confirm expected behavior and a reachable violation before editing; style preferences and speculative improvements do not qualify.

## Completion

If a fix is authorized, correct one proven defect and verify its direct effects. If no defect qualifies, stop after the selected area; do not search another area to manufacture a finding. If a required decision or environment is missing, identify it and finish independent inspection.

## Probe → repair → patch review

Carry the selected owner, expected invariant and reproducing input into the repair; then replay the failure and a normal control. When a meaningful patch was created, run [Patch Checking](../vibe-review/references/patch-checking.md) on the resulting change. A correction made during that review requires another review pass before the clean marker. Keep repairs tied to the selected invariant and the patch's direct consequences.

Only after this cycle is accepted can a requested next probe choose another unvisited primary owner. A failed required check returns to the current repair; a missing decision/environment or stalled correction stops this probe rather than switching areas.

Report one outcome with its primary area/owner, evidence and actual verification:

- `BUG_FOUND_FIXED`: the selected defect was repaired, its acceptance verified and the resulting patch reviewed clean.
- `BUG_FOUND`: a defect was established in inspection-only mode; no repair was authorized.
- `BUG_FOUND_BLOCKED`: a necessary fix or required verification is unresolved; distinguish changes already made from remaining work.
- `NO_BUG_FOUND_IN_NEW_AREA`: the bounded area yielded no qualifying defect; this is not a whole-repository clean verdict.
- `NO_NEW_UNVISITED_AREA`: no suitable new area is available from the visible context.

Keep the outcome in the visible conversation so the next probe can reconstruct history; do not create a repository ledger unless requested. An explicit request for several probes is a bounded set of these operations, not permission for an indefinite search.
