"""
User models: DB document shape + request/response schemas.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field

from app.models.common import MongoBaseModel, utcnow


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"


class UserStatus(str, Enum):
    ACTIVE = "active"
    PENDING_APPROVAL = "pending_approval"  # instructors awaiting super-admin approval
    SUSPENDED = "suspended"


class UserInDB(MongoBaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    role: UserRole = UserRole.STUDENT
    status: UserStatus = UserStatus.ACTIVE
    avatar_url: str | None = None
    bio: str | None = None

    # Gamification
    xp_points: int = 0
    level: int = 1
    current_streak: int = 0
    longest_streak: int = 0
    last_active_date: datetime | None = None
    badges: list[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.STUDENT  # instructors get PENDING_APPROVAL status server-side


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole
    status: UserStatus
    avatar_url: str | None = None
    xp_points: int
    level: int
    current_streak: int
    badges: list[str]


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic
