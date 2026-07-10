from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.grade import Grade
from app.models.mixins import TimestampMixin, UUIDMixin


class Classroom(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "classrooms"

    __table_args__ = (
        UniqueConstraint(
            "academic_year_id",
            "grade",
            "section",
            name="uq_classroom",
        ),
    )

    reading_assignments = relationship(
    "ReadingAssignment",
    back_populates="classroom",
    cascade="all, delete-orphan",
    )

    school_id: Mapped[str] = mapped_column(
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    academic_year_id: Mapped[str] = mapped_column(
        ForeignKey("academic_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    grade: Mapped[Grade] = mapped_column(
        Enum(Grade),
        nullable=False,
    )

    section: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        default=40,
    )

    room_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    school = relationship(
        "School",
        back_populates="classrooms",
    )

    academic_year = relationship(
        "AcademicYear",
        back_populates="classrooms",
    )

    class_teacher = relationship(
    "TeacherProfile",
    back_populates="classroom",
    )

    students = relationship(
    "StudentProfile",
    back_populates="classroom",
    cascade="all, delete-orphan",
    )