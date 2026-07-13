from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base


class ReadingAssignment(Base):
    __tablename__ = "reading_assignments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    passage_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reading_passages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    classroom_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classrooms.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    assigned_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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

    passage = relationship(
        "ReadingPassage",
        back_populates="assignments",
    )

    classroom = relationship(
        "Classroom",
        back_populates="reading_assignments",
    )

    teacher = relationship(
        "User",
        foreign_keys=[assigned_by],
    )


    student_assignments = relationship(
        "StudentAssignment",
        back_populates="assignment",
        cascade="all, delete-orphan",
    )

    audio_recordings = relationship(
        "AudioRecording",
        back_populates="assignment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    