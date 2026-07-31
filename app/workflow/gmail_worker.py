import time
import logging

from .gmail_pipeline import GmailPipeline
from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

class GmailWorker:
    def __init__(self):
        self.pipeline = GmailPipeline()

    def run(self):
        
        while True:
            try:
                self.pipeline.process_once()

            except Exception:
                logger.exception("Worker failed.")

            except KeyboardInterrupt:
                logger.info("Stopping Gmail Worker...")

            time.sleep(
                settings.gmail_poll_interval
            )