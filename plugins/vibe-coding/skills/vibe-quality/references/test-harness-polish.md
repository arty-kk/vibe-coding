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

- Demonstrate the test fails on the original defect when safely possible, then passes after the fix.
- Run the narrow test plus the directly affected suite/type/build checks.
- Report flaky, skipped, service-dependent, browser, or production-only gates separately.
