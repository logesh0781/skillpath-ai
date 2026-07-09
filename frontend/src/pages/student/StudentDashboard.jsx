import { useEffect, useState } from "react";
import { Line, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement,
  ArcElement, Tooltip, Legend, Filler,
} from "chart.js";
import client from "../../api/client";
import { useAuth } from "../../context/AuthContext";
import WaypointProgress from "../../components/WaypointProgress";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Tooltip, Legend, Filler);

const demoSteps = [
  { id: "1", title: "Intro" }, { id: "2", title: "Setup" }, { id: "3", title: "Core skill" },
  { id: "4", title: "Project" }, { id: "5", title: "Advanced" }, { id: "6", title: "Capstone" },
];

export default function StudentDashboard() {
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    client.get("/analytics/student/summary")
      .then(({ data }) => setSummary(data))
      .catch(() => setError("Couldn't reach the API yet — start the backend to see live data."));
  }, []);

  const daily = summary?.daily_activity ?? [];
  const lineData = {
    labels: daily.map((d) => d.date).reverse(),
    datasets: [
      {
        label: "Reading (min)",
        data: daily.map((d) => Math.round(d.reading_seconds / 60)).reverse(),
        borderColor: "#2F6F5E",
        backgroundColor: "rgba(47,111,94,0.15)",
        fill: true,
        tension: 0.3,
      },
      {
        label: "Video (min)",
        data: daily.map((d) => Math.round(d.video_seconds / 60)).reverse(),
        borderColor: "#E0A845",
        backgroundColor: "rgba(224,168,69,0.15)",
        fill: true,
        tension: 0.3,
      },
    ],
  };

  const doughnutData = {
    labels: ["Completed", "Active", "Not started"],
    datasets: [{
      data: [summary?.completed_courses ?? 0, summary?.active_courses ?? 0, 1],
      backgroundColor: ["#2F6F5E", "#E0A845", "#DDE3E0"],
      borderWidth: 0,
    }],
  };

  return (
    <div className="mx-auto max-w-6xl px-6 py-8">
      <h1 className="font-display text-2xl font-semibold text-ink">Welcome back, {user?.name?.split(" ")[0]}</h1>
      <p className="text-sm text-slate">Here's how your path is going.</p>
      {error && <p className="mt-4 rounded-lg bg-summit/10 px-4 py-2 text-sm text-summit">{error}</p>}

      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        {[
          { label: "XP points", value: summary?.xp_points ?? user?.xp_points ?? 0, color: "text-waypoint" },
          { label: "Level", value: summary?.level ?? user?.level ?? 1, color: "text-trail" },
          { label: "Day streak", value: summary?.current_streak ?? user?.current_streak ?? 0, color: "text-summit" },
          { label: "Active courses", value: summary?.active_courses ?? 0, color: "text-ink" },
        ].map((s) => (
          <div key={s.label} className="rounded-xl border border-mist bg-white p-4">
            <p className="text-xs font-mono uppercase text-slate">{s.label}</p>
            <p className={`mt-1 font-display text-3xl font-semibold ${s.color}`}>{s.value}</p>
          </div>
        ))}
      </div>

      <div className="mt-8 rounded-xl border border-mist bg-white p-5">
        <h2 className="font-display text-lg font-semibold text-ink">Current course path</h2>
        <WaypointProgress steps={demoSteps} currentIndex={2} />
      </div>

      <div className="mt-6 grid gap-6 md:grid-cols-3">
        <div className="rounded-xl border border-mist bg-white p-5 md:col-span-2">
          <h2 className="font-display text-lg font-semibold text-ink">Reading & video time (last 30 days)</h2>
          <div className="mt-4 h-64">
            <Line data={lineData} options={{ maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }} />
          </div>
        </div>
        <div className="rounded-xl border border-mist bg-white p-5">
          <h2 className="font-display text-lg font-semibold text-ink">Courses</h2>
          <div className="mt-4 h-64">
            <Doughnut data={doughnutData} options={{ maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }} />
          </div>
        </div>
      </div>
    </div>
  );
}
