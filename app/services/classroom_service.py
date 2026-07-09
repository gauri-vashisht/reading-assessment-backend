from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.classroom import Classroom
from app.repositories.academic_year_repository import academic_year_repository
from app.repositories.classroom_repository import classroom_repository
from app.repositories.school_repository import school_repository
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate


class ClassroomService:

    def create_classroom(self, db: Session, data: ClassroomCreate):

        if not school_repository.get_by_id(db, data.school_id):
            raise HTTPException(404, "School not found.")

        if not academic_year_repository.get_by_id(db, data.academic_year_id):
            raise HTTPException(404, "Academic year not found.")

        duplicate = classroom_repository.get_duplicate(
            db,
            data.academic_year_id,
            data.grade,
            data.section,
        )

        if duplicate:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Classroom already exists.",
            )

        classroom = Classroom(**data.model_dump())

        return classroom_repository.create(db, classroom)

    def get_classrooms(self, db):
        return classroom_repository.get_all(db)

    def get_classroom(self, db, classroom_id: UUID):

        classroom = classroom_repository.get_by_id(
            db,
            classroom_id,
        )

        if classroom is None:
            raise HTTPException(404, "Classroom not found.")

        return classroom

    def update_classroom(
        self,
        db,
        classroom_id,
        data: ClassroomUpdate,
    ):
        classroom = self.get_classroom(db, classroom_id)

        return classroom_repository.update(
            db,
            classroom,
            data.model_dump(exclude_unset=True),
        )

    def delete_classroom(self, db, classroom_id):

        classroom = self.get_classroom(db, classroom_id)

        classroom_repository.delete(
            db,
            classroom,
        )


classroom_service = ClassroomService()