from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment_result import AssessmentResult


class AssessmentResultRepository:

    def create(
        self,
        db: Session,
        assessment: AssessmentResult,
    ) -> AssessmentResult:

        db.add(assessment)
        db.flush()
        db.refresh(assessment)
        return assessment

    def get_by_id(
        self,
        db: Session,
        assessment_id: UUID,
    ) -> AssessmentResult | None:

        return db.get(
            AssessmentResult,
            assessment_id,
        )

    def get_by_recording(
        self,
        db: Session,
        recording_id: UUID,
    ) -> AssessmentResult | None:

        stmt = select(AssessmentResult).where(
            AssessmentResult.recording_id == recording_id
        )

        return db.scalar(stmt)

    def list_by_student(
        self,
        db: Session,
        student_profile_id: UUID,
    ) -> list[AssessmentResult]:

        stmt = (
            select(AssessmentResult)
            .where(
                AssessmentResult.student_profile_id == student_profile_id
            )
            .order_by(
                AssessmentResult.created_at.desc()
            )
        )

        return list(db.scalars(stmt).all())

    def update(
        self,
        db: Session,
        assessment: AssessmentResult,
    ) -> AssessmentResult:

        db.add(assessment)
        db.flush()
        db.refresh(assessment)
        return assessment

    def delete(
        self,
        db: Session,
        assessment: AssessmentResult,
    ) -> None:

        db.delete(assessment)