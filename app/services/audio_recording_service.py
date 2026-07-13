from uuid import UUID

from fastapi import HTTPException, UploadFile, status

from app.models.audio_recording import AudioRecording
from app.models.student_assignment import StudentAssignment
from app.models.student_profile import StudentProfile
from app.models.user import User
from loguru import logger

from app.enums.assignment_status import AssignmentStatus

from app.repositories.audio_recording_repository import (
    audio_recording_repository,
)
from app.repositories.reading_assignment_repository import (
    ReadingAssignmentRepository,
)
from app.repositories.student_profile_repository import (
    student_profile_repository,
)

from app.core.storage import storage_service

from sqlalchemy.orm import Session
class AudioRecordingService:

    def __init__(self, db: Session,):
        self.db = db

        self.assignment_repo = (
            ReadingAssignmentRepository(db)
        )

        self.audio_repo = (
            audio_recording_repository
        )

    def upload(
        self,
        assignment_id: UUID,
        file: UploadFile,
        current_user: User,
    ):

        assignment = self.assignment_repo.get_by_id(
            assignment_id
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found.",
            )

        student_profile = (
            student_profile_repository.get_by_user(
                self.db,
                current_user.id,
            )
        )

        if student_profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found.",
            )

        student_assignment = (
            self.db.query(StudentAssignment)
            .filter(
                StudentAssignment.assignment_id
                == assignment_id,
                StudentAssignment.student_id
                == current_user.id,
            )
            .first()
        )

        if student_assignment is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assignment does not belong to this student.",
            )

        if (
            student_assignment.status
            == AssignmentStatus.COMPLETED
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Assignment already completed.",
            )

        logger.info(
            "Uploading recording | "
            f"user={current_user.id} "
            f"assignment={assignment.id}"
        )

        metadata = storage_service.upload_audio(
            file=file,
            student_profile_id=str(
                student_profile.id
            ),
            assignment_id=str(
                assignment.id
            ),
        )

        recording = AudioRecording(
            assignment_id=assignment.id,
            student_profile_id=student_profile.id,
            bucket_name=metadata["bucket_name"],
            storage_key=metadata["storage_key"],
            original_filename=metadata[
                "original_filename"
            ],
            content_type=metadata["content_type"],
            file_size_bytes=metadata[
                "file_size_bytes"
            ],
            checksum=metadata["checksum"],
            duration_seconds=metadata.get("duration_seconds"),
        )

        try:

            self.audio_repo.create(
                self.db,
                recording,
            )

            self.db.commit()

            self.db.refresh(
                recording,
            )
            logger.success(
                "Recording Uploaded: {}",
                recording.id,
            )

            return recording

        except Exception as exc:
            
            logger.exception(
                f"Upload transaction failed: {exc}"
            )

            self.db.rollback()

            storage_service.delete_audio(
                bucket_name=metadata[
                    "bucket_name"
                ],
                storage_key=metadata[
                    "storage_key"
                ],
            )

            raise HTTPException(
                status_code=500,
                detail="Unable to Save Recording.",
            )
        

    def delete(
        self,
        recording_id: UUID,
        current_user:User,
    ):

        recording = self.audio_repo.get_by_id(
            self.db,
            recording_id,
        )

        if recording is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recording not found.",
            )
        student_profile=(
            student_profile_repository.get_by_user(
                self.db,
                current_user.id,
            )
        )
        if(
            student_profile is None
            or recording.student_profile_id != student_profile.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied.",
            )
        try:
            storage_service.delete_audio(
                bucket_name=recording.bucket_name,
                storage_key=recording.storage_key,
            )

            self.audio_repo.delete(
                self.db,
                recording,
            )

            self.db.commit()
            logger.info(
                "Recording Deleted: {}",
                recording.id,
            )

            return True
        
        except Exception as exc:
            logger.exception(f"Delete failed: {exc}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete recording.",
            )

    def get_by_id(
        self,
        recording_id: UUID,
    ):

        recording = self.audio_repo.get_by_id(
            self.db,
            recording_id,
        )

        if recording is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recording not found.",
            )

        return recording

    def my_recordings(
        self,
        current_user: User,
    ):

        student_profile = (
            student_profile_repository.get_by_user(
                self.db,
                current_user.id,
            )
        )

        if student_profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student profile not found.",
            )

        return self.audio_repo.get_by_student(
            self.db,
            student_profile.id,
        )

    def download_url(
        self,
        recording_id: UUID,
        current_user: User,
    ):

        recording = self.get_by_id(
            recording_id,
        )
        
        student_profile = (
            student_profile_repository.get_by_user(
                self.db,
                current_user.id,
            )
        )

        if (
            student_profile is None
            or recording.student_profile_id
            != student_profile.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        return storage_service.generate_download_url(
            bucket_name=recording.bucket_name,
            storage_key=recording.storage_key,
        )