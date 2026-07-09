"""
Aggregated analytics for student and instructor dashboards.
Uses MongoDB aggregation pipelines rather than pulling raw docs into Python.
"""
from bson import ObjectId
from fastapi import APIRouter, Depends

from app.core.deps import get_current_user, require_roles
from app.db.mongodb import get_db
from app.models.user import UserInDB, UserRole

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/student/summary")
async def student_summary(current_user: UserInDB = Depends(get_current_user)):
    db = get_db()
    progress_docs = await db.progress.find({"student_id": current_user.id}).to_list(200)
    daily = await db.daily_activity.find({"student_id": current_user.id}).sort("date", -1).to_list(30)

    active_courses = sum(1 for p in progress_docs if p.get("status") == "in_progress")
    completed_courses = sum(1 for p in progress_docs if p.get("status") == "completed")
    total_time = sum(p.get("total_time_spent_seconds", 0) for p in progress_docs)

    return {
        "xp_points": current_user.xp_points,
        "level": current_user.level,
        "current_streak": current_user.current_streak,
        "longest_streak": current_user.longest_streak,
        "active_courses": active_courses,
        "completed_courses": completed_courses,
        "total_time_spent_seconds": total_time,
        "daily_activity": [
            {"date": d["date"], "reading_seconds": d.get("reading_seconds", 0),
             "video_seconds": d.get("video_seconds", 0), "xp_earned": d.get("xp_earned", 0)}
            for d in daily
        ],
    }


@router.get("/instructor/summary")
async def instructor_summary(
    current_user: UserInDB = Depends(require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)),
):
    db = get_db()
    courses = await db.courses.find({"instructor_id": current_user.id}).to_list(200)
    course_ids = [c["_id"].__str__() for c in courses]

    total_students = 0
    completion_rates = []
    for c in courses:
        progresses = await db.progress.find({"course_id": str(c["_id"])}).to_list(1000)
        total_students += len(progresses)
        if progresses:
            avg_pct = sum(p.get("completion_percentage", 0) for p in progresses) / len(progresses)
            completion_rates.append({"course_id": str(c["_id"]), "course_title": c["title"], "avg_completion": round(avg_pct, 1)})

    return {
        "total_courses": len(courses),
        "total_students": total_students,
        "completion_by_course": completion_rates,
    }


@router.get("/admin/platform")
async def platform_summary(current_user: UserInDB = Depends(require_roles(UserRole.SUPER_ADMIN))):
    db = get_db()
    return {
        "total_users": await db.users.count_documents({}),
        "total_students": await db.users.count_documents({"role": "student"}),
        "total_instructors": await db.users.count_documents({"role": "instructor"}),
        "pending_instructor_approvals": await db.users.count_documents({"status": "pending_approval"}),
        "total_courses": await db.courses.count_documents({}),
        "total_certificates_issued": await db.certificates.count_documents({}),
    }
