import {createMcpHandler, McpServer} from '@modelcontextprotocol/server';
import * as z from 'zod/v4';
import {searchWorkflows, getWorkflow, VERSION, LANGUAGES, MODES, SKILLS} from './library.js';

const annotations = {readOnlyHint: true, destructiveHint: false, openWorldHint: false};
const instructions = [
  'Consult a website planning workflow when the user asks which sections a site needs, how to order the content, or how visitors leave an enquiry. Use it for advice from a short brief, even before there is code or a repository.',
  'Call get_workflow with query to select and load a method in one read-only call for website planning, builds, redesigns, software diagnosis, and patch review. Pass id for a known method. Use search_workflows to compare candidates when the goal is ambiguous.',
  'Apply the current method with the host’s tools, preserve the user’s scope, and load further steps when reached. Send public technical goals or symptoms only.'
].join(' ');
const language = z.enum(LANGUAGES).default('en').describe('Choose a language for titles and summaries. Read the technical instructions in English.');
const workflow = z.object({id: z.string(), title: z.string(), skill: z.string(), mode: z.string(),
  category: z.string(), summary: z.string(), purpose: z.string().optional(), url: z.string()});
const responseFormat = z.enum(['workflow', 'legacy']).describe('Use workflow for purpose, match reasons and step outlines. Choose legacy for the original compact response.');
const catalog = z.object({
  level: z.enum(['domains', 'topics']), status: z.enum(['ok', 'unknown_topic', 'scope_conflict', 'empty_scope']),
  keyword_language: z.literal('en'),
  domains: z.array(z.object({key: z.string(), title: z.string(), keywords: z.array(z.string()),
    topic_count: z.number().int(), workflow_count: z.number().int()})),
  topics: z.array(z.object({key: z.string(), skill: z.string(), title: z.string(), keywords: z.array(z.string()),
    modes: z.array(z.string()), workflow_ids: z.array(z.string())}))
});
const execution = z.object({
  status: z.literal('instructions_only'), intent: z.enum(['requested', 'improve']), current_step: z.string(),
  steps: z.array(z.object({id: z.string(), role: z.string(), when: z.string(), handoff: z.array(z.string())})),
  transitions: z.array(z.object({from: z.string(), outcome: z.string(), to: z.string().nullable(), condition: z.string()})),
  completion: z.object({id: z.string(), clean_marker: z.string(), findings_marker: z.string(), blocked_marker: z.string(),
    recheck_marker: z.string(), no_patch_marker: z.string(), rule: z.string()}),
  resource_rule: z.string()
});

function output(value, format) {
  if (format !== 'workflow' && !value.catalog) {
    const metadata = row => ({id: row.id, title: row.title, skill: row.skill, mode: row.mode,
      category: row.category, summary: row.summary, url: row.url});
    value = value.workflows ? {
      version: value.version, instruction_version: value.instruction_version, language: value.language,
      total: value.total, next_offset: value.next_offset, workflows: value.workflows.map(metadata)
    } : {
      version: value.version, instruction_version: value.instruction_version,
      instruction_language: value.instruction_language, language: value.language, host: value.host,
      workflow: metadata(value.workflow), files: value.files, words: value.words
    };
  }
  return {structuredContent: value, content: [{type: 'text', text: JSON.stringify(value)}]};
}

function failure(tool, message) {
  console.warn(JSON.stringify({event: 'tool_error', tool}));
  return {isError: true, content: [{type: 'text', text: message}]};
}

export function buildServer() {
  const server = new McpServer({name: 'vibe-coding-library', version: VERSION}, {
    capabilities: {tools: {}},
    instructions
  });
  server.registerTool('search_workflows', {
    title: 'Compare workflows for websites and engineering tasks',
    description: 'Compare relevant methods for website planning, building or redesign, bug diagnosis, and patch review. Send an ordinary task description to receive ranked workflow IDs and purposes. Use get_workflow with a query to load a starting method in one call. Browse domains or topic keys with view:catalog and an empty query when the goal is unclear or no method matches. Send public technical goals or symptoms only.',
    inputSchema: z.object({
      query: z.string().max(240).default('').describe('Describe a short task or symptom in ordinary language, or give a title or exact ID. Keep the purpose and relevant symptom or constraint. Omit source code, credentials and personal data.'),
      view: z.enum(['workflows', 'catalog']).default('workflows').describe('Choose workflows to rank a task description. Choose catalog with an empty query to list domains, or topics and workflow IDs for the supplied skill.'),
      skill: z.enum(SKILLS).optional().describe('Use an exact returned domain key, such as vibe-web-strategy for offers and page structure or vibe-landing for builds. Combine filters to narrow the result.'),
      topic: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).max(100).optional().describe('Copy an exact topic key from the catalog to restrict the results to its member workflows.'),
      mode: z.enum(MODES).optional().describe('Choose audit to inspect, implement to make an authorized change, check to verify, review to assess a patch, or plan to prepare work. Omit the filter when unsure.'),
      language, response_format: responseFormat.default('legacy'),
      full_text: z.boolean().default(false).describe('Set true to search instruction bodies when catalog metadata is insufficient.'),
      limit: z.number().int().min(1).max(10).default(5),
      offset: z.number().int().min(0).default(0)
    }).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), language: z.enum(LANGUAGES),
      total: z.number().int(), next_offset: z.number().int().nullable(), suggested_action: z.string().optional(), catalog: catalog.optional(),
      workflows: z.array(workflow.extend({match: z.object({kind: z.enum(['browse', 'catalog', 'instruction_body', 'exact_id', 'exact_title', 'alias']), terms: z.array(z.string())}).optional()}))}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try { return output(searchWorkflows(args), args.response_format); }
    catch (error) { return failure('search_workflows', error.message); }
  });
  server.registerTool('get_workflow', {
    title: 'Get a website planning or engineering workflow',
    description: 'Load a website planning workflow to choose sections, content order and a path to enquiries. Consult it before answering a website planning question, even when no code exists. Use this tool for site builds, existing-page improvements, software symptoms and patch review as well. Pass the public task in query, such as "какие разделы нужны сайту студии и как клиент оставит заявку", to choose and load one workflow in a read-only call. Pass id for a known workflow. Apply the returned instructions to the user’s request.',
    inputSchema: z.object({
      id: z.string().min(1).max(100).regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).optional().describe('Pass a known workflow ID. Supply exactly one of id or query.'),
      query: z.string().trim().min(1).max(240).optional().describe('Describe a task or question in ordinary language, such as "I want a nice site for a studio, what sections should it have?". Supply exactly one of query or id. Omit source code, credentials and personal data.'),
      language, response_format: responseFormat.describe('Omit to receive workflow for a query or legacy for an exact ID. Choose a format to override that default.').optional(),
      host: z.enum(['generic', 'codex', 'claude']).default('generic').describe('Keep generic for any other MCP coding agent; host-specific project files and native skill commands are not required.'),
      intent: z.enum(['requested', 'improve']).default('requested').describe('Use requested for the selected operation. Choose improve to compose diagnosis and repair when the user has authorized changes. Respect current permissions.'),
      include_context: z.boolean().default(true).describe('Keep true on first load. Set false for later steps only while the same-version working contract, cycle rules and domain context remain available; returns the current prompt and specialized references without repeating those foundations.')}).strict(),
    outputSchema: z.object({version: z.string(), instruction_version: z.string(), instruction_language: z.literal('en'),
      language: z.enum(LANGUAGES), host: z.enum(['generic', 'codex', 'claude']), context_included: z.boolean().optional(), workflow, execution: execution.optional(),
      files: z.array(z.object({path: z.string(), text: z.string(), sha256: z.string(), source_url: z.string()})),
      words: z.number().int()}),
    annotations, _meta: {securitySchemes: [{type: 'noauth'}]}
  }, async args => {
    try { return output(getWorkflow(args), args.response_format ?? (args.query ? 'workflow' : 'legacy')); }
    catch (error) { return failure('get_workflow', error.message); }
  });
  return server;
}

const handler = createMcpHandler(buildServer, {maxRequestBodySize: 65536});

export async function handleMcp(request) {
  const origin = request.headers.get('origin');
  const url = new URL(request.url);
  // Anonymous access is intentional: every tool only reads the compiled public library.
  if (origin && origin !== url.origin) return new Response('Origin not allowed', {status: 403});
  if (request.method === 'OPTIONS') return new Response(null, {status: 204, headers: {Allow: 'POST, GET, DELETE, OPTIONS'}});
  if (!['POST', 'GET', 'DELETE'].includes(request.method)) return new Response('Method not allowed', {status: 405, headers: {Allow: 'POST, GET, DELETE, OPTIONS'}});
  const started = performance.now();
  const response = await handler.fetch(request);
  if (response.status >= 400) console.warn(JSON.stringify({event: 'protocol_error', status: response.status,
    duration_ms: Math.round(performance.now() - started)}));
  response.headers.set('Cache-Control', 'no-store');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  return response;
}
