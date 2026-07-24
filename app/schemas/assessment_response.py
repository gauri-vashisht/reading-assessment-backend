from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field  # Added Field here

from app.models.assessment_result import AssessmentStatus
from app.enums.grade import Grade
from app.enums.reading_difficulty import ReadingDifficulty

class WordStatus(str, Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    SKIPPED = "skipped"

class WordResult(BaseModel):
    word: str
    status: WordStatus

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
    status: str
    is_overdue: bool
    completed_count: int
    pending_count: int 
    created_at: datetime
    updated_at: datetime

class ReadingAssignmentListResponse(BaseModel):
    items: list[ReadingAssignmentResponse]
    total: int

class AssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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
