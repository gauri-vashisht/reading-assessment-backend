from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.grade import Grade


class ClassroomBase(BaseModel):
    school_id: UUID
    academic_year_id: UUID

    grade: Grade

    section: str = Field(
        pattern=r"^[A-Z]$",
        examples=["A"],
    )

    capacity: int = Field(
        ge=1,
        le=100,
        default=40,
    )

    room_number: str | None = Field(
        default=None,
        max_length=20,
    )

    is_active: bool = True


class ClassroomCreate(ClassroomBase):
    pass


class ClassroomUpdate(BaseModel):

    grade: Grade | None = None

    section: str | None = Field(
        default=None,
        pattern=r"^[A-Z]$",
    )

    capacity: int | None = Field(
        default=None,
        ge=1,
        le=100,
    )

    room_number: str | None = None

    is_active: bool | None = None


class ClassroomResponse(ClassroomBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )