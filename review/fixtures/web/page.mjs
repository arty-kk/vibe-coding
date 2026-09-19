import { projects } from './data.mjs';
import { getCurrentUser } from './session.mjs';

export function loadProjectPage(projectId) {
  const user = getCurrentUser();
  const project = projects.get(projectId);
  if (!user || !project || project.ownerId !== user.id) throw new Error('Forbidden');
  return { project: { id: project.id, title: project.title }, formDefaults: { projectId, actorId: user.id } };
}
