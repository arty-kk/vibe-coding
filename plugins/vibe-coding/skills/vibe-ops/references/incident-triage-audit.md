# Incident Triage Audit

## Operation

Investigate the selected incident and report supported findings without product or operational changes. Read [incident response boundaries](../../../references/incident-response.md). If the user explicitly requests mitigation as well, continue under that authorization using the remediation recipe after identifying a concrete target.

## Required input

The affected user operation and cohorts, incident window, available symptom/runtime evidence, known changes, investigation or intervention authority and recovery criteria. Mark unavailable telemetry and unresolved causality explicitly.

## Domain invariants

- Incident claims distinguish user impact, observed failure and inferred cause using attributable and time-aligned evidence.
- A mitigation’s effect and a root-cause correction are separate claims; neither is established by temporal correlation alone.
- The intervention targets the authoritative failure owner and preserves directly affected compatibility, retry and durable-state contracts.
- Recovery is demonstrated by fresh affected-user behavior and required convergence, with valid traffic and functioning telemetry.
- Unfinished data repair and unobserved recurrence windows remain explicit even when immediate symptoms or alerts subside.

## Goal and scope

Establish what user operation is failing, where the first demonstrated divergence occurs and which explanations fit the evidence. Keep the investigation bounded by the incident's services, tenants, time window and dependencies. Do not broaden a single degraded operation into a repository-wide cleanup.

## Inspect

- User-visible errors, affected cohorts, onset, baseline behavior and current status.
- Deployments, configuration/flag changes, migrations, provider events and workload changes around the same period.
- Request traces, logs, error ratios, latency distributions, queue age/depth, resource saturation, retries and dependency health.
- Runtime ownership, request/job boundaries, health checks, timeout/retry configuration and relevant runbooks.

## Triage method

1. Define the incident symptom in product terms and a measurable success condition. Record the source and freshness of each observation.
2. Build a small timeline separating event time, ingestion time and observation time. Account for clock skew, sampling and missing intervals before asserting order.
3. Trace an affected request or job to its first supported failure. Compare a healthy control cohort, earlier version or unaffected path when available.
4. Keep competing hypotheses with evidence for, evidence against and a cheap discriminating check. A deployment near the onset is a candidate cause, not proof.
5. Identify the likely owner and a bounded mitigation or repair direction. Separate a reversible way to reduce impact from an established root-cause fix.

## Issue classes and priority

Prioritize ongoing data loss, unauthorized effects and failure of critical user operations, then expanding backlog, saturation, cascading retries and partial availability. Investigate stale configuration, dependency failures, schema incompatibility, leaked resources, missed work and invalid health signals where the timeline supports them. A noisy log line or a quiet alert alone does not establish the incident's severity or recovery.

## Evidence quality

For a code defect cite `path:line`, the reachable state and its operational evidence. For an external/runtime hypothesis name the specific observation and missing check. Do not invent metrics, read unavailable production systems or expose credentials/personal payloads in diagnostic output. Avoid destructive probes and keep read-only queries bounded.

## Evidence requirements

Report impact, verified timeline, supported cause or ranked hypotheses, owner, immediate repair/mitigation direction and recovery criteria. Clearly distinguish known facts from unresolved causality. If there is no demonstrated code defect, say what evidence would resolve the next decision instead of fabricating a patch.
