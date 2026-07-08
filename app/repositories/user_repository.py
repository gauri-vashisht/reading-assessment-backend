from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(
    BaseRepository[User]
):

    def __init__(self):

        super().__init__(User)

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:

        stmt = (
            select(User)
            .where(User.email == email)
        )

        return db.scalar(stmt)

    def update_last_login(
        self,
        db: Session,
        user: User,
    ) -> None:

        from datetime import datetime, UTC

        user.last_login = datetime.now(UTC)

        db.flush()


user_repository = UserRepository()