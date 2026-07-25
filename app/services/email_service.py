from openai import OpenAI

from app.core.config import get_settings
from app.models.lead import LeadExtraction
from app.models.qualification import LeadQualification, LeadStatus
from app.prompts.reply_prompt import DECLINE_PROMPT, QUALIFIED_PROMPT, REVIEW_PROMPT

settings = get_settings()

client = OpenAI(
    api_key=settings.groq_api_key,
    base_url=settings.groq_base_url,
)

class EmailService:
    def generate(
        self,
        lead: LeadExtraction,
        qualification: LeadQualification,
    ) -> str:

        if qualification.status == LeadStatus.QUALIFIED:
            instructions = QUALIFIED_PROMPT

        elif qualification.status == LeadStatus.NEEDS_REVIEW:
            instructions = REVIEW_PROMPT

        else:
            instructions = DECLINE_PROMPT

        response = client.responses.create(
            model=settings.llm_model,
            instructions=instructions,
            input=lead.model_dump_json(indent=2),
        )

        return response.output_text.strip()