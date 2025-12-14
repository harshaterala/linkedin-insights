from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Use db:5432 for Docker-to-Docker communication
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/linkedin_insights"
    
    # Application
    APP_NAME: str = "LinkedIn Insights Microservice"
    DEBUG: bool = True  # Enable debug for better error messages
    API_V1_PREFIX: str = "/api/v1"
    
    # LinkedIn API settings
    LINKEDIN_API_KEY: Optional[str] = None
    LINKEDIN_API_SECRET: Optional[str] = None
    PROXY_SERVER: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
