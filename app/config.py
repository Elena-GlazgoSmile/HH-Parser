from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "HeadHunter Parser"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./vacancies.db"
    
    NATS_URL: str = "nats://localhost:4222"
    NATS_SUBJECT: str = "vacancies.updates"
    
    HH_API_URL: str = "https://api.hh.ru/vacancies"
    BACKGROUND_TASK_INTERVAL: int = 600
    
    DEBUG: bool = False
    
    REDIS_URL: Optional[str] = None
    
    S3_ENDPOINT_URL: Optional[str] = None
    S3_BUCKET_NAME: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    WORKERS: int = 1
    LOG_LEVEL: str = "info"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()