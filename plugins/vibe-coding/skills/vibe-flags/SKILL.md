---
name: vibe-flags
description: "Audit, repair or verify feature-flag targeting, enforcement, fallback, exposure and removal."
---

# Feature flags & rollouts

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Feature Flags Rollout Audit → Improve Feature Flags Rollout → Feature Flag Exposure & Rollback Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry flag identity/environment, trusted targeting context, default/degraded-provider policy and the state created while enabled into correction. A known gate/removal bug starts at implementation; a check-only request does not change rollout state.

Trace flag evaluation through actual backend behavior, UI and exposure measurement. A flag lookup is not proof that a user saw treatment, and a client flag is not an authorization decision. Replay on/off, permitted/untargeted and the selected provider-failure or kill-switch transition.

A failed targeting, fallback or post-disable state returns to its owning rule/consumer, then the same scenario is rerun. Finish with the selected rollout contract verified and the patch reviewed clean. Disabling a flag does not automatically undo durable state created while it was on; preserve required migration/recovery gates.

## Recipes

| Recipe | Operation |
|---|---|
| [Feature Flag Exposure & Rollback Check](references/feature-flag-exposure-rollback-check.md) | check |
| [Feature Flags Rollout Audit](references/feature-flags-rollout-audit.md) | audit |
| [Improve Feature Flags Rollout](references/feature-flags-rollout-polish.md) | implement |
