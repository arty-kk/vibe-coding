# Delivery Restore & Rollback Check

## Goal

Verify the selected release or recovery path against exact artifact identity, compatible state and agreed recovery criteria.

## Context

Identify exact release/configuration identity, required recovery guarantee, current schema/data compatibility, backup identity, RPO/RTO criteria and authorized isolated environment.

## Scenarios

Select the cases that test the requested guarantee. Define expected state/effects before execution; use the authorized environment and a valid control.

- Build the same revision from clean inputs and compare the expected reproducibility/provenance properties and artifact digest lineage.
- Deploy/promote by digest through a safe environment, trigger health failure, pause/abort, and verify rollback or forward-fix decision.
- Toggle/target/fail the changed flag/config and verify defaults, cohort isolation, telemetry, rollback, and expiry ownership.
- Restore backups into isolated infrastructure, rebuild dependencies/config, validate data/application invariants, and measure RPO/RTO.
- Exercise loss of one failure domain/control-plane dependency and verify documented DR authority, communication, and return-to-primary procedure.

## Verification

Compare restored application data and behavior, artifact/configuration identity, lost work and measured recovery time; list unexercised deployment or disaster-recovery stages.

## Execute and decide

Fix the tested release/configuration, current state compatibility, backup/consistency point and recovery criteria before rehearsal. Establish a normal application/data control, then perform only the selected authorized promotion, abort, rollback or isolated restore sequence.

Verify the actual running artifact/configuration and restored business invariants, not merely process health or archive extraction. Measure lost acknowledged work and elapsed time from the agreed recovery start to usable application state, including required dependencies/operator steps. Separate observed timings from an unexercised full disaster scenario.

Return passed, failed or blocked for the stated recovery stage. Pass a failed identity/state/procedure link to the authorized owner repair, repeat its rehearsal/control after correction and finish Patch Checking for changed source. A missing backup, environment or safe action remains an explicit gate.
