from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ==========================
    # Application
    # ==========================
    APP_NAME: str = "Reading Assessment API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # ==========================
    # PostgreSQL
    # ==========================
    DATABASE_URL: str

    # ==========================
    # JWT
    # ==========================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==========================
    # MinIO
    # ==========================
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool = False
    MAX_AUDIO_SIZE_MB: int = 25
    MINIO_BUCKET: str

    ALLOWED_AUDIO_TYPES: list[str] = [
        "audio/wav",
        "audio/mpeg",
        "audio/webm",
        "audio/mp4",
        "audio/ogg",
        "audio/x-wav",
        "audio/x-m4a",
    ]
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()