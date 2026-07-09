import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-30 border-b border-mist bg-parchment/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
        <Link to="/" className="flex items-center gap-2">
          <span className="font-display text-xl font-semibold text-ink">SkillPath</span>
          <span className="rounded-full bg-trail px-2 py-0.5 text-[10px] font-mono uppercase tracking-wide text-parchment">AI</span>
        </Link>

        <nav className="hidden gap-6 font-body text-sm text-slate md:flex">
          <Link to="/courses" className="hover:text-trail">Explore paths</Link>
          {user?.role === "instructor" && <Link to="/instructor" className="hover:text-trail">Instructor studio</Link>}
          {user?.role === "super_admin" && <Link to="/admin" className="hover:text-trail">Admin</Link>}
          {user && <Link to="/dashboard" className="hover:text-trail">Dashboard</Link>}
        </nav>

        <div className="flex items-center gap-3">
          {user ? (
            <>
              <div className="hidden items-center gap-2 rounded-full bg-white px-3 py-1 text-xs font-mono text-slate shadow-sm md:flex">
                <span className="text-waypoint">★ {user.xp_points} XP</span>
                <span className="text-summit">🔥 {user.current_streak}d</span>
              </div>
              <button
                onClick={() => { logout(); navigate("/login"); }}
                className="rounded-lg border border-mist px-3 py-1.5 text-sm text-ink hover:border-trail hover:text-trail"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm text-ink hover:text-trail">Log in</Link>
              <Link to="/register" className="rounded-lg bg-trail px-4 py-1.5 text-sm font-medium text-parchment hover:bg-trailLight">
                Get started
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
