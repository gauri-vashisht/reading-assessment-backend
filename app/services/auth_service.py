from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.exceptions.auth import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.auth import LoginResponse
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
)


class AuthService:

    def register(
        self,
        db: Session,
        data: UserCreate,
    ) -> User:

        existing = user_repository.get_by_email(
            db,
            data.email,
        )

        if existing:
            raise UserAlreadyExistsException(
                "Email already registered."
            )

        user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=hash_password(data.password),
            role=data.role,
        )

        try:
            user = user_repository.create(
                db,
                user,
            )

            db.commit()
            db.refresh(user)

            return user

        except Exception:
            db.rollback()
            raise

    def login(
        self,
        db: Session,
        credentials: UserLogin,
    ) -> LoginResponse:

        user = user_repository.get_by_email(
            db,
            credentials.email,
        )

        if user is None:
            raise InvalidCredentialsException(
                "Invalid email or password."
            )

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsException(
                "Invalid email or password."
            )

        try:
            user_repository.update_last_login(
                db,
                user,
            )

            db.commit()

        except Exception:
            db.rollback()
            raise

        token = create_access_token(
            subject=str(user.id),
            role=user.role.value,
        )

        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )


auth_service = AuthService()