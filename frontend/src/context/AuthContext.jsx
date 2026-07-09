import { createContext, useContext, useEffect, useState } from "react";
import client from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setLoading(false);
      return;
    }
    client
      .get("/users/me")
      .then(({ data }) => {
        setUser(data);
        localStorage.setItem("user", JSON.stringify(data));
      })
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const persistSession = (tokenPair) => {
    localStorage.setItem("access_token", tokenPair.access_token);
    localStorage.setItem("refresh_token", tokenPair.refresh_token);
    localStorage.setItem("user", JSON.stringify(tokenPair.user));
    setUser(tokenPair.user);
  };

  const login = async (email, password) => {
    const { data } = await client.post("/auth/login", { email, password });
    persistSession(data);
    return data.user;
  };

  const register = async (payload) => {
    const { data } = await client.post("/auth/register", payload);
    persistSession(data);
    return data.user;
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
