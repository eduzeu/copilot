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

    storage_key_public: str = ""
    storage_key_secret: str = ""
    storage_url: str = ""
    
    class Config: 
        env_file = '.env' 
    
settings = Settings()


