import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: 'localhost', // or your preferred host
    port: 3000, // or your preferred port
  },
  build: {
    outDir: "dist",
    minify: true,
  }
})
