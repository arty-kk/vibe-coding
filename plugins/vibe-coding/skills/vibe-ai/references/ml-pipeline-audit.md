# ML Pipeline Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit machine-learning pipeline behavior across data contracts, feature generation, training, inference, evaluation, deployment, monitoring, and rollback. Keep only issues with current repository impact; do not turn generic ML advice into tasks.

## Inspect

Datasets/loaders, feature definitions, schemas, training scripts, notebooks only when wired into repo workflows, model artifacts, registry/versioning, inference services, batch jobs, config/env, preprocessing/postprocessing, thresholds, metrics, tests/evals, drift/monitoring hooks, CI/CD, docs, and downstream consumers.

## Issue classes

- Data and features: schema drift, train/serve skew, duplicated feature logic, leakage, missing null/category handling, unstable splits, non-reproducible sampling, and locale/timezone bugs.
- Training and evaluation: undocumented or unrunnable training path, metrics that do not match product risk, stale baselines, missing regression fixtures, threshold changes without validation, and untracked model/config versions.
- Inference behavior: pre/post-processing mismatch, invalid output ranges, no confidence/uncertainty state where product depends on it, batch/online inconsistency, and unsafe fallback behavior.
- Deployment and rollback: model artifact not pinned, incompatible model/code versions, migration gaps, missing warmup/health check, and no safe rollback path for changed predictions.
- Monitoring and operations: absent prediction/error metrics, drift signals, data-quality checks, alert/runbook gaps, and cost/latency hot paths.
- Privacy/compliance: training or logs include sensitive data without repo-visible guardrails, retention/deletion mismatch, or cross-tenant data mixing.

## Finding quality

- Include model/artifact/version owner, expected behavior, acceptance criteria, and validation/eval direction when discoverable.
- Do not propose research experiments, model-family swaps, or metric redesigns without repo-visible product need and validation path.

## Trace and hand off

Follow one observation from its prediction/generation time through data extraction, split assignment, feature transforms, training artifact and served prediction. Verify that the same feature has the same meaning and availability at training and inference time. Pass the violated data/artifact boundary, time/split identity and a reproducing row/slice to Improve ML Pipeline; a better training metric cannot resolve leakage or train/serve skew.
