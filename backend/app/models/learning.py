"""
Learning-path hierarchy: Skill -> Course -> Module -> Lesson -> Resource,
plus Quiz and Assignment models.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.models.common import MongoBaseModel, utcnow


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ResourceType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    VIDEO = "video"
    LINK = "link"
    PAPER = "paper"


# ---------- Skill ----------
class SkillInDB(MongoBaseModel):
    name: str
    slug: str
    description: str
    icon: str | None = None
    category: str | None = None
    created_by: str  # instructor/user id
    created_at: datetime = Field(default_factory=utcnow)


class SkillCreate(BaseModel):
    name: str
    description: str
    icon: str | None = None
    category: str | None = None


# ---------- Course ----------
class CourseInDB(MongoBaseModel):
    title: str
    slug: str
    description: str
    skill_id: str
    instructor_id: str
    thumbnail_url: str | None = None
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    estimated_hours: float = 0
    is_published: bool = False
    enrolled_count: int = 0
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class CourseCreate(BaseModel):
    title: str
    description: str
    skill_id: str
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    estimated_hours: float = 0
    thumbnail_url: str | None = None


# ---------- Module ----------
class ModuleInDB(MongoBaseModel):
    course_id: str
    title: str
    order: int
    learning_objectives: list[str] = Field(default_factory=list)
    estimated_minutes: int = 0
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    created_at: datetime = Field(default_factory=utcnow)


class ModuleCreate(BaseModel):
    title: str
    order: int
    learning_objectives: list[str] = Field(default_factory=list)
    estimated_minutes: int = 0
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER


# ---------- Lesson ----------
class LessonInDB(MongoBaseModel):
    module_id: str
    title: str
    order: int
    created_at: datetime = Field(default_factory=utcnow)


class LessonCreate(BaseModel):
    title: str
    order: int


# ---------- Resource ----------
class ResourceInDB(MongoBaseModel):
    lesson_id: str
    type: ResourceType
    title: str
    url: str  # Cloudinary URL or local storage path, or external link
    duration_seconds: int | None = None  # for video
    page_count: int | None = None  # for pdf/docx
    created_at: datetime = Field(default_factory=utcnow)


class ResourceCreate(BaseModel):
    type: ResourceType
    title: str
    url: str
    duration_seconds: int | None = None
    page_count: int | None = None


# ---------- Quiz ----------
class QuestionType(str, Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"


class QuizQuestion(BaseModel):
    question: str
    type: QuestionType
    options: list[str] = Field(default_factory=list)  # for MCQ
    correct_answer: str
    points: int = 1


class QuizInDB(MongoBaseModel):
    module_id: str
    title: str
    time_limit_minutes: int = 10
    questions: list[QuizQuestion] = Field(default_factory=list)
    generated_by_ai: bool = False
    created_at: datetime = Field(default_factory=utcnow)


class QuizCreate(BaseModel):
    title: str
    time_limit_minutes: int = 10
    questions: list[QuizQuestion]


class QuizSubmission(BaseModel):
    answers: list[str]  # index-aligned with quiz.questions


# ---------- Assignment ----------
class AssignmentInDB(MongoBaseModel):
    module_id: str
    title: str
    instructions: str
    deadline: datetime | None = None
    max_points: int = 100
    created_at: datetime = Field(default_factory=utcnow)


class AssignmentCreate(BaseModel):
    title: str
    instructions: str
    deadline: datetime | None = None
    max_points: int = 100


class AssignmentSubmissionInDB(MongoBaseModel):
    assignment_id: str
    student_id: str
    file_url: str
    submitted_at: datetime = Field(default_factory=utcnow)
    grade: float | None = None
    feedback: str | None = None
