from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import (
    get_current_user,
    require_admin,
)
from app.dependencies.database import DBSession
from app.schemas.teacher_profile import (
    TeacherProfileCreate,
    TeacherProfileResponse,
    TeacherProfileUpdate,
)
from app.services.teacher_profile_service import (
    teacher_profile_service,
)

router = APIRouter(
    prefix="/teacher-profiles",
    tags=["Teacher Profiles"],
)


@router.post(
    "",
    response_model=TeacherProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_teacher_profile(
    teacher: TeacherProfileCreate,
    db: DBSession,
    user=Depends(require_admin),
):
    return teacher_profile_service.create_teacher_profile(
        db,
        teacher,
    )


@router.get(
    "",
    response_model=list[TeacherProfileResponse],
)
def get_teacher_profiles(
    db: DBSession,
    user=Depends(get_current_user),
):
    return teacher_profile_service.get_teacher_profiles(db)


@router.get(
    "/{teacher_id}",
    response_model=TeacherProfileResponse,
)
def get_teacher_profile(
    teacher_id: UUID,
    db: DBSession,
    user=Depends(get_current_user),
):
    return teacher_profile_service.get_teacher_profile(
        db,
        teacher_id,
    )


@router.put(
    "/{teacher_id}",
    response_model=TeacherProfileResponse,
)
def update_teacher_profile(
    teacher_id: UUID,
    teacher: TeacherProfileUpdate,
    db: DBSession,
    user=Depends(require_admin),
):
    return teacher_profile_service.update_teacher_profile(
        db,
        teacher_id,
        teacher,
    )


@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_teacher_profile(
    teacher_id: UUID,
    db: DBSession,
    user=Depends(require_admin),
):
    teacher_profile_service.delete_teacher_profile(
        db,
        teacher_id,
    )