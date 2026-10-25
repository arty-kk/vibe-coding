---
name: vibe-temporal
description: "Audit, repair or verify Temporal determinism, Activities, message handling, replay and worker-version compatibility."
---

# Temporal

Apply [the working contract](../../references/workflow.md). Select one workflow type, Activity or deployment transition and identify the histories it must still process.

## Workflow

For an unexplained replay failure, repeated external effect or stuck message, start with **Temporal Workflows Audit**. Its handoff identifies the first incompatible command or unsafe state transition, the history/version that reaches it, and the required external outcome. For a specified correction, start with **Improve Temporal Workflows** using that evidence.

After a repair, run **Temporal Replay & Versioning Check** against the affected historical and live-worker cases, then [Patch Checking](../vibe-review/references/patch-checking.md). Repeat Patch Checking after any correction until a full pass returns the clean marker. Follow [the cycle contract](../../references/cycles.md); an audit or verification request stops at its requested result.

Carry the SDK and worker versions, representative history IDs, compatible routing/patching strategy, business effect identity and replay results between steps. A replay pass establishes command compatibility for those histories; it does not establish that a real Activity has correct timeout, cancellation or external side-effect behavior. Missing histories or unavailable worker integration remain explicit verification gaps.

## Recipes

| Recipe | Operation |
|---|---|
| [Temporal Replay & Versioning Check](references/temporal-replay-versioning-check.md) | check |
| [Temporal Workflows Audit](references/temporal-workflows-audit.md) | audit |
| [Improve Temporal Workflows](references/temporal-workflows-polish.md) | implement |
