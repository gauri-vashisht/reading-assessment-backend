from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student_assignment import StudentAssignment
from sqlalchemy.orm import joinedload


from app.models.reading_assignment import ReadingAssignment

class StudentAssignmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        assignment: StudentAssignment,
    ) -> StudentAssignment:

        self.db.add(assignment)
        return assignment

    def bulk_create(
        self,
        assignments: list[StudentAssignment],
    ):

        self.db.add_all(assignments)

    def get_by_student(
        self,
        student_id: UUID,
    ) -> list[StudentAssignment]:

        return (
            self.db.scalars(
                select(StudentAssignment)
                .where(
                    StudentAssignment.student_id == student_id
                )
                .order_by(
                    StudentAssignment.created_at.desc()
                )
            )
            .all()
        )

    def get_by_id(
        self,
        student_assignment_id: UUID,
    ) -> StudentAssignment | None:

        return self.db.scalar(
            select(StudentAssignment).where(
                StudentAssignment.id == student_assignment_id
            )
        )

    def update(
        self,
        assignment: StudentAssignment,
    ):

        self.db.flush()
        self.db.refresh(assignment)

        return assignment
    
    def commit(self):
        self.db.commit()

    def get_by_student(self, student_id):
        return (
            self.db.query(StudentAssignment)
            .options(
                joinedload(StudentAssignment.assignment)
                .joinedload(ReadingAssignment.passage)
            )
            .filter(StudentAssignment.student_id == student_id)
            .all()
        )