// userSession.js
import { writable } from 'svelte/store';

export const isAuthenticated = writable(false);
export const userData = writable(null);