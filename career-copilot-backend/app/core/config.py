from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Career Copilot"
    debug: bool = False
    database_url: str = "sqlite:///./career_copilot.db"
    AI_KEY: str = ""
    env: str = 'dev'
    SECRET_KEY: str 
    access_token_expire_minutes: int = 30

    STORAGE_KEY_PUBLIC: str = ""
    STORAGE_KEY_SECRET: str = ""
    SUPABASE_BUCKET: str = 'resumes'
    
    class Config: 
        env_file = '.env' 
    
settings = Settings()


