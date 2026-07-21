from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Career Copilot"
    debug: bool = False
    env: str = "dev"

    # Database
    database_url: str = "sqlite:///./career_copilot.db"

    # AI
    ai_key: str = ""

    # Authentication
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    database_connect_timeout_seconds: int = 5
    request_timeout_seconds: int = 30

    # AI reliability and cost controls
    ai_model: str = "gemini-2.5-flash"
    ai_timeout_seconds: int = 30
    ai_daily_requests_per_user: int = 30
    ai_cache_ttl_seconds: int = 24 * 60 * 60
    prompt_version: str = "2026-07-21"

    # Supabase
    supabase_key: str = ""
    supabase_url: str = ""
    storage_key_public: str = ""
    storage_key_secret: str = ""
    supabase_bucket: str = "resumes"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    max_upload_bytes: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.env.lower() in {"production", "prod"}:
            if self.secret_key == "change-me-in-production" or len(self.secret_key) < 32:
                raise ValueError("SECRET_KEY must be at least 32 characters in production")
            if self.debug:
                raise ValueError("DEBUG must be false in production")
        return self


settings = Settings()
