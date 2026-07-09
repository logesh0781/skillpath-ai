import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Landing() {
  return (
    <div className="bg-map-texture">
      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="grid items-center gap-12 md:grid-cols-2">
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <span className="font-mono text-xs uppercase tracking-widest text-trail">Smart India Hackathon</span>
            <h1 className="mt-3 font-display text-5xl font-semibold leading-tight text-ink">
              Every skill is a trail. <span className="text-trail">We help you find your way.</span>
            </h1>
            <p className="mt-4 max-w-md text-slate">
              SkillPath AI turns scattered PDFs, slides, and videos into a structured route —
              with an AI tutor, auto-generated quizzes, and a dashboard that shows exactly how far you've come.
            </p>
            <div className="mt-8 flex gap-3">
              <Link to="/register" className="rounded-lg bg-trail px-6 py-3 font-medium text-parchment hover:bg-trailLight">
                Start your path
              </Link>
              <Link to="/courses" className="rounded-lg border border-mist px-6 py-3 font-medium text-ink hover:border-trail hover:text-trail">
                Explore courses
              </Link>
            </div>
          </motion.div>

          {/* Signature element: a hand-drawn trail connecting waypoints, echoing the product name */}
          <motion.svg viewBox="0 0 400 300" className="w-full" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2, duration: 0.6 }}>
            <path d="M30 250 C 90 250, 90 180, 150 170 S 230 90, 260 90 S 330 40, 370 40" fill="none" stroke="#2F6F5E" strokeWidth="3" strokeDasharray="8 8" />
            {[
              { x: 30, y: 250, label: "Basics" },
              { x: 150, y: 170, label: "Practice" },
              { x: 260, y: 90, label: "Project" },
              { x: 370, y: 40, label: "Mastery" },
            ].map((p, i) => (
              <g key={p.label}>
                <circle cx={p.x} cy={p.y} r="9" fill={i === 3 ? "#E0A845" : "#2F6F5E"} />
                <text x={p.x} y={p.y - 16} textAnchor="middle" fontSize="12" fontFamily="IBM Plex Mono, monospace" fill="#14192B">
                  {p.label}
                </text>
              </g>
            ))}
          </motion.svg>
        </div>
      </section>

      <section className="border-t border-mist bg-white/60 py-16">
        <div className="mx-auto grid max-w-6xl grid-cols-1 gap-8 px-6 md:grid-cols-3">
          {[
            { title: "AI roadmap generator", body: "Tell it your goal and available time — get a week-by-week plan." },
            { title: "AI tutor & auto quizzes", body: "Ask questions grounded in your course material; get quizzes generated from it." },
            { title: "Real progress, not vanity stats", body: "Reading time, watch time, streaks, and completion — tracked automatically." },
          ].map((f) => (
            <div key={f.title} className="rounded-xl border border-mist bg-parchment p-6">
              <h3 className="font-display text-lg font-semibold text-ink">{f.title}</h3>
              <p className="mt-2 text-sm text-slate">{f.body}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
