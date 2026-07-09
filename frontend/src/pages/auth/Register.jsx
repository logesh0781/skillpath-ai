import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";
import toast from "react-hot-toast";
import { useAuth } from "../../context/AuthContext";

export default function Register() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm({ defaultValues: { role: "student" } });
  const { register: signup } = useAuth();
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);
  const role = watch("role");

  const onSubmit = async (values) => {
    setSubmitting(true);
    try {
      const user = await signup(values);
      if (user.status === "pending_approval") {
        toast.success("Account created — an admin will approve your instructor access shortly.");
        navigate("/login");
      } else {
        toast.success(`Welcome, ${user.name.split(" ")[0]}!`);
        navigate("/dashboard");
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "Registration failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-64px)] items-center justify-center bg-map-texture px-4">
      <div className="w-full max-w-md rounded-2xl border border-mist bg-white/90 p-8 shadow-sm">
        <h1 className="font-display text-2xl font-semibold text-ink">Start a new path</h1>
        <p className="mt-1 text-sm text-slate">Set up your account to begin.</p>

        <form onSubmit={handleSubmit(onSubmit)} className="mt-6 space-y-4">
          <div>
            <label className="text-xs font-mono uppercase text-slate">Full name</label>
            <input {...register("name", { required: "Name is required" })} className="mt-1 w-full rounded-lg border border-mist px-3 py-2 focus:border-trail" placeholder="Ada Lovelace" />
            {errors.name && <p className="mt-1 text-xs text-summit">{errors.name.message}</p>}
          </div>
          <div>
            <label className="text-xs font-mono uppercase text-slate">Email</label>
            <input type="email" {...register("email", { required: "Email is required" })} className="mt-1 w-full rounded-lg border border-mist px-3 py-2 focus:border-trail" placeholder="you@example.com" />
            {errors.email && <p className="mt-1 text-xs text-summit">{errors.email.message}</p>}
          </div>
          <div>
            <label className="text-xs font-mono uppercase text-slate">Password</label>
            <input type="password" {...register("password", { required: "Password is required", minLength: { value: 8, message: "At least 8 characters" } })} className="mt-1 w-full rounded-lg border border-mist px-3 py-2 focus:border-trail" placeholder="At least 8 characters" />
            {errors.password && <p className="mt-1 text-xs text-summit">{errors.password.message}</p>}
          </div>
          <div>
            <label className="text-xs font-mono uppercase text-slate">I am joining as a…</label>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {["student", "instructor"].map((r) => (
                <label key={r} className={`cursor-pointer rounded-lg border px-3 py-2 text-center text-sm capitalize ${role === r ? "border-trail bg-trail/10 text-trail" : "border-mist text-slate"}`}>
                  <input type="radio" value={r} {...register("role")} className="hidden" />
                  {r}
                </label>
              ))}
            </div>
            {role === "instructor" && (
              <p className="mt-1 text-xs text-slate">Instructor accounts need approval from a Super Admin before publishing courses.</p>
            )}
          </div>
          <button type="submit" disabled={submitting} className="w-full rounded-lg bg-trail py-2.5 font-medium text-parchment hover:bg-trailLight disabled:opacity-60">
            {submitting ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-slate">
          Already have an account? <Link to="/login" className="text-trail hover:underline">Log in</Link>
        </p>
      </div>
    </div>
  );
}
