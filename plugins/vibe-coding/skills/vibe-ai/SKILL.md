---
name: vibe-ai
description: "Audit, implement or verify AI features, RAG, OCR, model tools, ML pipelines, evaluation or serving at the selected model/data boundary."
---

# AI, RAG & ML

Apply [the working contract](../../references/workflow.md) once; read only the recipe for the requested result.

## Recipes

| Recipe | Operation |
|---|---|
| [AI Evaluation Audit](references/ai-evaluation-audit.md) | audit |
| [Improve AI Evaluation](references/ai-evaluation-polish.md) | implement |
| [AI Feature Audit](references/ai-feature-audit.md) | audit |
| [Improve AI Feature](references/ai-feature-polish.md) | implement |
| [AI ML Problem Framing](references/ai-ml-problem-framing.md) | plan |
| [AI Safety & Governance Audit](references/ai-safety-governance-audit.md) | audit |
| [Improve AI Safety & Governance](references/ai-safety-governance-polish.md) | implement |
| [LLM Agent Tools Audit](references/llm-agent-tools-audit.md) | audit |
| [Improve LLM Agent Tools](references/llm-agent-tools-polish.md) | implement |
| [ML Pipeline Audit](references/ml-pipeline-audit.md) | audit |
| [Improve ML Pipeline](references/ml-pipeline-polish.md) | implement |
| [Model Serving & Monitoring Audit](references/model-serving-monitoring-audit.md) | audit |
| [Improve Model Serving & Monitoring](references/model-serving-monitoring-polish.md) | implement |
| [OCR Document AI Audit](references/ocr-document-ai-audit.md) | audit |
| [Improve OCR Document AI](references/ocr-document-ai-polish.md) | implement |
| [RAG Audit](references/rag-audit.md) | audit |
| [Improve RAG](references/rag-polish.md) | implement |


Use [MCP](../vibe-mcp/SKILL.md) for protocol/transport conformance and [Harness](../vibe-harness/SKILL.md) for durable execution/checkpoint recovery. This skill owns model decisions, grounding and tool-selection quality.

For a verification-only request, apply the relevant audit recipe to the stated acceptance criteria and report the measured result and gaps. Verification alone does not authorize implementation; a separate check recipe is not required.
