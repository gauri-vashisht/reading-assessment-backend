from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.services.auth_service import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):

    try:
        return auth_service.register(
            db,
            user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/login")
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):

    try:
        return auth_service.login(
            db,
            credentials,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )