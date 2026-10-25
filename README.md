# Vibe Coding

**Understand the code. Make the change. Verify the result.**

Engineering workflows for coding agents with MCP: project mapping, planning, code review, debugging, implementation and verification. The library offers 241 focused entry points; native offline packages provide 46 skills for Codex and Claude Code.

[Browse the catalog](https://arty-kk.github.io/vibe-coding) · [Русский](README.ru.md) · [Releases](https://github.com/arty-kk/vibe-coding/releases) · [Support](https://github.com/arty-kk/vibe-coding/issues)

## Install

### Vibe Coding Library via MCP

[Vibe Coding Library](https://vibe-coding-library.swift-seal-1081.chatgpt.site/) works with any coding agent supporting MCP through Streamable HTTP. Its two read-only tools select a method from the task goal and load the current prompt, required context and conditional next steps. No publisher account, token or API key is required. Direct MCP use needs no Codex or Claude installation; the optional native distribution adds a selection skill.

Add this Streamable HTTP endpoint to a compatible MCP client:

```text
https://vibe-coding-library.swift-seal-1081.chatgpt.site/library/mcp
```

For Claude Code, the public repository marketplace also provides the Library distribution:

```sh
claude plugin marketplace add arty-kk/vibe-coding
claude plugin install vibe-coding-library@vibe-coding
```

For other agents, select transport **Streamable HTTP** and authentication **None**. The tools describe when to use the library; no native skill command is required. Native packages expose `/vibe-coding-library:vibe-library` in Claude Code and `$vibe-library` in Codex. See the [Library package](plugins/vibe-coding-library/README.md) for the tool and privacy contracts.

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

Use the plugin picker if your host displays names as `vibe-coding:<skill>`. Requests can be written in English, Spanish, Russian or Chinese. The [web catalog](https://arty-kk.github.io/vibe-coding/) and bundled offline catalog default to English and include Español, Русский and 简体中文. The public site has separate language URLs; the offline catalog remembers your language choice. Both provide localized search, workflow titles, descriptions and prompts. The public site includes a generic MCP prompt alongside the Codex and Claude examples. Technical recipe instructions are in English.

## Engineering coverage

- Product behavior, design systems, accessibility, content, mobile and desktop applications.
- APIs, authentication, permissions, payments, notifications, caches, search and realtime state.
- SQL, NoSQL, Redis, Kafka, RabbitMQ, Celery, Temporal, ClickHouse, storage and vector databases.
- Kubernetes, Terraform, CI/CD, observability, reliability, recovery and release readiness.
- AI features, RAG, OCR, evaluations, agent tools and execution harnesses.
- MCP tools/transports/authorization, SSR and hydration, server actions and OAuth/OIDC sessions.
- API/schema evolution, transactional event delivery, build trust, incident response and serverless/edge lifecycles.

## How it works

Agents can discover actual keys before searching: call `search_workflows` with `view:catalog`, choose a domain, then list its topics with `view:catalog, skill:<key>`. Select a returned `topic` and the requested `mode` to retrieve exact workflow members. English keys are stable; labels support all four catalog languages. A free-text miss leads back to this catalog rather than an invented keyword or a missing-capability claim.

Search from a technical goal or symptom, then load the selected ID. An authorized correction carries evidence from audit to repair, relevant verification and repeated Patch Checking. A known fix starts at repair. Only the reached prompt body is loaded; its result becomes the input to the next step.

Patch Checking retains the original review base across corrections. A correction requires validation and another review of the complete resulting patch. Only an unchanged final pass with no qualifying findings and all required evidence may produce the clean marker. Missing evidence or repeated failure without progress stays blocked. Retrieving instructions never counts as executing a check.

Audit and review requests produce findings. Implementation requests authorize relevant changes. A bug probe examines one area per run and records its outcome. Repository instructions and the user's requested scope govern the work.

Every agent retains its own project rules and permissions. The optional [host integration](plugins/vibe-coding/references/hosts.md) explains Codex `AGENTS.md` and Claude Code `CLAUDE.md`/scoped rules; those files are not required for generic MCP use.

The offline plugin uses the host's existing tools and adds no server or account connection. The optional Library distribution connects to the public MCP service. Individual projects may require their normal dependencies and credentials.

## Development

Python 3.10+ is required for the local tools; validation and packaging also require the pinned PyYAML dependency.

```sh
python3 -m pip install -r plugins/vibe-coding/requirements.txt -r site/requirements.txt
python3 plugins/vibe-coding/scripts/validate.py
python3 -m unittest discover -s tests -v
python3 plugins/vibe-coding/scripts/catalog.py search webhook --mode check
python3 plugins/vibe-coding/scripts/catalog.py search MCP --lang es
python3 plugins/vibe-coding/scripts/package.py --output dist/vibe-coding-1.6.1.zip
```

See [Contributing](CONTRIBUTING.md), [installation](plugins/vibe-coding/docs/INSTALL.md), [privacy](PRIVACY.md) and [license](LICENSE).
