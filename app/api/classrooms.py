from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.database import DBSession
from app.schemas.classroom import (
    ClassroomCreate,
    ClassroomResponse,
    ClassroomUpdate,
)
from app.services.classroom_service import classroom_service

router = APIRouter(
    prefix="/classrooms",
    tags=["Classrooms"],
)


@router.post("", response_model=ClassroomResponse, status_code=status.HTTP_201_CREATED)
def create_classroom(classroom: ClassroomCreate, db: DBSession, user=Depends(require_admin)):
    return classroom_service.create_classroom(db, classroom)


@router.get("", response_model=list[ClassroomResponse])
def get_classrooms(db: DBSession, user=Depends(get_current_user)):
    return classroom_service.get_classrooms(db)


@router.get("/{classroom_id}", response_model=ClassroomResponse)
def get_classroom(classroom_id: UUID, db: DBSession, user=Depends(get_current_user)):
    return classroom_service.get_classroom(db, classroom_id)


@router.put("/{classroom_id}", response_model=ClassroomResponse)
def update_classroom(classroom_id: UUID, classroom: ClassroomUpdate, db: DBSession, user=Depends(require_admin)):
    return classroom_service.update_classroom(db, classroom_id, classroom)


@router.delete("/{classroom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_classroom(classroom_id: UUID, db: DBSession, user=Depends(require_admin)):
    classroom_service.delete_classroom(db, classroom_id)