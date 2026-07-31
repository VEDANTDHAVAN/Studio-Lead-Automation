from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "Studio Lead Automation"
    debug: bool = True

    groq_api_key: str
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "qwen/qwen3-32b"

    slack_webhook_url: str = ""
    google_sheet_id: str = ""

    google_sheet_name: str
    google_service_account: str

    email_address: str = ""
    email_password: str = ""

    gmail_credentials_file: str = "credentials.json"
    gmail_token_file: str = "token.json"


@lru_cache
def get_settings() -> Settings:
    return Settings() # pyright: ignore[reportCallIssue]