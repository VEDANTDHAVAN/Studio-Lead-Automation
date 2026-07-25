from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "status": "running",
        "application": settings.app_name,
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }