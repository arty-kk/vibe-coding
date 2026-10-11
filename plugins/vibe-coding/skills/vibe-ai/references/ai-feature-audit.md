# AI Feature Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Audit AI-assisted product behavior for correctness, safety, cost, reliability, privacy, and regression risk. Keep only issues supported by current repository evidence, not generic AI best practices.

## Inspect

AI entrypoints, model clients, prompt/message builders, structured-output schemas, tool/function definitions, parsers, streaming handlers, queues/jobs, cache/retry/rate-limit code, RAG/OCR/ML dependencies, user-visible AI states, admin/operator controls, env/config validation, tests/evals, fixtures, logs/metrics/traces, docs, and `docs/ai_map.md` when present as a discovery aid.

## Issue classes

- Input/output contracts: unvalidated model inputs, weak schema parsing, enum/nullability drift, brittle natural-language parsing, partial-response handling, and unhandled refusal/empty output states.
- Prompt and tool boundaries: duplicated prompt rules, stale templates, unsafe tool argument construction, missing tool-result validation, prompt injection exposure through untrusted content, and mismatched user/system intent.
- Reliability: retry storms, non-idempotent replays, streaming state bugs, cache key drift, missing timeout/cancellation behavior, queue amplification, and degraded-provider behavior that misleads users.
- Safety/privacy: PII or secret leakage into prompts/logs, unsafe storage of model inputs/outputs, missing tenant/user scoping in AI context, policy bypass via background jobs, and user-visible diagnostic leakage.
- Cost and limits: unbounded context growth, duplicate model calls, missing rate/usage controls, large attachment handling without guardrails, and absent operator visibility for hot paths.
- Product truthfulness: UI promises not backed by model behavior, generated claims without source evidence, missing citations/source labels when the feature presents factual answers.
- Evaluation: missing or false eval coverage for critical prompts, RAG answers, OCR extraction, tool calls, structured outputs, safety boundaries, or known regressions.

## Finding quality

- Include model/prompt/tool/index/eval owner when relevant, expected behavior, acceptance criteria, and validation direction.
- Do not report abstract AI risks without current repo reachability, user impact, cost impact, or regression risk.
