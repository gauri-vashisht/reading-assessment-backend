from .reading_assignment import router as reading_assignment_router

api_router.include_router(
    reading_assignment_router
)