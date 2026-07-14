from __future__ import annotations

import os
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.storage import storage_service

from app.models.assessment_result import (
    AssessmentResult,
    AssessmentStatus,
)

from app.repositories.assessment_result_repository import (
    AssessmentResultRepository,
)

from app.repositories.audio_recording_repository import (
    audio_recording_repository,
)

from app.repositories.reading_assignment_repository import (
    ReadingAssignmentRepository,
)

from app.services.metrics_service import (
    metrics_service,
)

from app.services.text_comparison_service import (
    text_comparison_service,
)

from app.services.whisper_service import (
    whisper_service,
)


class AssessmentService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.assignment_repo = (
            ReadingAssignmentRepository(db)
        )

        self.audio_repo = (
            audio_recording_repository
        )

        self.assessment_repo = (
            AssessmentResultRepository()
        )

    def assess(
        self,
        recording_id: UUID,
    ) -> AssessmentResult:

        recording = self.audio_repo.get_by_id(
            self.db,
            recording_id,
        )

        if recording is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recording not found.",
            )

        assignment = (
            self.assignment_repo.get_by_id(
                recording.assignment_id,
            )
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found.",
            )

        assessment = (
            self.assessment_repo.get_by_recording(
                self.db,
                recording.id,
            )
        )

        if assessment is None:

            assessment = AssessmentResult(

                recording_id=recording.id,

                assignment_id=recording.assignment_id,

                student_profile_id=recording.student_profile_id,

                status=AssessmentStatus.PROCESSING,

            )

            assessment = (
                self.assessment_repo.create(
                    self.db,
                    assessment,
                )
            )

        audio_path = (
            storage_service.download_audio_to_temp(
                bucket_name=recording.bucket_name,
                storage_key=recording.storage_key,
            )
        )

        try:

            whisper_result = (
                whisper_service.transcribe_audio(
                    audio_path,
                )
            )

        finally:

            if os.path.exists(audio_path):
                os.remove(audio_path)

        comparison = (
            text_comparison_service.compare(

                assignment.passage.passage,

                whisper_result["transcript"],

            )
        )

        metrics = (
            metrics_service.build_metrics(

                comparison,

                recording.duration_seconds
                or 0,

            )
        )

        assessment.transcript = (
            whisper_result["transcript"]
        )

        assessment.total_words = (
            metrics["total_words"]
        )

        assessment.correct_words = (
            metrics["correct_words"]
        )

        assessment.incorrect_words = (
            metrics["incorrect_words"]
        )

        assessment.skipped_words = (
            metrics["skipped_words"]
        )

        assessment.extra_words = (
            metrics["extra_words"]
        )

        assessment.incorrect_word_list = (
            metrics["incorrect_word_list"]
        )

        assessment.skipped_word_list = (
            metrics["skipped_word_list"]
        )

        assessment.extra_word_list = (
            metrics["extra_word_list"]
        )

        assessment.accuracy_percentage = (
            metrics["accuracy_percentage"]
        )

        assessment.words_per_minute = (
            metrics["words_per_minute"]
        )

        assessment.processing_time_seconds = (
            whisper_result[
                "processing_time_seconds"
            ]
        )

        assessment.status = (
            AssessmentStatus.COMPLETED
        )

        self.assessment_repo.update(
            self.db,
            assessment,
        )

        self.db.commit()

        self.db.refresh(
            assessment,
        )

        return assessment