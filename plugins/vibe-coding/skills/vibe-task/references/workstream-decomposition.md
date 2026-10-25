# Workstream Decomposition

## Operation

Return an actionable plan for the requested outcome.

## Goal

Decompose one large, evidence-backed objective into the smallest dependency-ordered workstreams that can be implemented and validated independently without splitting a shared invariant across tasks.

## Context

Use the requested outcome and current defining sources to identify dependencies and acceptance. Split when independently useful stages are needed, not to meet a fixed number of tasks or pull requests. Keep unresolved decisions attached to the dependent stage; continue planning independent work. Existing maps are optional discovery aids.

## Decomposition rules

- Split on authoritative owner, product requirement/acceptance owner, policy decision owner, public/data contract, state migration, rollout/rollback, or independent validation boundaries.
- Keep one invariant and its directly affected producers/consumers in the same slice unless a compatible intermediate contract is explicit.
- Mark work parallel only when it does not write the same contract, migration sequence, generated artifact, or deployment gate.
- Define integration checkpoints before downstream work that depends on a new schema/API/event/config contract.
- Each workstream must be independently reviewable, testable, and stoppable; avoid a final catch-all integration task.
- Preserve exact `path:line[-line]` evidence and separate repository facts from assumptions; map IDs may be included only alongside direct owner evidence.
- Do not create coordination-only tasks, broad cleanup buckets, or artificial slices that cannot reach a meaningful acceptance boundary.

## Deliver and advance

For each workstream state its entry condition, defining owner, expected deliverable, observable acceptance, verification and direct prerequisites. Name the first dependency-ready workstream. A downstream consumer must receive the actual accepted schema/API/state contract, not merely the promise that its producer task is done.

When execution is requested, finish and verify the current workstream, including its Patch Checking loop, before advancing to a dependent one. If evidence invalidates an assumed intermediate contract, revise that dependency boundary and revalidate affected briefs. Do not keep an obsolete plan executable after its premise has changed.
