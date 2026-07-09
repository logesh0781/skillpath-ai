"""
Course, Module, Lesson, and Resource CRUD — nested under the learning-path hierarchy.
Also handles student enrollment.
"""
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user, require_roles
from app.db.mongodb import get_db
from app.models.common import utcnow
from app.models.learning import (
    CourseCreate, CourseInDB,
    LessonCreate, LessonInDB,
    ModuleCreate, ModuleInDB,
    ResourceCreate, ResourceInDB,
)
from app.models.progress import ProgressInDB
from app.models.user import UserInDB, UserRole
from app.utils.slug import slugify

router = APIRouter(prefix="/courses", tags=["Courses"])


# ---------------- Courses ----------------
@router.post("", response_model=CourseInDB, status_code=status.HTTP_201_CREATED)
async def create_course(
    payload: CourseCreate,
    current_user: UserInDB = Depends(require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)),
):
    db = get_db()
    doc = payload.model_dump()
    doc.update({
        "slug": slugify(payload.title),
        "instructor_id": current_user.id,
        "is_published": False,
        "enrolled_count": 0,
        "created_at": utcnow(),
        "updated_at": utcnow(),
    })
    result = await db.courses.insert_one(doc)
    doc["_id"] = result.inserted_id
    return CourseInDB(**doc)


@router.get("", response_model=list[CourseInDB])
async def list_courses(skill_id: str | None = None, published_only: bool = True):
    db = get_db()
    query: dict = {}
    if skill_id:
        query["skill_id"] = skill_id
    if published_only:
        query["is_published"] = True
    docs = await db.courses.find(query).to_list(200)
    return [CourseInDB(**d) for d in docs]


@router.get("/{course_id}", response_model=CourseInDB)
async def get_course(course_id: str):
    db = get_db()
    doc = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")
    return CourseInDB(**doc)


@router.patch("/{course_id}/publish", response_model=CourseInDB)
async def publish_course(
    course_id: str,
    current_user: UserInDB = Depends(require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)),
):
    db = get_db()
    await db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"is_published": True, "updated_at": utcnow()}})
    doc = await db.courses.find_one({"_id": ObjectId(course_id)})
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")
    return CourseInDB(**doc)


@router.post("/{course_id}/enroll", response_model=ProgressInDB, status_code=status.HTTP_201_CREATED)
async def enroll_in_course(course_id: str, current_user: UserInDB = Depends(get_current_user)):
    db = get_db()
    existing = await db.progress.find_one({"student_id": current_user.id, "course_id": course_id})
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Already enrolled in this course")
    doc = ProgressInDB(student_id=current_user.id, course_id=course_id).model_dump(exclude={"id"})
    result = await db.progress.insert_one(doc)
    doc["_id"] = result.inserted_id
    await db.courses.update_one({"_id": ObjectId(course_id)}, {"$inc": {"enrolled_count": 1}})
    return ProgressInDB(**doc)


# ---------------- Modules ----------------
@router.post("/{course_id}/modules", response_model=ModuleInDB, status_code=status.HTTP_201_CREATED)
async def create_module(
    course_id: str,
    payload: ModuleCreate,
    current_user: UserInDB = Depends(require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)),
):
    db = get_db()
    doc = payload.model_dump()
    doc.update({"course_id": course_id, "created_at": utcnow()})
    result = await db.modules.insert_one(doc)
    doc["_id"] = result.inserted_id
    return ModuleInDB(**doc)


@router.get("/{course_id}/modules", response_model=list[ModuleInDB])
async def list_modules(course_id: str):
    db = get_db()
    docs = await db.modules.find({"course_id": course_id}).sort("order", 1).to_list(200)
    return [ModuleInDB(**d) for d in docs]


# ---------------- Lessons ----------------
@router.post("/modules/{module_id}/lessons", response_model=LessonInDB, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    module_id: str,
    payload: LessonCreate,
    current_user: UserInDB = Depends(require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)),
):
    db = get_db()
    doc = payload.model_dump()
    doc.update({"module_id": module_id, "created_at": utcnow()})
    result = await db.lessons.insert_one(doc)
    doc["_id"] = result.inserted_id
    return LessonInDB(**doc)


@router.get("/modules/{module_id}/lessons", response_model=list[LessonInDB])
async def list_lessons(module_id: str):
    db = get_db()
    docs = await db.lessons.find({"module_id": module_id}).sort("order", 1).to_list(200)
    return [LessonInDB(**d) for d in docs]


# ---------------- Resources ----------------
@router.post("/lessons/{lesson_id}/resources", response_model=ResourceInDB, status_code=status.HTTP_201_CREATED)
async def add_resource(
    lesson_id: str,
    payload: ResourceCreate,
    current_user: UserInDB = Depends(require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)),
):
    db = get_db()
    doc = payload.model_dump()
    doc.update({"lesson_id": lesson_id, "created_at": utcnow()})
    result = await db.resources.insert_one(doc)
    doc["_id"] = result.inserted_id
    return ResourceInDB(**doc)


@router.get("/lessons/{lesson_id}/resources", response_model=list[ResourceInDB])
async def list_resources(lesson_id: str):
    db = get_db()
    docs = await db.resources.find({"lesson_id": lesson_id}).to_list(200)
    return [ResourceInDB(**d) for d in docs]
