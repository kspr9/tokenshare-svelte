// userSession.js
import { writable } from 'svelte/store';
import type { UserProps } from '../types/userProps';

export const userData = writable<UserProps | null>(null);