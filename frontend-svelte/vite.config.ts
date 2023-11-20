import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// Import the path module to resolve paths
import path from 'path';

// Configuring Vite to proxy API requests to Django to avoid CORS issues
// https://vitejs.dev/config/server-options.html#server-proxy

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  build: {
    // Specify outDir which is where production build files will be written
    outDir: path.resolve(__dirname, '../core/static/frontend'),
    sourcemap: true, // Enable sourcemaps for production
    rollupOptions: {
      // If needed, configure additional Rollup options here
      input: {
        main: path.resolve(__dirname, 'src/main.ts'),
      },
      output: {
        // To match the IIFE format
        format: 'iife', 
        // Global name when using IIFE format
        name: 'app', 
        // Output file, you could name it bundle.js as in your Rollup config
        entryFileNames: 'bundle.js',
      },
    },
  },
  server: {
    proxy: {
      // assuming the Django backend is served from localhost:8000
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      // if media files served from Django
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      // if static files served from Django
      '/static/frontend': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      // add more proxies as needed
    },
  },
});
