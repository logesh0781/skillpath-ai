import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/**
 * Guards a route to signed-in users, optionally restricted to specific roles.
 * Usage: <ProtectedRoute roles={["instructor", "super_admin"]}><Page/></ProtectedRoute>
 */
export default function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-parchment">
        <p className="font-mono text-sm text-slate">Loading your path…</p>
      </div>
    );
  }
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;
  return children;
}
