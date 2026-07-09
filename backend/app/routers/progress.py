"""
Progress tracking: course progress, reading analytics, video analytics,
quiz attempts, and the gamification side-effects (XP + streaks) they trigger.
"""
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.db.mongodb import get_db
from app.models.common import utcnow
from app.models.progress import (
    DailyActivityInDB, ProgressInDB, ReadingProgressInDB, VideoProgressInDB,
)
from app.models.user import UserInDB
from app.services.gamification import award_xp, bump_streak

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/course/{course_id}", response_model=ProgressInDB)
async def get_course_progress(course_id: str, current_user: UserInDB = Depends(get_current_user)):
    db = get_db()
    doc = await db.progress.find_one({"student_id": current_user.id, "course_id": course_id})
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not enrolled in this course")
    return ProgressInDB(**doc)


@router.post("/course/{course_id}/complete-module/{module_id}", response_model=ProgressInDB)
async def complete_module(course_id: str, module_id: str, current_user: UserInDB = Depends(get_current_user)):
    db = get_db()
    progress_doc = await db.progress.find_one({"student_id": current_user.id, "course_id": course_id})
    if not progress_doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not enrolled in this course")

    completed = set(progress_doc.get("completed_modules", []))
    completed.add(module_id)
    total_modules = await db.modules.count_documents({"course_id": course_id})
    pct = round(len(completed) / total_modules * 100, 2) if total_modules else 0.0

    update = {
        "completed_modules": list(completed),
        "completion_percentage": pct,
        "last_accessed_at": utcnow(),
        "status": "completed" if pct >= 100 else "in_progress",
    }
    if pct >= 100:
        update["completed_at"] = utcnow()

    await db.progress.update_one({"_id": progress_doc["_id"]}, {"$set": update})
    await award_xp(db, current_user.id, 50, reason="module_completed")
    await bump_streak(db, current_user.id)

    doc = await db.progress.find_one({"_id": progress_doc["_id"]})
    return ProgressInDB(**doc)


@router.put("/reading/{resource_id}", response_model=ReadingProgressInDB)
async def update_reading_progress(
    resource_id: str,
    last_page: int,
    total_pages: int,
    seconds_spent: int,
    current_user: UserInDB = Depends(get_current_user),
):
    db = get_db()
    pct = round(last_page / total_pages * 100, 2) if total_pages else 0.0
    result = await db.reading_progress.find_one_and_update(
        {"student_id": current_user.id, "resource_id": resource_id},
        {
            "$set": {
                "last_page": last_page, "total_pages": total_pages,
                "completion_percentage": pct, "updated_at": utcnow(),
            },
            "$inc": {"reading_time_seconds": seconds_spent},
            "$setOnInsert": {"student_id": current_user.id, "resource_id": resource_id, "bookmarks": [], "notes": []},
        },
        upsert=True,
        return_document=True,
    )
    await bump_streak(db, current_user.id)
    return ReadingProgressInDB(**result)


@router.put("/video/{resource_id}", response_model=VideoProgressInDB)
async def update_video_progress(
    resource_id: str,
    watched_seconds: int,
    total_seconds: int,
    last_position_seconds: int,
    playback_speed: float = 1.0,
    current_user: UserInDB = Depends(get_current_user),
):
    db = get_db()
    pct = round(watched_seconds / total_seconds * 100, 2) if total_seconds else 0.0
    result = await db.video_progress.find_one_and_update(
        {"student_id": current_user.id, "resource_id": resource_id},
        {
            "$set": {
                "watched_seconds": watched_seconds, "total_seconds": total_seconds,
                "last_position_seconds": last_position_seconds, "playback_speed": playback_speed,
                "completion_percentage": pct, "updated_at": utcnow(),
            },
            "$setOnInsert": {"student_id": current_user.id, "resource_id": resource_id},
        },
        upsert=True,
        return_document=True,
    )
    await bump_streak(db, current_user.id)
    return VideoProgressInDB(**result)
