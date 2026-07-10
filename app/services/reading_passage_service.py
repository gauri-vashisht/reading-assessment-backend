from uuid import UUID

from sqlalchemy.orm import Session

from app.models.reading_passage import ReadingPassage
from app.models.user import User
from app.repositories.reading_passage_repository import ReadingPassageRepository
from app.schemas.reading_passage import (
    ReadingPassageCreate,
    ReadingPassageUpdate,
)


class ReadingPassageService:

    def __init__(self, db: Session):
        self.repository = ReadingPassageRepository(db)

    def create(
        self,
        data: ReadingPassageCreate,
        current_user: User,
    ):
        passage = ReadingPassage(
            **data.model_dump(),
            created_by=current_user.id,
        )

        return self.repository.create(passage)

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, passage_id: UUID):
        return self.repository.get_by_id(passage_id)

    def update(
        self,
        passage_id: UUID,
        data: ReadingPassageUpdate,
    ):
        passage = self.repository.get_by_id(passage_id)

        if not passage:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(passage, key, value)

        return self.repository.update(passage)

    def delete(self, passage_id: UUID):
        passage = self.repository.get_by_id(passage_id)

        if not passage:
            return False

        self.repository.delete(passage)
        return True