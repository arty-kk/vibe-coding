# Infra Ops Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit operational readiness across CI/CD, runtime config, deployment, migrations, jobs, health checks, secrets, backups, observability, and recovery. This complements [Deploy Bootstrap](deploy-bootstrap.md): it finds repo-proven ops tasks instead of bootstrapping one opinionated deploy path.

## Inspect

CI workflows, deploy scripts, Docker/Compose/IaC files, package/build scripts, env examples and validation, secret handling, database migrations, rollback notes, queues/workers/cron, health/readiness endpoints, logging/metrics/tracing, alert hooks, backup/restore docs, rate limits, external services, runtime docs, tests, and `infra/README.md` when present.

## Issue classes

- CI/CD: required checks not running, deploy uses branch head instead of immutable commit, unsafe deploy triggers, missing build artifacts, lockfile drift, and unvalidated workflow syntax.
- Runtime config and secrets: required env not validated, insecure defaults, secret values printed/logged, env docs drift, and production debug behavior.
- Deploy and migrations: non-idempotent deploy scripts, unsafe cleanup, migrations without ordering/rollback notes, worker/web version skew, and health checks that mask degraded service.
- Jobs and queues: missing concurrency/idempotency controls, retry amplification, dead-letter gaps, stale cron assumptions, and unobservable background failures.
- Reliability and recovery: no backup/restore path for stateful services, absent runbooks for critical failures, missing readiness/liveness separation, and public errors exposing internals.
- Observability: logs lack correlation/user-safe context, missing metrics for critical paths, no alertable signal for known failure modes, and telemetry that leaks sensitive data.

## Finding quality

- Include expected operational behavior, acceptance criteria, validation command or manual verification direction, and rollback/recovery note when relevant.
- Do not propose new infrastructure platforms, vendors, or broad observability stacks without repo/user evidence.
