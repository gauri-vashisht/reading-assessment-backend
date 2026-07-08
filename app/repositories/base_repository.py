from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: type[ModelType]):
        self.model = model

    def create(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:

        db.add(obj)
        db.flush()
        db.refresh(obj)

        return obj

    def get_by_id(
        self,
        db: Session,
        id: UUID,
    ) -> ModelType | None:

        stmt = select(self.model).where(
            self.model.id == id
        )

        return db.scalar(stmt)

    def get_all(
        self,
        db: Session,
    ) -> list[ModelType]:

        stmt = select(self.model)

        return list(
            db.scalars(stmt)
        )

    def delete(
        self,
        db: Session,
        obj: ModelType,
    ) -> None:

        db.delete(obj)
        db.flush()