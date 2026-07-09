from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import (
    get_current_user,
    require_admin,
)
from app.dependencies.database import DBSession
from app.schemas.school import (
    SchoolCreate,
    SchoolResponse,
    SchoolUpdate,
)
from app.services.school_service import school_service

router = APIRouter(
    prefix="/schools",
    tags=["Schools"],
)


@router.post(
    "",
    response_model=SchoolResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_school(
    school: SchoolCreate,
    db: DBSession,
    user=Depends(require_admin),
):
    return school_service.create_school(
        db,
        school,
    )


@router.get(
    "",
    response_model=list[SchoolResponse],
)
def get_schools(
    db: DBSession,
    user=Depends(get_current_user),
):
    return school_service.get_schools(db)


@router.get(
    "/{school_id}",
    response_model=SchoolResponse,
)
def get_school(
    school_id: UUID,
    db: DBSession,
    user=Depends(get_current_user),
):
    return school_service.get_school(
        db,
        school_id,
    )


@router.put(
    "/{school_id}",
    response_model=SchoolResponse,
)
def update_school(
    school_id: UUID,
    school: SchoolUpdate,
    db: DBSession,
    user=Depends(require_admin),
):
    return school_service.update_school(
        db,
        school_id,
        school,
    )


@router.delete(
    "/{school_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_school(
    school_id: UUID,
    db: DBSession,
    user=Depends(require_admin),
):
    school_service.delete_school(
        db,
        school_id,
    )