import { writable } from 'svelte/store';

import type { Workspace } from '../types/workspacesType';

export const workspaces = writable<Workspace[]>([]);