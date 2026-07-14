from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.assessment_result import AssessmentStatus


class AssessmentResultBase(BaseModel):
    transcript: str | None = None

    total_words: int = 0

    correct_words: int = 0

    incorrect_words: int = 0

    skipped_words: int = 0

    extra_words: int = 0

    accuracy_percentage: float = 0

    words_per_minute: float = 0

    processing_time_seconds: float | None = None

    status: AssessmentStatus = AssessmentStatus.PENDING


class AssessmentResultCreate(BaseModel):
    recording_id: UUID


class AssessmentResultUpdate(BaseModel):
    transcript: str | None = None

    total_words: int | None = None

    correct_words: int | None = None

    incorrect_words: int | None = None

    skipped_words: int | None = None

    extra_words: int | None = None

    accuracy_percentage: float | None = None

    words_per_minute: float | None = None

    processing_time_seconds: float | None = None

    status: AssessmentStatus | None = None


class AssessmentResultResponse(
    AssessmentResultBase,
):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    recording_id: UUID

    assignment_id: UUID

    student_profile_id: UUID

    created_at: datetime

    updated_at: datetime

    reading_level: str

    teacher_feedback: str

    student_feedback: str

    summary: str