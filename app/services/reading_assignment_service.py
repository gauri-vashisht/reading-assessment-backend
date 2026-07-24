from uuid import UUID
from fastapi import HTTPException, status
from datetime import datetime, timezone
from app.enums.assignment_status import AssignmentStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.classroom import Classroom
from app.models.reading_assignment import ReadingAssignment
from app.models.reading_passage import ReadingPassage
from app.models.student_assignment import StudentAssignment
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.repositories.reading_assignment_repository import (
    ReadingAssignmentRepository,
)
from app.repositories.student_assignment_repository import (
    StudentAssignmentRepository,
)
from app.schemas.reading_assignment import (
    ClassroomSummary,
    PassageSummary,
    ReadingAssignmentCreate,
    ReadingAssignmentListResponse,
    ReadingAssignmentResponse,
    ReadingAssignmentUpdate,
    StudentSummary,
)
class ReadingAssignmentService:

    def __init__(self, db: Session):
        self.db = db
        self.assignment_repo = ReadingAssignmentRepository(db)
        self.student_repo = StudentAssignmentRepository(db)

    def _to_response(
        self,
        assignment: ReadingAssignment,
    ) -> ReadingAssignmentResponse:

        student = None

        if assignment.classroom_id is None:
            if assignment.student_assignments:
                user = assignment.student_assignments[0].student

                student = StudentSummary(
                    id=user.id,
                    full_name=user.full_name,
                )

        completed_count = sum(
            1
            for sa in assignment.student_assignments
            if sa.status == AssignmentStatus.COMPLETED
        )

        pending_count = sum(
            1
            for sa in assignment.student_assignments
            if sa.status == AssignmentStatus.PENDING
        )

        is_overdue = (
            assignment.due_date is not None
            and assignment.due_date < datetime.now(timezone.utc)
            and pending_count > 0
        )

        status = (
            "COMPLETED"
            if pending_count == 0
            else "OVERDUE"
            if is_overdue
            else "ACTIVE"
        )

        return ReadingAssignmentResponse(
            id=assignment.id,

            passage=PassageSummary.model_validate(
                assignment.passage
            ),

            classroom=(
                ClassroomSummary.model_validate(
                    assignment.classroom
                )
                if assignment.classroom
                else None
            ),

            student=student,

            due_date=assignment.due_date,

            remarks=assignment.remarks,

            student_count=len(
                assignment.student_assignments
            ),

            status=status,

            is_overdue=is_overdue,

            completed_count=completed_count,

            pending_count=pending_count,

            created_at=assignment.created_at,

            updated_at=assignment.updated_at,
        )

    def create(
        self,
        data: ReadingAssignmentCreate,
        current_user: User,
    ) -> ReadingAssignmentResponse:

        if (data.student_user_id is None) == (
            data.classroom_id is None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide either student_user_id or classroom_id.",
            )

        passage = self.db.get(
            ReadingPassage,
            data.passage_id,
        )

        if passage is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reading passage not found.",
            )

        if data.classroom_id:

            classroom = self.db.get(
                Classroom,
                data.classroom_id,
            )

            if classroom is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Classroom not found.",
                )

        if data.student_user_id:

            user = self.db.get(
                User,
                data.student_user_id,
            )


            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student not found.",
                )
            student_profile = self.db.scalar(
            select(StudentProfile).where(
                StudentProfile.user_id == data.student_user_id
                )
            )

            if student_profile is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student profile not found.",
                )

        assignment = ReadingAssignment(
            passage_id=data.passage_id,
            classroom_id=(
                data.classroom_id
                if data.student_user_id is None
                else None
            ),
            assigned_by=current_user.id,
            due_date=data.due_date,
            remarks=data.remarks,
        )

        assignment = self.assignment_repo.create(
            assignment
        )

        if data.student_user_id:

            self.student_repo.create(
                StudentAssignment(
                    assignment_id=assignment.id,
                    student_id=data.student_user_id,
                )
            )

        else:

            students = (
                self.db.scalars(
                    select(StudentProfile).where(
                        StudentProfile.classroom_id
                        == data.classroom_id
                    )
                )
                .all()
            )

            if not students:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No students found in classroom.",
                )

            student_assignments = [
                StudentAssignment(
                    assignment_id=assignment.id,
                    student_id=student.user_id,
                )
                for student in students
            ]

            self.student_repo.bulk_create(
                student_assignments
            )

        self.db.commit()
        assignment = self.assignment_repo.get_by_id(
            assignment.id
        )

        return self._to_response(
            assignment
        )
    def get_by_id(
        self,
        assignment_id: UUID,
    ) -> ReadingAssignmentResponse:

        assignment = self.assignment_repo.get_by_id(
            assignment_id
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found.",
            )

        return self._to_response(
            assignment
        )

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> ReadingAssignmentListResponse:

        assignments, total = self.assignment_repo.get_all(
            skip,
            limit,
        )

        return ReadingAssignmentListResponse(
            items=[
                self._to_response(
                    assignment
                )
                for assignment in assignments
            ],
            total=total,
        )

    def update(
        self,
        assignment_id: UUID,
        data: ReadingAssignmentUpdate,
    ) -> ReadingAssignmentResponse:

        assignment = self.assignment_repo.get_by_id(
            assignment_id
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found.",
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if (
            "classroom_id" in update_data
            and update_data["classroom_id"] is not None
        ):

            classroom = self.db.get(
                Classroom,
                update_data["classroom_id"],
            )

            if classroom is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Classroom not found.",
                )

        for key, value in update_data.items():
            setattr(
                assignment,
                key,
                value,
            )

        assignment = self.assignment_repo.update(
            assignment
        )

        self.db.commit()
        assignment = self.assignment_repo.get_by_id(
            assignment.id
        )

        return self._to_response(
            assignment
        )

    def delete(
        self,
        assignment_id: UUID,
    ) -> None:

        assignment = self.assignment_repo.get_by_id(
            assignment_id
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found.",
            )

        self.assignment_repo.delete(
            assignment
        )

        self.db.commit()
        return True