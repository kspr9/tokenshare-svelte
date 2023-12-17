import { writable } from 'svelte/store';

import type { Contract } from '../types/contractsType';

export const contracts = writable<Contract[]>([]);