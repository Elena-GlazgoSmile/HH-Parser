from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "HeadHunter Parser"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./vacancies.db"
    
    NATS_URL: str = "nats://localhost:4222"
    NATS_SUBJECT: str = "vacancies.updates"
    
    HH_API_URL: str = "https://api.hh.ru/vacancies"
    
    BACKGROUND_TASK_INTERVAL: int = 600
    
    class Config:
        env_file = ".env"

settings = Settings()
