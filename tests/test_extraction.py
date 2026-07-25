from unittest.mock import MagicMock
from typing import Optional

from app.models.lead import LeadExtraction, Budget
from app.services.extraction_service import ExtractionService


def test_extraction():
    service = ExtractionService()

    service.llm.extract = MagicMock(
        return_value={
            "company": "Lakme",
            "contact_name": "John",
            "contact_email": "john@acme.com",
            "project_type": "Website",
            "deliverables": [],
            "budget": Budget(
        min=6000,
        max=6000,
        currency="USD",
    ),
            "deadline": None,
            "urgency": None,
            "missing_fields": [],
            "summary": "Test",
        }
    )

    lead = service.analyze("email")

    assert isinstance(lead, LeadExtraction)
    assert lead.company == "Lakme"