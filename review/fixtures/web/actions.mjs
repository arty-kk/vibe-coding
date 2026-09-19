'use server';
import { projects } from './data.mjs';

export async function renameProject({ projectId, actorId, title }) {
  const project = projects.get(projectId);
  if (!project || project.ownerId !== actorId) throw new Error('Forbidden');
  if (typeof title !== 'string' || !title.trim()) throw new Error('Invalid title');
  project.title = title.trim();
  return { id: project.id, title: project.title };
}
