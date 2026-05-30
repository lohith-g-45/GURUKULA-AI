from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "GURUKULA AI"
    BACKEND_NAME: str = "GURUKULA AI Backend"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    LOG_LEVEL: str = "INFO"
    
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_TEMPERATURE: float = 0.7
    GROQ_MAX_TOKENS: int = 2048
    GROQ_MAX_RETRIES: int = 3
    GROQ_RETRY_DELAY: float = 1.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
