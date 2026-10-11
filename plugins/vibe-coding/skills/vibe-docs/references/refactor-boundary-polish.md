# Improve Refactor Boundary

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Move the selected behavior to its intended owner and update direct dependents without changing unrelated contracts.

## Domain rules

- Move behavior to one owner and update all directly affected consumers as part of the same accepted change.
- Preserve contracts by default; when changing them, provide explicit migration and remove obsolete paths when safe.
- Avoid wrapper-only layers, duplicate adapters, temporary flags, and mass formatting/renames unrelated to the boundary.
- Synchronize tests, docs, generated outputs, config, registration, and build/deploy references.

## Validation

- Run affected unit/integration/type/build/import/dependency checks.
- Verify old/new compatibility or migration, dead-path removal, generated artifacts, and one representative runtime trace.
- Report untested plugin/reflection/deployment consumers explicitly.
