from uuid import UUID

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.assessment_response import (
    AssessmentResponse,
)

from app.services.assessment_service import (
    AssessmentService,
)

from app.services.feedback_service import (
    feedback_service,
)

router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


@router.post(
    "/{recording_id}",
    response_model=AssessmentResponse,
)
def assess_audio(
    recording_id: UUID,
    db: Session = Depends(get_db),
):

    service = AssessmentService(db)

    assessment,comparison = service.assess(
        recording_id,
    )

    return AssessmentResponse(

        **assessment.__dict__,
        word_results=comparison["word_results"],
        reading_level=feedback_service.reading_level(
            assessment.words_per_minute,
        ),

        teacher_feedback=feedback_service.teacher_feedback(
            assessment.accuracy_percentage,
            assessment.skipped_words,
            assessment.incorrect_words,
            assessment.extra_words,
        ),

        student_feedback=feedback_service.student_feedback(
            assessment.accuracy_percentage,
            assessment.skipped_words,
            assessment.incorrect_words,
        ),

        summary=feedback_service.summary(
            assessment.correct_words,
            assessment.total_words,
            assessment.words_per_minute,
            assessment.accuracy_percentage,
        ),

    )