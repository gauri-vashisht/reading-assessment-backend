from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.grade import Grade
from app.enums.reading_difficulty import ReadingDifficulty


class ReadingAssignmentCreate(BaseModel):
    passage_id: UUID
    classroom_id: UUID | None = None
    student_user_id: UUID | None = None
    due_date: datetime | None = None
    remarks: str | None = Field(default=None, max_length=1000)


class ReadingAssignmentUpdate(BaseModel):
    classroom_id: UUID | None = None
    due_date: datetime | None = None
    remarks: str | None = Field(default=None, max_length=1000)


# ---------- Summary Models ----------

class PassageSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    grade: int
    difficulty: ReadingDifficulty
    word_count: int


class ClassroomSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    grade: Grade
    section: str


class StudentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str


# ---------- Response ----------

class ReadingAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    passage: PassageSummary
    classroom: ClassroomSummary | None
    student: StudentSummary | None
    due_date: datetime | None
    remarks: str | None
    student_count: int
    created_at: datetime
    updated_at: datetime
    status: str
    is_overdue: bool
    completed_count: int
    pending_count: int


class ReadingAssignmentListResponse(BaseModel):
    items: list[ReadingAssignmentResponse]
    total: int