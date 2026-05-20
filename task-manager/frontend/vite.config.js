// ==============================
// Vite configuration
// ==============================
// This file configures the frontend build tool and React plugin.
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
});
