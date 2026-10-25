# Domain Data Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map domain entities, relationships, state transitions, persistence owners and relevant data-lifecycle rules.

Suggested saved map: `docs/domain_data_map.md`.

## Build the view

Establish entity/key identity and enforced constraints from schemas and migrations. Trace writers and state-transition code before describing lifecycle rules, then connect authoritative records to caches, indexes, analytics and other projections. A status column or ORM relation does not by itself define legal transitions or deletion behavior. Verify representative read/write paths and mark projection freshness, ownership and lifecycle edges at their actual sources.

## Inspect

Database schemas, migrations, ORM models, NoSQL collections, object keys, search/vector indexes, generated clients/types, serializers, fixtures, factories, seed data, retention/deletion jobs, import/export code, API schemas, analytics tables, and docs.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: entity `ENT-*`, relationship `REL-*`, state machine `STM-*`, field group `FLD-*`, index/cache `IDX-*`, sensitive data `PII-*`, lifecycle rule `LIFE-*`.
- Anchor each entry to current repository evidence and distinguish source schema from generated clients, projections, docs, fixtures, and inferred behavior.

### Coverage

Cover entities, fields, relationships, ownership and tenant scope, lifecycle statuses, validation, uniqueness, migrations, indexes, caches/materialized views, retention/deletion/export, PII/sensitive data, access boundaries, fixtures, tests, generated artifacts, and analytics derivations.

### Entry details

For each entity, capture owner schema/model, key fields, state transitions, relations, readers/writers, permissions, data lifecycle rules, migrations, tests/fixtures, derived projections, and stale or missing documentation.
