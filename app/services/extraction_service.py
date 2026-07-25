from app.models.lead import LeadExtraction
from app.services.llm_service import LLMService

class ExtractionService:
    def __init__(self):
        self.llm = LLMService()

    def analyze(self, email: str):
        data = self.llm.extract(email)

        return LeadExtraction.model_validate(data)