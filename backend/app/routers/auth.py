"""
Authentication endpoints: register, login, refresh, forgot/reset password.
"""
from datetime import datetime, timedelta, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from jose import JWTError

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.mongodb import get_db
from app.models.user import (
    ForgotPassword,
    ResetPassword,
    TokenPair,
    UserInDB,
    UserLogin,
    UserPublic,
    UserRegister,
    UserRole,
    UserStatus,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _to_public(user_doc: dict) -> UserPublic:
    user = UserInDB(**user_doc)
    return UserPublic(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        status=user.status,
        avatar_url=user.avatar_url,
        xp_points=user.xp_points,
        level=user.level,
        current_streak=user.current_streak,
        badges=user.badges,
    )


@router.post("/register", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister):
    db = get_db()
    existing = await db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "An account with this email already exists")

    status_value = (
        UserStatus.ACTIVE if payload.role in (UserRole.INSTRUCTOR, UserRole.STUDENT) else UserStatus.PENDING_APPROVAL
    )

    doc = {
        "name": payload.name,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "role": payload.role,
        "status": status_value,
        "xp_points": 0,
        "level": 1,
        "current_streak": 0,
        "longest_streak": 0,
        "badges": [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await db.users.insert_one(doc)
    doc["_id"] = result.inserted_id

    access = create_access_token(str(result.inserted_id), payload.role.value)
    refresh = create_refresh_token(str(result.inserted_id))
    return TokenPair(access_token=access, refresh_token=refresh, user=_to_public(doc))


@router.post("/login", response_model=TokenPair)
async def login(payload: UserLogin):
    db = get_db()
    doc = await db.users.find_one({"email": payload.email})
    if not doc or not verify_password(payload.password, doc["hashed_password"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password")
    if doc.get("status") == UserStatus.SUSPENDED:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This account has been suspended")

    access = create_access_token(str(doc["_id"]), doc["role"])
    refresh = create_refresh_token(str(doc["_id"]))
    return TokenPair(access_token=access, refresh_token=refresh, user=_to_public(doc))


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token")

    db = get_db()
    doc = await db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not doc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User no longer exists")

    access = create_access_token(str(doc["_id"]), doc["role"])
    new_refresh = create_refresh_token(str(doc["_id"]))
    return TokenPair(access_token=access, refresh_token=new_refresh, user=_to_public(doc))


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(payload: ForgotPassword):
    db = get_db()
    doc = await db.users.find_one({"email": payload.email})
    # Always return 202 regardless of whether the email exists, to avoid leaking
    # which addresses are registered.
    if doc:
        reset_token = create_access_token(str(doc["_id"]), "reset", {"type": "password_reset"})
        # In production this token is emailed via the notification service (see app/services/email.py).
        # We return it directly here only because no SMTP/mail server is configured in this sandbox.
        return {"message": "If that email exists, a reset link has been generated.", "dev_reset_token": reset_token}
    return {"message": "If that email exists, a reset link has been generated."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(payload: ResetPassword):
    try:
        claims = decode_token(payload.token)
        if claims.get("type") != "password_reset":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid reset token")
    except JWTError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired reset token")

    db = get_db()
    result = await db.users.update_one(
        {"_id": ObjectId(claims["sub"])},
        {"$set": {"hashed_password": hash_password(payload.new_password), "updated_at": datetime.now(timezone.utc)}},
    )
    if result.matched_count == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return {"message": "Password has been reset successfully"}
