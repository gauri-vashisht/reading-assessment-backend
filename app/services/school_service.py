from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.school import School
from app.repositories.school_repository import school_repository
from app.schemas.school import SchoolCreate, SchoolUpdate


class SchoolService:

    def create_school(
        self,
        db: Session,
        data: SchoolCreate,
    ) -> School:

        if school_repository.get_by_code(db, data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="School code already exists.",
            )

        if school_repository.get_by_name(db, data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="School name already exists.",
            )

        school = School(**data.model_dump())

        return school_repository.create(db, school)

    def get_school(
        self,
        db: Session,
        school_id: UUID,
    ) -> School:

        school = school_repository.get_by_id(db, school_id)

        if school is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="School not found.",
            )

        return school

    def get_schools(
        self,
        db: Session,
    ) -> list[School]:
        return school_repository.get_all(db)

    def update_school(
        self,
        db: Session,
        school_id: UUID,
        data: SchoolUpdate,
    ) -> School:

        school = self.get_school(db, school_id)

        if data.code and data.code != school.code:
            existing = school_repository.get_by_code(db, data.code)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="School code already exists.",
                )

        if data.name and data.name != school.name:
            existing = school_repository.get_by_name(db, data.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="School name already exists.",
                )

        return school_repository.update(
            db,
            school,
            data.model_dump(exclude_unset=True),
        )

    def delete_school(
        self,
        db: Session,
        school_id: UUID,
    ) -> None:

        school = self.get_school(db, school_id)

        school_repository.delete(db, school)


school_service = SchoolService()