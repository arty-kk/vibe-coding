---
name: vibe-kubernetes
description: "Audit, repair or verify rendered Kubernetes workloads, probes, scheduling, policy, storage and rollout behavior."
---

# Kubernetes

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Kubernetes Platform Audit → Improve Kubernetes Platform → Kubernetes Rollout & Failure Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry the exact chart/overlay, rendered resources, cluster/workload identity, availability/termination promise and stateful dependencies between prompts. A known render or lifecycle defect starts at correction; verification-only work does not apply changes.

Trace the mismatch from maintained source to rendered selectors/references and actual admission, traffic, drain or recovery. Correct the chart/operator/overlay owner, then compare the same target render and selected runtime transition. Keep rollout availability, voluntary eviction budgets and involuntary loss as distinct guarantees.

A failed reference, endpoint, drain or state-recovery case returns to its owning source/resource. Repeat affected checks and finish patch review; a render/schema pass alone is not a live rollout result. Applying workloads, evicting pods or disrupting nodes requires the corresponding authorized test environment.

## Recipes

| Recipe | Operation |
|---|---|
| [Kubernetes Platform Audit](references/kubernetes-platform-audit.md) | audit |
| [Improve Kubernetes Platform](references/kubernetes-platform-polish.md) | implement |
| [Kubernetes Rollout & Failure Check](references/kubernetes-rollout-failure-check.md) | check |
