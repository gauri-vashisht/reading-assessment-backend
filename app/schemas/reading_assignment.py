from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReadingAssignmentCreate(BaseModel):
    passage_id: UUID
    classroom_id: UUID | None = None
    student_id: UUID | None = None
    due_date: datetime | None = None
    remarks: str | None = Field(default=None, max_length=1000)


class ReadingAssignmentUpdate(BaseModel):
    classroom_id: UUID | None = None
    due_date: datetime | None = None
    remarks: str | None = Field(default=None, max_length=1000)


class ReadingAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    passage_id: UUID
    classroom_id: UUID | None
    assigned_by: UUID
    due_date: datetime | None
    remarks: str | None
    created_at: datetime
    updated_at: datetime


class ReadingAssignmentListResponse(BaseModel):
    items: list[ReadingAssignmentResponse]
    total: int