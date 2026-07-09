import axios from "axios";

const client = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
});

// Attach the access token to every outgoing request.
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// On a 401, try one silent refresh before giving up and logging the user out.
let isRefreshing = false;

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retried && !isRefreshing) {
      original._retried = true;
      isRefreshing = true;
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        const { data } = await axios.post("/api/v1/auth/refresh", null, {
          params: { refresh_token: refreshToken },
        });
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        original.headers.Authorization = `Bearer ${data.access_token}`;
        return client(original);
      } catch (refreshError) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export default client;
