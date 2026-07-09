from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDMixin


class School(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "schools"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    address_line: Mapped[str | None] = mapped_column(
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

    phone: Mapped[str | None] = mapped_column(
    String(20),
    nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        default="India",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    academic_years = relationship(
    "AcademicYear",
    back_populates="school",
    cascade="all, delete-orphan",
    )

    classrooms = relationship(
    "Classroom",
    back_populates="school",
    cascade="all, delete-orphan",
    )

    teacher_profiles = relationship(
    "TeacherProfile",
    back_populates="school",
    cascade="all, delete-orphan",
    )   

    student_profiles = relationship(
    "StudentProfile",
    back_populates="school",
    cascade="all, delete-orphan",
    )