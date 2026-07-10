from uuid import UUID

from sqlalchemy.orm import Session

from app.models.reading_passage import ReadingPassage


class ReadingPassageRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, passage: ReadingPassage):
        self.db.add(passage)
        self.db.commit()
        self.db.refresh(passage)
        return passage

    def get_all(self):
        return (
            self.db.query(ReadingPassage)
            .order_by(ReadingPassage.created_at.desc())
            .all()
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