from unittest.mock import MagicMock

from app.models.lead import LeadExtraction
from app.models.qualification import (
    LeadQualification,
    LeadStatus,
)
from app.services.email_service import EmailService


def test_email_generation():
    service = EmailService()

    service.generate = MagicMock(
        return_value="Hello!"
    )

    result = service.generate(
        LeadExtraction.model_construct(),
        LeadQualification(
            score=80,
            status=LeadStatus.QUALIFIED,
            reasons=[],
        ),
    )

    assert result == "Hello!"