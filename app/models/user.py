import uuid

from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import UserRole


from app.models.mixins import TimestampMixin

class User(Base, TimestampMixin):

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.STUDENT,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )


    teacher_profile = relationship(
        "TeacherProfile",
        back_populates="user",
        uselist=False,
    )    

    student_profile = relationship(
    "StudentProfile",
    back_populates="user",
    uselist=False,
    )

    reading_passages = relationship(
    "ReadingPassage",
    back_populates="creator",
    cascade="all, delete-orphan",
    )

