export const projects = new Map();
export function reset() {
  projects.clear();
  projects.set('p1', { id: 'p1', ownerId: 'alice', title: 'Roadmap' });
  projects.set('p2', { id: 'p2', ownerId: 'bob', title: 'Budget' });
}
reset();
