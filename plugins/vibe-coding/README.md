# Vibe Coding

43 skills and 221 engineering workflows for Codex: repository mapping, planning, review, debugging, implementation and verification.

[Website and catalog](https://arty-kk.github.io/vibe-coding) · [Repository](https://github.com/arty-kk/vibe-coding) · [Support](https://github.com/arty-kk/vibe-coding/issues)

## Install

```sh
codex plugin marketplace add arty-kk/vibe-coding
```

Select the Vibe Coding marketplace in the desktop Plugins Directory, install Vibe Coding, and start a new task.

## Use

Ask: `Use Vibe Coding. Map this repository and explain its main contracts.`

Choose `$vibe-review` for a patch, `$vibe-probe` for one bug, `$vibe-task` for a task brief, or a domain skill from the [skill catalog](references/catalog.md).

[Browse recipes](CATALOG.html) · [Workflow](references/workflow.md) · [Installation](docs/INSTALL.md) · [Maintenance](docs/MAINTENANCE.md)

## Local tools

Python 3.10+:

```sh
python3 scripts/catalog.py search webhook --mode check
python3 scripts/catalog.py show patch-checking
python3 scripts/validate.py
python3 scripts/package.py --output ../vibe-coding-1.0.2.zip
```

MIT License. No bundled MCP server, account connection or telemetry.
