// ==============================
// Authentication context
// ==============================
import { createContext, useContext, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const navigate = useNavigate();
  const [token, setToken] = useState(localStorage.getItem("token"));

  // Log in by storing token and redirecting to dashboard.
  const login = (accessToken) => {
    localStorage.setItem("token", accessToken);
    setToken(accessToken);
    navigate("/dashboard");
  };

  // Log out by clearing token and redirecting to login.
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    navigate("/");
  };

  const value = useMemo(() => ({ token, login, logout }), [token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
