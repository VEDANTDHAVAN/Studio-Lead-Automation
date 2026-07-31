from app.models.lead import LeadExtraction
from app.services.llm_service import LLMService

class ExtractionService:
    def __init__(self):
        self.llm = LLMService()

    def analyze(self, email: str):
        data = self.llm.extract(email)

        if not data.get("is_lead", True):
            return LeadExtraction(
                is_lead=False, reason=data.get("reason"),
            )

        return LeadExtraction.model_validate(data)