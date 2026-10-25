# Improve Test Harness

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Repair or add the test that proves the selected behavior, using controlled inputs and observable assertions.

## Domain rules

- Add or repair the nearest stable test at the contract boundary; avoid duplicating the implementation in test code.
- Use controllable clocks, deterministic IDs, bounded retries, and explicit synchronization for async/concurrent paths.
- Make skipped or environment-dependent checks visible and fail closed where the repository contract requires them.
- Keep fixtures minimal, representative, privacy-safe, and versioned with the contract they encode.

## Validation

First define the input, observable result and distinguishing failure. Select the nearest existing test boundary that actually reaches the owner, then control its time, identity, concurrency and external dependencies without mocking away the property under test. Repair the assertion/setup before widening production interfaces.

- Demonstrate the test fails on the original defect when safely possible, then passes after the fix.
- Run the narrow test plus the directly affected suite/type/build checks.
- Report flaky, skipped, service-dependent, browser, or production-only gates separately.

Pair a failure scenario with a healthy control so a broken harness or unavailable dependency cannot masquerade as successful rejection. When covering already-correct behavior, use a meaningful counterexample or a controlled mutation only when useful; do not invent a product defect to force a historical red test.

If validation exposes a product defect, return it to the appropriate implementation step within the user's authorized scope. Re-run the distinguishing assertion after repair, then review the full harness/product patch through Patch Checking until clean or blocked.
