from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
    status,
)

from app.dependencies.auth import (
    get_current_user,
    require_student,
)
from app.dependencies.database import DBSession

from app.models.user import User

from app.schemas.audio_recording import (
    AudioRecordingListResponse,
    AudioRecordingResponse,
    DownloadUrlResponse,
)

from app.services.audio_recording_service import (
    AudioRecordingService,
)

router = APIRouter(
    prefix="/audio-recordings",
    tags=["Audio Recordings"],
)


@router.post(
    "/upload/{assignment_id}",
    response_model=AudioRecordingResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_audio(
    assignment_id: UUID,
    db: DBSession,
    file: UploadFile = File(...),
    current_user: User = Depends(require_student),
       
):
    service = AudioRecordingService(db)

    recording = service.upload(
        assignment_id,
        file,
        current_user,
    )

    return AudioRecordingResponse.model_validate(
        recording
    )

@router.get(
    "/{recording_id}/download",
    response_model=DownloadUrlResponse,
)
def download_audio(
    recording_id: UUID,
    db: DBSession,
    current_user: User = Depends(get_current_user),
):
    service = AudioRecordingService(db)

    return DownloadUrlResponse(
        download_url=service.download_url(
            recording_id,
            current_user,
        )
    )


@router.delete(
    "/{recording_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_recording(
    recording_id: UUID,
    db: DBSession,
    current_user: User = Depends(require_student),
):
    service = AudioRecordingService(db)

    service.delete(
        recording_id,
        current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )