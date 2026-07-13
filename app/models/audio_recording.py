from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDMixin


class AudioRecording(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "audio_recordings"

    assignment_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "reading_assignments.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    student_profile_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "student_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    bucket_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    checksum: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    assignment = relationship(
        "ReadingAssignment",
        back_populates="audio_recordings",
    )

    student = relationship(
        "StudentProfile",
        back_populates="audio_recordings",
    )