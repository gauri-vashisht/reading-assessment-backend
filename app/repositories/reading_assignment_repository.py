from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from app.models.reading_assignment import ReadingAssignment
from app.models.student_assignment import StudentAssignment
from app.models.user import User
class ReadingAssignmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        assignment: ReadingAssignment,
    ) -> ReadingAssignment:

        self.db.add(assignment)
        self.db.flush()
        self.db.refresh(assignment)

        return assignment

    def get_by_id(
        self,
        assignment_id: UUID,
    ) -> ReadingAssignment | None:

        result = self.db.execute(
            select(ReadingAssignment)
            .options(
                joinedload(ReadingAssignment.passage),
                joinedload(ReadingAssignment.classroom),
                joinedload(
                    ReadingAssignment.student_assignments
                ).joinedload(
                    StudentAssignment.student
                ),
            )
            .where(
                ReadingAssignment.id == assignment_id
            )
        )

        return result.unique().scalar_one_or_none()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[ReadingAssignment], int]:

        total = self.db.scalar(
            select(func.count()).select_from(
                ReadingAssignment
            )
        )

        result = self.db.execute(
            select(ReadingAssignment)
            .options(
                joinedload(
                    ReadingAssignment.passage
                ),
                joinedload(
                    ReadingAssignment.classroom
                ),
                joinedload(
                    ReadingAssignment.student_assignments
                ).joinedload(
                    StudentAssignment.student
                ),
            )
            .order_by(
                ReadingAssignment.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        assignments = result.unique().scalars().all()

        return assignments, total

    def update(
        self,
        assignment: ReadingAssignment,
    ) -> ReadingAssignment:

        self.db.flush()
        self.db.refresh(assignment)

        return assignment

    def delete(
        self,
        assignment: ReadingAssignment,
    ):

        self.db.delete(assignment)


    def commit(self):
        self.db.commit()