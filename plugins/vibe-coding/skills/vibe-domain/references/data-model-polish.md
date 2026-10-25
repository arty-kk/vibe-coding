# Improve Data Model

## Goal

Correct the selected schema or persistence invariant, including required migration and reader/writer compatibility.

## Domain rules

- Change the canonical model and update all directly affected contracts; avoid a second mutable model or adapter that disagrees with the defining schema.
- Use a compatible transition appropriate to the live reader/writer window, such as expand/migrate/contract when needed; make required backfills idempotent/resumable.
- Add constraints only after validating/backfilling existing data and define violation handling.
- Synchronize generated types, fixtures, analytics, docs, retention, and operator checks.

## Validation

- Run schema/type/migration/model/API/event/data-quality tests.
- Exercise old/new compatibility, backfill retry/resume, constraint violations, deletion/retention, and rollback/forward-fix.
- Report production data volume/distribution and maintenance-window gates separately.

Pin representative existing records and the failed write/transition, then correct the canonical constraint or transaction and stage any required data migration. Verify old/new readers and writers at each supported transition, including retry/resume of a partial backfill. A failed persisted result returns to that owner rather than a second model copy. Once acceptance is supported, run Patch Checking with remaining production-data gates explicit.
