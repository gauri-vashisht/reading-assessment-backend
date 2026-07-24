from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.database.session import get_db
from app.dependencies.auth import (
    get_current_user,
    require_teacher,
)
from app.models.user import User
from app.schemas.reading_passage import (
    ReadingPassageCreate,
    ReadingPassageResponse,
    ReadingPassageUpdate,
)
from app.services.reading_passage_service import ReadingPassageService
from app.schemas.reading_passage import ReadingPassageSummaryResponse

router = APIRouter(
    prefix="/reading-passages",
    tags=["Reading Passages"],
)

@router.post(
    "",
    response_model=ReadingPassageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reading_passage(
    passage: ReadingPassageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    service = ReadingPassageService(db)
    return service.create(passage, current_user)

@router.get(
    "",
    response_model=list[ReadingPassageSummaryResponse] | list[ReadingPassageResponse],
)
def get_all_reading_passages(
    is_active: bool | None = Query(None),
    summary: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ReadingPassageService(db)

    return service.get_all(
        is_active=is_active,
        summary=summary,
    )

@router.get(
    "/{passage_id}",
    response_model=ReadingPassageResponse,
)
def get_reading_passage(
    passage_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ReadingPassageService(db)

    passage = service.get_by_id(passage_id)

    if not passage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading passage not found.",
        )

    return passage


@router.put(
    "/{passage_id}",
    response_model=ReadingPassageResponse,
)
def update_reading_passage(
    passage_id: UUID,
    data: ReadingPassageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    service = ReadingPassageService(db)

    passage = service.update(
        passage_id,
        data,
    )

    if not passage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading passage not found.",
        )

    return passage


@router.delete(
    "/{passage_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reading_passage(
    passage_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher),
):
    service = ReadingPassageService(db)

    deleted = service.delete(passage_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading passage not found.",
        )