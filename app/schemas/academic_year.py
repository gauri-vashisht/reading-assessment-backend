from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AcademicYearBase(BaseModel):
    school_id: UUID

    name: str = Field(
        pattern=r"^\d{4}-\d{4}$",
        examples=["2025-2026"],
    )

    start_date: date
    end_date: date

    is_current: bool = False

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError(
                "end_date must be after start_date."
            )
        return self


class AcademicYearCreate(AcademicYearBase):
    pass


class AcademicYearUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        pattern=r"^\d{4}-\d{4}$",
    )

    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date
            and self.end_date
            and self.end_date <= self.start_date
        ):
            raise ValueError(
                "end_date must be after start_date."
            )
        return self


class AcademicYearResponse(AcademicYearBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )