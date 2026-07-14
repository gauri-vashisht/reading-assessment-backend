from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.assessment_result import (
    AssessmentResultResponse,
)

from app.services.assessment_service import (
    AssessmentService,
)

router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


@router.post(
    "/{recording_id}",
    response_model=AssessmentResultResponse,
)
def assess_audio(
    recording_id: UUID,
    db: Session = Depends(get_db),
):

    service = AssessmentService(db)

    return service.assess(
        recording_id,
    )