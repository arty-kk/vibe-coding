# Test Coverage Audit

## Operation

Inspect the selected behavior and report evidence-backed defects; do not change product code.

## Goal

Find critical behavior that is untested, falsely tested, or fragile enough to allow regressions. Keep coverage gaps that matter to correctness, contracts, security, UX, or operability.

## Inspect

Tests, test utilities, fixtures, mocks, snapshots, coverage config, CI workflows, package scripts, product/traceability/test maps when present, and the source behavior those tests claim to protect. Include generated maps/docs only as discovery aids.

## Coverage issues

- Missing tests for reachable critical behavior, product acceptance, RBAC/ABAC decisions, payment/provider events, notification delivery, cache/search freshness, feature-flag states, mobile offline paths, extension permissions, or desktop local-runtime boundaries.
- Tests that assert implementation details while missing observable behavior.
- Mocks/stubs that bypass the risk being tested.
- Snapshot-only or smoke-only coverage for behavior with branching rules.
- Flaky-risk patterns: real timers/network, order coupling, shared mutable state, nondeterministic data, unawaited async work.
- CI not running the tests that protect important behavior.
- Tests or fixtures that encode outdated contracts and would hide regressions.

## Finding quality

- Include reachable surface, affected actors/consumers/states, expected behavior, acceptance criteria, and validation direction when discoverable.
- Cite both the behavior owner and the missing/weak test evidence.
- Make each finding about adding or repairing tests for one behavior owner and state the expected observable assertion.
- Do not create product-code change tasks unless the code is untestable because of a demonstrated behavior-boundary problem.

## Trace and hand off

Choose the required behavior and a reachable violating input/state. Follow the existing test's setup, exercised production path and assertions to determine whether it would detect that violation. Distinguish no coverage from an ineffective assertion, an inaccurate fixture and a CI path that never runs the test.

Pass Improve Test Harness the behavior owner, expected assertion, missing scenario and the narrow test boundary when changes are requested. Existing correct behavior may need added coverage without a product-code fix. Do not generate tests solely to repeat implementation text or increase coverage percentages.
