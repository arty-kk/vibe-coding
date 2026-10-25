---
name: vibe-docs
description: "Create or synchronize repository docs; plan or implement a scoped refactor or migration using current code and contracts."
---

# Documentation & refactoring

Apply [the working contract](../../references/workflow.md) once. Select documentation or refactoring by the requested deliverable; a documentation mismatch does not automatically authorize product changes.

## Workflows

- **Create a README or design reference:** Document the Repository / Document the Design System → verify sources, examples and links → [Patch Checking](../vibe-review/references/patch-checking.md) when repository files changed. Start from maintained documentation and preserve the requested language/format.
- **Repair stale documentation:** Documentation Sync Audit when the drift is unknown → Improve Documentation Sync → recheck the affected statements/examples → Patch Checking. Carry each stale claim and its governing source into the correction. If code violates an accepted requirement, keep that discrepancy visible rather than rewriting the requirement.
- **Move an implementation boundary:** Refactor Boundary Audit when ownership or consumers are unclear → Migration & Refactor Plan when a compatibility/data/rollout transition is needed → Improve Refactor Boundary → behavior/compatibility checks → Patch Checking until clean or blocked. A known mechanical move can start at implementation without manufacturing an audit and migration plan.

## Handoff and completion

A refactor handoff names the invariant, old/new owner, affected consumers, compatible intermediate states and the checks that must remain true. A documentation handoff names the claim, maintained source/generator and corrected example or reference.

Failed validation returns to the owning document generator or implementation boundary, then repeats the affected check and reviews the new patch. Stop at the requested artifact or accepted transition; a missing external environment is a stated gate, not permission to invent runtime success or replace the target architecture.

## Recipes

| Recipe | Operation |
|---|---|
| [Document the Design System](references/design-gen.md) | document |
| [Documentation Sync Audit](references/documentation-sync-audit.md) | audit |
| [Improve Documentation Sync](references/documentation-sync-polish.md) | implement |
| [Migration & Refactor Plan](references/migration-refactor-plan.md) | plan |
| [Document the Repository](references/readme-gen.md) | document |
| [Refactor Boundary Audit](references/refactor-boundary-audit.md) | audit |
| [Improve Refactor Boundary](references/refactor-boundary-polish.md) | implement |
