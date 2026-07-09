"""
XP, leveling, and streak logic shared across routers.
Level formula: level N requires N * 200 cumulative XP (simple, tunable curve).
"""
from datetime import datetime, timedelta, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


def _level_for_xp(xp: int) -> int:
    level = 1
    while xp >= level * 200:
        xp -= level * 200
        level += 1
    return level


async def award_xp(db: AsyncIOMotorDatabase, user_id: str, amount: int, reason: str) -> None:
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return
    new_xp = user.get("xp_points", 0) + amount
    new_level = _level_for_xp(new_xp)
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"xp_points": new_xp, "level": new_level}},
    )
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    await db.daily_activity.update_one(
        {"student_id": user_id, "date": today},
        {"$inc": {"xp_earned": amount}, "$setOnInsert": {"student_id": user_id, "date": today}},
        upsert=True,
    )


async def bump_streak(db: AsyncIOMotorDatabase, user_id: str) -> None:
    """Increment the daily streak once per calendar day; reset if a day was missed."""
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return
    now = datetime.now(timezone.utc)
    last_active = user.get("last_active_date")

    if last_active:
        last_date = last_active.date() if isinstance(last_active, datetime) else None
        days_gap = (now.date() - last_date).days if last_date else None
    else:
        days_gap = None

    if days_gap == 0:
        return  # already counted today
    elif days_gap == 1:
        new_streak = user.get("current_streak", 0) + 1
    else:
        new_streak = 1  # missed a day (or first activity ever) — restart

    longest = max(user.get("longest_streak", 0), new_streak)
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"current_streak": new_streak, "longest_streak": longest, "last_active_date": now}},
    )
