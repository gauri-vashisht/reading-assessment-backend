from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums.assignment_status import AssignmentStatus
from app.models.student_assignment import StudentAssignment
from datetime import datetime,timezone
from zoneinfo import ZoneInfo 
from app.models.user import User
from app.repositories.student_assignment_repository import (
    StudentAssignmentRepository,
)
from app.schemas.student_assignment import (
    StudentAssignmentResponse,
)


class StudentAssignmentService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = StudentAssignmentRepository(db)

    def get_my_assignments(
        self,
        current_user: User,
    ) -> list[StudentAssignmentResponse]:

        assignments = self.repository.get_by_student(
            current_user.id
        )

        return [
            StudentAssignmentResponse.model_validate(a)
            for a in assignments
        ]

    def get_pending_assignments(
        self,
        current_user: User,
    ) -> list[StudentAssignmentResponse]:

        assignments = [
            a
            for a in self.repository.get_by_student(
                current_user.id
            )
            if a.status == AssignmentStatus.PENDING
        ]

        return [
            StudentAssignmentResponse.model_validate(a)
            for a in assignments
        ]

    def get_completed_assignments(
        self,
        current_user: User,
    ) -> list[StudentAssignmentResponse]:

        assignments = [
            a
            for a in self.repository.get_by_student(
                current_user.id
            )
            if a.status == AssignmentStatus.COMPLETED
        ]

        return [
            StudentAssignmentResponse.model_validate(a)
            for a in assignments
        ]

    def mark_completed(
        self,
        student_assignment_id: UUID,
        current_user: User,
    ) -> StudentAssignmentResponse:

        assignment = self.repository.get_by_id(
            student_assignment_id
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found.",
            )

        if assignment.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed.",
            )

        if assignment.status == AssignmentStatus.COMPLETED:
            return StudentAssignmentResponse.model_validate(
            assignment
        )

        assignment.status = AssignmentStatus.COMPLETED
        assignment.completed_at = datetime.now(timezone.utc)


        assignment = self.repository.update(
            assignment
        )

        self.db.commit()
        self.db.refresh(assignment)

        return StudentAssignmentResponse.model_validate(
            assignment
        )