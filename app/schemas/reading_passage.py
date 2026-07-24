from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.reading_difficulty import ReadingDifficulty


class ReadingPassageBase(BaseModel):
    title: str = Field(..., max_length=255)
    passage: str
    grade: int = Field(..., ge=3, le=8)
    difficulty: ReadingDifficulty
    is_active: bool = True
    expected_reading_time_minutes: int = Field(..., gt=0)


class ReadingPassageCreate(ReadingPassageBase):
    pass


class ReadingPassageUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    passage: str | None = None
    grade: int | None = Field(default=None, ge=3, le=8)
    difficulty: ReadingDifficulty | None = None
    is_active: bool | None = None


class ReadingPassageResponse(ReadingPassageBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    word_count: int

class ReadingPassageSummaryResponse(BaseModel):
    id: UUID
    title: str
    grade: int

    model_config = {
        "from_attributes": True
    }