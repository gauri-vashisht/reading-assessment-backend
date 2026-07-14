from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.assessment_result import AssessmentStatus


class WordStatus(str, Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    SKIPPED = "skipped"


class WordResult(BaseModel):
    word: str
    status: WordStatus


class AssessmentResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    recording_id: UUID

    assignment_id: UUID

    student_profile_id: UUID

    transcript: str | None

    total_words: int

    correct_words: int

    incorrect_words: int

    skipped_words: int

    extra_words: int

    incorrect_word_list: list[str]

    skipped_word_list: list[str]

    extra_word_list: list[str]

    word_results: list[WordResult]

    accuracy_percentage: float

    words_per_minute: float

    processing_time_seconds: float | None

    status: AssessmentStatus

    created_at: datetime

    updated_at: datetime

    reading_level: str

    teacher_feedback: str

    student_feedback: str

    summary: str