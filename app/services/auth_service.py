from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import (
    UserCreate,
    UserLogin,
)


class AuthService:

    def register(
        self,
        db: Session,
        user_data: UserCreate,
    ):

        existing = user_repository.get_by_email(
            db,
            user_data.email,
        )

        if existing:
            raise ValueError(
                "Email already exists."
            )

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
            role=user_data.role,
        )

        return user_repository.create(
            db,
            user,
        )

    def login(
        self,
        db: Session,
        credentials: UserLogin,
    ):

        user = user_repository.get_by_email(
            db,
            credentials.email,
        )

        if user is None:
            raise ValueError(
                "Invalid credentials."
            )

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid credentials."
            )

        token = create_access_token(
            subject=str(user.id),
            role=user.role.value,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }


auth_service = AuthService()