# Vibe Coding Library

Engineering methods for any coding agent supporting MCP over Streamable HTTP. Search 241 workflow entries from the task goal and load the current prompt with its domain instructions, required references and conditional next steps. Instructions and client distribution share version 1.6.1.

Direct MCP use needs no native skill installation. The optional native packages expose `$vibe-library` in Codex and `/vibe-coding-library:vibe-library` in Claude Code. Search supports English, Spanish, Russian and Simplified Chinese; technical purposes and instructions are English.

The public Streamable HTTP endpoint is:

```text
https://vibe-coding-library.swift-seal-1081.chatgpt.site/library/mcp
```

Select transport **Streamable HTTP**, authentication **None**. No publisher account, token or API key is required. Your agent or model provider retains its normal settings and charges.

`search_workflows` accepts a short technical goal, symptom, title or ID, such as `fix stale cache after a write`. Results expose the individual purpose, operation, stable ID and match reason. Explicit filters are preserved; result language does not restrict corpus language. Body search is opt-in.

`get_workflow` loads the ID with `host:generic` by default. `intent:requested` preserves the selected operation; `intent:improve` composes audit, already-authorized repair, relevant checks and repeated Patch Checking. This flag grants no permission. A known implementation starts at its implementation ID. Returned `execution` is an instruction outline, not execution state or a verdict.

Apply the text with your project tools and rules. Carry actual evidence between stages and fetch each reached next-step ID. Use `include_context:false` only while the same-version foundations and domain context remain available. Later prompts are not loaded in advance. Recheck corrections against the original patch boundary; only an actual final clean pass may emit the clean marker.

After a server update, reconnect or refresh discovery in clients that cache tool descriptions. Automatic tool choice remains controlled by the agent and its tool settings.

The MCP server reads its compiled public library. It has no repository, local-file or connected-account access, and does not edit or deploy code. Do not send source code, credentials, personal data or confidential information as search input.

[Live server and examples](https://vibe-coding-library.swift-seal-1081.chatgpt.site/) · [Catalog](https://arty-kk.github.io/vibe-coding/) · [Source](https://github.com/arty-kk/vibe-coding) · [Support](https://github.com/arty-kk/vibe-coding/issues) · [Privacy](https://vibe-coding-library.swift-seal-1081.chatgpt.site/privacy) · [Terms](https://vibe-coding-library.swift-seal-1081.chatgpt.site/terms)

The complete offline Vibe Coding plugin remains available separately, with 46 local skills and all 241 recipes. The Library distribution uses one selection skill and retrieves the chosen instructions on demand.

Use `response_format:workflow` on both tools for the current purposes and structured outline. Calls that omit the option retain the exact 1.5.1 response shape while still using current search and instruction content; this keeps previously published schemas working during continuous review.

Discover before searching when the topic is unknown:

```text
search_workflows({"view":"catalog"})
search_workflows({"view":"catalog","skill":"vibe-domain"})
search_workflows({"topic":"auth-permissions","mode":"implement","response_format":"workflow"})
get_workflow({"id":"auth-permissions-polish","response_format":"workflow"})
```

The compact catalog lists actual domain/topic keys and canonical English keywords without instruction bodies. Choose by the meaning of the user’s request; reuse known keys for the same library version. Topic lookup uses explicit membership, not an invented query term. Text search remains available, including Russian authorization forms. Unknown topic keys return catalog guidance. A miss does not authorize dropping an explicit filter. No embedding model, API key or external query processing is required. Existing requests that omit the new catalog/topic arguments retain their previous result shapes.

Text typo repair uses only the actual metadata vocabulary and registered concepts: words of at least five letters may be corrected by one edit or an adjacent transposition when the semantic target is unambiguous. Exact topic/workflow ID arguments are never fuzzy-corrected. Unknown or ambiguous phrases remain eligible for catalog-guided selection by the caller.
