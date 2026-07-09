"""
Skill CRUD — the top of the learning-path hierarchy.
"""
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user, require_roles
from app.db.mongodb import get_db
from app.models.common import utcnow
from app.models.learning import SkillCreate, SkillInDB
from app.models.user import UserInDB, UserRole
from app.utils.slug import slugify

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.post("", response_model=SkillInDB, status_code=status.HTTP_201_CREATED)
async def create_skill(
    payload: SkillCreate,
    current_user: UserInDB = Depends(require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)),
):
    db = get_db()
    doc = payload.model_dump()
    doc.update({"slug": slugify(payload.name), "created_by": current_user.id, "created_at": utcnow()})
    result = await db.skills.insert_one(doc)
    doc["_id"] = result.inserted_id
    return SkillInDB(**doc)


@router.get("", response_model=list[SkillInDB])
async def list_skills(category: str | None = None):
    db = get_db()
    query = {"category": category} if category else {}
    docs = await db.skills.find(query).to_list(200)
    return [SkillInDB(**d) for d in docs]


@router.get("/{skill_id}", response_model=SkillInDB)
async def get_skill(skill_id: str):
    db = get_db()
    doc = await db.skills.find_one({"_id": ObjectId(skill_id)})
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found")
    return SkillInDB(**doc)


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: str,
    current_user: UserInDB = Depends(require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)),
):
    db = get_db()
    await db.skills.delete_one({"_id": ObjectId(skill_id)})
