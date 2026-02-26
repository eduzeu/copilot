from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Career Copilot"
    debug: bool = False
    database_url: str = "sqlite:///./career_copilot.db"
    openai_api_key: str = ""
    env: str = 'dev'
    access_token_expire_minutes: int = 30

    class Config: 
        env_file = '.env' 
    
settings = Settings()


