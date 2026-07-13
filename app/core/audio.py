from __future__ import annotations

import subprocess
from pathlib import Path


def get_audio_duration(file_path: str) -> int | None:
    """
    Returns duration in seconds using ffprobe.
    Returns None if duration cannot be determined.
    """

    try:

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return round(float(result.stdout.strip()))

    except Exception:
        return None