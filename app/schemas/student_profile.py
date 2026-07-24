from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.enums.gender import Gender

PHONE_REGEX = r"^[6-9]\d{9}$"
PIN_REGEX = r"^\d{6}$"


class StudentProfileBase(BaseModel):
    user_id: UUID
    school_id: UUID
    classroom_id: UUID

    admission_number: str = Field(min_length=1, max_length=30)
    roll_number: str = Field(min_length=1, max_length=20)

    date_of_birth: date
    gender: Gender

    guardian_name: str = Field(min_length=2, max_length=255)

    guardian_phone: str = Field(pattern=PHONE_REGEX)

    guardian_email: EmailStr | None = None

    address: str | None = None

    city: str | None = None

    state: str | None = None

    postal_code: str | None = Field(
        default=None,
        pattern=PIN_REGEX,
    )

    is_active: bool = True

    @model_validator(mode="after")
    def validate_dob(self):
        if self.date_of_birth >= date.today():
            raise ValueError(
                "Date of birth must be in the past."
            )
        return self


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(BaseModel):

    classroom_id: UUID | None = None

    roll_number: str | None = None

    guardian_name: str | None = None

    guardian_phone: str | None = Field(
        default=None,
        pattern=PHONE_REGEX,
    )

    guardian_email: EmailStr | None = None

    address: str | None = None

    city: str | None = None

    state: str | None = None

    postal_code: str | None = Field(
        default=None,
        pattern=PIN_REGEX,
    )

    is_active: bool | None = None
class StudentProfileResponse(StudentProfileBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
    )
class StudentSummaryResponse(BaseModel):
    id: UUID          # User.id
    full_name: str

    model_config = {
        "from_attributes": True
    }