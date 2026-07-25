import json

from openai import OpenAI

from app.core.config import get_settings
from app.prompts.extract_prompt import EXTRACTION_PROMPT

settings = get_settings()

client = OpenAI(
    api_key=settings.groq_api_key,
    base_url=settings.groq_base_url,
)


class LLMService:
    def extract(self, prompt: str) -> dict:
        response = client.responses.create(
            model=settings.llm_model,
            instructions=EXTRACTION_PROMPT,
            input=prompt,
        )

        text = response.output_text.strip()

        return json.loads(text)