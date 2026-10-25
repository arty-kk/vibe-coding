---
name: vibe-go-rust
description: "Audit, repair or verify Go/Rust service task ownership, cancellation, concurrency, resource bounds and shutdown."
---

# Go & Rust services

Apply [the working contract](../../references/workflow.md) once.

## Workflow

Go Rust Microservices Audit → Improve Go Rust Microservices → Go Rust Concurrency & Shutdown Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Fix the selected operation's spawn/join owner, cancellation/deadline contract, commit/effect boundary and resource budget. A known failure starts at correction; verification-only work uses the check without edits. Use the project's actual runtime/toolchain rather than requiring the same instrumentation for both languages.

Trace caller cancellation or shutdown through child work, queues, locks, pools and durable effects. Correct ownership/admission/cleanup at that boundary, then replay the same interleaving with a healthy control. Aborting a task does not imply that a committed external effect was rolled back.

Return failed drain, leak or cancellation evidence to the same lifecycle owner, repeat the affected sequence and complete the patch review. Retain unavailable instrumentation, target-platform or load evidence as gates; task counts and local fixtures alone do not establish production capacity.

## Recipes

| Recipe | Operation |
|---|---|
| [Go Rust Concurrency & Shutdown Check](references/go-rust-concurrency-shutdown-check.md) | check |
| [Go Rust Microservices Audit](references/go-rust-microservices-audit.md) | audit |
| [Improve Go Rust Microservices](references/go-rust-microservices-polish.md) | implement |
