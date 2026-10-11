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

Report **fixed**, **no qualifying defect found**, or **blocked**, with the primary area/owner, evidence, changed behavior and verification. Keep the area and result visible so a later probe can reconstruct history. An explicit request for several probes is a bounded set of these operations, not permission for an indefinite loop.
