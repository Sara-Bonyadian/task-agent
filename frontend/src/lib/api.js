import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // Reads from .env.development
  timeout: 10000,
});

// Simple error logging for now
api.interceptors.response.use(
  (resp) => resp,
  (err) => {
    console.error("[API]", err?.response?.status, err?.message);
    return Promise.reject(err);
  }
);

// Example service for tasks
export const TaskService = {
  list(params = {}) {
    return api.get("/tasks", { params }).then((r) => r.data);
  },
};
