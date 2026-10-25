---
name: vibe-terraform
description: "Audit, repair or verify Terraform module, plan and state identity, drift or resource moves; preparation does not authorize apply."
---

# Terraform

Apply [the working contract](../../references/workflow.md). Establish the configuration revision, backend/workspace and selected resource addresses before interpreting a plan.

## Workflow

For unexpected replacement, drift or failed delivery, run **Terraform Delivery Audit**. Hand its classified drift, address mapping and exact plan identity to **Improve Terraform Delivery**. For a specified module or address change, start with the repair recipe and preserve the same environment identity.

Run **Terraform Plan & State Check** on the resulting configuration, then [Patch Checking](../vibe-review/references/patch-checking.md), repeating after corrections under [the cycle contract](../../references/cycles.md). An audit or plan review ends with findings and evidence. Preparing a patch, saved plan or recovery procedure does not execute an apply or mutate remote state.

Carry the non-secret variable-set identifier, provider lock digest, module versions, backend/workspace, expected address/action set and state lineage between steps. An unknown computed attribute is acceptable when the intended action is still assessable. An unknown target identity or unresolved destructive action prevents approval of that part of the plan.

## Recipes

| Recipe | Operation |
|---|---|
| [Terraform Delivery Audit](references/terraform-delivery-audit.md) | audit |
| [Improve Terraform Delivery](references/terraform-delivery-polish.md) | implement |
| [Terraform Plan & State Check](references/terraform-plan-state-check.md) | check |
