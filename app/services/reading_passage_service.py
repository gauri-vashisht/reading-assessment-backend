from uuid import UUID

from sqlalchemy.orm import Session

from app.models.reading_passage import ReadingPassage
from app.schemas.reading_passage import ReadingPassageSummaryResponse, ReadingPassageResponse
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
        passage_data = data.model_dump()

        passage_data["word_count"] = len(
            passage_data["passage"].split()
        )

        passage = ReadingPassage(
            **passage_data,
            created_by=current_user.id,
        )

        return self.repository.create(passage)

    def get_all(self, is_active: bool | None = None, summary: bool = False, ):
        passages = self.repository.get_all(
            is_active=is_active
        )

        if summary:
            return [
                ReadingPassageSummaryResponse.model_validate(
                    passage
                )
                for passage in passages
            ]

        return [
            ReadingPassageResponse.model_validate(
                passage
            )
            for passage in passages
        ]

    def get_by_id(self, passage_id: UUID):
        passage = self.repository.get_by_id(passage_id)

        if not passage:
            return None

        return ReadingPassageResponse.model_validate(passage)

    def update(
        self,
        passage_id: UUID,
        data: ReadingPassageUpdate,
    ):
        passage = self.repository.get_by_id(passage_id)

        if not passage:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "passage" in update_data:
            update_data["word_count"] = len(
                update_data["passage"].split()
        )

        for key, value in update_data.items():
            setattr(passage, key, value)

        return self.repository.update(passage)

    def delete(self, passage_id: UUID):
        passage = self.repository.get_by_id(passage_id)

        if not passage:
            return False

        self.repository.delete(passage)
        return True