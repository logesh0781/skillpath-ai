import { useEffect, useState } from "react";
import client from "../api/client";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    client.get("/courses")
      .then(({ data }) => setCourses(data))
      .catch(() => setError("Couldn't reach the API yet — start the backend to browse real courses."));
  }, []);

  return (
    <div className="mx-auto max-w-6xl px-6 py-8">
      <h1 className="font-display text-2xl font-semibold text-ink">Explore learning paths</h1>
      {error && <p className="mt-4 rounded-lg bg-summit/10 px-4 py-2 text-sm text-summit">{error}</p>}

      {courses.length === 0 && !error && (
        <p className="mt-6 text-sm text-slate">No published courses yet — instructors can create one from their studio.</p>
      )}

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {courses.map((c) => (
          <div key={c.id} className="rounded-xl border border-mist bg-white p-5 hover:border-trail">
            <span className="font-mono text-[10px] uppercase text-trail">{c.difficulty}</span>
            <h3 className="mt-1 font-display text-lg font-semibold text-ink">{c.title}</h3>
            <p className="mt-1 text-sm text-slate line-clamp-2">{c.description}</p>
            <p className="mt-3 text-xs text-slate">{c.enrolled_count} enrolled · {c.estimated_hours}h</p>
          </div>
        ))}
      </div>
    </div>
  );
}
