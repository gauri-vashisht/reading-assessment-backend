from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.reading_assignment import ReadingAssignment


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

        return self.db.scalar(
            select(ReadingAssignment).where(
                ReadingAssignment.id == assignment_id
            )
        )

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

        assignments = (
            self.db.scalars(
                select(ReadingAssignment)
                .offset(skip)
                .limit(limit)
                .order_by(
                    ReadingAssignment.created_at.desc()
                )
            )
            .all()
        )

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