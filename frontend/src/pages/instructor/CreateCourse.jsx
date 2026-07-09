import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";
import client from "../../api/client";

const DIFFICULTIES = [
  { value: "beginner", label: "Beginner" },
  { value: "intermediate", label: "Intermediate" },
  { value: "advanced", label: "Advanced" },
];

export default function CreateCourse() {
  const navigate = useNavigate();
  const [skills, setSkills] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ defaultValues: { difficulty: "beginner", estimated_hours: 1 } });

  useEffect(() => {
    client.get("/skills").then(({ data }) => setSkills(data)).catch(() => {});
  }, []);

  const onSubmit = async (values) => {
    setSubmitting(true);
    try {
      const payload = {
        ...values,
        estimated_hours: parseFloat(values.estimated_hours) || 0,
        thumbnail_url: values.thumbnail_url || null,
      };
      await client.post("/courses", payload);
      toast.success("Course created!");
      navigate("/instructor");
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        toast.error(detail.map((d) => d.msg).join(", "));
      } else {
        toast.error(typeof detail === "string" ? detail : "Failed to create course.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const Field = ({ label, error, children }) => (
    <div>
      <label className="block text-sm font-medium text-ink mb-1">{label}</label>
      {children}
      {error && <p className="mt-1 text-xs text-summit">{error.message}</p>}
    </div>
  );

  const inputCls =
    "w-full rounded-lg border border-mist bg-white px-3 py-2 text-sm text-ink placeholder:text-slate focus:outline-none focus:ring-2 focus:ring-trail/40";

  return (
    <div className="mx-auto max-w-2xl px-6 py-8">
      <button
        onClick={() => navigate("/instructor")}
        className="mb-6 flex items-center gap-1 text-sm text-slate hover:text-trail"
      >
        ← Back to studio
      </button>

      <h1 className="font-display text-2xl font-semibold text-ink">Create a new course</h1>
      <p className="mt-1 text-sm text-slate">Fill in the details below — you can edit everything later.</p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-5">
        <Field label="Course title *" error={errors.title}>
          <input
            className={inputCls}
            placeholder="e.g. Introduction to Machine Learning"
            {...register("title", { required: "Title is required", minLength: { value: 3, message: "At least 3 characters" } })}
          />
        </Field>

        <Field label="Description *" error={errors.description}>
          <textarea
            rows={4}
            className={inputCls}
            placeholder="What will students learn? What should they know beforehand?"
            {...register("description", { required: "Description is required", minLength: { value: 10, message: "At least 10 characters" } })}
          />
        </Field>

        <Field label="Skill / Category *" error={errors.skill_id}>
          <select
            className={inputCls}
            {...register("skill_id", { required: "Please select a skill" })}
          >
            <option value="">— Select a skill —</option>
            {skills.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
          {skills.length === 0 && (
            <p className="mt-1 text-xs text-slate">
              No skills found.{" "}
              <a href="/admin" className="underline text-trail">Ask an admin to add skills first.</a>
            </p>
          )}
        </Field>

        <div className="grid grid-cols-2 gap-4">
          <Field label="Difficulty" error={errors.difficulty}>
            <select className={inputCls} {...register("difficulty")}>
              {DIFFICULTIES.map((d) => (
                <option key={d.value} value={d.value}>{d.label}</option>
              ))}
            </select>
          </Field>

          <Field label="Estimated hours" error={errors.estimated_hours}>
            <input
              type="number"
              min="0"
              step="0.5"
              className={inputCls}
              {...register("estimated_hours", { min: { value: 0, message: "Must be 0 or more" } })}
            />
          </Field>
        </div>

        <Field label="Thumbnail URL (optional)" error={errors.thumbnail_url}>
          <input
            className={inputCls}
            placeholder="https://example.com/image.jpg"
            {...register("thumbnail_url")}
          />
        </Field>

        <div className="pt-2 flex gap-3">
          <button
            type="submit"
            disabled={submitting}
            className="rounded-lg bg-trail px-6 py-2.5 text-sm font-medium text-white hover:bg-trail/90 disabled:opacity-50"
          >
            {submitting ? "Creating…" : "Create course"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/instructor")}
            className="rounded-lg border border-mist px-6 py-2.5 text-sm font-medium text-slate hover:text-ink"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
