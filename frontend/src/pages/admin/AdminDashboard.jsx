import { useEffect, useState } from "react";
import client from "../../api/client";

export default function AdminDashboard() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    client.get("/analytics/admin/platform")
      .then(({ data }) => setSummary(data))
      .catch(() => setError("Couldn't reach the API yet — start the backend to see live data."));
  }, []);

  const cards = [
    { label: "Total users", value: summary?.total_users },
    { label: "Students", value: summary?.total_students },
    { label: "Instructors", value: summary?.total_instructors },
    { label: "Pending approvals", value: summary?.pending_instructor_approvals, accent: "text-summit" },
    { label: "Total courses", value: summary?.total_courses },
    { label: "Certificates issued", value: summary?.total_certificates_issued },
  ];

  return (
    <div className="mx-auto max-w-6xl px-6 py-8">
      <h1 className="font-display text-2xl font-semibold text-ink">Platform overview</h1>
      <p className="text-sm text-slate">Super admin — manage instructors, courses, and platform health.</p>
      {error && <p className="mt-4 rounded-lg bg-summit/10 px-4 py-2 text-sm text-summit">{error}</p>}

      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-3">
        {cards.map((c) => (
          <div key={c.label} className="rounded-xl border border-mist bg-white p-4">
            <p className="text-xs font-mono uppercase text-slate">{c.label}</p>
            <p className={`mt-1 font-display text-3xl font-semibold ${c.accent ?? "text-trail"}`}>{c.value ?? "—"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
