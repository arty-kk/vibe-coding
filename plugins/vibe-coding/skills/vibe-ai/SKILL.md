---
name: vibe-ai
description: "Audit, implement or verify AI features, RAG, OCR, model tools, ML pipelines, evaluation or serving at the selected model/data boundary."
---

# AI, RAG & ML

Apply [the working contract](../../references/workflow.md) once. Select the owning decision/data boundary before choosing a prompt or model change.

## Choose the workflow

| Requested outcome | Prompt chain and distinguishing evidence |
|---|---|
| Define a new AI/ML problem | AI ML Problem Framing → the selected feature/pipeline workflow; preserve actor, decision-time data, baseline and acceptable failure |
| Correct an AI product response | AI Feature Audit → Improve AI Feature → typed output/refusal/fallback scenarios and the affected evaluation |
| Ground retrieved answers | RAG Audit → Improve RAG → query → retrieved sources/ACL/freshness → supported answer and citations |
| Extract document data | OCR Document AI Audit → Improve OCR Document AI → representative document/region → extracted/corrected/exported field states |
| Correct model tool use | LLM Agent Tools Audit → Improve LLM Agent Tools → tool choice/arguments, authorization and actual effect/replay trace |
| Make evaluation trustworthy | AI Evaluation Audit → Improve AI Evaluation → labelled controls, paired candidate/baseline results and uncertainty |
| Correct training/inference data | ML Pipeline Audit → Improve ML Pipeline → decision-time features, split/preprocessing/artifact lineage and held-out results |
| Correct serving behavior | Model Serving & Monitoring Audit → Improve Model Serving & Monitoring → artifact/routing identity, degraded load and fallback evidence |
| Correct a selected safety/release control | AI Safety & Governance Audit → Improve AI Safety & Governance → reachable misuse, enforcement, review and disable/recovery evidence |

Start at implementation when the defect/requirement and owner are already established. An audit-only request ends with supported findings. Verification-only work applies the relevant audit method to explicit acceptance criteria and reports expected/observed results without editing; it does not need a new check prompt just to change the label.

## Execute and recheck

Carry the failing case, allowed input/context, owner, expected result and exact model/prompt/data/tool/config identity into correction. Validate the deterministic contract first, then the semantic/model property with an appropriate evaluation. A mock/provider fixture proves its own boundary; it cannot establish actual model quality, live latency or production safety.

Return a failed case to its owning retrieval, parser, prompt, tool policy, data or serving layer. Keep the comparison inputs fixed so a changed result can be attributed to the candidate, and report stochastic variance where relevant. After acceptance is supported, finish the resulting patch through [Patch Checking](../vibe-review/references/patch-checking.md) until clean or blocked. Do not keep tuning against a held-out release set to manufacture a passing score.

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
