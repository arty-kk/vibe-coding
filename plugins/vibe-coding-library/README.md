# Vibe Coding Library

Search 241 engineering workflows and load one selected working context over MCP. The server returns the selected recipe, its domain skill, the working contract and directly required references. The audited instruction library is version 1.4.1; this MCP distribution is version 1.5.1.

Use `$vibe-library` in Codex or `/vibe-coding-library:vibe-library` in Claude Code. The search catalog supports English, Spanish, Russian and Simplified Chinese; technical instructions are in English.

The public Streamable HTTP endpoint is:

```text
https://vibe-coding-library.swift-seal-1081.chatgpt.site/library/mcp
```

No account, token or API key is required. `search_workflows` accepts technical keywords, operation and skill filters, catalog language and bounded pagination. `get_workflow` accepts a returned workflow ID and optional host preference. The agent applies the guidance with its existing repository tools and permissions.

The MCP server reads its compiled public library. It has no repository, local-file or connected-account access, and does not edit or deploy code. Do not send source code, credentials, personal data or confidential information as search input.

[Live server and examples](https://vibe-coding-library.swift-seal-1081.chatgpt.site/) · [Catalog](https://arty-kk.github.io/vibe-coding/) · [Source](https://github.com/arty-kk/vibe-coding) · [Support](https://github.com/arty-kk/vibe-coding/issues) · [Privacy](https://vibe-coding-library.swift-seal-1081.chatgpt.site/privacy) · [Terms](https://vibe-coding-library.swift-seal-1081.chatgpt.site/terms)

The complete offline Vibe Coding plugin remains available separately, with 46 local skills and all 241 recipes. The Library distribution uses one selection skill and retrieves the chosen instructions on demand.
