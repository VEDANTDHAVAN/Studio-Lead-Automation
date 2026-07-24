from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = Field(alias="APP_NAME")
    debug: bool = Field(alias="DEBUG")

    gemini_api_key: str = Field(alias="GEMINI_API_KEY")

    slack_webhook_url: str = Field(alias="SLACK_WEBHOOK_URL")

    google_sheet_id: str = Field(alias="GOOGLE_SHEET_ID")

    email_address: str = Field(alias="EMAIL_ADDRESS")

    email_password: str = Field(alias="EMAIL_PASSWORD")


@lru_cache
def get_settings():
    return Settings()