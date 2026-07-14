import time
import whisper
from app.core.config import settings

class WhisperService:

    def __init__(self):
        self.model = None

    def _get_model(self):
        if self.model is None:
            self.model = whisper.load_model(
                settings.WHISPER_MODEL
            )
        return self.model

    def transcribe_audio(
        self,
        audio_path: str,
    ) -> dict:

        start = time.time()
        model = self._get_model()

        result = model.transcribe(
            audio_path,
            language="en",
        )

        end = time.time()

        return {
            "transcript": result["text"].strip(),
            "language": result["language"],
            "processing_time_seconds": round(end - start, 2),
        }


whisper_service = WhisperService()