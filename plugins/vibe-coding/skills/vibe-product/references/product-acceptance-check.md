# Product Acceptance Check

## Goal

Verify one selected product requirement, acceptance criterion, or release slice through bounded, reproducible evidence without reopening broad product discovery or unrelated implementation work.

## Context

Identify the requirement/acceptance ID or description, expected behavior, actor/state matrix, implementation summary or patch boundary, safe environment, and available repository-native commands or manual scenarios.

## Scenarios

- Exercise the happy path and the most important negative path for the selected actor.
- Verify loading, empty, error, retry, no-access, over-quota/no-plan, and success states only when reachable for this requirement.
- Confirm UI/API/data/copy/analytics/test behavior matches the same acceptance wording.
- Check that docs/maps are not contradicting the implemented behavior when they are part of the workflow.

## Execute and decide

Fix the requirement, candidate revision, actor/context and expected visible/durable result before testing. Establish the normal entry/action path, then execute the negative or recovery state that distinguishes the criterion. Inspect UI feedback, request/response and persisted effect at the actual boundary; run rendered/keyboard checks when that behavior is part of acceptance.

Return passed, failed or blocked per required criterion with the trigger and observed evidence. Feed a failure to the owning authorized repair, repeat its scenario/control after correction and finish Patch Checking on a changed patch. Do not expand one selected requirement into a new broad product audit.
