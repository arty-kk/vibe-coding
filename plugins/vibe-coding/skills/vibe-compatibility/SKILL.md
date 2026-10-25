---
name: vibe-compatibility
description: "Reconstruct, implement or verify a compatibility contract using an authorized reference and differential fixtures."
---

# Compatibility & protocols

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Reverse Engineering Audit → Improve Reverse Engineering → Compatibility Golden Master Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Fix the authorized reference version/environment, candidate boundary and supported corpus before inferring a contract. The audit produces observations, competing hypotheses and discriminating cases; implementation consumes the supported model and explicit unknowns. A known compatibility defect may start at implementation, and a check-only request does not edit.

Compare semantic output, errors, state and effects using the same input identities. Normalize only fields whose nondeterminism is demonstrated; retain raw captures separately. A mismatch returns to the owning parser/adapter/model of the contract, followed by the same differential case and valid controls.

Complete when the selected corpus and supported version window are compatible and the patch has a clean review pass. Unavailable reference behavior or an intentional deviation remains an explicit gate/decision. Do not regenerate expected output from the candidate to erase a mismatch.

## Recipes

| Recipe | Operation |
|---|---|
| [Compatibility Golden Master Check](references/compatibility-golden-master-check.md) | check |
| [Reverse Engineering Audit](references/reverse-engineering-audit.md) | audit |
| [Improve Reverse Engineering](references/reverse-engineering-polish.md) | implement |
