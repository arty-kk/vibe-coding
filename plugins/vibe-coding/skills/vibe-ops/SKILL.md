---
name: vibe-ops
description: "Audit or repair runtime configuration, jobs, CI/CD or an incident. Prepare deployment files only for the selected target."
---

# Infrastructure & background jobs

Apply [the working contract](../../references/workflow.md) once. Separate source/configuration work, live intervention and evidence of recovery.

## Workflows

- **Incident:** Incident Triage Audit when the cause/target is unresolved → Improve Incident Remediation for an authorized mitigation/correction → Incident Recovery Check → [Patch Checking](../vibe-review/references/patch-checking.md) for changed source/configuration. A credible known incident target can start at remediation. Keep immediate mitigation and root-cause closure distinct.
- **Background job:** Background Jobs Audit → Improve Background Jobs → controlled enqueue/worker/retry/effect verification → Patch Checking. Prefer the actual queue engine's specialized workflow when its delivery/lifecycle semantics own the failure.
- **Operational path:** Infra Ops Audit → Improve Infra Ops → render/config/startup/degraded/drain checks relevant to the target → Patch Checking.
- **New deployment setup:** Deploy Bootstrap for the selected host/runtime → validate generated workflow/config/artifact and document missing external inputs. Preparation alone does not deploy.

## Handoff and completion

Carry immutable artifact/config identity, affected operation/cohort, failure timeline, accepted recovery criteria and actual intervention authority between steps. A queue/job handoff also carries payload/operation identity and the durable completion boundary.

Return a failed startup, effect or recovery observation to the owning configuration/runtime/worker step and repeat the affected check. Review a changed patch again after corrections. Do not call production recovered from a local build, idle traffic or a quiet alert; leave required live rollout, repair and recurrence-window evidence explicit. Use existing providers and identities rather than selecting a new platform to satisfy a generic template.

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
