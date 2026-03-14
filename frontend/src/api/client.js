import axios from "axios";
import { logout } from "../utils/auth";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL || "https://fastapi-backend-6rew.onrender.com",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      logout();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export default api;
