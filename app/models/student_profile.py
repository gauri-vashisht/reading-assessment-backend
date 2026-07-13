from datetime import date

from sqlalchemy import (
    Boolean,
    Date,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.gender import Gender
from app.models.mixins import TimestampMixin, UUIDMixin


class StudentProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "student_profiles"

    __table_args__ = (
        UniqueConstraint(
            "school_id",
            "admission_number",
            name="uq_student_admission",
        ),
        UniqueConstraint(
            "classroom_id",
            "roll_number",
            name="uq_student_roll",
        ),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    school_id: Mapped[str] = mapped_column(
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    classroom_id: Mapped[str] = mapped_column(
        ForeignKey("classrooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    admission_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    roll_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    gender: Mapped[Gender] = mapped_column(
        Enum(Gender),
        nullable=False,
    )

    guardian_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    guardian_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    guardian_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    user = relationship(
        "User",
        back_populates="student_profile",
    )

    school = relationship(
        "School",
        back_populates="student_profiles",
    )

    classroom = relationship(
        "Classroom",
        back_populates="students",
    )

    audio_recordings = relationship(
        "AudioRecording",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )