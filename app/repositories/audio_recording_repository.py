from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audio_recording import AudioRecording
from app.repositories.base_repository import BaseRepository


class AudioRecordingRepository(
    BaseRepository[AudioRecording]
):

    def __init__(self):
        super().__init__(AudioRecording)

    def get_by_storage_key(
        self,
        db: Session,
        storage_key: str,
    ) -> AudioRecording | None:

        stmt = select(AudioRecording).where(
            AudioRecording.storage_key == storage_key
        )

        return db.scalar(stmt)

    def get_by_assignment(
        self,
        db: Session,
        assignment_id,
    ) -> list[AudioRecording]:

        stmt = (
            select(AudioRecording)
            .where(
                AudioRecording.assignment_id
                == assignment_id
            )
            .order_by(
                AudioRecording.created_at.desc()
            )
        )

        return list(
            db.scalars(stmt)
        )

    def get_by_student(
        self,
        db: Session,
        student_profile_id,
    ) -> list[AudioRecording]:

        stmt = (
            select(AudioRecording)
            .where(
                AudioRecording.student_profile_id
                == student_profile_id
            )
            .order_by(
                AudioRecording.created_at.desc()
            )
        )

        return list(
            db.scalars(stmt)
        )


audio_recording_repository = AudioRecordingRepository()