import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";
import toast from "react-hot-toast";
import { useAuth } from "../../context/AuthContext";

export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (values) => {
    setSubmitting(true);
    try {
      const user = await login(values.email, values.password);
      toast.success(`Welcome back, ${user.name.split(" ")[0]}`);
      navigate(user.role === "instructor" ? "/instructor" : user.role === "super_admin" ? "/admin" : "/dashboard");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Could not log in — check your details");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-64px)] items-center justify-center bg-map-texture px-4">
      <div className="w-full max-w-md rounded-2xl border border-mist bg-white/90 p-8 shadow-sm">
        <h1 className="font-display text-2xl font-semibold text-ink">Continue your path</h1>
        <p className="mt-1 text-sm text-slate">Log in to pick up where you left off.</p>

        <form onSubmit={handleSubmit(onSubmit)} className="mt-6 space-y-4">
          <div>
            <label className="text-xs font-mono uppercase text-slate">Email</label>
            <input
              type="email"
              {...register("email", { required: "Email is required" })}
              className="mt-1 w-full rounded-lg border border-mist px-3 py-2 focus:border-trail"
              placeholder="you@example.com"
            />
            {errors.email && <p className="mt-1 text-xs text-summit">{errors.email.message}</p>}
          </div>
          <div>
            <label className="text-xs font-mono uppercase text-slate">Password</label>
            <input
              type="password"
              {...register("password", { required: "Password is required" })}
              className="mt-1 w-full rounded-lg border border-mist px-3 py-2 focus:border-trail"
              placeholder="••••••••"
            />
            {errors.password && <p className="mt-1 text-xs text-summit">{errors.password.message}</p>}
          </div>
          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-lg bg-trail py-2.5 font-medium text-parchment hover:bg-trailLight disabled:opacity-60"
          >
            {submitting ? "Logging in…" : "Log in"}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-slate">
          New here? <Link to="/register" className="text-trail hover:underline">Create an account</Link>
        </p>
      </div>
    </div>
  );
}
