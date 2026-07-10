from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import (
    get_current_user,
    require_teacher,
)
from app.models.user import User
from app.schemas.reading_assignment import (
    ReadingAssignmentCreate,
    ReadingAssignmentListResponse,
    ReadingAssignmentResponse,
    ReadingAssignmentUpdate,
)
from app.services.reading_assignment_service import (
    ReadingAssignmentService,
)

router = APIRouter(
    prefix="/reading-assignments",
    tags=["Reading Assignments"],
)


@router.post(
    "",
    response_model=ReadingAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reading_assignment(
    assignment: ReadingAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    service = ReadingAssignmentService(db)

    return service.create(
        assignment,
        current_user,
    )


@router.get(
    "",
    response_model=ReadingAssignmentListResponse,
)
def get_all_reading_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ReadingAssignmentService(db)

    return service.get_all(
        skip,
        limit,
    )


@router.get(
    "/{assignment_id}",
    response_model=ReadingAssignmentResponse,
)
def get_reading_assignment(
    assignment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ReadingAssignmentService(db)

    assignment = service.get_by_id(
        assignment_id,
    )

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading assignment not found.",
        )

    return assignment


@router.put(
    "/{assignment_id}",
    response_model=ReadingAssignmentResponse,
)
def update_reading_assignment(
    assignment_id: UUID,
    data: ReadingAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    service = ReadingAssignmentService(db)

    assignment = service.update(
        assignment_id,
        data,
    )

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading assignment not found.",
        )

    return assignment


@router.delete(
    "/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reading_assignment(
    assignment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    service = ReadingAssignmentService(db)

    deleted = service.delete(
        assignment_id,
    )

    if deleted is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading assignment not found.",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )




