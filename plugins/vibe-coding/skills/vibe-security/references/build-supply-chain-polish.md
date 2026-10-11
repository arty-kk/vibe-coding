# Improve Build Supply Chain

## Operation

Implement the selected dependency, CI or release-assembly trust correction. Follow [supply-chain boundaries](../../../references/supply-chain.md). Use the demonstrated actor-to-effect path and existing release policy to define the change; avoid a blanket tooling migration.

## Required input

The selected dependency/build/publishing workflow, trigger and ref, actor-controlled inputs, executing identity, available privileges and intended artifact. Identify the actual trust crossing and permitted publication policy.

## Domain invariants

- Untrusted source, scripts, cache entries and artifacts cannot execute with publishing authority merely because an earlier job succeeded.
- Build inputs resolve to the intended registry/ref/digest and lockfile under the repository’s dependency policy.
- Privilege follows the job’s required operation and cannot be expanded by attacker-controlled event or artifact metadata.
- Release bytes come from an explicitly approved inventory; unexpected sensitive files and escaping paths fail before publication.
- Integrity checks, publisher identity, provenance and inventory are verified as distinct properties against the project’s actual policy.

## Goal and scope

Remove the specific route by which untrusted input gains execution privileges or enters approved release bytes. Complete directly affected workflow permissions, input validation, artifact handling, inventory and verification so the same behavior cannot bypass the fix through another step in the selected path.

## Establish acceptance criteria

Identify the controlling actor, trigger, selected ref, execution context, credentials and permitted output. Reproduce the unsafe behavior with synthetic data or a disposable fixture. Define a valid control build and the malicious/accidental input that must be rejected. Determine whether the owner is trigger design, script execution, dependency resolution, cache reuse or final package assembly.

## Implementation targets

- Separate untrusted contribution checks from privileged publication. Avoid checking out and executing attacker-controlled code after entering a context with publishing secrets.
- Minimize workflow token permissions at the owning scope. Preserve required release operations and use repository-native identity/environment controls rather than unexplained broad permission removal.
- Bind external actions, dependencies or tools to the immutable identity required by the project. Preserve lockfile/generator consistency and inspect lifecycle scripts that execute during installation.
- Treat downloaded artifacts and cache contents according to their producing trust domain. Verify identity and paths before extraction or execution; artifact names alone are not authority.
- Assemble releases from an explicitly reviewed inventory. Reject unexpected or sensitive files and symlink/path escapes before creating publishable output. Do not regenerate an approval list from arbitrary current files during every build.
- Keep diagnostics useful without revealing credentials or private file contents. Preserve the intended publisher and exact source/artifact association.

## Change discipline

Update the workflow or script that owns the boundary, plus directly dependent configuration and maintenance instructions. Do not paper over a failing build by disabling its security gate or rerunning privileged code with additional secrets. Preserve ordinary contribution and release paths and document any intentional workflow constraint.

## Validation

Show the original synthetic case fails before the correction and is rejected afterward, while the valid control still builds. Verify permissions/ref selection where possible, release inventory and archive bytes, deterministic assembly when promised, and relevant CI on the actual changed commit. For a dependency change run the necessary native checks; for packaging verify no final or partial artifact survives validation failure.

Report the repaired trust path, evidence, checks run and remaining hosted-runner or registry checks. Publish only within the user's existing authorization and the repository's applicable controls.
