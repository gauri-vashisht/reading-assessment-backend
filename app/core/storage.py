from __future__ import annotations

import hashlib
import os
import tempfile
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from minio.error import S3Error

from app.core.audio import get_audio_duration
from app.core.config import settings
from app.core.minio import minio_client
from loguru import logger
from minio.error import S3Error



class StorageService:

    def download_audio_to_temp(
        self,
        *,
        bucket_name: str,
        storage_key: str,
    ) -> str:

        suffix = Path(storage_key).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_path = temp_file.name

        try:

            minio_client.fget_object(
                bucket_name=bucket_name,
                object_name=storage_key,
                file_path=temp_path,
            )

            return temp_path

        except S3Error as exc:

            Path(temp_path).unlink(
                missing_ok=True,
            )

            raise HTTPException(
                status_code=500,
                detail=str(exc),
            )
    def upload_audio(
        self,
        *,
        file: UploadFile,
        student_profile_id: str,
        assignment_id: str,
    ) -> dict:

        if file.content_type not in settings.ALLOWED_AUDIO_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Unsupported audio format.",
            )

        extension = Path(
            file.filename
        ).suffix.lower()

        sha256 = hashlib.sha256()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:

            total_size = 0

            while True:

                chunk = file.file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                total_size += len(chunk)

                if (
                    total_size
                    > settings.MAX_AUDIO_SIZE_MB
                    * 1024
                    * 1024
                ):
                    raise HTTPException(
                        status_code=413,
                        detail="Audio exceeds maximum size.",
                    )

                sha256.update(chunk)

                temp_file.write(chunk)

        checksum = sha256.hexdigest()

        duration = get_audio_duration(
            temp_file.name
        )

        storage_key = (
            f"audio/"
            f"{student_profile_id}/"
            f"{assignment_id}/"
            f"{uuid4()}{extension}"
        )

        try:

            with open(
                temp_file.name,
                "rb",
            ) as stream:

                minio_client.put_object(
                    bucket_name=settings.MINIO_BUCKET,
                    object_name=storage_key,
                    data=stream,
                    length=os.path.getsize(
                        temp_file.name
                    ),
                    content_type=file.content_type,
                )

        except S3Error as exc:

            raise HTTPException(
                status_code=500,
                detail=str(exc),
            )

        finally:

            Path(
                temp_file.name
            ).unlink(
                missing_ok=True,
            )

        return {

            "bucket_name":
                settings.MINIO_BUCKET,

            "storage_key":
                storage_key,

            "original_filename":
                file.filename,

            "content_type":
                file.content_type,

            "file_size_bytes":
                total_size,

            "checksum":
                checksum,

            "duration_seconds":
                duration,
        }



    def delete_audio(
        self,
        *,
        bucket_name: str,
        storage_key: str,
    ) -> None:

        try:
            minio_client.remove_object(
                bucket_name=bucket_name,
                object_name=storage_key,
            )

            logger.info(
                "Deleted MinIO object: {}",
                storage_key,
            )

        except S3Error as exc:
            logger.exception(
                "Failed to delete MinIO object: {}",
                exc,
            )
            raise

    def generate_download_url(
        self,
        *,
        bucket_name: str,
        storage_key: str,
    ):

        return minio_client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=storage_key,
            expires=timedelta(
                minutes=5,
            ),
        )


storage_service = StorageService()