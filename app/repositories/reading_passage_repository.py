from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.reading_passage import ReadingPassage


class ReadingPassageRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, passage: ReadingPassage):
        self.db.add(passage)
        self.db.commit()
        self.db.refresh(passage)
        return passage

    def get_all(self, is_active: bool | None = None,):
        query = select(ReadingPassage)

        if is_active is not None:
            query = query.where(
                ReadingPassage.is_active == is_active
            )
        query = query.order_by(
            ReadingPassage.grade,
            ReadingPassage.title,
        )
        return (
            self.db.scalars(query).all()
        )

    def get_by_id(self, passage_id: UUID):
        return (
            self.db.query(ReadingPassage)
            .filter(ReadingPassage.id == passage_id)
            .first()
        )

    def update(self, passage: ReadingPassage):
        self.db.commit()
        self.db.refresh(passage)
        return passage

    def delete(self, passage: ReadingPassage):
        self.db.delete(passage)
        self.db.commit()