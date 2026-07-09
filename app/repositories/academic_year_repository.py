from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.academic_year import AcademicYear
from app.repositories.base_repository import BaseRepository


class AcademicYearRepository(
    BaseRepository[AcademicYear]
):

    def __init__(self):
        super().__init__(AcademicYear)

    def get_by_name(
        self,
        db: Session,
        school_id,
        name: str,
    ):
        stmt = select(AcademicYear).where(
            AcademicYear.school_id == school_id,
            AcademicYear.name == name,
        )

        return db.scalar(stmt)

    def get_current(
        self,
        db: Session,
        school_id,
    ):
        stmt = select(AcademicYear).where(
            AcademicYear.school_id == school_id,
            AcademicYear.is_current.is_(True),
        )

        return db.scalar(stmt)

    def update(
        self,
        db: Session,
        academic_year: AcademicYear,
        data: dict,
    ):

        for key, value in data.items():
            setattr(academic_year, key, value)

        db.flush()
        db.refresh(academic_year)

        return academic_year


academic_year_repository = AcademicYearRepository()