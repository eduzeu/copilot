from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Career Copilot"
    debug: bool = False
    env: str = "dev"

    # Database
    database_url: str = "sqlite:///./career_copilot.db"

    # AI
    AI_KEY: str = ""

    # Authentication
    SECRET_KEY: str
    access_token_expire_minutes: int = 30

    # Supabase
    SUPABASE_KEY: str = ""
    SUPABASE_URL: str = ""
    STORAGE_KEY_PUBLIC: str = ""
    STORAGE_KEY_SECRET: str = ""
    SUPABASE_BUCKET: str = "resumes"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()