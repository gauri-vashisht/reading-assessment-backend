from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.core.config import settings
from app.api.schools import router as school_router
from app.api.academic_years import (
    router as academic_year_router,
)
from app.api.classrooms import router as classroom_router
from app.api.teacher_profiles import (
    router as teacher_profile_router,
)
from app.api.student_profiles import (
    router as student_profile_router,
)
from app.api.reading_passage import router as reading_passage_router
from app.api.reading_assignment import router as reading_assignment_router
from app.api.student_assignment import (
    router as student_assignment_router,
)
from app.api.audio_recordings import (
    router as audio_recording_router,
)
from app.core.minio import ensure_bucket_exists
from app.api.assessments import router as assessment_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Reading Assessment API started")
    
    ensure_bucket_exists()
    yield
    logger.info("Reading Assessment API stopped")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.include_router(
    assessment_router
)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(school_router)
app.include_router(
    academic_year_router
)
app.include_router(classroom_router)
app.include_router(
    teacher_profile_router,
)
app.include_router(
    student_profile_router,
)
app.include_router(reading_passage_router)
app.include_router(reading_assignment_router)
app.include_router(
    student_assignment_router,
)
app.include_router(
    audio_recording_router
)

@app.get("/", tags=["Root"])
def root():
    return {
        "status": "Running",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }

from app.exceptions.auth import AuthenticationException
from app.exceptions.handlers import (
    authentication_exception_handler,
    global_exception_handler,
)
app.add_exception_handler(
    AuthenticationException,
    authentication_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)



