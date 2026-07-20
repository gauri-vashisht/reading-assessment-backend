from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.assignment_status import AssignmentStatus

from app.enums.reading_difficulty import ReadingDifficulty
class ReadingPassageSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    passage: str
    grade: int
    difficulty: ReadingDifficulty
    word_count: int
    expected_reading_time_minutes: int


class ReadingAssignmentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    due_date: datetime | None
    remarks: str | None

    passage: ReadingPassageSummary


class StudentAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    assignment_id: UUID
    student_id: UUID

    status: AssignmentStatus
    completed_at: datetime | None

    created_at: datetime
    updated_at: datetime

    assignment: ReadingAssignmentSummary