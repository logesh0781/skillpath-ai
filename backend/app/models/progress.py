"""
Progress tracking, reading/video analytics, certificates, notifications, notes.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.models.common import MongoBaseModel, utcnow


class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ProgressInDB(MongoBaseModel):
    student_id: str
    course_id: str
    completed_modules: list[str] = Field(default_factory=list)
    completed_lessons: list[str] = Field(default_factory=list)
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    completion_percentage: float = 0.0
    total_time_spent_seconds: int = 0
    last_accessed_at: datetime = Field(default_factory=utcnow)
    started_at: datetime = Field(default_factory=utcnow)
    completed_at: datetime | None = None


class ReadingProgressInDB(MongoBaseModel):
    student_id: str
    resource_id: str
    last_page: int = 0
    total_pages: int = 0
    reading_time_seconds: int = 0
    completion_percentage: float = 0.0
    bookmarks: list[int] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=utcnow)


class VideoProgressInDB(MongoBaseModel):
    student_id: str
    resource_id: str
    watched_seconds: int = 0
    total_seconds: int = 0
    last_position_seconds: int = 0
    playback_speed: float = 1.0
    completion_percentage: float = 0.0
    updated_at: datetime = Field(default_factory=utcnow)


class QuizAttemptInDB(MongoBaseModel):
    student_id: str
    quiz_id: str
    answers: list[str]
    score: float
    max_score: float
    time_taken_seconds: int
    submitted_at: datetime = Field(default_factory=utcnow)


class CertificateInDB(MongoBaseModel):
    student_id: str
    course_id: str
    certificate_id: str  # human-readable unique ID, e.g. SPA-2026-000123
    student_name: str
    course_title: str
    completion_date: datetime
    pdf_url: str
    qr_verification_url: str
    issued_at: datetime = Field(default_factory=utcnow)


class NotificationType(str, Enum):
    ASSIGNMENT_REMINDER = "assignment_reminder"
    LEARNING_REMINDER = "learning_reminder"
    CERTIFICATE_ISSUED = "certificate_issued"
    ANNOUNCEMENT = "announcement"
    GRADE_POSTED = "grade_posted"


class NotificationInDB(MongoBaseModel):
    user_id: str
    type: NotificationType
    title: str
    message: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=utcnow)


class DailyActivityInDB(MongoBaseModel):
    """One row per student per calendar day — powers streaks & activity heatmaps."""
    student_id: str
    date: str  # ISO date string, e.g. "2026-07-05"
    reading_seconds: int = 0
    video_seconds: int = 0
    quizzes_taken: int = 0
    xp_earned: int = 0
