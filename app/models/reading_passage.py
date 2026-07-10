from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin
from app.enums.reading_difficulty import ReadingDifficulty


class ReadingPassage(Base, TimestampMixin):
    __tablename__ = "reading_passages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    title = Column(String(255), nullable=False)

    passage = Column(Text, nullable=False)

    grade = Column(Integer, nullable=False)

    subject = Column(String(100), nullable=False)

    difficulty = Column(
        Enum(ReadingDifficulty, name="reading_difficulty_enum"),
        nullable=False,
    )

    language = Column(
        String(50),
        nullable=False,
        default="English",
    )

    expected_reading_time = Column(
        Integer,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    creator = relationship(
        "User",
        back_populates="reading_passages",
    )