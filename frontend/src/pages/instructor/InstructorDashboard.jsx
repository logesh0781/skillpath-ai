import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend,
} from "chart.js";
import client from "../../api/client";
import { useAuth } from "../../context/AuthContext";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function InstructorDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    client.get("/analytics/instructor/summary")
      .then(({ data }) => setSummary(data))
      .catch(() => setError("Couldn't reach the API yet — start the backend to see live data."));
  }, []);

  const courses = summary?.completion_by_course ?? [];
  const barData = {
    labels: courses.map((c) => c.course_title),
    datasets: [{
      label: "Avg. completion %",
      data: courses.map((c) => c.avg_completion),
      backgroundColor: "#2F6F5E",
      borderRadius: 6,
    }],
  };

  return (
    <div className="mx-auto max-w-6xl px-6 py-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold text-ink">Instructor studio</h1>
          <p className="text-sm text-slate">Welcome, {user?.name}. Here's how your courses are performing.</p>
        </div>
        <button
          onClick={() => navigate("/instructor/create-course")}
          className="rounded-lg bg-trail px-4 py-2 text-sm font-medium text-white hover:bg-trail/90"
        >
          + Create course
        </button>
      </div>
      {error && <p className="mt-4 rounded-lg bg-summit/10 px-4 py-2 text-sm text-summit">{error}</p>}

      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-3">
        {[
          { label: "Courses", value: summary?.total_courses ?? 0 },
          { label: "Total students", value: summary?.total_students ?? 0 },
          { label: "Avg. courses / student", value: summary && summary.total_courses ? (summary.total_students / summary.total_courses).toFixed(1) : "—" },
        ].map((s) => (
          <div key={s.label} className="rounded-xl border border-mist bg-white p-4">
            <p className="text-xs font-mono uppercase text-slate">{s.label}</p>
            <p className="mt-1 font-display text-3xl font-semibold text-trail">{s.value}</p>
          </div>
        ))}
      </div>

      <div className="mt-6 rounded-xl border border-mist bg-white p-5">
        <h2 className="font-display text-lg font-semibold text-ink">Completion by course</h2>
        <div className="mt-4 h-72">
          <Bar data={barData} options={{ maintainAspectRatio: false, scales: { y: { max: 100 } } }} />
        </div>
      </div>
    </div>
  );
}
