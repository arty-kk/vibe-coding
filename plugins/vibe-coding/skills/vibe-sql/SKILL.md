---
name: vibe-sql
description: "Audit, repair or verify SQL queries, transactions, locks, migrations, pools and replica/failover behavior."
---

# SQL & connections

Apply [the working contract](../../references/workflow.md) once.

## Workflow

SQL Databases Audit → Improve SQL Databases → SQL Load Lock & Failover Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry database/proxy/version/topology, actual application role, query/transaction identity, required committed invariant and connection/deadline/freshness budget between prompts. A known query or migration defect starts at correction; a check-only request does not alter production state.

Trace acquire → transaction/locks/query → commit → reader/projection and cleanup. Correct the owning constraint, transaction, query/index, migration or pool rule, then replay the same conflicting or ambiguous sequence with a normal control. An uncertain commit outcome is not evidence that a write can safely be retried.

Failed final-state, plan/resource or recovery evidence returns to its owner, followed by affected checks and final patch review. An in-memory substitute, administrator role or small dataset cannot establish the actual engine, application-policy or production-topology guarantee.

## Recipes

| Recipe | Operation |
|---|---|
| [SQL Databases Audit](references/sql-databases-audit.md) | audit |
| [Improve SQL Databases](references/sql-databases-polish.md) | implement |
| [SQL Load Lock & Failover Check](references/sql-load-lock-failover-check.md) | check |
