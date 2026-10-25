# Document the Repository

## Scope

Create or update the requested README using current repository evidence. Preserve a useful existing format and the user’s documentation language; an exact heading or universal section template is not required.

## Procedure

1. Inspect entry docs, application/package roots, manifests and lockfiles, supported scripts, configuration examples, CI/runtime files and directly relevant tests.
2. Explain project purpose and supported capabilities, principal entry points/owners and links to canonical detailed specifications.
3. Document actual prerequisites and setup/run/verification commands. Check flags, paths, environment-variable names and regeneration ownership against their defining sources.
4. Include data/migration/runtime/deployment notes only when needed to operate this project. Keep detailed runbooks linked rather than copied into the README.
5. Resolve stale factual examples against current sources. Distinguish intended product requirements from observed implementation when they disagree; do not rewrite the specification to conceal a bug.

## Verification

Check documented paths and links, commands and examples, configuration names and supported capabilities. Run safe relevant examples where possible; identify external prerequisites not exercised. Omit invented features, secrets, placeholder sections and duplicated agent policies from `AGENTS.md` or `CLAUDE.md`.

Make the handoff useful to a new maintainer: they should know what the project does, which maintained entry to use, how to run the relevant checks and where deeper operating constraints live. Correct failed examples at their maintained owner and recheck them. A saved README change finishes through Patch Checking; an explanation requested in chat does not create an unsolicited documentation file.
