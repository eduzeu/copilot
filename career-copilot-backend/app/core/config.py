from pydantic import field_validator
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


settings = Settings()
