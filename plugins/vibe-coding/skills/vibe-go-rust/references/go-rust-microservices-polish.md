# Improve Go Rust Microservices

## Goal

Correct the selected Go or Rust service behavior, preserving task ownership, cancellation, resource bounds and shutdown.

## Domain rules

- Use structured ownership (`errgroup`/task groups/join sets or existing equivalents) and propagate deadlines/cancellation to all child work.
- Bound queues, tasks, streams, pools, and retries before increasing parallelism; reject work or shed load explicitly at saturation.
- Keep blocking I/O/CPU off async executors and minimize lock scope; establish one lock order where multiple locks are unavoidable.
- Preserve stable API/error contracts and attach causal context internally without exposing implementation or secrets.
- Implement graceful shutdown as an ordered state transition with readiness change, admission stop, drain/cancel deadline, and final resource closure.

## Validation

- Run repository tests plus Go race/vet/static checks or Rust clippy/test/loom/miri/sanitizer checks where already supported and applicable.
- Exercise cancellation, deadline, downstream stall, connection loss, concurrent shutdown, panic/error propagation, and repeated start/stop.
- Measure live goroutines/tasks, queue depth, memory, connections, latency, and drain completion under representative concurrency.

Correct the owning spawn/join, admission, cancellation or shutdown boundary while preserving already committed effects and supported response semantics. Replay the controlled wait/I/O/commit interleaving and feed its lifecycle/resource observations to the concurrency check. A failed child cleanup or drain returns to that owner; supported acceptance proceeds to Patch Checking. Do not substitute arbitrary sleeps or broader parallelism for the missing ownership guarantee.
