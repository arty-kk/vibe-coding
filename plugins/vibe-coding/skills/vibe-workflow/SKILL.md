---
name: vibe-workflow
description: "Maintain Vibe Coding's prompt workflows and retrieval, reconcile evidence, refresh stale maps, or run a scoped audit/repair/check when no domain workflow fits. Select the specific utility; do not turn an ordinary task into package maintenance."
---

# Workflow checks & maintenance

Apply [the working contract](../../references/workflow.md) once. Select one lane by the requested output.

## Workflows

- **Maintain this plugin:** Prompt Skill Sync Audit → Improve Prompt Skill Sync → package/retrieval checks → [Patch Checking](../vibe-review/references/patch-checking.md). Start at the implementation step for an already established change. Carry the affected trigger, prompt, workflow transition or tool contract into the correction and its regression scenario.
- **Maintain repository maps:** Map Staleness Check → Improve Map Refresh for proven stale entries → Map Staleness Check again on the updated sources. If files changed, finish their Patch Checking loop. A fresh map ends this lane; it does not authorize a product change.
- **Normalize conflicting inputs:** Evidence Normalization → [Synthesis](../vibe-task/references/synthesis.md) when the user wants actionable tasks. Carry source, environment, uncertainty and the observation needed to distinguish conflicting claims. Normalization itself neither prioritizes changes nor edits code.
- **Handle an uncovered behavior:** Scoped Audit when the cause/owner is unknown → Improve Scoped when a change is authorized → Behavior Check → Patch Checking if a patch exists. A known requirement may start at Improve Scoped; a check-only request stops after verification.

## Carry state between steps

Pass the selected target, current source anchors, expected result, relevant findings and observed checks. Reuse accepted facts, but invalidate claims whose source changed. Return a failed domain check to the owning repair step when repair is authorized; then rerun the affected check and review the resulting patch. Stop at the requested result, an unresolved decision/environment or a repeated failure without new evidence.

The clean Patch Checking sentinel applies to an actual reviewed patch. Evidence normalization and a check with no patch must return their own result instead of manufacturing that sentinel.

## Recipes

| Recipe | Operation |
|---|---|
| [Behavior Check](references/behavior-check.md) | check |
| [Evidence Normalization](references/evidence-normalization.md) | plan |
| [Improve Map Refresh](references/map-refresh-polish.md) | implement |
| [Map Staleness Check](references/map-staleness-check.md) | check |
| [Prompt Skill Sync Audit](references/prompt-skill-sync-audit.md) | audit |
| [Improve Prompt Skill Sync](references/prompt-skill-sync-polish.md) | implement |
| [Scoped Audit](references/scoped-audit.md) | audit |
| [Improve Scoped](references/scoped-polish.md) | implement |
