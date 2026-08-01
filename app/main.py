import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.api.lead_routes import router as lead_router

from app.core.config import get_settings
from app.workflow.gmail_pipeline import GmailPipeline
from app.database.init_db import *

logger = logging.getLogger(__name__)

settings = get_settings()

gmail_pipeline = GmailPipeline()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Gmail worker...")

    task = asyncio.create_task(
        asyncio.to_thread(
            gmail_pipeline.start, settings.gmail_poll_interval,
        )
    )

    yield

    logger.info("Stopping Gmail worker...")

    task.cancel()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0", lifespan=lifespan,
)

app.include_router(router)
app.include_router(lead_router)

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
        "gmail_worker": "running",
    }