import { writable } from 'svelte/store';

import type { Company } from '../types/companiesType';

export const companies = writable<Company[]>([]);