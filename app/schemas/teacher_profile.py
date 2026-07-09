from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.enums.teacher_designation import TeacherDesignation


PHONE_REGEX = r"^[6-9]\d{9}$"


class TeacherProfileBase(BaseModel):
    user_id: UUID
    school_id: UUID
    classroom_id: UUID | None = None

    employee_id: str = Field(min_length=2, max_length=30)

    designation: TeacherDesignation = TeacherDesignation.TEACHER

    qualification: str | None = Field(default=None, max_length=255)

    experience_years: int = Field(
        default=0,
        ge=0,
        le=60,
    )

    joining_date: date

    phone: str | None = Field(
        default=None,
        pattern=PHONE_REGEX,
    )

    alternate_phone: str | None = Field(
        default=None,
        pattern=PHONE_REGEX,
    )

    is_class_teacher: bool = False

    @model_validator(mode="after")
    def validate_class_teacher(self):
        if self.is_class_teacher and self.classroom_id is None:
            raise ValueError(
                "classroom_id is required when is_class_teacher=True."
            )
        return self


class TeacherProfileCreate(TeacherProfileBase):
    pass


class TeacherProfileUpdate(BaseModel):

    classroom_id: UUID | None = None

    designation: TeacherDesignation | None = None

    qualification: str | None = None

    experience_years: int | None = Field(
        default=None,
        ge=0,
        le=60,
    )

    joining_date: date | None = None

    phone: str | None = Field(
        default=None,
        pattern=PHONE_REGEX,
    )

    alternate_phone: str | None = Field(
        default=None,
        pattern=PHONE_REGEX,
    )

    is_class_teacher: bool | None = None


class TeacherProfileResponse(TeacherProfileBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )