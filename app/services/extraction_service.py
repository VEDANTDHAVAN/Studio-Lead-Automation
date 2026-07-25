from app.models.lead import LeadExtraction
from app.services.llm_service import LLMService
from app.services.qualification_service import QualificationService
from app.integrations.sheets import GoogleSheetsClient
from app.integrations.slack import SlackClient
from app.services.email_service import EmailService

class ExtractionService:
    def __init__(self):
        self.llm = LLMService()
        self.qualifier = QualificationService()
        self.sheets = GoogleSheetsClient()
        self.slack = SlackClient()
        self.email = EmailService()

    def analyze(self, email: str):
        data = self.llm.extract(email)
        lead = LeadExtraction.model_validate(data) 
        qualification = self.qualifier.evaluate(lead)
        self.sheets.append(lead, qualification)
        self.slack.notify(lead, qualification)
        reply = self.email.generate(lead, qualification)

        return {
            "lead": lead.model_dump(),
            "qualification": qualification.model_dump(),
            "reply_email": reply,
        }