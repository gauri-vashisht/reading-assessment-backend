from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AudioRecordingResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    assignment_id: UUID

    student_profile_id: UUID

    original_filename: str

    content_type: str

    file_size_bytes: int

    duration_seconds: int | None

    uploaded_at: datetime

    created_at: datetime

    updated_at: datetime


class AudioRecordingListResponse(BaseModel):

    items: list[AudioRecordingResponse]

    total: int


class DownloadUrlResponse(BaseModel):

    download_url: str