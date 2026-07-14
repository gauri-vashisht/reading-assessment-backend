from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Integer,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AssessmentStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    recording_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("audio_recordings.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    assignment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reading_assignments.id", ondelete="CASCADE"),
        nullable=False,
    )

    student_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("student_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    transcript: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    total_words: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    correct_words: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    incorrect_words: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    skipped_words: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    extra_words: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    incorrect_word_list: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    skipped_word_list: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    extra_word_list: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    accuracy_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    words_per_minute: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    processing_time_seconds: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[AssessmentStatus] = mapped_column(
        SqlEnum(
            AssessmentStatus,
            name="assessment_status",
            create_constraint=True,
            create_type=False,
        ),
        default=AssessmentStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    recording = relationship(
        "AudioRecording",
        back_populates="assessment_result",
    )

    assignment = relationship(
        "ReadingAssignment",
    )

    student = relationship(
        "StudentProfile",
    )