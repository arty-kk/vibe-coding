---
name: vibe-domain
description: "Audit, repair or verify application identity, access policy, tenancy, entitlements, data models/pipelines, experiments or product events."
---

# Permissions, data & business rules

Apply [the working contract](../../references/workflow.md) once. Choose the business decision/data owner before selecting a technical fix.

## Workflows

| Boundary | Prompt chain and acceptance evidence |
|---|---|
| Identity/session and general access | Auth Permissions Audit → Improve Auth Permissions → allowed/denied session/access cases; OAuth OIDC Session Check when that protocol owns the selected flow |
| Role/attribute policy | RBAC ABAC Policy Audit → Improve RBAC ABAC Policy → RBAC ABAC Matrix Check |
| Tenant resource isolation | Multi Tenant Isolation Audit → Improve Multi Tenant Isolation → Tenant Isolation Check |
| Local plan, quota and entitlement | Billing Entitlements Audit → Improve Billing Entitlements → plan/lifecycle/quota cases; policy matrix check where the changed access decision needs it |
| Persistence/state model | Data Model Audit → Improve Data Model → schema/constraint, migration and reader/writer acceptance |
| Source-to-sink data | Data Pipeline & Quality Audit → Improve Data Pipeline & Quality → identity/window/checkpoint reconciliation and retry recovery |
| Repeatable notebook | Notebook Productionization Audit → Improve Notebook Productionization → clean ordered execution, artifact lineage and selected restart/resource checks |
| Product event/metric | Product Analytics Audit → Improve Product Analytics → producer → event grain/identity → transform → consumer value |
| Experiment decision | Experiment Design Audit → Improve Experiment Design → assignment/exposure/data-quality and versioned analysis checks |

Start at implementation for a known defect or clear requirement, or at a named check for verification-only work. Audits and plans do not authorize changes. Carry the subject/resource/state or dataset/window identity, expected decision/value, authoritative owner and distinguishing input into the next prompt.

## Recheck and completion

An access rejection is verified only when it prevents the protected effect and a permitted control works. A data/metric result is verified at its consumer with the relevant grain, time and lineage, not merely by a successful job. Failed acceptance returns to the corresponding policy, transaction, transform or analysis owner; repeat the affected cases after repair.

For every changed patch, finish [Patch Checking](../vibe-review/references/patch-checking.md) until clean or blocked. Keep missing product/legal decisions, private datasets and external identity/payment/scheduler behavior as explicit gates. Do not invent pricing, policy or experiment success to close the workflow.

For OAuth/OIDC verification, select the session check. For a requested authentication fix, use Auth Permissions Polish and apply the relevant protocol checks during verification.

## Recipes

| Recipe | Operation |
|---|---|
| [Auth Permissions Audit](references/auth-permissions-audit.md) | audit |
| [Improve Auth Permissions](references/auth-permissions-polish.md) | implement |
| [Billing Entitlements Audit](references/billing-entitlements-audit.md) | audit |
| [Improve Billing Entitlements](references/billing-entitlements-polish.md) | implement |
| [Data Model Audit](references/data-model-audit.md) | audit |
| [Improve Data Model](references/data-model-polish.md) | implement |
| [Data Pipeline & Quality Audit](references/data-pipeline-quality-audit.md) | audit |
| [Improve Data Pipeline & Quality](references/data-pipeline-quality-polish.md) | implement |
| [Experiment Design Audit](references/experiment-design-audit.md) | audit |
| [Improve Experiment Design](references/experiment-design-polish.md) | implement |
| [Multi Tenant Isolation Audit](references/multi-tenant-isolation-audit.md) | audit |
| [Improve Multi Tenant Isolation](references/multi-tenant-isolation-polish.md) | implement |
| [OAuth OIDC Session Check](references/oauth-oidc-session-check.md) | check |
| [Notebook Productionization Audit](references/notebook-productionization-audit.md) | audit |
| [Improve Notebook Productionization](references/notebook-productionization-polish.md) | implement |
| [Product Analytics Audit](references/product-analytics-audit.md) | audit |
| [Improve Product Analytics](references/product-analytics-polish.md) | implement |
| [RBAC ABAC Matrix Check](references/rbac-abac-matrix-check.md) | check |
| [RBAC ABAC Policy Audit](references/rbac-abac-policy-audit.md) | audit |
| [Improve RBAC ABAC Policy](references/rbac-abac-policy-polish.md) | implement |
| [Tenant Isolation Check](references/tenant-isolation-check.md) | check |


For provider requests, signed webhooks and external payment reconciliation, use [Payments](../vibe-payments/SKILL.md). Local plan/role/entitlement policy remains here.
