import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // --- Add this 'server' section ---
  server: {
    // Set the port the development server will run on.
    port: 3000,
    // This is crucial for Docker. It exposes the server on all network interfaces
    // within the container, allowing Docker's port mapping to connect to it.
    host: true,
  },
})