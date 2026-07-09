from datetime import date

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.enums.teacher_designation import TeacherDesignation
from app.models.mixins import TimestampMixin, UUIDMixin


class TeacherProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "teacher_profiles"

    __table_args__ = (
        UniqueConstraint(
            "school_id",
            "employee_id",
            name="uq_teacher_employee",
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

    classroom_id: Mapped[str | None] = mapped_column(
        ForeignKey("classrooms.id", ondelete="SET NULL"),
        nullable=True,
    )

    employee_id: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    designation: Mapped[TeacherDesignation] = mapped_column(
        Enum(TeacherDesignation),
        nullable=False,
        default=TeacherDesignation.TEACHER,
    )

    qualification: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    experience_years: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    joining_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    alternate_phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_class_teacher: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    user = relationship(
        "User",
        back_populates="teacher_profile",
    )

    school = relationship(
        "School",
        back_populates="teacher_profiles",
    )

    classroom = relationship(
        "Classroom",
        back_populates="class_teacher",
    )