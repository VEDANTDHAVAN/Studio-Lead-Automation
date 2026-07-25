from app.core.logger import logger

from app.integrations.sheets import GoogleSheetsClient
from app.integrations.slack import SlackClient
from app.models.lead import LeadExtraction
from app.services.email_service import EmailService
from app.services.extraction_service import ExtractionService
from app.services.qualification_service import QualificationService


class LeadPipeline:
    def __init__(self):
        self.extractor = ExtractionService()
        self.qualifier = QualificationService()

        self.sheets = GoogleSheetsClient()
        self.slack = SlackClient()

        self.email = EmailService()

    def run(self, email: str):
        # 1. Extract
        lead: LeadExtraction = self.extractor.analyze(email)

        # 2. Qualify
        qualification = self.qualifier.evaluate(lead)

        # 3. Persist
        try:
            self.sheets.append(
                lead,
                qualification,
            )
        except Exception as e:
            logger.exception(f"Google Sheets failed: {e}")

        # 4. Notify
        try:
            self.slack.notify(
                lead,
                qualification,
            )
        except Exception as e:
            logger.exception(f"Slack failed: {e}")

        # 5. Generate reply
        reply = self.email.generate(
            lead,
            qualification,
        )

        return {
            "lead": lead.model_dump(),
            "qualification": qualification.model_dump(),
            "reply_email": reply,
        }