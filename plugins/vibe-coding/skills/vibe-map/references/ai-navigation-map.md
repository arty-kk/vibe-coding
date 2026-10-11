# AI Navigation Map

## Operation

Map the requested area using current repository evidence.

## Goal

Map the selected AI capabilities from input and model calls through prompts, tools or retrieval to outputs and evaluation.

Suggested saved map: `docs/ai_map.md`.

## Inspect

Model invocation sites, SDK clients, prompt templates, system/developer/user message builders, tool/function schemas, structured-output parsers, streaming handlers, retry/cache layers, rate-limit code, queues/jobs, RAG ingestion/retrieval, vector indexes, OCR/document processing, ML model artifacts, feature stores, eval scripts, fixtures, tests, telemetry/logging, config/env validation, docs, and generated artifacts.

## Map content

### Evidence and IDs

- Suggested IDs for new entries: capability `AI-*`, model call `MC-*`, prompt/template `PT-*`, tool/function `TF-*`, retriever/index `RG-*`, OCR/doc pipeline `DOC-*`, ML model/pipeline `ML-*`, eval `EV-*`, safety boundary `SB-*`.

### Coverage

Cover user-visible AI features, internal/background AI jobs, model/provider configuration, input/output contracts, tool/function contracts, schema validators, streaming and async state, RAG/OCR/ML sub-pipelines, eval coverage, data/privacy boundaries, cost/rate-limit controls, logs/metrics/traces, fallbacks, and operator runbooks when discoverable.

### Entry details

For each AI capability, capture owner symbol, caller surface, input sources, model/provider/config, prompt/template owner, output schema, downstream consumers, validation/parsing, error/fallback behavior, privacy/security boundary, tests/evals, telemetry, cost/rate-limit controls, and known drift. For RAG/OCR/ML entries, include ingestion/source data, transformation steps, index/model artifact owners, freshness/versioning, and acceptance/eval signals.
