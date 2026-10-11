# Improve Data Model

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected schema or persistence invariant, including required migration and reader/writer compatibility.

## Domain rules

- Change the canonical model and update all directly affected contracts; avoid a second mutable model or adapter that disagrees with the defining schema.
- Use expand/migrate/contract for incompatible live changes and make backfills idempotent/resumable.
- Add constraints only after validating/backfilling existing data and define violation handling.
- Synchronize generated types, fixtures, analytics, docs, retention, and operator checks.

## Validation

- Run schema/type/migration/model/API/event/data-quality tests.
- Exercise old/new compatibility, backfill retry/resume, constraint violations, deletion/retention, and rollback/forward-fix.
- Report production data volume/distribution and maintenance-window gates separately.
