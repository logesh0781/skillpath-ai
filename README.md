# SkillPath AI — Intelligent Learning Path Dashboard

A working full-stack foundation for the SIH "Learning Path Dashboard" brief:
React + Vite + Tailwind frontend, FastAPI + MongoDB backend, JWT auth with
role-based access (student / instructor / super admin), gamification (XP,
levels, streaks), progress/reading/video analytics, and an AI layer wired for
Google Gemini (roadmap generator, tutor, quiz generator, notes generator,
skill-gap analysis) with a mock fallback so the app runs with zero API keys.

## What's actually built and running

- **Auth**: register, login, JWT access+refresh tokens, forgot/reset password,
  role-based route protection (backend dependencies + frontend guards).
- **Learning hierarchy**: Skill → Course → Module → Lesson → Resource, full CRUD.
- **Enrollment & progress**: enroll, mark modules complete, reading/video progress
  tracking with percentages, time spent, bookmarks.
- **Gamification**: XP awarding, level curve, daily streak logic with day-gap detection.
- **Analytics endpoints**: student summary, instructor summary, admin platform summary
  — all real MongoDB aggregations, feeding real Chart.js charts on the frontend.
- **AI endpoints**: `/ai/roadmap`, `/ai/tutor`, `/ai/generate-quiz`, `/ai/generate-notes`,
  `/ai/skill-gap-analysis` — call Gemini if `GEMINI_API_KEY` is set, otherwise return a
  clearly-labeled mock response so nothing breaks in a fresh clone.
- **Frontend**: landing page, course explorer, login/register, student/instructor/admin
  dashboards with live charts, a signature "waypoint trail" progress component,
  a distinct visual identity (not the default AI-generated look) themed around trails/maps.

## What's scaffolded but intentionally left for you to extend

The original brief is genuinely enormous — quiz-taking UI with timers, assignment
submission + grading UI, certificate PDF+QR generation, notifications (in-app + email),
leaderboards/badges UI, search, dark mode toggle, and the AI Tutor chat UI are either
partially modeled (backend schemas exist in `app/models/`) or not yet started. Building
all of it to genuine production quality is realistically weeks of work, not one response.
The architecture below is deliberately built so each of those is a natural extension —
add a router in `backend/app/routers/`, a page in `frontend/src/pages/`.

## Run it locally

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                # then edit .env (Mongo URI, JWT secret, Gemini key)
uvicorn app.main:app --reload                       # http://localhost:8000, docs at /docs
```
You need a MongoDB instance — either local (`mongodb://localhost:27017`) or a free
MongoDB Atlas cluster; just update `MONGO_URI` in `.env`.

### Frontend
```bash
cd frontend
npm install
npm run dev                                          # http://localhost:5173
```
The Vite dev server proxies `/api` to `http://localhost:8000`, so no CORS config is
needed locally.

## 🚀 Visit the Website

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge)](https://skillpath-aizip--logesh0781.replit.app)

## Project structure
```
backend/app/
  core/       config, security (JWT/bcrypt), route-protection dependencies
  db/         MongoDB connection + indexes
  models/     Pydantic schemas (user, learning hierarchy, progress/analytics)
  routers/    auth, users, skills, courses, progress, analytics, ai
  services/   gamification (XP/streaks), AI provider abstraction (Gemini/mock)

frontend/src/
  api/        Axios client with auto token-refresh
  context/    AuthContext (login/register/logout, persisted session)
  components/ Navbar, ProtectedRoute, WaypointProgress (signature UI element)
  pages/      Landing, Courses, auth/, student/, instructor/, admin/
```

## Suggested build order for what's left
1. Quiz-taking UI (timer, MCQ/true-false/short-answer, auto-score) → pairs with the
   existing `QuizInDB`/`QuizAttemptInDB` models; needs a `quizzes` router.
2. Assignment submission + grading UI → `AssignmentSubmissionInDB` model exists.
3. Certificate generation (PDF + QR via `reportlab`/`qrcode`, already in requirements.txt).
4. Notifications (in-app list + email via SMTP settings already in `.env.example`).
5. AI Tutor chat UI + AI Notes/Quiz generator UI, calling the existing `/ai/*` endpoints.
6. Leaderboards, badges, dark mode toggle, global search.

Tell me which of these to build next and I'll continue directly on this codebase.
