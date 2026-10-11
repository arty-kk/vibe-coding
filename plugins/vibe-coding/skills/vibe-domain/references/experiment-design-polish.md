# Improve Experiment Design

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Correct the selected assignment, exposure or analysis contract before interpreting the experiment result.

## Domain rules

- Fix assignment/exposure/metric semantics before changing estimators or declaring a result.
- Version experiment configuration and analysis; make eligibility, allocation, windows, exclusions, and stopping rules deterministic.
- Add SRM and data-quality gates that stop interpretation rather than silently filtering anomalies.
- Use an estimator compatible with the randomization/analysis unit and report effect with uncertainty and practical threshold.
- Synchronize rollout/flag, telemetry, dashboard, analysis, guardrails, and reversal criteria.

## Validation

- Run assignment determinism/allocation/SRM and event-semantic tests on representative identities and windows.
- Reproduce analysis from versioned inputs and compare sensitivity to exclusions, clustering, windows, and missing data.
- Exercise treatment delivery/exposure failure and rollback; list duration/seasonality/business-signoff gates separately.
