// ==============================
// API client configuration
// ==============================
// Create a shared Axios instance for backend calls.
import axios from "axios";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || import.meta.env.API_BASE_URL || "http://127.0.0.1:8000";

if (!import.meta.env.VITE_API_BASE_URL && !import.meta.env.API_BASE_URL) {
  console.warn(
    "No API_BASE_URL or VITE_API_BASE_URL set. Defaulting to http://127.0.0.1:8000. " +
    "Set API_BASE_URL in Vercel environment variables for production deployments."
  );
}

const API = axios.create({
  baseURL: apiBaseUrl,
});

// Attach the authorization token to each request if available.
API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

export default API;
