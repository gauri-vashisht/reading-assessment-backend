from fastapi import FastAPI

from app.core.config import settings
from app.exceptions.handlers import global_exception_handler



app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)


@app.get("/")
def root():

    return {
        "status": "Running"
    }

from app.api.health import router as health_router
app.include_router(health_router)

from contextlib import asynccontextmanager
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Reading Assessment API started")
    yield
    logger.info("Reading Assessment API stopped")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

from app.api.auth import router as auth_router
app.include_router(auth_router)
