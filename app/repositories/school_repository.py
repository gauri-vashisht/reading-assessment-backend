from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.school import School
from app.repositories.base_repository import BaseRepository


class SchoolRepository(BaseRepository[School]):
    def __init__(self):
        super().__init__(School)

    def get_by_code(
        self,
        db: Session,
        code: str,
    ) -> School | None:
        stmt = select(School).where(
            School.code == code
        )
        return db.scalar(stmt)

    def get_by_name(
        self,
        db: Session,
        name: str,
    ) -> School | None:
        stmt = select(School).where(
            School.name == name
        )
        return db.scalar(stmt)

    def update(
        self,
        db: Session,
        school: School,
        data: dict,
    ) -> School:

        for key, value in data.items():
            setattr(school, key, value)

        db.flush()
        db.refresh(school)

        return school


school_repository = SchoolRepository()