from app.models.lead import LeadExtraction
from app.services.llm_service import LLMService
from app.services.qualification_service import QualificationService
from app.integrations.sheets import GoogleSheetsClient
from app.integrations.slack import SlackClient

class ExtractionService:
    def __init__(self):
        self.llm = LLMService()
        self.qualifier = QualificationService()
        self.sheets = GoogleSheetsClient()
        self.slack = SlackClient()

    def analyze(self, email: str):
        data = self.llm.extract(email)
        lead = LeadExtraction.model_validate(data) 
        qualification = self.qualifier.evaluate(lead)
        self.sheets.append(lead, qualification)
        self.slack.notify(lead, qualification)

        return {
            "lead": lead.model_dump(),
            "qualification": qualification.model_dump(),
        }