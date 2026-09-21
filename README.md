# Vibe Coding

**Understand the code. Make the change. Verify the result.**

46 skills and 241 focused engineering workflows for Codex and Claude Code: project mapping, planning, code review, debugging, implementation and release checks.

[Browse the catalog](https://arty-kk.github.io/vibe-coding) · [Русский](README.ru.md) · [Releases](https://github.com/arty-kk/vibe-coding/releases) · [Support](https://github.com/arty-kk/vibe-coding/issues)

## Install

### Codex

Add the public marketplace:

```sh
codex plugin marketplace add arty-kk/vibe-coding
```

Open the Plugins Directory in the desktop app, select **Vibe Coding**, and install **Vibe Coding**. Start a new task to load the skills. The marketplace name is `vibe-coding`.

Also available in the [OpenAI Plugins Directory](https://chatgpt.com/plugins/plugins_6aae54a259ac8191b56161d366fb6e51).

### Claude Code

```sh
claude plugin marketplace add arty-kk/vibe-coding
claude plugin install vibe-coding@vibe-coding
```

Start a new session and use `/vibe-coding:vibe`. Focused skills use the same namespace, for example `/vibe-coding:vibe-review`. See the [installation and update guide](plugins/vibe-coding/docs/INSTALL.md).

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
| Verify an MCP integration | `$vibe-mcp` | Audit the tool contract and authorization for the supported protocol version. |
| Fix web rendering | `$vibe-web` | Fix the hydration failure and verify the server/client boundary. |

Use the plugin picker if your host displays names as `vibe-coding:<skill>`. Requests can be written in English, Spanish, Russian or Chinese. The [web catalog](https://arty-kk.github.io/vibe-coding/) and bundled offline catalog default to English and include Español, Русский and 简体中文. The public site has separate language URLs; the offline catalog remembers your language choice. Both provide localized search, workflow titles, descriptions and prompts. Choose Codex or Claude Code before copying a prompt. Technical recipe instructions are in English.

## Engineering coverage

- Product behavior, design systems, accessibility, content, mobile and desktop applications.
- APIs, authentication, permissions, payments, notifications, caches, search and realtime state.
- SQL, NoSQL, Redis, Kafka, RabbitMQ, Celery, Temporal, ClickHouse, storage and vector databases.
- Kubernetes, Terraform, CI/CD, observability, reliability, recovery and release readiness.
- AI features, RAG, OCR, evaluations, agent tools and execution harnesses.
- MCP tools/transports/authorization, SSR and hydration, server actions and OAuth/OIDC sessions.
- API/schema evolution, transactional event delivery, build trust, incident response and serverless/edge lifecycles.

## How it works

The entry skill selects the relevant domain and operation. The assistant reads the selected recipe, follows current code to the owner of the contract, performs the requested work and verifies the affected behavior. Detailed recipes load only when needed.

Audit and review requests produce findings. Implementation requests authorize relevant changes. A bug probe examines one area per run and records its outcome. Repository instructions and the user's requested scope govern the work.

The [host integration](plugins/vibe-coding/references/hosts.md) respects Codex `AGENTS.md` and Claude Code `CLAUDE.md`/scoped rules without changing project instructions or host settings.

The plugin uses the host's existing tools. It adds no MCP server, background service, account connection, telemetry or API-key requirement. Individual projects may require their normal dependencies and credentials.

## Development

Python 3.10+ is required for the local tools; validation and packaging also require the pinned PyYAML dependency.

```sh
python3 -m pip install -r plugins/vibe-coding/requirements.txt -r site/requirements.txt
python3 plugins/vibe-coding/scripts/validate.py
python3 -m unittest discover -s tests -v
python3 plugins/vibe-coding/scripts/catalog.py search webhook --mode check
python3 plugins/vibe-coding/scripts/catalog.py search MCP --lang es
python3 plugins/vibe-coding/scripts/package.py --output dist/vibe-coding-1.3.0.zip
```

See [Contributing](CONTRIBUTING.md), [installation](plugins/vibe-coding/docs/INSTALL.md), [privacy](PRIVACY.md) and [license](LICENSE).
