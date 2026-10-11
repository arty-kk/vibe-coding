# Architecture Probe

## Scope

Inspect one dependency or ownership relationship. Establish the governing rule from project instructions, an ADR, package API, configured boundary tool or a demonstrated build/runtime failure. Folder placement and architecture preferences alone do not establish a defect.

## Procedure

1. Trace the selected import, module API, composition path or generated-source chain. Identify both sides and the rule they must preserve.
2. Check for a real cycle, forbidden dependency/type, conflicting rule owners, wrong instance scope or generated output that disagrees with its source.
3. Locate the defining owner. If authorized, repair the dependency or rule there and update direct callers; preserve supported public interfaces.
4. A suppression, widened alias or cast must not substitute for restoring the rule. Introduce a shared contract or move behavior only when the demonstrated dependency needs it.

## Verification

Run the relevant existing boundary/type/build/generation checks and inspect affected imports or consumers. If execution is unavailable, report the rule and source evidence inspected, with the unverified build/runtime consequence. Apply the selection/history and result rules in the parent skill.
