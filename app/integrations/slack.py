import httpx

from app.core.config import get_settings
from app.models.lead import LeadExtraction
from app.models.qualification import LeadQualification

settings = get_settings()


class SlackClient:
    def notify(
        self,
        lead: LeadExtraction,
        qualification: LeadQualification,
    ) -> None:
        message = f"""
🚀 *New Lead Received*

*Company:* {lead.company or "Unknown"}

*Project:* {lead.project_type or "Unknown"}

*Budget:* {
    f"${lead.budget.min:,}"
    if lead.budget and lead.budget.min
    else "Not specified"
}

*Deadline:* {lead.deadline or "Not specified"}

*Score:* {qualification.score}

*Status:* {qualification.status.value.upper()}

*Summary:*
{lead.summary}
"""

        with httpx.Client(timeout=10) as client:
            response = client.post(
                settings.slack_webhook_url,
                json={"text": message},
            )

            response.raise_for_status()