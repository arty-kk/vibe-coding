import { AsyncLocalStorage } from 'node:async_hooks';
const context = new AsyncLocalStorage();
export const withUser = (user, action) => context.run(user, action);
export const getCurrentUser = () => context.getStore() ?? null;
