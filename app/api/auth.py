from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.dependencies.database import DBSession
from app.models.user import User
from app.schemas.auth import LoginResponse
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: DBSession,
):

    try:

        created_user = auth_service.register(
            db,
            user,
        )

        return UserResponse.model_validate(created_user)

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    credentials: UserLogin,
    db: DBSession,
):

    try:

        return auth_service.login(
            db,
            credentials,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):

    return UserResponse.model_validate(current_user)