# Release Artifact Trust Check

## Operation

Verify the selected source-to-release-to-environment artifact contract without changing release state. Read [supply-chain boundaries](../../../references/supply-chain.md). Upstream exploit remediation belongs to Security; this check establishes what bytes are being promoted and whether they can be recovered safely.

## Context

The exact source commit, build identity, candidate artifact/digest, required CI and provenance policy, target environment and rollback contract. Identify which publication/promotion/restore checks are authorized and available.

## Domain invariants

- The checked source/build inputs and approved release contents identify the same candidate artifact.
- The published and promoted bytes match the tested object or have explicit evidence for any rebuild equivalence.
- Checksum integrity, authorized builder/publisher identity and policy-required attestations are independently established.
- Configuration, data/schema/event compatibility and available rollback artifacts preserve the intended recovery path.
- Local assembly, remote publication, deployment and restore evidence are not substituted for one another.

## Establish the chain

Record the source commit/tag, build identity, toolchain and lockfile inputs, required CI results, archive/container digest, published asset identity and target environment. Use exact identifiers rather than a moving branch name or latest tag. Define the repository's provenance/signature/inventory policy before judging missing metadata.

## Artifact checks

- Confirm that required checks ran on the source inputs used to build the candidate, including relevant generated files and dependency state.
- Compare the actual archive/image contents with the approved release inventory. Check unexpected files, sensitive paths, symlinks/path traversal, missing runtime assets and version/manifest disagreement.
- Verify the digest of the candidate and the downloaded published asset. A matching checksum detects changed bytes; it does not by itself prove the authorized builder or publisher.
- Where required, validate signatures/attestations against the expected identity and subject digest. An SBOM is an inventory, not evidence that every listed component was safe or that the build was trusted.
- Confirm the promoted object is the tested object. If the system rebuilds per environment, identify the changed inputs and the evidence needed to establish equivalence rather than assuming it.

## Runtime and recovery checks

Trace deployment configuration to the same immutable artifact and inspect version reporting. Identify mutable configuration, migrations, feature flags and external contracts that may change behavior despite identical application bytes.

Verify that a rollback candidate is available and compatible with the current schema, stored data and events. When rollback cannot be safe, identify the bounded forward-fix or restore plan and the evidence supporting it. Do not trigger a deployment or restore merely to complete an inspection request; use an existing approved test environment or recorded exercise where available.

## Verification method

Use repository-native build, digest, archive and attestation tools. Rebuild only when reproducibility is part of the selected promise; compare actual bytes and report nondeterministic inputs. Use synthetic canaries for exclusion checks and avoid exposing real secret values. Pair failure cases with a valid package so an always-rejecting gate is not considered sufficient.

## Evidence and limitations

Report each link as verified, failed or not exercised with exact identifiers, commands and evidence. Separate local assembly, remote publication, environment promotion and recovery readiness. Tie failures to the owning source and one repair direction; do not infer production readiness solely from a green build or a locally valid ZIP.

Pass a failed link with candidate/downloaded/runtime digest, expected builder/policy identity and the violated inventory/compatibility condition into the authorized owning repair. Repeat that same comparison after correction and review any changed source patch. New publication, promotion or restore is not an automatic next step of an inspection-only result.
