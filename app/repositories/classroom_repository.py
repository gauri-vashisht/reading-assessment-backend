from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.classroom import Classroom
from app.repositories.base_repository import BaseRepository


class ClassroomRepository(BaseRepository[Classroom]):

    def __init__(self):
        super().__init__(Classroom)

    def get_duplicate(
        self,
        db: Session,
        academic_year_id,
        grade,
        section,
    ):
        stmt = select(Classroom).where(
            Classroom.academic_year_id == academic_year_id,
            Classroom.grade == grade,
            Classroom.section == section,
        )

        return db.scalar(stmt)

    def get_all(
        self,
        db: Session,
        is_active: bool | None = None,
    ):
        stmt = select(Classroom)

        if is_active is not None:
            stmt = stmt.where(
                Classroom.is_active == is_active
            )

        stmt = stmt.order_by(
            Classroom.grade,
            Classroom.section,
        )

        return db.scalars(stmt).all()

    def update(
        self,
        db: Session,
        classroom: Classroom,
        data: dict,
    ):

        for key, value in data.items():
            setattr(classroom, key, value)

        db.flush()
        db.refresh(classroom)

        return classroom


classroom_repository = ClassroomRepository()