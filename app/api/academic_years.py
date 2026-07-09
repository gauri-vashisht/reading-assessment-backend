from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import (
    get_current_user,
    require_admin,
)
from app.dependencies.database import DBSession
from app.schemas.academic_year import (
    AcademicYearCreate,
    AcademicYearResponse,
    AcademicYearUpdate,
)
from app.services.academic_year_service import (
    academic_year_service,
)

router = APIRouter(
    prefix="/academic-years",
    tags=["Academic Years"],
)


@router.post(
    "",
    response_model=AcademicYearResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_academic_year(
    academic_year: AcademicYearCreate,
    db: DBSession,
    user=Depends(require_admin),
):
    return academic_year_service.create_academic_year(
        db,
        academic_year,
    )


@router.get(
    "",
    response_model=list[AcademicYearResponse],
)
def get_academic_years(
    db: DBSession,
    user=Depends(get_current_user),
):
    return academic_year_service.get_academic_years(
        db
    )


@router.get(
    "/{academic_year_id}",
    response_model=AcademicYearResponse,
)
def get_academic_year(
    academic_year_id: UUID,
    db: DBSession,
    user=Depends(get_current_user),
):
    return academic_year_service.get_academic_year(
        db,
        academic_year_id,
    )


@router.put(
    "/{academic_year_id}",
    response_model=AcademicYearResponse,
)
def update_academic_year(
    academic_year_id: UUID,
    academic_year: AcademicYearUpdate,
    db: DBSession,
    user=Depends(require_admin),
):
    return academic_year_service.update_academic_year(
        db,
        academic_year_id,
        academic_year,
    )


@router.delete(
    "/{academic_year_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_academic_year(
    academic_year_id: UUID,
    db: DBSession,
    user=Depends(require_admin),
):
    academic_year_service.delete_academic_year(
        db,
        academic_year_id,
    )