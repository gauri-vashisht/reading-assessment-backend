from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.academic_year import AcademicYear
from app.repositories.academic_year_repository import (
    academic_year_repository,
)
from app.repositories.school_repository import school_repository
from app.schemas.academic_year import (
    AcademicYearCreate,
    AcademicYearUpdate,
)


class AcademicYearService:

    def create_academic_year(
        self,
        db: Session,
        data: AcademicYearCreate,
    ) -> AcademicYear:

        school = school_repository.get_by_id(
            db,
            data.school_id,
        )

        if school is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="School not found.",
            )

        existing = academic_year_repository.get_by_name(
            db,
            data.school_id,
            data.name,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Academic year already exists.",
            )

        if data.is_current:

            current = academic_year_repository.get_current(
                db,
                data.school_id,
            )

            if current:
                current.is_current = False

        academic_year = AcademicYear(
            **data.model_dump()
        )

        return academic_year_repository.create(
            db,
            academic_year,
        )

    def get_academic_year(
        self,
        db: Session,
        academic_year_id: UUID,
    ) -> AcademicYear:

        academic_year = academic_year_repository.get_by_id(
            db,
            academic_year_id,
        )

        if academic_year is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Academic year not found.",
            )

        return academic_year

    def get_academic_years(
        self,
        db: Session,
    ) -> list[AcademicYear]:

        return academic_year_repository.get_all(db)

    def update_academic_year(
        self,
        db: Session,
        academic_year_id: UUID,
        data: AcademicYearUpdate,
    ) -> AcademicYear:

        academic_year = self.get_academic_year(
            db,
            academic_year_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:

            existing = academic_year_repository.get_by_name(
                db,
                academic_year.school_id,
                update_data["name"],
            )

            if (
                existing
                and existing.id != academic_year.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Academic year already exists.",
                )

        if update_data.get("is_current"):

            current = academic_year_repository.get_current(
                db,
                academic_year.school_id,
            )

            if (
                current
                and current.id != academic_year.id
            ):
                current.is_current = False

        return academic_year_repository.update(
            db,
            academic_year,
            update_data,
        )

    def delete_academic_year(
        self,
        db: Session,
        academic_year_id: UUID,
    ):

        academic_year = self.get_academic_year(
            db,
            academic_year_id,
        )

        academic_year_repository.delete(
            db,
            academic_year,
        )


academic_year_service = AcademicYearService()