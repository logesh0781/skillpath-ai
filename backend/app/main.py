"""
SkillPath AI — FastAPI application entrypoint.
Run with:  uvicorn app.main:app --reload
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo
from app.routers import ai, analytics, auth, courses, progress, skills, users

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger("skillpath")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Connecting to MongoDB at %s ...", settings.MONGO_URI)
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/", tags=["Health"])
async def root():
    return {"service": settings.APP_NAME, "status": "ok"}


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
