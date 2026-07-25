from fastapi import APIRouter

from app.models.request import EmailRequest
from app.workflow.lead_pipeline import LeadPipeline

router = APIRouter()

pipeline = LeadPipeline()


@router.post("/analyze")
def analyze(request: EmailRequest):
    result = pipeline.run(request.email_text)

    return result