---
name: vibe-ops
description: "Audit or repair runtime configuration, jobs, CI/CD or an incident. Prepare deployment files only for the selected target."
---

# Infrastructure & background jobs

Apply [the working contract](../../references/workflow.md) once; read only the recipe for the requested result.

## Recipes

| Recipe | Operation |
|---|---|
| [Incident Triage Audit](references/incident-triage-audit.md) | audit |
| [Improve Incident Remediation](references/incident-remediation-polish.md) | implement |
| [Incident Recovery Check](references/incident-recovery-check.md) | check |
| [Background Jobs Audit](references/background-jobs-audit.md) | audit |
| [Improve Background Jobs](references/background-jobs-polish.md) | implement |
| [Deploy Bootstrap](references/deploy-bootstrap.md) | implement |
| [Infra Ops Audit](references/infra-ops-audit.md) | audit |
| [Improve Infra Ops](references/infra-ops-polish.md) | implement |


For an observed outage or regression, use incident triage, remediation or recovery check according to the requested action. Alert semantics belong to [Observability](../vibe-observability/SKILL.md); restore/rollback machinery to [Recovery](../vibe-recovery/SKILL.md).
