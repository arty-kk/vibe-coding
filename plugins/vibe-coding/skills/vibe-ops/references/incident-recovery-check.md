# Incident Recovery Check

## Operation

Verify that the selected incident remediation restored the affected operation without changing product or operational state. Read [incident response boundaries](../../../references/incident-response.md). Deployment, restart, rollback and data repair remain separate actions governed by the user's authorization.

## Context

The affected user operation and cohorts, incident window, available symptom/runtime evidence, known changes, investigation or intervention authority and recovery criteria. Mark unavailable telemetry and unresolved causality explicitly.

## Domain invariants

- Incident claims distinguish user impact, observed failure and inferred cause using attributable and time-aligned evidence.
- A mitigation’s effect and a root-cause correction are separate claims; neither is established by temporal correlation alone.
- The intervention targets the authoritative failure owner and preserves directly affected compatibility, retry and durable-state contracts.
- Recovery is demonstrated by fresh affected-user behavior and required convergence, with valid traffic and functioning telemetry.
- Unfinished data repair and unobserved recurrence windows remain explicit even when immediate symptoms or alerts subside.

## Establish criteria

Name the incident, affected operation/cohorts, intervention identity and deployment/configuration time. Use the incident's success criteria and baseline; do not invent a convenient new threshold after seeing the result. Identify the current artifact/configuration and the observation window needed for the failure mode to recur or backlog to converge.

## Recovery evidence

- Fresh successful user operations through the previously failing path, including the affected identity, region or workload where relevant.
- Error ratio and latency with a meaningful denominator and comparable traffic; an idle service has not demonstrated recovery.
- Queue age, retries, dead-letter work and durable-state reconciliation, not only queue depth or process health.
- Resource saturation, connection/task cleanup and downstream behavior during the workload that exposed the incident.
- Absence of the original failure signature with functioning telemetry, plus checks for directly induced regressions.
- Completion or explicit remaining scope of repairs for partially written data, missed events or duplicate effects.

## Verification method

1. Confirm the intervention actually reached the intended runtime; compare immutable release/configuration identifiers.
2. Correlate fresh evidence with the intervention timeline using event and ingestion times correctly. Exclude old delayed log entries from current-failure counts without hiding real delayed effects.
3. Repeat the original reproduction or an equivalent safe product check. Use a valid control and the affected cohort; a health endpoint alone is insufficient.
4. Inspect backlog and state convergence over the agreed window. Establish that retries are draining rather than simply being disabled or silently dropped.
5. Compare with the baseline and document uncertainty from traffic changes, sampling, missing telemetry or unexercised providers.

## Evidence and limitations

Classify the result as recovered, mitigated with remaining work, failed or not sufficiently observed. Support it with exact queries/checks, timestamps, observed values and remaining criteria. Tie a failing code/configuration condition to its owner when the source supports that conclusion; keep external causes as evidence-backed hypotheses.

Do not infer causality solely because two graphs changed together, or declare full recovery because alerts stopped. State which user guarantees are restored and which data repair, recurrence, provider or longer-window checks remain open. Recommend the smallest next investigation or authorized repair rather than expanding into unrelated operations.
