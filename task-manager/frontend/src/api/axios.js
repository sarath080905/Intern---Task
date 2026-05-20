// ==============================
// API client configuration
// ==============================
// Create a shared Axios instance for backend calls.
import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || import.meta.env.API_BASE_URL || "http://127.0.0.1:8000",
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
