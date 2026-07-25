from fastapi import APIRouter

from app.models.request import EmailRequest
from app.services.extraction_service import ExtractionService

router = APIRouter()

service = ExtractionService()


@router.post("/analyze")
def analyze(request: EmailRequest):
    result = service.analyze(request.email_text)

    return result