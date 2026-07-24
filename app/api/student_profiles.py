from uuid import UUID

from fastapi import APIRouter, Depends, status, Query
from app.schemas.student_profile import (
    StudentSummaryResponse,
)

from app.dependencies.auth import (
    get_current_user,
    require_admin,
)
from app.dependencies.database import DBSession
from app.schemas.student_profile import (
    StudentProfileCreate,
    StudentProfileResponse,
    StudentProfileUpdate,
)
from app.services.student_profile_service import (
    student_profile_service,
)

router = APIRouter(
    prefix="/student-profiles",
    tags=["Student Profiles"],
)


@router.post(
    "",
    response_model=StudentProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student: StudentProfileCreate,
    db: DBSession,
    user=Depends(require_admin),
):
    return student_profile_service.create_student_profile(
        db,
        student,
    )


@router.get(
    "",
    response_model=list[StudentSummaryResponse] | list[StudentProfileResponse],
)
def get_students(
    db: DBSession,
    user=Depends(get_current_user),
    classroom_id: UUID | None = Query(None),
    summary: bool = Query(False),
):
    return student_profile_service.get_students(
        db,
        classroom_id=classroom_id,
        summary=summary,
    )


@router.get(
    "/{student_id}",
    response_model=StudentProfileResponse,
)
def get_student(
    student_id: UUID,
    db: DBSession,
    user=Depends(get_current_user),
):
    return student_profile_service.get_student(
        db,
        student_id,
    )


@router.put(
    "/{student_id}",
    response_model=StudentProfileResponse,
)
def update_student(
    student_id: UUID,
    student: StudentProfileUpdate,
    db: DBSession,
    user=Depends(require_admin),
):
    return student_profile_service.update_student(
        db,
        student_id,
        student,
    )


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(
    student_id: UUID,
    db: DBSession,
    user=Depends(require_admin),
):
    student_profile_service.delete_student(
        db,
        student_id,
    )