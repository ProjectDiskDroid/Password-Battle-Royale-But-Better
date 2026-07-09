import { defineConfig } from 'vite';
import { resolve } from 'path';
export default defineConfig({
  root: './',
  server: {
    // port: 5173, // default, can change as needed
    open: true, // automatically open browser on dev start
    proxy: {
      '/api': 'http://localhost:3000' // Means requests to /api/… will be forwarded
    }
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      // Multi-page build - the leaderboard lives on its own page (leaderboard.html),
      // so both entry points need to be listed here or only index.html would get built.
      input: {
        main: resolve(__dirname, 'index.html'),
        leaderboard: resolve(__dirname, 'leaderboard.html'),
      }
    }
  }
});
