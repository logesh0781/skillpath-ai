"""
Reusable FastAPI dependencies: current-user resolution and role guards.
"""
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.security import decode_token
from app.db.mongodb import get_db
from app.models.user import UserInDB, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise credentials_exception
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = get_db()
    doc = await db.users.find_one({"_id": ObjectId(user_id)})
    if doc is None:
        raise credentials_exception
    return UserInDB(**doc)


def require_roles(*allowed_roles: UserRole):
    """Dependency factory: require_roles(UserRole.INSTRUCTOR, UserRole.SUPER_ADMIN)"""

    async def checker(user: UserInDB = Depends(get_current_user)) -> UserInDB:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return user

    return checker
