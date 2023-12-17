import { writable } from 'svelte/store';

import type { Company, Workspace, Contract } from '../types/governanceTypes';


export const companies = writable<Company[]>([]);

export const contracts = writable<Contract[]>([]);

export const workspaces = writable<Workspace[]>([]);


