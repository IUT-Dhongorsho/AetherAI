import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000, // Force Vite to run on port 3000 as requested
    proxy: {
      '/api': {
        target: 'http://nafis-server.tail634f34.ts.net/aether-api',
        changeOrigin: true,
      },
      '/reports': {
        target: 'http://nafis-server.tail634f34.ts.net/aether-api',
        changeOrigin: true,
      }
    }
  },
  base: '/aetherai/'
})
