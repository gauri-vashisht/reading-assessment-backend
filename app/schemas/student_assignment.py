from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.assignment_status import AssignmentStatus


class StudentAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    assignment_id: UUID
    student_id: UUID

    status: AssignmentStatus
    completed_at: datetime | None

    created_at: datetime
    updated_at: datetime


class StudentAssignmentUpdate(BaseModel):
    status: AssignmentStatus | None = None
    completed_at: datetime | None = None