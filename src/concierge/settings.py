from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings."""

    APP_NAME: str = "Concierge Service"

    # AGENT_MODEL: str = "gpt-4o-mini"
    AGENT_MODEL: str = "gpt-5.1"
    OPENAI_API_KEY: str = Field(..., min_length=1, description="OpenAI API key is required")

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate that the API key is not empty and has a reasonable format."""
        if not v or v.strip() == "":
            msg = "OPENAI_API_KEY must be set. Please add it to your .env file or environment variables."
            raise ValueError(msg)
        if not v.startswith("sk-"):
            msg = "OPENAI_API_KEY appears to be invalid. OpenAI API keys should start with 'sk-'."
            raise ValueError(msg)
        return v


settings = AppSettings()
