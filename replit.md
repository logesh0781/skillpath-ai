# SkillPath AI

AI-powered Learning Path Dashboard — Smart India Hackathon project.

## Stack
- **Frontend**: React 18 + Vite + Tailwind CSS v3 (port 5000 in dev)
- **Backend**: FastAPI + Motor (async MongoDB) + JWT auth (port 8000 in dev)
- **Database**: MongoDB Atlas
- **AI**: Google Gemini (with mock fallback if no API key)

## Running the project

Two workflows must both be running:
- **Backend** — `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- **Start application** — `cd frontend && npm run dev` (proxies `/api` → port 8000)

## Required secrets (Replit Secrets)
| Key | Description |
|-----|-------------|
| `MONGO_URI` | MongoDB Atlas connection string |
| `JWT_SECRET_KEY` | Any long random string for JWT signing |

Optional: `GEMINI_API_KEY` for real AI responses (app uses mock fallback without it).

## Deployment
- **Target**: autoscale
- **Build**: `cd frontend && npm run build`
- **Run**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 5000`
- The FastAPI backend serves the built React frontend as static files in production.
- MongoDB Atlas Network Access must include `0.0.0.0/0` so Replit servers can connect.

## Project structure
```
backend/app/
  core/       config, security (JWT/bcrypt)
  db/         MongoDB connection (certifi used for Atlas SSL)
  models/     Pydantic schemas
  routers/    auth, users, skills, courses, progress, analytics, ai
  services/   gamification, AI provider (Gemini/mock)

frontend/src/
  api/        Axios client with auto token-refresh
  context/    AuthContext
  components/ Navbar, ProtectedRoute, WaypointProgress
  pages/      Landing, Courses, auth/, student/, instructor/, admin/
```

## User preferences
- Keep existing project structure — do not restructure or migrate
