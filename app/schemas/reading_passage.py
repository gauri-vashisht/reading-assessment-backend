from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.reading_difficulty import ReadingDifficulty


class ReadingPassageBase(BaseModel):
    title: str = Field(..., max_length=255)
    passage: str
    grade: int = Field(..., ge=3, le=8)
    subject: str = Field(..., max_length=100)
    difficulty: ReadingDifficulty
    language: str = Field(default="English", max_length=50)
    expected_reading_time: int = Field(..., gt=0)
    is_active: bool = True


class ReadingPassageCreate(ReadingPassageBase):
    pass


class ReadingPassageUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    passage: str | None = None
    grade: int | None = Field(default=None, ge=3, le=8)
    subject: str | None = Field(default=None, max_length=100)
    difficulty: ReadingDifficulty | None = None
    language: str | None = Field(default=None, max_length=50)
    expected_reading_time: int | None = Field(default=None, gt=0)
    is_active: bool | None = None


class ReadingPassageResponse(ReadingPassageBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime