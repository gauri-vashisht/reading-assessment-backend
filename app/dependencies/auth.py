from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.dependencies.database import DBSession
from app.repositories.user_repository import user_repository

security = HTTPBearer()


def get_current_user(
    db: DBSession,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = user_repository.get_by_id(
        db,
        UUID(user_id),
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def require_teacher(user=Depends(get_current_user)):
    if user.role.value != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Teacher access required",
        )
    return user


def require_student(user=Depends(get_current_user)):
    if user.role.value != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access required",
        )
    return user


def require_admin(user=Depends(get_current_user)):
    if user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    return user