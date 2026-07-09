"""
SkillPath AI — FastAPI application entrypoint.
Run with:  uvicorn app.main:app --reload
"""
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo
from app.routers import ai, analytics, auth, courses, progress, skills, users

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger("skillpath")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Log only host/db — never the full URI which contains credentials
    from urllib.parse import urlparse
    _parsed = urlparse(settings.MONGO_URI)
    logger.info("Connecting to MongoDB at %s/%s ...", _parsed.hostname or "unknown", settings.MONGO_DB_NAME)
    await connect_to_mongo()
    logger.info("Startup complete.")
    yield
    await close_mongo_connection()
    logger.info("Shutdown complete.")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Learning Path Dashboard — API",
    version="1.0.0",
    lifespan=lifespan,
)

_extra = [o.strip() for o in settings.EXTRA_ALLOWED_ORIGINS.split(",") if o.strip()]
_origins = list(set(settings.ALLOWED_ORIGINS + _extra))

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}


PREFIX = settings.API_V1_PREFIX
app.include_router(auth.router, prefix=PREFIX)
app.include_router(users.router, prefix=PREFIX)
app.include_router(skills.router, prefix=PREFIX)
app.include_router(courses.router, prefix=PREFIX)
app.include_router(progress.router, prefix=PREFIX)
app.include_router(analytics.router, prefix=PREFIX)
app.include_router(ai.router, prefix=PREFIX)

# Serve built React frontend (production)
STATIC_DIR = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")

    @app.get("/", include_in_schema=False)
    async def serve_root():
        return FileResponse(str(STATIC_DIR / "index.html"))

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        file_path = STATIC_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(STATIC_DIR / "index.html"))
else:
    @app.get("/", tags=["Health"])
    async def root():
        return {"service": settings.APP_NAME, "status": "ok"}
