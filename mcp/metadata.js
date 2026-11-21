import metadata from './generated/metadata.json' with {type: 'json'};

export const VERSION = metadata.version;
export const INSTRUCTION_VERSION = metadata.instructionVersion;
export const DIGEST = metadata.digest;
export const LANGUAGES = metadata.languages;
export const MODES = metadata.modes;
export const SKILLS = metadata.domains;

export function libraryStatus() {
  return {service: 'Vibe Coding Library', version: VERSION, instruction_version: INSTRUCTION_VERSION,
    workflows: metadata.workflowCount, skills: metadata.skillCount, digest: DIGEST,
    tools: ['search_workflows', 'get_workflow', 'get_website_plan_workflow'], authentication: 'none'};
}
