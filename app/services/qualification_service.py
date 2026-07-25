from app.models.lead import LeadExtraction
from app.models.qualification import LeadQualification, LeadStatus


class QualificationService:
    def evaluate(self, lead: LeadExtraction) -> LeadQualification:
        score = 0
        reasons: list[str] = []

        # Budget (40)
        if lead.budget and lead.budget.min is not None:
            if lead.budget.min >= 10000:
                score += 40
                reasons.append("Budget is within target range.")
            elif lead.budget.min >= 5000:
                score += 20
                reasons.append("Budget is acceptable but below ideal.")
            else:
                reasons.append("Budget is below preferred range.")
        else:
            reasons.append("Budget not specified.")

        # Deadline (20)
        if lead.deadline:
            score += 20
            reasons.append("Deadline provided.")
        else:
            reasons.append("Deadline missing.")

        # Project Type (20)
        if lead.project_type:
            score += 20
            reasons.append("Project type identified.")
        else:
            reasons.append("Project type missing.")

        # Contact Name (10)
        if lead.contact_name:
            score += 10
            reasons.append("Contact name available.")
        else:
            reasons.append("Missing contact name.")

        # Contact Email (10)
        if lead.contact_email:
            score += 10
            reasons.append("Contact email available.")
        else:
            reasons.append("Missing contact email.")

        if score >= 80:
            status = LeadStatus.QUALIFIED
        elif score >= 50:
            status = LeadStatus.NEEDS_REVIEW
        else:
            status = LeadStatus.DECLINED

        return LeadQualification(
            score=score,
            status=status,
            reasons=reasons,
        )