# Build Supply Chain Audit

## Operation

Inspect the selected dependency, CI or build trust boundary without product edits. Read [supply-chain boundaries](../../../references/supply-chain.md). Establish a reachable path from less-trusted input to execution, credentials or release bytes before reporting a vulnerability.

## Required input

The selected dependency/build/publishing workflow, trigger and ref, actor-controlled inputs, executing identity, available privileges and intended artifact. Identify the actual trust crossing and permitted publication policy.

## Domain invariants

- Untrusted source, scripts, cache entries and artifacts cannot execute with publishing authority merely because an earlier job succeeded.
- Build inputs resolve to the intended registry/ref/digest and lockfile under the repository’s dependency policy.
- Privilege follows the job’s required operation and cannot be expanded by attacker-controlled event or artifact metadata.
- Release bytes come from an explicitly approved inventory; unexpected sensitive files and escaping paths fail before publication.
- Integrity checks, publisher identity, provenance and inventory are verified as distinct properties against the project’s actual policy.

## Goal and scope

Determine who controls each build input, where code executes and which identity can publish the result. Follow one actual workflow or dependency installation from trigger to artifact. Keep final promotion/rollback verification with Recovery, while inspecting upstream trust violations that can taint its inputs.

## Inspect

- Workflow triggers, event payloads, branch/ref selection, reusable workflows, actions, runner identity, token permissions, environments and secret exposure.
- Checkout of pull-request code, install/build scripts, dependency lifecycle hooks, registry configuration, lockfiles, immutable references and generated sources.
- Cache keys/scopes, artifact producers/downloads, filenames, extraction paths, output variables and handoff between unprivileged and privileged jobs.
- Release assembly, approved file inventory, package exclusions, signing/attestation policy, publishing credentials and logs.

## Audit method

1. Draw the concrete trust path: actor-controlled input → selected ref/data → execution step → available privileges → artifact or external effect.
2. Distinguish merely reading untrusted source from executing it. Trace shell interpolation, script hooks and downloaded artifacts where the workflow crosses that boundary.
3. Compare the identity and permissions of producer and consumer jobs. A successful earlier workflow or familiar artifact name does not make its contents trusted.
4. Inspect dependency and cache resolution under the actual configuration. Confirm which registry, digest/ref and lockfile govern the selected build; do not infer dependency confusion from a package name alone.
5. Inspect the exact release contents using synthetic canaries where useful. Demonstrate accidental private-file inclusion without reading or printing real secrets.

## Issue classes and priority

Prioritize reachable credential theft, unauthorized publication, arbitrary code execution in a privileged job and attacker-controlled release bytes. Next consider cache/artifact poisoning, mutable dependency inputs contrary to release policy, unsafe extraction and weak separation of pull-request and publishing work. A missing SBOM or signature is not automatically a vulnerability without the established trust/consumer requirement.

## Evidence requirements

Cite the triggering actor/event, exact workflow/source lines, controlled value, execution sink, available privilege and resulting impact. Provide a minimal safe reproduction or complete source trace, one correction at the trust owner and an observable regression. Do not execute an exploit against a live registry or transmit credentials to prove reachability.

Bound the conclusion to inspected workflows and inputs. Keep checksum integrity, signer identity, build provenance and dependency inventory distinct; none individually proves every other property.

Pass the controlling actor/trigger/ref, exact execution sink, available privileges and synthetic input to Improve Build Supply Chain. Preserve a valid contribution/build control so the proposed correction can be judged against required release behavior. Do not replace a demonstrated path with a generic tool/registry recommendation.
