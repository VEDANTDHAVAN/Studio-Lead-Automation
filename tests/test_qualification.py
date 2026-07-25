from app.models.lead import Budget, LeadExtraction
from app.models.qualification import LeadStatus
from app.services.qualification_service import QualificationService


def test_qualified_lead():
    lead = LeadExtraction(
        company="Lakme",
        contact_name="John",
        contact_email="john@acme.com",
        project_type="Website",
        deliverables=["Website"],
        budget=Budget(
            min=15000,
            max=15000,
            currency="USD",
        ),
        deadline="October",
        urgency="High",
        missing_fields=[],
        summary="Test",
    )

    result = QualificationService().evaluate(lead)

    assert result.status == LeadStatus.QUALIFIED
    assert result.score >= 80

def test_needs_review():
    lead = LeadExtraction(
        company="Acme",
        contact_name=None,
        contact_email="john@acme.com",
        project_type="Website",
        deliverables=[],
        budget=Budget(
            min=6000,
            max=6000,
            currency="USD",
        ),
        deadline=None,
        urgency=None,
        missing_fields=[],
        summary="Test",
    )

    result = QualificationService().evaluate(lead)

    assert result.score == 50
    assert result.status == LeadStatus.NEEDS_REVIEW

def test_declined():
    lead = LeadExtraction(
        company="Acme",
        contact_name=None,
        contact_email=None,
        project_type=None,
        deliverables=[],
        budget=Budget(max=None),
        deadline=None,
        urgency=None,
        missing_fields=[],
        summary="Test",
    )

    result = QualificationService().evaluate(lead)

    assert result.status == LeadStatus.DECLINED