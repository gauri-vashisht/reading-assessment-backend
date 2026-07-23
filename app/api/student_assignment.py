from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.student_assignment import (
    StudentAssignmentResponse,
)
from app.services.student_assignment_service import (
    StudentAssignmentService,
)

router = APIRouter(
    prefix="/student-assignments",
    tags=["Student Assignments"],
)


@router.get(
    "/my",
    response_model=list[StudentAssignmentResponse],
)
def get_my_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StudentAssignmentService(db)

    return service.get_my_assignments(
        current_user,
    )


@router.get(
    "/pending",
    response_model=list[StudentAssignmentResponse],
)
def get_pending_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StudentAssignmentService(db)

    return service.get_pending_assignments(
        current_user,
    )


@router.get(
    "/completed",
    response_model=list[StudentAssignmentResponse],
)
def get_completed_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StudentAssignmentService(db)

    return service.get_completed_assignments(
        current_user,
    )


@router.patch(
    "/{student_assignment_id}/complete",
    response_model=StudentAssignmentResponse,
)
def mark_assignment_completed(
    student_assignment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StudentAssignmentService(db)

    return service.mark_completed(
        student_assignment_id,
        current_user,
    )