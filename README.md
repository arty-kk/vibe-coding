# Vibe Coding

**Understand the code. Make the change. Verify the result.**

43 Codex skills and 221 focused engineering workflows for project mapping, planning, code review, debugging, implementation and release checks.

[Browse the catalog](https://arty-kk.github.io/vibe-coding) · [Русский](README.ru.md) · [Releases](https://github.com/arty-kk/vibe-coding/releases) · [Support](https://github.com/arty-kk/vibe-coding/issues)

## Install

Add the public marketplace:

```sh
codex plugin marketplace add arty-kk/vibe-coding
```

Open the Plugins Directory in the desktop app, select **Vibe Coding**, and install **Vibe Coding**. Start a new task to load the skills. The marketplace name is `vibe-coding`.

This repository provides a public marketplace source. Availability in the universal Plugins Directory is managed separately through OpenAI review.

## Start working

```text
Use Vibe Coding. Map this repository and explain its main contracts.
```

| Task | Skill | Example |
| --- | --- | --- |
| Understand a repository | `$vibe-map` | Map the API, data owners and runtime flow. |
| Define implementation scope | `$vibe-task` | Turn these requirements into an implementation task with acceptance criteria. |
| Review a change | `$vibe-review` | Review this branch against main and report actionable defects. |
| Find a bug | `$vibe-probe` | Find and fix one new backend bug, then run the relevant checks. |
| Implement product behavior | `$vibe-product` | Implement the selected form behavior and verify its acceptance criteria. |
| Check a release | `$vibe-quality` | Assess this release against its required checks and report remaining gaps. |

Use the plugin picker if your host displays names as `vibe-coding:<skill>`. Requests can be written in English or Russian. The catalog interface and many examples are in Russian; engineering recipes are in English.

## Engineering coverage

- Product behavior, design systems, accessibility, content, mobile and desktop applications.
- APIs, authentication, permissions, payments, notifications, caches, search and realtime state.
- SQL, NoSQL, Redis, Kafka, RabbitMQ, Celery, Temporal, ClickHouse, storage and vector databases.
- Kubernetes, Terraform, CI/CD, observability, reliability, recovery and release readiness.
- AI features, RAG, OCR, evaluations, agent tools and execution harnesses.

## How it works

The entry skill selects the relevant domain and operation. Codex reads the selected recipe, follows current code to the owner of the contract, performs the requested work and verifies the affected behavior. Detailed recipes load only when needed.

Audit and review requests produce findings. Implementation requests authorize relevant changes. A bug probe examines one area per run and records its outcome. Repository instructions and the user's requested scope govern the work.

The plugin uses the host's existing tools. It adds no MCP server, background service, account connection, telemetry or API-key requirement. Individual projects may require their normal dependencies and credentials.

## Development

Python 3.10 or later is required only for the local catalog and packaging tools.

```sh
python3 plugins/vibe-coding/scripts/validate.py
python3 -m unittest discover -s tests -v
python3 plugins/vibe-coding/scripts/catalog.py search webhook --mode check
python3 plugins/vibe-coding/scripts/package.py --output dist/vibe-coding-1.0.3.zip
```

See [Contributing](CONTRIBUTING.md), [installation](plugins/vibe-coding/docs/INSTALL.md), [privacy](PRIVACY.md) and [license](LICENSE).
