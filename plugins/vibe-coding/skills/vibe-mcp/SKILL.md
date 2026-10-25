---
name: vibe-mcp
description: "Audit, implement or verify MCP discovery, schemas, transport, result handling and authorization for supported versions."
---

# MCP servers & clients

Read [the shared workflow](../../references/workflow.md) once, then the recipe matching the user's operation. The target is an existing MCP implementation or an explicitly requested MCP contract, not installation of arbitrary servers.

## Workflow

MCP Server Audit → Improve MCP Server → MCP Protocol & Authorization Check → [Patch Checking](../vibe-review/references/patch-checking.md).

Carry the actual client/SDK/protocol window, transport, advertised operation, trusted principal and expected result/effect between prompts. Start at implementation for an established failure or at the check for verification-only work. A deliberately public read-only capability does not acquire an OAuth requirement merely because private-data tools need authentication.

Trace discovery → accepted schema → transport dispatch → call-time policy → handler/effect → serialized result → client interpretation. Correct the first violating owner and replay the same request with a valid control and its relevant invalid/denied case. Transport success, tool execution success and a consumer's successful workflow completion are different observations.

A failed header/result/principal boundary returns to that owner and is rechecked through the real available transport, then the resulting patch receives repeated Patch Checking. Missing host, cryptographic verifier or provider evidence stays explicit. Do not upgrade the SDK, add extensions or change supported protocol eras merely to make an unrelated example fit.

| Request | Recipe |
|---|---|
| Inspect a server/client contract without edits | [MCP Server Audit](references/mcp-server-audit.md) |
| Fix or implement a named contract | [Improve MCP Server](references/mcp-server-polish.md) |
| Verify protocol, tool results or authorization | [MCP Protocol & Authorization Check](references/mcp-protocol-auth-check.md) |

The recipes share [version and trust boundaries](../../references/mcp-contract.md). Select the repository's supported SDK/protocol version before applying a rule. Do not treat an optional feature or a newer specification as an automatic migration requirement. An audit-and-fix request includes the correction and meaningful verification.

Durable application execution belongs to [Harness](../vibe-harness/SKILL.md); model tool-choice quality belongs to [AI](../vibe-ai/SKILL.md). Keep protocol compliance separate from those concerns.
