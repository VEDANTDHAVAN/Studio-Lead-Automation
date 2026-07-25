from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from app.core.config import get_settings
from app.models.lead import LeadExtraction
from app.models.qualification import LeadQualification

settings = get_settings()


class GoogleSheetsClient:
    def __init__(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials = Credentials.from_service_account_file(
            settings.google_service_account,
            scopes=scopes,
        )

        client = gspread.authorize(credentials)

        self.sheet = client.open(settings.google_sheet_name).sheet1

    def append(
        self,
        lead: LeadExtraction,
        qualification: LeadQualification,
    ):
        self.sheet.append_row(
            [
                datetime.utcnow().isoformat(),

                lead.company or "",
                lead.contact_name or "",
                lead.contact_email or "",

                lead.project_type or "",

                lead.budget.min if lead.budget and lead.budget.min is not None else "",
                lead.budget.max if lead.budget and lead.budget.max is not None else "",
                lead.budget.currency if lead.budget and lead.budget.currency else "",

                lead.deadline or "",

                qualification.score,
                qualification.status.value,

                lead.summary,
            ]
        )