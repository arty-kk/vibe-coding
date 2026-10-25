---
name: vibe-nosql
description: "Audit, repair or verify NoSQL access using the actual engine’s key, atomicity, indexing, consistency and recovery semantics."
---

# NoSQL

Apply [the working contract](../../references/workflow.md) once.

## Workflow

NoSQL Databases Audit → Improve NoSQL Databases → NoSQL Consistency & Hot Partition Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry the actual engine/topology, key/document identity, access path, conditional/consistency policy and expected stored invariant between prompts. Start at correction for a known defect or at the check for verification-only work.

Identify whether failure begins at the atomic item boundary, a multi-item protocol, query/index path, partition budget or TTL/CDC lifecycle. Correct that owner using the engine's real semantics and replay the same conflict/retry/read sequence with a normal control.

Compare final values, read freshness and query/resource evidence rather than counting successful requests. A failed invariant, hot partition or resume gap returns to its owner, followed by the affected check and patch review. Local/emulated results do not establish an untested managed topology or capacity guarantee.

## Recipes

| Recipe | Operation |
|---|---|
| [NoSQL Consistency & Hot Partition Check](references/nosql-consistency-hot-partition-check.md) | check |
| [NoSQL Databases Audit](references/nosql-databases-audit.md) | audit |
| [Improve NoSQL Databases](references/nosql-databases-polish.md) | implement |
