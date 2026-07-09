"""
User profile + super-admin user management endpoints.
"""
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user, require_roles
from app.db.mongodb import get_db
from app.models.user import UserInDB, UserPublic, UserRole, UserStatus

router = APIRouter(prefix="/users", tags=["Users"])


def _public(doc: dict) -> UserPublic:
    u = UserInDB(**doc)
    return UserPublic(
        id=u.id, name=u.name, email=u.email, role=u.role, status=u.status,
        avatar_url=u.avatar_url, xp_points=u.xp_points, level=u.level,
        current_streak=u.current_streak, badges=u.badges,
    )


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: UserInDB = Depends(get_current_user)):
    return _public(current_user.model_dump(by_alias=True))


@router.get("", response_model=list[UserPublic])
async def list_users(
    role: UserRole | None = None,
    current_user: UserInDB = Depends(require_roles(UserRole.SUPER_ADMIN)),
):
    db = get_db()
    query = {"role": role} if role else {}
    docs = await db.users.find(query).to_list(500)
    return [_public(d) for d in docs]


@router.patch("/{user_id}/approve", response_model=UserPublic)
async def approve_instructor(
    user_id: str, current_user: UserInDB = Depends(require_roles(UserRole.SUPER_ADMIN))
):
    db = get_db()
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"status": UserStatus.ACTIVE}})
    doc = await db.users.find_one({"_id": ObjectId(user_id)})
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return _public(doc)


@router.patch("/{user_id}/suspend", response_model=UserPublic)
async def suspend_user(
    user_id: str, current_user: UserInDB = Depends(require_roles(UserRole.SUPER_ADMIN))
):
    db = get_db()
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"status": UserStatus.SUSPENDED}})
    doc = await db.users.find_one({"_id": ObjectId(user_id)})
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return _public(doc)
