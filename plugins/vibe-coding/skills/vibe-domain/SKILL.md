---
name: vibe-domain
description: "Audit, repair or verify application identity, access policy, tenancy, entitlements, data models/pipelines, experiments or product events."
---

# Permissions, data & business rules

Apply [the working contract](../../references/workflow.md) once; read only the recipe for the requested result.

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
