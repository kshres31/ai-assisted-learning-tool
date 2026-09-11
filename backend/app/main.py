from fastapi import FastAPI

from app.api.assistance import router as assistance_router
from app.api.exercises import router as exercises_router
from app.api.health import router as health_router
from app.api.sessions import router as sessions_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="AI-Assisted Learning Tool API",
        version="0.1.0",
        description="Local-first coding exercises with deliberately staged assistance.",
    )
    application.include_router(health_router, prefix="/api")
    application.include_router(exercises_router, prefix="/api")
    application.include_router(assistance_router, prefix="/api")
    application.include_router(sessions_router, prefix="/api")
    return application


app = create_app()
