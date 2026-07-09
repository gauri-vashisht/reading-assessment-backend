from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SchoolBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
        examples=["ABC Public School"],
    )

    code: str = Field(
        min_length=2,
        max_length=50,
        pattern=r"^[A-Z0-9_-]+$",
        examples=["ABC001"],
    )

    address_line: str | None = Field(
        default=None,
        max_length=255,
    )

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    postal_code: str | None = Field(
        default=None,
        pattern=r"^\d{6}$",
        examples=["147001"],
    )

    country: str = Field(
        default="India",
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        pattern=r"^[6-9]\d{9}$",
        examples=["9876543210"],
    )

    email: EmailStr | None = None

    is_active: bool = True


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)

    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        pattern=r"^[A-Z0-9_-]+$",
        unique=True,
    )

    address_line: str | None = Field(default=None, max_length=255)

    city: str | None = Field(default=None, max_length=100)

    state: str | None = Field(default=None, max_length=100)

    postal_code: str | None = Field(
        default=None,
        pattern=r"^\d{6}$",
    )

    country: str | None = Field(default=None, max_length=100)

    phone: str | None = Field(
        default=None,
        pattern=r"^[6-9]\d{9}$",
    )

    email: EmailStr | None = None

    is_active: bool | None = None


class SchoolResponse(SchoolBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)