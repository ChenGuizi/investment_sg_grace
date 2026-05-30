from functools import lru_cache

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Singapore Stock Intelligence"
    environment: str = "development"
    database_url: str = "sqlite:///./stockintel.db"
    jwt_secret: str = "change-me"
    web_app_url: AnyHttpUrl | str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    market_data_provider: str = "demo"
    news_provider: str = "demo"
    sendgrid_api_key: str | None = None
    gmail_client_id: str | None = None
    gmail_client_secret: str | None = None
    gmail_refresh_token: str | None = None
    email_from: str = "reports@example.com"
    daily_report_hour_sgt: int = Field(default=7, ge=0, le=23)

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
