"""
MongoDB connection lifecycle (Motor async client) and collection accessors.
"""
import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    global _client, _db
    _client = AsyncIOMotorClient(settings.MONGO_URI, tlsCAFile=certifi.where())
    _db = _client[settings.MONGO_DB_NAME]
    # Indexes — created once on startup, safe to call repeatedly (idempotent)
    await _db.users.create_index("email", unique=True)
    await _db.skills.create_index("slug", unique=True)
    await _db.courses.create_index("slug", unique=True)
    await _db.certificates.create_index("certificate_id", unique=True)
    await _db.notifications.create_index([("user_id", 1), ("created_at", -1)])
    await _db.progress.create_index([("student_id", 1), ("course_id", 1)], unique=True)


async def close_mongo_connection() -> None:
    if _client:
        _client.close()


def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not initialized. Did the app startup event run?")
    return _db
