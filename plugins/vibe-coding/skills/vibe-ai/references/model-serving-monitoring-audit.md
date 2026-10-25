# Model Serving & Monitoring Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal and scope

Audit model serving across artifact identity, preprocessing, routing, batching, concurrency, fallback, observability, and safe rollout.

## Domain invariants

- Serving loads the intended model/preprocessing/schema/threshold versions atomically and reports their identity.
- Admission, batching, pools, concurrency, timeouts, cancellation, retry, and memory/GPU limits are bounded.
- Fallback or shadow routing preserves semantics, tenant/privacy controls, and truthful status; it never silently changes product policy.
- Latency, errors, saturation, input/output quality, drift, and cost are observable with privacy-safe dimensions and rollback controls.

## Audit method

1. Trace request routing through preprocessing, model selection, batch/queue, inference, postprocessing, persistence, and response.
2. Check artifact/config skew, cold start, overload, partial batch, timeout, cancellation, provider outage, fallback, and mixed-version rollout.
3. Inspect health/readiness semantics, autoscaling signals, cache identity, canary/shadow evaluation, alerts, and operator disable.
4. Separate performance evidence from quality/drift evidence.

## Handoff

Return the request class, loaded model/preprocessing/config identity, queue/routing path and the observed contract violation. Pair an overloaded, canceled or degraded request with a normal control. Pass the violated admission, batching, artifact or fallback boundary and an observable recovery criterion into Improve Model Serving & Monitoring.
